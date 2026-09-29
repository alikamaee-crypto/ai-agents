# -*- coding: utf-8 -*-
import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebAutomationAgent:
    """
    هسته ماژولار ایجنت اتوماسیون با قابلیت مدیریت خطایاب و استخراج داده
    """
    def __init__(self, headless=False):
        self.headless = headless
        self.driver = None
        self.wait = None
        self._setup_driver()

    def _setup_driver(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        gecko_path = os.path.join(current_dir, "geckodriver.exe")
        
        options = Options()
        if self.headless:
            options.add_argument("--headless")

        # حذف ردپای اتوماسیون برای جلوگیری از بلاک شدن توسط بات‌هانترها
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("useAutomationExtension", False)

        service = Service(executable_path=gecko_path)
        self.driver = webdriver.Firefox(service=service, options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        print("[Agent Status] موتور مرورگر با موفقیت فعال شد.")

    def navigate_to(self, url):
        """بارگذاری آدرس با گزارش کامل"""
        print(f"[Agent Action] رفتن به: {url}")
        self.driver.get(url)
        time.sleep(2)
        print(f"[Agent Info] عنوان فعلی صفحه: {self.driver.title}")
        print(f"[Agent Info] آدرس نهایی صفحه: {self.driver.current_url}")

    def extract_elements_text(self, css_selector, limit=5):
        """استخراج متن المان‌های صفحه بر اساس CSS Selector"""
        results = []
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
            elements = self.driver.find_elements(By.CSS_SELECTOR, css_selector)
            for el in elements:
                txt = el.text.strip()
                if txt and txt not in results:
                    results.append(txt)
                if len(results) >= limit:
                    break
        except Exception as e:
            print(f"[Agent Warning] المان با سلکتور '{css_selector}' یافت نشد.")
        return results

    def take_screenshot(self, filename="agent_output.png"):
        """ثبت وضعیت تصویری صفحه"""
        self.driver.save_screenshot(filename)
        print(f"[Agent Log] تصویر صفحه ذخیره شد: {filename}")

    def close(self):
        """خاتمه جلسه کاربری"""
        if self.driver:
            self.driver.quit()
            print("[Agent Status] جلسه مرورگر بسته شد.")

if __name__ == "__main__":
    agent = WebAutomationAgent(headless=False)
    try:
        # تست روی یک تارگت معتبر با ساختار استاندارد (اخبار و رویدادهای پایتون)
        agent.navigate_to("https://www.python.org/blogs/")
        
        print("\n[Agent Action] در حال جمع‌آوری عناوین آخرین مقالات و آپدیت‌ها...")
        articles = agent.extract_elements_text("h3 a", limit=5)
        
        print("\n--- [Agent Output] فهرست استخراج‌شده ---")
        if articles:
            for idx, item in enumerate(articles, 1):
                print(f"{idx}. {item}")
        else:
            print("هیچ متنی استخراج نشد.")

        agent.take_screenshot("python_blogs.png")
    finally:
        agent.close()
