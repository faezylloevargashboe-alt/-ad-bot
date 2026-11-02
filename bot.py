import os
import re
import asyncio
from flask import Flask
import threading
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# Слова для удаления рекламы
AD_WORDS = ["https://", "http://", "t.me/", "@", "купить", "продам", "скидка", "заработок", "переходи", "подпишись"]

async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    text = update.message.text.lower()
    for word in AD_WORDS:
        if word in text:
            try:
                await update.message.delete()
                return
            except:
                return

# Веб-сервер чтобы Render не спал
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message))
    application.run_polling()

if __name__ == '__main__':
    main()
