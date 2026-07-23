# M_title_stage_images/bosses/Stage_4_Boss.py
import pygame
import os
import random
import math
from M_title_stage_images.config import *

class Stage4Boss:
    def __init__(self, res_manager):
        self.res = res_manager

        # 이미지 로드 (ResourceManager 연동)
        self.boss_image = self.res.load_image("bosses", "boss_stage4.png", size=(150, 150))
        self.boss_attack_images = {
            "high": self.res.load_image("boss_skilles", "boss_stage4_a.png", size=(30, 30)),
            "medium": self.res.load_image("boss_skilles", "boss_stage4_b.png", size=(30, 30)),
            "low": self.res.load_image("boss_skilles", "boss_stage4_c.png", size=(30, 30))
        }
        self.gem_image = self.res.load_image("items", "mob_Jewelry_4.png", size=(40, 40))

        # 보스 속성 초기화
        self.max_boss_hp = 18
        self.boss_hp = self.max_boss_hp
        self.boss_damage = 1
        self.boss_pos = [640 - 75, 150]
        self.boss_active = False
        self.boss_attacks = []
        self.boss_last_attack_time = 0
        self.attack_interval = 1200
        self.boss_defeated = False
        self.boss_appeared = False
        self.stage_cleared = False
        self.gem_active = False
        self.gem_pos = None
        
        # 무적 및 피격 상태
        self.invincible = False
        self.invincible_duration = 300
        self.last_hit_time = 0
        self.boss_hit = False
        self.boss_hit_start_time = 0
        self.boss_hit_duration = 100
        
        # 가속 이동 속성
        self.boss_speed = 2
        self.acceleration = 0.05
        self.max_speed = 7
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]
