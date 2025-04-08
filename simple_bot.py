import os

from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    CallbackQueryHandler,
    filters, ConversationHandler,
)

# Load environment variables from .env file
load_dotenv()


ASK_NAME, ASK_AGE = range(2)

# 1. Start – start conversation
async def start_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! What is your name?")
    return ASK_NAME

# 2. Step 1 – Get name
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Супер! А скільки тобі років?")
    return ASK_AGE

# 3. Step 2 – get age and give response
async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = context.user_data.get("name")
    age = update.message.text
    await update.message.reply_text(f"Привіт, {name}! Тобі {age} років.")
    return ConversationHandler.END

# 4. Canceling
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Діалог скасовано.")
    return ConversationHandler.END


async def say_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if args:
        text = " ".join(args)
        return await update.message.reply_text(f"Ти сказав: {text}")
    else:
        return await update.message.reply_text("❗️Напиши щось після /say. Наприклад: /say Привіт")


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

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("survey", start_conversation)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            ASK_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    # commands
    app.add_handler(conv_handler)

    app.add_handler(CommandHandler("start", echo))
    app.add_handler(CommandHandler("say", say_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("menu", start_with_buttons))

    app.add_handler(CallbackQueryHandler(handle_button_click))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.run_polling()


if __name__ == "__main__":
    main()
