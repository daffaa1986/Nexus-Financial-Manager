"""
Boros Detector
==============
Mendeteksi "pemborosan": kategori pengeluaran terbesar,
hari dengan pengeluaran tertinggi, dan transaksi besar tidak wajar.
"""

from ..config import BOROS_CATEGORY_PCT, BOROS_SEVERE_PCT, BOROS_DAY_SPIKE_PCT


def deteksi(transaksi_list, total_expense):
    """Detect wasteful spending patterns."""
    boros = []

    if not transaksi_list or total_expense <= 0:
        return boros

    # === KATEGORI TERBESAR ===
    by_category = {}
    for t in transaksi_list:
        if t.get('type') != 'DB':
            continue
        cat = t.get('category', 'Lainnya')
        if cat not in by_category:
            by_category[cat] = 0
        by_category[cat] += t['amount']

    sorted_cats = sorted(by_category.items(), key=lambda x: x[1], reverse=True)
    if sorted_cats:
        top_cat, top_total = sorted_cats[0]
        persen = (top_total / total_expense) * 100
        if persen > BOROS_CATEGORY_PCT:
            boros.append({
                'type': 'boros',
                'title': f'Pengeluaran terbesar: {top_cat}',
                'description': f'{persen:.1f}% dari total pengeluaran (Rp{top_total:,.0f}). Perlu dikurangi.',
                'severity': 'high' if persen > BOROS_SEVERE_PCT else 'medium',
                'amount': top_total,
                'percentage': round(persen, 1),
            })

    # === HARI PALING BOROS ===
    by_date = {}
    for t in transaksi_list:
        if t.get('type') != 'DB':
            continue
        date = t.get('date', '')
        by_date[date] = by_date.get(date, 0) + t['amount']

    if by_date:
        max_date, max_total = max(by_date.items(), key=lambda x: x[1])
        if max_total > total_expense * (BOROS_DAY_SPIKE_PCT / 100):
            day_count = sum(1 for t in transaksi_list if t.get('date') == max_date and t.get('type') == 'DB')
            boros.append({
                'type': 'boros',
                'title': f'Hari belanja paling boros: {max_date}',
                'description': f'Rp{max_total:,.0f} terpakai dalam 1 hari ({day_count} transaksi).',
                'severity': 'medium',
                'amount': max_total,
            })

    return boros
