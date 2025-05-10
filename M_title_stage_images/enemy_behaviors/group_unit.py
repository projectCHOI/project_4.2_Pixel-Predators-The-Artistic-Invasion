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

# 적 이미지
FRONT_SIZE = 50
BACK_SIZE = 30
front_image = load_image("enemies", "mob_enemy_Sentinel Shooter_left.png", size=(FRONT_SIZE, FRONT_SIZE))
back_image  = load_image("enemies", "mob_enemy_Ambush Striker_3.png", size=(BACK_SIZE, BACK_SIZE))

# 그룹 유닛 생성 수 및 기본 속도
GROUP_COUNT = 5
SPEED = 3


def generate(level, win_width, win_height):

    enemies = []

    group_id = random.randint(1000, 9999)

    base_x = random.randint(100, max(100, win_width - 100))
    base_y = 0

    for i in range(GROUP_COUNT):
        if i == 0:
            size = FRONT_SIZE
            image = front_image
        else:
            size = BACK_SIZE
            image = back_image
        # 각 유닛 y 오프셋
        pos = [base_x, base_y + i * (size + 5)]
        direction = [0, 1]  # 기본 아래 방향

        enemies.append([
            pos,            # [x, y]
            size,           # 크기
            "group_unit",   # 타입
            direction,      # 이동 벡터
            SPEED,          # 속도
            None,           # target_pos (미사용)
            0,              # shots_fired (미사용)
            image,          # 이미지 참조
            SPEED,          # original_speed
            group_id,       # 그룹 ID
            i,              # index_in_group
            1               # alive_flag
        ])
    return enemies
