#!/usr/bin/env python3
"""
ProThemesRU - Автоматический деплой
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Выполняет команду и выводит результат"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - УСПЕШНО")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} - ОШИБКА")
            print(f"Ошибка: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - ИСКЛЮЧЕНИЕ: {e}")
        return False
    return True

def main():
    print("=" * 50)
    print("🚀 ProThemesRU - АВТОМАТИЧЕСКИЙ ДЕПЛОЙ")
    print("=" * 50)
    
    # Проверяем, что мы в правильной папке
    if not os.path.exists("app.py") and not os.path.exists("index.html"):
        print("❌ ОШИБКА: Не найдены файлы проекта!")
        print("Убедитесь, что вы находитесь в папке ProThemesRU1")
        return
    
    # Выполняем команды деплоя
    commands = [
        ("git add .", "Добавление файлов в git"),
        ("git commit -m \"ProThemesRU: Полный деплой - сайт + бот + все функции\"", "Создание коммита"),
        ("git push origin main", "Отправка на GitHub")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            print(f"\n❌ Деплой прерван на этапе: {description}")
            return
    
    print("\n" + "=" * 50)
    print("🎉 ДЕПЛОЙ УСПЕШНО ЗАВЕРШЕН!")
    print("=" * 50)
    print("\n📋 Что произошло:")
    print("✅ Все файлы добавлены в git")
    print("✅ Создан коммит со всеми изменениями")
    print("✅ Изменения отправлены на GitHub")
    print("✅ Vercel автоматически обновит сайт")
    print("\n🤖 Следующие шаги для бота:")
    print("1. Перейдите в папку telegram_bot")
    print("2. Выполните: railway login")
    print("3. Выполните: railway up")
    print("4. Настройте переменные окружения в Railway")
    print("5. Установите вебхук для бота")
    print("\n🌐 Ваш сайт будет доступен на Vercel через несколько минут")

if __name__ == "__main__":
    main() 