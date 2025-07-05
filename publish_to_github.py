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
    if not run_command("git status"):
        print("❌ Ошибка: Git не инициализирован")
        sys.exit(1)
    
    # Добавляем все файлы
    print("📁 Добавление файлов в git...")
    if not run_command("git add ."):
        sys.exit(1)
    
    # Коммитим изменения
    print("💾 Создание коммита...")
    if not run_command('git commit -m "Update: ProThemesRU with enhanced templates and blocks"'):
        sys.exit(1)
    
    # Проверяем, есть ли remote
    result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
    if "origin" not in result.stdout:
        print("🔗 Добавление remote origin...")
        repo_url = input("Введите URL вашего GitHub репозитория (например, https://github.com/username/ProThemesRU.git): ")
        if not run_command(f'git remote add origin {repo_url}'):
            sys.exit(1)
    
    # Пушим в GitHub
    print("📤 Отправка в GitHub...")
    if not run_command("git push -u origin master"):
        print("⚠️ Попробуйте создать репозиторий на GitHub вручную:")
        print("1. Перейдите на https://github.com/new")
        print("2. Создайте репозиторий 'ProThemesRU'")
        print("3. Скопируйте URL репозитория")
        print("4. Запустите: git remote set-url origin <URL>")
        print("5. Запустите: git push -u origin master")
        sys.exit(1)
    
    print("🎉 Проект успешно опубликован на GitHub!")
    print("📋 Следующие шаги:")
    print("1. Настройте GitHub Secrets для телеграм бота")
    print("2. Включите GitHub Actions")
    print("3. Настройте деплой на выбранную платформу")

if __name__ == "__main__":
    main() 