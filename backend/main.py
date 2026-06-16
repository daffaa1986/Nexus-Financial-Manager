from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
from ai_engine import proses_dokumen_mutasi # IMPORT FILE AI KITA!
from db_config import init_db, simpan_transaksi, ambil_semua_transaksi

# Langsung nyalakan database saat server hidup
init_db()

app = FastAPI(title="Nexus Finance API")

# 1 & 2. (KODE CORS & WEBSOCKET MANAGER TETAP SAMA SEPERTI SEBELUMNYA)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    async def send_message(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/updates")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# =======================================================
# 3. MESIN AI ASLI (Menggunakan ai_engine.py & SQLite)
# =======================================================
async def proses_ai_background(filename: str, file_bytes: bytes):
    try:
        await manager.send_message({"status": "loading", "message": f"📄 AI sedang mengekstrak {filename}..."})
        
        # Proses AI Asli
        data_hasil_ai = await asyncio.to_thread(proses_dokumen_mutasi, file_bytes)
        
        # === KODE BARU: SIMPAN KE DATABASE ===
        await manager.send_message({"status": "loading", "message": "💾 Menyimpan data secara permanen..."})
        await asyncio.to_thread(simpan_transaksi, data_hasil_ai, filename)
        # =====================================
        
        # Kirim hasil asli ke Web HTML
        await manager.send_message({
            "status": "success", 
            "data": {
                "message": f"Berhasil memproses transaksi!",
                "new_transactions": data_hasil_ai
            }
        })
    except Exception as e:
        print(f"Error Sistem: {e}")
        await manager.send_message({"status": "success", "data": {"new_transactions": []}})

# =======================================================
# 4. JALUR UPLOAD FILE
# =======================================================
@app.post("/api/upload")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    print(f"📥 [SERVER] Menerima file: {file.filename}")
    file_bytes = await file.read() # Baca file PDF nya
    
    # Lempar file ke background AI
    background_tasks.add_task(proses_ai_background, file.filename, file_bytes)
    return {"message": "Memproses di background..."}

# =======================================================
# 5. JALUR AMBIL DATA DATABASE (Untuk me-refresh Web)
# =======================================================
@app.get("/api/transactions")
async def get_transactions():
    print("📤 [SERVER] Web meminta data transaksi terbaru...")
    data_db = ambil_semua_transaksi()
    return {"status": "success", "data": data_db}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)