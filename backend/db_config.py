import sqlite3

DB_NAME = "nexus_finance.db"

def init_db():
    """Fungsi ini akan membuat file database dan tabel jika belum ada."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Membuat blueprint tabel penyimpanan transaksi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            label TEXT,
            amount REAL,
            category TEXT,
            type TEXT,
            source_file TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("🗄️ Sistem Database Aktif & Siap Menerima Data!")

def simpan_transaksi(data_list, filename):
    """Fungsi untuk memasukkan data hasil tebakan AI ke dalam tabel."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    for trx in data_list:
        cursor.execute('''
            INSERT INTO transactions (date, label, amount, category, type, source_file)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (trx['date'], trx['label'], trx['amount'], trx['category'], trx.get('type', 'DB'), filename))
        
    conn.commit()
    conn.close()

# Tambahkan di baris paling bawah db_config.py
def ambil_semua_transaksi():
    """Fungsi untuk menarik data dari database untuk ditampilkan ke web."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Agar data keluar dalam bentuk Dictionary (JSON)
    cursor = conn.cursor()
    
    # Ambil 50 transaksi terakhir
    cursor.execute('SELECT * FROM transactions ORDER BY id DESC LIMIT 50')
    rows = cursor.fetchall()
    conn.close()
    
    # Ubah formatnya agar mudah dibaca oleh JavaScript
    return [dict(row) for row in rows]
