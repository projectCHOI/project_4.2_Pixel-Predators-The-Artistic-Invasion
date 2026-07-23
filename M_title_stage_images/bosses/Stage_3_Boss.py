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

    def check_appear(self, seconds, current_level):
        """매 초 타이머와 레벨을 체크하여 보스 활성화"""
        if current_level == 3 and not self.boss_active and seconds >= 10 and not self.boss_appeared:
            self.boss_active = True
            self.boss_pos = [640 - 60, 150]
            self.boss_hp = self.max_boss_hp
            self.boss_appeared = True
            self.last_teleport_time = pygame.time.get_ticks()

    def move(self):
        """4초마다 랜덤 위치로 텔레포트"""
        if not self.boss_active or self.boss_hp <= 0:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_teleport_time > self.teleport_interval:
            self.boss_pos = [
                random.randint(50, WIN_WIDTH - 170),
                random.randint(50, WIN_HEIGHT - 350)
            ]
            self.last_teleport_time = current_time
            self.attack()

    def attack(self):
        """체력이 떨어질수록 360도 전방위 방사 공격 개수 증가"""
        if not self.boss_active or self.boss_hp <= 0:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.boss_last_attack_time > self.attack_interval:
            self.boss_last_attack_time = current_time
            num_shots = 3 + (self.max_boss_hp - self.boss_hp) // 3
            
            for _ in range(num_shots):
                angle = random.uniform(0, 360)
                radian = math.radians(angle)
                dx = math.cos(radian) * 6
                dy = math.sin(radian) * 6
                attack_type = self.get_attack_type()
                
                # 탄환 시작 위치: 보스 중앙
                start_x = self.boss_pos[0] + 60
                start_y = self.boss_pos[1] + 60
                self.boss_attacks.append([[start_x, start_y], [dx, dy], angle, attack_type])

    def get_attack_type(self):
        health_ratio = self.boss_hp / self.max_boss_hp
        if health_ratio > 0.6:
            return "high"
        elif health_ratio > 0.3:
            return "medium"
        else:
            return "low"

    def update_attacks(self, player_rect, is_invincible=False):
        """탄환 이동 및 플레이어 충돌 검사"""
        new_attacks = []
        player_hit = False

        for attack in self.boss_attacks:
            attack[0][0] += attack[1][0]
            attack[0][1] += attack[1][1]

            bx, by = attack[0]
            if -50 <= bx <= WIN_WIDTH + 50 and -50 <= by <= WIN_HEIGHT + 50:
                bullet_rect = pygame.Rect(bx - 20, by - 20, 40, 40)
                if not is_invincible and bullet_rect.colliderect(player_rect):
                    player_hit = True
                else:
                    new_attacks.append(attack)

        self.boss_attacks = new_attacks
        return self.boss_damage if player_hit else 0

    def check_hit(self, player_bullets_group):
        """main.py의 EnergyBall 탄환 그룹과의 충돌 검사"""
        if not self.boss_active or self.boss_hp <= 0:
            return

        current_time = pygame.time.get_ticks()
        if self.boss_hit and (current_time - self.boss_hit_start_time) < self.invincible_duration:
            return

        self.boss_hit = False
        boss_rect = pygame.Rect(self.boss_pos[0], self.boss_pos[1], 120, 120)

        for bullet in player_bullets_group:
            if boss_rect.colliderect(bullet.rect):
                bullet.kill()
                self.boss_hp -= 1
                self.boss_hit = True
                self.boss_hit_start_time = current_time

                if self.boss_hp <= 0:
                    self.boss_hp = 0
                    self.boss_active = False
                    self.gem_pos = [self.boss_pos[0] + 40, self.boss_pos[1] + 40]
                    self.gem_active = True
                    self.boss_defeated = True
                break

    def draw(self, win):
        """보스 렌더링 및 피격 시 깜빡임"""
        if self.boss_active and self.boss_hp > 0:
            current_time = pygame.time.get_ticks()
            if self.boss_hit:
                if current_time - self.boss_hit_start_time >= self.invincible_duration:
                    self.boss_hit = False
                    win.blit(self.boss_image, self.boss_pos)
                else:
                    if (current_time // 80) % 2 == 0:
                        win.blit(self.boss_image, self.boss_pos)
            else:
                win.blit(self.boss_image, self.boss_pos)

    def draw_attacks(self, win):
        """보스 탄환 드로잉 (각도 회전 적용)"""
        for attack in self.boss_attacks:
            angle = -attack[2] + 90
            attack_type = attack[3]
            img = self.boss_attack_images.get(attack_type, self.boss_attack_images["low"])
            rotated_image = pygame.transform.rotate(img, angle)
            rect = rotated_image.get_rect(center=attack[0])
            win.blit(rotated_image, rect)

    def draw_gem(self, win):
        if self.gem_active:
            win.blit(self.gem_image, self.gem_pos)
            
    def draw_health_bar(self, win, font):
        """보스 체력바 UI (하단 고정)"""
        if self.boss_active and self.boss_hp > 0:
            boss_text = font.render("BOSS LV.3", True, (255, 255, 255))
            
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
        self.boss_pos = [640 - 60, 200]
        self.boss_defeated = False
        self.boss_appeared = False
        self.boss_attacks = []
        self.gem_active = False
        self.gem_pos = None
        self.boss_hit = False
        self.stage_cleared = False
