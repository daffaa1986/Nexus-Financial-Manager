import re
import json
from datetime import datetime, timedelta
from collections import defaultdict

try:
    import google.generativeai as genai
    import os
    API_KEY = os.environ.get("GEMINI_API_KEY", "")
    if API_KEY:
        genai.configure(api_key=API_KEY)
        model_ai = genai.GenerativeModel('gemini-1.5-flash')
    else:
        model_ai = None
except:
    model_ai = None

def hitung_statistik_transaksi(transaksi_list):
    stats = {
        'total_income': 0,
        'total_expense': 0,
        'by_category': defaultdict(lambda: {'total': 0, 'count': 0, 'avg': 0, 'max': 0, 'items': []}),
        'by_date': defaultdict(lambda: {'total': 0, 'count': 0}),
        'by_day_of_week': defaultdict(lambda: {'total': 0, 'count': 0}),
        'small_frequent': [],
        'large_transactions': [],
        'all_expenses': [],
    }

    for t in transaksi_list:
        tipe = t.get('type', 'DB')
        amount = t.get('amount', 0)
        date = t.get('date', '')
        category = t.get('category', 'Lainnya')

        if tipe == 'CR':
            stats['total_income'] += amount
            continue

        stats['total_expense'] += amount

        stats['by_category'][category]['total'] += amount
        stats['by_category'][category]['count'] += 1
        stats['by_category'][category]['items'].append({
            'label': t.get('label', ''),
            'amount': amount,
            'date': date
        })

        if amount > stats['by_category'][category]['max']:
            stats['by_category'][category]['max'] = amount

        stats['by_date'][date]['total'] += amount
        stats['by_date'][date]['count'] += 1

        try:
            dt = datetime.strptime(date, '%Y-%m-%d')
            day_name = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'][dt.weekday()]
            stats['by_day_of_week'][day_name]['total'] += amount
            stats['by_day_of_week'][day_name]['count'] += 1
        except:
            pass

        stats['all_expenses'].append({
            'label': t.get('label', ''),
            'amount': amount,
            'date': date,
            'category': category
        })

    for cat in stats['by_category']:
        data = stats['by_category'][cat]
        data['avg'] = data['total'] / data['count'] if data['count'] > 0 else 0

    return stats

def deteksi_bocor(stats):
    bocor = []

    small_transactions = []
    for cat, data in stats['by_category'].items():
        if cat == 'Income':
            continue
        for item in data['items']:
            if item['amount'] < 50000:
                small_transactions.append(item)

    if small_transactions:
        small_by_label = defaultdict(lambda: {'total': 0, 'count': 0, 'items': []})
        for st in small_transactions:
            label_clean = re.sub(r'\d+', '', st['label']).strip()[:30]
            small_by_label[label_clean]['total'] += st['amount']
            small_by_label[label_clean]['count'] += 1
            small_by_label[label_clean]['items'].append(st)

        for label, data in small_by_label.items():
            if data['count'] >= 3 and data['total'] >= 50000:
                bocor.append({
                    'type': 'bocor',
                    'title': f'Pengeluaran kecil tapi sering: {label}',
                    'description': f'{data["count"]}x transaksi = Rp{data["total"]:,.0f}/bulan. Kecil-kecil jadi bukit!',
                    'severity': 'high' if data['total'] >= 200000 else 'medium',
                    'amount': data['total'],
                    'count': data['count'],
                    'items': data['items'][:5],
                })

    return bocor

def deteksi_boros(stats):
    boros = []

    sorted_cats = sorted(
        [(k, v) for k, v in stats['by_category'].items() if k != 'Income'],
        key=lambda x: x[1]['total'],
        reverse=True
    )

    if sorted_cats and stats['total_expense'] > 0:
        top_cat, top_data = sorted_cats[0]
        persen = (top_data['total'] / stats['total_expense']) * 100
        if persen > 40:
            boros.append({
                'type': 'boros',
                'title': f'Pengeluaran terbesar: {top_cat}',
                'description': f'{persen:.1f}% dari total pengeluaran (Rp{top_data["total"]:,.0f}). Perlu dikurangi.',
                'severity': 'high' if persen > 50 else 'medium',
                'amount': top_data['total'],
                'percentage': persen,
            })

    if stats['by_date']:
        max_date = max(stats['by_date'].items(), key=lambda x: x[1]['total'])
        if max_date[1]['total'] > stats['total_expense'] * 0.25:
            boros.append({
                'type': 'boros',
                'title': f'Hari belanja paling boros: {max_date[0]}',
                'description': f'Rp{max_date[1]["total"]:,.0f} terpakai dalam 1 hari ({max_date[1]["count"]} transaksi).',
                'severity': 'medium',
                'amount': max_date[1]['total'],
            })

    return boros

def deteksi_pola_harian(stats):
    tips = []

    if stats['by_day_of_week']:
        sorted_days = sorted(stats['by_day_of_week'].items(), key=lambda x: x[1]['total'], reverse=True)
        top_day = sorted_days[0]
        low_day = sorted_days[-1]

        if top_day[1]['total'] > low_day[1]['total'] * 2:
            tips.append({
                'type': 'tip',
                'title': f'Hari paling boros: {top_day[0]}',
                'description': f'Pengeluaran {top_day[0]} (Rp{top_day[1]["total"]:,.0f}) jauh lebih tinggi dari {low_day[0]} (Rp{low_day[1]["total"]:,.0f}).',
                'severity': 'medium',
            })

    return tips

