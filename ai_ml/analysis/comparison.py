"""
Monthly Comparison
==================
Membandingkan pengeluaran bulan ini dengan bulan sebelumnya.
"""

from collections import defaultdict


def hitung_statistik(transaksi_list):
    """Calculate summary statistics from a transaction list."""
    stats = {
        'total_income': 0,
        'total_expense': 0,
        'by_category': defaultdict(lambda: {'total': 0, 'count': 0, 'avg': 0}),
        'by_date': defaultdict(float),
        'by_day_of_week': defaultdict(lambda: {'total': 0, 'count': 0}),
    }

    for t in transaksi_list:
        tipe = t.get('type', 'DB')
        amount = t.get('amount', 0)
        date = t.get('date', '')
        category = t.get('category', 'Lainnya')

        if tipe == 'CR':
            stats['total_income'] += amount
        else:
            stats['total_expense'] += amount
            stats['by_category'][category]['total'] += amount
            stats['by_category'][category]['count'] += 1
            stats['by_date'][date] += amount

    # Calculate averages
    for cat in stats['by_category']:
        data = stats['by_category'][cat]
        data['avg'] = round(data['total'] / data['count']) if data['count'] > 0 else 0

    return stats


def bandingkan_bulan(transaksi_bulan_ini, transaksi_bulan_lalu):
    """Compare two months of spending data."""
    if not transaksi_bulan_ini:
        return {'error': 'Tidak ada data bulan ini'}

    now = hitung_statistik(transaksi_bulan_ini)
    prev = hitung_statistik(transaksi_bulan_lalu) if transaksi_bulan_lalu else None

    current = {
        'income': now['total_income'],
        'expense': now['total_expense'],
        'balance': now['total_income'] - now['total_expense'],
        'categories': {k: v['total'] for k, v in now['by_category'].items()},
    }

    comparison = {'current': current}

    if prev and prev['total_expense'] > 0:
        prev_expense = prev['total_expense']
        curr_expense = now['total_expense']
        change_pct = ((curr_expense - prev_expense) / prev_expense) * 100

        comparison['previous'] = {
            'income': prev['total_income'],
            'expense': prev['total_expense'],
            'balance': prev['total_income'] - prev['total_expense'],
            'categories': {k: v['total'] for k, v in prev['by_category'].items()},
        }

        comparison['change'] = {
            'expense_change_pct': round(change_pct, 1),
            'expense_change_amount': round(curr_expense - prev_expense),
            'direction': 'naik' if change_pct > 0 else 'turun',
        }

        # Category-wise changes
        cat_changes = {}
        all_cats = set(list(comparison['current']['categories'].keys()) +
                       list(comparison['previous'].get('categories', {}).keys()))
        for cat in all_cats:
            curr_val = comparison['current']['categories'].get(cat, 0)
            prev_val = comparison['previous']['categories'].get(cat, 0)
            if prev_val > 0:
                cat_pct = ((curr_val - prev_val) / prev_val) * 100
                cat_changes[cat] = {
                    'current': curr_val,
                    'previous': prev_val,
                    'change_pct': round(cat_pct, 1),
                    'direction': 'naik' if cat_pct > 0 else 'turun',
                }
        comparison['category_changes'] = cat_changes

    return comparison
