#!/usr/bin/env python3
"""
Главный скрипт запуска ProThemes
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """Вывод баннера приложения"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║                    🚀 ProThemes                             ║
    ║              Современный конструктор сайтов                 ║
    ║                                                              ║
    ║  Создавайте профессиональные сайты без знания программирования  ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Проверка версии Python"""
    if sys.version_info < (3, 8):
        print("❌ Требуется Python 3.8 или выше")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]}")

def check_dependencies():
    """Проверка зависимостей"""
    print("🔍 Проверка зависимостей...")
    
    required_packages = [
        'flask', 'sqlalchemy', 'flask-login', 'flask-cors',
        'requests', 'beautifulsoup4', 'pillow', 'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Отсутствуют пакеты: {', '.join(missing_packages)}")
        print("Установите: pip install -r requirements.txt")
        return False
    
    print("✅ Все зависимости установлены")
    return True

def setup_environment():
    """Настройка окружения"""
    print("⚙️  Настройка окружения...")
    
    root_dir = Path(__file__).parent
    
    # Создаем необходимые директории
    directories = ['logs', 'uploads', 'static', 'media', 'temp']
    for dir_name in directories:
        dir_path = root_dir / dir_name
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
            print(f"📁 Создана директория: {dir_name}")
    
    # Проверяем .env файл
    env_file = root_dir / '.env'
    if not env_file.exists():
        env_example = root_dir / '.env.example'
        if env_example.exists():
            print("📝 Создайте файл .env на основе .env.example")
        else:
            print("📝 Создайте файл .env с настройками")
        return False
    
    print("✅ Окружение настроено")
    return True

def start_backend():
    """Запуск backend сервера"""
    print("🔧 Запуск backend сервера...")
    
    try:
        # Запускаем Flask приложение
        from app import create_app, db
        from app.models import User, Project, Template, Block, Order, MediaFile, ScrapingProfile
        
        app = create_app()
        
        with app.app_context():
            # Создаем таблицы
            db.create_all()
            
            # Создаем администратора
            admin = User.query.filter_by(email='admin@prothemes.ru').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@prothemes.ru',
                    role='admin'
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("✅ Администратор создан: admin@prothemes.ru / admin123")
        
        print("✅ Backend сервер запущен на http://localhost:5000")
        return app
        
    except Exception as e:
        print(f"❌ Ошибка запуска backend: {e}")
        return None

def start_frontend():
    """Запуск frontend сервера"""
    print("🎨 Запуск frontend сервера...")
    
    frontend_dir = Path(__file__).parent / 'frontend'
    if not frontend_dir.exists():
        print("❌ Директория frontend не найдена")
        return None
    
    try:
        # Проверяем node_modules
        node_modules = frontend_dir / 'node_modules'
        if not node_modules.exists():
            print("📦 Установка npm зависимостей...")
            subprocess.run(['npm', 'install'], cwd=frontend_dir, check=True)
        
        # Запускаем React приложение
        print("🚀 Запуск React приложения...")
        process = subprocess.Popen(
            ['npm', 'start'],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        print("✅ Frontend сервер запущен на http://localhost:3000")
        return process
        
    except Exception as e:
        print(f"❌ Ошибка запуска frontend: {e}")
        return None

def start_telegram_bot():
    """Запуск Telegram бота"""
    print("🤖 Запуск Telegram бота...")
    
    bot_dir = Path(__file__).parent / 'telegram_bot'
    if not bot_dir.exists():
        print("❌ Директория telegram_bot не найдена")
        return None
    
    try:
        bot_file = bot_dir / 'bot.py'
        if bot_file.exists():
            process = subprocess.Popen(
                [sys.executable, 'bot.py'],
                cwd=bot_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print("✅ Telegram бот запущен")
            return process
        else:
            print("❌ Файл bot.py не найден")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка запуска Telegram бота: {e}")
        return None

def show_status():
    """Показать статус сервисов"""
    print("\n" + "="*60)
    print("📊 СТАТУС СЕРВИСОВ")
    print("="*60)
    print("🌐 Backend API:    http://localhost:5000")
    print("🎨 Frontend:       http://localhost:3000")
    print("👤 Админ панель:   http://localhost:5000/admin")
    print("📊 API документация: http://localhost:5000/api/docs")
    print("🤖 Telegram бот:   @prothemes_bot")
    print("="*60)
    print("👤 Админ: admin@prothemes.ru / admin123")
    print("📧 Поддержка: support@prothemes.ru")
    print("🌍 Сайт: https://prothemes.ru")
    print("="*60)

def main():
    """Основная функция"""
    print_banner()
    
    # Проверки
    check_python_version()
    if not check_dependencies():
        sys.exit(1)
    if not setup_environment():
        sys.exit(1)
    
    print("\n🚀 Запуск ProThemes...")
    
    # Запускаем сервисы
    backend_app = start_backend()
    if not backend_app:
        sys.exit(1)
    
    frontend_process = start_frontend()
    telegram_process = start_telegram_bot()
    
    # Показываем статус
    show_status()
    
    print("\n🎉 ProThemes успешно запущен!")
    print("Нажмите Ctrl+C для остановки")
    
    try:
        # Запускаем Flask приложение
        backend_app.run(
            host='0.0.0.0',
            port=5000,
            debug=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Остановка сервисов...")
        
        # Останавливаем процессы
        if frontend_process:
            frontend_process.terminate()
            print("✅ Frontend остановлен")
        
        if telegram_process:
            telegram_process.terminate()
            print("✅ Telegram бот остановлен")
        
        print("👋 ProThemes остановлен")

if __name__ == '__main__':
    main() 