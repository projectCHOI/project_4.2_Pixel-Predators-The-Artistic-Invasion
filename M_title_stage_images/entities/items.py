# 아이템 클래스
import pygame
import random
from M_title_stage_images.config import *

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, item_type, res_manager):
        super().__init__()
        self.res = res_manager
        self.type = item_type