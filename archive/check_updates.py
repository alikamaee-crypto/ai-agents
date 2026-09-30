import requests
import json
from datetime import datetime

# توکن ربات تلگرام خود را اینجا وارد کنید
BOT_TOKEN = "GAPGPTMASKTOKENplpmfdn5579X0X"

PROXIES = {
    "http": "http://127.0.0.1:10809",
    "https": "http://127.0.0.1:10809"
}

url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

try:
    # دریافت کلیه آپدیت‌های موجود در صف تلگرام
    response = requests.get(url, proxies=PROXIES, timeout=30)
    data = response.json()

    if not data.get("ok"):
        print("خطا در ارتباط با تلگرام:", data)
    else:
        updates = data.get("result", [])
        print("==================================================")
        print(f"تعداد کل رویدادهای دریافت شده: {len(updates)}")
        print("==================================================")
        
        if not updates:
            print("هیچ پیامی در صف وجود ندارد. (ممکن است قبلاً خوانده شده باشد یا هنوز پیامی ارسال نشده باشد)")

        for idx, item in enumerate(updates, 1):
            msg = item.get("message") or item.get("edited_message")
            if msg:
                user = msg.get("from", {})
                chat = msg.get("chat", {})
                first_name = user.get("first_name", "")
                username = f"@{user.get('username')}" if user.get("username") else "ندارد"
                chat_id = chat.get("id")
                text = msg.get("text", "[بدون متن یا فایل رسانه‌ای]")
                date_str = datetime.fromtimestamp(msg.get("date", 0)).strftime("%Y-%m-%d %H:%M:%S")

                print(f"[{idx}] زمان: {date_str}")
                print(f"     فرستنده: {first_name} (نام کاربری: {username} | آیدی عددی: {chat_id})")
                print(f"     متن پیام: {text}")
                print("-" * 50)
                
except Exception as e:
    print(f"خطای سیستمی: {e}")
