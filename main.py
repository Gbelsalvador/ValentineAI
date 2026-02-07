# main.py
import pygame
import sys
import threading
import time
import math
from datetime import datetime
from config import Config
from audio_input import AudioInput
from audio_output import AudioOutput
from brain import ValentineBrain
from avatar import ValentineAvatar

class ValentineAI:
    def __init__(self):
        pygame.init()
        
        # Fenêtre
        self.screen = pygame.display.set_mode(
            (Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT),
            pygame.RESIZABLE
        )
        pygame.display.set_caption("ValentineAI - Compagnon Émotionnel")
        
        # Horloge pour FPS stable
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Composants - Utilise le constructeur par défaut qui priorise OpenRouter
        self.brain = ValentineBrain()
        self.audio_input = AudioInput()
        self.audio_output = AudioOutput()
        self.avatar = ValentineAvatar(self.screen)
        
        # État
        self.running = True
        self.current_state = "greeting"
        self.user_input_text = ""
        self.ai_response_text = ""
        self.last_activity = datetime.now()
        
        # Police pour le texte
        try:
            self.font = pygame.font.SysFont("Arial", 20)
            self.small_font = pygame.font.SysFont("Arial", 16)
        except:
            # Fallback si Arial n'est pas disponible
            self.font = pygame.font.Font(None, 24)
            self.small_font = pygame.font.Font(None, 18)
        
        # Configuration des callbacks
        self.audio_output.volume_callback = self._on_volume_update
        
        # Démarrer
        self._startup_sequence()
    
    def _startup_sequence(self):
        """Séquence de démarrage douce"""
        def startup():
            # Attente initiale
            time.sleep(1)
            
            # Salutation
            greeting = self.brain.get_greeting()
            self.ai_response_text = greeting
            
            # Parle la salutation
            self.audio_output.speak(greeting, self._on_speech_end)
            
            # Démarre l'écoute
            time.sleep(2)
            self.audio_input.start_listening(self._on_user_speech)
            self.current_state = "listening"
        
        threading.Thread(target=startup, daemon=True).start()
    
    def _on_user_speech(self, text):
        """Callback quand l'utilisateur parle"""
        print(f"Vous: {text}")
        self.user_input_text = text
        self.current_state = "processing"
        self.last_activity = datetime.now()
        
        # Traite dans un thread séparé
        threading.Thread(target=self._process_user_input, args=(text,), daemon=True).start()
    
    def _process_user_input(self, text):
        """Traite l'entrée utilisateur et génère une réponse"""
        # Génère la réponse
        response = self.brain.process_input(text)
        print(f"Valentine: {response}")
        self.ai_response_text = response
        
        # Parle la réponse
        self.audio_output.speak(response, self._on_speech_end)
        
        # Re-passe en mode écoute
        self.current_state = "speaking"
    
    def _on_speech_end(self):
        """Quand l'IA finit de parler"""
        if self.current_state == "speaking":
            self.current_state = "listening"
            self.user_input_text = ""
    
    def _on_volume_update(self, volume_levels):
        """Mise à jour pour l'animation de la bouche"""
        self.avatar.update_mouth(volume_levels)
    
    def _handle_events(self):
        """Gère les événements PyGame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # Simulation de parole pour tests
                    self._on_user_speech("Je me sens seul aujourd'hui")
                elif event.key == pygame.K_t:
                    # Test direct de la synthèse vocale
                    test_text = "Bonjour, je suis Valentine. Je suis là pour toi."
                    self.ai_response_text = test_text
                    self.audio_output.speak(test_text, self._on_speech_end)
                    self.current_state = "speaking"
            
            elif event.type == pygame.VIDEORESIZE:
                # Redimensionnement de la fenêtre
                Config.WINDOW_WIDTH = event.w
                Config.WINDOW_HEIGHT = event.h
                self.screen = pygame.display.set_mode(
                    (event.w, event.h),
                    pygame.RESIZABLE
                )
    
    def _draw_interface(self):
        """Dessine l'interface complète"""
        # Avatar
        self.avatar.draw()
        
        # État actuel
        state_text = {
            "greeting": "Initialisation...",
            "listening": "🎤 J'écoute...",
            "processing": "💭 Je réfléchis...",
            "speaking": "💬 Je parle..."
        }.get(self.current_state, "")
        
        state_surface = self.font.render(state_text, True, pygame.Color("#8B475D"))
        self.screen.blit(state_surface, (20, 20))
        
        # Dernière entrée utilisateur
        if self.user_input_text:
            user_text = f"Vous: {self.user_input_text[:50]}..." if len(self.user_input_text) > 50 else f"Vous: {self.user_input_text}"
            user_surface = self.small_font.render(user_text, True, pygame.Color("#666666"))
            self.screen.blit(user_surface, (20, Config.WINDOW_HEIGHT - 60))
        
        # Réponse IA
        if self.ai_response_text:
            # Affiche la réponse progressivement
            chars_to_show = min(len(self.ai_response_text), 
                              int((pygame.time.get_ticks() // 50) % (len(self.ai_response_text) + 20)))
            display_text = f"Valentine: {self.ai_response_text[:chars_to_show]}"
            
            # Wrapping du texte
            words = display_text.split(' ')
            lines = []
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                if self.font.size(test_line)[0] < Config.WINDOW_WIDTH - 40:
                    current_line.append(word)
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
            lines.append(' '.join(current_line))
            
            # Affiche chaque ligne
            for i, line in enumerate(lines[-3:]):  # Max 3 lignes
                ai_surface = self.small_font.render(line, True, pygame.Color("#CD6889"))
                self.screen.blit(ai_surface, (20, Config.WINDOW_HEIGHT - 90 + i * 25))
        
        # Instructions
        instr = "ESC: Quitter | ESPACE: Simulation | T: Test voix"
        instr_surface = self.small_font.render(instr, True, pygame.Color("#999999"))
        self.screen.blit(instr_surface, (Config.WINDOW_WIDTH - instr_surface.get_width() - 20, 20))
        
        # Cœur animé en bas
        heart_size = 20 + 5 * abs(math.sin(pygame.time.get_ticks() / 500))
        heart_pos = (Config.WINDOW_WIDTH // 2, Config.WINDOW_HEIGHT - 30)
        self._draw_heart(heart_pos, heart_size, pygame.Color("#FF6B8B"))
    
    def _draw_heart(self, pos, size, color):
        """Dessine un petit cœur"""
        # Coeur simplifié avec deux cercles et un triangle
        x, y = pos
        
        # Cercles (parties supérieures)
        left_circle_center = (x - size//3, y - size//4)
        right_circle_center = (x + size//3, y - size//4)
        
        pygame.draw.circle(self.screen, color, left_circle_center, size//3)
        pygame.draw.circle(self.screen, color, right_circle_center, size//3)
        
        # Triangle (partie inférieure)
        points = [
            (x - size//2, y - size//4),
            (x + size//2, y - size//4),
            (x, y + size//2)
        ]
        pygame.draw.polygon(self.screen, color, points)
    
    def run(self):
        """Boucle principale"""
        while self.running:
            # Gestion des événements
            self._handle_events()
            
            # Mise à jour de l'animation
            if self.current_state == "speaking":
                self.avatar.update_mouth()
            else:
                self.avatar.update_mouth([])
            
            # Dessin
            self._draw_interface()
            
            # Mise à jour de l'affichage
            pygame.display.flip()
            
            # FPS stable
            self.clock.tick(self.fps)
        
        # Nettoyage
        self._cleanup()
    
    def _cleanup(self):
        """Nettoyage à la fermeture"""
        self.audio_input.stop_listening()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = ValentineAI()
    app.run()