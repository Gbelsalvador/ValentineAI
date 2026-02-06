# audio_output.py
import pyttsx3
import pygame
import numpy as np
import threading
import tempfile
import os
import time
from config import Config

class AudioOutput:
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.engine = self._init_tts_engine()
        self.is_speaking = False
        self.volume_data = []
        self.volume_callback = None
    
    def _init_tts_engine(self):
        """Initialise le moteur TTS avec une voix française douce"""
        engine = pyttsx3.init()
        
        # Configure une voix douce
        voices = engine.getProperty('voices')
        french_voices = [v for v in voices if 'french' in v.name.lower()]
        
        if french_voices:
            engine.setProperty('voice', french_voices[0].id)
        else:
            # Essaye de trouver une voix féminine
            for voice in voices:
                if 'female' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
        
        # Paramètres doux
        engine.setProperty('rate', 150)  # Plus lent
        engine.setProperty('volume', 0.8)  # Moins fort
        engine.setProperty('pitch', 110)  # Un peu plus aigu
        
        return engine
    
    def speak(self, text, callback=None):
        """Convertit le texte en parole et joue l'audio"""
        if self.is_speaking:
            return
        
        self.is_speaking = True
        
        def speak_thread():
            try:
                # Crée un fichier audio temporaire
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                    temp_file = f.name
                
                # Sauvegarde la parole dans un fichier
                self.engine.save_to_file(text, temp_file)
                self.engine.runAndWait()

                # Attendre que le fichier soit réellement écrit
                if not self._wait_for_file_ready(temp_file):
                    print("Erreur synthèse vocale: fichier audio vide ou illisible")
                    # Fallback: parle sans analyse de volume
                    self.engine.say(text)
                    self.engine.runAndWait()
                    if self.volume_callback:
                        self.volume_callback(self._fake_volume_data(text))
                    return
                
                # Charge et joue avec pygame pour analyser le volume
                self._play_with_volume_analysis(temp_file)
                
                # Nettoie le fichier temporaire
                os.unlink(temp_file)
                
            except Exception as e:
                print(f"Erreur synthèse vocale: {e}")
            finally:
                self.is_speaking = False
                self.volume_data = []
                if callback:
                    callback()
        
        threading.Thread(target=speak_thread, daemon=True).start()
    
    def _play_with_volume_analysis(self, filename):
        """Joue l'audio et analyse le volume pour l'animation"""
        try:
            sound = pygame.mixer.Sound(filename)
            channel = sound.play()
            
            # Capture les données audio pour l'analyse de volume
            array = pygame.sndarray.array(sound)
            if array.ndim == 2:  # Stéréo
                array = array.mean(axis=1)
            
            # Normalise et réduit la fréquence d'échantillonnage
            self.volume_data = self._process_audio_data(array)
            
            # Notifie l'animation
            if self.volume_callback:
                self._send_volume_updates()
            
            # Attend la fin de la lecture
            while channel and channel.get_busy():
                pygame.time.delay(50)
                
        except Exception as e:
            print(f"Erreur lecture audio: {e}")

    def _wait_for_file_ready(self, filename, timeout_s=5.0):
        """Attend que le fichier audio soit écrit et non vide"""
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            try:
                if os.path.exists(filename) and os.path.getsize(filename) > 44:
                    return True
            except OSError:
                pass
            time.sleep(0.05)
        return False
    
    def _process_audio_data(self, audio_array):
        """Traite les données audio pour l'animation"""
        # Normalise
        if len(audio_array) > 0:
            audio_array = audio_array / np.max(np.abs(audio_array))
        
        # Réduit la résolution pour l'animation
        target_length = 100  # 100 points pour toute la phrase
        if len(audio_array) > target_length:
            step = len(audio_array) // target_length
            audio_array = audio_array[::step][:target_length]
        
        # Convertit en volume (valeur absolue)
        volume = np.abs(audio_array)
        return volume.tolist()
    
    def _send_volume_updates(self):
        """Envoie les mises à jour de volume pour l'animation en temps réel"""
        if not self.volume_callback or not self.volume_data:
            return
        
        # Pour une implémentation temps réel, on utiliserait un thread
        # Ici, on simule avec un envoi unique
        self.volume_callback(self.volume_data)

    def _fake_volume_data(self, text):
        """Volume factice quand l'audio n'est pas lisible"""
        # Durée approximative: ~12 caractères par seconde
        length = max(40, min(140, len(text) // 2))
        return [0.4] * length
