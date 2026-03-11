# 아이템 클래스
import pygame
import random
from M_title_stage_images.config import *

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, item_type, res_manager):
        super().__init__()
        self.res = res_manager
        self.type = item_type

        if self.type == 'heal':
            self.image = self.res.load_image("items", "heal_item.png", size=(30, 30))
        elif self.type == 'power':
            self.image = self.res.load_image("items", "power_item.png", size=(30, 30))
        elif self.type == 'speed':
            self.image = self.res.load_image("items", "speed_item.png", size=(30, 30))
            
        self.rect = self.image.get_rect(center=pos)
        self.speed = 3

def update(self):
        self.rect.y += self.speed
        if self.rect.top > WIN_HEIGHT:
            self.kill()

def apply_effect(self, player):
        if self.type == 'heal':
            if player.health < player.max_health:
                player.health += 1
                return "체력 회복!"
        elif self.type == 'power':
            return "공격력 강화!"
        elif self.type == 'speed':
            player.speed += 2
            return "이동 속도 증가!"
        return ""