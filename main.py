import json
import datetime
import re

class NexusIntelligenceAgent:
    """
    موتور ایجنت هوشمند پردازش سیگنال، فرصت‌های مالی و لیدهای با ارزش بالا
    (Nexus Autonomous Market & Lead Intelligence Core)
    """
    def __init__(self, agent_name="Nexus-Prime"):
        self.agent_name = agent_name
        self.version = "2.1-Alpha"
        self.log_file = "execution_logs.txt"
        self.processed_records = []

    def log_event(self, record):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        payload = {
            "timestamp": timestamp,
            "agent": self.agent_name,
            "version": self.version,
            "payload": record
        }
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def analyze_opportunity(self, source_id, raw_text):
        """تحلیل عمیق ورودی، استخراج ارقام مالی، تعیین ریسک و ارزش اقدام"""
        text_lower = raw_text.lower()
        
        # ۱. استخراج خودکار مقادیر مالی (میلیون / میلیارد / اعداد)
        found_amounts = re.findall(r'\d+', raw_text)
        est_volume = int(found_amounts[0]) if found_amounts else 0

        # ۲. محاسبه نمره اهمیت و فوریت (Lead Scoring Engine)
        score = 50
        urgency = "NORMAL"
        sentiment = "NEUTRAL"
        
        if any(w in text_lower for w in ["فوری", "عجله", "urgent", "مهم", "نقد", "تسویه"]):
            score += 30
            urgency = "CRITICAL"
            
        if any(w in text_lower for w in ["سرمایه", "میلیارد", "دلاری", "پروژه بزرگ", "عمده"]):
            score += 25
            
        if any(w in text_lower for w in ["مشکل", "اعتراض", "خراب", "شکایت", "کلاهبرداری"]):
            sentiment = "NEGATIVE_RISK"
            score += 15
        elif any(w in text_lower for w in ["عالی", "موافقم", "تایید", "آماده"]):
            sentiment = "POSITIVE"

        # دسته‌بندی نهایی اقدام ایجنت
        if score >= 80:
            tier = "VIP_GOLD"
            action_code = "DISPATCH_IMMEDIATE_NOTIFICATION"
            response_strategy = "اتصال خودکار به خط اول مذاکره / رزرو سهمیه اختصاصی"
        elif score >= 55:
            tier = "STANDARD_ACTIVE"
            action_code = "EXECUTE_PIPELINE_ROUTING"
            response_strategy = "ثبت در صف تبدیل فرصت و ارائه کاتالوگ ارزش‌افزوده"
        else:
            tier = "NURTURE_POOL"
            action_code = "AUTO_ENGAGE_NURTURE"
            response_strategy = "ارسال پاسخ خودکار هوشمند و پایش تعامل آتی"

        analysis_report = {
            "source_channel": source_id,
            "raw_input": raw_text,
            "intelligence_matrix": {
                "lead_score": score,
                "urgency_level": urgency,
                "sentiment_vector": sentiment,
                "detected_volume_units": est_volume,
                "tier_classification": tier
            },
            "autonomous_decision": {
                "action_code": action_code,
                "execution_strategy": response_strategy
            }
        }

        self.processed_records.append(analysis_report)
        self.log_event(analysis_report)
        return analysis_report

if __name__ == "__main__":
    print(f"\n========================================================")
    print(f"[*] راه اندازی هسته هوشمند Nexus Intelligence Agent")
    print(f"[*] حالت پایش فعال: پردازش رویدادهای زنده و فرصت‌های سودآور")
    print(f"========================================================\n")

    agent = NexusIntelligenceAgent()

    # سیگنال‌ها و پیام‌های ورودی با ارزش بالا برای تست قدرت تحلیل موتور
    incoming_streams = [
        {"source": "Direct_Client_X", "content": "سلام، آماده سرمایه‌گذاری ۵۰۰ میلیونی فوری در پروژه نقد هستم"},
        {"source": "Market_Bot_Scraper", "content": "آگهی جدید زیر قیمت منطقه ثبت شد، ارزش تخمینی ۱۲۰۰ واحد"},
        {"source": "Corporate_Inquiry", "content": "درخواست عقد قرارداد تامین سازمانی ماهانه به صورت عمده و همکاری رسمی"},
        {"source": "Standard_User", "content": "شرایط عضویت و خدمات پلتفرم شما چطوریه؟"}
    ]

    for stream in incoming_streams:
        result = agent.analyze_opportunity(stream["source"], stream["content"])
        matrix = result["intelligence_matrix"]
        decision = result["autonomous_decision"]
        
        print(f"▶ کانال ورودی: {result['source_channel']}")
        print(f"  متن پیام: \"{result['raw_input']}\"")
        print(f"  [تحلیل هوشمند] رتبه: {matrix['tier_classification']} | امتیاز: {matrix['lead_score']} | فوریت: {matrix['urgency_level']}")
        print(f"  [تصمیم ایجنت]: {decision['execution_strategy']}")
        print("-" * 56)

    print("\n[✓] تحلیل ماتریسی تمام سیگنال‌ها انجام و در لاگ پایدار ثبت شد.")
