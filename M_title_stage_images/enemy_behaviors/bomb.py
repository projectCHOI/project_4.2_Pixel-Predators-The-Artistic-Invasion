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

# 폭탄 이미지
enemy_bomb_image = load_image("enemies", "mob_item_bomb.png", size=(40, 40))

# 폭탄 등장 스테이지
BOMB_STAGES = {2, 3, 5, 7, 11}
# 등장 가능 방향
DIRECTIONS = ["left", "right", "up", "down"]
# 고정 속성
SIZE = 40
SPEED = 9

def generate(level, win_width, win_height):

    enemies = []
    if level in BOMB_STAGES:
        direction = random.choice(DIRECTIONS)

        # 시작 위치
        if direction == "left":
            pos = [0, random.randint(0, win_height - SIZE)]
        elif direction == "right":
            pos = [win_width - SIZE, random.randint(0, win_height - SIZE)]
        elif direction == "up":
            pos = [random.randint(0, win_width - SIZE), 0]
        else:  # "down"
            pos = [random.randint(0, win_width - SIZE), win_height - SIZE]

        # 플레이어 방향 벡터 계산
        target = [win_width // 2, win_height // 2]
        dx, dy = target[0] - pos[0], target[1] - pos[1]
        dist = math.hypot(dx, dy) or 1
        dir_norm = [dx / dist, dy / dist]

        enemies.append([
            pos,             # [x, y]
            SIZE,            # 크기
            "bomb",          # 타입
            dir_norm,        # 이동 벡터
            SPEED,           # 속도
            None,            # target_pos (미사용)
            0,               # shots_fired (미사용)
            enemy_bomb_image,# 이미지 참조
            SPEED            # original_speed
        ])
    return enemies
