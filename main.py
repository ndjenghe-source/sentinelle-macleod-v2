import os
from google import genai  # ✔ nouveau package

# Récupérer les clés depuis les variables d'environnement
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Vérifier que les clés existent
if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    raise Exception("⚠️ TELEGRAM_TOKEN ou GEMINI_API_KEY manquant dans les variables d'environnement !")

# Configurer Google GenAI
genai.configure(api_key=GEMINI_API_KEY)

# Ici tu peux mettre ton code Telegram / OpenClaw
# Exemple minimal :
print("✅ Tout est configuré, votre agent peut démarrer !")
