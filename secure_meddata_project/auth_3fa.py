# auth_3fa.py
# ----------------------------------------
# Модуль трифакторної аутентифікації (3FA)
# 1. Парольний рівень (bcrypt)
# 2. OTP-код (pyotp)
# 3. Біометричний рівень (імітаційний, стабільний у VS Code)

import pyotp
import bcrypt
import time

def authenticate_user():
    print("=== МОДУЛЬ ТРИФАКТОРНОЇ АВТЕНТИФІКАЦІЇ ===")

    # --- 1. Ініціалізація користувача ---
    username = "admin"
    password = "securepass"
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # --- 2. Перевірка пароля ---
    user_input = input("🔐 Введіть пароль: ").strip()

    # обмежуємо довжину до 72 байтів, щоб уникнути ValueError
    if len(user_input.encode()) > 72:
        user_input = user_input.encode()[:72].decode(errors="ignore")

    if not bcrypt.checkpw(user_input.encode(), hashed_pw):
        print("❌ Невірний пароль.")
        return False

    # --- 3. Генерація OTP-коду ---
    otp = pyotp.TOTP(pyotp.random_base32())
    code = otp.now()
    print(f"\n📲 Ваш одноразовий OTP-код: {code}")
    user_code = input("Введіть OTP-код: ").strip()
    if user_code != code:
        print("❌ Невірний OTP-код.")
        return False

    # --- 4. Біометричний рівень (імітаційний, з кількома спробами) ---
    print("\n🧠 Біометрична перевірка особи (імітаційний рівень)")
    print("Для проходження введіть 'ok' (імітація зчитування відбитка):")

    biometric_verified = False
    for attempt in range(3):
        biometric_input = input("➡️  Біометричне підтвердження: ").strip().lower()
        if biometric_input == "ok":
            biometric_verified = True
            break
        else:
            print(f"⚠️  Невірне підтвердження ({attempt+1}/3). Спробуйте ще раз.")

    if not biometric_verified:
        print("❌ Біометрична автентифікація не пройдена. Доступ заборонено.")
        return False

    # --- 5. Остаточне підтвердження ---
    print("\n✅ Успішна трифакторна автентифікація користувача!\n")
    time.sleep(0.5)
    return True
