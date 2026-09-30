import sqlite3
import html
from pathlib import Path
from datetime import datetime

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


# شناسه عددی تلگرام مدیر اصلی
ADMIN_ID = 106928579

# مسیر مطمئن دیتابیس در کنار فایل‌های پروژه
DB_PATH = Path(__file__).resolve().parent / "crm_data.db"


def is_admin(update: Update) -> bool:
    """بررسی می‌کند دستور فقط از طرف مدیر ارسال شده باشد."""
    user = update.effective_user

    if user is None:
        return False

    return user.id == ADMIN_ID


async def access_denied(update: Update):
    """پاسخ به کاربران غیرمجاز."""
    if update.message:
        await update.message.reply_text(
            "این دستور فقط برای مدیریت مجموعه فعال است."
        )


async def send_chunks(update: Update, lines):
    """ارسال پیام‌های طولانی در چند بخش."""
    if not update.message:
        return

انی در چند بخش."""
    if not update.message:
        return

        if len(current) + len(line) + 1 > 3800:
            chunks.append(current)
            current = line
        else:
            if current:
                current += "\n"
            current += line

    if current:
        chunks.append(current)

    for chunk in chunks:
        await update.message.reply_text(
            chunk,
            parse_mode="HTML"
        )


async def leads_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """نمایش آخرین لیدهای ثبت‌شده."""

    if not is_admin(update):
        await access_denied(update)
        return

    try:
        connection = sqlite3.connect(str(DB_PATH))
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM leads
            ORDER BY id DESC
            LIMIT 20
        """)

        rows = cursor.fetchall()
        connection.close()

        if not rows:
            await update.message.reply_text(
                "هیچ لیدی در دیتابیس ثبت نشده است."
            )
            return

        lines = [
            "📊 <b>آخرین لیدهای Kamaee Group</b>",
            "━━━━━━━━━━━━━━━━━━━━"
        ]

        for row in rows:
            lead_id = row[0]
            user_id = row[2]
            username = row[3] or "-"
            need = row[4] or "-"
            status = row[5] or "-"
            message = row[8] or "-"
            created_at = row[9] or "-"

            username = html.escape(str(username))
            need = html.escape(str(need))
            status = html.escape(str(status))
            message = html.escape(str(message))
            created_at = html.escape(str(created_at))

            if len(message) > 100:
                message = message[:100] + "..."

            lines.append(
                f"🆔 <b>لید {lead_id}</b>\n"
                f"👤 کاربر: @{username}\n"
                f"🔢 شناسه: <code>{user_id}</code>\n"
                f"🎯 نیاز: {need}\n"
                f"📌 وضعیت: <b>{status}</b>\n"
                f"💬 پیام: {message}\n"
                f"🕒 زمان: {created_at}\n"
                f"━━━━━━━━━━━━━━━━━━━━"
            )

        await send_chunks(update, lines)

    except Exception as error:
        await update.message.reply_text(
            "خطا در خواندن اطلاعات لیدها."
        )
        print("LEADS COMMAND ERROR:", error)


async def stats_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """نمایش آمار کلی CRM."""

    if not is_admin(update):
        await access_denied(update)
        return

    try:
        connection = sqlite3.connect(str(DB_PATH))
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM leads")
        total_leads = cursor.fetchone()[0]

        cursor.execute("""
            SELECT status, COUNT(*)
            FROM leads
            GROUP BY status
            ORDER BY COUNT(*) DESC
        """)
        status_rows = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT(*)
            FROM followups
            WHERE status = 'pending'
        """)
        pending_followups = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM followups
            WHERE status = 'cancelled'
        """)
        cancelled_followups = cursor.fetchone()[0]

        connection.close()

        lines = [
            "📈 <b>آمار مدیریتی Kamaee Group</b>",
            "━━━━━━━━━━━━━━━━━━━━",
            f"👥 مجموع لیدها: <b>{total_leads}</b>",
            f"⏳ پیگیری‌های فعال: <b>{pending_followups}</b>",
            f"✅ پیگیری‌های لغوشده: <b>{cancelled_followups}</b>",
            "",
            "📌 <b>تفکیک وضعیت لیدها:</b>"
        ]

        if status_rows:
            for status, count in status_rows:
                status = html.escape(str(status or "-"))
                lines.append(f"• {status}: <b>{count}</b>")
        else:
            lines.append("• هنوز آماری ثبت نشده است.")

        await send_chunks(update, lines)

    except Exception as error:
        await update.message.reply_text(
            "خطا در محاسبه آمار CRM."
        )
        print("STATS COMMAND ERROR:", error)


async def handoff_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """نمایش لیدهای ارجاع‌شده به مدیریت."""

    if not is_admin(update):
        await access_denied(update)
        return

    try:
        connection = sqlite3.connect(str(DB_PATH))
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM leads
            WHERE status = 'Handoff'
            ORDER BY id DESC
            LIMIT 20
        """)

        rows = cursor.fetchall()
        connection.close()

        if not rows:
            await update.message.reply_text(
                "در حال حاضر هیچ لید ارجاع‌شده‌ای وجود ندارد."
            )
            return

        lines = [
            "🚨 <b>لیدهای ارجاع‌شده به مدیریت</b>",
            "━━━━━━━━━━━━━━━━━━━━"
        ]

        for row in rows:
            lead_id = row[0]
            user_id = row[2]
            username = row[3] or "-"
            need = row[4] or "-"
            message = row[8] or "-"
            created_at = row[9] or "-"

            username = html.escape(str(username))
            need = html.escape(str(need))
            message = html.escape(str(message))
            created_at = html.escape(str(created_at))

            if len(message) > 120:
                message = message[:120] + "..."

            lines.append(
                f"🆔 <b>لید {lead_id}</b>\n"
                f"👤 کاربر: @{username}\n"
                f"🔢 شناسه: <code>{user_id}</code>\n"
                f"🎯 نیاز: {need}\n"
                f"💬 پیام: {message}\n"
                f"🕒 زمان: {created_at}\n"
                f"━━━━━━━━━━━━━━━━━━━━"
            )

        await send_chunks(update, lines)

    except Exception as error:
        await update.message.reply_text(
            "خطا در خواندن لیدهای ارجاع‌شده."
        )
        print("HANDOFF COMMAND ERROR:", error)


async def admin_help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """راهنمای دستورات مدیریت."""

    if not is_admin(update):
        await access_denied(update)
        return

    await update.message.reply_text(
        "🛠 <b>دستورات مدیریت Kamaee Group</b>\n\n"
        "/leads - نمایش آخرین لیدها\n"
        "/stats - نمایش آمار CRM\n"
        "/handoff - نمایش لیدهای ارجاع‌شده\n"
        "/adminhelp - نمایش این راهنما",
        parse_mode="HTML"
    )


def register_admin_handlers(application):
    """ثبت دستورات مدیریت در ربات."""

    application.add_handler(
        CommandHandler("leads", leads_command)
    )

    application.add_handler(
        CommandHandler("stats", stats_command)
    )

    application.add_handler(
        CommandHandler("handoff", handoff_command)
    )

    application.add_handler(
        CommandHandler("adminhelp", admin_help_command)
    )
