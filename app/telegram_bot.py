import logging
import requests
import zipfile
import io
import os
import re
from datetime import datetime

from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from flask import Blueprint, request, current_app, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User

# Включите логирование для отладки
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# Установите более низкий уровень для httpx, чтобы не спамить консоль
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Создаем Blueprint для Telegram бота
telegram_bp = Blueprint('telegram', __name__, url_prefix='/telegram')

# --- КОНФИГУРАЦИЯ БОТА ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
FLASK_API_BASE_URL = os.getenv("FLASK_API_BASE_URL", "http://127.0.0.1:5000/api")
FLASK_PUBLIC_SITE_URL = os.getenv("FLASK_PUBLIC_SITE_URL", "http://127.0.0.1:5000/public")
FLASK_EDITOR_URL = os.getenv("FLASK_EDITOR_URL", "http://localhost:3000")

# Админские учетные данные (в реальном проекте используйте переменные окружения)
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "adminpassword")
ADMIN_ACCESS_TOKEN = None

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ДЛЯ CSS ---
def css_string_to_object(css_string):
    styles = {}
    if not css_string:
        return styles
    
    css_string = re.sub(r'\/\*[\s\S]*?\*\/|([^:]|^)\/\/.*$', r'\1', css_string)

    parts = css_string.split(';')
    for part in parts:
        trimmed_part = part.strip()
        if trimmed_part:
            if ':' in trimmed_part:
                key, value = trimmed_part.split(':', 1)
                styles[key.strip()] = value.strip()
    return styles

def object_to_css_string(css_object):
    if not css_object:
        return ""
    return "; ".join([f"{key}: {value}" for key, value in css_object.items()]) + (";" if css_object else "")

# --- ФУНКЦИЯ ГЕНЕРАЦИИ HTML/CSS ---
def _generate_html_css_from_elements(elements):
    """
    Генерирует HTML и CSS из массива элементов конструктора,
    используя адаптивный контейнер и вложенность для групп.
    """
    MAX_CONTAINER_WIDTH = 960

    element_map = {el['id']: el for el in elements}
    root_elements = [el for el in elements if not el.get('parentId')]

    minX = float('inf')
    minY = float('inf')
    maxX = float('-inf')
    maxY = float('-inf')

    if root_elements:
        for el in root_elements:
            minX = min(minX, el['x'])
            minY = min(minY, el['y'])
            maxX = max(maxX, el['x'] + el['width'])
            maxY = max(maxY, el['y'] + el['height'])
    else:
        minX = 0; minY = 0; maxX = MAX_CONTAINER_WIDTH; maxY = 300

    original_design_width = maxX - minX
    original_design_height = maxY - minY

    scale_factor = 1
    if original_design_width > MAX_CONTAINER_WIDTH and original_design_width > 0:
        scale_factor = MAX_CONTAINER_WIDTH / original_design_width

    scaled_container_height = original_design_height * scale_factor

    html_content_parts = []
    css_content_parts = []

    html_content_parts.append(f"""<!DOCTYPE html><html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Мой Сайт (ProThemesRU)</title>
    <link rel="stylesheet" href="style.css">
    <style>
        .canvas-element {{
            box-sizing: border-box;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .canvas-element[style*="position: absolute;"] {{
             position: absolute;
        }}

        .canvas-element > * {{
            width: 100%;
            height: 100%;
            box-sizing: border-box;
        }}

        .text-element {{
            text-align: center;
            word-break: break-word;
            padding: 5px;
        }}
        .image-element {{
            display: block;
            object-fit: contain;
            max-width: 100%;
            height: auto;
        }}
        .button-element {{
            padding: 8px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            white-space: nowrap;
        }}
        .shape-element {{
        }}
    </style>
</head>
<body>
    <div id="main-content-area">""")

    css_content_parts.append(f"""
body {{
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
    background-color: #f0f0f0;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 20px 0;
    box-sizing: border-box;
}}

#main-content-area {{
    position: relative;
    max-width: {MAX_CONTAINER_WIDTH}px;
    width: 100%;
    margin: 0 auto;
    min-height: {max(scaled_container_height, 200)}px;
    background-color: #ffffff;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    overflow: hidden;
}}
""")

    def render_element_html_and_css(element):
        children = [el for el in elements if el.get('parentId') == element['id']]

        inline_styles = ""
        element_classes = 'canvas-element'

        parent = element.get('parentId')
        is_child_of_flex_container = False
        if parent:
            parent_el = element_map.get(parent)
            if parent_el and parent_el.get('type') == 'group' and parent_el['props'].get('displayMode') == 'flex':
                is_child_of_flex_container = True

        if is_child_of_flex_container:
            inline_styles += f"width: {element['width']}px; height: {element['height']}px;"
        else:
            elX = element['x']
            elY = element['y']
            newX = (elX - minX) * scale_factor if element.get('parentId') is None else elX
            newY = (elY - minY) * scale_factor if element.get('parentId') is None else elY
            newWidth = element['width'] * scale_factor if element.get('parentId') is None else element['width']
            newHeight = element['height'] * scale_factor if element.get('parentId') is None else element['height']

            inline_styles += f"position: absolute; left: {newX}px; top: {newY}px; width: {newWidth}px; height: {newHeight}px;"

        if element['props'].get('customClasses') and len(element['props']['customClasses']) > 0:
            element_classes += f" {' '.join(element['props']['customClasses'])}"
        
        inner_html = ""
        if element['type'] == 'text':
            inner_html = f'<div class="text-element">{element["props"].get("content", "")}</div>'
            inline_styles += f" font-size: {element['props'].get('fontSize', '16px')}; color: {element['props'].get('color', '#000000')};"
        elif element['type'] == 'image':
            inner_html = f'<img src="{element["props"].get("src", "")}" alt="{element["props"].get("alt", "")}" class="image-element">'
        elif element['type'] == 'button':
            inner_html = f'<button class="button-element">{element["props"].get("label", "")}</button>'
            inline_styles += f" background-color: {element['props'].get('bgColor', '#007bff')}; color: {element['props'].get('textColor', '#ffffff')};"
        elif element['type'] == 'shape':
            inner_html = f'<div class="shape-element"></div>'
            inline_styles += f" background-color: {element['props'].get('bgColor', '#ffc107')}; border-radius: {element['props'].get('borderRadius', '0')};"
        elif element['type'] == 'group':
            element_classes += ' group-element'
            if element['props'].get('displayMode') == 'flex':
                inline_styles += f" display: flex;"
                if element['props'].get('flexDirection'): inline_styles += f" flex-direction: {element['props']['flexDirection']};"
                if element['props'].get('justifyContent'): inline_styles += f" justify-content: {element['props']['justifyContent']};"
                if element['props'].get('alignItems'): inline_styles += f" align-items: {element['props']['alignItems']};"
                if element['props'].get('gap'): inline_styles += f" gap: {element['props']['gap']};"
            else:
                inline_styles += f" position: absolute;"
                inline_styles += f" background-color: rgba(255, 255, 255, 0.05); border: 1px dashed rgba(0, 0, 0, 0.1);"

            for child in children:
                inner_html += render_element_html_and_css(child)
        else:
            inner_html = f'<div>Неизвестный элемент</div>'
        
        if element['props'].get('customStyles'):
            inline_styles += f" {object_to_css_string(element['props']['customStyles'])}"

        return f'        <div id="{element["id"]}" class="{element_classes}" style="{inline_styles}">{inner_html}</div>'

    for el in root_elements:
        html_content_parts.append(render_element_html_and_css(el))

    html_content_parts.append(f"""    </div>
</body>
</html>""")

    return "".join(html_content_parts), "".join(css_content_parts)

