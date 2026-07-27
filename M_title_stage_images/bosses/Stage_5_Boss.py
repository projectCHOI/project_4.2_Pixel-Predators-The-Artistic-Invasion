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

    def _move_left_side(self):
        self.attack()
        if self.going_forward:
            self.boss_pos[0] += 3
            if self.boss_pos[0] >= 400:
                self.boss_pos[0] = 400
                self.going_forward = False
        else:
            self.boss_pos[0] -= 4
            if self.boss_pos[0] <= 100:
                self.boss_pos[0] = 100
                self._change_state("wait2")

    def _move_right_side(self):
        self.attack()
        speed = 5
        target_up = 80
        target_down = 250

        moving_up = (self.vertical_moves_done % 2 == 0)
        if moving_up:
            self.boss_pos[1] -= speed
            if self.boss_pos[1] <= target_up:
                self.boss_pos[1] = target_up
                self.vertical_moves_done += 1
        else:
            self.boss_pos[1] += speed
            if self.boss_pos[1] >= target_down:
                self.boss_pos[1] = target_down
                self.vertical_moves_done += 1

        if self.vertical_moves_done >= 6:
            self._change_state("wait2")

    def attack(self):
        if self.state != "act" or not self.boss_active or self.boss_defeated:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = current_time

            if self.boss_hp > self.max_boss_hp * 0.75:
                directions = [0]
                self.attack_cooldown = 800
            elif self.boss_hp > self.max_boss_hp * 0.5:
                directions = [-15, 0, 15]
                self.attack_cooldown = 600
            elif self.boss_hp > self.max_boss_hp * 0.25:
                directions = [-30, -15, 0, 15, 30]
                self.attack_cooldown = 500
            else:
                directions = [-45, -30, -15, 0, 15, 30, 45]
                self.attack_cooldown = 350

            for angle_offset in directions:
                angle_deg = 0 if self.side == "left" else 180
                angle_deg += angle_offset
                rad = math.radians(angle_deg)
                dx = math.cos(rad) * 8
                dy = math.sin(rad) * 8

                start_x = self.boss_pos[0] + 150
                start_y = self.boss_pos[1] + 150

                random_attack_image = random.choice(self.boss_attack_images)

                self.boss_attacks.append({
                    'pos': [start_x, start_y],
                    'dir': [dx, dy],
                    'angle': angle_deg,
                    'image': random_attack_image
                })

    def update_attacks(self, player_rect, is_invincible=False):
        new_boss_attacks = []
        player_hit = False

        # 보스 본체 및 이펙트 몸통 충돌
        if self.boss_active and not is_invincible and self.state == "act":
            boss_rect = pygame.Rect(self.boss_pos[0], self.boss_pos[1], 300, 300)
            if player_rect.colliderect(boss_rect):
                player_hit = True

        # 탄환 충돌
        for attack in self.boss_attacks:
            attack['pos'][0] += attack['dir'][0]
            attack['pos'][1] += attack['dir'][1]
            bx, by = attack['pos']

            if -50 <= bx <= WIN_WIDTH + 50 and -50 <= by <= WIN_HEIGHT + 50:
                bullet_rect = pygame.Rect(bx - 15, by - 15, 30, 30)
                if not is_invincible and bullet_rect.colliderect(player_rect):
                    player_hit = True
                else:
                    new_boss_attacks.append(attack)

        self.boss_attacks = new_boss_attacks
        return self.boss_damage if player_hit else 0

    def check_hit(self, player_bullets_group):
        if not self.boss_active or self.boss_defeated:
            return
        if self.state != "act":
            return

        current_time = pygame.time.get_ticks()
        if self.boss_hit and (current_time - self.boss_hit_start_time) < self.boss_invincible_duration:
            return

        self.boss_hit = False
        boss_rect = pygame.Rect(self.boss_pos[0], self.boss_pos[1], 300, 300)

        for bullet in player_bullets_group:
            if boss_rect.colliderect(bullet.rect):
                bullet.kill()
                self.boss_hp -= 1
                self.boss_hit = True
                self.boss_hit_start_time = current_time

                if self.boss_hp <= 0:
                    self.boss_hp = 0
                    self.boss_defeated = True
                    self.boss_active = False
                    self.boss_attacks.clear()
                    self.gem_pos = [self.boss_pos[0] + 130, self.boss_pos[1] + 130]
                    self.gem_active = True
                break
                
    def draw(self, win):
        if not self.boss_active:
            return

        if not self.boss_defeated and self.boss_hp > 0:
            current_time = pygame.time.get_ticks()
            if self.boss_hit:
                if current_time - self.boss_hit_start_time < self.boss_invincible_duration:
                    if (current_time // self.boss_hit_duration) % 2 == 0:
                        win.blit(self.boss_image, self.boss_pos)
                else:
                    self.boss_hit = False
                    win.blit(self.boss_image, self.boss_pos)
            else:
                win.blit(self.boss_image, self.boss_pos)

        # 등장 및 퇴장 상태 잔상 이펙트 드로잉
        if self.state in ("appear", "wait1", "wait2", "wait3", "leave"):
            for (offset_x, offset_y) in self.effect_offsets:
                effect_x = self.boss_pos[0] + 60 + offset_x
                effect_y = self.boss_pos[1] + 60 + offset_y
                win.blit(self.boss_effect_image, (effect_x, effect_y))

    def draw_attacks(self, win):
        if not self.boss_active:
            return

        for attack in self.boss_attacks:
            angle = -attack['angle'] + 90
            rotated_image = pygame.transform.rotate(attack['image'], angle)
            rect = rotated_image.get_rect(center=attack['pos'])
            win.blit(rotated_image, rect)

    def draw_gem(self, win):
        if self.gem_active and self.gem_pos:
            win.blit(self.gem_image, self.gem_pos)

    def draw_health_bar(self, win, font):
        if not self.boss_active and not self.boss_defeated:
            return

        if not self.boss_defeated and self.boss_hp > 0:
            boss_text = font.render("BOSS LV.5", True, (255, 255, 255))
            
            bar_width = 600
            bar_height = 20
            bar_x = (WIN_WIDTH // 2) - (bar_width // 2)
            bar_y = WIN_HEIGHT - 80
            
            win.blit(boss_text, (bar_x, bar_y - 25))

            health_ratio = self.boss_hp / self.max_boss_hp
            current_health_width = int(bar_width * health_ratio)

            pygame.draw.rect(win, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(win, (210, 20, 4), (bar_x, bar_y, current_health_width, bar_height))
            pygame.draw.rect(win, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

    def check_gem_collision(self, player_rect):
