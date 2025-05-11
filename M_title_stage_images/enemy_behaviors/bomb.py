import random
import math
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

# 폭탄 설정
SIZE = 40
SPEED = 9
enemy_bomb_image = load_image("enemies", "mob_item_bomb.png", size=(SIZE, SIZE))

# 등장 조건
BOMB_STAGES = {2, 3, 5, 7, 11}
DIRECTIONS = ["left", "right", "up", "down"]

def generate(level, win_width, win_height):
    enemies = []

    if level in BOMB_STAGES:
        direction = random.choice(DIRECTIONS)

        # 화면 가장자리 스폰
        if direction == "left":
            pos = [0, random.randint(0, win_height - SIZE)]
        elif direction == "right":
            pos = [win_width - SIZE, random.randint(0, win_height - SIZE)]
        elif direction == "up":
            pos = [random.randint(0, win_width - SIZE), 0]
        else:  # down
            pos = [random.randint(0, win_width - SIZE), win_height - SIZE]

        # 목표
        target = [win_width // 2, win_height // 2]
        dx, dy = target[0] - pos[0], target[1] - pos[1]
        dist = math.hypot(dx, dy) or 1
        dir_norm = [dx / dist, dy / dist]

        enemies.append([
            pos,               
            SIZE,              
            "bomb",            
            dir_norm,          
            SPEED,             
            None,              
            0,                 
            enemy_bomb_image,  
            SPEED              
        ])

    return enemies
