#!/usr/bin/env python3
"""
Тестовый скрипт для проверки API ProThemesRU
"""

import requests
import json
import sys

# Базовый URL API (замените на ваш реальный URL)
BASE_URL = "https://pro-themes-ru-maxkhams-projects.vercel.app"  # Для локального тестирования
# BASE_URL = "https://your-real-url-here.com"  # Для продакшена

def test_endpoint(endpoint, method="GET", data=None, headers=None):
    """Тестирует API эндпоинт"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        
        print(f"\n🔍 Тестируем: {method} {endpoint}")
        print(f"📡 Статус: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Успешно!")
            try:
                result = response.json()
                print(f"📄 Ответ: {json.dumps(result, indent=2, ensure_ascii=False)}")
            except:
                print(f"📄 Ответ: {response.text}")
        else:
            print("❌ Ошибка!")
            print(f"📄 Ответ: {response.text}")
            
        return response.status_code == 200
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

def main():
    print("🚀 Тестирование API ProThemesRU")
    print("=" * 50)
    
    # Тест 1: Главная страница
    test_endpoint("/")
    
    # Тест 2: Проверка здоровья API
    test_endpoint("/api/health")
    
    # Тест 3: Получение шаблонов
    test_endpoint("/api/templates")
    
    # Тест 4: Регистрация пользователя
    test_user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    test_endpoint("/api/auth/register", method="POST", data=test_user_data)
    
    # Тест 5: Вход пользователя
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    response = test_endpoint("/api/auth/login", method="POST", data=login_data)
    
    print("\n" + "=" * 50)
    print("🎉 Тестирование завершено!")
    print("\n💡 Для полного тестирования:")
    print("1. Запустите сервер: python app.py")
    print("2. Замените BASE_URL на ваш реальный URL")
    print("3. Запустите тест: python test_api.py")

if __name__ == "__main__":
    main() 