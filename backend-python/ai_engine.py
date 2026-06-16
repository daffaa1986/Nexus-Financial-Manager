import os
import io
import re
import pdfplumber
import google.generativeai as genai

API_KEY = os.environ.get("GEMINI_API_KEY", "MASUKKAN_API_KEY_YANG_VALID_DISINI")

model_llm = None
if API_KEY and API_KEY != "MASUKKAN_API_KEY_YANG_VALID_DISINI":
    try:
        genai.configure(api_key=API_KEY)
        model_llm = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        print(f"Gagal inisialisasi Gemini AI: {e}")

BANK_PATTERNS = {
    'BCA': {
        'pattern': r'(\d{2}/\d{2})\s+(.+?)\s+((?:\d{1,3}(?:,\d{3})*|\d+)\.\d{2}(?:\s+DB|\s+CR|DB|CR)?)',
        'date_format': '%Y-%m-%d',
    },
    'MANDIRI': {
        'pattern': r'(\d{2}/\d{2}/\d{4})\s+(.+?)\s+([\d,.]+)\s+(DB|CR)',
        'date_format': '%Y-%m-%d',
    },
    'BRI': {
        'pattern': r'(\d{2}/\d{2})\s+(.+?)\s+([\d,.]+)\s+(DB|CR)',
        'date_format': '%Y-%m-%d',
    },
    'BNI': {
        'pattern': r'(\d{2}/\d{2})\s+(.+?)\s+([\d,.]+)\s+(DB|CR)',
        'date_format': '%Y-%m-%d',
    },
    'BSI': {
        'pattern': r'(\d{2}/\d{2})\s+(.+?)\s+([\d,.]+)\s+(DB|CR)',
        'date_format': '%Y-%m-%d',
    },
}

def detect_bank(teks_mentah):
    teks_upper = teks_mentah.upper()
    if 'BCA' in teks_upper or 'BANK CENTRAL ASIA' in teks_upper:
        return 'BCA'
    if 'MANDIRI' in teks_upper or 'BANK MANDIRI' in teks_upper:
        return 'MANDIRI'
    if 'BRI' in teks_upper or 'BANK RAKYAT' in teks_upper:
        return 'BRI'
    if 'BNI' in teks_upper or 'BANK NEGARA' in teks_upper:
        return 'BNI'
    if 'BSI' in teks_upper or 'BANK SYARIAH' in teks_upper:
        return 'BSI'
    return 'BCA'

def ekstrak_tabel_mutasi(teks_mentah, bank='BCA'):
    dataset = []
    lines = teks_mentah.split('\n')

    year_match = re.search(r'(\d{4})', teks_mentah[:500])
    year = int(year_match.group(1)) if year_match else 2026

    for baris in lines:
        baris = baris.strip()
        if not baris:
            continue

        if bank == 'BCA':
            match = re.search(r'(\d{2}/\d{2})\s+(.+?)\s+((?:\d{1,3}(?:,\d{3})*|\d+)\.\d{2}(?:\s+DB|\s+CR|DB|CR)?)', baris)
            if match:
                tanggal = match.group(1)
                ket_mentah = match.group(2).strip()
                nom_raw = match.group(3).strip()
                tipe = "DB" if "DB" in nom_raw else "CR"
                nominal = float(re.sub(r'[^\d.]', '', nom_raw.split(' ')[0]))
                bulan, hari = tanggal.split('/')
                dataset.append({
                    "date": f"{year}-{bulan}-{hari}",
                    "keterangan": ket_mentah,
                    "nominal": nominal,
                    "tipe": tipe
                })
        else:
            for bank_name, pattern_info in BANK_PATTERNS.items():
                if bank_name != bank:
                    continue
                match = re.search(pattern_info['pattern'], baris)
                if match:
                    tanggal_raw = match.group(1)
                    ket_mentah = match.group(2).strip()
                    nom_raw = match.group(3).strip().replace(',', '')
                    tipe = match.group(4) if match.lastindex >= 4 else ("DB" if "DB" in nom_raw else "CR")

                    if '/' in tanggal_raw and len(tanggal_raw.split('/')) == 3:
                        parts = tanggal_raw.split('/')
                        bulan, hari, yr = parts[0], parts[1], parts[2]
                        year = int(yr)
                    else:
                        bulan, hari = tanggal_raw.split('/')

                    nominal = float(re.sub(r'[^\d.]', '', nom_raw))
                    dataset.append({
                        "date": f"{year}-{bulan}-{hari}",
                        "keterangan": ket_mentah,
                        "nominal": nominal,
                        "tipe": tipe
                    })
                    break

    return dataset

