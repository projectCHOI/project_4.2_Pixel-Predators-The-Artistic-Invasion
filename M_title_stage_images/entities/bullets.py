# 공격 및 에너지볼 클래스
import pygame
from M_title_stage_images.config import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, color, speed=15):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class EnergyBall(pygame.sprite.Sprite):
    def __init__(self, pos, target_pos, speed=5):
        super().__init__()
        # 이미지 크기 등은 설정에 따라 조절 가능
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (10, 10), 10)
        self.rect = self.image.get_rect(center=pos)
        
        # 목표 방향 계산 (벡터 활용)
        direction = pygame.math.Vector2(target_pos) - pygame.math.Vector2(pos)
        if direction.length() > 0:
            self.velocity = direction.normalize() * speed
        else:
            self.velocity = pygame.math.Vector2(0, speed)