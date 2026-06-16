"""
Helpers
========
Fungsi bantu untuk AI/ML system.
"""

from datetime import datetime


def parse_date_to_month_year(date_str):
    """Extract month and year from date string."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.month, dt.year
    except:
        try:
            parts = date_str.split('-')
            return int(parts[1]), int(parts[0])
        except:
            now = datetime.now()
            return now.month, now.year


def format_rupiah(amount):
    """Format number to Indonesian Rupiah string."""
    return f"Rp {amount:,.0f}".replace(',', '.')


def extract_bulan_tahun_dari_list(transaksi_list):
    """Get a set of (month, year) pairs from a transaction list."""
    dates = set()
    for t in transaksi_list:
        try:
            dt = datetime.strptime(t.get('date', ''), '%Y-%m-%d')
            dates.add((dt.month, dt.year))
        except:
            pass
    return sorted(dates)
