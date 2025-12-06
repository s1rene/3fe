# analyze_bench.py
import pandas as pd
import numpy as np

df = pd.read_csv("results/enc_bench.csv")

# Перетворюємо RSA поля в числа (якщо там пусті -> NaN)
df['rsa_enc'] = pd.to_numeric(df['rsa_enc'], errors='coerce')
df['rsa_dec'] = pd.to_numeric(df['rsa_dec'], errors='coerce')

def stats(series):
    return {
        "count": int(series.count()),
        "mean": float(series.mean()) if series.count()>0 else None,
        "std": float(series.std()) if series.count()>0 else None,
        "min": float(series.min()) if series.count()>0 else None,
        "max": float(series.max()) if series.count()>0 else None
    }

print("=== Fernet (AES) encrypt stats ===")
print(stats(df['fernet_enc']))
print("=== Fernet (AES) decrypt stats ===")
print(stats(df['fernet_dec']))

print("\n=== RSA encrypt stats ===")
print(stats(df['rsa_enc']))
print("=== RSA decrypt stats ===")
print(stats(df['rsa_dec']))

# throughput (опер/с) оцінка
total_enc_time_fernet = df['fernet_enc'].sum()
throughput_fernet = len(df) / total_enc_time_fernet if total_enc_time_fernet>0 else None
print(f"\nThroughput Fernet (ops/s): {throughput_fernet:.2f}" if throughput_fernet else "No data")