def nlp_bersihkan_teks(teks):
    teks = str(teks).upper()
    teks = re.sub(r'(TRANSAKSI DEBIT|TRSF E-BANKING CR|TRSF E-BANKING DB|BI-FAST CR|TARIKAN ATM \d{2}/\d{2}|SWITCHING DB|QRIS|SETORAN|PENARIKAN|TRANSFER|BUNGA|PAJAK|ADMIN|BIAYA)', '', teks)
    teks = re.sub(r'TANGGAL\s?:\s?\d{2}/\d{2}|TGL:\s*\d{2}/\d{2}', '', teks)
    teks = re.sub(r'\d{4}/[A-Z]+/[A-Z0-9]+', '', teks)
    teks = re.sub(r'[A-Z0-9]{15,}', '', teks)
    teks = re.sub(r'\d{2}/\d{2}/\d{4}', '', teks)
    teks = re.sub(r'\s+', ' ', teks).strip()
    return teks if teks else "LAINNYA"

KATEGORI_KEYWORDS = {
    'Food & Beverage': [
        "BAKSO", "CINCAU", "WARTEG", "TEH", "PADANG", "GORENG", "MAYO", "KOPI",
        "FOOD", "AYAM", "BURJO", "WARUNG", "PISANG", "SNACK", "SUSUKA", "DUREN",
        "RESTO", "CAFE", "KULINER", "MIE", "NASI", "JUS", "ES", "RUMAH MAKAN",
        "RM ", "KANTIN", "FOODCOURT", "MCD", "KFC", "PIZZA", "HOKBEN",
        "BREADTALK", "STARBUCKS", "SUBWAY", "WENDYS", "Burger", "CHICKEN",
        "SATE", "BEBEK", "SOTO", "PECEL", "GADO", "TEMPE", "TAHU", "SOTO",
        "WARKOP", "KEDAI", "PENDEKAR", "ANTJ", "ANTELOPE", "COFFEE BEAN"
    ],
    'Shopping': [
        "ALFAMART", "INDOMARET", "SHOPPING", "MART", "MALL", "FO",
        "GRAMEDIA", "BOOK", "FASHION", "TOPED", "SHOPEE", "LAZADA",
        "TOKOPEDIA", "BUKALAPAK", "BLIBLI", "TIKETCOM", "TRAVELOKA",
        "ZALORA", "BLOOMINGDALE", "UNIQLO", "HNM", "ZARA", "ORIFLAME",
        "MATAHARI", "CENTRO", "MAP", "ACE HARDWARE", "TOYS KINGDOM",
        "TIMEZONE", "AMAZONE", "KFC", "BREADTALK"
    ],
    'Transport': [
        "TRANSPORT", "GOJEK", "GRAB", "MAXIM", "WAHANA", "TIKI", "JNE",
        "J&T", "GOPAY", "OVO", "FLAZZ", "Pertamina", "SHELL", "SPBU",
        "PERTAMAX", "PERTALITE", "SPBU", "BENSIN", "SOLAR", "BIO SOLAR",
        "ANTARAN", "EXPRESS", "SICEPAT", "POS INDONESIA", "NINJA EXPRESS",
        "LALAMOVE", "GOSEND", "GRABSEND", "GRAB FOOD", "GRAB MART"
    ],
    'Bills & Utility': [
        "PLN", "PULSA", "INTERNET", "WIFI", "TELKOM", "VISIONET", "FLIPTECH",
        "IPAYMU", "LISTRIK", "AIR MINUM", "PDAM", "GAS", "TELKOMSEL",
        "INDOSAT", "XL", "AXIS", "TRI", "SMARTFREN", "BY.U", "IM3",
        "VOUCHER", "TOKEN LISTRIK", "PLN MOBILE", "BPJS", "DANA SEHAT",
        "LAUND", "K24", "APOTEK", "OBAT", "TOKO OBAT", "KIMIA FARMA",
        "GUDE", "KAWAN", "KENCANA"
    ],
    'Entertainment': [
        "NETFLIX", "SPOTIFY", "DISNEY", "HOTSTAR", "HBO", "YOUTUBE",
        "GAME", "STEAM", "GARENA", "MOBILE LEGEND", "PUBG", "FREE FIRE",
        "CATCHPLAY", "VIU", "IFLIX", "VIDIO", "WE TV", "GENflix",
        "CINEMA", "XXI", "CINEPOLIS", "CGV", "BLITZ", "TIX.ID"
    ],
    'Health': [
        "APOTEK", "K24", "GUDE", "KAWAN", "KIMIA FARMA", "HERBAL",
        "DOKTER", "KLINIK", "RUMAH SAKIT", "RS ", "BPJS", "VITAMIN",
        "SUPLEMEN", "TOKO OBAT", "FARMASI", "OBAT"
    ],
    'Investment': [
        "INVEST", "REKSADANA", "BIBIT", "STOCKBIT", "AJAIB", "CRYPTO",
        "BINANCE", "SAHAM", "TRADING", "ETF", "EMAS", "LOGAM MULIA",
        "TAMBAHAN EMAS", "TABUNGAN EMAS"
    ],
    'Education': [
        "COURSE", "KURSUS", "BELAJAR", "EDU", "COURSERA", "UDACITY",
        "SKILLSHARE", "UDEMY", "DICODING", "BIMBEL", "LES ", "SEKOLAH",
        "KULIAH", "UNIVERSITAS", "POLITEKNIK"
    ],
    'Income': [],
}