# --- ФУНКЦИИ БОТА ---
async def get_admin_token():
    """Получает и сохраняет токен доступа администратора."""
    global ADMIN_ACCESS_TOKEN
    if ADMIN_ACCESS_TOKEN:
        return ADMIN_ACCESS_TOKEN

    try:
        response = requests.post(
            f"{FLASK_API_BASE_URL}/login",
            json={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD}
        )
        response.raise_for_status()
        data = response.json()
        ADMIN_ACCESS_TOKEN = data.get("access_token")
        logger.info("Admin token obtained successfully.")
        return ADMIN_ACCESS_TOKEN
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get admin token: {e}")
        return None

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение при команде /start."""
    user = update.effective_user
    await update.message.reply_html(
        f"Привет, {user.mention_html()}! 👋\n"
        "Я ваш помощник для конструктора сайтов ProThemesRU.\n"
        "Чем могу быть полезен?\n\n"
        "Используйте /help для просмотра всех команд."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение со списком доступных команд."""
    help_text = (
        "Вот список команд, которые я понимаю:\n\n"
        "/start - Приветствие\n"
        "/help - Показать это сообщение\n"
        "/editor - Открыть онлайн-редактор сайтов\n"
        "/my_site - Посмотреть опубликованный сайт\n"
        "/export_zip - Получить ZIP-архив с HTML/CSS текущего сайта (только для админа)\n"
        "/faq - Часто задаваемые вопросы\n"
        "/support - Связаться со службой поддержки"
    )
    await update.message.reply_text(help_text)

async def editor_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет ссылку на онлайн-редактор."""
    await update.message.reply_text(
        f"Откройте ваш онлайн-редактор здесь: {FLASK_EDITOR_URL}"
    )

async def my_site_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет ссылку на опубликованный сайт."""
    await update.message.reply_text(
        f"Ваш опубликованный сайт доступен по адресу: {FLASK_PUBLIC_SITE_URL}/index.html"
    )

