import pygame
import os
import math
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_IMAGE_PATH = os.path.join(BASE_DIR, "assets", "images")

def load_image(*path_parts, size=None):
    path = os.path.join(BASE_IMAGE_PATH, *path_parts)
    try:
        image = pygame.image.load(path).convert_alpha()
    except pygame.error as e:
        raise SystemExit(f"Cannot load image: {path}\\n{e}")
    if size:
        image = pygame.transform.scale(image, size)
    return image

class Stage3Boss:
    def __init__(self):
        self.boss_image = load_image("bosses", "boss_stage3.png", size=(240, 240))
        self.boss_attack_images = {
            "down": load_image("boss_skilles", "boss_stage3_a.png", size=(40, 40)),
            "up": load_image("boss_skilles", "boss_stage3_b.png", size=(40, 40)),
            "right": load_image("boss_skilles", "boss_stage3_c.png", size=(40, 40)),
            "left": load_image("boss_skilles", "boss_stage3_d.png", size=(40, 40))
        }
        self.gem_image = load_image("items", "mob_Jewelry_3.png", size=(40, 40))
        
        self.boss_hp = self.max_boss_hp = 20
        self.boss_damage = 2
        self.boss_speed = 7
        self.boss_pos = [640 - 60, 360 - 60]
        self.boss_direction_x, self.boss_direction_y = 1, 1
        self.boss_active = self.boss_defeated = self.boss_appeared = self.gem_active = False
        self.boss_attacks = []
        self.boss_last_attack_time = pygame.time.get_ticks()
        self.stage_cleared = False
        self.boss_attack_cooldown = 1000
        self.direction_change_trigger = False

    def move(self):
        self.boss_pos[0] += self.boss_speed * self.boss_direction_x
        self.boss_pos[1] += self.boss_speed * self.boss_direction_y

        # Bounce off edges and trigger direction change for attack
        if self.boss_pos[0] <= 0 or self.boss_pos[0] >= 1280 - 120:
            self.boss_direction_x *= -1
            self.direction_change_trigger = True
        if self.boss_pos[1] <= 0 or self.boss_pos[1] >= 720 - 120:
            self.boss_direction_y *= -1
            self.direction_change_trigger = True

    def attack(self, player_pos):
        current_time = pygame.time.get_ticks()
        if self.direction_change_trigger and current_time - self.boss_last_attack_time > self.boss_attack_cooldown:
            self.boss_last_attack_time = current_time
            self.direction_change_trigger = False
            
            # Increase attack count as health decreases
            attack_count = 1 + (self.max_boss_hp - self.boss_hp) // (self.max_boss_hp // 4)
            for _ in range(attack_count):
                attack_direction = [player_pos[0] - self.boss_pos[0], player_pos[1] - self.boss_pos[1]]
                length = math.hypot(attack_direction[0], attack_direction[1])
                if length != 0:
                    attack_direction = [attack_direction[0] / length, attack_direction[1] / length]
                    self.boss_attacks.append([self.boss_pos[0] + 120, self.boss_pos[1] + 120, attack_direction])

    def update_attacks(self, player_pos):
        new_boss_attacks = []
        player_hit = False
        for attack in self.boss_attacks:
            attack[0] += attack[2][0] * 10
            attack[1] += attack[2][1] * 10
            if 0 <= attack[0] <= 1280 and 0 <= attack[1] <= 720:
                if self.check_energy_ball_collision((attack[0], attack[1]), player_pos):
                    player_hit = True
                else:
                    new_boss_attacks.append(attack)
        self.boss_attacks = new_boss_attacks
        return player_hit

    def check_energy_ball_collision(self, ball_pos, player_pos):
        bx, by = ball_pos
        px, py = player_pos
        player_width, player_height = 50, 50
        return px < bx < px + player_width and py < by < py + player_height
        return True
        return False

    def check_attack_collision(self, attack_start, attack_end, boss_pos, boss_size):
        ex, ey = boss_pos
        sx, sy = attack_start
        ex2, ey2 = ex + boss_size, ey + boss_size

        # 공격 선분과 보스 사각형의 충돌 검사
        rect = pygame.Rect(ex, ey, boss_size, boss_size)
        line = (sx, sy), attack_end
        if rect.clipline(line):
            return True
        return False
