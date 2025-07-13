#!/usr/bin/env python3
"""
Скрипт для обновления URL во всех файлах проекта
"""

import os
import sys
import re

def update_file_content(file_path, old_url, new_url):
    """Обновляет URL в файле"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Заменяем URL
        updated_content = content.replace(old_url, new_url)
        
        if content != updated_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            return True
        return False
    except Exception as e:
        print(f"❌ Ошибка обновления {file_path}: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("❌ Использование: python update_urls.py <new-url>")
        print("Пример: python update_urls.py https://my-app.vercel.app")
        sys.exit(1)
    
    new_url = sys.argv[1]
    old_urls = [
        "https://your-vercel-url.vercel.app",
        "http://localhost:5000",
        "your-vercel-url.vercel.app"
    ]
    
    files_to_update = [
        "telegram_bot/config.py",
        "telegram_bot/bot.py", 
        "test_api.py",
        "test_full_system.py",
        "app.py",
        "main.py",
        "server.py"
    ]
    
    print(f"🔄 Обновление URL на: {new_url}")
    print("=" * 50)
    
    updated_count = 0
    
    for file_path in files_to_update:
        if os.path.exists(file_path):
            for old_url in old_urls:
                if update_file_content(file_path, old_url, new_url):
                    print(f"✅ Обновлен: {file_path}")
                    updated_count += 1
                    break
        else:
            print(f"⚠️  Файл не найден: {file_path}")
    
    print("=" * 50)
    print(f"📊 Обновлено файлов: {updated_count}")
    
    if updated_count > 0:
        print("\n🎉 URL успешно обновлен!")
        print("💡 Теперь можете протестировать систему:")
        print(f"   python test_full_system.py --url \"{new_url}\"")
    else:
        print("\n⚠️  URL не был обновлен. Проверьте правильность старого URL.")

if __name__ == "__main__":
    main() 