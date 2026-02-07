# audio_output.py - Version simplifiée pour Windows
import pyttsx3
import pygame
import numpy as np
import threading
import time
import math
import random
from config import Config

class AudioOutput:
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.engine = self._init_tts_engine()
        self.is_speaking = False
        self.volume_callback = None
        self.speech_events = []
        
    def _init_tts_engine(self):
        """Initialise le moteur TTS avec une voix française douce"""
        try:
            engine = pyttsx3.init()
            
            # Configure une voix douce
            voices = engine.getProperty('voices')
            print(f"Voix disponibles: {[v.name for v in voices]}")
            
            french_voices = [v for v in voices if 'french' in v.name.lower() or 'france' in v.name.lower()]
            
            if french_voices:
                engine.setProperty('voice', french_voices[0].id)
                print(f"✅ Voix française sélectionnée: {french_voices[0].name}")
            else:
                # Essaye de trouver une voix féminine
                female_voices = [v for v in voices if 'female' in v.name.lower() 
                               or 'zira' in v.name.lower() 
                               or 'hazel' in v.name.lower()]
                if female_voices:
                    engine.setProperty('voice', female_voices[0].id)
                    print(f"✅ Voix féminine sélectionnée: {female_voices[0].name}")
                else:
                    print(f"⚠️  Utilisation de la voix par défaut: {voices[0].name}")
            
            # Paramètres doux
            engine.setProperty('rate', 160)  # Vitesse moyenne
            engine.setProperty('volume', 0.9)  # Volume
            
            # Connecte les événements pour suivre la parole
            engine.connect('started-word', self._on_speech_start)
            engine.connect('finished-utterance', self._on_speech_end)
            
            return engine
        except Exception as e:
            print(f"❌ Erreur initialisation TTS: {e}")
            return None
    
    def _on_speech_start(self, name, location, length):
        """Quand la parole commence"""
        self.speech_events.append(('start', time.time()))
    
    def _on_speech_end(self, name, completed):
        """Quand la parole se termine"""
        self.speech_events.append(('end', time.time()))
    
    def speak(self, text, callback=None):
        """Convertit le texte en parole et joue l'audio"""
        if self.is_speaking or not self.engine:
            print(f"⚠️  Déjà en train de parler ou moteur TTS non initialisé")
            return
        
        print(f"🎤 Début de la synthèse vocale: '{text[:50]}...'")
        self.is_speaking = True
        
        def speak_thread():
            try:
                # Génère des données de volume factices pour l'animation
                fake_volume_data = self._generate_volume_data(text)
                
                # Envoie les données de volume pour l'animation
                if self.volume_callback:
                    print(f"📊 Envoi des données d'animation: {len(fake_volume_data)} points")
                    self.volume_callback(fake_volume_data)
                
                # Parle le texte
                self.engine.say(text)
                self.engine.runAndWait()
                
                print(f"✅ Synthèse vocale terminée")
                
            except Exception as e:
                print(f"❌ Erreur synthèse vocale: {e}")
            finally:
                self.is_speaking = False
                if callback:
                    callback()
        
        threading.Thread(target=speak_thread, daemon=True).start()
    
    def _generate_volume_data(self, text):
        """Génère des données de volume réalistes pour l'animation"""
        # Durée approximative basée sur la longueur du texte
        # Environ 15 caractères par seconde pour une parole naturelle
        duration = max(2, min(10, len(text) / 15))  # Entre 2 et 10 secondes
        
        # Génère un pattern de parole réaliste
        num_points = 100  # Points pour l'animation
        volume_data = []
        
        # Crée un pattern qui ressemble à de la parole
        for i in range(num_points):
            # Position dans le temps (0 à 1)
            t = i / num_points
            
            # Pattern de base : oscillations avec variations
            if t < 0.1:
                # Début doux
                base = 0.3 + 0.2 * math.sin(t * 20) * 0.5
            elif t > 0.9:
                # Fin douce
                base = 0.3 + 0.2 * math.sin(t * 20) * 0.5
            else:
                # Corps avec variations
                # Fréquence principale
                freq1 = 2 + math.sin(t * 5) * 1.5
                # Fréquence secondaire
                freq2 = 5 + math.cos(t * 3) * 2
                
                base = 0.4 + 0.3 * math.sin(t * freq1 * 2 * math.pi) + 0.1 * math.cos(t * freq2 * 2 * math.pi)
            
            # Ajoute du bruit pour plus de réalisme
            noise = 0.05 * (random.random() - 0.5)
            
            # Applique une enveloppe (plus fort au milieu)
            envelope = 4 * t * (1 - t)  # Courbe parabolique
            
            # Valeur finale
            value = max(0.1, min(0.9, (base + noise) * envelope))
            volume_data.append(value)
        
        # Ajoute des pauses occasionnelles (comme dans la vraie parole)
        for i in range(5):
            pause_pos = random.randint(10, 90)
            pause_length = random.randint(3, 8)
            for j in range(pause_length):
                if pause_pos + j < len(volume_data):
                    volume_data[pause_pos + j] *= 0.3
        
        return volume_data
    
    def stop(self):
        """Arrête la parole en cours"""
        if self.engine and self.is_speaking:
            self.engine.stop()
            self.is_speaking = False