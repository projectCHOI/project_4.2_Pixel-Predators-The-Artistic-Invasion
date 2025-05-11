import random
import os
import pygame

# 이미지 로딩
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

# 유닛 크기 및 이미지
FRONT_SIZE = 50
BACK_SIZE = 30
SPACING = 5  # 유닛 간 y 간격
SPEED = 3
GROUP_COUNT = 5

front_image = load_image("enemies", "mob_enemy_Sentinel Shooter_left.png", size=(FRONT_SIZE, FRONT_SIZE))
back_image  = load_image("enemies", "mob_enemy_Ambush Striker_3.png", size=(BACK_SIZE, BACK_SIZE))

def generate(level, win_width, win_height):

    enemies = []
    group_id = random.randint(1000, 9999)

    base_x = random.randint(100, win_width - FRONT_SIZE - 100)
    base_y = 0

    for i in range(GROUP_COUNT):
        if i == 0:
            size = FRONT_SIZE
            image = front_image
        else:
            size = BACK_SIZE
            image = back_image

        pos = [base_x, base_y + i * (size + SPACING)]
        direction = [0, 1]  # 기본 아래 방향

        enemies.append([
            pos,            
            size,           
            "group_unit",   
            direction,      
            SPEED,          
            None,           
            0,              
            image,          
            SPEED,          
            group_id,       
            i,              
            1               
        ])

    return enemies
