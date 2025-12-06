from blockchain_audit import Blockchain, Block
import time, os

# Ініціалізація блокчейну
bc = Blockchain()

# Додавання блоків (імітація дій користувача)
bc.add_block(Block(1, time.time(), "user_001", "LOGIN", "hash_abc"))
bc.add_block(Block(2, time.time(), "user_001", "VIEW_RECORD", "hash_def"))
bc.add_block(Block(3, time.time(), "user_002", "UPDATE_RECORD", "hash_xyz"))

# Експортуємо у JSON
os.makedirs("results", exist_ok=True)
bc.export_log("results/audit_log.json")

# Перевірка цілісності
if bc.is_chain_valid():
    print("✅ Ланцюг блоків цілісний, аудит успішний.")
else:
    print("❌ Помилка цілісності блокчейну!")

# Вивід на екран
for block in bc.chain:
    print(f"[{block.index}] {block.action} ({block.user_id}) | HASH: {block.hash[:15]}...")