def generate_ai_analysis(transaksi_list, receipts_list=None):
    if not transaksi_list:
        return {
            'stats': None,
            'insights': [],
            'summary': 'Belum ada data transaksi. Upload mutasi rekening atau struk belanjaan untuk mulai analisis.',
        }

    stats = hitung_statistik_transaksi(transaksi_list)

    bocor = deteksi_bocor(stats)
    boros = deteksi_boros(stats)
    pola = deteksi_pola_harian(stats)

    all_insights = bocor + boros + pola

    if receipts_list:
        receipt_stats = defaultdict(lambda: {'total': 0, 'count': 0})
        for r in receipts_list:
            store = r.get('store_name', 'Toko')
            receipt_stats[store]['total'] += r.get('total', 0)
            receipt_stats[store]['count'] += 1

        top_receipt_stores = sorted(receipt_stats.items(), key=lambda x: x[1]['total'], reverse=True)[:5]
        for store, data in top_receipt_stores:
            if data['count'] >= 2:
                all_insights.append({
                    'type': 'bocor',
                    'title': f'Sering belanja di: {store}',
                    'description': f'{data["count"]}x belanja = Rp{data["total"]:,.0f} total.',
                    'severity': 'medium',
                    'amount': data['total'],
                })

    all_insights.sort(key=lambda x: {'high': 3, 'medium': 2, 'low': 1}.get(x.get('severity', 'low'), 0), reverse=True)

    savings_rate = stats.get('savings_rate') if isinstance(stats, dict) and 'savings_rate' in stats else (
        ((stats['total_income'] - stats['total_expense']) / stats['total_income'] * 100)
        if stats['total_income'] > 0 else 0
    )

    summary_lines = []
    summary_lines.append(f"Total Pemasukan: Rp{stats['total_income']:,.0f}")
    summary_lines.append(f"Total Pengeluaran: Rp{stats['total_expense']:,.0f}")
    summary_lines.append(f"Saldo Bersih: Rp{stats['total_income'] - stats['total_expense']:,.0f}")
    summary_lines.append(f"Rasio Tabungan: {savings_rate:.1f}%")
    summary_lines.append(f"Jumlah Transaksi: {len(transaksi_list)}")

    if all_insights:
        high_count = sum(1 for i in all_insights if i.get('severity') == 'high')
        if high_count > 0:
            summary_lines.append(f"\nAda {high_count} masalah serius yang perlu diperhatikan!")
        else:
            summary_lines.append("\nKeuangan dalam kondisi cukup baik.")
    else:
        summary_lines.append("\nTidak ada masalah signifikan terdeteksi.")

    stats_formatted = {
        'income': stats['total_income'],
        'expense': stats['total_expense'],
        'balance': stats['total_income'] - stats['total_expense'],
        'savings_rate': round(savings_rate, 1),
        'by_category': {k: {'total': v['total'], 'count': v['count'], 'avg': round(v['avg'])} for k, v in stats['by_category'].items()},
        'by_date': dict(stats['by_date']),
        'by_day_of_week': dict(stats['by_day_of_week']),
    }

    return {
        'stats': stats_formatted,
        'insights': all_insights[:15],
        'summary': "\n".join(summary_lines),
        'bocor_count': len(bocor),
        'boros_count': len(boros),
    }

def generate_monthly_comparison(transaksi_bulan_ini, transaksi_bulan_lalu):
    if not transaksi_bulan_ini:
        return {'error': 'Tidak ada data bulan ini'}

    stats_now = hitung_statistik_transaksi(transaksi_bulan_ini)
    stats_prev = hitung_statistik_transaksi(transaksi_bulan_lalu) if transaksi_bulan_lalu else None

    comparison = {
        'current': {
            'income': stats_now['total_income'],
            'expense': stats_now['total_expense'],
            'balance': stats_now['total_income'] - stats_now['total_expense'],
            'categories': {k: v['total'] for k, v in stats_now['by_category'].items() if k != 'Income'},
        }
    }

    if stats_prev:
        prev_expense = stats_prev['total_expense']
        curr_expense = stats_now['total_expense']
        change_pct = ((curr_expense - prev_expense) / prev_expense * 100) if prev_expense > 0 else 0

        comparison['previous'] = {
            'income': stats_prev['total_income'],
            'expense': stats_prev['total_expense'],
            'balance': stats_prev['total_income'] - stats_prev['total_expense'],
            'categories': {k: v['total'] for k, v in stats_prev['by_category'].items() if k != 'Income'},
        }
        comparison['change'] = {
            'expense_change_pct': round(change_pct, 1),
            'expense_change_amount': round(curr_expense - prev_expense),
            'direction': 'naik' if change_pct > 0 else 'turun',
        }

        cat_changes = {}
        all_cats = set(list(comparison['current']['categories'].keys()) + list(comparison['previous']['categories'].keys()))
        for cat in all_cats:
            curr_val = comparison['current']['categories'].get(cat, 0)
            prev_val = comparison['previous']['categories'].get(cat, 0)
            if prev_val > 0:
                cat_pct = ((curr_val - prev_val) / prev_val * 100)
                cat_changes[cat] = {
                    'current': curr_val,
                    'previous': prev_val,
                    'change_pct': round(cat_pct, 1),
                    'direction': 'naik' if cat_pct > 0 else 'turun'
                }
        comparison['category_changes'] = cat_changes

    return comparison
