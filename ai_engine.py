# ai_engine.py
# Kamaee Group - Decision & AI Response Engine

HANDOFF_KEYWORDS = ["قرارداد", "فاکتور", "جلسه حضوری", "شکایت", "شراکت", "مدیریت", "جناب کمایی"]
MAX_DISCOUNT_PERCENT = 10.0
MAX_DEAL_VALUE = 10_000_000  # 10 Million Tomans

HANDOFF_MESSAGE = (
    "درخواست شما جهت بررسی دقیق و تصمیم‌گیری نهایی به مدیریت مجموعه "
    "گروه کمائی (Kamaee Group)، جناب آقای کمایی، ارجاع شد. "
    "ایشان به‌زودی در همین گفتگو پاسخگوی شما خواهند بود."
)

CATEGORIES = {
    "1": "ساخت ایجنت اختصاصی",
    "2": "اتوماسیون کسب‌وکار",
    "3": "پروژه‌های فریلنسری و درآمدزایی",
    "4": "مشاوره تخصصی و آموزش"
}

def analyze_intent(user_text: str, discount_requested: float = 0.0, deal_value: float = 0.0):
    """
    بررسی اولیه بر اساس فیلترهای ارجاع به مدیریت و قواعد بیزینس
    """
    # بررسی عبارات کلیدی حساس
    for word in HANDOFF_KEYWORDS:
        if word in user_text:
            return {
                "action": "HANDOFF",
                "reason": f"کلمه کلیدی ارجاع: {word}",
                "reply": HANDOFF_MESSAGE
            }

    # سقف تخفیف و مبلغ قرارداد
    if discount_requested > MAX_DISCOUNT_PERCENT:
        return {
            "action": "HANDOFF",
            "reason": f"تخفیف درخواستی {discount_requested}% بالای سقف مجاز است.",
            "reply": HANDOFF_MESSAGE
        }

    if deal_value > MAX_DEAL_VALUE:
        return {
            "action": "HANDOFF",
            "reason": f"ارزش پروژه ({deal_value:,} تومان) بالاتر از سقف سیستم است.",
            "reply": HANDOFF_MESSAGE
        }

    # تشخیص مقدماتی دسته‌بندی
    detected_cat = "نامشخص"
    if any(k in user_text for k in ["ایجنت", "ربات", "شخصیت"]):
        detected_cat = CATEGORIES["1"]
    elif any(k in user_text for k in ["اتوماسیون", "خودکارسازی", "سیستم سازی"]):
        detected_cat = CATEGORIES["2"]
    elif any(k in user_text for k in ["درآمد", "فریلنسری", "پروژه"]):
        detected_cat = CATEGORIES["3"]
    elif any(k in user_text for k in ["آموزش", "مشاوره", "یادگیری"]):
        detected_cat = CATEGORIES["4"]

    # پاسخ استاندارد برند Kamaee Group
    reply_text = (
        f"درود بر شما. به مجموعه تخصصی هوش مصنوعی Kamaee Group خوش آمدید.\n"
        f"حوزه درخواستی شما: [{detected_cat}]\n"
        f"چگونه می‌توانیم در توسعه این راهکار به شما کمک کنیم؟"
    )

    return {
        "action": "REPLY",
        "category": detected_cat,
        "reply": reply_text
    }

if __name__ == "__main__":
    # تست عملکرد لاجیک
    print("--- تست ۱: پیام معمولی مشاوره ---")
    test1 = analyze_intent("سلام، می‌خواستم درباره آموزش هوش مصنوعی سوال کنم.")
    print("خروجی:", test1["reply"])

    print("\n--- تست ۲: درخواست کلمه حساس (ارجاع به مدیریت) ---")
    test2 = analyze_intent("لطفاً برای عقد قرارداد رسمی و ارسال فاکتور راهنمایی کنید.")
    print("عملیات:", test2["action"])
    print("پیام سیستم:", test2["reply"])

    print("\n--- تست ۳: درخواست تخفیف بیش از حد ---")
    test3 = analyze_intent("قیمت چنده؟", discount_requested=15.0)
    print("عملیات:", test3["action"])
    print("پیام سیستم:", test3["reply"])
