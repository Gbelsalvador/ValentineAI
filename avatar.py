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
        self.hair_color = pygame.Color("#3D2430")
        self.hair_highlight = pygame.Color("#6B4050")
        self.eye_color = pygame.Color("#4A2636")
        self.skin_shadow = pygame.Color("#F0B9C5")
        self.blush_color = pygame.Color("#F49CAF")
        self.outfit_color = pygame.Color("#B94E72")
        self.outfit_shadow = pygame.Color("#8E3557")
        self.mouth_color = pygame.Color("#B84D70")
        self.lip_highlight = pygame.Color("#E989A3")
        
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
        """Dessine le portrait et ses éléments animés."""

        self.width, self.height = self.screen.get_size()
        self.face_center = (self.width // 2, self.height // 2)
        self.face_radius = min(self.width, self.height) // 3

        self.screen.fill(pygame.Color(Config.BG_COLOR))
        
        # Silhouette : cheveux, cou, épaules et buste derrière le visage.
        shoulder_y = self.face_center[1] + self.face_radius + self.face_radius // 3
        torso_top = shoulder_y - self.face_radius // 5
        torso_bottom = self.height + self.face_radius
        center_x = self.face_center[0]
        pygame.draw.polygon(
            self.screen,
            self.outfit_color,
            [
                (center_x - self.face_radius * 3 // 2, torso_top),
                (center_x - self.face_radius // 2, torso_top - self.face_radius // 8),
                (center_x - self.face_radius // 3, torso_top + self.face_radius // 4),
                (center_x + self.face_radius // 3, torso_top + self.face_radius // 4),
                (center_x + self.face_radius // 2, torso_top - self.face_radius // 8),
                (center_x + self.face_radius * 3 // 2, torso_top),
                (center_x + self.face_radius * 2, torso_bottom),
                (center_x - self.face_radius * 2, torso_bottom),
            ],
        )
        pygame.draw.line(
            self.screen,
            self.outfit_shadow,
            (center_x, torso_top + self.face_radius // 5),
            (center_x, torso_bottom),
            max(2, self.face_radius // 25),
        )
        pygame.draw.ellipse(
            self.screen,
            self.skin_shadow,
            (
                center_x - self.face_radius // 3,
                shoulder_y - self.face_radius // 2,
                self.face_radius * 2 // 3,
                self.face_radius * 5 // 4,
            ),
        )
        pygame.draw.ellipse(
            self.screen,
            self.outfit_shadow,
            (
                center_x - self.face_radius * 3 // 2,
                torso_top - self.face_radius // 5,
                self.face_radius * 3,
                self.face_radius,
            ),
        )

        # Visage et mèches latérales.
        pygame.draw.circle(
            self.screen,
            self.face_color,
            self.face_center,
            self.face_radius
        )
        self._draw_hair_frame()
        
        # Yeux
        self._draw_eyes()
        
        # Bouche
        self._draw_mouth()
        
        # Sourcils (très simples)
        self._draw_eyebrows()

        # Nez et joues pour donner du relief au portrait.
        nose_x = self.face_center[0]
        nose_y = self.face_center[1] + self.face_radius // 8
        pygame.draw.line(
            self.screen,
            self.skin_shadow,
            (nose_x, nose_y - self.face_radius // 12),
            (nose_x - self.face_radius // 18, nose_y + self.face_radius // 10),
            max(1, self.face_radius // 35),
        )
        pygame.draw.circle(
            self.screen,
            self.blush_color,
            (self.face_center[0] - self.face_radius * 2 // 3, self.face_center[1] + self.face_radius // 5),
            max(2, self.face_radius // 12),
        )
        earring_y = self.face_center[1] + self.face_radius // 3
        for earring_x in (self.face_center[0] - self.face_radius, self.face_center[0] + self.face_radius):
            pygame.draw.circle(
                self.screen,
                pygame.Color("#F7C96B"),
                (earring_x, earring_y),
                max(2, self.face_radius // 24),
            )
        pygame.draw.circle(
            self.screen,
            self.blush_color,
            (self.face_center[0] + self.face_radius * 2 // 3, self.face_center[1] + self.face_radius // 5),
            max(2, self.face_radius // 12),
        )

    def _draw_hair_frame(self):
        """Dessine la frange et les mèches qui encadrent le visage."""
        top = self.face_center[1] - self.face_radius
        pygame.draw.arc(
            self.screen,
            self.hair_highlight,
            (
                self.face_center[0] - self.face_radius,
                top - self.face_radius // 8,
                self.face_radius * 2,
                self.face_radius * 2 // 3,
            ),
            math.pi,
            math.tau,
            max(2, self.face_radius // 18),
        )
        for side in (-1, 1):
            x = self.face_center[0] + side * (self.face_radius - self.face_radius // 8)
            pygame.draw.ellipse(
                self.screen,
                self.hair_color,
                (
                    x - self.face_radius // 5,
                    self.face_center[1] - self.face_radius // 2,
                    self.face_radius * 2 // 5,
                    self.face_radius * 3 // 2,
                ),
            )

        # Frange souple qui donne une forme plus expressive au visage.
        pygame.draw.polygon(
            self.screen,
            self.hair_color,
            [
                (self.face_center[0] - self.face_radius, self.face_center[1] - self.face_radius // 2),
                (self.face_center[0] - self.face_radius * 3 // 5, self.face_center[1] - self.face_radius),
                (self.face_center[0] - self.face_radius // 6, self.face_center[1] - self.face_radius * 3 // 5),
                (self.face_center[0] + self.face_radius // 8, self.face_center[1] - self.face_radius),
                (self.face_center[0] + self.face_radius * 3 // 5, self.face_center[1] - self.face_radius * 4 // 5),
                (self.face_center[0] + self.face_radius, self.face_center[1] - self.face_radius // 2),
            ],
        )
    
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
        
        # Yeux en amande avec iris et reflets.
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

        for eye_x in (left_eye_pos[0], right_eye_pos[0]):
            pygame.draw.circle(
                self.screen,
                pygame.Color("#B86A83"),
                (eye_x, left_eye_pos[1]),
                max(2, eye_radius // 2),
            )
        
        # Pupilles
        pupil_radius = eye_radius // 3
        pygame.draw.circle(
            self.screen,
            pygame.Color("#FFFFFF"),
            left_eye_pos,
            pupil_radius
        )

        if self.eye_blink_progress < 0.7:
            for eye_x in (left_eye_pos[0], right_eye_pos[0]):
                pygame.draw.line(
                    self.screen,
                    self.eye_color,
                    (eye_x - eye_radius, left_eye_pos[1] - current_eye_height),
                    (eye_x + eye_radius, left_eye_pos[1] - current_eye_height),
                    max(1, self.face_radius // 35),
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
        
        # Lèvres avec ouverture animée par la voix.
        pygame.draw.ellipse(self.screen, self.mouth_color, mouth_rect)
        if mouth_height > 2:
            inner_rect = mouth_rect.inflate(-max(2, self.face_radius // 12), -max(1, self.face_radius // 25))
            pygame.draw.ellipse(self.screen, pygame.Color("#5A1E35"), inner_rect)
        pygame.draw.arc(
            self.screen,
            self.lip_highlight,
            mouth_rect,
            math.pi,
            math.tau,
            max(1, self.face_radius // 35),
        )
    
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
