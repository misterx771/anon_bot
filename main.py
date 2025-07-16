from telegram import Update, ForceReply
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "твой_бот_токен"
ADMIN_ID = 2077750894  # твой Telegram ID

user_reply_map = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Это анонимный бот.\n✉️ Просто отправь сообщение — оно будет передано."
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    if user.id == ADMIN_ID and update.message.reply_to_message:
        original_message = update.message.reply_to_message.text
        for uid, uname in user_reply_map.items():
            if uname in original_message:
                await context.bot.send_message(chat_id=uid, text=text)
                await update.message.reply_text("✅ Ответ отправлен.")
                return
        await update.message.reply_text("⚠️ Не удалось определить получателя.")
        return

    if user.id != ADMIN_ID:
        username_info = f"@{user.username}" if user.username else "(нет username)"
        msg = f"✉️ Новое сообщение:\n\n{text}\n\n👤 {username_info}"
        user_reply_map[user.id] = username_info
        await context.bot.send_message(chat_id=ADMIN_ID, text=msg, reply_markup=ForceReply(selective=True))
        await update.message.reply_text("✅ Сообщение отправлено.")

async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("🤖 Бот запущен. Ожидаем сообщения...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio, nest_asyncio
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()

