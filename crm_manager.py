import os
import sqlite3
import datetime
import logging
import google.generativeai as genai

# =========================================================
# پیکربندی زیرساخت و ارتباطات شبکه
# =========================================================
DB_NAME = "crm_data.db"
OPENAI_PROXY = "http://127.0.0.1:10809"

# تنظیم پروکسی سیستمی برای عبور ترافیک گوگل از V2RayN
os.environ["HTTP_PROXY"] = OPENAI_PROXY
os.environ["HTTPS_PROXY"] = OPENAI_PROXY

# کلید دریافتی از گوگل را اینجا جایگذاری کنید
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "import os
from google import genai

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
)

tools = [
    {
        'type': 'google_search',
    },
]

generation_config = {
    'temperature': 1,
    'max_output_tokens': 65536,
    'top_p': 0.95,
    'thinking_level': 'high',
}

interaction = client.interactions.create(
    model='models/gemini-3-flash-preview',
    input="""INSERT_INPUT_HERE""",
    tools=tools,
    generation_config=generation_config,
)

print(interaction.steps[-1])



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# پیکربندی اتصال به گوگل جیمینی
genai.configure(api_key=GEMINI_API_KEY)

# =========================================================
# پرامپت مهندسی‌شده: سوپر ایجنت حل مسئله و فروش Kamaee Group
# =========================================================
SYSTEM_PROMPT = """
تو مغز متفکر هوش مصنوعی و سوپر ایجنت ارشد برند Kamaee Group (گروه کمائی) هستی.
ماموریت تو: حل حرفه‌ای هرگونه مسئله، تبدیل کاربر به لید داغ، ارزش‌آفرینی اختصاصی و بستن معامله (Closing Sales) در تمام کانال‌ها (تلگرام، اینستاگرام، واتساپ).

حوزه‌های تسلط جامع:
۱. مالی، سرمایه‌گذاری، حسابداری و مدیریت بحران‌های نقدی
۲. حقوقی، دعاوی، انحصار وراثت، قراردادها و تنظیم لوایح
۳. آموزشی، مهارت‌آموزی، برنامه‌ریزی درسی و تحصیلی
۴. ورزشی، برنامه‌ریزی تغذیه، تناسب اندام و ریکاوری
۵. کسب‌وکار، اتوماسیون، بهینه‌سازی فرآیندها و هوش مصنوعی
۶. فنی، خودرو، مهندسی و مسائل عمومی روزمره

اصول ۵ مرحله‌ای رفتار و قیف فروش (Sales Funnel Execution):
مرحله ۱: ارزیابی و ارزش‌آفرینی اولیه (Value Injection)
- پیام کاربر را در هر زمینه‌ای که باشد با منطق کامل، احترام و دقت بالا تحلیل کن.
- یک راه‌حل اولیه، استراتژیک و کاربردی بده تا کاربر تخصص و اقتدار Kamaee Group را احساس کند.

مرحله ۲: حرارت‌سنجی و تبدیل به لید داغ (Lead Warming)
- عواقب حل‌نشدن ریشه‌ای مسئله یا فرصت‌های از دست رفته را برای کاربر شفاف کن.
- حس فوریت منطقی ایجاد کن تا متوجه شود نیاز به یک نقشه راه اختصاصی و منسجم دارد.

مرحله ۳: طراحی و معرفی محصول متناسب (Customized Offer)
- برای درد یا خواسته دقیق کاربر، یک محصول دیجیتال یا بسته اختصاصی پیشنهاد بده (مانند: کتابچه جامع اقدام، برنامه گام‌به‌گام اختصاصی، پکیج چک‌لیست و راهکار اجرایی، شیوه‌نامه گام‌به‌گام).
- ارزش واقعی آن را بسیار بالاتر از هزینه مطرح کن.

مرحله ۴: مدیریت هوشمند چانه‌زنی و ابهامات (Objection Handling)
- اگر کاربر درباره قیمت یا هزینه تردید کرد یا چانه زد، ارزش افزوده، پشتیبانی و گارانتی کارآمدی را برجسته کن.
- پیشنهاد تخفیف اقدام سریع یا نسخه فشرده ارائه بده تا مانع مالی برطرف شود.

مرحله ۵: هدایت به بستن معامله (Call To Action)
- در پایان پاسخ، دقیقاً بگو چه کاری انجام دهد (مثلاً: «جهت دریافت نسخه کامل و فعال‌سازی این بسته اختصاصی، عدد ۱ یا کلمه "ثبت سفارش" را ارسال فرمایید»).

قوانین ساختاری و نگارشی:
- لحن کاملاً جدی، مقتدر، حرفه‌ای، منطقی، صمیمی، دلسوز و بدون شوخی باشد.
- مطالب را بخش‌بندی‌شده، تمیز و ساختاریافته بنویس.
- زبان پاسخ تماماً فارسی دقیق و شیوا باشد.
"""

# مدل پیش‌فرض پرسرعت و بهینه گوگل
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# =========================================================
# مدیریت پایگاه داده یکپارچه CRM
# =========================================================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            user_id TEXT,
            username TEXT,
            category TEXT,
            status TEXT,
            score REAL DEFAULT 0.0,
            deal_value REAL DEFAULT 0.0,
            notes TEXT,
            created_at TEXT,
            updated_at TEXT,
            followup_status TEXT DEFAULT 'pending',
            chat_id INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

