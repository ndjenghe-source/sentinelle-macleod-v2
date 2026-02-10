import os
import telebot
from flask import Flask, request
import google.generativeai as genai

# --- Variables d'environnement ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")

# --- Configuration Gemini ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- Bot Telegram ---
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# --- Flask App ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Sentinelle Macleod active 🚀"

# --- Webhook route ---
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    try:
        bot.process_new_updates([update])
    except Exception as e:
        print(f"Erreur dans webhook: {e}")
    return "OK", 200

# --- Gestion des messages ---
@bot.message_handler(func=lambda message: True)
def discuter(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Surchauffe cérébrale 😵‍💫 : {str(e)}")

# --- Configuration webhook au démarrage ---
if __name__ == "__main__":
    # Supprime les webhooks existants
    bot.remove_webhook()
    # Configure le webhook vers Render
    bot.set_webhook(url=f"{RENDER_EXTERNAL_URL}/{TELEGRAM_TOKEN}")

    # Lance Flask (Gunicorn prendra le relais en production)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
