#!/usr/bin/env python3
"""
Быстрая публикация ProThemesRU на GitHub
"""

import subprocess
import sys

def run_cmd(cmd):
    """Выполнить команду"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {cmd}")
            return True
        else:
            print(f"❌ {cmd}")
            print(f"Ошибка: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    print("🚀 Быстрая публикация ProThemesRU на GitHub...")
    
    # Проверяем remote
    if not run_cmd("git remote -v"):
        print("❌ Remote не настроен!")
        print("📋 Создайте репозиторий на GitHub и добавьте remote:")
        print("git remote add origin https://github.com/YOUR_USERNAME/ProThemesRU.git")
        return
    
    # Пушим
    if run_cmd("git push -u origin master"):
        print("🎉 Успешно опубликовано на GitHub!")
        print("📋 Следующие шаги:")
        print("1. Настройте GitHub Secrets")
        print("2. Включите GitHub Actions")
        print("3. Проверьте PUBLISH_INSTRUCTIONS.md")
    else:
        print("❌ Ошибка публикации!")
        print("📋 Проверьте:")
        print("- Создан ли репозиторий на GitHub")
        print("- Правильный ли URL в remote")
        print("- Есть ли права на запись")

if __name__ == "__main__":
    main() 