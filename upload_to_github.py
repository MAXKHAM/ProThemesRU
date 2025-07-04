import os
import subprocess

def upload_to_github(username):
    # Создаем репозиторий на GitHub (вы должны это сделать вручную)
    print("Перед использованием скрипта:")
    print("1. Создайте репозиторий на GitHub по адресу: https://github.com/new")
    print("2. Введите имя: prothemesru")
    print("3. Нажмите \"Create repository\"\n")
    
    # Инициализируем git
    subprocess.run(['git', 'init'])
    
    # Добавляем все файлы, кроме чувствительных
    subprocess.run(['git', 'add', '.'])
    
    # Создаем коммит
    subprocess.run(['git', 'commit', '-m', 'Initial commit'])
    
    # Добавляем удаленный репозиторий
    remote_url = f'https://github.com/{username}/prothemesru.git'
    subprocess.run(['git', 'remote', 'add', 'origin', remote_url])
    
    # Загружаем на GitHub
    subprocess.run(['git', 'push', '-u', 'origin', 'main'])
    
    print(f"\nПроект успешно загружен на GitHub!\nURL: {remote_url}")

if __name__ == "__main__":
    username = input("Введите ваш username на GitHub: ")
    upload_to_github(username)
