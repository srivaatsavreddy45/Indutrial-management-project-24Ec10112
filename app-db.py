import sqlite3

conn = sqlite3.connect("supply.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS records (
    sku TEXT,
    stock INTEGER,
    forecast REAL,
    decision TEXT
)
""")
conn.commit()


def save_result(sku, stock, forecast, decision):
    cursor.execute(
        "INSERT INTO records VALUES (?, ?, ?, ?)",
        (sku, stock, forecast, decision),
    )
    conn.commit()