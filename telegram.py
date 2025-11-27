import requests
from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_KEY = os.getenv("TELEGRAM_KEY")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_KEY}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'HTML'  # опционально, для форматирования
    }
    response = requests.post(url, json=payload)
    return response.status_code == 200  # True, если успешно