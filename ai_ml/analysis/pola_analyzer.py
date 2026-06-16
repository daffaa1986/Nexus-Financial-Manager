"""
Pola Analyzer
==============
Menganalisis pola pengeluaran harian dan mingguan.
"""

from collections import defaultdict
from datetime import datetime


DAYS_INDONESIA = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']


def analisis_harian(transaksi_list):
    """Analyze daily spending patterns."""
    tips = []

    if not transaksi_list:
        return tips

    by_day = defaultdict(lambda: {'total': 0, 'count': 0})

    for t in transaksi_list:
        if t.get('type') != 'DB':
            continue
        try:
            dt = datetime.strptime(t['date'], '%Y-%m-%d')
            day_name = DAYS_INDONESIA[dt.weekday()]
            by_day[day_name]['total'] += t['amount']
            by_day[day_name]['count'] += 1
        except:
            pass

    if len(by_day) < 2:
        return tips

    sorted_days = sorted(by_day.items(), key=lambda x: x[1]['total'], reverse=True)
    top_day = sorted_days[0]
    bottom_day = sorted_days[-1]

    if top_day[1]['total'] > bottom_day[1]['total'] * 1.5:
        tips.append({
            'type': 'tip',
            'title': f'Hari paling boros: {top_day[0]}',
            'description': (
                f'Pengeluaran {top_day[0]} (Rp{top_day[1]["total"]:,.0f}) '
                f'lebih tinggi dari {bottom_day[0]} (Rp{bottom_day[1]["total"]:,.0f}).'
            ),
            'severity': 'medium',
        })

    return tips
