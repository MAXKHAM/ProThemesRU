import os
import zipfile
from io import BytesIO
from flask import send_file
from datetime import datetime

def export_site_as_zip(html_content: str, filename='site_export.zip'):
    """
    Экспортирует HTML-контент сайта в ZIP-архив.
    
    Args:
        html_content (str): HTML-код сайта
        filename (str): Имя файла для скачивания
    
    Returns:
        Flask response с ZIP-архивом
    """
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Добавляем основной HTML-файл
        zf.writestr('index.html', html_content)
        
        # Здесь можно добавить другие статические файлы (CSS, JS, изображения),
        # если они были собраны или если они нужны для автономной работы.
        # Например, если у вас есть папка 'assets' с общими файлами:
        # for root, dirs, files in os.walk('app/static/common_assets'):
        #     for file in files:
        #         file_path = os.path.join(root, file)
        #         arcname = os.path.relpath(file_path, 'app/static')
        #         zf.write(file_path, arcname)

    memory_file.seek(0)
    return send_file(memory_file, download_name=filename, as_attachment=True, mimetype='application/zip') 