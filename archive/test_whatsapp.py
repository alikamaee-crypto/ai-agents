# -*- coding: utf-8 -*-
import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

current_dir = os.path.dirname(os.path.abspath(__file__))
driver_path = os.path.join(current_dir, "geckodriver.exe")

# پوشه ذخیره نشست کاربر برای مراجعات بعدی
profile_dir = os.path.join(current_dir, "whatsapp_profile")
if not os.path.exists(profile_dir):
    os.makedirs(profile_dir)

options = Options()
options.add_argument("-profile")
options.add_argument(profile_dir)

service = Service(executable_path=driver_path)

print("[INFO] Launching Firefox for WhatsApp Web...")
driver = webdriver.Firefox(service=service, options=options)

try:
    driver.get("https://web.whatsapp.com")
    print("[INFO] WhatsApp Web opened.")
    print("=" * 60)
    print("[ACTION REQUIRED]")
    print("1. Open WhatsApp on your phone.")
    print("2. Go to Settings > Linked Devices > Link a Device.")
    print("3. Scan the QR code displayed on the screen.")
    print("4. Wait until your chats load completely.")
    print("=" * 60)
    input(">>> Press Enter in this terminal AFTER your chats are loaded... ")
    print("[SUCCESS] Session saved in profile folder.")
finally:
    driver.quit()
    print("[INFO] Browser closed successfully.")
