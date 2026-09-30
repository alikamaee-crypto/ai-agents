import requests
import json

proxies = {
    "http": "http://127.0.0.1:10809",
    "https": "http://127.0.0.1:10809"
}

API_KEY = os.getenv("GEMINI_API_KEY")

CANDIDATE_MODELS = [
    "gemini-flash-lite-latest",
    "gemini-3.1-flash-lite",
    "gemini-2.5-pro",
    "gemini-pro-latest",
    "gemini-3.5-flash"
]

try:
    with open("system_prompt.txt", "r", encoding="utf-8") as f:
        system_instruction = f.read()
except FileNotFoundError:
    print("خطا: فایل system_prompt.txt پیدا نشد!")
    exit()

# حافظه مکالمات به تفکیک کاربر: {chat_id: [{"role": "user"|"model", "parts": [...]}]}
USER_SESSIONS = {}

def ask_agent(user_message, chat_id=1):
    # مقداردهی اولیه سابقه چت برای کاربر جدید
    if chat_id not in USER_SESSIONS:
        USER_SESSIONS[chat_id] = []
        
    # افزودن پیام جدید کاربر به تاریخچه
    USER_SESSIONS[chat_id].append({
        "role": "user",
        "parts": [{"text": user_message}]
    })
    
    # نگه داشتن حداکثر ۱۰ پیام آخر برای جلوگیری از سنگین شدن ترافیک
    if len(USER_SESSIONS[chat_id]) > 10:
        USER_SESSIONS[chat_id] = USER_SESSIONS[chat_id][-10:]
        
    headers = {"Content-Type": "application/json"}
    payload = {
        "system_instruction": {
            "parts": [{"text": system_instruction}]
        },
        "contents": USER_SESSIONS[chat_id]
    }
    
    last_error = ""
    for model in CANDIDATE_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
        try:
            response = requests.post(url, headers=headers, json=payload, proxies=proxies, timeout=60)
            result = response.json()
            
            if response.status_code == 200:
                answer = result['candidates'][0]['content']['parts'][0]['text']
                # ذخیره پاسخ مدل در تاریخچه همان کاربر
                USER_SESSIONS[chat_id].append({
                    "role": "model",
                    "parts": [{"text": answer}]
                })
                return answer, model
            else:
                last_error = result.get('error', {}).get('message', response.text)
        except Exception as e:
            last_error = str(e)
            
    return f"تمام مدل‌ها شلوغ بودند. خطا: {last_error}", None
