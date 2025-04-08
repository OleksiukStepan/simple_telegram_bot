import os
from datetime import datetime

from dotenv import load_dotenv

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton, ReplyKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    CallbackQueryHandler,
    filters,
    ConversationHandler,
)

load_dotenv()


ASK_NAME, ASK_AGE = range(2)

menu_keyboard = [
    [KeyboardButton("📷 Надіслати фото")],
    [KeyboardButton("📎 Надіслати документ")],
    [KeyboardButton("🌍 Надіслати локацію")],
    [KeyboardButton("❌ Вийти")]
]

reply_markup = ReplyKeyboardMarkup(
    keyboard=menu_keyboard,
    resize_keyboard=True,
    one_time_keyboard=False
)

async def start_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Вибери дію з меню нижче 👇",
        reply_markup=reply_markup
    )


async def handle_menu_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📷 Надіслати фото":
        context.user_data["next_action"] = "photo"
        await update.message.reply_text("Надішли, будь ласка, фото 📷")
    elif text == "📎 Надіслати документ":
        context.user_data["next_action"] = "doc"
        await update.message.reply_text("Надішли документ 📎")
    elif text == "🌍 Надіслати локацію":
        context.user_data["next_action"] = "location"
        await update.message.reply_text("Поділись локацією 🌍")
    elif text == "❌ Вийти":
        await update.message.reply_text("Меню приховано. Напиши /start, щоб повернутись.", reply_markup=None)
    else:
        await update.message.reply_text("Я не розпізнав дію 🤖")


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


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("next_action") == "photo":
        photo = update.message.photo[-1]  # last photo in list
        file = await photo.get_file()
        filename = datetime.now().strftime("photo_%Y%m%d_%H%M%S.jpg")

        save_dir = "media"
        os.makedirs(save_dir, exist_ok=True)

        save_path = os.path.join(save_dir, filename)
        await file.download_to_drive(save_path)
        await update.message.reply_text("Фото збережено!")
        await update.message.reply_text("📸 Дякую за фото!")
        context.user_data["next_action"] = None
    else:
        await update.message.reply_text("Я не чекав фото 🤔")



async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("next_action") == "doc":
        doc = update.message.document
        file = await doc.get_file()
        original_name = doc.file_name or "unnamed"
        name, ext = os.path.splitext(original_name)
        name = name.replace(" ", "_")
        ext = ext.lstrip(".")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.{ext}"

        save_dir = "docs"
        os.makedirs(save_dir, exist_ok=True)

        save_path = os.path.join(save_dir, filename)
        await file.download_to_drive(save_path)
        await update.message.reply_text("📎 Отримав документ!")
        await update.message.reply_text(f"Документ збережено як {filename}!")
        context.user_data["next_action"] = None
    else:
        await update.message.reply_text("Я не чекав документ 🤔")


async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("next_action") == "location":
        location = update.message.location
        await update.message.reply_text(f"🌍 Твоя локація:\nШирота: {location.latitude}\nДовгота: {location.longitude}")
        context.user_data["next_action"] = None
    else:
        await update.message.reply_text("Я не чекав фото 🤔")


async def say_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if args:
        text = " ".join(args)
        return await update.message.reply_text(f"Ти сказав: {text}")
    else:
        return await update.message.reply_text(
            "❗️Напиши щось після /say. Наприклад: /say Привіт"
        )


async def tf_upper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if args:
        text = " ".join(args)
        return await update.message.reply_text(text.upper())
    else:
        return await update.message.reply_text(
            "❗️Напиши щось після /tf. Наприклад: /tf привіт"
        )


async def start_with_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("ℹ️ Про бота", callback_data="about")],
        [InlineKeyboardButton("❓️ Допомога", callback_data="help")],
        [InlineKeyboardButton("📤 Ехо", callback_data="echo")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🔘 Обери дію:", reply_markup=reply_markup)


async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "about":
        await query.edit_message_text("🤖 Це бот Степана для навчання.")
    elif data == "help":
        await query.edit_message_text("❓ Просто натискай кнопки або пиши мені.")
    elif data == "echo":
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
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # commands
    app.add_handler(conv_handler)

    # app.add_handler(CommandHandler("start", echo))
    app.add_handler(CommandHandler("start", start_menu))
    app.add_handler(CommandHandler("say", say_command))
    app.add_handler(CommandHandler("tf", tf_upper))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("menu", start_with_buttons))

    app.add_handler(CallbackQueryHandler(handle_button_click))

    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_choice))

    app.run_polling()


if __name__ == "__main__":
    main()
