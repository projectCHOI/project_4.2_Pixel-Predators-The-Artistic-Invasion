import pygame
import os
import math
import random

# BASE_DIR 설정: 현재 파일의 부모 디렉토리 기준으로 설정
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

class Stage3Boss:
    def __init__(self):
        # 이미지 로드
        self.boss_image = load_image("bosses", "boss_stage3.png", size=(240, 240))
        self.boss_attack_images = {
            "down": load_image("boss_skilles", "boss_stage3_a.png", size=(40, 40)),
            "up": load_image("boss_skilles", "boss_stage3_b.png", size=(40, 40)),
            "right": load_image("boss_skilles", "boss_stage3_c.png", size=(40, 40)),
            "left": load_image("boss_skilles", "boss_stage3_d.png", size=(40, 40))
        }
        self.gem_image = load_image("items", "mob_Jewelry_3.png", size=(40, 40))
        # 보스 속성 초기화
        self.max_boss_hp = 20
        self.boss_hp = self.max_boss_hp
        self.boss_damage = 2
        self.boss_speed = 7
        self.boss_pos = [640 - 120, 0]
        self.boss_direction = [1, 1]  # 대각선 이동
        self.boss_active = False
        self.boss_attacks = []
        self.boss_last_attack_time = 0
        self.attack_interval = 1000  # 방향 전환 시마다 공격
        self.gem_pos = None
        self.gem_active = False
        self.stage_cleared = False
        self.invincible = False
        self.invincible_duration = 500  # 무적 상태 지속 시간 (밀리초)
        self.last_hit_time = 0

    def check_appear(self, seconds, current_level):
        if current_level == 3 and not self.boss_active and seconds >= 20:  # 예시: 20초 이후 등장
            self.boss_active = True
            self.boss_pos = [640 - 120, 0]

    def move(self):
        # 화면에서 바운스하는 대각선 이동
        self.boss_pos[0] += self.boss_speed * self.boss_direction[0]
        self.boss_pos[1] += self.boss_speed * self.boss_direction[1]

        # 경계에 닿으면 방향 전환 및 공격
        if self.boss_pos[0] <= 0 or self.boss_pos[0] >= 1280 - 240:
            self.boss_direction[0] *= -1
            self.attack()  # 방향 전환 시 공격
        if self.boss_pos[1] <= 0 or self.boss_pos[1] >= 720 - 240:
            self.boss_direction[1] *= -1
            self.attack()  # 방향 전환 시 공격

    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.boss_last_attack_time > self.attack_interval:
            self.boss_last_attack_time = current_time

            # 플레이어를 향해 발사할 단일 타겟 샷 수 결정
            num_shots = 1 + (self.max_boss_hp - self.boss_hp) // 5  # 체력 감소 시 공격 횟수 증가
            for _ in range(num_shots):
                target_x, target_y = random.randint(100, 1180), random.randint(100, 620)  # 플레이어의 예측 위치 설정
                dx, dy = target_x - self.boss_pos[0], target_y - self.boss_pos[1]
                length = math.hypot(dx, dy)
                if length > 0:
                    direction = (dx / length, dy / length)
                    self.boss_attacks.append([self.boss_pos[0] + 120, self.boss_pos[1] + 120, direction])

    def update_attacks(self, player_pos):
        new_attacks = []
        player_hit = False
        for attack in self.boss_attacks:
            attack[0] += attack[2][0] * 10
            attack[1] += attack[2][1] * 10
            if 0 <= attack[0] <= 1280 and 0 <= attack[1] <= 720:
                if self.check_energy_ball_collision((attack[0], attack[1]), player_pos):
                    player_hit = True
                else:
                    new_attacks.append(attack)
        self.boss_attacks = new_attacks
        return player_hit

    def check_hit(self, attacks):
        current_time = pygame.time.get_ticks()
        if self.invincible and current_time - self.last_hit_time < self.invincible_duration:
            return

        for attack in attacks:
            attack_start, attack_end, thickness = attack
            if self.check_attack_collision(attack_start, attack_end, self.boss_pos, 240):
                self.boss_hp -= 1  # 데미지 적용
                self.invincible = True
                self.last_hit_time = current_time
                if self.boss_hp <= 0:
                    self.boss_active = False
                    self.gem_pos = [self.boss_pos[0] + 95, self.boss_pos[1] + 95]
                    self.gem_active = True
                    self.stage_cleared = True
                break

    def draw(self, win):
        win.blit(self.boss_image, self.boss_pos)

    def draw_attacks(self, win):
        for attack in self.boss_attacks:
            win.blit(self.boss_attack_images["down"], (attack[0], attack[1]))

    def check_energy_ball_collision(self, ball_pos, player_pos):
        bx, by = ball_pos
        px, py = player_pos
        player_width, player_height = 50, 50
        return px < bx < px + player_width and py < by < py + player_height

    def check_attack_collision(self, attack_start, attack_end, boss_pos, boss_size):
        ex, ey = boss_pos
        sx, sy = attack_start
        ex2, ey2 = ex + boss_size, ey + boss_size

        rect = pygame.Rect(ex, ey, boss_size, boss_size)
        line = (sx, sy), attack_end
        return rect.clipline(line)

    def reset(self):
        self.boss_active = False
        self.boss_hp = self.max_boss_hp
        self.boss_pos = [640 - 120, 0]
        self.boss_direction = [1, 1]
        self.boss_attacks = []
        self.gem_active = False
        self.stage_cleared = False
        self.invincible = False
