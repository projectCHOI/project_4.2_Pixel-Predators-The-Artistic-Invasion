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

enemy_image_up = load_image("enemies", "mob_enemy_Relentless Charger_1.png", size=(SIZE, SIZE))
enemy_image_down = load_image("enemies", "mob_enemy_Relentless Charger_2.png", size=(SIZE, SIZE))

def generate(level, win_width, win_height):

    enemies = []

    speed = random.randint(10, 12)
    num_enemies = random.randint(3, 8)

    directions = [(0, 1), (0, -1)]
    for _ in range(num_enemies):
        direction = random.choice(directions)
        # 위에서 아래로 이동
        if direction == (0, 1):
            pos = [random.randint(0, win_width - SIZE), 0]
            image = enemy_image_up
        else:
            # 아래에서 위로 이동
            pos = [random.randint(0, win_width - SIZE), win_height - SIZE]
            image = enemy_image_down

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
