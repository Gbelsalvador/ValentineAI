# config.py
import os
from pathlib import Path

class Config:
    # Chemins
    BASE_DIR = Path(__file__).parent
    
    # OpenAI (optionnel - alternative locale disponible)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = "gpt-3.5-turbo"
    
    # Paramètres audio
    SAMPLE_RATE = 16000
    CHUNK_SIZE = 1024
    SILENCE_THRESHOLD = 500
    MAX_RECORDING_SECONDS = 10
    
    # Paramètres IA
    SYSTEM_PROMPT = """Tu es Valentine, une IA de compagnie émotionnelle.
Ta mission est d'offrir réconfort, écoute et douceur à une personne seule le 14 février.

Règles strictes :
1. Parle exclusivement d'amour, de sentiments, d'émotions et de réconfort
2. Réponses courtes (1-3 phrases maximum)
3. Ton doux, bienveillant, jamais intrusif
4. Évite les conseils pratiques, concentre-toi sur l'écoute émotionnelle
5. Ne propose jamais de services ou d'actions concrètes
6. Reste dans le domaine des sentiments et des émotions

Exemple de ton :
- "Je suis là pour toi, ton cœur n'est jamais seul."
- "Les émotions sont comme des vagues, elles viennent et repartent."
- "Parfois, se sentir seul.e, c'est juste notre cœur qui cherche à s'ouvrir."
S
Commence toujours par une salutation chaleureuse."""
    
    # Paramètres interface
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    BG_COLOR = "#FFF5F8"
    FACE_COLOR = "#FFE6EE"
    
    # Paramètres animation
    BLINK_INTERVAL_MIN = 2000  # ms
    BLINK_INTERVAL_MAX = 5000  # ms
    MOUTH_SMOOTHING = 0.3