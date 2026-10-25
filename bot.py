import os
from datetime import time
from zoneinfo import ZoneInfo
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update

TOKEN = os.environ["BOT_TOKEN"]
VAQT = time(13, 30, tzinfo=ZoneInfo("Asia/Tashkent"))  # har kuni 13:30
SAVOL = "Obeddan keyin nima ichamiz? 🥤"
VARIANTLAR = ["Yashil choy 🍵", "Qora choy ☕", "Suv 💧", "Kompot 🧃", "Sok 🍊", "Kofe ☕"]


async def poll_yubor(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_poll(
        chat_id=context.job.chat_id,
        question=SAVOL,
        options=VARIANTLAR,
        is_anonymous=False,
    )


async def boshla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    for j in context.job_queue.get_jobs_by_name(str(chat_id)):
        j.schedule_removal()
    context.job_queue.run_daily(
        poll_yubor, VAQT, chat_id=chat_id, name=str(chat_id)
    )
    await update.message.reply_text("Tayyor! Har kuni 13:30 da so'rovnoma yuboraman. 🥤")


async def hozir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_chat.send_poll(
        question=SAVOL, options=VARIANTLAR, is_anonymous=False
    )


async def toxtat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for j in context.job_queue.get_jobs_by_name(str(update.effective_chat.id)):
        j.schedule_removal()
    await update.message.reply_text("To'xtatildi.")


app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("boshla", boshla))
app.add_handler(CommandHandler("hozir", hozir))
app.add_handler(CommandHandler("toxtat", toxtat))
app.run_polling()
