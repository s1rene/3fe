# plot_crypto_comparison.py
import matplotlib.pyplot as plt

# Дані з експериментів (середній час у секундах)
methods = ['AES (Fernet)', 'RSA', 'Paillier']
encryption_time = [0.00004, 0.00037, 0.0164]
decryption_time = [0.000025, 0.00037, 0.0051]

# Побудова графіка
plt.figure(figsize=(8, 5))
bar_width = 0.35
x = range(len(methods))

# Стовпчики для шифрування та розшифрування
plt.bar(x, encryption_time, width=bar_width, label='Шифрування', alpha=0.8)
plt.bar([i + bar_width for i in x], decryption_time, width=bar_width, label='Розшифрування', alpha=0.8)

# Підписи та оформлення
plt.xlabel('Метод шифрування', fontsize=11)
plt.ylabel('Час виконання, с', fontsize=11)
plt.title('Порівняння швидкодії криптографічних методів (AES, RSA, Paillier)', fontsize=13)
plt.xticks([i + bar_width/2 for i in x], methods)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Збереження графіка
plt.tight_layout()
plt.savefig('results/crypto_comparison.png', dpi=300)
plt.show()
