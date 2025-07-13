#!/usr/bin/env python3
"""
Комплексное тестирование системы ProThemesRU
Проверяет API, базу данных и основные функции
"""

import requests
import json
import sys
import time
from datetime import datetime

class ProThemesRUTester:
    def __init__(self, base_url="https://your-real-url-here.com"):
        self.base_url = base_url
        self.test_results = []
        self.session = requests.Session()
        
    def log_test(self, test_name, success, message=""):
        """Логирует результат теста"""
        status = "✅ ПРОЙДЕН" if success else "❌ ПРОВАЛЕН"
        timestamp = datetime.now().strftime("%H:%M:%S")
        result = f"[{timestamp}] {status} {test_name}"
        if message:
            result += f" - {message}"
        print(result)
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': timestamp
        })
        return success
    
    def test_api_health(self):
        """Тест 1: Проверка здоровья API"""
        try:
            response = self.session.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                data = response.json()
                return self.log_test(
                    "API Health Check",
                    True,
                    f"Status: {data.get('status')}, Templates: {data.get('templates_count')}"
                )
            else:
                return self.log_test("API Health Check", False, f"Status code: {response.status_code}")
        except Exception as e:
            return self.log_test("API Health Check", False, str(e))
    
    def test_main_page(self):
        """Тест 2: Главная страница"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                return self.log_test(
                    "Main Page",
                    True,
                    f"Version: {data.get('version')}, Status: {data.get('status')}"
                )
            else:
                return self.log_test("Main Page", False, f"Status code: {response.status_code}")
        except Exception as e:
            return self.log_test("Main Page", False, str(e))
    
    def test_templates_api(self):
        """Тест 3: API шаблонов"""
        try:
            response = self.session.get(f"{self.base_url}/api/templates")
            if response.status_code == 200:
                data = response.json()
                templates_count = len(data.get('templates', []))
                return self.log_test(
                    "Templates API",
                    True,
                    f"Found {templates_count} templates"
                )
            else:
                return self.log_test("Templates API", False, f"Status code: {response.status_code}")
        except Exception as e:
            return self.log_test("Templates API", False, str(e))
    
    def test_user_registration(self):
        """Тест 4: Регистрация пользователя"""
        try:
            test_user = {
                "username": f"testuser_{int(time.time())}",
                "email": f"test_{int(time.time())}@example.com",
                "password": "testpassword123"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/auth/register",
                json=test_user
            )
            
            if response.status_code == 201:
                data = response.json()
                return self.log_test(
                    "User Registration",
                    True,
                    f"User created: {test_user['username']}"
                )
            else:
                return self.log_test("User Registration", False, f"Status code: {response.status_code}")
        except Exception as e:
            return self.log_test("User Registration", False, str(e))
    
    def test_user_login(self):
        """Тест 5: Вход пользователя"""
        try:
            login_data = {
                "username": "testuser",
                "password": "testpassword123"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/auth/login",
                json=login_data
            )
            
            if response.status_code == 200:
                data = response.json()
                token = data.get('access_token')
                if token:
                    self.session.headers.update({'Authorization': f'Bearer {token}'})
                    return self.log_test(
                        "User Login",
                        True,
                        "Token received successfully"
                    )
                else:
                    return self.log_test("User Login", False, "No token in response")
            else:
                return self.log_test("User Login", False, f"Status code: {response.status_code}")
        except Exception as e:
            return self.log_test("User Login", False, str(e))
    
    def test_sites_api(self):
        """Тест 6: API сайтов (требует аутентификации)"""
        try:
            response = self.session.get(f"{self.base_url}/api/sites")
            if response.status_code == 200:
                data = response.json()
                sites_count = len(data.get('sites', []))
                return self.log_test(
                    "Sites API",
                    True,
                    f"Found {sites_count} sites"
                )
            elif response.status_code == 401:
                return self.log_test("Sites API", False, "Authentication required")
            else:
                return self.log_test("Sites API", False, f"Status code: {response.status_code}")
        except Exception as e:
            return self.log_test("Sites API", False, str(e))
    
    def test_database_connection(self):
        """Тест 7: Подключение к базе данных"""
        try:
            response = self.session.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                data = response.json()
                if data.get('database') == 'connected':
                    return self.log_test(
                        "Database Connection",
                        True,
                        "Database is connected"
                    )
                else:
                    return self.log_test("Database Connection", False, "Database not connected")
            else:
                return self.log_test("Database Connection", False, f"Status code: {response.status_code}")
        except Exception as e:
            return self.log_test("Database Connection", False, str(e))
    
    def run_all_tests(self):
        """Запускает все тесты"""
        print("🚀 Запуск комплексного тестирования ProThemesRU")
        print("=" * 60)
        
        tests = [
            self.test_api_health,
            self.test_main_page,
            self.test_templates_api,
            self.test_database_connection,
            self.test_user_registration,
            self.test_user_login,
            self.test_sites_api
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
            time.sleep(0.5)  # Небольшая пауза между тестами
        
        print("=" * 60)
        print(f"📊 Результаты тестирования:")
        print(f"✅ Пройдено: {passed}/{total}")
        print(f"❌ Провалено: {total - passed}/{total}")
        print(f"📈 Успешность: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 Все тесты пройдены! Система работает корректно.")
        else:
            print(f"\n⚠️  {total - passed} тестов провалено. Проверьте настройки.")
        
        return passed == total

def main():
    """Главная функция"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Тестирование ProThemesRU')
    parser.add_argument('--url', default='https://your-real-url-here.com', 
                       help='URL API (по умолчанию: https://your-real-url-here.com)')
    
    args = parser.parse_args()
    
    print(f"🔗 Тестируем API по адресу: {args.url}")
    print("💡 Для тестирования продакшена используйте: --url https://your-domain.com")
    
    tester = ProThemesRUTester(args.url)
    success = tester.run_all_tests()
    
    if success:
        print("\n🚀 Система готова к использованию!")
        print("📋 Следующие шаги:")
        print("1. Разверните Telegram бота")
        print("2. Подключите фронтенд")
        print("3. Настройте платежную систему")
        print("4. Привлекайте пользователей!")
    else:
        print("\n🔧 Требуется исправление ошибок перед использованием.")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 