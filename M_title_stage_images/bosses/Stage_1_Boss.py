import pygame
import os
import math
from M_title_stage_images.config import *

class Stage1Boss:
    def __init__(self, res_manager):
        self.res = res_manager

        self.boss_image = self.res.load_image("bosses", "boss_stage1.png", size=(140, 140))
        self.boss_attack_image = self.res.load_image("boss_skilles", "boss_stage1_a.png", size=(40, 40))
        self.gem_image = self.res.load_image("items", "mob_Jewelry_1.png", size=(40, 40))

        self.boss_appear_time = 10
        self.max_boss_hp = 15
        self.boss_hp = self.max_boss_hp
        self.boss_damage = 1
        self.boss_speed = 6
        self.boss_pos = [640 - 70, 0]
        
        self.boss_direction_x = 1
        self.boss_direction_y = 1
        
        self.boss_active = False
        self.boss_defeated = False
        self.boss_appeared = False
        self.boss_move_phase = 1
        
        self.boss_hit = False
        self.boss_hit_start_time = 0
        self.boss_hit_duration = 100
        self.boss_invincible_duration = 200

        self.boss_attacks = []
        self.boss_attack_cooldown = 1000
        self.boss_last_attack_time = 0

        self.gem_pos = None
        self.gem_active = False
        self.stage_cleared = False

    def check_appear(self, seconds, current_level):
        if current_level == 1 and not self.boss_active and seconds >= self.boss_appear_time and not self.boss_appeared:
            self.boss_active = True
            self.boss_pos = [640 - 70, 20]
            self.boss_hp = self.max_boss_hp
            self.boss_move_phase = 2
            self.boss_appeared = True

    def move(self):
        if not self.boss_active or self.boss_hp <= 0:
            return

        def limit_position():
            self.boss_pos[0] = max(0, min(self.boss_pos[0], WIN_WIDTH - 140))
            self.boss_pos[1] = max(0, min(self.boss_pos[1], WIN_HEIGHT - 350))

        if self.boss_move_phase == 2:
            self.boss_pos[0] += self.boss_speed * self.boss_direction_x
            if self.boss_pos[0] <= 0 or self.boss_pos[0] >= WIN_WIDTH - 140:
                self.boss_direction_x *= -1

            if self.boss_hp <= self.max_boss_hp * 0.5:
                self.boss_move_phase = 3

        elif self.boss_move_phase == 3:
            self.boss_pos[0] += self.boss_speed * self.boss_direction_x
            self.boss_pos[1] += self.boss_speed * self.boss_direction_y
            if self.boss_pos[0] <= 0 or self.boss_pos[0] >= WIN_WIDTH - 140:
                self.boss_direction_x *= -1
            if self.boss_pos[1] <= 0 or self.boss_pos[1] >= WIN_HEIGHT - 350:
                self.boss_direction_y *= -1

        limit_position()

    def attack(self):
        if not self.boss_active or self.boss_hp <= 0:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.boss_last_attack_time > self.boss_attack_cooldown:
            self.boss_last_attack_time = current_time
            attack_angles = []

            if self.boss_hp > self.max_boss_hp * 0.75:
                attack_angles = [90]
            elif self.boss_hp > self.max_boss_hp * 0.5:
                attack_angles = [85, 90, 95]
            elif self.boss_hp > self.max_boss_hp * 0.25:
                attack_angles = [80, 85, 90, 95, 100]
            else:
                attack_angles = [75, 80, 85, 90, 95, 100, 105]

            attack_start_pos = [self.boss_pos[0] + 70, self.boss_pos[1] + 120]

            for angle in attack_angles:
                radian = math.radians(angle)
                dx = math.cos(radian) * 8
                dy = math.sin(radian) * 8
                self.boss_attacks.append({
                    'pos': [attack_start_pos[0], attack_start_pos[1]],
                    'dir': [dx, dy],
                    'angle': angle
                })

    def update_attacks(self, player_rect, is_invincible=False):
        new_boss_attacks = []
        player_hit = False

        for attack in self.boss_attacks:
            attack['pos'][0] += attack['dir'][0]
            attack['pos'][1] += attack['dir'][1]
            bx, by = attack['pos']
            
            if -50 <= bx <= WIN_WIDTH + 50 and -50 <= by <= WIN_HEIGHT + 50:
                bullet_rect = pygame.Rect(bx - 12, by - 12, 25, 25)
                
                if not is_invincible and bullet_rect.colliderect(player_rect):
                    player_hit = True
                else:
                    new_boss_attacks.append(attack)

        self.boss_attacks = new_boss_attacks
        return self.boss_damage if player_hit else 0

    def check_hit(self, player_bullets_group):
        if not self.boss_active or self.boss_hp <= 0:
            return

        current_time = pygame.time.get_ticks()
        if self.boss_hit and (current_time - self.boss_hit_start_time) < self.boss_invincible_duration:
            return

        self.boss_hit = False
        boss_rect = pygame.Rect(self.boss_pos[0], self.boss_pos[1], 140, 140)

        for bullet in player_bullets_group:
            if boss_rect.colliderect(bullet.rect):
                bullet.kill()
                self.boss_hp -= 1
                self.boss_hit = True
                self.boss_hit_start_time = current_time
                
                if self.boss_hp <= 0:
                    self.boss_hp = 0
                    self.boss_active = False
                    self.boss_defeated = True
                    self.gem_pos = [self.boss_pos[0] + 50, self.boss_pos[1] + 50]
                    self.gem_active = True
                break

    def check_gem_collision(self, player_rect):
        if self.gem_active:
            gem_rect = pygame.Rect(self.gem_pos[0], self.gem_pos[1], 40, 40)
            if gem_rect.colliderect(player_rect):
                self.gem_active = False
                self.stage_cleared = True
                return True
        return False

    def draw(self, win):
        if self.boss_active and self.boss_hp > 0:
            current_time = pygame.time.get_ticks()
            if self.boss_hit:
                if (current_time // self.boss_hit_duration) % 2 == 0:
                    win.blit(self.boss_image, self.boss_pos)
            else:
                win.blit(self.boss_image, self.boss_pos)

    def draw_attacks(self, win):
        for attack in self.boss_attacks:
            angle = -attack['angle'] + 90
            rotated_image = pygame.transform.rotate(self.boss_attack_image, angle)
            rect = rotated_image.get_rect(center=attack['pos'])
            win.blit(rotated_image, rect)

    def draw_gem(self, win):
        if self.gem_active:
            win.blit(self.gem_image, self.gem_pos)

    # 🔍 [수정] font 매개변수를 추가하여 Stage2Boss와 메서드 서명을 동일하게 맞췄습니다.
    def draw_health_bar(self, win, font):
        if self.boss_active and self.boss_hp > 0:
            boss_text = font.render("BOSS LV.1", True, (255, 255, 255))
            
            bar_width = 600
            bar_height = 20
            bar_x = (WIN_WIDTH // 2) - (bar_width // 2)
            bar_y = WIN_HEIGHT - 80
            
            win.blit(boss_text, (bar_x, bar_y - 25))

            health_ratio = self.boss_hp / self.max_boss_hp
            current_health_width = int(bar_width * health_ratio)

            pygame.draw.rect(win, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(win, (230, 20, 20), (bar_x, bar_y, current_health_width, bar_height))
            pygame.draw.rect(win, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

    def reset(self):
        self.boss_active = False
        self.boss_hp = self.max_boss_hp
        self.boss_pos = [640 - 70, 0]
        self.boss_defeated = False
        self.boss_appeared = False
        self.boss_attacks = []
        self.gem_active = False
        self.gem_pos = None
        self.boss_move_phase = 1
        self.boss_hit = False
        self.stage_cleared = False