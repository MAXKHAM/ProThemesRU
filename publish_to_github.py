#!/usr/bin/env python3
"""
Скрипт для публикации ProThemesRU на GitHub
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None):
    """Выполнить команду и вернуть результат"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Ошибка выполнения команды: {command}")
            print(f"Ошибка: {result.stderr}")
            return False
        print(f"✅ {command}")
        if result.stdout.strip():
            print(result.stdout)
        return True
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    print("🚀 Публикация ProThemesRU на GitHub...")
    
    # Проверяем, что мы в корневой папке проекта
    if not Path("telegram_bot").exists():
        print("❌ Ошибка: Запустите скрипт из корневой папки проекта")
        sys.exit(1)
    
    # Проверяем статус git
    print("📊 Проверка статуса Git...")
    if not run_command("git status"):
        print("❌ Ошибка: Git не инициализирован")
        sys.exit(1)
    
    # Проверяем, есть ли remote
    print("🔍 Проверка remote origin...")
    result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
    
    if "origin" not in result.stdout:
        print("🔗 Добавление remote origin...")
        repo_url = input("Введите URL вашего GitHub репозитория (например, https://github.com/username/ProThemesRU.git): ")
        if not run_command(f'git remote add origin {repo_url}'):
            sys.exit(1)
    else:
        print("✅ Remote origin уже настроен")
    
    # Проверяем, есть ли изменения для коммита
    status_result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if status_result.stdout.strip():
        print("📁 Обнаружены несохраненные изменения...")
        print("💾 Добавление файлов в git...")
        if not run_command("git add ."):
            sys.exit(1)
        
        print("💾 Создание коммита...")
        if not run_command('git commit -m "Update: ProThemesRU with latest changes"'):
            sys.exit(1)
    else:
        print("✅ Все изменения уже закоммичены")
    
    # Пушим в GitHub
    print("📤 Отправка в GitHub...")
    if not run_command("git push -u origin master"):
        print("⚠️ Ошибка при отправке в GitHub!")
        print("📋 Возможные решения:")
        print("1. Убедитесь, что репозиторий создан на GitHub")
        print("2. Проверьте правильность URL в remote origin")
        print("3. Убедитесь, что у вас есть права на запись")
        print("4. Попробуйте создать репозиторий вручную:")
        print("   - Перейдите на https://github.com/new")
        print("   - Создайте репозиторий 'ProThemesRU'")
        print("   - Скопируйте URL репозитория")
        print("   - Запустите: git remote set-url origin <URL>")
        print("   - Запустите: git push -u origin master")
        sys.exit(1)
    
    print("🎉 Проект успешно опубликован на GitHub!")
    print("📋 Следующие шаги:")
    print("1. Настройте GitHub Secrets для телеграм бота")
    print("2. Включите GitHub Actions")
    print("3. Настройте деплой на выбранную платформу")
    print("4. Проверьте файл PUBLISH_INSTRUCTIONS.md для подробных инструкций")

if __name__ == "__main__":
    main() 