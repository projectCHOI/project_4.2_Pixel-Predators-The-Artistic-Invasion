import pygame
import os
import random
import math
from M_title_stage_images.config import *

class Stage3Boss:
    def __init__(self, res_manager):
        self.res = res_manager

        # 이미지 로드 (ResourceManager 활용)
        self.boss_image = self.res.load_image("bosses", "boss_stage3.png", size=(120, 120))
        self.boss_attack_images = {
            "high": self.res.load_image("boss_skilles", "boss_stage3_a.png", size=(40, 40)),
            "medium": self.res.load_image("boss_skilles", "boss_stage3_b.png", size=(40, 40)),
            "low": self.res.load_image("boss_skilles", "boss_stage3_c.png", size=(40, 40))
        }
        self.teleport_warning_image = self.res.load_image("stages", "Stage18_mist.png", size=(60, 60))
        self.gem_image = self.res.load_image("items", "mob_Jewelry_3.png", size=(40, 40))

        # 보스 속성 초기화
        self.max_boss_hp = 15
        self.boss_hp = self.max_boss_hp
        self.boss_damage = 1
        self.boss_pos = [640 - 60, 200]
        self.boss_active = False
        self.boss_attacks = []
        self.boss_last_attack_time = 0
        self.attack_interval = 1000
        self.teleport_interval = 4000
        self.last_teleport_time = 0
        self.gem_pos = None
        self.gem_active = False
        self.boss_defeated = False
        self.boss_appeared = False
        self.stage_cleared = False
        self.invincible = False
        self.invincible_duration = 300
        self.last_hit_time = 0
        self.boss_hit = False
        self.boss_hit_start_time = 0
        self.boss_hit_duration = 100
