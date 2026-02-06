# brain.py
import random
import json
from datetime import datetime
from config import Config

class ValentineBrain:
    def __init__(self, use_openai=False):
        self.use_openai = use_openai
        self.conversation_history = []
        self._init_responses_db()
        
        # Salutations basées sur l'heure
        self.greetings = [
            "Bonjour, je suis Valentine. Ton cœur a-t-il des choses à partager aujourd'hui?",
            "Je suis là pour toi. Comment te sens-tu en ce jour spécial?",
            "L'amour n'a pas besoin d'être à deux pour exister. Parle-moi de ton cœur.",
            "Chaque émotion mérite d'être écoutée. Je t'écoute."
        ]
    
    def _init_responses_db(self):
        """Base de données de réponses locales pour fallback"""
        self.local_responses = {
            "solitude": [
                "La solitude est parfois le jardin secret où notre cœur apprend à se connaître.",
                "Être seul.e aujourd'hui ne signifie pas être sans amour. Ton propre cœur t'aime.",
                "Je suis avec toi dans ce moment. Chaque sentiment a sa place."
            ],
            "amour": [
                "L'amour est comme une rivière, il trouve toujours son chemin.",
                "Aimer, c'est parfois laisser son cœur respirer librement.",
                "Ton cœur a une capacité infinie d'amour, même quand il se sent vide."
            ],
            "tristesse": [
                "Les larmes nettoient l'âme pour laisser place à de nouvelles émotions.",
                "Il est normal de se sentir triste. C'est ton cœur qui parle.",
                "Je t'écoute sans jugement. Tes sentiments sont valides."
            ],
            "espoir": [
                "Même la plus petite étincelle d'espoir peut illuminer un cœur.",
                "L'amour revient toujours sous une forme ou une autre.",
                "Ton cœur a une résilience que tu ne soupçonnes même pas."
            ]
        }
    
    def get_greeting(self):
        """Retourne une salutation appropriée"""
        hour = datetime.now().hour
        if hour < 12:
            return random.choice(self.greetings)
        elif hour < 18:
            return "Bonjour, comment va ton cœur cet après-midi?"
        else:
            return "Bonsoir, la nuit est souvent le moment où le cœur parle le plus. Je t'écoute."
    
    def process_input(self, user_input):
        """Traite l'entrée utilisateur et génère une réponse"""
        if not user_input or len(user_input.strip()) < 2:
            return "Je t'écoute... Parle-moi de ce que tu ressens."
        
        # Ajoute à l'historique
        self.conversation_history.append(f"Utilisateur: {user_input}")
        
        # Limite l'historique
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
        
        # Essaie OpenAI d'abord si configuré
        if self.use_openai:
            try:
                return self._get_openai_response(user_input)
            except Exception:
                pass  # Fallback sur les réponses locales
        
        # Réponse locale basée sur les mots-clés
        return self._get_local_response(user_input)
    
    def _get_local_response(self, text):
        """Génère une réponse basée sur des mots-clés"""
        text_lower = text.lower()
        
        # Détection de mots-clés
        keywords = {
            "seul": "solitude",
            "solitude": "solitude",
            "seule": "solitude",
            "aimer": "amour",
            "amour": "amour",
            "amoureux": "amour",
            "triste": "tristesse",
            "pleure": "tristesse",
            "tristesse": "tristesse",
            "espoir": "espoir",
            "espérer": "espoir",
            "future": "espoir",
            "demain": "espoir"
        }
        
        # Trouve la catégorie principale
        category = None
        for word, cat in keywords.items():
            if word in text_lower:
                category = cat
                break
        
        # Si aucune catégorie trouvée, réponse générale
        if not category:
            categories = list(self.local_responses.keys())
            category = random.choice(categories)
        
        return random.choice(self.local_responses[category])
    
    def _get_openai_response(self, user_input):
        """Utilise l'API OpenAI pour générer une réponse"""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=Config.OPENAI_API_KEY)
            
            messages = [
                {"role": "system", "content": Config.SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
            
            response = client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=messages,
                max_tokens=100,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except ImportError:
            return self._get_local_response(user_input)