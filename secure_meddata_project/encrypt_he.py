# encrypt_he.py
from cryptography.fernet import Fernet

def aes_encrypt_decrypt(data: str):
    key = Fernet.generate_key()
    cipher = Fernet(key)
    encrypted = cipher.encrypt(data.encode())
    decrypted = cipher.decrypt(encrypted).decode()
    return encrypted, decrypted
