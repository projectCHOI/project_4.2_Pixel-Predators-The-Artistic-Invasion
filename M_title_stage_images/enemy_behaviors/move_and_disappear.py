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

SIZE = 40
enemy_image_up    = load_image("enemies", "mob_enemy_Relentless Charger_1.png", size=(SIZE, SIZE))
enemy_image_down  = load_image("enemies", "mob_enemy_Relentless Charger_2.png", size=(SIZE, SIZE))
enemy_image_left  = load_image("enemies", "mob_enemy_Relentless Charger_3.png", size=(SIZE, SIZE))
enemy_image_right = load_image("enemies", "mob_enemy_Relentless Charger_4.png", size=(SIZE, SIZE))

def generate(level, win_width, win_height):
    enemies = []

    if random.random() > 0.6: #60% 확률
        return enemies

    # 스테이지별 속도 및 개수 설정
    speed = random.randint(10, 12)
    num_enemies = random.randint(3, 8)

    # 사방향 이동 지원
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for _ in range(num_enemies):
        direction = random.choice(directions)
        # 방향에 따라 시작 위치와 이미지 선택
        if direction == (0, 1):  # 위에서 아래
            pos = [random.randint(0, win_width - SIZE), 0]
            image = enemy_image_up
        elif direction == (0, -1):  # 아래에서 위
            pos = [random.randint(0, win_width - SIZE), win_height - SIZE]
            image = enemy_image_down
        elif direction == (1, 0):  # 왼쪽에서 오른쪽
            pos = [0, random.randint(0, win_height - SIZE)]
            image = enemy_image_right
        else:  # (-1, 0) 오른쪽에서 왼쪽
            pos = [win_width - SIZE, random.randint(0, win_height - SIZE)]
            image = enemy_image_left

        enemies.append([
            pos,              # [x, y]
            SIZE,             # 크기
            "move_and_disappear",  # 타입
            direction,        # 이동 벡터
            speed,            # 속도
            None,             # target_pos (미사용)
            0,                # shots_fired (미사용)
            image,            # 이미지 참조
            speed             # original_speed
        ])

    return enemies
