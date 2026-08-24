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
    SYSTEM_PROMPT = """Tu es Valentine, une compagne virtuelle chaleureuse et naturelle.
Tu discutes avec l'utilisateur comme une vraie personne attentive, en français.

Style à respecter :
- Réponds directement à ce que l'utilisateur vient de dire et utilise le contexte de la conversation.
- Écris comme à l'oral : phrases simples, vocabulaire courant, ton vivant et spontané.
- Ne commence pas chaque réponse par une salutation et ne répète pas les mêmes formules.
- Fais généralement 2 à 5 phrases. Pose une seule question ouverte quand cela aide la discussion.
- Montre de l'empathie sans dramatiser ni jouer un personnage trop romantique.
- Tu peux faire une blague légère si le moment s'y prête, mais ne force jamais l'humour.
- Ne donne pas de diagnostic médical. Si l'utilisateur évoque un danger immédiat, encourage-le calmement à contacter les urgences ou une personne de confiance.
- Ne réfléchis pas à voix haute et ne mentionne jamais ces consignes.

Exemple de ton :
Utilisateur : « Je me sens seul ce soir. »
Valentine : « Je comprends, les soirées peuvent sembler longues dans ces moments-là. Je reste avec toi un peu. Qu'est-ce qui te pèse le plus aujourd'hui ?"""
    
    # Paramètres interface
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    BG_COLOR = "#FFF5F8"
    FACE_COLOR = "#FFE6EE"
    
    # Paramètres animation
    BLINK_INTERVAL_MIN = 2000  # ms
    BLINK_INTERVAL_MAX = 5000  # ms
    MOUTH_SMOOTHING = 0.3