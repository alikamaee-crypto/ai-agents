# -*- coding: utf-8 -*-
import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service

print("Starting Firefox driver locally...")

# تعیین مسیر درایور در پوشه فعلی
driver_path = os.path.abspath("geckodriver.exe")
service = Service(executable_path=driver_path)

driver = webdriver.Firefox(service=service)

try:
    print("Opening browser and loading Google...")
    driver.get("https://www.google.com")
    print("Page title successfully fetched:", driver.title)
    time.sleep(5)
finally:
    print("Closing browser...")
    driver.quit()
    print("Browser test completed successfully.")
