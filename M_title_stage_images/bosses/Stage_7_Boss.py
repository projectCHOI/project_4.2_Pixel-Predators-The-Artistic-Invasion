import pygame
import os
import math
import random

# BASE_DIR 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_IMAGE_PATH = os.path.join(BASE_DIR, "assets", "images")

def load_image(*path_parts, size=None):
    path = os.path.join(BASE_IMAGE_PATH, *path_parts)
    try:
        image = pygame.image.load(path).convert_alpha()
    except pygame.error as e:
        raise SystemExit(f"Cannot load image: {path}\n{e}")
    if size:
        image = pygame.transform.scale(image, size)
    return image

class Stage7Boss:
    def __init__(self):
        self.boss_image = load_image("bosses", "boss_stage7.png", size=(120, 120))
        self.boss_attack_image1 = load_image("boss_skilles", "boss_stage7_a.png", size=(40, 40))
        self.boss_attack_image2 = load_image("boss_skilles", "boss_stage7_b.png", size=(40, 40))
        self.gem_image = load_image("items", "mob_Jewelry_7.png", size=(40, 40))

        # 보스 속성 초기화
        self.boss_appear_time = 10
        self.max_boss_hp = 10
        self.boss_hp = self.max_boss_hp
        self.boss_damage = 2
        self.boss_speed = 5
        self.boss_pos = [640 - 60, 0]
        self.boss_active = False
        self.boss_defeated = False
        self.boss_appeared = False
        self.boss_attacks = []
        self.boss_attack_cooldown = 1000
        self.boss_last_attack_time = 0
        self.gem_active = False
        self.stage_cleared = False
        self.move_start_time = pygame.time.get_ticks()
        self.move_phase = 0
        self.move_positions = [[640, 100], [213, 200], [640, 300], [1066, 400], [640, 500], [213, 600]]
        self.boss_invincible_duration = 500
        self.boss_hit_duration = 100

    def check_appear(self, seconds, current_level):
        if current_level == 7 and not self.boss_active and seconds >= self.boss_appear_time and not self.boss_appeared:
            self.boss_active = True
            self.boss_pos = [640 - 60, 0]
            self.boss_hp = self.max_boss_hp
            self.boss_appeared = True

    def move(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.move_start_time) / 1000
        move_duration = 10

        phase_index = self.move_phase % len(self.move_positions)
        next_phase_index = (self.move_phase + 1) % len(self.move_positions)
        start_pos = self.move_positions[phase_index]
        end_pos = self.move_positions[next_phase_index]

        if elapsed_time < move_duration:
            t = elapsed_time / move_duration
            self.boss_pos[0] = start_pos[0] + (end_pos[0] - start_pos[0]) * t
            self.boss_pos[1] = start_pos[1] + (end_pos[1] - start_pos[1]) * t
        else:
            self.move_phase += 1
            self.move_start_time = current_time

    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.boss_last_attack_time > self.boss_attack_cooldown:
            self.boss_last_attack_time = current_time
            attack_count = 10 + (self.max_boss_hp - self.boss_hp)
            attack_start_pos = [self.boss_pos[0] + 60, self.boss_pos[1] + 60]
            for i in range(attack_count):
                angle = random.uniform(0, 360)
                radian = math.radians(angle)
                dx = math.cos(radian) * 3
                dy = math.sin(radian) * 3
                attack_image = self.boss_attack_image1 if dx < 0 else self.boss_attack_image2
                self.boss_attacks.append({'pos': [attack_start_pos[0], attack_start_pos[1]], 'dir': [dx, dy], 'angle': angle, 'image': attack_image})

    def update_attacks(self, player_pos):
        new_boss_attacks = []
        player_hit = False
        for attack in self.boss_attacks:
            attack['pos'][0] += attack['dir'][0]
            attack['pos'][1] += attack['dir'][1]
            bx, by = attack['pos']
            if 0 <= bx <= 1280 and 0 <= by <= 720:
                if self.check_energy_ball_collision((bx, by), player_pos):
                    player_hit = True
                else:
                    new_boss_attacks.append(attack)
        self.boss_attacks = new_boss_attacks
        return player_hit

    def check_energy_ball_collision(self, ball_pos, player_pos):
        bx, by = ball_pos
        px, py = player_pos
        return px < bx < px + 50 and py < by < py + 50

    def draw_health_bar(self, win, font):
        if self.boss_active and self.boss_hp > 0:
            boss_text = font.render("BOSS", True, (255, 255, 255))
            win.blit(boss_text, (10, 680))
            health_ratio = self.boss_hp / self.max_boss_hp
            pygame.draw.rect(win, (50, 50, 50), (80, 680, 200, 30))
            pygame.draw.rect(win, (210, 20, 4), (80, 680, int(200 * health_ratio), 30))
            pygame.draw.rect(win, (255, 255, 255), (80, 680, 200, 30), 2)
    
    def check_hit(self, attacks):
        for attack in attacks:
            if self.boss_pos[0] < attack[0] < self.boss_pos[0] + 120 and \
            self.boss_pos[1] < attack[1] < self.boss_pos[1] + 120:
                self.boss_hp -= 1  # 보스 체력 감소
                if self.boss_hp <= 0:
                    self.boss_defeated = True
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
        self.stage_cleared = False
        self.boss_move_phase = 1
        self.boss_hit = False

    def check_energy_ball_collision(self, ball_pos, player_pos):
        bx, by = ball_pos
        px, py = player_pos
        player_width, player_height = 50, 50  # 플레이어 크기
        if px < bx < px + player_width and py < by < py + player_height:
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
