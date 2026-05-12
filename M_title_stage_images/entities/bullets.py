# 공격 및 에너지볼 클래스
import pygame
import math
from M_title_stage_images.config import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, color, target_pos):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (5, 5), 5)
        self.rect = self.image.get_rect(center=pos)
        
        self.speed = 15

        dx = target_pos[0] - pos[0]
        dy = target_pos[1] - pos[1]
        distance = math.hypot(dx, dy)
        
        if distance == 0:
            self.vx = 0
            self.vy = -self.speed
        else:
            self.vx = (dx / distance) * self.speed
            self.vy = (dy / distance) * self.speed
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
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

def update(self):
        # 계산된 방향 벡터만큼 이동
        self.x += self.vx
        self.y += self.vy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # 화면 경계 체크
        if (self.rect.bottom < 0 or self.rect.top > WIN_HEIGHT or 
                    self.rect.right < 0 or self.rect.left > WIN_WIDTH):
                    self.kill()
