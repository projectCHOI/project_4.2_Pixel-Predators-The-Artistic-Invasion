# M_title_stage_images/entities/bullets.py
import pygame
import math
from M_title_stage_images.config import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, color, target_pos): # target_pos 추가
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (5, 5), 5)
        self.rect = self.image.get_rect(center=pos)
        
        self.speed = 15
        # 방향 계산 로직
        mx, my = target_pos
        px, py = pos
        angle = math.atan2(my - py, mx - px) # 각도 계산
        
        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if not (0 <= self.rect.x <= WIN_WIDTH and 0 <= self.rect.y <= WIN_HEIGHT):
            self.kill()
class EnergyBall(pygame.sprite.Sprite):
    def __init__(self, pos, res_manager, target_pos): # target_pos 추가
        super().__init__()
        self.res = res_manager
        # 에너지볼 이미지 로드 (경로 확인 필수)
        self.image = self.res.load_image("player", "mob_me_ball.png", size=(30, 30))
        self.rect = self.image.get_rect(center=pos)
        
        self.speed = 8
        
        # 방향 계산
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

        if not (0 <= self.rect.x <= WIN_WIDTH and 0 <= self.rect.y <= WIN_HEIGHT):
            self.kill()        