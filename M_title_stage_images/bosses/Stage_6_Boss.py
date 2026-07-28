import pygame
import os
import random
import math
from M_title_stage_images.config import *

class Stage6Boss: 
    def __init__(self, res_manager):
        self.res = res_manager

        # 이미지 로드 (ResourceManager 연동)
        self.boss_image = self.res.load_image("bosses", "boss_stage6.png", size=(250, 250))
        self.gem_image = self.res.load_image("items", "mob_Jewelry_6.png", size=(40, 40))
        self.boss_attack_images = {
            "high": self.res.load_image("boss_skilles", "boss_stage6_a.png", size=(30, 30)),
            "medium": self.res.load_image("boss_skilles", "boss_stage6_b.png", size=(30, 30)),
            "low": self.res.load_image("boss_skilles", "boss_stage6_c.png", size=(30, 30))
        }

        # 보스 속성 초기화
        self.max_boss_hp = 25
        self.boss_hp = self.max_boss_hp
        self.boss_damage = 1
        self.boss_pos = [950, 600]
        self.boss_active = False
        self.boss_appearing = False
        self.boss_waiting = False
        self.boss_disappearing = False
        self.boss_appeared = False
        self.boss_moving = False
        self.boss_returning = False
        self.move_target = None
        self.boss_speed = 3
        self.wait_time = 0
        self.boss_attacks = []
        self.boss_last_attack_time = 0
        self.attack_interval = 1200
        self.boss_defeated = False
        self.stage_cleared = False
        self.gem_active = False
        self.gem_pos = None
        
        # 무적 및 피격 제어
        self.invincible_duration = 300
        self.boss_hit_duration = 100
        self.boss_hit = False
        self.boss_hit_start_time = 0
        
    def get_attack_type(self):
        health_ratio = self.boss_hp / self.max_boss_hp
        if health_ratio > 0.6:
            return "low"
        elif health_ratio > 0.3:
            return "medium"
        else:
            return "high"

    def check_appear(self, seconds, current_level):
        """매 초 타이머와 레벨을 체크하여 보스 활성화"""
        if current_level == 6 and not self.boss_active and seconds >= 10 and not self.boss_appeared:
            self.boss_active = True
            self.boss_appearing = True
            self.boss_hp = self.max_boss_hp
            self.boss_appeared = True
