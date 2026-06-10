import psycopg2
from datetime import datetime

def load_rates(conn, data):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS raw_exchange_rates (
                id SERIAL PRIMARY KEY,
                base_currency VARCHAR(5),
                target_currency VARCHAR(5),
                rate FLOAT,
                rate_date TIMESTAMP,
                loaded_at TIMESTAMP DEFAULT NOW()
            );
        """)
        for currency, rate in data["rates"].items():
            cur.execute("""
                INSERT INTO raw_exchange_rates (base_currency, target_currency, rate, rate_date)
                VALUES (%s, %s, %s, %s)
            """, (data["base"], currency, rate, data["timestamp"]))
        conn.commit()
    print(f"Loaded {len(data['rates'])} rates.")
