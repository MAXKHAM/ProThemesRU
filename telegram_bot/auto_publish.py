#!/usr/bin/env python3
"""
Автоматическая публикация ProThemesRU на GitHub
"""

import os
import subprocess
import sys
import time

def run_command(command, description):
    """Выполнить команду и показать результат"""
    print(f"\n🔄 {description}...")
    print(f"Команда: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.stdout:
            print("✅ Вывод:")
            print(result.stdout)
        
        if result.stderr:
            print("⚠️  Предупреждения:")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {description} выполнено успешно!")
            return True
        else:
            print(f"❌ {description} завершилось с ошибкой!")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при выполнении команды: {e}")
        return False

def check_git_status():
    """Проверить статус Git"""
    print("📋 Проверка статуса Git...")
    
    result = subprocess.run("git status", shell=True, capture_output=True, text=True)
    
    if "nothing to commit" in result.stdout:
        print("✅ Все изменения уже зафиксированы")
        return True
    else:
        print("📝 Есть незафиксированные изменения:")
        print(result.stdout)
        return False

def get_remote_url():
    """Получить URL удаленного репозитория"""
    result = subprocess.run("git remote get-url origin", shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return None

def main():
    """Основная функция"""
    print("🚀 ProThemesRU - Автоматическая публикация на GitHub")
    print("=" * 60)
    
    # Проверяем, что мы в Git репозитории
    if not os.path.exists(".git"):
        print("❌ Ошибка: Не найден Git репозиторий!")
        print("💡 Убедитесь, что вы находитесь в папке проекта")
        return False
    
    # Проверяем статус
    if not check_git_status():
        print("\n📦 Добавляем изменения...")
        if not run_command("git add .", "Добавление файлов"):
            return False
        
        print("\n💾 Создаем коммит...")
        commit_message = "Update: Final version with Render deployment fixes and enhanced templates"
        if not run_command(f'git commit -m "{commit_message}"', "Создание коммита"):
            return False
    
    # Проверяем remote
    remote_url = get_remote_url()
    if not remote_url:
        print("\n⚠️  Remote origin не настроен!")
        print("💡 Выполните следующие команды:")
        print("   git remote add origin https://github.com/YOUR_USERNAME/ProThemesRU.git")
        print("   git push -u origin master")
        return False
    
    print(f"\n🌐 Remote URL: {remote_url}")
    
    # Публикуем на GitHub
    print("\n🚀 Публикация на GitHub...")
    if not run_command("git push origin master", "Отправка на GitHub"):
        print("\n❌ Ошибка при публикации!")
        print("💡 Возможные причины:")
        print("   - Неправильный remote URL")
        print("   - Нет прав на запись в репозиторий")
        print("   - Проблемы с аутентификацией")
        return False
    
    print("\n🎉 Публикация завершена успешно!")
    print("\n📋 Что было исправлено:")
    print("✅ Обновлен requirements.txt для Python 3.13")
    print("✅ Добавлен runtime.txt (Python 3.11.7)")
    print("✅ Создан app.py для Render webhook")
    print("✅ Создан run_bot.py для фонового бота")
    print("✅ Обновлен Procfile для Render")
    print("✅ Обновлен render.yaml")
    print("✅ Добавлены все шаблоны и стили")
    
    print("\n🔧 Следующие шаги:")
    print("1. Перейдите на GitHub и проверьте репозиторий")
    print("2. Настройте переменные окружения на Render:")
    print("   - TELEGRAM_BOT_TOKEN")
    print("   - TELEGRAM_ADMIN_CHAT_ID")
    print("3. Деплой на Render должен пройти успешно")
    
    return True

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n✅ Все готово! Проект успешно опубликован!")
    else:
        print("\n❌ Произошла ошибка при публикации")
        sys.exit(1) 