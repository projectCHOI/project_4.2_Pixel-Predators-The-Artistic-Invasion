import pygame
import os
import random
import math

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

class Stage1Boss:
    def __init__(self):
        # 보스 속성 초기화
        self.boss_image = load_image("bosses", "boss_stage5.png", size=(120, 120))
        self.max_boss_hp = 15
        self.boss_hp = self.max_boss_hp
        self.boss_pos = [1280 - 120, 720]  # 보스 초기 위치
        self.boss_active = False
        self.boss_appeared = False
        self.invincible = False
        self.invincible_duration = 500
        self.last_hit_time = 0
        self.gem_active = False
        self.bullets = []  # 보스가 발사하는 탄환 리스트
        self.units = []  # 소환된 유닛 리스트

    def reset(self):
        self.boss_active = False
        self.boss_hp = self.max_boss_hp
        self.boss_pos = [1280 - 120, 720]
        self.boss_appeared = False
        self.invincible = False
        self.bullets.clear()  # 보스 공격 초기화
        self.units.clear()  # 소환된 유닛 초기화

    def check_appear(self, seconds, current_level):
        if current_level == 1 and not self.boss_active and seconds >= 10 and not self.boss_appeared:
            self.boss_active = True
            self.boss_hp = self.max_boss_hp
            self.boss_appeared = True

        # 공격 관련 속성
        self.bullets = []
        self.units = []
        self.last_summon_time = 0

        # 에너지 볼 이미지
        self.energy_balls = {
            "a": {
                "image": load_image("boss_skilles", "boss_stage9_a.png", size=(40, 40)),
                "speed": 5
            },
            "b": {
                "image": load_image("boss_skilles", "boss_stage9_b.png", size=(50, 50)),
                "speed": 6
            },
            "c": {
                "image": load_image("boss_skilles", "boss_stage9_c.png", size=(60, 60)),
                "speed": 7
            }
        }

        # 유닛 관련 속성
        self.unit_image = load_image("bosses", "boss_stage10.png", size=(50, 50))
        self.unit_attack_image = load_image("boss_skilles", "boss_stage10_a.png", size=(30, 30))
        self.unit_attack_speed = 5
        self.unit_attack_interval = 500  # 0.5초 간격 공격

    def attack(self, player_pos):
        if not self.boss_active:
            return
        
        # 랜덤한 에너지 볼 선택
        attack_type = random.choice(["a", "b", "c"])
        attack_data = self.energy_balls[attack_type]

        # 보스 중앙에서 발사
        bullet_x = self.boss_pos[0] + 60  # 보스 중앙
        bullet_y = self.boss_pos[1] + 120
        target_x, target_y = player_pos

        # 방향 계산
        angle = math.atan2(target_y - bullet_y, target_x - bullet_x)
        speed_x = math.cos(angle) * attack_data["speed"]
        speed_y = math.sin(angle) * attack_data["speed"]

        # 탄환 추가
        self.bullets.append({
            "x": bullet_x, "y": bullet_y,
            "speed_x": speed_x, "speed_y": speed_y,
            "image": attack_data["image"]
        })
    
    def summon_units(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_summon_time < 6000:
            return  # 6초가 지나지 않았다면 소환하지 않음

        self.last_summon_time = current_time
        unit_positions = []

        while len(unit_positions) < 4:
            # 랜덤한 위치 생성
            unit_x = random.randint(100, 1180)
            unit_y = random.randint(100, 600)

            # 겹치는지 확인
            overlap = any(math.dist((unit_x, unit_y), pos) < 50 for pos in unit_positions)
            if not overlap:
                unit_positions.append((unit_x, unit_y))

        # 유닛 리스트에 추가
        for pos in unit_positions:
            self.units.append({
                "x": pos[0], "y": pos[1],
                "attacks": [],  # 유닛이 발사하는 탄환 리스트
                "last_attack_time": pygame.time.get_ticks()
            })

    def update_units(self, player_pos):
        current_time = pygame.time.get_ticks()
        for unit in self.units:
            if current_time - unit["last_attack_time"] >= self.unit_attack_interval:
                unit["last_attack_time"] = current_time
                unit_x, unit_y = unit["x"], unit["y"]
                target_x, target_y = player_pos

                # 방향 계산
                angle = math.atan2(target_y - unit_y, target_x - unit_x)
                speed_x = math.cos(angle) * self.unit_attack_speed
                speed_y = math.sin(angle) * self.unit_attack_speed

                # 유닛 탄환 추가
                unit["attacks"].append({
                    "x": unit_x, "y": unit_y,
                    "speed_x": speed_x, "speed_y": speed_y,
                    "image": self.unit_attack_image
                })

        # 보스 등장
    def move(self):
        if self.boss_pos[1] > 360:
            self.boss_pos[1] -= 1

    def draw(self, win):
        if self.boss_hp > 0:
            win.blit(self.boss_image, self.boss_pos)
        
        # 보스 탄환 그리기
        for bullet in self.bullets:
            bullet["x"] += bullet["speed_x"]
            bullet["y"] += bullet["speed_y"]
            win.blit(bullet["image"], (bullet["x"], bullet["y"]))

        # 유닛 그리기
        for unit in self.units:
            win.blit(self.unit_image, (unit["x"], unit["y"]))
            for attack in unit["attacks"]:
                attack["x"] += attack["speed_x"]
                attack["y"] += attack["speed_y"]
                win.blit(attack["image"], (attack["x"], attack["y"]))

    def reset(self):
        self.boss_active = False
        self.boss_hp = self.max_boss_hp
        self.boss_pos = [1280 - 120, 720]
        self.boss_appeared = False
        self.invincible = False
        self.bullets.clear()
        self.units.clear()
