from datetime import datetime, time
import requests
from dotenv import load_dotenv
import os
import json
from telegram import send_telegram_message

load_dotenv()

SESSION_ID = os.getenv("SESSION_ID")
SK_TOKEN = os.getenv("SK_TOKEN")
BUSINESS_ID = os.getenv("BUSINESS_ID")
CAMPAIGN_ID = os.getenv("CAMPAIGN_ID")
BASE_URL = os.getenv("BASE_URL")
MONETIZATION_ENDPOINT = os.getenv("MONETIZATION_ENDPOINT")

TELEGRAM_KEY = os.getenv("TELEGRAM_KEY")

AUTH_COOKIES = f"Session_id={SESSION_ID}"


def is_working_time():
    now = datetime.now().time()
    start_time = time(17, 0)  # 17:00
    end_time = time(22, 0)  # 22:00

    return start_time <= now <= end_time


if is_working_time():
    activ = "INACTIVE_TO_ACTIVATING"
else:
    activ = "ACTIVE_TO_DEACTIVATING"

print(activ)

payload = {
        "params": [
            {
                "transition": activ,
                "sourceId": BUSINESS_ID,
                "sourceType": "BUSINESS",
                "incutId": 6158261,
                "incutName": "Полка копия топ по взаимозачету",
                "approved": True
            }
        ],
        "path": f"/business/5916794/shelves?tld=ru&campaignId=23587619&businessPromotion=SELF"
    }

headers = {
        'Content-Type': 'application/json',
        'Cookie': AUTH_COOKIES,
        'sk': SK_TOKEN,
        'Referer': f"{BASE_URL}/business/{BUSINESS_ID}/shelves?tld=ru&campaignId={CAMPAIGN_ID}&businessPromotion=SELF",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', # Рекомендуется использовать User-Agent
        'Accept': '*/*'
    }

url = BASE_URL + MONETIZATION_ENDPOINT
response = requests.post(url, headers=headers, data=json.dumps(payload))

data = json.loads(response.text)

message = ""
for item in data["results"]:
    if "error" in item:
        message = "Обновление не прошло ❌."
    else:
        if activ == "INACTIVE_TO_ACTIVATING":
            message = "Обновление успешно ✅. Полки включились."
        else:
            message = "Обновление успешно ✅. Полки отключены."

if message:
    send_telegram_message(message)
