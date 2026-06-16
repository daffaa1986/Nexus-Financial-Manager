"""
Bocor Detector
==============
Mendeteksi "kebocoran" keuangan: transaksi kecil yang sering terjadi.
Contoh: beli kopi 5x seminggu, jajan ringan tiap hari.
"""

from collections import defaultdict
import re
from ..config import BOCOR_AMOUNT_THRESHOLD, BOCOR_MIN_COUNT, BOCOR_MIN_TOTAL, BOCOR_SEVERE_TOTAL


def deteksi(transaksi_list):
    """Detect financial 'leaks' - small but frequent transactions."""
    bocor = []

    # Filter transaksi kecil (< threshold)
    small = [t for t in transaksi_list 
             if t.get('type') == 'DB' and t.get('amount', 0) < BOCOR_AMOUNT_THRESHOLD]

    if not small:
        return bocor

    # Group by similar labels
    by_label = defaultdict(lambda: {'total': 0, 'count': 0, 'items': []})
    for st in small:
        label_clean = re.sub(r'\d+', '', st.get('label', '')).strip()[:30]
        by_label[label_clean]['total'] += st['amount']
        by_label[label_clean]['count'] += 1
        by_label[label_clean]['items'].append(st)

    # Flag if frequent enough
    for label, data in by_label.items():
        if data['count'] >= BOCOR_MIN_COUNT and data['total'] >= BOCOR_MIN_TOTAL:
            bocor.append({
                'type': 'bocor',
                'title': f'Pengeluaran kecil tapi sering: {label}',
                'description': f'{data["count"]}x transaksi = Rp{data["total"]:,.0f}/bulan. Kecil-kecil jadi bukit!',
                'severity': 'high' if data['total'] >= BOCOR_SEVERE_TOTAL else 'medium',
                'amount': data['total'],
                'count': data['count'],
            })

    return bocor
