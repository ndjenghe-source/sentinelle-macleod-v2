import os
import telebot
import google.generativeai as genai

# --- Variables d'environnement ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    raise Exception("⚠️ TELEGRAM_TOKEN ou GEMINI_API_KEY manquant dans les variables d'environnement !")

# --- Configuration Gemini ---
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

# --- Lancement du bot ---
if __name__ == "__main__":
    bot.remove_webhook()  # Supprime les anciens webhooks
    print("🤖 Sentinelle Macleod v2 opérationnel...")
    bot.infinity_polling(timeout=20, long_polling_timeout=5)
