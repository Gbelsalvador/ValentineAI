# ValentineAI

## Intelligence Artificielle de Compagnie Émotionnelle

ValentineAI est une application Python interactive conçue pour offrir réconfort et compagnie émotionnelle. Dotée d'une interface graphique immersive avec avatar animé, elle combine synthèse vocale et reconnaissance vocale pour créer une expérience conversationnelle bienveillante.

---

## 🎯 Fonctionnalités

### 🧠 Intelligence Émotionnelle
- **Réponses contextuelles** adaptées aux émotions exprimées
- **Base de connaissances locale** avec réponses pré-définies
- **Prompt système spécialisé** en réconfort et soutien émotionnel
- **Historique de conversation** pour des échanges cohérents

### 🎤 Interface Vocale Bidirectionnelle
- **Reconnaissance vocale** via microphone
- **Synthèse vocale** avec voix douce et rassurante
- **Support français** natif
- **Animation labiale** synchronisée avec la parole

### 👀 Interface Graphique Immersive
- **Avatar 2D animé** avec expressions faciales
- **Yeux qui clignent** automatiquement
- **Bouche animée** en temps réel
- **Cœur pulsant** pour l'ambiance émotionnelle
- **Interface épurée** aux couleurs apaisantes

### 🔄 Flux d'Interaction
1. Lancement de l'application
2. Salutation vocale initiale
3. Capture audio utilisateur
4. Traitement et génération de réponse
5. Synthèse vocale avec animation
6. Retour en mode écoute

---

## 📋 Prérequis Système

### 🖥️ Configuration
- **Système d'exploitation** : Windows 10/11 (64-bit)
- **Python** : Version 3.12 recommandée
  - ⚠️ La version 3.13 présente des incompatibilités avec `SpeechRecognition`
- **Espace disque** : 100 MB minimum
- **Microphone** : Intégré ou externe (recommandé)

### 📦 Outils de Développement
- **Microsoft C++ Build Tools** (pour la compilation de PyAudio)
- **Git** (pour le clonage du dépôt)

---

## 🚀 Installation

### Méthode 1 : Installation Standard (Recommandée)

```powershell
# Cloner le dépôt
git clone https://github.com/votre-username/ValentineAI.git
cd ValentineAI

# Installer les dépendances avec Python 3.12
py -3.12 -m pip install -r requirements.txt
```

### Méthode 2 : Installation avec Environnement Virtuel

```powershell
# Créer et activer l'environnement virtuel
py -3.12 -m venv venv
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### 🔧 Résolution des Problèmes d'Installation

#### Problème avec PyAudio
```powershell
# Solution 1 : Installer une version spécifique
py -3.12 -m pip install PyAudio==0.2.14

# Solution 2 : Utiliser pipwin (recommandé pour Windows)
py -3.12 -m pip install pipwin
pipwin install pyaudio
```

#### Problème avec SpeechRecognition (Python 3.13)
```powershell
# ⚠️ IMPORTANT : Utiliser Python 3.12
# SpeechRecognition n'est pas compatible avec Python 3.13+
# En raison de la suppression du module aifc de la bibliothèque standard
```

#### Problème avec setuptools
```powershell
# Mettre à jour setuptools si nécessaire
py -3.12 -m pip install -U setuptools wheel
```

---

## 🎮 Utilisation

### Lancement de l'Application

```powershell
# Depuis le dossier du projet
py -3.12 main.py
```

### Commandes et Contrôles

| Touche | Fonction |
|--------|----------|
| **ESC** | Quitter l'application |
| **ESPACE** | Simuler une entrée vocale (mode test) |
| **ENTRÉE** | Envoyer un message texte |
| **Clic souris** | Interagir avec l'interface |

### Flux Utilisateur Typique
1. **Démarrage** : Valentine salue l'utilisateur vocalement
2. **Interaction** : L'utilisateur parle dans le microphone
3. **Traitement** : Transcription et génération de réponse
4. **Réponse** : Valentine répond vocalement avec animation
5. **Boucle** : Retour à l'étape 2

---

## 🏗️ Architecture du Projet

### Structure des Fichiers

```
ValentineAI/
├── main.py              # Point d'entrée principal et boucle d'application
├── config.py            # Configuration globale et constantes
│
├── audio_input.py       # Capture audio et reconnaissance vocale
├── audio_output.py      # Synthèse vocale et animation labiale
├── brain.py             # Logique IA et gestion des réponses
├── avatar.py            # Rendu et animation du visage
│
├── requirements.txt     # Dépendances Python
├── .env.example         # Variables d'environnement (API keys)
└── README.md           # Documentation
```

### Modules Principaux

#### 🎭 `avatar.py`
- **Rendu 2D** du visage avec Pygame
- **Animations** : clignotement des yeux, mouvement de bouche
- **Expressions faciales** selon le contexte émotionnel
- **Effets visuels** : cœur pulsant, particules décoratives

#### 🧠 `brain.py`
- **Moteur de réponse** émotionnelle
- **Gestion de conversation** avec historique
- **Support OpenAI API** (optionnel)
- **Fallback local** avec base de réponses pré-définies

#### 🎤 `audio_input.py`
- **Capture microphone** avec PyAudio
- **Reconnaissance vocale** via Google Speech Recognition
- **Gestion du bruit** ambiant
- **Timeout intelligent** pour la détection de parole

#### 🔊 `audio_output.py`
- **Synthèse vocale** avec pyttsx3
- **Configuration de voix** française
- **Animation labiale** basée sur le volume audio
- **Gestion asynchrone** de la parole

---

## ⚙️ Configuration

### Fichier `config.py`

```python
# Paramètres Audio
SAMPLE_RATE = 16000          # Fréquence d'échantillonnage
CHUNK_SIZE = 1024            # Taille des buffers audio
MAX_RECORDING_SECONDS = 10   # Durée maximale d'enregistrement

