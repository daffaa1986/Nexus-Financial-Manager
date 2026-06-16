"""
NLP Text Cleaner
=================
Membersihkan teks transaksi dari noise sebelum dikategorisasi.
"""

import re


def bersihkan_teks(teks):
    """Clean raw transaction text by removing banking noise."""
    teks = str(teks).upper()
    
    bank_keywords = [
        'TRANSAKSI DEBIT', 'TRSF E-BANKING CR', 'TRSF E-BANKING DB',
        'BI-FAST CR', 'TARIKAN ATM', 'SWITCHING DB', 'QRIS',
        'SETORAN', 'PENARIKAN', 'TRANSFER', 'BUNGA', 'PAJAK',
        'ADMIN', 'BIAYA', 'MUTASI', 'SALDO', 'BUNGA'
    ]
    for kw in bank_keywords:
        teks = re.sub(kw, '', teks)

    teks = re.sub(r'TANGGAL\s?:\s?\d{2}/\d{2}|TGL:\s*\d{2}/\d{2}', '', teks)
    teks = re.sub(r'\d{4}/[A-Z]+/[A-Z0-9]+', '', teks)
    teks = re.sub(r'[A-Z0-9]{15,}', '', teks)
    teks = re.sub(r'\d{2}/\d{2}/\d{4}', '', teks)
    teks = re.sub(r'\s+', ' ', teks).strip()
    
    return teks if teks else "LAINNYA"
