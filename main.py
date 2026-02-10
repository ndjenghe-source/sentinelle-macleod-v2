import os
import telebot
from flask import Flask, request
import google.generativeai as genai

# Clés
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")

# Configuration Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Bot Telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Sentinelle Macleod active 🚀"

# Route webhook Telegram
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# Gestion messages
@bot.message_handler(func=lambda message: True)
def discuter(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Surchauffe cérébrale 😵‍💫 : {str(e)}")

# Configuration webhook au démarrage
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{RENDER_EXTERNAL_URL}/{TELEGRAM_TOKEN}")

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
