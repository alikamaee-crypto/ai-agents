import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

target_phone = os.getenv("WHATSAPP_TARGET_PHONE")
if not target_phone or "xxxx" in target_phone:
    print("خطا: لطفاً متغیر WHATSAPP_TARGET_PHONE را در فایل .env مقداردهی کنید.")
    exit(1)

message = "پیام تستی سیستم اتوماسیون Kamaee Group"

# مسیر درایور و پروفایل محلی
profile_path = os.path.abspath("whatsapp_profile")
gecko_path = os.path.abspath("geckodriver.exe")

options = Options()
options.add_argument("-profile")
options.add_argument(profile_path)

service = Service(executable_path=gecko_path)
driver = webdriver.Firefox(service=service, options=options)

try:
    print("در حال باز کردن واتساپ با نشست ذخیره‌شده...")
    url = f"https://web.whatsapp.com/send?phone={target_phone}"
    driver.get(url)

    print("در حال انتظار برای بارگذاری کادر پیام...")
    wait = WebDriverWait(driver, 35)

    # جستجوی کادر ورود پیام با استفاده از سلکتورهای پایدار واتساپ وب
    input_box = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            '//footer//div[@contenteditable="true"] | //div[@role="textbox"][@contenteditable="true"]'
        ))
    )

    time.sleep(2)
    input_box.click()
    input_box.send_keys(message)
    time.sleep(1)
    input_box.send_keys(Keys.ENTER)

    print("پیام با موفقیت ارسال شد.")
    time.sleep(5)

except Exception as e:
    print(f"خطا در ارسال پیام: {e}")
    driver.save_screenshot("whatsapp_send_error.png")

finally:
    driver.quit()
