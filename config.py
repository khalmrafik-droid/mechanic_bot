import os
from dotenv import load_dotenv

# Сначала пробуем взять токен из переменных окружения (как на Bothost)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Если токена нет (мы на локальном ПК), загружаем из .env
if not BOT_TOKEN:
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ Токен не найден! Добавь его в .env или в переменные хостинга.")