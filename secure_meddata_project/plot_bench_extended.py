# plot_bench_extended.py
import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv("results/enc_bench.csv")
df['rsa_enc'] = pd.to_numeric(df['rsa_enc'], errors='coerce')
df['rsa_dec'] = pd.to_numeric(df['rsa_dec'], errors='coerce')

os.makedirs("results", exist_ok=True)

# Bar chart mean times
means = {
    "Fernet enc": df['fernet_enc'].mean(),
    "Fernet dec": df['fernet_dec'].mean(),
    "RSA enc": df['rsa_enc'].mean(),
    "RSA dec": df['rsa_dec'].mean()
}
labels = list(means.keys())
values = [v if pd.notna(v) else 0 for v in means.values()]

plt.figure(figsize=(8,5))
plt.bar(labels, values)
plt.ylabel("Час (с)")
plt.title("Середній час операцій (Fernet vs RSA)")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig("results/mean_times.png")
plt.show()

# Boxplot (only methods with data)
data_for_box = []
labels_box = []
if df['fernet_enc'].notna().any():
    data_for_box.append(df['fernet_enc'].dropna())
    labels_box.append('Fernet enc')
if df['rsa_enc'].notna().any():
    data_for_box.append(df['rsa_enc'].dropna())
    labels_box.append('RSA enc')

if data_for_box:
    plt.figure(figsize=(8,5))
    plt.boxplot(data_for_box, labels=labels_box)
    plt.ylabel("Час (с)")
    plt.title("Розподіл часу шифрування")
    plt.tight_layout()
    plt.savefig("results/box_enc.png")
    plt.show()

print("Графіки збережено в папці results/")
