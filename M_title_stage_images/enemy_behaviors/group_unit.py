# 여러 유닛으로 구성된 집단 적
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

# 유닛 크기 및 이미지
FRONT_SIZE = 50
BACK_SIZE = 30
SPACING = 5
SPEED = 1.5
GROUP_COUNT = 5

front_image = load_image("enemies", "mob_enemy_group_unit_1.png", size=(FRONT_SIZE, FRONT_SIZE))
back_image  = load_image("enemies", "mob_enemy_group_unit_2.png", size=(BACK_SIZE, BACK_SIZE))

def generate(level, win_width, win_height):
    enemies = []
    stage_spawn_chances = {
        1: 0.0,
        2: 0.0,
        3: 0.0,
        4: 0.4,
        5: 0.6,
        6: 0.8,
        7: 0.9,
        8: 0.95,
        9: 0.95
    }

    spawn_chance = stage_spawn_chances.get(level, 0.0)
    if random.random() > spawn_chance:
        return enemies

    group_id = random.randint(1000, 9999)
    base_x = random.randint(100, win_width - FRONT_SIZE - 100)
    base_y = 0
    spawn_time = pygame.time.get_ticks()

    # 유닛 생성 (1 front + 4 back)
    for i in range(GROUP_COUNT):
        size = FRONT_SIZE if i == 0 else BACK_SIZE
        image = front_image if i == 0 else back_image

        base_pos = [base_x, base_y + i * (size + SPACING)]
        wave_offset = random.uniform(0, 2 * math.pi)
        amplitude = 50

        t = (pygame.time.get_ticks() - spawn_time) / 500
        x = base_pos[0] + amplitude * math.sin(t + wave_offset)
        y = base_pos[1] + SPEED * t
        pos = [x, y]
        
        direction = [0, 1] 

        last_attack_time = pygame.time.get_ticks()
        attack_delay = 3000 if i == 0 else 1000
        
        enemies.append([
            pos,            # [x, y]
            size,           # 유닛 크기
            "group_unit",   # 타입
            direction,      # 이동 방향
            SPEED,          # 속도
            None,           # target_pos (미사용)
            last_attack_time, # 공격 시간 기록
            image,          # 이미지
            SPEED,          # original_speed
            group_id,       # 그룹 식별자
            i,              # 그룹 내 인덱스
            1,              # 생존 여부 (1: 살아있음)
            wave_offset,    # 좌우 이동 위상
            base_pos,       # 기준 위치
            spawn_time,     # 생성 시간
            attack_delay    # 공격 주기            
        ])

    return enemies
