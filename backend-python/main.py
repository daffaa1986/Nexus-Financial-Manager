from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import os
import sys
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Import dari AI/ML System yang terorganisir
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from ai_ml.data.parser_mutasi import proses_dokumen_mutasi
from ai_ml.analysis.insight_engine import generate_analysis as generate_ai_analysis
from ai_ml.analysis.insight_engine import generate_llm_insights as generate_ai_insights
from ai_ml.analysis.comparison import bandingkan_bulan as generate_monthly_comparison
from ai_ml.ocr.gemini_vision import ocr_struk as ocr_receipt_with_gemini
from ai_ml.ocr.receipt_normalizer import parse_single_receipt, receipt_to_transaction
from db_config import (
    init_db, simpan_transaksi, simpan_receipt,
    ambil_semua_transaksi, ambil_transaksi_per_bulan, ambil_transaksi_per_rentang,
    ambil_semua_receipt, ambil_goals, tambah_goal,
    ambil_budgets, simpan_budget, ambil_ringkasan_bulan, cek_dan_simpan_file_hash
)
from datetime import datetime

init_db()

app = FastAPI(title="Nexus Finance AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_message(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

@app.websocket("/ws/updates")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def proses_mutasi_background(filename: str, file_bytes: bytes, bank: str = None):
    try:
        await manager.send_message({"status": "loading", "message": f"AI sedang mengekstrak {filename}..."})

        data_hasil_ai, detected_bank = await asyncio.to_thread(proses_dokumen_mutasi, file_bytes, bank)

        await manager.send_message({"status": "loading", "message": f"Menyimpan {len(data_hasil_ai)} transaksi dari {detected_bank}..."})
        await asyncio.to_thread(simpan_transaksi, data_hasil_ai, filename, detected_bank)

        await manager.send_message({
            "status": "success",
            "data": {
                "message": f"Berhasil memproses {len(data_hasil_ai)} transaksi dari {detected_bank}!",
                "new_transactions": data_hasil_ai,
                "bank": detected_bank,
                "count": len(data_hasil_ai),
            }
        })
    except Exception as e:
        print(f"Error proses mutasi: {e}")
        await manager.send_message({"status": "error", "data": {"message": f"Gagal memproses: {str(e)}"}})

async def proses_receipt_background(image_bytes: bytes, filename: str = "receipt.jpg"):
    try:
        await manager.send_message({"status": "loading", "message": "OCR sedang membaca struk..."})

        ocr_result = await asyncio.to_thread(ocr_receipt_with_gemini, image_bytes)

        parsed = parse_single_receipt(ocr_result)

        if parsed:
            await manager.send_message({"status": "loading", "message": f"Toko: {parsed['store_name']} - Menyimpan data..."})
            await asyncio.to_thread(simpan_receipt, [parsed], filename)

            trx_format = receipt_to_transaction(parsed)
            await asyncio.to_thread(simpan_transaksi, [trx_format], f"receipt_{filename}", "RECEIPT")
        else:
            await manager.send_message({"status": "error", "data": {"message": "Gagal memproses struk"}})
            return

        await manager.send_message({
            "status": "success",
            "data": {
                "message": f"Struk berhasil diproses! Total: Rp{parsed['total']:,.0f}",
                "receipt": parsed,
            }
        })
    except Exception as e:
        print(f"Error proses receipt: {e}")
        await manager.send_message({"status": "error", "data": {"message": f"Gagal OCR: {str(e)}"}})

@app.post("/api/upload")
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    bank: str = Query(None, description="Bank name (auto-detect if not provided)")
):
    import hashlib
    print(f"Menerima file: {file.filename}")
    file_bytes = await file.read()
    
    # Hitung hash file untuk mendeteksi duplikat isi file (walau nama filenya berbeda)
    file_hash = hashlib.sha256(file_bytes).hexdigest()
    if not cek_dan_simpan_file_hash(file.filename, file_hash):
        return {"status": "duplicate", "message": "File ini sudah pernah diunggah sebelumnya (duplikat)."}

    ext = file.filename.lower().split('.')[-1] if '.' in file.filename else ''

    if ext in ['jpg', 'jpeg', 'png', 'webp']:
        background_tasks.add_task(proses_receipt_background, file_bytes, file.filename)
    else:
        background_tasks.add_task(proses_mutasi_background, file.filename, file_bytes, bank)

    return {"status": "processing", "message": "Memproses di background...", "filename": file.filename}

