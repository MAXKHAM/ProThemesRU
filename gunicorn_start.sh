#!/bin/bash
# Запуск Gunicorn вручную
exec gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
