import pygame
import os
import math
import random
from M_title_stage_images.config import *

class Stage5Boss:
    def __init__(self, res_manager):
        self.res = res_manager

        # 이미지 로드 (ResourceManager 활용)
        self.boss_image_left = self.res.load_image("bosses", "boss_stage5_Left.png", size=(300, 300))
        self.boss_image_right = self.res.load_image("bosses", "boss_stage5_Right.png", size=(300, 300))
        self.boss_attack_images = [
            self.res.load_image("boss_skilles", "boss_stage5_a.png", size=(40, 40)),
            self.res.load_image("boss_skilles", "boss_stage5_b.png", size=(40, 40)),
            self.res.load_image("boss_skilles", "boss_stage5_c.png", size=(40, 40)),
        ]
        self.gem_image = self.res.load_image("items", "mob_Jewelry_5.png", size=(40, 40))
        self.boss_effect_image = self.res.load_image("boss_skilles", "boss_stage5_d.png", size=(180, 180))
        
        self.effect_offsets = [
            (-100, -100), (100, -100), (-125, 125), (125, 125),
            (-50, -50), (50, -50), (-50, 50), (50, 50),
            (-100, 0), (0, -100), (100, 0), (0, 100), (0, 0)
        ]
        
        self.max_boss_hp = 20
        self.boss_hp = self.max_boss_hp
        self.boss_damage = 1
        self.boss_invincible_duration = 300
        self.boss_hit_duration = 100

        self.side = random.choice(["left", "right"])
        if self.side == "left":
            self.boss_pos = [-300, 150]
            self.boss_image = self.boss_image_left
        else:
            self.boss_pos = [WIN_WIDTH + 100, 150]
            self.boss_image = self.boss_image_right

        self.boss_attacks = []
        self.boss_active = False
        self.boss_appeared = False
        self.boss_defeated = False
        self.gem_active = False
        self.gem_pos = None

        self.state = "appear"
        self.state_start_time = pygame.time.get_ticks()

        self.attack_cooldown = 1000
        self.last_attack_time = pygame.time.get_ticks()
        self.boss_hit = False
        self.boss_hit_start_time = 0

        self.vertical_moves_done = 0
        self.going_forward = True
        self.stage_cleared = False