# Paramètres Interface
WINDOW_WIDTH = 900           # Largeur de la fenêtre
WINDOW_HEIGHT = 700          # Hauteur de la fenêtre
BG_COLOR = "#FFF5F8"         # Couleur de fond (rose clair)

# Paramètres Animation
BLINK_INTERVAL_MIN = 2000    # Intervalle minimum de clignotement (ms)
BLINK_INTERVAL_MAX = 5000    # Intervalle maximum de clignotement (ms)

# Paramètres IA
SYSTEM_PROMPT = """Tu es Valentine, une IA de compagnie émotionnelle..."""
```

### Variables d'Environnement (Optionnel)

```env
# Fichier .env
OPENAI_API_KEY=votre_clé_api_ici
```

---

## 🛠️ Développement

### Ajouter de Nouvelles Réponses

Modifiez `brain.py` pour étendre la base de connaissances :

```python
self.responses["nouvelle_catégorie"] = [
    "Réponse émotionnelle 1",
    "Réponse émotionnelle 2",
    "Réponse émotionnelle 3"
]
```

### Personnaliser l'Apparence

Modifiez `config.py` pour changer les couleurs et dimensions :

```python
# Couleurs personnalisées
BG_COLOR = "#F0F8FF"          # Bleu très clair
FACE_COLOR = "#E6F3FF"        # Bleu pastel
ACCENT_COLOR = "#4A90E2"      # Bleu vif
```

### Intégrer d'autres Services IA

Ajoutez de nouveaux fournisseurs dans `brain.py` :

```python
def get_openai_response(self, user_input):
    # Implémentation OpenAI
    pass

def get_local_llm_response(self, user_input):
    # Implémentation locale (Ollama, etc.)
    pass
```

---

## 🐛 Dépannage

### Problèmes Courants

#### ❌ "ModuleNotFoundError: No module named 'aifc'"
**Cause** : Utilisation de Python 3.13+ avec SpeechRecognition  
**Solution** : Utiliser Python 3.12

```powershell
# Vérifier la version de Python
python --version

# Si version 3.13+, installer Python 3.12 depuis python.org
# Puis utiliser :
py -3.12 main.py
```

#### ❌ Échec d'installation de PyAudio
**Cause** : Compilateurs C++ manquants  
**Solution** : Installer Microsoft C++ Build Tools ou utiliser pipwin

```powershell
# Méthode recommandée pour Windows
pip install pipwin
pipwin install pyaudio
```

#### ❌ Microphone non détecté
**Solution** :
1. Vérifier les permissions microphone dans les paramètres Windows
2. Tester avec une autre application (ex: Dictée Windows)
3. Vérifier la connexion du microphone

#### ❌ Pas de son en sortie
**Solution** :
1. Vérifier le volume système
2. Tester la synthèse vocale avec un script simple :

```python
import pyttsx3
engine = pyttsx3.init()
engine.say("Test audio")
engine.runAndWait()
```

### Journaux et Debug

Activez les logs détaillés dans `config.py` :

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📊 Tests

### Tests Unitaires

```powershell
# Exécuter les tests de base
python -m pytest tests/ -v
```

### Tests d'Intégration

1. **Test audio** : Vérifier capture et synthèse
2. **Test interface** : Vérifier animations et réponses
3. **Test performance** : Mesurer temps de réponse

### Scripts de Test

```python
# test_audio.py
import speech_recognition as sr
import pyttsx3

# Test reconnaissance
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Parlez...")
    audio = r.listen(source)
    print(f"Transcrit: {r.recognize_google(audio, language='fr-FR')}")

