# database_setup.py
# ------------------------------
# Створення тестової бази даних медичних записів (SQLite + CSV)
# для експериментального середовища

import sqlite3
import pandas as pd
import os

# --- 1. Створюємо CSV-файл з тестовими даними ---
data = {
    "patient_id": [101, 102, 103, 104, 105],
    "full_name": ["Іваненко І.І.", "Петренко О.М.", "Сидоренко В.П.", "Коваленко Л.М.", "Мельник Т.Г."],
    "diagnosis": ["ГРВІ", "Пневмонія", "Діабет", "Гіпертонія", "Алергія"],
    "medication": ["Парацетамол", "Азитроміцин", "Інсулін", "Еналаприл", "Цетиризин"],
    "doctor_id": [1, 2, 3, 4, 5],
    "record_date": ["2025-10-01", "2025-10-02", "2025-10-03", "2025-10-04", "2025-10-05"]
}

df = pd.DataFrame(data)
df.to_csv("medical_records.csv", index=False, encoding="utf-8")
print("✅ Створено файл medical_records.csv")

# --- 2. Створюємо базу даних SQLite ---
conn = sqlite3.connect("medical_records.db")
df.to_sql("records", conn, if_exists="replace", index=False)
conn.commit()
conn.close()

print("✅ Створено базу даних medical_records.db та таблицю 'records'")
