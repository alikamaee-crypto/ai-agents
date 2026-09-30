import time
import requests
from agent_brain import ask_agent

# ================= تنظیمات =================
# توکن دریافتی از BotFather را دقیقاً بین دو کوتیشن قرار دهید
BOT_TOKEN = "8943809140:AAHKMTgFUW-OHR_fYttNZq0nAjOdxTcb1Gs"

# پروکسی هماهنگ با v2rayN
PROXIES = {
    "http": "http://127.0.0.1:10809",
    "https": "http://127.0.0.1:10809"
}

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
# ===========================================

def get_updates(offset=None):
    url = f"{BASE_URL}/getUpdates"
    params = {"timeout": 20, "offset": offset}
    try:
        response = requests.get(url, params=params, proxies=PROXIES, timeout=30)
        if response.status_code == 200:
            return response.json().get("result", [])
        else:
            print(f"خطای دریافت آپدیت از تلگرام: {response.text}")
    except Exception as e:
        print(f"خطای شبکه تلگرام: {e}")
    return []

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        response = requests.post(url, json=payload, proxies=PROXIES, timeout=20)
        return response.status_code == 200
    except Exception as e:
        print(f"خطای ارسال پیام: {e}")
        return False

def main():
    print("==================================================")
    print("  ربات تلگرام گروه کمائی متصل به هوش مصنوعی روشن شد  ")
    print("==================================================")
    print("در حال شنود پیام‌های ورودی لیدها...")
    
    last_update_id = None

    while True:
        updates = get_updates(last_update_id)
        for update in updates:
            last_update_id = update["update_id"] + 1
            
            message = update.get("message")
            if not message or "text" not in message:
                continue
                
            chat_id = message["chat"]["id"]
            user_text = message["text"]
            user_name = message["from"].get("first_name", "کاربر")
            
            print(f"\n[پیام جدید] از {user_name} ({chat_id}): {user_text}")
            
            # ارسال به مغز هوش مصنوعی
            ai_reply, used_model = ask_agent(user_text)
            
            print(f"[پاسخ هوش مصنوعی با {used_model} آماده شد]")
            
            # ارسال پاسخ به کاربر
            if send_message(chat_id, ai_reply):
                print(f"[پاسخ با موفقیت به {user_name} ارسال شد]")
            else:
                print(f"[خطا در تحویل پاسخ به تلگرام]")
            
        time.sleep(1)

if __name__ == "__main__":
    main()
