"""
Insight Engine
==============
Menggabungkan semua detektor + AI LLM untuk menghasilkan insight keuangan.
"""

from collections import defaultdict
from ..config import GEMINI_API_KEY
from .bocor_detector import deteksi as deteksi_bocor
from .boros_detector import deteksi as deteksi_boros
from .pola_analyzer import analisis_harian
from .comparison import hitung_statistik


def generate_analysis(transaksi_list, receipts_list=None):
    """
    Main analysis function.
    Returns: { stats, insights, summary, bocor_count, boros_count }
    """
    if not transaksi_list:
        return {
            'stats': None,
            'insights': [],
            'summary': 'Belum ada data transaksi. Upload mutasi atau struk untuk mulai analisis.',
            'bocor_count': 0,
            'boros_count': 0,
        }

    stats = hitung_statistik(transaksi_list)
    total_expense = stats['total_expense']

    # Run all detectors
    bocor = deteksi_bocor(transaksi_list)
    boros = deteksi_boros(transaksi_list, total_expense)
    pola = analisis_harian(transaksi_list)

    all_insights = bocor + boros + pola

    # Add receipt-based insights if available
    if receipts_list:
        receipt_store_insights = _analyze_receipt_stores(receipts_list)
        all_insights.extend(receipt_store_insights)

    # Sort severity
    severity_order = {'high': 3, 'medium': 2, 'low': 1}
    all_insights.sort(key=lambda x: severity_order.get(x.get('severity', 'low'), 0), reverse=True)

    # Build summary
    savings_rate = ((stats['total_income'] - stats['total_expense']) / stats['total_income'] * 100) \
        if stats['total_income'] > 0 else 0

    summary_lines = [
        f"Total Pemasukan: Rp{stats['total_income']:,.0f}",
        f"Total Pengeluaran: Rp{stats['total_expense']:,.0f}",
        f"Saldo Bersih: Rp{stats['total_income'] - stats['total_expense']:,.0f}",
        f"Rasio Tabungan: {savings_rate:.1f}%",
        f"Jumlah Transaksi: {len(transaksi_list)}",
    ]

    high_count = sum(1 for i in all_insights if i.get('severity') == 'high')
    if high_count > 0:
        summary_lines.append(f"\nAda {high_count} masalah serius yang perlu diperhatikan!")
    else:
        summary_lines.append("\nKeuangan dalam kondisi cukup baik.")

    return {
        'stats': {
            'income': stats['total_income'],
            'expense': stats['total_expense'],
            'balance': stats['total_income'] - stats['total_expense'],
            'savings_rate': round(savings_rate, 1),
            'by_category': stats['by_category'],
            'by_day_of_week': stats['by_day_of_week'],
        },
        'insights': all_insights[:15],
        'summary': "\n".join(summary_lines),
        'bocor_count': len(bocor),
        'boros_count': len(boros),
    }


def _analyze_receipt_stores(receipts_list):
    """Analyze receipt store patterns for additional insights."""
    insights = []
    store_stats = defaultdict(lambda: {'total': 0, 'count': 0})

    for r in receipts_list:
        store = r.get('store_name', 'Toko')
        store_stats[store]['total'] += r.get('total_amount', 0)
        store_stats[store]['count'] += 1

    for store, data in store_stats.items():
        if data['count'] >= 2:
            insights.append({
                'type': 'bocor',
                'title': f'Sering belanja di: {store}',
                'description': f'{data["count"]}x belanja = Rp{data["total"]:,.0f} total.',
                'severity': 'medium',
                'amount': data['total'],
            })

    return insights


def generate_llm_insights(transaksi_list):
    """Generate AI insights using Gemini LLM (advanced analysis)."""
    if not transaksi_list:
        return []

    import re
    import json

    # Prepare data summary for LLM
    summary = {}
    for t in transaksi_list:
        cat = t.get('category', 'Lainnya')
        if cat not in summary:
            summary[cat] = {'total': 0, 'count': 0, 'items': []}
        if t.get('type') == 'DB':
            summary[cat]['total'] += t.get('amount', 0)
            summary[cat]['count'] += 1
            if len(summary[cat]['items']) < 3:
                summary[cat]['items'].append(f"{t.get('label', '')} Rp{t.get('amount', 0):,.0f}")

    deskripsi = "\n".join([
        f"- {cat}: Rp{data['total']:,.0f} ({data['count']} transaksi) "
        f"Contoh: {', '.join(data['items'])}"
        for cat, data in summary.items() if data['count'] > 0
    ])

    if not deskripsi:
        return []

    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = f"""Analisis data pengeluaran berikut dan berikan insight dalam Bahasa Indonesia:

{deskripsi}

Berikan 3-5 insight dengan format JSON array:
[
  {{
    "type": "bocor" atau "boros" atau "tip" atau "good",
    "title": "Judul singkat",
    "description": "Penjelasan 1-2 kalimat",
    "severity": "high" atau "medium" atau "low"
  }}
]"""

        response = model.generate_content(prompt)
        text = response.text.strip()
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*$', '', text)

        return json.loads(text)
    except Exception as e:
        print(f"Error LLM insights: {e}")
        return []
