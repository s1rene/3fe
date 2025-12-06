import time
import random
from auth_3fa import authenticate_user
from cryptography.fernet import Fernet
from blockchain_audit import Blockchain, Block

# Ініціалізація блокчейну для аудиту
bc = Blockchain()

# Імітація п’яти користувачів з різними ролями
users = [
    {"id": "admin_001", "role": "Адміністратор"},
    {"id": "doctor_001", "role": "Лікар"},
    {"id": "doctor_002", "role": "Лікар"},
    {"id": "nurse_001", "role": "Медсестра"},
    {"id": "assistant_001", "role": "Медичний асистент"}
]

# Ініціалізація шифрування AES (Fernet)
key = Fernet.generate_key()
cipher = Fernet(key)

# Типи можливих дій користувачів
actions = ["LOGIN", "VIEW_RECORD", "UPDATE_RECORD", "ENCRYPT_DATA", "AUDIT_CHECK"]

# Імітація виконання дій усіма користувачами
print("=== ІМІТАЦІЯ ДІЙ КОРИСТУВАЧІВ ===\n")
for user in users:
    user_id = user["id"]
    role = user["role"]
    print(f"👤 {role} ({user_id}) починає роботу в системі...")

    for i in range(3):  # кожен користувач виконує 3 дії
        action = random.choice(actions)
        payload = f"record_{random.randint(1, 100)}_{action}".encode()

        # Імітація шифрування даних
        t_start = time.perf_counter()
        enc_data = cipher.encrypt(payload)
        t_end = time.perf_counter()
        delay = t_end - t_start

        # Додаємо дію у блокчейн-аудит
        bc.add_block(Block(len(bc.chain), time.time(), user_id, action, str(hash(enc_data))))

        print(f"   ➤ {action} виконано (затримка шифрування: {delay:.6f} с)")

    print(f"✅ Користувач {user_id} завершив роботу.\n")
    time.sleep(0.5)

# Експортуємо журнал аудиту
bc.export_log("results/audit_users.json")

# Перевірка цілісності ланцюга
print("\n=== РЕЗУЛЬТАТ ПЕРЕВІРКИ ===")
if bc.is_chain_valid():
    print("✅ Ланцюг блоків цілісний, аудит завершено успішно.")
else:
    print("❌ Виявлено порушення цілісності блокчейну!")

print(f"📄 Журнал дій збережено у results/audit_users.json")
