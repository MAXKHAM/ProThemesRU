from typing import List, Dict, Optional
from flask import current_app
from app.models import SiteBlock, db
import zipfile
from io import BytesIO

class BlockService:
    @staticmethod
    def get_all_blocks() -> List[SiteBlock]:
        """Получает все доступные блоки"""
        return SiteBlock.query.all()

    @staticmethod
    def get_block_by_id(block_id: int) -> Optional[SiteBlock]:
        """Получает блок по ID"""
        return SiteBlock.query.get(block_id)

    @staticmethod
    def generate_site(blocks: List[SiteBlock]) -> BytesIO:
        """Генерирует сайт из выбранных блоков"""
        html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Сайт</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <nav class="navbar navbar-expand-lg navbar-light bg-light">
                    <a class="navbar-brand" href="#">Мой Сайт</a>
                </nav>
            </div>
        </div>
        <div class="row">
            <div class="col-12">
                <main class="py-4">
                    <div class="container">
                        <div class="row">
                            <div class="col-12">
                                <h1 class="text-center mb-4">Содержимое сайта</h1>
                                <div class="blocks-container">
                                    {blocks_content}
                                </div>
                            </div>
                        </div>
                    </div>
                </main>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

        blocks_content = ""
        for block in blocks:
            blocks_content += block.html_content

        html_content = html_content.replace("{blocks_content}", blocks_content)

        # Создаем ZIP архив
        zip_stream = BytesIO()
        with zipfile.ZipFile(zip_stream, 'w') as zipf:
            zipf.writestr("index.html", html_content)
            # Добавляем CSS файл
            css_content = """body {
                font-family: 'Arial', sans-serif;
                line-height: 1.6;
                color: #333;
            }
            .blocks-container {
                margin-top: 2rem;
            }
            .block {
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }"""
            zipf.writestr("style.css", css_content)

        zip_stream.seek(0)
        return zip_stream
