import pygame
import os
import math

# 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_IMAGE_PATH = os.path.join(BASE_DIR, "assets", "images")

def load_image(*path_parts, size=None):
    path = os.path.join(BASE_IMAGE_PATH, *path_parts)
    image = pygame.image.load(path).convert_alpha()
    if size:
        image = pygame.transform.scale(image, size)
    return image

class Stage9Boss:
    def __init__(self):
        # 이미지 로드
        self.boss_image = load_image("bosses", "boss_stage9_S.png", size=(180, 180))
        self.minion_attack_image = load_image("bosses", "boss_stage9_N.png", size=(60, 60))
        self.attack_images = {
            "phase1": load_image("boss_skilles", "boss_stage9_a.png", size=(40, 40)),
            "phase2": load_image("boss_skilles", "boss_stage9_b.png", size=(40, 40)),
            "phase3": load_image("boss_skilles", "boss_stage9_c.png", size=(40, 40)),
            "phase4": load_image("boss_skilles", "boss_stage9_d.png", size=(40, 40))
        }
        self.gem_image = load_image("items", "mob_Jewelry_9.png", size=(40, 40))

        # 기본 속성 설정
        self.boss_pos = [1400, 300]  # 화면 우측 바깥에서 등장
        self.boss_hp = 100
        self.max_boss_hp = 100
        self.boss_active = False
        self.boss_appeared = False
        self.boss_defeated = False
        self.stage_cleared = False

        # 공격 관련
        self.boss_attacks = []
        self.boss_phase = 1
        self.attack_cooldown = 2000
        self.last_attack_time = 0

        # 보석
        self.gem_active = False
        self.gem_pos = None

        # 피격 관련
        self.boss_hit = False
        self.boss_hit_start_time = 0
        self.boss_invincible_duration = 500

    def draw(self, win):
        win.blit(self.boss_image, self.boss_pos)

    def draw_attacks(self, win):
        image = self.attack_images[f"phase{self.boss_phase}"]
        for attack in self.boss_attacks:
            rotated = pygame.transform.rotate(image, attack.get("angle", 0))
            rect = rotated.get_rect(center=attack["pos"])
            win.blit(rotated, rect)

    def draw_gem(self, win):
        if self.gem_active:
            win.blit(self.gem_image, self.gem_pos)

    def get_current_phase(self):
        if self.boss_hp > 75:
            return 1
        elif self.boss_hp > 50:
            return 2
        elif self.boss_hp > 25:
            return 3
        else:
            return 4

    def update_phase(self):
        self.boss_phase = self.get_current_phase()

    def reset(self):
        self.__init__()
