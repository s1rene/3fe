import sqlite3
import pandas as pd

# Підключення до бази
conn = sqlite3.connect("medical_records.db")

# Вибірка даних
query = "SELECT * FROM records"
df = pd.read_sql_query(query, conn)

print("📋 Дані з таблиці records:")
print(df)

conn.close()