def kategorisasi_aturan(teks_bersih, tipe_trx):
    if tipe_trx == "CR":
        teks = teks_bersih.upper()
        if any(k in teks for k in ["GAJI", "SALARY", "INCOME", "PENGHASILAN", "BONUS", "FEE", "KOMISI"]):
            return "Income"
        if any(k in teks for k in ["TRANSFER", "TF", "CR", "SETOR", "DEPOSIT"]):
            return "Income"
        return "Income"

    teks = teks_bersih.upper()
    for kategori, keywords in KATEGORI_KEYWORDS.items():
        for kw in keywords:
            if kw in teks:
                return kategori
    return None

def llm_tebak_kategori(teks_bersih, tipe_trx):
    if not teks_bersih or teks_bersih == "LAINNYA":
        return "Lainnya" if tipe_trx == "DB" else "Income"

    kategori_lokal = kategorisasi_aturan(teks_bersih, tipe_trx)
    if kategori_lokal:
        return kategori_lokal

    if model_llm is None:
        return "Lainnya" if tipe_trx == "DB" else "Income"

    pilihan = ", ".join(KATEGORI_KEYWORDS.keys()) + ", Lainnya"
    prompt = f"""Kategorikan transaksi ini: '{teks_bersih}' (Tipe: {tipe_trx})
Pilihan kategori: {pilihan}
Jawab HANYA 1 kategori saja, tanpa penjelasan."""
    try:
        hasil = model_llm.generate_content(prompt).text.strip()
        if hasil in KATEGORI_KEYWORDS or hasil == "Lainnya":
            return hasil
        for k in KATEGORI_KEYWORDS:
            if k.lower() == hasil.lower():
                return k
        return hasil
    except Exception as e:
        print(f"Error AI kategorisasi: {e}")
        return "Lainnya"

def proses_dokumen_mutasi(file_bytes, bank=None):
    print("AI: Membaca PDF mutasi...")
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        teks_mentah = "\n".join([h.extract_text() for h in pdf.pages if h.extract_text()])

    if not bank:
        bank = detect_bank(teks_mentah)
    print(f"Bank terdeteksi: {bank}")

    transaksi_mentah = ekstrak_tabel_mutasi(teks_mentah, bank)

    hasil_akhir = []
    for trx in transaksi_mentah:
        bersih = nlp_bersihkan_teks(trx['keterangan'])
        kategori = llm_tebak_kategori(bersih, trx['tipe'])
        hasil_akhir.append({
            "date": trx['date'],
            "label": bersih,
            "amount": trx['nominal'],
            "category": kategori,
            "type": trx['tipe']
        })

    print(f"Berhasil ekstrak {len(hasil_akhir)} transaksi dari {bank}")
    return hasil_akhir, bank

def generate_ai_insights(transaksi_list):
    if not model_llm or not transaksi_list:
        return []

    summary = {}
    for t in transaksi_list:
        cat = t.get('category', 'Lainnya')
        if cat not in summary:
            summary[cat] = {'total': 0, 'count': 0, 'items': []}
        if t.get('type') == 'DB':
            summary[cat]['total'] += t.get('amount', 0)
            summary[cat]['count'] += 1
            if len(summary[cat]['items']) < 3:
                summary[cat]['items'].append(f"{t.get('label','')} Rp{t.get('amount',0):,.0f}")

    deskripsi = "\n".join([
        f"- {cat}: Rp{data['total']:,.0f} ({data['count']} transaksi) Contoh: {', '.join(data['items'])}"
        for cat, data in summary.items() if data['count'] > 0
    ])

    prompt = f"""Analisis data pengeluaran berikut dan berikan insight dalam Bahasa Indonesia:

{deskripsi}

Berikan 3-5 insight dengan format JSON array:
[
  {{
    "type": "bocor" atau "boros" atau "tip" atau "good",
    "title": "Judul singkat",
    "description": "Penjelasan 1-2 kalimat",
    "severity": "high" atau "medium" atau "low"
  }}
]

Fokus pada:
1. Pengeluaran kecil yang sering (bocor)
2. Kategori yang paling besar (boros)
3. Tips hemat
4. Hal positif dari pola belanja"""

    try:
        response = model_llm.generate_content(prompt)
        text = response.text.strip()
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*$', '', text)
        import json
        return json.loads(text)
    except Exception as e:
        print(f"Error generate insights: {e}")
        return []
