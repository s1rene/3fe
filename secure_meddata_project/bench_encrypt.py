# bench_encrypt.py
import sqlite3
import pandas as pd
import time
import os
import csv

# cryptography for Fernet (AES) and RSA
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

# --- Налаштування ---
DB_PATH = "medical_records.db"
RESULTS_DIR = "results"
CSV_OUT = os.path.join(RESULTS_DIR, "enc_bench.csv")
N_RECORDS = 200   # для тесту можна ставити 200, або 1000 якщо хочеш повний прогін

os.makedirs(RESULTS_DIR, exist_ok=True)

# --- Завантажуємо записи ---
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query(f"SELECT * FROM records LIMIT {N_RECORDS}", conn)
conn.close()

# --- Підготовка AES (Fernet) ---
fkey = Fernet.generate_key()
f = Fernet(fkey)

# --- Підготовка RSA (генеруємо ключі) ---
rsa_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
rsa_public_key = rsa_private_key.public_key()

# --- Функції для RSA (OAEP) ---
def rsa_encrypt(pubkey, plaintext_bytes):
    return pubkey.encrypt(
        plaintext_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def rsa_decrypt(privkey, ciphertext):
    return privkey.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

# --- Бенчмарк ---
results = []
for idx, row in df.iterrows():
    payload = str(row.to_dict()).encode()  # серіалізація запису у bytes

    # Fernet (AES)
    t0 = time.perf_counter()
    c_f = f.encrypt(payload)
    t1 = time.perf_counter()
    p_f = f.decrypt(c_f)
    t2 = time.perf_counter()

    # RSA (має сенс лише для невеликих payload; для великих даних RSA часто використовується для шифрування симетричного ключа)
    # Тому для порівняння ми обмежимо payload до 190 байт для RSA-OAEP з 2048 біт ключем (приблизно).
    rsa_payload = payload[:190]  # зріз, щоб уникнути помилок при RSA
    t3 = time.perf_counter()
    try:
        c_r = rsa_encrypt(rsa_public_key, rsa_payload)
        t4 = time.perf_counter()
        p_r = rsa_decrypt(rsa_private_key, c_r)
        t5 = time.perf_counter()
    except Exception as e:
        # якщо RSA не вдається (payload занадто великий), позначимо як None
        c_r = None
        p_r = None
        t4 = t5 = None

    # Записуємо результати
    res = {
        "index": int(idx),
        "len_payload": len(payload),
        "fernet_enc": t1 - t0,
        "fernet_dec": t2 - t1,
        "rsa_enc": (t4 - t3) if t4 and t3 else None,
        "rsa_dec": (t5 - t4) if t5 and t4 else None
    }
    results.append(res)

# --- Збереження у CSV ---
keys = ["index", "len_payload", "fernet_enc", "fernet_dec", "rsa_enc", "rsa_dec"]
with open(CSV_OUT, "w", newline="", encoding="utf-8") as fcsv:
    writer = csv.DictWriter(fcsv, fieldnames=keys)
    writer.writeheader()
    for r in results:
        writer.writerow(r)

print(f"✅ Бенчмарк завершено. Результати збережено у {CSV_OUT}")
