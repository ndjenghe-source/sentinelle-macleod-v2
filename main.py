import os
import telebot
from flask import Flask
import threading
import google.generativeai as genai
import time

# 1. Récupération des clés (configurées plus tard sur Render)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# 2. Configuration du cerveau Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')
# 3. Initialisation du Bot avec sécurité anti-conflit
bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False)

app = Flask(__name__)

@app.route('/')
def home():
    return "Sentinelle Macleod v2 : Système opérationnel et stabilisé. 🚀"

# 4. Fonction de discussion
@bot.message_handler(func=lambda message: True)
def discuter(message):
    try:
        # Envoie le message à Gemini
        response = model.generate_content(message.text)
        # Renvoie la réponse de l'IA sur Telegram
        bot.reply_to(message, response.text)
    except Exception as e:
        # Affiche l'erreur réelle pour nous aider à débugger si besoin
        bot.reply_to(message, f"Petite surchauffe de cerveau... Erreur : {str(e)}")

# 5. Lancement du Bot avec nettoyage automatique
def run_bot():
    # Cette ligne force Telegram à déconnecter les anciens "fantômes"
    bot.remove_webhook()
    time.sleep(1)
    print("La Sentinelle Milk écoute...")
    # On utilise infinity_polling pour que le bot redémarre tout seul en cas de micro-coupure
    bot.infinity_polling(timeout=20, long_polling_timeout=5)

# 6. Lancement du serveur Web (obligatoire pour Render)
def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # On lance le Web et le Bot en même temps
    threading.Thread(target=run_web).start()
    run_bot()
