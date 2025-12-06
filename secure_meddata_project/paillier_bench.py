# paillier_bench.py
from phe import paillier
import sqlite3, pandas as pd, time, os

DB="medical_records.db"
N=200
conn = sqlite3.connect(DB)
df = pd.read_sql_query(f"SELECT * FROM records LIMIT {N}", conn)
conn.close()

public_key, private_key = paillier.generate_paillier_keypair(n_length=1024)

enc_times = []
op_times = []
dec_times = []

for idx, row in df.iterrows():
    payload = len(str(row.to_dict()))
    # Для демонстрації беремо число (наприклад patient_id) — Paillier оперує над числами
    a = int(row['patient_id'])

    t0 = time.perf_counter()
    c = public_key.encrypt(a)
    t1 = time.perf_counter()

    # Приклад гомоморфної операції: додавання (складаємо зашифровані значення)
    t2 = time.perf_counter()
    c_sum = c + public_key.encrypt(5)  # додаємо 5 як приклад
    t3 = time.perf_counter()

    t4 = time.perf_counter()
    dec = private_key.decrypt(c_sum)
    t5 = time.perf_counter()

    enc_times.append(t1 - t0)
    op_times.append(t3 - t2)
    dec_times.append(t5 - t4)

import statistics, csv, os
os.makedirs("results", exist_ok=True)
with open("results/paillier_bench.csv","w",newline="",encoding="utf-8") as f:
    writer=csv.writer(f)
    writer.writerow(["enc_mean","op_mean","dec_mean"])
    writer.writerow([statistics.mean(enc_times), statistics.mean(op_times), statistics.mean(dec_times)])

print("Paillier benchmark done. Results saved to results/paillier_bench.csv")
