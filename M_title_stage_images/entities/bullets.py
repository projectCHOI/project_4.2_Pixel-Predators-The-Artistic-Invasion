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