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
        self.boss_image = load_image("bosses", "boss_stage2.png", size=(240, 240))
        self.boss_attack_images = {
            "down": load_image("boss_skilles", "boss_stage2_a.png", size=(40, 40)),
            "up": load_image("boss_skilles", "boss_stage2_b.png", size=(40, 40)),
            "right": load_image("boss_skilles", "boss_stage2_c.png", size=(40, 40)),
            "left": load_image("boss_skilles", "boss_stage2_d.png", size=(40, 40))
        }
        self.gem_image = load_image("items", "mob_Jewelry_2.png", size=(40, 40))