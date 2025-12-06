# generate_medical_data.py
# ------------------------------
# Генерація 1000 тестових медичних записів для експерименту
# Створює medical_records.csv і базу medical_records.db

import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta

# --- 1. Початкові списки для генерації випадкових даних ---
names = [
    "Іваненко І.І.", "Петренко О.М.", "Сидоренко В.П.", "Коваленко Л.М.", "Мельник Т.Г.",
    "Шевченко А.В.", "Григоренко С.О.", "Лисенко О.П.", "Бондар Т.В.", "Романюк В.С.",
    "Дмитренко І.М.", "Кравчук Ю.А.", "Онищенко О.М.", "Семенюк А.В.", "Захарченко І.В."
]
diagnoses = [
    "ГРВІ", "Пневмонія", "Гіпертонія", "Діабет", "Алергія", "Мігрень", "Отит", "Гастрит", "Бронхіт", "Анемія"
]
medications = [
    "Парацетамол", "Азитроміцин", "Інсулін", "Еналаприл", "Цетиризин",
    "Ібупрофен", "Амоксицилін", "Но-шпа", "Лоратадин", "Магній В6"
]

# --- 2. Генерація 1000 записів ---
records = []
for i in range(1, 1001):
    patient_id = i
    full_name = random.choice(names)
    diagnosis = random.choice(diagnoses)
    medication = random.choice(medications)
    doctor_id = random.randint(1, 50)
    record_date = (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 300))).strftime("%Y-%m-%d")
    records.append([patient_id, full_name, diagnosis, medication, doctor_id, record_date])

# --- 3. Створення DataFrame ---
df = pd.DataFrame(records, columns=["patient_id", "full_name", "diagnosis", "medication", "doctor_id", "record_date"])

# --- 4. Збереження у CSV ---
df.to_csv("medical_records.csv", index=False, encoding="utf-8")
print("✅ Файл medical_records.csv створено успішно!")

# --- 5. Створення бази даних SQLite ---
conn = sqlite3.connect("medical_records.db")
df.to_sql("records", conn, if_exists="replace", index=False)
conn.commit()
conn.close()

print("✅ База даних medical_records.db створена успішно!")
print("📊 Кількість записів у таблиці: 1000")
