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
            
    def move(self):
        """순환형 잠복 및 기습 이동 패턴"""
        if not self.boss_active or self.boss_defeated:
            return

        if self.boss_appearing:
            self.boss_pos[1] -= self.boss_speed
            if self.boss_pos[1] <= 200:
                self.boss_appearing = False
                self.boss_waiting = True
                self.wait_time = pygame.time.get_ticks()
                
        elif self.boss_waiting:
            if pygame.time.get_ticks() - self.wait_time >= 2000:
                self.boss_waiting = False
                self.boss_moving = True
                self.move_target = self.boss_pos[0] - 400

        elif self.boss_moving:
            if self.boss_pos[0] > self.move_target:
                self.boss_pos[0] -= self.boss_speed
            else:
                self.boss_moving = False
                self.boss_returning = True

        elif self.boss_returning:
            if self.boss_pos[0] < 950:
                self.boss_pos[0] += self.boss_speed
            else:
                self.boss_returning = False
                self.boss_disappearing = True

        elif self.boss_disappearing:
            self.boss_pos[1] += self.boss_speed
            if self.boss_pos[1] >= 600:
                self.boss_disappearing = False
                self.boss_appearing = True

    def attack(self):
        """이동 상태 중 360도 방사형 일제 사격"""
        if not self.boss_active or self.boss_defeated:
            return
        if not self.boss_moving and not self.boss_returning:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.boss_last_attack_time > self.attack_interval:
            self.boss_last_attack_time = current_time
            attack_type = self.get_attack_type()
            
            num_shots = {"low": 12, "medium": 24, "high": 36}[attack_type]
            speed = {"low": 5, "medium": 6, "high": 7}[attack_type]
            image = self.boss_attack_images[attack_type]
            
            angle_step = 360 / num_shots
            start_x = self.boss_pos[0] + 125
            start_y = self.boss_pos[1] + 125

            for i in range(num_shots):
                angle = angle_step * i
                radian = math.radians(angle)
                dx = math.cos(radian) * speed
                dy = math.sin(radian) * speed
                self.boss_attacks.append([[start_x, start_y], [dx, dy], angle, image])
