# M_title_stage_images/entities/bullets.py
import pygame
import math
from M_title_stage_images.config import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, color, target_pos):
        super().__init__()
        # 반지름 2인 빨간색/지정색 작은 원 생성
        self.radius = 2
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=pos)
        
        self.speed = 40
        
        mx, my = target_pos
        px, py = pos
        angle = math.atan2(my - py, mx - px)
        
        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
            self.x += self.vx
            self.y += self.vy
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)
    
            if (self.rect.bottom < 0 or self.rect.top > WIN_HEIGHT or 
                self.rect.right < 0 or self.rect.left > WIN_WIDTH):
                self.kill()

class EnergyBall(pygame.sprite.Sprite):
    def __init__(self, pos, res_manager, target_pos):
        super().__init__()
        self.res = res_manager
        
        self.radius = 10
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
