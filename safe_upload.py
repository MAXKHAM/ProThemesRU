import os
import shutil
import subprocess

def safe_upload_to_github():
    # Создаем временную директорию для безопасной версии проекта
    temp_dir = 'prothemesru_safe'
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    # Копируем только безопасные файлы
    safe_files = [
        'README.md',
        'requirements.txt',
        'app.py',
        'models.py',
        'templates',
        'static',
        'api',
        'frontend',
        'config/config_template.py',
        'safe_gitignore'
    ]
    
    for file in safe_files:
        src = os.path.join('..', file)
        dst = os.path.join(temp_dir, file)
        if os.path.exists(src):
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
    
    # Переходим в временную директорию
    os.chdir(temp_dir)
    
    # Инициализируем git
    subprocess.run(['git', 'init'])
    
    # Добавляем .gitignore
    shutil.copy2('../safe_gitignore', '.gitignore')
    
    # Добавляем все файлы
    subprocess.run(['git', 'add', '.'])
    
    # Создаем коммит
    subprocess.run(['git', 'commit', '-m', 'Initial safe commit'])
    
    # Добавляем удаленный репозиторий
    subprocess.run(['git', 'remote', 'add', 'origin', 'https://github.com/ВАШ_ЮЗЕРНЕЙМ/prothemesru.git'])
    
    # Загружаем на GitHub
    subprocess.run(['git', 'push', '-u', 'origin', 'main'])
    
    print("Проект успешно загружен на GitHub!")

if __name__ == "__main__":
    safe_upload_to_github()
