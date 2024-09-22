#Stage_1_Boss
import random
import math
import pygame
import os

# BASE_DIR은 현재 파일의 디렉토리를 기준으로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_image(*path_parts, size=None):
    path = os.path.join(BASE_DIR, *path_parts)
    image = pygame.image.load(path)
    if size:
        image = pygame.transform.scale(image, size)
    return image

class Stage1Boss:
    def __init__(self):
        # 보스 이미지 및 속성 초기화
        self.boss_image = load_image("assets", "images", "bosses", "boss_stage1.png", size=(120, 120))
        self.boss_attack_images = {
            "down": load_image("assets", "images", "boss_skilles", "boss_stage1_a.png", size=(40, 40)),
            "up": load_image("assets", "images", "boss_skilles", "boss_stage1_b.png", size=(40, 40)),
            "right": load_image("assets", "images", "boss_skilles", "boss_stage1_c.png", size=(40, 40)),
            "left": load_image("assets", "images", "boss_skilles", "boss_stage1_d.png", size=(40, 40))
        }
        self.boss_appear_time = 30  # 보스 등장 시간 (초)
        self.boss_hp = 100
        self.boss_speed = 5
        self.boss_pos = [640 - 60, 0]  # 초기 보스 위치
        self.boss_direction_x = 1  # 좌우 이동 방향
        self.boss_direction_y = 1  # 위아래 이동 방향
        self.boss_active = False
        self.boss_defeated = False
        self.boss_move_phase = 1  # 1: 중앙 이동, 2: 좌우 이동, 3: 좌우+위아래 이동
        self.boss_hit = False
        self.boss_hit_start_time = 0
        self.boss_hit_duration = 500  # 보스가 점멸할 시간 (밀리초)
        self.boss_attacks = []
        self.boss_attack_cooldown = 1000  # 보스 공격 간격 (밀리초)
        self.boss_last_attack_time = 0
        self.gem_image = load_image("assets", "images", "items", "mob_Jewelry_1.png", size=(40, 40))
        self.gem_pos = None  # 보석 위치
        self.gem_active = False

    def check_appear(self, seconds):
        if not self.boss_active and seconds >= self.boss_appear_time and not self.boss_defeated:
            self.boss_active = True
            self.boss_pos = [640 - 60, 0]
            self.boss_hp = 100  # 보스 체력 초기화

    def move(self):
        if self.boss_move_phase == 1:  # 중앙으로 이동
            target_pos = [640 - 60, 360 - 60]
            direction = [target_pos[0] - self.boss_pos[0], target_pos[1] - self.boss_pos[1]]
            length = math.hypot(direction[0], direction[1])
            if length > self.boss_speed:
                direction = [direction[0] / length, direction[1] / length]
                self.boss_pos[0] += direction[0] * self.boss_speed
                self.boss_pos[1] += direction[1] * self.boss_speed
            else:
                self.boss_pos = target_pos
                self.boss_move_phase = 2

        elif self.boss_move_phase == 2:  # 좌우 이동
            if self.boss_hp > 50:
                self.boss_pos[0] += self.boss_speed * self.boss_direction_x
                if self.boss_pos[0] <= 60 or self.boss_pos[0] >= 1280 - 180:
                    self.boss_direction_x *= -1  # 방향 전환
            else:
                self.boss_move_phase = 3

        elif self.boss_move_phase == 3:  # 좌우+위아래 이동
            self.boss_pos[0] += self.boss_speed * self.boss_direction_x
            self.boss_pos[1] += self.boss_speed * self.boss_direction_y
            if self.boss_pos[0] <= 60 or self.boss_pos[0] >= 1280 - 180:
                self.boss_direction_x *= -1  # 좌우 방향 전환
            if self.boss_pos[1] <= 60 or self.boss_pos[1] >= 720 - 180:
                self.boss_direction_y *= -1  # 위아래 방향 전환

    def attack(self):
        if pygame.time.get_ticks() - self.boss_last_attack_time > self.boss_attack_cooldown:
            self.boss_last_attack_time = pygame.time.get_ticks()
            possible_directions = []

            # 보스의 체력에 따른 공격 방향 설정
            if self.boss_hp > 80:
                possible_directions = ["down"]
            elif self.boss_hp > 60:
                possible_directions = ["down", "up"]
            elif self.boss_hp > 40:
                possible_directions = ["down", "up", "right"]
            elif self.boss_hp > 0:
                possible_directions = ["down", "up", "right", "left"]

            if possible_directions:
                attack_direction = random.choice(possible_directions)
                attack_start_pos = self.get_attack_start_pos(attack_direction)
                self.boss_attacks.append([attack_start_pos[0], attack_start_pos[1], attack_direction])

    def get_attack_start_pos(self, direction):
        if direction == "down":
            return [self.boss_pos[0] + 60, self.boss_pos[1] + 120]
        elif direction == "up":
            return [self.boss_pos[0] + 60, self.boss_pos[1]]
        elif direction == "right":
            return [self.boss_pos[0] + 120, self.boss_pos[1] + 60]
        elif direction == "left":
            return [self.boss_pos[0], self.boss_pos[1] + 60]

    def draw(self, win):
        if self.boss_hit:
            current_time = pygame.time.get_ticks()
            if (current_time - self.boss_hit_start_time) // 100 % 2 == 0:
                win.blit(self.boss_image, self.boss_pos)
        else:
            win.blit(self.boss_image, self.boss_pos)

    def draw_attacks(self, win):
        for attack in self.boss_attacks:
            win.blit(self.boss_attack_images[attack[2]], (attack[0], attack[1]))

    def update_attacks(self, player_pos):
        new_boss_attacks = []
        for attack in self.boss_attacks:
            if attack[2] == "down":
                attack[1] += 10
            elif attack[2] == "up":
                attack[1] -= 10
            elif attack[2] == "right":
                attack[0] += 10
            elif attack[2] == "left":
                attack[0] -= 10

            if 0 <= attack[0] <= 1280 and 0 <= attack[1] <= 720:
                if self.check_energy_ball_collision((attack[0], attack[1]), player_pos):
                    return 2  # 플레이어에게 맞음
                else:
                    new_boss_attacks.append(attack)

        self.boss_attacks = new_boss_attacks

    def check_hit(self, attacks):
        for attack in attacks:
            attack_start, attack_end, thickness = attack
            if self.check_attack_collision(attack_start, attack_end, self.boss_pos, 120):
                self.boss_hp -= 1  # 공격력 적용
                self.boss_hit = True  # 보스가 공격을 받았음을 표시
                self.boss_hit_start_time = pygame.time.get_ticks()  # 점멸 시작 시간 기록
                if self.boss_hp <= 0:
                    self.boss_active = False
                    self.boss_hp = 0  # 보스 체력을 0으로 유지
                    self.gem_pos = [self.boss_pos[0] + 40, self.boss_pos[1] + 40]  # 보석 위치 설정
                    self.gem_active = True
                    self.boss_defeated = True  # 보스가 제거된 것으로 표시
                break  # 한 번에 하나의 공격만 처리

    def reset(self):
        self.boss_active = False
        self.boss_hp = 100
        self.boss_pos = [640 - 60, 0]
        self.boss_defeated = False
        self.boss_attacks = []
        self.gem_active = False
        self.gem_pos = None

    def check_energy_ball_collision(self, ball_pos, player_pos):
        bx, by = ball_pos
        px, py = player_pos
        player_width, player_height = 40, 40  # 플레이어 크기
        if px < bx < px + player_width and py < by < py + player_height:
            return True
        return False

    def check_attack_collision(self, attack_start, attack_end, boss_pos, boss_size):
        ex, ey = boss_pos
        sx, sy = attack_start
        ex2, ey2 = ex + boss_size, ey + boss_size

        # 공격 선분과 보스 사각형의 충돌 검사
        # 선분과 사각형의 충돌 여부를 판별하는 알고리즘을 사용합니다.
        rect = pygame.Rect(ex, ey, boss_size, boss_size)
        line = (sx, sy), attack_end
        if rect.clipline(line):
            return True
        return False
