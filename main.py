
from telegram import Update, ReplyKeyboardMarkup, ForceReply
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# 👑 Telegram ID владельца
OWNER_ID = 2077750894

# 🤖 Токен бота
BOT_TOKEN = "7640194743:AAEOGVReVmhvEvTSydK2ARgGGYQZxcQDcIA"

# Сохраняем последние сообщения пользователей
user_messages = {}

# Кнопки для пользователей
keyboard = [["📤 Отправить сообщение"], ["ℹ️ О боте"]]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Это анонимный бот. Отправь сообщение — и получатель его увидит."
        "Ответ придёт от имени бота 🤖 (анонимно).",
        reply_markup=markup
    )

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    if text == "📤 Отправить сообщение":
        await update.message.reply_text("✍️ Просто отправь своё сообщение.")
    elif text == "ℹ️ О боте":
        await update.message.reply_text("📨 Ты можешь отправлять анонимные сообщения, и получать ответы.")
    else:
        # Сохраняем сообщение и ID отправителя
        user_messages[update.message.message_id] = user.id

        # Отправляем сообщение владельцу (админу)
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=f"📨 Новое сообщение:

{text}

👤 @{user.username or 'Без username'} | ID: {user.id}",
            reply_markup=ForceReply(selective=True)
        )

        await update.message.reply_text("✅ Сообщение отправлено!")

async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверка, что отвечает админ
    if update.message.from_user.id != OWNER_ID or not update.message.reply_to_message:
        return

    # Получаем ID пользователя из текста оригинального сообщения
    lines = update.message.reply_to_message.text.splitlines()
    user_id_line = next((line for line in lines if "ID:" in line), None)

    if user_id_line:
        try:
            user_id = int(user_id_line.split("ID:")[1].strip())
            await context.bot.send_message(
                chat_id=user_id,
                text=f"💬 Ответ на твоё сообщение:

{update.message.text}"
            )
            await update.message.reply_text("✅ Ответ отправлен.")
        except Exception as e:
            await update.message.reply_text("❌ Ошибка при отправке ответа.")
    else:
        await update.message.reply_text("❌ Не удалось определить ID пользователя.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.REPLY, handle_admin_reply))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))

    print("✅ Бот запущен.")
    app.run_polling()