async def export_zip_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Получает HTML/CSS опубликованного сайта и отправляет его в виде ZIP-архива.
    Требует админских прав (через токен).
    """
    await update.message.reply_text("Запрашиваю данные сайта для экспорта, это может занять несколько секунд...")

    token = await get_admin_token()
    if not token:
        await update.message.reply_text("Не удалось авторизоваться как администратор. Пожалуйста, проверьте учетные данные бота.")
        return

    headers = {"Authorization": f"Bearer {token}"}

    try:
        # Загружаем текущие элементы из базы данных Flask-приложения
        load_response = requests.get(f"{FLASK_API_BASE_URL}/admin/load_my_site_data", headers=headers)
        load_response.raise_for_status()
        elements = load_response.json()

        if not elements:
            await update.message.reply_text("На канвасе нет элементов для экспорта.")
            return

        # Генерируем HTML и CSS из полученных элементов
        html_content, css_content = _generate_html_css_from_elements(elements)

        # Создаем ZIP-архив в памяти
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("index.html", html_content.encode('utf-8'))
            zf.writestr("style.css", css_content.encode('utf-8'))
        zip_buffer.seek(0)

        # Отправляем ZIP-архив
        await update.message.reply_document(
            document=zip_buffer,
            filename="my_website_export.zip",
            caption="Ваш сайт экспортирован в ZIP-архив!"
        )
        logger.info(f"ZIP export sent to user {update.effective_user.id}")
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed during export: {e}")
        await update.message.reply_text(f"Ошибка при получении данных сайта с сервера: {e}")
    except Exception as e:
        logger.error(f"Error during ZIP generation/sending: {e}")
        await update.message.reply_text(f"Произошла непредвиденная ошибка при экспорте: {e}")

async def faq_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет ответы на часто задаваемые вопросы."""
    faq_text = (
        "❓ *Часто задаваемые вопросы:*\n\n"
        "*В: Нужны ли навыки программирования для использования конструктора?*\n"
        "О: Нет! Наш конструктор создан для того, чтобы вы могли создавать сайты полностью без кода, используя интуитивный Drag-and-Drop интерфейс.\n\n"
        "*В: Мой сайт будет адаптивным?*\n"
        "О: Да, все созданные с помощью ProThemesRU сайты автоматически адаптируются под разные устройства (компьютеры, планшеты, смартфоны).\n\n"
        "*В: Могу ли я подключить свой домен?*\n"
        "О: Да, вы можете легко подключить свой собственный домен к сайту, созданному у нас.\n\n"
        "*В: Предоставляете ли вы хостинг?*\n"
        "О: Да, хостинг входит в стоимость тарифа. Вам не нужно беспокоиться о технических деталях."
    )
    await update.message.reply_markdown(faq_text)

async def support_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Предоставляет контактные данные для поддержки."""
    support_text = (
        "📞 *Служба поддержки:*\n\n"
        "Если у вас возникли вопросы или проблемы, свяжитесь с нами:\n"
        "📧 Email: [support@prothemes.ru](mailto:support@prothemes.ru)\n"
        "🌐 Наш сайт: [prothemes.ru](http://prothemes.ru)\n\n"
        "Мы работаем 24/7 и готовы помочь!"
    )
    await update.message.reply_markdown(support_text)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает текстовые сообщения, если нет других команд."""
    await update.message.reply_text(
        "Извините, я не понял вашу команду. Пожалуйста, используйте /help для просмотра доступных команд."
    )

# --- FLASK INTEGRATION ---
@telegram_bp.route('/webhook', methods=['POST'])
def telegram_webhook():
    """Webhook endpoint для Telegram бота."""
    try:
        # Здесь будет обработка webhook от Telegram
        # Пока что это заглушка
        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({'error': str(e)}), 500

def init_telegram_bot():
    """Инициализация Telegram бота."""
    if TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        logger.warning("Telegram bot token not configured!")
        return None
    
    try:
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

        # Обработчики команд
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("editor", editor_command))
        application.add_handler(CommandHandler("my_site", my_site_command))
        application.add_handler(CommandHandler("export_zip", export_zip_command))
        application.add_handler(CommandHandler("faq", faq_command))
        application.add_handler(CommandHandler("support", support_command))

        # Обработчик для любых текстовых сообщений
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

        logger.info("Telegram bot initialized successfully.")
        return application
    except Exception as e:
        logger.error(f"Failed to initialize Telegram bot: {e}")
        return None

# Глобальная переменная для хранения экземпляра бота
telegram_app = None

def start_telegram_bot():
    """Запускает Telegram бота в отдельном потоке."""
    global telegram_app
    telegram_app = init_telegram_bot()
    if telegram_app:
        logger.info("Starting Telegram bot polling...")
        telegram_app.run_polling(allowed_updates=Update.ALL_TYPES)
