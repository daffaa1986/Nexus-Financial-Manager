"""
Receipt Normalizer
==================
Menormalisasi data hasil OCR struk dan mengkonversinya ke format transaksi.
"""

import re
from datetime import datetime
from collections import defaultdict

STORE_CATEGORIES = {
    'Food & Beverage': [
        "MCD", "KFC", "PIZZA HUT", "HOKBEN", "SUBWAY", "BREADTALK",
        "STARBUCKS", "COFFEE BEAN", "WARUNG", "RUMAH MAKAN", "RM ",
        "RESTO", "CAFE", "FOOD COURT", "BAKSO", "MIE AYAM", "SATE",
        "SOTO", "PADANG", "WARKOP", "J.CO", "DOMINOS", "KANTIN"
    ],
    'Shopping': [
        "ALFAMART", "INDOMARET", "CIRCLE K", "GRAMEDIA", "MATAHARI",
        "UNIQLO", "ZARA", "ACE HARDWARE", "MINISO", "DAISO", "MR DIY"
    ],
    'Health': [
        "APOTEK", "K24", "KIMIA FARMA", "GUDE", "KAWAN",
        "TOKO OBAT", "KLINIK", "DOKTER", "RS ", "RUMAH SAKIT"
    ],
    'Bills & Utility': [
        "PLN", "TELKOM", "INDOSAT", "XL", "AXIS", "TRI",
        "TELKOMSEL", "PDAM", "SPBU", "PERTAMINA", "BPJS"
    ],
    'Transport': ["GOJEK", "GRAB", "MAXIM", "JNE", "J&T", "SICEPAT"],
    'Entertainment': ["XXI", "CINEPOLIS", "CGV", "NETFLIX", "SPOTIFY"],
}


def klasifikasi_toko(store_name):
    """Classify a store into a spending category."""
    if not store_name:
        return "Lainnya"
    store_upper = store_name.upper()
    for kategori, keywords in STORE_CATEGORIES.items():
        for kw in keywords:
            if kw in store_upper:
                return kategori
    return "Lainnya"


def normalisasi_tanggal(date_str):
    """Normalize various date formats to YYYY-MM-DD."""
    if not date_str:
        return datetime.now().strftime('%Y-%m-%d')
    date_str = date_str.strip()

    formats = [
        '%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%d/%m/%y',
        '%d %m %Y', '%d %B %Y', '%d %b %Y',
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue
    return datetime.now().strftime('%Y-%m-%d')


def parse_items(items_data):
    """Parse receipt items from OCR result."""
    parsed = []
    if not items_data:
        return parsed

    for item in items_data:
        if isinstance(item, dict):
            name = str(item.get('name', 'Item')).strip()
            qty = int(item.get('qty', 1))
            price = float(item.get('price', 0))
        else:
            continue

        if price > 0:
            parsed.append({
                'name': name,
                'qty': qty,
                'price': price,
                'subtotal': price * qty
            })
    return parsed


def parse_single_receipt(ocr_result):
    """Parse a single OCR result into a normalized receipt format."""
    if 'error' in ocr_result:
        return None

    store_name = ocr_result.get('store_name', 'Unknown Store')
    category = ocr_result.get('category', '') or klasifikasi_toko(store_name)
    date = normalisasi_tanggal(ocr_result.get('date', ''))
    items = parse_items(ocr_result.get('items', []))
    total = ocr_result.get('total', 0) or ocr_result.get('subtotal', 0)

    if total == 0 and items:
        total = sum(item['subtotal'] for item in items)

    return {
        'store_name': store_name,
        'date': date,
        'items': items,
        'subtotal': ocr_result.get('subtotal', 0),
        'tax': ocr_result.get('tax', 0),
        'total': total,
        'payment_method': ocr_result.get('payment_method', ''),
        'category': category,
        'raw_ocr_text': ocr_result.get('raw_ocr_text', ''),
    }


def receipt_to_transaction(receipt):
    """Convert receipt data to transaction format for database storage."""
    return {
        'date': receipt.get('date', ''),
        'label': f"{receipt.get('store_name', 'Toko')} (Struk)",
        'amount': receipt.get('total', 0),
        'category': receipt.get('category', 'Lainnya'),
        'type': 'DB',
    }
