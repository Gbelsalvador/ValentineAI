import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "http://localhost",
    "X-Title": "ValentineAI",
    "Content-Type": "application/json"
}

data = {
    "model": OPENROUTER_MODEL,
    "messages": [
        {"role": "system", "content": "Tu es une IA gentille."},
        {"role": "user", "content": "Bonjour, comment ça va?"}
    ],
    "max_tokens": 50,
    "temperature": 0.7
}

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers=headers,
    json=data,
    timeout=10
)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print(f"Réponse: {result['choices'][0]['message']['content']}")
else:
    print(f"Erreur: {response.text}")