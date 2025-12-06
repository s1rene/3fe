import sqlite3
import pandas as pd

# Підключення до бази
conn = sqlite3.connect("medical_records.db")

# Перевірка кількості записів
query = "SELECT COUNT(*) AS total FROM records"
df = pd.read_sql_query(query, conn)
print("🔎 Загальна кількість записів у базі:", int(df['total'][0]))

# Перегляд перших 5 записів
preview = pd.read_sql_query("SELECT * FROM records LIMIT 5", conn)
print("\n📋 Перші 5 записів:")
print(preview)

conn.close()
