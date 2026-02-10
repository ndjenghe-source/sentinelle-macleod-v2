import os
from google import genai

# Variables d'environnement
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    raise Exception("⚠️ TELEGRAM_TOKEN ou GEMINI_API_KEY manquant !")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.TextModel(model="gemini-1.5-turbo")  # exemple
