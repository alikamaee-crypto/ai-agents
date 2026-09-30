import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from crm_manager import process_incoming_message, get_pending_followups, update_followup_status

# بارگذاری متغیرهای محیطی
load_dotenv()

# پیکربندی سیستم لاگ
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("خطا: متغیر TELEGRAM_BOT_TOKEN در فایل .env یافت نشد.")

# تنظیم پروکسی لوکال V2RayN
PROXY_URL = os.getenv("PROXY_URL", "http://127.0.0.1:10809")

# تنظیم اسکژولر با تایم‌زون مشخص برای رفع خطای ویندوز
scheduler = AsyncIOScheduler(timezone="Asia/Tehran")

async def send_followup_job(application):
    """بررسی و ارسال خودکار پیام‌های پیگیری به لیدها"""
    try:
        pending_leads = get_pending_followups()
        for lead in pending_leads:
            chat_id = lead["chat_id"]
            message_text = (
                "سلام و درود! 🌟\n"
                "علی‌آقا از گروه کمائی پیگیر وضعیت درخواست شما هستند.\n"
                "آیا در خصوص سفارش و راه‌اندازی ایجنت هوش مصنوعی نیاز به راهنمایی بیشتری دارید؟"
            )
            await application.bot.send_message(chat_id=chat_id, text=message_text)
            update_followup_status(chat_id, status="followed_up")
            logger.info(f"پیام پیگیری برای شناسه {chat_id} ارسال شد.")
    except Exception as e:
        logger.error(f"خطا در ارسال پیگیری خودکار: {e}")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پاسخ به دستور استارت"""
    user = update.effective_user
    welcome_text = (
        f"سلام {user.first_name} عزیز! به مجموعه‌ی Kamaee Group خوش آمدید.\n"
        "سیستم هوشمند پشتیبانی و فروش آماده‌ی ثبت سفارش و پاسخگویی به شماست."
    )
    await update.message.reply_text(welcome_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دریافت پیام، پردازش منطقی و ثبت در دیتابیس CRM"""
    user = update.effective_user
    text = update.message.text

    reply_text = process_incoming_message(
        user_id=user.id,
        username=user.username,
        full_name=user.full_name,
        message=text
    )
    
    await update.message.reply_text(reply_text)

async def post_init(application):
    """راه‌اندازی اسکژولر پس از اتصال موفق به تلگرام"""
    scheduler.add_job(send_followup_job, "interval", hours=1, args=[application])
    scheduler.start()
    logger.info("اسکژولر پیگیری خودکار Kamaee Group با موفقیت فعال شد.")

def main():
    logger.info(f"در حال اتصال به تلگرام از طریق پروکسی: {PROXY_URL}")
    application = (
        ApplicationBuilder()
        .token(TOKEN)
        .proxy(PROXY_URL)
        .get_updates_proxy(PROXY_URL)
        .post_init(post_init)
        .build()
    )

    # اتصال دستورات و هندلرها
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("ربات گروه کمائی روشن شد و در حال دریافت پیام است...")
    application.run_polling()

if __name__ == "__main__":
    main()
