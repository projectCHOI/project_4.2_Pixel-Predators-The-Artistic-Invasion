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

    def check_appear(self, seconds, current_level):
        """매 초 타이머와 레벨을 체크하여 보스 활성화"""
        if current_level == 4 and not self.boss_active and seconds >= 10 and not self.boss_appeared:
            self.boss_active = True
            self.boss_pos = [640 - 75, 150]
            self.boss_hp = self.max_boss_hp
            self.boss_appeared = True
            self.boss_speed = 2

    def move(self):
        """보스 가속 바운스 이동 알고리즘"""
        if not self.boss_active or self.boss_hp <= 0:
            return

        self.boss_speed = min(self.boss_speed + self.acceleration, self.max_speed)
        self.boss_pos[0] += self.direction[0] * self.boss_speed
        self.boss_pos[1] += self.direction[1] * self.boss_speed

        # 벽 충돌 시 반사
        if self.boss_pos[0] <= 10 or self.boss_pos[0] >= WIN_WIDTH - 160:
            self.direction[0] = -self.direction[0]
        if self.boss_pos[1] <= 10 or self.boss_pos[1] >= WIN_HEIGHT - 320:
            self.direction[1] = -self.direction[1]

        self.boss_pos[0] = max(10, min(self.boss_pos[0], WIN_WIDTH - 160))
        self.boss_pos[1] = max(10, min(self.boss_pos[1], WIN_HEIGHT - 320))
    
    def attack(self):
        """체력 잔량에 따른 난사 공격"""
        if not self.boss_active or self.boss_hp <= 0:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.boss_last_attack_time > self.attack_interval:
            self.boss_last_attack_time = current_time
            num_shots = 4 + (self.max_boss_hp - self.boss_hp) // 4
            
            for _ in range(num_shots):
                angle = random.uniform(0, 360)
                radian = math.radians(angle)
                dx = math.cos(radian) * 6
                dy = math.sin(radian) * 6
                attack_type = self.get_attack_type()
                
                start_x = self.boss_pos[0] + 75
                start_y = self.boss_pos[1] + 75
                self.boss_attacks.append([[start_x, start_y], [dx, dy], angle, attack_type])
    
    def get_attack_type(self):
        health_ratio = self.boss_hp / self.max_boss_hp
        if health_ratio > 0.6:
            return "low"
        elif health_ratio > 0.3:
            return "medium"
        else:
            return "high"