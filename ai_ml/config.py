"""
AI/ML Configuration
=====================
Semua konfigurasi AI/ML dalam satu tempat.
"""

import os

# ============================================
# GEMINI AI (LLM untuk kategorisasi & insight)
# ============================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "MASUKKAN_API_KEY_YANG_VALID_DISINI")
GEMINI_MODEL = 'gemini-1.5-flash'

# ============================================
# KATEGORI TRANSAKSI
# ============================================
KATEGORI_KEYWORDS = {
    'Food & Beverage': [
        "BAKSO", "CINCAU", "WARTEG", "TEH", "PADANG", "GORENG", "MAYO", "KOPI",
        "FOOD", "AYAM", "BURJO", "WARUNG", "PISANG", "SNACK", "SUSUKA", "DUREN",
        "RESTO", "CAFE", "KULINER", "MIE", "NASI", "JUS", "ES", "RUMAH MAKAN",
        "RM ", "KANTIN", "FOODCOURT", "MCD", "KFC", "PIZZA", "HOKBEN",
        "BREADTALK", "STARBUCKS", "SUBWAY", "WENDYS", "Burger", "CHICKEN",
        "SATE", "BEBEK", "SOTO", "PECEL", "GADO", "TEMPE", "TAHU",
        "WARKOP", "KEDAI", "COFFEE BEAN", "J.CO", "DOMINOS"
    ],
    'Shopping': [
        "ALFAMART", "INDOMARET", "SHOPPING", "MART", "MALL", "FO",
        "GRAMEDIA", "BOOK", "FASHION", "TOPED", "SHOPEE", "LAZADA",
        "TOKOPEDIA", "BUKALAPAK", "BLIBLI", "ZALORA", "UNIQLO", "ZARA",
        "MATAHARI", "ACE HARDWARE", "AMAZON"
    ],
    'Transport': [
        "TRANSPORT", "GOJEK", "GRAB", "MAXIM", "TIKI", "JNE", "J&T",
        "GOPAY", "OVO", "FLAZZ", "PERTAMINA", "SHELL", "SPBU",
        "BENSIN", "SOLAR", "PERTALITE", "PERTAMAX",
        "EXPRESS", "SICEPAT", "POS INDONESIA", "NINJA EXPRESS",
        "LALAMOVE", "GOSEND", "GRABSEND"
    ],
    'Bills & Utility': [
        "PLN", "PULSA", "INTERNET", "WIFI", "TELKOM", "VISIONET", "FLIPTECH",
        "IPAYMU", "LISTRIK", "PDAM", "GAS", "TELKOMSEL",
        "INDOSAT", "XL", "AXIS", "TRI", "SMARTFREN",
        "VOUCHER", "TOKEN LISTRIK", "BPJS",
        "LAUND", "K24", "APOTEK", "OBAT"
    ],
    'Entertainment': [
        "NETFLIX", "SPOTIFY", "DISNEY", "HBO", "YOUTUBE",
        "GAME", "STEAM", "GARENA", "MOBILE LEGEND", "PUBG", "FREE FIRE",
        "CINEMA", "XXI", "CINEPOLIS", "CGV", "TIX.ID"
    ],
    'Health': [
        "APOTEK", "K24", "KIMIA FARMA", "GUDE", "KAWAN",
        "HERBAL", "DOKTER", "KLINIK", "RUMAH SAKIT", "RS ",
        "BPJS", "VITAMIN", "SUPLEMEN", "OBAT", "FARMASI"
    ],
    'Investment': [
        "INVEST", "REKSADANA", "BIBIT", "STOCKBIT", "AJAIB", "CRYPTO",
        "BINANCE", "SAHAM", "TRADING", "ETF", "EMAS", "LOGAM MULIA",
        "TABUNGAN EMAS"
    ],
    'Education': [
        "COURSE", "KURSUS", "BELAJAR", "EDU", "COURSERA",
        "UDEMY", "DICODING", "BIMBEL", "LES ", "SEKOLAH",
        "KULIAH", "UNIVERSITAS", "POLITEKNIK"
    ],
    'Income': [],
}

# ============================================
# BOCOR/BOROS DETECTION THRESHOLDS
# ============================================
BOCOR_AMOUNT_THRESHOLD = 50000      # Transaksi < 50rb dianggap "kecil"
BOCOR_MIN_COUNT = 3                  # Minimal 3x transaksi untuk dianggap bocor
BOCOR_MIN_TOTAL = 50000             # Minimal total 50rb untuk dianggap bocor
BOCOR_SEVERE_TOTAL = 200000         # > 200rb dianggap bocor parah

BOROS_CATEGORY_PCT = 40             # Kategori > 40% total pengeluaran dianggap boros
BOROS_SEVERE_PCT = 50               # > 50% dianggap boros parah
BOROS_DAY_SPIKE_PCT = 25            # 1 hari > 25% total dianggap boros

# ============================================
# DATABASE
# ============================================
DB_TYPE = os.environ.get("DB_TYPE", "sqlite")
