import os
import shutil
import subprocess

def prepare_gh_pages():
    # Создаем директорию для GitHub Pages
    if os.path.exists('public'):
        shutil.rmtree('public')
    os.makedirs('public')
    
    # Копируем необходимые файлы
    files_to_copy = [
        'index.html',
        'CNAME',
        '.nojekyll'
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, 'public/')
    
    # Копируем статические файлы
    if os.path.exists('static'):
        shutil.copytree('static', 'public/static')
    
    # Копируем шаблоны
    if os.path.exists('templates'):
        shutil.copytree('templates', 'public/templates')
    
    # Инициализируем git
    subprocess.run(['git', 'init'])
    
    # Добавляем все файлы
    subprocess.run(['git', 'add', '.'])
    
    # Создаем коммит
    subprocess.run(['git', 'commit', '-m', 'Prepare for GitHub Pages'])
    
    # Добавляем удаленный репозиторий
    subprocess.run(['git', 'remote', 'add', 'origin', 'https://github.com/maxkham/ProThemesRU.git'])
    
    # Загружаем на GitHub
    subprocess.run(['git', 'push', '-u', 'origin', 'main'])
    
    print("Проект успешно подготовлен для GitHub Pages!")

if __name__ == "__main__":
    prepare_gh_pages()
