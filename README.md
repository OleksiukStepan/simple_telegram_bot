# Simple Telegram Bot

This is a basic Telegram bot created for learning purposes using Python and the `python-telegram-bot` library (v20+).

## 🔧 Technologies Used

- Python 3
- [python-telegram-bot v20+](https://docs.python-telegram-bot.org/)
- python-dotenv

## ⚙️ Features

This bot provides a simple interface with a reply keyboard and supports several user interactions:

### ✅ Available Commands and Features

- **/start**  
  Sends a greeting message and displays a reply keyboard with options:
    - 📷 Send Photo
    - 📎 Send Document
    - 🌍 Send Location
    - ❌ Exit

- **📷 Send Photo**  
  Prompts the user to send a photo. When a photo is received, it is saved locally to the `photos/` directory.

- **📎 Send Document**  
  Prompts the user to send a document. When a document is received, it is saved locally to the `docs/` directory.

- **🌍 Send Location**  
  Asks the user to share their location. Upon receiving it, the bot responds with latitude and longitude.

- **❌ Exit**  
  Hides the keyboard and ends the interaction. The user can return by sending `/start`.

- **Input validation**  
  If a user sends a photo, document, or location without choosing the correct menu option first, the bot will notify them of an incorrect action.

- **Context tracking**  
  The bot remembers the selected action (e.g., expecting photo or document) and processes only the relevant data.

## 🗂 Project Structure

- `simple_bot.py` — main bot logic
- `.env` — environment file that stores your bot token

## 🚀 Getting Started

1. Install the dependencies:
```bash
pip install python-telegram-bot python-dotenv
```

2. Create a `.env` file with your bot token:
```
TOKEN=your_telegram_bot_token
```

3. Run the bot:
```bash
python simple_bot.py
```

## 📁 File Storage

- All received photos are saved to the `photos/` folder.
- All received documents are saved to the `docs/` folder.

## 👨‍💻 Author

This bot was developed by Stepan Oleksiuk as part of a Telegram bot development learning process using Python.