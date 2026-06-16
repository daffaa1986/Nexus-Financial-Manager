"""
PostgreSQL Database Configuration for Nexus Finance
====================================================

To use PostgreSQL instead of SQLite:
1. Install: pip install psycopg2-binary sqlalchemy
2. Create database 'nexus_finance' in PostgreSQL
3. Update .env file with your PostgreSQL credentials

.env configuration:
    DB_TYPE=postgresql
    PGHOST=localhost
    PGPORT=5432
    PGDATABASE=nexus_finance
    PGUSER=postgres
    PGPASSWORD=your_password
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

def get_postgres_engine():
    host = os.environ.get("PGHOST", "localhost")
    port = os.environ.get("PGPORT", "5432")
    database = os.environ.get("PGDATABASE", "nexus_finance")
    user = os.environ.get("PGUSER", "postgres")
    password = os.environ.get("PGPASSWORD", "")
    db_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    return create_engine(db_url, pool_size=10, max_overflow=20)

def get_postgres_session():
    engine = get_postgres_engine()
    Session = sessionmaker(bind=engine)
    return Session()

def init_postgres_db():
    engine = get_postgres_engine()

    engine.execute(text("""
        CREATE TABLE IF NOT EXISTS transactions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER DEFAULT 1,
            date DATE,
            label VARCHAR(255),
            amount DECIMAL(15,2) DEFAULT 0,
            category VARCHAR(100),
            type VARCHAR(3) DEFAULT 'DB',
            source VARCHAR(50) DEFAULT 'mutation',
            source_file VARCHAR(255),
            month INTEGER,
            year INTEGER,
            bank VARCHAR(50) DEFAULT 'BCA',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))
    engine.execute(text("CREATE INDEX IF NOT EXISTS idx_trx_month_year ON transactions (month, year)"))
    engine.execute(text("CREATE INDEX IF NOT EXISTS idx_trx_category ON transactions (category)"))
    engine.execute(text("CREATE INDEX IF NOT EXISTS idx_trx_date ON transactions (date)"))

    engine.execute(text("""
        CREATE TABLE IF NOT EXISTS receipts (
            id SERIAL PRIMARY KEY,
            user_id INTEGER DEFAULT 1,
            store_name VARCHAR(255),
            total_amount DECIMAL(15,2) DEFAULT 0,
            date DATE,
            items JSONB,
            raw_ocr_text TEXT,
            image_path VARCHAR(500),
            category VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))
    engine.execute(text("CREATE INDEX IF NOT EXISTS idx_receipt_store ON receipts (store_name)"))
    engine.execute(text("CREATE INDEX IF NOT EXISTS idx_receipt_date ON receipts (date)"))

    engine.execute(text("""
        CREATE TABLE IF NOT EXISTS goals (
            id SERIAL PRIMARY KEY,
            user_id INTEGER DEFAULT 1,
            name VARCHAR(255),
            target_amount DECIMAL(15,2),
            current_amount DECIMAL(15,2) DEFAULT 0,
            deadline DATE,
            category VARCHAR(100) DEFAULT 'Savings',
            status VARCHAR(20) DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))

    engine.execute(text("""
        CREATE TABLE IF NOT EXISTS budgets (
            id SERIAL PRIMARY KEY,
            user_id INTEGER DEFAULT 1,
            category VARCHAR(100),
            monthly_limit DECIMAL(15,2),
            month INTEGER,
            year INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (user_id, category, month, year)
        )
    """))

    engine.execute(text("""
        CREATE TABLE IF NOT EXISTS spending_insights (
            id SERIAL PRIMARY KEY,
            user_id INTEGER DEFAULT 1,
            insight_type VARCHAR(50),
            title VARCHAR(255),
            description TEXT,
            amount DECIMAL(15,2),
            severity VARCHAR(10) DEFAULT 'medium',
            month INTEGER,
            year INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))

    print("PostgreSQL Database tables created/verified!")

def simpan_transaksi_postgres(data_list, filename, bank='BCA'):
    session = get_postgres_session()
    try:
        if not data_list:
            return

        sample_date = data_list[0].get('date', '')
        from datetime import datetime
        try:
            dt = datetime.strptime(sample_date, "%Y-%m-%d")
            bulan, tahun = dt.month, dt.year
        except:
            bulan, tahun = datetime.now().month, datetime.now().year

        session.execute(
            text("DELETE FROM transactions WHERE month = :bulan AND year = :tahun AND source_file = :filename"),
            {'bulan': bulan, 'tahun': tahun, 'filename': filename}
        )

        for trx in data_list:
            try:
                dt = datetime.strptime(trx['date'], "%Y-%m-%d")
            except:
                dt = datetime.now()

            session.execute(
                text("""INSERT INTO transactions (user_id, date, label, amount, category, type, source, source_file, month, year, bank)
                        VALUES (1, :date, :label, :amount, :cat, :type, 'mutation', :file, :month, :year, :bank)"""),
                {
                    'date': trx['date'], 'label': trx['label'], 'amount': trx['amount'],
                    'cat': trx['category'], 'type': trx.get('type', 'DB'),
                    'file': filename, 'month': dt.month, 'year': dt.year, 'bank': bank
                }
            )

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error PostgreSQL simpan_transaksi: {e}")
    finally:
        session.close()
