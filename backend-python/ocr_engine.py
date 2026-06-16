import os
import io
import re
import base64
import google.generativeai as genai
from PIL import Image

API_KEY = os.environ.get("GEMINI_API_KEY", "MASUKKAN_API_KEY_YANG_VALID_DISINI")

model_vision = None
model_llm = None
if API_KEY and API_KEY != "MASUKKAN_API_KEY_YANG_VALID_DISINI":
    try:
        genai.configure(api_key=API_KEY)
        model_vision = genai.GenerativeModel('gemini-1.5-flash')
        model_llm = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        print(f"Gagal inisialisasi Gemini Vision: {e}")

def ocr_receipt_with_gemini(image_bytes):
    if model_vision is None:
        return {"error": "Gemini Vision belum dikonfigurasi. Set GEMINI_API_KEY di environment."}

    image = Image.open(io.BytesIO(image_bytes))

    prompt = """Analisis gambar struk belanja/receipt ini dan ekstrak informasi berikut dalam format JSON:
{
    "store_name": "Nama Toko/Restoran",
    "date": "YYYY-MM-DD (jika ada, kosongkan jika tidak)",
    "items": [
        {"name": "Nama Item", "qty": 1, "price": harga_per_item}
    ],
    "subtotal": jumlah_sebelum_pajak,
    "tax": pajak_ppn,
    "total": total_bayar,
    "payment_method": "Metode Pembayaran (jika ada)",
    "category": "Kategori: Food & Beverage, Shopping, Bills & Utility, Health, Entertainment, atau Lainnya"
}

Jika ada item yang sulit dibaca, tebak seakurat mungkin.
Jika ada nilai yang tidak ditemukan, gunakan 0.
Jika tanggal tidak ada, gunakan string kosong "".
Jawab HANYA JSON, tanpa penjelasan tambahan."""

    try:
        response = model_vision.generate_content([prompt, image])
        text = response.text.strip()
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*$', '', text)
        text = text.strip()

        import json
        result = json.loads(text)
        result['raw_ocr_text'] = response.text
        return result
    except json.JSONDecodeError:
        return {
            "store_name": "Unknown Store",
            "date": "",
            "items": [],
            "subtotal": 0,
            "tax": 0,
            "total": 0,
            "payment_method": "",
            "category": "Lainnya",
            "raw_ocr_text": response.text if 'response' in dir() else "",
            "error": "Gagal parse JSON dari Gemini"
        }
    except Exception as e:
        return {"error": f"Error OCR: {str(e)}"}

def ocr_receipt_batch(image_list):
    results = []
    for idx, img_bytes in enumerate(image_list):
        print(f"OCR struk {idx+1}/{len(image_list)}...")
        result = ocr_receipt_with_gemini(img_bytes)
        results.append(result)
    return results

def ocr_receipt_from_file(file_path):
    with open(file_path, 'rb') as f:
        image_bytes = f.read()
    return ocr_receipt_with_gemini(image_bytes)

def analyze_receipt_pattern(receipts_list):
    if not model_llm or not receipts_list:
        return []

    store_summary = {}
    for r in receipts_list:
        store = r.get('store_name', 'Unknown')
        total = r.get('total', 0)
        cat = r.get('category', 'Lainnya')
        if store not in store_summary:
            store_summary[store] = {'total': 0, 'count': 0, 'category': cat}
        store_summary[store]['total'] += total
        store_summary[store]['count'] += 1

    deskripsi = "\n".join([
        f"- {store}: Rp{s['total']:,.0f} ({s['count']}x) [Kategori: {s['category']}]"
        for store, s in store_summary.items()
    ])

    prompt = f"""Analisis pola belanja dari data struk berikut dalam Bahasa Indonesia:

{deskripsi}

Berikan insight dalam format JSON array:
[
  {{
    "type": "bocor" atau "boros" atau "tip" atau "good",
    "title": "Judul singkat",
    "description": "Penjelasan 1-2 kalimat",
    "severity": "high" atau "medium" atau "low"
  }}
]

Fokus pada:
1. Toko yang paling sering dikunjungi (potensi bocor)
2. Total pengeluaran per toko
3. Tips menghemat di toko tersebut"""

    try:
        response = model_llm.generate_content(prompt)
        text = response.text.strip()
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*$', '', text)
        import json
        return json.loads(text)
    except Exception as e:
        print(f"Error analisis receipt pattern: {e}")
        return []
