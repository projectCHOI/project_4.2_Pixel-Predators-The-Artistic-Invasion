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

# 이미지 로딩
SIZE = 20
enemy_image_up    = load_image("enemies", "mob_enemy_Relentless Charger_1.png", size=(SIZE, SIZE))
enemy_image_down  = load_image("enemies", "mob_enemy_Relentless Charger_2.png", size=(SIZE, SIZE))
enemy_image_left  = load_image("enemies", "mob_enemy_Relentless Charger_3.png", size=(SIZE, SIZE))
enemy_image_right = load_image("enemies", "mob_enemy_Relentless Charger_4.png", size=(SIZE, SIZE))


def generate(level, win_width, win_height):

    enemies = []

    speed = random.randint(10, 18)
    num_enemies = random.randint(6, 26)

    # 사방에서 등장
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for _ in range(num_enemies):
        spawn_dir = random.choice(directions)
        if spawn_dir == (0, 1):  # 위에서 아래
            pos = [random.randint(0, win_width - SIZE), 0]
            image = enemy_image_up
        elif spawn_dir == (0, -1):  # 아래에서 위
            pos = [random.randint(0, win_width - SIZE), win_height - SIZE]
            image = enemy_image_down
        elif spawn_dir == (1, 0):  # 왼쪽에서 오른쪽
            pos = [0, random.randint(0, win_height - SIZE)]
            image = enemy_image_right
        else:  # (-1, 0) 오른쪽에서 왼쪽
            pos = [win_width - SIZE, random.randint(0, win_height - SIZE)]
            image = enemy_image_left

        placeholder_dir = [0, 0]

        enemies.append([
            pos,                          # [x, y]
            SIZE,                         # 크기
            "approach_and_shoot",         # 타입
            placeholder_dir,              # 초기 방향 (미사용)
            speed,                        # 속도
            None,                         # target_pos (미사용)
            0,                            # shots_fired (미사용)
            image,                        # 이미지 참조
            speed                         # original_speed
        ])

    return enemies
