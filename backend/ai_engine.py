import io
import re
import pdfplumber
import google.generativeai as genai

# MASUKKAN API KEY GEMINI KAMU DI SINI
API_KEY = "MASUKKAN_API_KEY_YANG_VALID_DISINI"
genai.configure(api_key=API_KEY)
model_llm = genai.GenerativeModel('gemini-1.5-flash')

def ekstrak_tabel_bca(teks_mentah):
    dataset = []
    for baris in teks_mentah.split('\n'):
        baris = baris.strip()
        match = re.search(r'(\d{2}/\d{2})\s+(.+?)\s+((?:\d{1,3}(?:,\d{3})*|\d+)\.\d{2}(?:\s+DB|\s+CR|DB|CR)?)', baris)
        if match:
            tanggal = match.group(1)
            ket_mentah = match.group(2).strip()
            nom_raw = match.group(3).strip()
            tipe = "DB" if "DB" in nom_raw else "CR"
            nominal = float(re.sub(r'[^\d.]', '', nom_raw.split(' ')[0]))
            # Format tanggal disesuaikan untuk UI (Contoh: 04-12)
            dataset.append({"tanggal": f"2026-{tanggal.replace('/','-')}", "keterangan": ket_mentah, "nominal": nominal, "tipe": tipe})
    return dataset

def nlp_bersihkan_teks(teks):
    teks = str(teks).upper()
    teks = re.sub(r'(TRANSAKSI DEBIT|TRSF E-BANKING CR|TRSF E-BANKING DB|BI-FAST CR|TARIKAN ATM \d{2}/\d{2}|SWITCHING DB)', '', teks)
    teks = re.sub(r'TANGGAL\s?:\s?\d{2}/\d{2}|TGL:\s*\d{2}/\d{2}', '', teks)
    teks = re.sub(r'\d{4}/[A-Z]+/[A-Z0-9]+', '', teks)
    teks = re.sub(r'[A-Z0-9]{15,}', '', teks)
    teks = re.sub(r'\s+', ' ', teks).strip()
    return teks if teks else "LAINNYA"

def llm_tebak_kategori(teks_bersih, tipe_trx):
    if not teks_bersih or teks_bersih == "LAINNYA": return "Lainnya"
    prompt = f"Kategorikan transaksi '{teks_bersih}' (Tipe: {tipe_trx}). Pilihan: Food & Beverage, Shopping, Transport, Entertainment, Utility, Income, Lainnya. Jawab HANYA 1 kategori spesifik."
    try:
        return model_llm.generate_content(prompt).text.strip()
    except Exception as e:
        print(f"Error AI: {e}")
        return "Uncategorized"

def proses_dokumen_mutasi(file_bytes):
    print("🤖 AI: Membaca PDF...")
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        teks_mentah = "\n".join([halaman.extract_text() for halaman in pdf.pages if halaman.extract_text()])
    
    transaksi_mentah = ekstrak_tabel_bca(teks_mentah)
    
    # KITA BATASI 5 TRANSAKSI DULU AGAR TESTING TIDAK LAMA
    transaksi_limit = transaksi_mentah[:5] 
    
    hasil_akhir = []
    for trx in transaksi_limit:
        bersih = nlp_bersihkan_teks(trx['keterangan'])
        kategori = llm_tebak_kategori(bersih, trx['tipe'])
        
        hasil_akhir.append({
            "date": trx['tanggal'],
            "label": bersih,
            "amount": trx['nominal'],
            "category": kategori,
            "type": trx['tipe']
        })
        
    return hasil_akhir
