# brain.py - Version corrigée pour  s'adpater avec OpenRouter 
import random
import requests
import json
from datetime import datetime
from config import Config
from memory import ConversationMemory

class ValentineBrain:
    def __init__(self, memory_path=None):
        # Vérifie la configuration OpenRouter
        self.use_openrouter = bool(Config.OPENROUTER_API_KEY.strip())
        self.memory = ConversationMemory(
            memory_path or Config.MEMORY_FILE,
            Config.MEMORY_MAX_MESSAGES,
        )
        self.conversation_history = self.memory.messages
        self._init_responses_db()
        
        print(f"🧠 Configuration Brain:")
        print(f"   • OpenRouter activé: {self.use_openrouter}")
        print(f"   • Modèle: {Config.OPENROUTER_MODEL}")
        
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
            greeting = random.choice(self.greetings)
        elif hour < 18:
            greeting = "Bonjour, comment va ton cœur cet après-midi?"
        else:
            greeting = "Bonsoir, la nuit est souvent le moment où le cœur parle le plus. Je t'écoute."

        self.memory.add_assistant_message(greeting)
        self.conversation_history = self.memory.messages
        return greeting
    
    def process_input(self, user_input):
        """Traite l'entrée utilisateur et génère une réponse"""
        if not user_input or len(user_input.strip()) < 2:
            return "Je t'écoute... Parle-moi de ce que tu ressens."
        
        print(f"🧠 Utilisateur dit: '{user_input}'")
        
        # Essaie OpenRouter d'abord si configuré
        response = None
        if self.use_openrouter:
            try:
                print("🔄 Tentative de réponse via OpenRouter...")
                response = self._get_openrouter_response(user_input)
                if response and len(response.strip()) > 10:
                    print(f"Réponse OpenRouter: '{response}'")
                else:
                    print("Réponse OpenRouter trop courte, fallback local")
                    response = None
            except Exception as e:
                print(f"Erreur OpenRouter: {e}")
        
        if response is None:
            print("Utilisation des réponses locales...")
            response = self._get_local_response(user_input)

        self.memory.add_exchange(user_input, response)
        self.conversation_history = self.memory.messages
        return response

    def clear_memory(self):
        """Efface l'historique local de conversation."""
        self.memory.clear()
        self.conversation_history = self.memory.messages

    def _build_messages(self, user_input):
        """Construit les messages dans l'ordre attendu par l'API."""
        return [
            {"role": "system", "content": Config.SYSTEM_PROMPT},
            *self.memory.snapshot(),
            {"role": "user", "content": user_input},
        ]
    
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
        
        response = random.choice(self.local_responses[category])
        print(f"📦 Réponse locale: '{response}'")
        return response
    
    def _get_openrouter_response(self, user_input):
        """Utilise l'API OpenRouter pour générer une réponse"""
        try:
            headers = {
                "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
                "HTTP-Referer": Config.OPENROUTER_SITE_URL or "http://localhost",
                "X-Title": Config.OPENROUTER_SITE_NAME or "ValentineAI",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": Config.OPENROUTER_MODEL,
                "messages": self._build_messages(user_input),
                "max_tokens": 150,
                "temperature": 0.7,
                "top_p": 0.9,
                "frequency_penalty": 0.3,
                "presence_penalty": 0.3
            }
            
            print(f"🌐 Envoi requête à OpenRouter...")
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=15  # Timeout plus long
            )
            
            print(f"📡 Statut HTTP: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"📦 Réponse brute: {result}")
                
                if "choices" in result and len(result["choices"]) > 0:
                    content = result["choices"][0]["message"]["content"].strip()
                    
                    # Nettoyage de la réponse
                    # Retire les réflexions internes comme "Alright, the user..."
                    if "Alright," in content or "The user" in content or "I should" in content:
                        # C'est une réflexion, on prend la partie après la dernière réflexion
                        lines = content.split('\n')
                        for line in reversed(lines):
                            if line.strip() and not line.startswith(("Alright", "The user", "I should", "Since")):
                                content = line.strip()
                                break
                    
                    return content
                else:
                    raise Exception("Pas de réponse dans les choix")
            else:
                error_msg = f"Erreur HTTP {response.status_code}"
                if response.text:
                    error_msg += f": {response.text}"
                raise Exception(error_msg)
                
        except requests.exceptions.Timeout:
            raise Exception("Timeout: OpenRouter ne répond pas")
        except requests.exceptions.ConnectionError:
            raise Exception("Erreur de connexion")
        except Exception as e:
            print(f"❌ Erreur détaillée OpenRouter: {e}")
            raise