from pywebcopy import save_webpage, save_website
import validators
import os

def warning(text):
    print("\033[1m\033[31m{}\033[0m".format(text))

def webpage(url, folder, name):
    save_webpage(
        url=url,
        project_folder=folder,
        project_name=name,
        bypass_robots=True,
        debug=True,
        open_in_browser=True,
        delay=None,
        threaded=False,
    )

def website(url, folder, name):
    save_website(
        url=url,
        project_folder=folder,
        project_name=name,
        bypass_robots=True,
        debug=True,
        open_in_browser=True,
        delay=None,
        threaded=False,
    )

def batch_download(urls_file, folder, mode='page'):
    with open(urls_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]
    for idx, url in enumerate(urls, 1):
        if not validators.url(url):
            warning(f"Пропущена некорректная ссылка: {url}")
            continue
        name = f"template_{idx}"
        print(f"Скачиваю {url} как {name}...")
        try:
            if mode == 'site':
                website(url, folder, name)
            else:
                webpage(url, folder, name)
        except Exception as e:
            warning(f"Ошибка при скачивании {url}: {e}")

if __name__ == "__main__":
    # Автоматический режим для скачивания шаблонов в проект
    import sys
    import os
    
    # Получаем путь к корневой папке проекта
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    templates_folder = os.path.join(project_root, "templates", "blocks")
    
    # Создаем папку если её нет
    os.makedirs(templates_folder, exist_ok=True)
    
    print(f"Скачиваю шаблоны в папку: {templates_folder}")
    
    # Проверяем наличие файла urls.txt
    urls_file = os.path.join(project_root, "urls.txt")
    if not os.path.exists(urls_file):
        print("Файл urls.txt не найден. Создаю пример файла...")
        sample_urls = [
            "https://html5up.net/spectral",
            "https://html5up.net/phantom",
            "https://html5up.net/identity",
            "https://html5up.net/forty",
            "https://html5up.net/escape-velocity"
        ]
        with open(urls_file, 'w', encoding='utf-8') as f:
            for url in sample_urls:
                f.write(url + '\n')
        print(f"Создан файл {urls_file} с примерами ссылок")
    
    # Запускаем пакетное скачивание
    try:
        batch_download(urls_file, templates_folder, 'page')
        print(f"\n✅ Все шаблоны успешно скачаны в папку: {templates_folder}")
    except Exception as e:
        print(f"❌ Ошибка при скачивании: {e}") 