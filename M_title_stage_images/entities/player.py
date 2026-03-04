# 플레이어 클래스
import pygame
from M_title_stage_images.config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, res_manager):
        super().__init__()
        self.res = res_manager
        
        # 이미지 로드 및 초기 설정
        self.size = (50, 50)
        self.img_right = self.res.load_image("player", "mob_me1_png.png", size=self.size)
        self.img_left = self.res.load_image("player", "mob_me2_png.png", size=self.size)
        
        # 충돌 시 이미지 (딕셔너리 형태로 관리 가능)
        self.collision_imgs = {
            3: self.res.load_image("player", "mob_death_1.png", size=self.size),
            2: self.res.load_image("player", "mob_death_2.png", size=self.size),
            1: self.res.load_image("player", "mob_death_3.png", size=self.size)
        }
