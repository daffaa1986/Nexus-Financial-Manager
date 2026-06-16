import sqlite3
from datetime import datetime

DB_NAME = "nexus_finance.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            date TEXT,
            label TEXT,
            amount REAL,
            category TEXT,
            type TEXT,
            source TEXT DEFAULT 'mutation',
            source_file TEXT,
            month INTEGER,
            year INTEGER,
            bank TEXT DEFAULT 'BCA',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            store_name TEXT,
            total_amount REAL,
            date TEXT,
            items TEXT,
            raw_ocr_text TEXT,
            image_path TEXT,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            name TEXT,
            target_amount REAL,
            current_amount REAL DEFAULT 0,
            deadline TEXT,
            category TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            category TEXT,
            monthly_limit REAL,
            month INTEGER,
            year INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS spending_insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            insight_type TEXT,
            title TEXT,
            description TEXT,
            amount REAL,
            severity TEXT,
            month INTEGER,
            year INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uploaded_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            file_hash TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("Database aktif & siap!")

def _parse_date_to_month_year(date_str):
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

def simpan_transaksi(data_list, filename, bank='BCA'):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if not data_list:
        conn.close()
        return

    sample_date = data_list[0].get('date', '')
    bulan, tahun = _parse_date_to_month_year(sample_date)

    cursor.execute('DELETE FROM transactions WHERE month = ? AND year = ? AND source_file = ?', (bulan, tahun, filename))

    for trx in data_list:
        bulan_trx, tahun_trx = _parse_date_to_month_year(trx.get('date', ''))
        cursor.execute('''
            INSERT INTO transactions (user_id, date, label, amount, category, type, source, source_file, month, year, bank)
            VALUES (1, ?, ?, ?, ?, ?, 'mutation', ?, ?, ?, ?)
        ''', (trx['date'], trx['label'], trx['amount'], trx['category'], trx.get('type', 'DB'), filename, bulan_trx, tahun_trx, bank))

    conn.commit()
    conn.close()

def simpan_receipt(data_list, image_path=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for item in data_list:
        cursor.execute('''
            INSERT INTO receipts (user_id, store_name, total_amount, date, items, raw_ocr_text, image_path, category)
            VALUES (1, ?, ?, ?, ?, ?, ?, ?)
        ''', (item.get('store_name', ''), item.get('total_amount', 0), item.get('date', ''),
              str(item.get('items', [])), item.get('raw_ocr_text', ''), image_path or '',
              item.get('category', 'Lainnya')))

    conn.commit()
    conn.close()

def ambil_semua_transaksi():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions ORDER BY date DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def ambil_transaksi_per_bulan(bulan, tahun):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions WHERE month = ? AND year = ? ORDER BY date ASC', (bulan, tahun))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def ambil_transaksi_per_rentang(tgl_awal, tgl_akhir):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions WHERE date BETWEEN ? AND ? ORDER BY date ASC', (tgl_awal, tgl_akhir))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def ambil_semua_receipt():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM receipts ORDER BY date DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def ambil_goals():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM goals WHERE status = "active" ORDER BY deadline ASC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def tambah_goal(name, target_amount, deadline, category):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO goals (name, target_amount, deadline, category) VALUES (?, ?, ?, ?)',
                   (name, target_amount, deadline, category))
    conn.commit()
    conn.close()

def ambil_budgets(bulan, tahun):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM budgets WHERE month = ? AND year = ?', (bulan, tahun))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def simpan_budget(category, monthly_limit, bulan, tahun):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM budgets WHERE category = ? AND month = ? AND year = ?', (category, bulan, tahun))
    cursor.execute('INSERT INTO budgets (category, monthly_limit, month, year) VALUES (?, ?, ?, ?)',
                   (category, monthly_limit, bulan, tahun))
    conn.commit()
    conn.close()

def ambil_ringkasan_bulan(bulan, tahun):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT SUM(amount) as total FROM transactions WHERE month = ? AND year = ? AND type = "CR"', (bulan, tahun))
    income = cursor.fetchone()['total'] or 0

    cursor.execute('SELECT SUM(amount) as total FROM transactions WHERE month = ? AND year = ? AND type = "DB"', (bulan, tahun))
    expense = cursor.fetchone()['total'] or 0

    cursor.execute('SELECT category, SUM(amount) as total FROM transactions WHERE month = ? AND year = ? AND type = "DB" GROUP BY category ORDER BY total DESC', (bulan, tahun))
    kategori = [dict(row) for row in cursor.fetchall()]

    cursor.execute('SELECT COUNT(*) as total FROM transactions WHERE month = ? AND year = ?', (bulan, tahun))
    trx_count = cursor.fetchone()['total']

    cursor.execute('SELECT COUNT(*) as total FROM receipts WHERE substr(date, 1, 7) = ?', (f'{tahun:04d}-{bulan:02d}',))
    receipt_count = cursor.fetchone()['total']

    conn.close()
    return {
        'income': income,
        'expense': expense,
        'balance': income - expense,
        'savings_rate': round(((income - expense) / income * 100), 1) if income > 0 else 0,
        'kategori': kategori,
        'trx_count': trx_count,
        'receipt_count': receipt_count
    }

def cek_dan_simpan_file_hash(filename, file_hash):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO uploaded_files (filename, file_hash) VALUES (?, ?)', (filename, file_hash))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Hash already exists in the database
        conn.close()
        return False

