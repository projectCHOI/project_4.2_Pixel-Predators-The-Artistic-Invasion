# 일직선으로 이동 후 화면 밖으로 사라지는 적
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

    stage_spawn_chances = {
        1: 0.6,
        2: 0.6,
        3: 0.6,
        4: 0.7,
        5: 0.7,
        2: 0.7,
        3: 0.8,
        4: 0.8,
        5: 0.8,
        }
                
    spawn_chance = stage_spawn_chances.get(level, 0.1)

    if random.random() > spawn_chance:
        return enemies
    
    # 이동 속도를 10~12 사이에서 무작위로 설정
    speed = random.randint(6, 10)
    # 등장 수 3~8 사이에서 무작위로 설정
    num_enemies = random.randint(4, 16)

    # 사방향 이동 지원
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for _ in range(num_enemies):
        direction = random.choice(directions)
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
