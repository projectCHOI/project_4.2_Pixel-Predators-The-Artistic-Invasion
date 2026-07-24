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

    def check_appear(self, seconds, current_level):
        """매 초 타이머와 레벨을 체크하여 보스 활성화"""
        if current_level == 5 and not self.boss_active and seconds >= 10 and not self.boss_appeared:
            self.boss_active = True
            self.boss_appeared = True
            self.boss_hp = self.max_boss_hp
            self.state = "appear"
            self.state_start_time = pygame.time.get_ticks()

    def move(self):
        if not self.boss_active or self.boss_defeated:
            return

        current_time = pygame.time.get_ticks()
        time_in_state = current_time - self.state_start_time

        if self.state == "appear":
            speed = 4
            if self.side == "left":
                self.boss_pos[0] += speed
                if self.boss_pos[0] >= 100:
                    self.boss_pos[0] = 100
                    self._change_state("wait1")
            else:
                self.boss_pos[0] -= speed
                if self.boss_pos[0] <= WIN_WIDTH - 400:
                    self.boss_pos[0] = WIN_WIDTH - 400
                    self._change_state("wait1")

        elif self.state == "wait1":
            if time_in_state >= 1500:
                self._change_state("act")

        elif self.state == "act":
            if self.side == "left":
                self._move_left_side()
            else:
                self._move_right_side()

        elif self.state == "wait2":
            if time_in_state >= 1500:
                self._change_state("leave")

        elif self.state == "leave":
            speed = 6
            if self.side == "left":
                self.boss_pos[0] -= speed
                if self.boss_pos[0] <= -350:
                    self.boss_pos[0] = -350
                    self._change_state("wait3")
            else:
                self.boss_pos[0] += speed
                if self.boss_pos[0] >= WIN_WIDTH + 100:
                    self.boss_pos[0] = WIN_WIDTH + 100
                    self._change_state("wait3")

        elif self.state == "wait3":
            if time_in_state >= 1500:
                self.reset(reinit_side=True)
                self.boss_active = True
                self.boss_appeared = True
                self._change_state("appear")

    def _change_state(self, new_state):
        self.state = new_state
        self.state_start_time = pygame.time.get_ticks()