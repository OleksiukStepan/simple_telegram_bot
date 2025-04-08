import os

from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    CallbackQueryHandler,
    filters,
)

# Load environment variables from .env file
load_dotenv()



async def start_with_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("ℹ️ Про бота", callback_data='about')],
        [InlineKeyboardButton("❓️ Допомога", callback_data='help')],
        [InlineKeyboardButton("📤 Ехо", callback_data='echo')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🔘 Обери дію:", reply_markup=reply_markup)


async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == 'about':
        await query.edit_message_text("🤖 Це бот Степана для навчання.")
    elif data == 'help':
        await query.edit_message_text("❓ Просто натискай кнопки або пиши мені.")
    elif data == 'echo':
        await query.edit_message_text("📤 Напиши щось, і я повторю його.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Я можу повторювати твої повідомлення!\n\n"
        "Команди:\n"
        "/start - почати\n"
        "/help - допомога\n"
        "/about - про бота"
    )


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Я простий Telegram-бот, створений Степаном для навчання.\n"
        "Пишу на Python з використанням бібліотеки python-telegram-bot!"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

def main():
    app = ApplicationBuilder().token(os.getenv("TOKEN")).build()

    app.add_handler(CommandHandler("start", echo))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("menu", start_with_buttons))

    app.add_handler(CallbackQueryHandler(handle_button_click))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.run_polling()


if __name__ == "__main__":
    main()
