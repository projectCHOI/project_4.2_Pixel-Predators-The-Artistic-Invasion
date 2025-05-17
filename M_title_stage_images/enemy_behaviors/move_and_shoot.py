import random
import os
import pygame
import math

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

# 적 이미지
SIZE = 60
ambush_striker_up    = load_image("enemies", "mob_enemy_Ambush Striker_1.png", size=(SIZE, SIZE))
ambush_striker_down  = load_image("enemies", "mob_enemy_Ambush Striker_2.png", size=(SIZE, SIZE))
ambush_striker_left  = load_image("enemies", "mob_enemy_Ambush Striker_3.png", size=(SIZE, SIZE))
ambush_striker_right = load_image("enemies", "mob_enemy_Ambush Striker_4.png", size=(SIZE, SIZE))


def generate(level, win_width, win_height):
    enemies = []

    stage_spawn_chances = {
        1: 0.3,
        2: 0.4,
        3: 0.5,
        4: 0.6,
        5: 0.7,
        6: 0.8,
        7: 0.9,
        8: 0.9,
        9: 0.95,
    }

    spawn_chance = stage_spawn_chances.get(level, 0.0)

    if random.random() > spawn_chance:
        return enemies

    # 이동 속도를 10~16 사이에서 무작위로 설정
    speed = random.randint(10, 16)
    # 등장 수 6~24 사이에서 무작위로 설정
    num_enemies = random.randint(6, 24)

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for _ in range(num_enemies):
        direction = random.choice(directions)
        # 시작 위치와 이미지 선택
        if direction == (0, 1):  # 위에서 아래
            pos = [random.randint(0, win_width - SIZE), 0]
            image = ambush_striker_up
        elif direction == (0, -1):  # 아래에서 위
            pos = [random.randint(0, win_width - SIZE), win_height - SIZE]
            image = ambush_striker_down
        elif direction == (1, 0):  # 왼쪽에서 오른쪽
            pos = [0, random.randint(0, win_height - SIZE)]
            image = ambush_striker_left
        else:  # (-1, 0) 오른쪽에서 왼쪽
            pos = [win_width - SIZE, random.randint(0, win_height - SIZE)]
            image = ambush_striker_right

        # 목표 위치 설정 (맵 내 랜덤 지점)
        target_pos = [
            random.randint(100, win_width - 100),
            random.randint(100, win_height - 100)
        ]
        dx, dy = target_pos[0] - pos[0], target_pos[1] - pos[1]
        dist = math.hypot(dx, dy) or 1
        dir_norm = [dx / dist, dy / dist]

        enemies.append([
            pos,               # [x, y]
            SIZE,              # 크기
            "move_and_shoot",  # 타입
            dir_norm,          # 이동 벡터
            speed,             # 속도
            target_pos,        # 목표 위치
            0,                 # shots_fired 초기화
            image,             # 이미지 참조
            speed              # original_speed
        ])

    return enemies
