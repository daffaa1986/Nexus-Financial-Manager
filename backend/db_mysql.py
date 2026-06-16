"""
MySQL Database Configuration for Nexus Finance
================================================

To use MySQL instead of SQLite:
1. Install: pip install pymysql sqlalchemy
2. Create database 'nexus_finance' in MySQL
3. Update .env file with your MySQL credentials

.env configuration:
    DB_TYPE=mysql
    MYSQL_HOST=localhost
    MYSQL_PORT=3306
    MYSQL_DATABASE=nexus_finance
    MYSQL_USER=root
    MYSQL_PASSWORD=your_password
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

def get_mysql_engine():
    host = os.environ.get("MYSQL_HOST", "localhost")
    port = os.environ.get("MYSQL_PORT", "3306")
    database = os.environ.get("MYSQL_DATABASE", "nexus_finance")
    user = os.environ.get("MYSQL_USER", "root")
    password = os.environ.get("MYSQL_PASSWORD", "")
    db_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4"
    return create_engine(db_url, pool_size=10, max_overflow=20)

def get_mysql_session():
    engine = get_mysql_engine()
    Session = sessionmaker(bind=engine)
    return Session()

def init_mysql_db():
    engine = get_mysql_engine()
    
    # Create tables if they don't exist
    engine.execute(text("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT DEFAULT 1,
            date DATE,
            label VARCHAR(255),
            amount DECIMAL(15,2) DEFAULT 0,
            category VARCHAR(100),
            type ENUM('DB', 'CR') DEFAULT 'DB',
            source VARCHAR(50) DEFAULT 'mutation',
            source_file VARCHAR(255),
            month INT,
            year INT,
            bank VARCHAR(50) DEFAULT 'BCA',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_month_year (month, year),
            INDEX idx_category (category),
            INDEX idx_date (date)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """))

    engine.execute(text("""
        CREATE TABLE IF NOT EXISTS receipts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT DEFAULT 1,
            store_name VARCHAR(255),
            total_amount DECIMAL(15,2) DEFAULT 0,
            date DATE,
            items JSON,
            raw_ocr_text TEXT,
            image_path VARCHAR(500),
            category VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_store (store_name),
            INDEX idx_date (date)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """))

    engine.execute(text("""
        CREATE TABLE IF NOT EXISTS goals (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT DEFAULT 1,
            name VARCHAR(255),
            target_amount DECIMAL(15,2),
            current_amount DECIMAL(15,2) DEFAULT 0,
            deadline DATE,
            category VARCHAR(100) DEFAULT 'Savings',
            status ENUM('active', 'completed', 'cancelled') DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """))

    engine.execute(text("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT DEFAULT 1,
            category VARCHAR(100),
            monthly_limit DECIMAL(15,2),
            month INT,
            year INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY uq_budget (user_id, category, month, year)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """))

    engine.execute(text("""
        CREATE TABLE IF NOT EXISTS spending_insights (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT DEFAULT 1,
            insight_type VARCHAR(50),
            title VARCHAR(255),
            description TEXT,
            amount DECIMAL(15,2),
            severity ENUM('high', 'medium', 'low') DEFAULT 'medium',
            month INT,
            year INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """))

    print("MySQL Database tables created/verified!")

def simpan_transaksi_mysql(data_list, filename, bank='BCA'):
    session = get_mysql_session()
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

        # Delete existing data for same month
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
        print(f"Error MySQL simpan_transaksi: {e}")
    finally:
        session.close()
