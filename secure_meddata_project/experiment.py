# experiment.py
# ----------------------------------------
# Експериментальна перевірка системи захисту медичних даних
# Підключення до БД, шифрування записів, аудит і заміри часу

import sqlite3
import pandas as pd
import time
import hashlib
from encrypt_he import aes_encrypt_decrypt
from blockchain_audit import Blockchain, Block
from auth_3fa import authenticate_user
import matplotlib.pyplot as plt

# --- 1. Етап автентифікації ---
print("=== ЕТАП 1: АУТЕНТИФІКАЦІЯ ===")
if authenticate_user():
    print("✅ Доступ користувача підтверджено!\n")
    current_user = "authenticated_user"  # можна змінити на реальний ID користувача
else:
    print("❌ Відмова у доступі.")
    exit()

# --- 2. Підключення до бази даних ---
print("=== ЕТАП 2: З'ЄДНАННЯ З БАЗОЮ ДАНИХ ===")
conn = sqlite3.connect("medical_records.db")
df = pd.read_sql_query("SELECT * FROM records LIMIT 1000", conn)
conn.close()
print(f"📊 Завантажено {len(df)} медичних записів.\n")

# --- 3. Ініціалізація блокчейну ---
blockchain = Blockchain()

# Додавання початкового запису в блокчейн
genesis_block = Block(
    index=len(blockchain.chain),
    timestamp=time.time(),
    user_id=current_user,
    action="User authenticated",
    data_hash="0"
)
blockchain.add_block(genesis_block)

# --- 4. Експеримент із шифруванням ---
print("=== ЕТАП 3: ШИФРУВАННЯ ТА АНАЛІЗ ===")
times = []

for i, row in df.iterrows():
    start = time.time()
    encrypted, decrypted = aes_encrypt_decrypt(str(row.to_dict()))
    end = time.time()
    times.append(end - start)
    
    # Додавання блоку для кожного зашифрованого запису
    new_block = Block(
        index=len(blockchain.chain),
        timestamp=time.time(),
        user_id=current_user,
        action=f"Encrypted record {row['patient_id']}",
        data_hash=hashlib.sha256(str(encrypted).encode()).hexdigest()
    )
    blockchain.add_block(new_block)
    
    if i % 200 == 0:
        print(f"🔒 Оброблено {i} записів...")

avg_time = sum(times) / len(times)
print(f"\n⏱️ Середній час шифрування одного запису: {avg_time:.4f} с")

# --- 5. Візуалізація результатів ---
plt.figure(figsize=(8,5))
plt.plot(times[:100], marker='o', linestyle='-', label='Encryption time')
plt.xlabel('Номер запису')
plt.ylabel('Час (с)')
plt.title('Графік часу шифрування перших 100 записів')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("results/timing_plot.png")
plt.show()
print("📈 Графік збережено у папці results/timing_plot.png")

# --- 6. Перевірка блокчейну ---
print("\n=== ЕТАП 4: ПЕРЕВІРКА ЦІЛІСНОСТІ БЛОКЧЕЙНУ ===")
if blockchain.is_chain_valid():
    print("✅ Ланцюг блоків цілісний, аудит успішний.")
else:
    print("❌ Виявлено порушення цілісності ланцюга!")

# --- 7. Експорт журналу аудиту ---
blockchain.export_log()
print("📂 Журнал аудиту збережено у results/audit_log.json")

print("\nЕксперимент завершено успішно ✅")