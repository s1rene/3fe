import hashlib
import time
import json

class Block:
    def __init__(self, index, timestamp, user_id, action, data_hash, prev_hash=""):
        self.index = index
        self.timestamp = timestamp
        self.user_id = user_id
        self.action = action
        self.data_hash = data_hash
        self.prev_hash = prev_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Обчислення SHA-256 хешу для блоку"""
        record = (str(self.index) + str(self.timestamp) +
                  str(self.user_id) + str(self.action) +
                  str(self.data_hash) + str(self.prev_hash))
        return hashlib.sha256(record.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        """Створення початкового блоку"""
        return Block(0, time.time(), "system", "INIT", "0", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        """Додавання нового блоку у ланцюг"""
        new_block.prev_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_chain_valid(self):
        """Перевірка цілісності ланцюга блоків"""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                print("❌ Хеш поточного блоку змінено!")
                return False
            if current.prev_hash != prev.hash:
                print("❌ Порушено ланцюг хешів!")
                return False
        return True

    def export_log(self, filename="results/audit_log.json"):
        """Експортування журналу аудиту у JSON"""
        data = [vars(block) for block in self.chain]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
