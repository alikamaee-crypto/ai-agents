import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

print("در حال آماده‌سازی درایور فایرفاکس...")

service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service)

try:
    print("در حال باز کردن مرورگر و لود صفحه گوگل...")
    driver.get("https://www.google.com")
    print("عنوان صفحه دریافت شد:", driver.title)
    time.sleep(5)
finally:
    print("بستن مرورگر...")
    driver.quit()
    print("عملیات با موفقیت انجام شد.")
