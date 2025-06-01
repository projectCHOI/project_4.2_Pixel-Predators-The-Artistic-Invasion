# 플레이어를 향해 돌진하는 폭탄형 적
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
enemy_bomb_image = load_image("enemies", "mob_enemy_bomb.png", size=(SIZE, SIZE))

# 등장 조건
BOMB_STAGES = {2, 3, 5, 7, 11}
DIRECTIONS = ["left", "right", "up", "down"]

def generate(level, win_width, win_height, player_pos):
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
        else:
            pos = [random.randint(0, win_width - SIZE), win_height - SIZE]

        # 목표
        dx, dy = player_pos[0] - pos[0], player_pos[1] - pos[1]
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
            SPEED,
            True,
            {
                "count": 8,
                "speed": 6,
                "size": 30,
                "image_path": ["enemies", "mob_enemy_bomb.png"]
            }              
        ])

    return enemies

def generate_purple_bullets(center_pos):
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]
    speed = 5
    now = pygame.time.get_ticks()
    bullets = []

    for d in directions:
        vel = [d[0] * speed, d[1] * speed]
        bullets.append({
            "pos": [center_pos[0], center_pos[1]],  # 시작 위치
            "vel": vel,                              # 속도 벡터
            "image": PURPLE_BULLET_IMAGE,            # 이미지
            "spawn_time": now                        # 생성 시간
        })

    return bullets