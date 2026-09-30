import sqlite3

DB_NAME = "crm_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. جدول مشتریان و لیدها (Leads)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform TEXT NOT NULL,          -- telegram / instagram
        user_id TEXT UNIQUE NOT NULL,    -- شناسه کاربر
        username TEXT,                   -- یوزرنیم کاربر
        category TEXT,                   -- یکی از ۴ شاخه اصلی
        status TEXT DEFAULT 'New',       -- New, Qualified, Active_Nurturing, Handoff, Closed
        discount_requested REAL DEFAULT 0.0,
        deal_value REAL DEFAULT 0.0,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 2. جدول صف پیگیری‌های خودکار (Follow-ups)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS followups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lead_id INTEGER NOT NULL,
        step INTEGER NOT NULL,           -- 1: 3 hours, 2: 24 hours, 3: 72 hours
        scheduled_time TIMESTAMP NOT NULL,
        status TEXT DEFAULT 'pending',   -- pending, sent, cancelled
        FOREIGN KEY (lead_id) REFERENCES leads (id)
    )
    """)

    conn.commit()
    conn.close()
    print("[OK] Database and CRM tables initialized successfully.")

if __name__ == "__main__":
    init_db()
