import pygame
import os
import math
import random
from M_title_stage_images.config import *

class Stage2Boss: 
    def __init__(self, res_manager):
        self.res = res_manager

        # 이미지 로드 (ResourceManager 활용)
        self.boss_image = self.res.load_image("bosses", "boss_stage2.png", size=(120, 120))
        self.boss_attack_images = self.res.load_image("boss_skilles", "boss_stage2_a.png", size=(40, 40))
        self.gem_image = self.res.load_image("items", "mob_Jewelry_2.png", size=(40, 40))
        
        # 보스 속성 초기화
        self.max_boss_hp = 20
        self.boss_hp = self.max_boss_hp
        self.boss_damage = 1
        self.boss_speed = 5
        self.boss_pos = [640 - 60, 0]
        self.boss_direction = [1, 1]  # 대각선 이동
        self.boss_active = False
        self.boss_attacks = []
        self.boss_last_attack_time = 0
        self.attack_interval = 1000  # 공격 간격
        self.gem_pos = None
        self.gem_active = False
        self.boss_defeated = False
        self.boss_appeared = False
        self.stage_cleared = False
        
        # 무적 및 깜박임 제어
        self.boss_hit = False
        self.invincible = False
        self.invincible_duration = 300  # 무적 지속 시간(ms)
        self.last_hit_time = 0

    def check_appear(self, seconds, current_level):
        """매 초 타이머와 레벨을 체크하여 보스 활성화"""
        if current_level == 2 and not self.boss_active and seconds >= 10 and not self.boss_appeared:
            self.boss_active = True
            self.boss_pos = [640 - 60, 20]
            self.boss_hp = self.max_boss_hp
            self.boss_appeared = True

    def move(self):
        """화면 벽에 튕기는 대각선 이동 알고리즘"""
        if not self.boss_active or self.boss_hp <= 0:
            return

        self.boss_pos[0] += self.boss_speed * self.boss_direction[0]
        self.boss_pos[1] += self.boss_speed * self.boss_direction[1]

        # 경계 감지 후 튕기기 및 사격
        if self.boss_pos[0] <= 0 or self.boss_pos[0] >= WIN_WIDTH - 120:
            self.boss_direction[0] *= -1
            self.attack()
            
        if self.boss_pos[1] <= 0 or self.boss_pos[1] >= WIN_HEIGHT - 300:
            self.boss_direction[1] *= -1
            self.attack()

    def attack(self):
        """체력이 깎일수록 무작위 위치로 많은 탄환 발사"""
        if not self.boss_active or self.boss_hp <= 0:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.boss_last_attack_time > self.attack_interval:
            self.boss_last_attack_time = current_time
            
            # 체력이 낮을수록 발사 횟수 증가
            num_shots = 1 + (self.max_boss_hp - self.boss_hp) // 5
            for _ in range(num_shots):
                target_x = random.randint(100, WIN_WIDTH - 100)
                target_y = random.randint(200, WIN_HEIGHT - 100)
                
                dx = target_x - self.boss_pos[0]
                dy = target_y - self.boss_pos[1]
                length = math.hypot(dx, dy)
                
                if length > 0:
                    direction = (dx / length, dy / length)
                    self.boss_attacks.append([self.boss_pos[0] + 60, self.boss_pos[1] + 60, direction])

    def update_attacks(self, player_rect, is_invincible=False):
        """보스 탄환 이동 및 플레이어 충돌 검사"""
        new_attacks = []
        player_hit = False

        for attack in self.boss_attacks:
            attack[0] += attack[2][0] * 8  # 탄속
            attack[1] += attack[2][1] * 8
            
            if -50 <= attack[0] <= WIN_WIDTH + 50 and -50 <= attack[1] <= WIN_HEIGHT + 50:
                bullet_rect = pygame.Rect(attack[0] - 20, attack[1] - 20, 40, 40)
                if not is_invincible and bullet_rect.colliderect(player_rect):
                    player_hit = True
                else:
                    new_attacks.append(attack)

        self.boss_attacks = new_attacks
        return self.boss_damage if player_hit else 0

    def check_hit(self, player_bullets_group):
        """main.py의 EnergyBall 스프라이트 그룹과 충돌 검사"""
        if not self.boss_active or self.boss_hp <= 0:
            return

        current_time = pygame.time.get_ticks()
        if self.invincible and (current_time - self.last_hit_time) < self.invincible_duration:
            return

        self.invincible = False
        boss_rect = pygame.Rect(self.boss_pos[0], self.boss_pos[1], 120, 120)

        for bullet in player_bullets_group:
            if boss_rect.colliderect(bullet.rect):
                bullet.kill()
                self.boss_hp -= 1
                self.invincible = True
                self.boss_hit = True
                self.last_hit_time = current_time
                
                if self.boss_hp <= 0:
                    self.boss_hp = 0
                    self.boss_active = False
                    self.gem_pos = [self.boss_pos[0] + 40, self.boss_pos[1] + 40]
                    self.gem_active = True
                    self.boss_defeated = True
                break

    def draw(self, win):
        """보스 피격 시 깜빡임 출력"""
        if self.boss_active and self.boss_hp > 0:
            current_time = pygame.time.get_ticks()
            if self.boss_hit:
                if current_time - self.last_hit_time >= self.invincible_duration:
                    self.boss_hit = False
                    win.blit(self.boss_image, self.boss_pos)
                else:
                    if (current_time // 80) % 2 == 0:
                        win.blit(self.boss_image, self.boss_pos)
            else:
                win.blit(self.boss_image, self.boss_pos)

    def draw_attacks(self, win):
        for attack in self.boss_attacks:
            win.blit(self.boss_attack_images, (attack[0] - 20, attack[1] - 20))

    def draw_health_bar(self, win, font):
        """하단 보스 전용 HP 게이지"""
        if self.boss_active and self.boss_hp > 0:
            boss_text = font.render("BOSS LV.2", True, (255, 255, 255))
            
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

    def draw_gem(self, win):
        if self.gem_active:
            win.blit(self.gem_image, self.gem_pos)

    def check_gem_collision(self, player_rect):
        if self.gem_active:
            gem_rect = pygame.Rect(self.gem_pos[0], self.gem_pos[1], 40, 40)
            if gem_rect.colliderect(player_rect):
                self.gem_active = False
                self.stage_cleared = True
                return True
        return False

    def reset(self):
        self.boss_active = False
        self.boss_hp = self.max_boss_hp
        self.boss_pos = [640 - 60, 0]
        self.boss_defeated = False
        self.boss_appeared = False
        self.boss_attacks = []
        self.gem_active = False
        self.gem_pos = None
        self.boss_hit = False
        self.invincible = False
        self.stage_cleared = False