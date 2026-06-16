"""
Transaction Classifier
=======================
Mengklasifikasikan transaksi ke dalam kategori menggunakan:
1. Aturan berbasis keyword (cepat, tanpa API)
2. Fallback ke Gemini LLM (akurat, tapi butuh API key)
"""

from ..config import GEMINI_API_KEY, GEMINI_MODEL, KATEGORI_KEYWORDS
from ..data.cleaner import bersihkan_teks

_llm_model = None

def _init_llm():
    global _llm_model
    if _llm_model is not None:
        return _llm_model is not None
    
    if GEMINI_API_KEY and GEMINI_API_KEY != "MASUKKAN_API_KEY_YANG_VALID_DISINI":
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            _llm_model = genai.GenerativeModel(GEMINI_MODEL)
            return True
        except Exception as e:
            print(f"Gagal init Gemini: {e}")
    
    _llm_model = False
    return False


def _kategorisasi_aturan(teks_bersih, tipe_trx):
    """Rule-based categorization using keyword matching."""
    if tipe_trx == "CR":
        teks = teks_bersih.upper()
        if any(k in teks for k in ["GAJI", "SALARY", "INCOME", "PENGHASILAN", "BONUS", "FEE", "KOMISI"]):
            return "Income"
        return "Income"

    teks = teks_bersih.upper()
    for kategori, keywords in KATEGORI_KEYWORDS.items():
        for kw in keywords:
            if kw in teks:
                return kategori
    return None


def _llm_tebak_kategori(teks_bersih, tipe_trx):
    """LLM-based categorization using Google Gemini."""
    if not _init_llm():
        return "Lainnya" if tipe_trx == "DB" else "Income"
    
    import google.generativeai as genai
    pilihan = ", ".join(KATEGORI_KEYWORDS.keys()) + ", Lainnya"
    
    prompt = f"""Kategorikan transaksi ini: '{teks_bersih}' (Tipe: {tipe_trx})
Pilihan kategori: {pilihan}
Jawab HANYA 1 kategori saja, tanpa penjelasan."""
    
    try:
        hasil = _llm_model.generate_content(prompt).text.strip()
        if hasil in KATEGORI_KEYWORDS or hasil == "Lainnya":
            return hasil
        for k in KATEGORI_KEYWORDS:
            if k.lower() == hasil.lower():
                return k
        return hasil
    except Exception as e:
        print(f"Error LLM: {e}")
        return "Lainnya"


def klasifikasi_transaksi(teks_bersih, tipe_trx):
    """Classify a transaction into a category."""
    if not teks_bersih or teks_bersih == "LAINNYA":
        return "Lainnya" if tipe_trx == "DB" else "Income"

    # Try rule-based first (fast, free)
    kategori = _kategorisasi_aturan(teks_bersih, tipe_trx)
    if kategori:
        return kategori

    # Fallback to LLM (slower, needs API key)
    return _llm_tebak_kategori(teks_bersih, tipe_trx)


def proses_transaksi(transaksi_mentah_list):
    """Process raw transactions through cleaning and classification pipeline."""
    hasil_akhir = []
    
    for trx in transaksi_mentah_list:
        bersih = bersihkan_teks(trx.get('keterangan', ''))
        kategori = klasifikasi_transaksi(bersih, trx.get('tipe', 'DB'))
        
        hasil_akhir.append({
            "date": trx['date'],
            "label": bersih,
            "amount": trx['nominal'],
            "category": kategori,
            "type": trx['tipe']
        })
    
    return hasil_akhir
