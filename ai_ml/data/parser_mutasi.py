"""
Parser Mutasi Rekening
=======================
Membaca dan mengekstrak transaksi dari file PDF mutasi rekening.
Support multi-bank: BCA, Mandiri, BRI, BNI, BSI.
"""

import io
import re
import pdfplumber
from ..utils.bank_detector import detect_bank
from ..utils.helpers import parse_date_to_month_year

BANK_PATTERNS = {
    'BCA': r'(\d{2}/\d{2})\s+(.+?)\s+((?:\d{1,3}(?:,\d{3})*|\d+)\.\d{2}(?:\s+DB|\s+CR|DB|CR)?)',
    'MANDIRI': r'(\d{2}/\d{2}/\d{4})\s+(.+?)\s+([\d,.]+)\s+(DB|CR)',
    'BRI': r'(\d{2}/\d{2})\s+(.+?)\s+([\d,.]+)\s+(DB|CR)',
    'BNI': r'(\d{2}/\d{2})\s+(.+?)\s+([\d,.]+)\s+(DB|CR)',
    'BSI': r'(\d{2}/\d{2})\s+(.+?)\s+([\d,.]+)\s+(DB|CR)',
}


def ekstrak_tabel_mutasi(teks_mentah, bank='BCA'):
    """Extract transactions from raw bank statement text."""
    dataset = []
    year = _detect_year(teks_mentah)

    for baris in teks_mentah.split('\n'):
        baris = baris.strip()
        if not baris:
            continue

        if bank == 'BCA':
            trx = _parse_bca_line(baris, year)
        else:
            trx = _parse_generic_line(baris, bank, year)

        if trx:
            dataset.append(trx)

    return dataset


def _detect_year(teks):
    match = re.search(r'(\d{4})', teks[:500])
    return int(match.group(1)) if match else 2026


def _parse_bca_line(baris, year):
    """Parse BCA bank statement line format."""
    pattern = r'(\d{2}/\d{2})\s+(.+?)\s+((?:\d{1,3}(?:,\d{3})*|\d+)\.\d{2}(?:\s+DB|\s+CR|DB|CR)?)'
    match = re.search(pattern, baris)
    if not match:
        return None

    tanggal = match.group(1)
    ket_mentah = match.group(2).strip()
    nom_raw = match.group(3).strip()
    tipe = "DB" if "DB" in nom_raw else "CR"
    nominal = float(re.sub(r'[^\d.]', '', nom_raw.split(' ')[0]))

    bulan, hari = tanggal.split('/')
    return {
        "date": f"{year}-{bulan}-{hari}",
        "keterangan": ket_mentah,
        "nominal": nominal,
        "tipe": tipe
    }


def _parse_generic_line(baris, bank, year):
    """Parse other bank statement line format."""
    pattern = BANK_PATTERNS.get(bank)
    if not pattern:
        return None

    match = re.search(pattern, baris)
    if not match:
        return None

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
    return {
        "date": f"{year}-{bulan}-{hari}",
        "keterangan": ket_mentah,
        "nominal": nominal,
        "tipe": tipe
    }


def proses_dokumen_mutasi(file_bytes, bank=None):
    """Main pipeline: read PDF -> detect bank -> extract -> return transactions."""
    print("AI: Membaca PDF mutasi...")
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        teks_mentah = "\n".join([h.extract_text() for h in pdf.pages if h.extract_text()])

    if not bank:
        bank = detect_bank(teks_mentah)
    print(f"Bank terdeteksi: {bank}")

    transaksi_mentah = ekstrak_tabel_mutasi(teks_mentah, bank)

    from ..models.classifier import proses_transaksi
    hasil_akhir = proses_transaksi(transaksi_mentah)

    print(f"Berhasil ekstrak {len(hasil_akhir)} transaksi dari {bank}")
    return hasil_akhir, bank
