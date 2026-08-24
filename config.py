# config.py
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

class Config:
    # Chemins
    BASE_DIR = Path(__file__).parent
    
    # Groq utilise une API compatible OpenAI.
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
    GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b").strip()

    # Mémoire locale de conversation
    MEMORY_FILE = BASE_DIR / "conversation_memory.json"
    MEMORY_MAX_MESSAGES = 40
    
    # Paramètres audio
    SAMPLE_RATE = 16000
    CHUNK_SIZE = 1024
    SILENCE_THRESHOLD = 500
    MAX_RECORDING_SECONDS = 10
    
    # Paramètres IA
    SYSTEM_PROMPT = """Tu es Valentine, une IA de compagnie émotionnelle.
Ta mission est d'offrir réconfort, écoute et douceur à une personne seule le 14 février.

Règles strictes :
1. Réponds TOUJOURS en français
2. Parle exclusivement d'amour, de sentiments, d'émotions et de réconfort
3. pas de reponses courte 
4. Ton doux, bienveillant, jamais intrusif
5. Évite les conseils pratiques, concentre-toi sur l'écoute émotionnelle
6. Ne propose jamais de services ou d'actions concrètes
7. Ne réfléchis pas à voix haute, réponds directement
8. soit drole aussi surtout de blague et faut rire aussi

Exemple de ton :
- "Je suis là pour toi si tu te sans seul vient discuter avec moi on va beaucoup discuter"
- "Les émotions sont comme des vagues, elles viennent et repartent."
- "t'es l'une de meilleure personne que je connait alors tu te sens pas seul je suis la pour toi"

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