def detect_category(message: str) -> str:
    text = message.lower()
    if any(w in text for w in ["ارث", "وراثت", "دادگاه", "حقوق", "وکیل", "قرارداد", "شکایت", "سند"]):
        return "حقوقی و قراردادها"
    if any(w in text for w in ["مالی", "سرمایه", "وام", "بدهی", "سود", "هزینه", "بودجه", "حسابداری"]):
        return "مالی و سرمایه‌گذاری"
    if any(w in text for w in ["ورزش", "بدنسازی", "لاغری", "چاقی", "برنامه تمرینی", "رژیم", "مکمل"]):
        return "ورزشی و تناسب اندام"
    if any(w in text for w in ["درس", "کنکور", "آموزش", "دانشگاه", "مهارت", "یادگیری", "دوره"]):
        return "آموزشی و مهارتی"
    if any(w in text for w in ["سمند", "خودرو", "ماشین", "موتور", "برق", "سنسور", "تعمیر"]):
        return "فنی و خودرو"
    return "عمومی و کسب‌وکار"

def calculate_lead_score(message: str) -> tuple:
    text = message.lower()
    status = "Qualified"
    score = 40.0

    hot_keywords = ["خرید", "ثبت سفارش", "قیمت", "هزینه", "تخفیف", "شماره کارت", "چطور بخرم", "ارسال کنید"]
    objection_keywords = ["گرونه", "ارزون‌تر", "تخفیف نداره", "چقدر میشه", "کمتر راه نداره"]

    if any(w in text for w in hot_keywords):
        status = "Hot Lead"
        score = 85.0
    elif any(w in text for w in objection_keywords):
        status = "Negotiation (چانه زنی)"
        score = 75.0
    elif len(text.split()) > 10:
        status = "Warm Lead"
        score = 60.0

    return status, score

# =========================================================
# موتور هوش مصنوعی Gemini
# =========================================================
def ask_ai_agent(user_message: str, history_notes: str = "") -> str:
    if not user_message or not user_message.strip():
        return "درود و احترام. لطفاً مسئله یا چالش خود را مطرح فرمایید تا دقیق‌ترین راهکار اختصاصی خدمت شما ارائه گردد."

    prompt_content = ""
    if history_notes:
        clean_context = history_notes[-1500:]
        prompt_content += f"[سوابق تعاملات قبلی برای پیگیری و مذاکره:\n{clean_context}]\n\n"

    prompt_content += f"پیام کاربر:\n{user_message.strip()}"

    try:
        response = model.generate_content(
            prompt_content,
            generation_config=genai.types.GenerationConfig(
                temperature=0.4,
                max_output_tokens=900,
            )
        )
        return response.text.strip() if response and response.text else "پاسخی دریافت نشد، لطفاً دوباره ارسال فرمایید."

    except Exception as error:
        logger.exception("خطا در پاسخ‌دهی ایجنت Gemini: %s", error)
        return (
            "سامانه هوشمند در حال به‌روزرسانی لحظه‌ای است. "
            "پیام شما ثبت گردید و به زودی راهکار دقیق ارسال خواهد شد."
        )

# =========================================================
# پردازش جریان ورودی پیام، ثبت چندکاناله و ذخیره CRM
# =========================================================
def process_incoming_message(
    user_id: int,
    username: str,
    full_name: str,
    message: str,
    platform: str = "telegram"
) -> str:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    category = detect_category(message)
    status, score = calculate_lead_score(message)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, notes FROM leads WHERE user_id = ?", (str(user_id),))
    row = cursor.fetchone()

    old_notes = row[1] if row and row[1] else ""
    current_log = f"[{now}] [{platform.upper()}] کاربر: {message}"
    combined_notes = f"{old_notes}\n{current_log}".strip()[-8000:]

    ai_reply = ask_ai_agent(message, history_notes=old_notes)

    agent_log = f"[{now}] [AGENT]: {ai_reply[:150]}..."
    combined_notes = f"{combined_notes}\n{agent_log}".strip()

    if row:
        lead_id = row[0]
        cursor.execute("""
            UPDATE leads
            SET
                username = ?,
                category = ?,
                status = ?,
                score = ?,
                notes = ?,
                updated_at = ?,
                followup_status = 'pending'
            WHERE id = ?
        """, (
            username or full_name or "مشتری محترم",
            category,
            status,
            score,
            combined_notes,
            now,
            lead_id
        ))
    else:
        cursor.execute("""
            INSERT INTO leads (
                platform,
                user_id,
                username,
                category,
                status,
                score,
                deal_value,
                notes,
                created_at,
                updated_at,
                followup_status,
                chat_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            platform,
            str(user_id),
            username or full_name or "مشتری محترم",
            category,
            status,
            score,
            0.0,
            combined_notes,
            now,
            now,
            "pending",
            user_id
        ))

    conn.commit()
    conn.close()

    return ai_reply

def analyze_intent(message: str) -> tuple:
    category = detect_category(message)
    status, _ = calculate_lead_score(message)
    reply = ask_ai_agent(message)
    return category, status, reply

def get_pending_followups():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT chat_id, username, category, status
        FROM leads
        WHERE followup_status = 'pending' AND chat_id IS NOT NULL
    """)
    rows = cursor.fetchall()
    conn.close()
    return [
        {"chat_id": r[0], "username": r[1], "category": r[2], "status": r[3]}
        for r in rows
    ]

def update_followup_status(chat_id: int, status: str = "followed_up"):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE leads
        SET followup_status = ?, updated_at = ?
        WHERE chat_id = ?
    """, (status, now, chat_id))
    conn.commit()
    conn.close()
