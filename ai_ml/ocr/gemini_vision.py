"""
Gemini Vision OCR
==================
Menggunakan Google Gemini Vision untuk membaca dan mengekstrak
informasi dari foto struk belanjaan.
"""

import io
import re
import json
from PIL import Image
from ..config import GEMINI_API_KEY

_model_vision = None


def _init_model():
    global _model_vision
    if _model_vision is not None:
        return True

    if not GEMINI_API_KEY or GEMINI_API_KEY == "MASUKKAN_API_KEY_YANG_VALID_DISINI":
        _model_vision = False
        return False

    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        _model_vision = genai.GenerativeModel('gemini-1.5-flash')
        return True
    except Exception as e:
        print(f"Gagal init Gemini Vision: {e}")
        _model_vision = False
        return False


def ocr_struk(image_bytes):
    """
    OCR receipt image using Gemini Vision.
    Returns parsed receipt data as dict.
    """
    if not _init_model():
        return {'error': 'Gemini Vision belum dikonfigurasi. Set GEMINI_API_KEY.'}

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
Jawab HANYA JSON, tanpa penjelasan tambahan."""

    try:
        response = _model_vision.generate_content([prompt, image])
        text = _bersihkan_json(response.text)

        result = json.loads(text)
        result['raw_ocr_text'] = response.text
        return result
    except json.JSONDecodeError:
        return {
            'store_name': 'Unknown Store', 'date': '', 'items': [],
            'subtotal': 0, 'tax': 0, 'total': 0,
            'category': 'Lainnya', 'error': 'Gagal parse JSON dari Gemini'
        }
    except Exception as e:
        return {'error': f'Error OCR: {str(e)}'}


def _bersihkan_json(text):
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*$', '', text)
    return text.strip()
