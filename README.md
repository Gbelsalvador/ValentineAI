# ValentineAI

## Intelligence Artificielle de Compagnie Émotionnelle

ValentineAI est une application Python interactive conçue pour offrir réconfort et compagnie émotionnelle. Dotée d'une interface graphique immersive avec avatar animé, elle combine synthèse vocale et reconnaissance vocale pour créer une expérience conversationnelle bienveillante.

---

## 🎯 Fonctionnalités

### 🧠 Intelligence Émotionnelle
- **Réponses contextuelles** adaptées aux émotions exprimées
- **Base de connaissances locale** avec réponses pré-définies
- **Prompt système spécialisé** en réconfort et soutien émotionnel
- **Mémoire persistante locale** pour conserver le contexte entre les tours et les redémarrages

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
git clone https://github.com/gbelsalvador/ValentineAI.git
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
├── memory.py            # Persistance locale de l'historique
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
- **Gestion de conversation** avec historique persistant
- **Support Groq avec GPT OSS** (optionnel)
- **Fallback local** avec base de réponses pré-définies

#### 💾 Mémoire de conversation
L'historique est enregistré dans `conversation_memory.json` à côté de l'application.
Il est limité aux 40 derniers messages et est envoyé à Groq à chaque nouveau tour
pour que Valentine puisse garder le fil de la discussion après un redémarrage.
Ce fichier reste local et ne doit pas être partagé s'il contient des informations privées.

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
GROQ_API_KEY=votre_clé_groq_ici
GROQ_MODEL=openai/gpt-oss-120b
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
- [Discussions GitHub](https://github.com/gbelsalvador/ValentineAI/discussions)
- [Signalement de bugs](https://github.com/gbelsalvador/ValentineAI/issues)

### Contact
Pour les questions techniques :  
📧 gbelsalvador6gmail.com

Pour les questions éthiques :  
📧 gbelsalvador6gmail.comS

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