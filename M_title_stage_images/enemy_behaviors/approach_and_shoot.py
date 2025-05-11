import random
import os
import pygame
import math

# 기본 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_IMAGE_PATH = os.path.join(BASE_DIR, "assets", "images")

def load_image(*path_parts, size=None):
    path = os.path.join(BASE_IMAGE_PATH, *path_parts)
    try:
        img = pygame.image.load(path).convert_alpha()
    except pygame.error as e:
        raise SystemExit(f"Cannot load image: {path}\n{e}")
    if size:
        img = pygame.transform.scale(img, size)
    return img

# 이미지 로딩
SIZE = 20
enemy_image_up    = load_image("enemies", "mob_enemy_Relentless Charger_1.png", size=(SIZE, SIZE))
enemy_image_down  = load_image("enemies", "mob_enemy_Relentless Charger_2.png", size=(SIZE, SIZE))
enemy_image_left  = load_image("enemies", "mob_enemy_Relentless Charger_3.png", size=(SIZE, SIZE))
enemy_image_right = load_image("enemies", "mob_enemy_Relentless Charger_4.png", size=(SIZE, SIZE))

# 적 생성 함수
def generate(level, win_width, win_height):

    enemies = []

    speed = random.randint(10, 18)
    num_enemies = random.randint(6, 26)

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for _ in range(num_enemies):
        spawn_dir = random.choice(directions)

        if spawn_dir == (0, 1):
            pos = [random.randint(0, win_width - SIZE), 0]
            image = enemy_image_up
        elif spawn_dir == (0, -1):
            pos = [random.randint(0, win_width - SIZE), win_height - SIZE]
            image = enemy_image_down
        elif spawn_dir == (1, 0):
            pos = [0, random.randint(0, win_height - SIZE)]
            image = enemy_image_right
        else:
            pos = [win_width - SIZE, random.randint(0, win_height - SIZE)]
            image = enemy_image_left

        direction = [0, 0]  # 추적용, main.py에서 계산
        bounce_dir = [random.choice([-1, 1]), random.choice([-1, 1])]  # 반사 이동용

        enemies.append([
            pos,                          
            SIZE,                         
            "approach_and_shoot",         
            direction,                    
            speed,                        
            None,                         
            0,                            
            image,                        
            speed,                        
            bounce_dir                    
        ])

    return enemies
