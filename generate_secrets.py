import secrets
import string
import hashlib
import os

def generate_secure_key(length=32):
    """Генерация надежного секретного ключа"""
    # Символы для генерации
    chars = string.ascii_letters + string.digits + string.punctuation
    
    # Генерация случайной строки
    random_string = ''.join(secrets.choice(chars) for _ in range(length))
    
    # Хеширование для дополнительной безопасности
    hashed_key = hashlib.sha256(random_string.encode()).hexdigest()
    
    return hashed_key

def generate_jwt_secret():
    """Генерация секретного ключа для JWT"""
    return secrets.token_urlsafe(32)

def main():
    # Генерация ключей
    secret_key = generate_secure_key()
    jwt_secret = generate_jwt_secret()
    
    print("\nСгенерированные секретные ключи:")
    print("SECRET_KEY:", secret_key)
    print("JWT_SECRET_KEY:", jwt_secret)
    
    # Сохранение в файл
    with open('.env', 'w') as f:
        f.write(f"SECRET_KEY={secret_key}\n")
        f.write(f"JWT_SECRET_KEY={jwt_secret}\n")
        f.write("\n# Остальные настройки будут добавлены позже\n")

    print("\nКлючи сохранены в файл .env")
    print("Пожалуйста, сохраните эти ключи в надежном месте")

if __name__ == "__main__":
    main()