@app.post("/api/upload-receipt")
async def upload_receipt(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    print(f"Menerima struk: {file.filename}")
    image_bytes = await file.read()
    background_tasks.add_task(proses_receipt_background, image_bytes, file.filename)
    return {"message": "OCR struk diproses di background..."}

@app.get("/api/transactions")
async def get_transactions():
    data_db = ambil_semua_transaksi()
    return {"status": "success", "data": data_db}

@app.get("/api/transactions/month/{bulan}/{tahun}")
async def get_transactions_by_month(bulan: int, tahun: int):
    data = ambil_transaksi_per_bulan(bulan, tahun)
    return {"status": "success", "data": data, "month": bulan, "year": tahun}

@app.get("/api/receipts")
async def get_receipts():
    data = ambil_semua_receipt()
    return {"status": "success", "data": data}

@app.get("/api/insights")
async def get_ai_insights(
    bulan: int = Query(default=datetime.now().month),
    tahun: int = Query(default=datetime.now().year)
):
    transaksi = ambil_transaksi_per_bulan(bulan, tahun)
    receipts = ambil_semua_receipt()

    result = await asyncio.to_thread(generate_ai_analysis, transaksi, receipts)

    return {"status": "success", "data": result}

@app.get("/api/insights/generate")
async def generate_ai_insights_from_data(
    bulan: int = Query(default=datetime.now().month),
    tahun: int = Query(default=datetime.now().year)
):
    transaksi = ambil_transaksi_per_bulan(bulan, tahun)

    if not transaksi:
        return {"status": "success", "data": {"insights": [], "summary": "Belum ada data."}}

    result = await asyncio.to_thread(generate_ai_insights, transaksi)
    return {"status": "success", "data": {"insights": result}}

@app.get("/api/comparison")
async def get_monthly_comparison(
    bulan: int = Query(default=datetime.now().month),
    tahun: int = Query(default=datetime.now().year)
):
    bulan_ini = ambil_transaksi_per_bulan(bulan, tahun)

    bulan_lalu = bulan - 1
    tahun_lalu = tahun
    if bulan_lalu == 0:
        bulan_lalu = 12
        tahun_lalu = tahun - 1

    bulan_lalu_data = ambil_transaksi_per_bulan(bulan_lalu, tahun_lalu)

    result = await asyncio.to_thread(generate_monthly_comparison, bulan_ini, bulan_lalu_data)
    return {"status": "success", "data": result}

@app.get("/api/summary")
async def get_summary(
    bulan: int = Query(default=datetime.now().month),
    tahun: int = Query(default=datetime.now().year)
):
    ringkasan = ambil_ringkasan_bulan(bulan, tahun)
    return {"status": "success", "data": ringkasan}

@app.get("/api/analytics/daily")
async def get_daily_analytics(
    bulan: int = Query(default=datetime.now().month),
    tahun: int = Query(default=datetime.now().year)
):
    transaksi = ambil_transaksi_per_bulan(bulan, tahun)

    daily = {}
    for t in transaksi:
        date = t.get('date', '')
        if date not in daily:
            daily[date] = {'income': 0, 'expense': 0, 'count': 0, 'transactions': []}

        tipe = t.get('type', 'DB')
        amount = t.get('amount', 0)

        if tipe == 'CR':
            daily[date]['income'] += amount
        else:
            daily[date]['expense'] += amount

        daily[date]['count'] += 1
        daily[date]['transactions'].append({
            'label': t.get('label', ''),
            'amount': amount,
            'category': t.get('category', ''),
            'type': tipe
        })

    return {"status": "success", "data": daily}

@app.get("/api/goals")
async def get_goals():
    data = ambil_goals()
    return {"status": "success", "data": data}

@app.post("/api/goals")
async def create_goal(name: str, target_amount: float, deadline: str, category: str = "Savings"):
    tambah_goal(name, target_amount, deadline, category)
    return {"status": "success", "message": "Goal berhasil dibuat"}

@app.get("/api/budgets")
async def get_budgets(
    bulan: int = Query(default=datetime.now().month),
    tahun: int = Query(default=datetime.now().year)
):
    data = ambil_budgets(bulan, tahun)
    return {"status": "success", "data": data}

@app.post("/api/budgets")
async def set_budget(category: str, monthly_limit: float, bulan: int = Query(default=datetime.now().month), tahun: int = Query(default=datetime.now().year)):
    simpan_budget(category, monthly_limit, bulan, tahun)
    return {"status": "success", "message": "Budget berhasil disimpan"}

@app.get("/api/bank-detect")
async def detect_bank_from_file(file: UploadFile = File(...)):
    file_bytes = await file.read()
    from ai_engine import detect_bank
    import pdfplumber
    import io

    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            teks = "\n".join([h.extract_text() for h in pdf.pages if h.extract_text()])
        bank = detect_bank(teks)
        return {"status": "success", "bank": bank}
    except:
        return {"status": "error", "message": "Gagal mendeteksi bank"}

if __name__ == "__main__":
    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", "8000"))
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