# Test synthèse
engine = pyttsx3.init()
engine.say("Test de synthèse vocale")
engine.runAndWait()
```

---

## 🔄 Maintenance

### Mise à Jour des Dépendances

```powershell
# Mettre à jour pip
py -3.12 -m pip install --upgrade pip

# Mettre à jour les packages
pip list --outdated
pip install --upgrade package_name
```

### Sauvegarde des Configurations

```powershell
# Exporter les packages installés
pip freeze > requirements_backup.txt

# Sauvegarder les fichiers de configuration
copy config.py config_backup.py
```

---

## 🎨 Personnalisation Avancée

### Thèmes Visuels

Créez de nouveaux thèmes dans `config.py` :

```python
THEMES = {
    "romantique": {
        "bg": "#FFF5F8",
        "face": "#FFE6EE",
        "accent": "#CD6889"
    },
    "apaisant": {
        "bg": "#F0F8FF",
        "face": "#E6F3FF", 
        "accent": "#4A90E2"
    },
    "nature": {
        "bg": "#F0FFF0",
        "face": "#E8F5E8",
        "accent": "#228B22"
    }
}
```

### Voix Personnalisées

```python
# Dans audio_output.py
def configure_custom_voice(self):
    voices = self.engine.getProperty('voices')
    
    # Sélectionner une voix spécifique
    for voice in voices:
        if 'french' in voice.name.lower():
            self.engine.setProperty('voice', voice.id)
            break
    
    # Ajuster les paramètres
    self.engine.setProperty('rate', 140)    # Plus lent
    self.engine.setProperty('pitch', 110)   # Plus aigu
    self.engine.setProperty('volume', 0.85) # Volume réduit
```

### Animations Supplémentaires

Ajoutez de nouvelles animations dans `avatar.py` :

```python
def add_special_effect(self, effect_name):
    if effect_name == "blush":
        # Ajouter des joues rosées
        pygame.draw.circle(self.screen, "#FFB6C1", 
                          (self.face_x - 40, self.face_y + 20), 15)
        pygame.draw.circle(self.screen, "#FFB6C1",
                          (self.face_x + 40, self.face_y + 20), 15)
```

---

## 📈 Améliorations Futures

### Roadmap

1. **Phase 1** (Actuelle)
   - Interface de base fonctionnelle
   - Reconnaissance vocale stable
   - Synthèse vocale en français

2. **Phase 2** (Planifiée)
   - Support multi-langues
   - Expressions faciales avancées
   - Integration avec calendrier (dates spéciales)

3. **Phase 3** (Future)
   - Apprentissage des préférences utilisateur
   - Suggestions d'activités apaisantes
   - Mode hors ligne amélioré

### Contributions

Les contributions sont bienvenues ! Voici comment aider :

1. **Signaler un bug** : Ouvrir une issue avec les étapes de reproduction
2. **Proposer une fonctionnalité** : Décrire le cas d'utilisation
3. **Soumettre un correctif** : Pull request avec tests
4. **Améliorer la documentation** : Corrections ou traductions

---

## ⚖️ Considérations Éthiques

### Utilisation Responsable

ValentineAI est conçu comme un **outil de réconfort temporaire**, pas comme un substitut à :
- Les relations humaines authentiques
- L'aide psychologique professionnelle
- Les interactions sociales réelles

### Mesures de Protection

1. **Limites temporelles** : Sessions limitées à 30 minutes
2. **Ressources externes** : Liens vers aide professionnelle
3. **Transparence** : Clarification du statut d'IA
4. **Confidentialité** : Données locales uniquement

### Recommandations d'Usage

- Utiliser comme complément, non comme remplacement
- Consulter un professionnel en cas de détresse
- Maintenir des interactions humaines régulières
- Être conscient des limites de l'IA

---

## 📞 Support

### Documentation
- [Guide d'installation détaillé](docs/INSTALLATION.md)
- [Guide de développement](docs/DEVELOPMENT.md)
- [FAQ](docs/FAQ.md)

### Communauté
- [Discussions GitHub](https://github.com/votre-username/ValentineAI/discussions)
- [Signalement de bugs](https://github.com/votre-username/ValentineAI/issues)

### Contact
Pour les questions techniques :  
📧 technique@valentineai.example.com

Pour les questions éthiques :  
📧 ethique@valentineai.example.com

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🙏 Remerciements

- **Pygame** pour le moteur graphique
- **SpeechRecognition** pour la transcription vocale
- **pyttsx3** pour la synthèse vocale
- **OpenAI** pour l'API GPT (optionnel)
- **Tous les contributeurs** qui améliorent ValentineAI

---

*ValentineAI - Parce que chaque cœur mérite d'être écouté* 💝