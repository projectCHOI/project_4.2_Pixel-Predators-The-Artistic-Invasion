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