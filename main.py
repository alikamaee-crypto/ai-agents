import requests
import urllib3

# غیرفعال کردن هشدارهای امنیتی مربوط به SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TOKEN = '8943809140:AAHKMTgFUW-OHR_fYttNZq0nAjOdxTcb1Gs'
CHAT_ID = '106928579' # آیدی خود را اینجا قرار دهید

# تنظیمات پراکسی (پورت 10809 مربوط به HTTP در V2RayN)
proxies = {
    'http': 'http://127.0.0.1:10809',
    'https': 'http://127.0.0.1:10809'
}

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': text}
    try:
        # اضافه کردن verify=False برای دور زدنِ تداخلِ گواهینامه‌های SSL
        response = requests.post(url, data=payload, proxies=proxies, timeout=15, verify=False)
        if response.status_code == 200:
            print("✅ پیام با موفقیت ارسال شد.")
        else:
            print(f"❌ خطا از سمت سرور تلگرام: {response.text}")
    except Exception as e:
        print(f"❌ خطای شبکه: {e}")

if __name__ == "__main__":
    send_message("سیستم Kamaee Group آنلاین شد.")
