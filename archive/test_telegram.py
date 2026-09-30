# -*- coding: utf-8 -*-
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json

def load_token():
    env_file = Path(".env")
    if not env_file.exists():
        raise FileNotFoundError("فایل .env پیدا نشد.")

    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("TELEGRAM_BOT_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise ValueError("TELEGRAM_BOT_TOKEN در فایل .env پیدا نشد.")

TOKEN = load_token()

def telegram_api(method, params=None):
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    data = urlencode(params or {}).encode("utf-8")
    req = Request(url, data=data)
    with urlopen(req, timeout=20) as resp:
        res = json.loads(resp.read().decode("utf-8"))
    if not res.get("ok"):
        raise RuntimeError(res)
    return res["result"]

bot = telegram_api("getMe")
print("Bot connected:", bot.get("username"))

updates = telegram_api("getUpdates")
chat_id = None

for update in reversed(updates):
    message = update.get("message", {})
    chat = message.get("chat", {})
    if chat.get("type") == "private":
        chat_id = chat.get("id")
        break

if chat_id is None:
    raise RuntimeError("گفت‌وگوی خصوصی پیدا نشد. مجدد به ربات پیام /start بدهید.")

telegram_api("sendMessage", {
    "chat_id": chat_id,
    "text": "سلام علی آقا! اتصال ایجنت هوش مصنوعی به تلگرام با موفقیت برقرار شد."
})

print("Message sent successfully!")
