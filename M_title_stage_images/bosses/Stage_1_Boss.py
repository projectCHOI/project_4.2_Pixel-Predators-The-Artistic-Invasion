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
        self.invincible_duration = 500  # 무적 시간 (밀리초)
        self.last_hit_time = 0
        self.gem_active = False

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

    def check_hit(self, attacks):
        current_time = pygame.time.get_ticks()
        
        # 무적 상태라면 공격을 무시
        if self.invincible and (current_time - self.last_hit_time) < self.invincible_duration:
            return
        
        for attack in attacks:
            attack_start, attack_end, thickness = attack
            if self.check_attack_collision(attack_start, attack_end, self.boss_pos, 120):
                self.boss_hp -= 1
                if self.boss_hp < 0:
                    self.boss_hp = 0
                self.invincible = True
                self.last_hit_time = current_time
                break

    def check_attack_collision(self, attack_start, attack_end, boss_pos, boss_size):
        ex, ey = boss_pos
        sx, sy = attack_start
        ex2, ey2 = ex + boss_size, ey + boss_size

        # 공격 선분과 보스 사각형의 충돌 검사
        rect = pygame.Rect(ex, ey, boss_size, boss_size)
        line = (sx, sy), attack_end
        return rect.clipline(line)

    def check_appear(self, seconds, current_level):
        if current_level == 1 and not self.boss_active and seconds >= 10 and not self.boss_appeared:
            self.boss_active = True
            self.boss_hp = self.max_boss_hp
            self.boss_appeared = True

    def reset(self):
        self.boss_active = False
        self.boss_hp = self.max_boss_hp
        self.boss_pos = [1200, 700]  # 다시 우측 하단에서 등장하도록 설정
        self.boss_appearing = True  # 다시 등장 애니메이션 활성화
        self.boss_defeated = False
        self.boss_appeared = False  # 보스 등장 여부 재설정
        self.boss_attacks = []
        self.boss_hit = False
        self.stage_cleared = False
        self.gem_active = False
        self.gem_pos = None
