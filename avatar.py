# avatar.py
import pygame
import random
import math
import threading
import time
from config import Config

class ValentineAvatar:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT
        
        # État des yeux
        self.eyes_open = True
        self.eye_blink_progress = 0  # 0-1 pour l'animation
        self.blink_timer = 0
        self.next_blink = random.randint(
            Config.BLINK_INTERVAL_MIN,
            Config.BLINK_INTERVAL_MAX
        )
        
        # État de la bouche
        self.mouth_openness = 0.3  # 0.3-0.7
        self.target_mouth_openness = 0.3
        self.speaking = False
        self.volume_levels = []
        self.current_volume_index = 0
        
        # Couleurs
        self.face_color = pygame.Color(Config.FACE_COLOR)
        self.eye_color = pygame.Color("#8B475D")
        self.mouth_color = pygame.Color("#CD6889")
        
        # Position des éléments
        self.face_center = (self.width // 2, self.height // 2)
        self.face_radius = min(self.width, self.height) // 3
        
        # Démarrage de clignotement
        self._start_blinking()
    
    def _start_blinking(self):
        """Démarrage de thread de clignotement automatique"""
        def blink_thread():
            while True:
                current_time = pygame.time.get_ticks()
                
                if current_time - self.blink_timer > self.next_blink:
                    self._blink()
                    self.blink_timer = current_time
                    self.next_blink = random.randint(
                        Config.BLINK_INTERVAL_MIN,
                        Config.BLINK_INTERVAL_MAX
                    )
                
                time.sleep(0.05)  
        
        threading.Thread(target=blink_thread, daemon=True).start()
    
    def _blink(self):
        """Effectue un clignotement"""
        # Animation rapide d'ouverture/fermeture
        for i in range(10):
            self.eye_blink_progress = i / 10
            time.sleep(0.01)
        
        for i in range(10, -1, -1):
            self.eye_blink_progress = i / 10
            time.sleep(0.01)
        
        self.eye_blink_progress = 0
    
    def update_mouth(self, volume_levels=None):
        """Met à jour l'ouverture de la bouche basée sur le volume"""
        if volume_levels:
            self.volume_levels = volume_levels
            self.current_volume_index = 0
            self.speaking = True
        
        if self.speaking and self.volume_levels:
            # Avance dans les niveaux de volume
            if self.current_volume_index < len(self.volume_levels):
                volume = self.volume_levels[self.current_volume_index]
                self.target_mouth_openness = 0.3 + volume * 0.4
                self.current_volume_index += 1
            else:
                self.speaking = False
                self.target_mouth_openness = 0.3
        
        # Interpolation douce
        self.mouth_openness += (self.target_mouth_openness - self.mouth_openness) * Config.MOUTH_SMOOTHING
    
    def draw(self):
        """fonction pour dessiner les vsages"""

        self.screen.fill(pygame.Color(Config.BG_COLOR))
        
        # Visage
        pygame.draw.circle(
            self.screen,
            self.face_color,
            self.face_center,
            self.face_radius
        )
        
        # Yeux
        self._draw_eyes()
        
        # Bouche
        self._draw_mouth()
        
        # Sourcils (très simples)
        self._draw_eyebrows()
    
    def _draw_eyes(self):
        """Dessine les yeux avec animation de clignotement"""
        eye_y_offset = -self.face_radius // 4
        eye_spacing = self.face_radius // 2
        eye_radius = self.face_radius // 6
        
        # Ajuste la taille verticale avec le clignotement
        current_eye_height = eye_radius * (1 - self.eye_blink_progress * 0.8)
        
        # Œil gauche
        left_eye_pos = (
            self.face_center[0] - eye_spacing,
            self.face_center[1] + eye_y_offset
        )
        
        # Œil droit
        right_eye_pos = (
            self.face_center[0] + eye_spacing,
            self.face_center[1] + eye_y_offset
        )
        
        # les yeux comme des ellipses
        pygame.draw.ellipse(
            self.screen,
            self.eye_color,
            (
                left_eye_pos[0] - eye_radius,
                left_eye_pos[1] - current_eye_height,
                eye_radius * 2,
                current_eye_height * 2
            )
        )
        
        pygame.draw.ellipse(
            self.screen,
            self.eye_color,
            (
                right_eye_pos[0] - eye_radius,
                right_eye_pos[1] - current_eye_height,
                eye_radius * 2,
                current_eye_height * 2
            )
        )
        
        # Pupilles
        pupil_radius = eye_radius // 3
        pygame.draw.circle(
            self.screen,
            pygame.Color("#FFFFFF"),
            left_eye_pos,
            pupil_radius
        )
        pygame.draw.circle(
            self.screen,
            pygame.Color("#FFFFFF"),
            right_eye_pos,
            pupil_radius
        )
    
    def _draw_mouth(self):
        """ la bouche avec animation"""
        mouth_width = self.face_radius // 1.5
        mouth_height = self.face_radius // 4 * self.mouth_openness
        
        mouth_rect = pygame.Rect(
            self.face_center[0] - mouth_width // 2,
            self.face_center[1] + self.face_radius // 3 - mouth_height // 2,
            mouth_width,
            mouth_height
        )
        
        # Dessiner un sourire doux
        pygame.draw.ellipse(self.screen, self.mouth_color, mouth_rect)
    
    def _draw_eyebrows(self):
        """Dessine des sourcils très simples"""
        eyebrow_y = self.face_center[1] - self.face_radius // 2
        eyebrow_length = self.face_radius // 3
        
        # Sourcil gauche
        pygame.draw.line(
            self.screen,
            pygame.Color("#8B475D"),
            (self.face_center[0] - self.face_radius // 2, eyebrow_y),
            (self.face_center[0] - self.face_radius // 2 + eyebrow_length, eyebrow_y - 5),
            3
        )
        
        # Sourcil droit
        pygame.draw.line(
            self.screen,
            pygame.Color("#8B475D"),
            (self.face_center[0] + self.face_radius // 2 - eyebrow_length, eyebrow_y - 5),
            (self.face_center[0] + self.face_radius // 2, eyebrow_y),
            3
        )
