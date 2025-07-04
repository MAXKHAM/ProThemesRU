
# 🚀 ProThemesRU — Готовый визуальный сайт-конструктор

## 🧩 Возможности
- Визуальный редактор сайтов (drag'n'drop)
- Редактирование текста прямо в блоках
- Live preview результата
- Экспорт HTML в ZIP (одним нажатием)
- Tailwind CSS встроен
- Готов к деплою

## ⚙️ Быстрый старт
```bash
pip install -r requirements.txt
cp .env.example .env
python run.py
```
Или через Docker:
```bash
docker build -t prothemes .
docker run -p 5000:5000 prothemes
```

Зайди в браузере: http://localhost:5000/constructor

## 🛠 Переменные .env
- `SECRET_KEY` — секретный ключ Flask
- `FLASK_ENV` — production или development

## 📦 Состав
- `/constructor` — редактор в стиле Figma
- `/app/` — backend Flask
- `index.html` → экспортируется в ZIP

## 📬 Контакты
Проект создан для демонстрации и старта продаж.
