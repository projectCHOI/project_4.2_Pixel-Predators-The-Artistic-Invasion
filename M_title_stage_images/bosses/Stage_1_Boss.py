import pygame
import os
import random

# BASE_DIR 설정: 현재 작업 디렉토리를 기준으로 설정
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
        # 이미지 로드 (보스 이미지만 유지)
        self.boss_image = load_image("bosses", "boss_stage5.png", size=(120, 120))
        
        # 보스 속성 초기화
        self.max_boss_hp = 15
        self.boss_hp = self.max_boss_hp
        self.boss_pos = [1280 - 120, 720]  # 화면 우측 하단에서 시작
        self.boss_active = False
        self.boss_appeared = False
        self.invincible = False
        self.invincible_duration = 500
        self.last_hit_time = 0
        self.gem_active = False

    def check_appear(self, seconds, current_level):
        if current_level == 1 and not self.boss_active and seconds >= 10 and not self.boss_appeared:
            self.boss_active = True
            self.boss_hp = self.max_boss_hp
            self.boss_appeared = True

    def move(self):
        # 천천히 위로 이동하여 등장
        if self.boss_pos[1] > 360:  # 목표 위치까지 이동
            self.boss_pos[1] -= 1

    def draw(self, win):
        if self.boss_hp > 0:
            win.blit(self.boss_image, self.boss_pos)
    
    def check_hit(self, attacks):
        current_time = pygame.time.get_ticks()
        if self.invincible and (current_time - self.last_hit_time) < self.invincible_duration:
            return  # 무적 상태일 경우 공격 무시
        
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
    
    def reset(self):
        self.boss_active = False
        self.boss_hp = self.max_boss_hp
        self.boss_pos = [1280 - 120, 720]  # 화면 우측 하단에서 시작
        self.boss_appeared = False
        self.invincible = False
