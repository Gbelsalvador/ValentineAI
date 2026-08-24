# brain.py - Cerveau conversationnel avec Groq et GPT OSS
import random
import requests
import json
from datetime import datetime
from config import Config
from memory import ConversationMemory

class ValentineBrain:
    def __init__(self, memory_path=None):
        self.memory = ConversationMemory(
            memory_path or Config.MEMORY_FILE,
            Config.MEMORY_MAX_MESSAGES,
        )
        self.conversation_history = self.memory.messages
        self._init_responses_db()
        
        print(f"🧠 Configuration Brain:")
        print(f"   • Groq configuré: {bool(Config.GROQ_API_KEY)}")
        print(f"   • Modèle: {Config.GROQ_MODEL}")
        
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
                "Je comprends, les moments de solitude peuvent vraiment peser. Je reste avec toi un peu. Qu'est-ce qui te manque le plus aujourd'hui ?",
                "Ça arrive d'avoir besoin de présence. On peut parler tranquillement, sans faire semblant que tout va bien. Tu veux me raconter ta journée ?",
                "Je suis là. On peut parler de ce que tu ressens, ou penser à quelque chose de plus léger si tu préfères."
            ],
            "amour": [
                "L'amour peut être beau, mais aussi un peu compliqué. Qu'est-ce qui te fait penser à ça en ce moment ?",
                "On sent que cette personne compte pour toi. Tu as envie de me dire ce qui s'est passé ?",
                "Les histoires de cœur ne sont jamais très simples, sinon on s'ennuierait vite. Tu le vis plutôt bien ou ça te travaille ?"
            ],
            "tristesse": [
                "Je suis désolée que tu traverses ça. Tu n'as pas besoin de minimiser ce que tu ressens avec moi. Qu'est-ce qui t'a rendu triste ?",
                "Je t'écoute, vraiment. Même si tu n'arrives pas à tout expliquer, tu peux commencer par me dire ce qui fait le plus mal.",
                "C'est lourd à porter, je comprends. On peut prendre les choses doucement, une phrase à la fois."
            ],
            "espoir": [
                "J'aime bien entendre cette petite part d'espoir. Qu'est-ce qui te donne envie d'y croire aujourd'hui ?",
                "Même un petit mieux compte. Tu imagines quoi pour la suite ?",
                "Ça fait du bien de garder une fenêtre ouverte. On peut réfléchir ensemble à ce qui te redonnerait un peu d'élan."
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
        
        response = None
        if Config.GROQ_API_KEY:
            try:
                response = self._get_groq_response(user_input)
                if response and len(response.strip()) > 10:
                    print(f"Réponse Groq: '{response}'")
                else:
                    print("Réponse Groq trop courte, fallback local")
                    response = None
            except Exception as e:
                print(f"Erreur Groq: {e}")
        
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
    
    def _get_groq_response(self, user_input):
        """Utilise le modèle GPT OSS via l'API Groq."""
        try:
            headers = {
                "Authorization": f"Bearer {Config.GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": Config.GROQ_MODEL,
                "messages": self._build_messages(user_input),
                "max_tokens": 150,
                "temperature": 0.7,
                "top_p": 0.9,
                "frequency_penalty": 0.3,
                "presence_penalty": 0.3
            }
            
            print("🌐 Envoi requête à Groq...")
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=15
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
            raise Exception("Timeout: Groq ne répond pas")
        except requests.exceptions.ConnectionError:
            raise Exception("Erreur de connexion")
        except Exception as e:
            print(f"❌ Erreur détaillée Groq: {e}")
            raise