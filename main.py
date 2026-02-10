import os
import telebot
import google.generativeai as genai

# --- Variables ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# --- Config Gemini ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- Bot Telegram ---
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# --- Gestion des messages ---
@bot.message_handler(func=lambda message: True)
def discuter(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Surchauffe cérébrale 😵‍💫 : {str(e)}")

# --- Lancer le bot ---
if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling(timeout=20, long_polling_timeout=5)
