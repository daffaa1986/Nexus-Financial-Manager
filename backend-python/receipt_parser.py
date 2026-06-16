import re
from datetime import datetime

STORE_CATEGORIES = {
    'Food & Beverage': [
        "MCD", "KFC", "PIZZA HUT", "HOKBEN", "SUBWAY", "BREADTALK",
        "STARBUCKS", "COFFEE BEAN", "TOKO KOPI", "KEDAI KOPI", "WARUNG",
        "RUMAH MAKAN", "RM ", "RESTO", "CAFE", "FOOD COURT", "FOODCOURT",
        "BAKSO", "MIE AYAM", "SATE", "SOTO", "PADANG", "WARKOP",
        "J.CO", "DOMINOS", "PAPA RON", "A&W", "WENDYS", "CARL JR",
        "ICHITAN", "GONG CHA", "TIGA TIGA KOPI", "KOPITIAM",
        "ATELIER", "KAFE", "KANTIN", "DEPOT"
    ],
    'Shopping': [
        "ALFAMART", "INDOMARET", "CIRCLE K", "AGEN BRILINK",
        "GRAMEDIA", "MATAHARI", "CENTRO", "MAP", "ZARA", "UNIQLO",
        "TOPED", "SHOPEE", "LAZADA", "TOKOPEDIA", "BLIBLI",
        "ACE HARDWARE", "ACE", "HARDWARE", "TOKO BANGUNAN",
        "OPTIK", "OPTIK SEIS", "OPTIK MELAWAI"
    ],
    'Health': [
        "APOTEK", "K24", "KIMIA FARMA", "GUDE", "KAWAN",
        "TOKO OBAT", "HERBAL", "VITAMIN", "SUPLEMEN",
        "KLINIK", "DOKTER", "RS ", "RUMAH SAKIT",
        "BPJS", "FARMASI", "CAPSULE", "FARMASI"
    ],
    'Bills & Utility': [
        "PLN", "TELKOM", "INDOSAT", "XL", "AXIS", "TRI",
        "SMARTFREN", "TELKOMSEL", "PDAM", "PDAM TIRTA",
        "SPBU", "PERTAMINA", "SHELL", "BPJS",
        "PAS PASCABAYAR", "PRA BAYAR"
    ],
    'Transport': [
        "GOJEK", "GRAB", "MAXIM", "TOKO PULSA",
        "TIKI", "JNE", "J&T", "SICEPAT", "NINJA",
        "POS INDONESIA", "ANTARAN"
    ],
    'Entertainment': [
        "NETFLIX", "SPOTIFY", "DISNEY", "CINEMA",
        "XXI", "CINEPOLIS", "CGV", "BLITZ", "GAME"
    ],
    'Education': [
        "COURSE", "KURSUS", "TOKO BUKU", "BUKU",
        "EDUCATION", "SEKOLAH"
    ],
}

def classify_store(store_name):
    if not store_name:
        return "Lainnya"

    store_upper = store_name.upper()

    for kategori, keywords in STORE_CATEGORIES.items():
        for kw in keywords:
            if kw in store_upper:
                return kategori

    return "Lainnya"

def parse_receipt_items(items_data):
    parsed_items = []
    if not items_data:
        return parsed_items

    for item in items_data:
        if isinstance(item, dict):
            name = item.get('name', 'Item')
            qty = item.get('qty', 1)
            price = item.get('price', 0)
        elif isinstance(item, (list, tuple)) and len(item) >= 2:
            name = str(item[0])
            qty = int(item[1]) if len(item) > 1 else 1
            price = float(item[2]) if len(item) > 2 else 0
        else:
            continue

        try:
            price = float(price)
            qty = int(qty)
        except (ValueError, TypeError):
            continue

        if price > 0:
            parsed_items.append({
                'name': str(name).strip(),
                'qty': qty,
                'price': price,
                'subtotal': price * qty
            })

    return parsed_items

def normalize_receipt_date(date_str):
    if not date_str:
        return datetime.now().strftime('%Y-%m-%d')

    date_str = date_str.strip()

    formats = [
        '%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%d/%m/%y',
        '%d %m %Y', '%d %B %Y', '%d %b %Y',
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            continue

    return datetime.now().strftime('%Y-%m-%d')

def parse_single_receipt(ocr_result):
    if 'error' in ocr_result:
        return None

    store_name = ocr_result.get('store_name', 'Unknown Store')
    total = ocr_result.get('total', 0)
    date = normalize_receipt_date(ocr_result.get('date', ''))
    items = parse_receipt_items(ocr_result.get('items', []))
    category = ocr_result.get('category', '')

    if not category:
        category = classify_store(store_name)

    if total == 0 and items:
        total = sum(item['subtotal'] for item in items)

    if total == 0:
        total = ocr_result.get('subtotal', 0)

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

def parse_multiple_receipts(ocr_results_list):
    parsed = []
    for r in ocr_results_list:
        result = parse_single_receipt(r)
        if result:
            parsed.append(result)
    return parsed

def receipt_to_transaction_format(receipt):
    return {
        'date': receipt.get('date', ''),
        'label': f"{receipt.get('store_name', 'Toko')} (Struk)",
        'amount': receipt.get('total', 0),
        'category': receipt.get('category', 'Lainnya'),
        'type': 'DB',
    }
