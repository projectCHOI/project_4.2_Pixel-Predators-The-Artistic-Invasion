# 설정값 (색상, 화면 크기, 상수)
import pygame

# 화면 설정
WIN_WIDTH, WIN_HEIGHT = 1280, 720
FPS = 30

# 색상 정의
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (255, 0, 0)
BLUE   = (0, 0, 255)
CYAN   = (0, 255, 255)
YELLOW = (255, 255, 0)
GREEN  = (0, 255, 0)

# 플레이어 설정
PLAYER_START_HEALTH = 3
PLAYER_MAX_HEALTH = 5
INVINCIBLE_DURATION = 3000

# 아이템 확률
ITEM_CHANCE = {
    "speed": 0.1,
    "power": 0.1,
    "heal": 0.4
}

# 공격 색상 매핑
ATTACK_COLORS = {
    0: (255, 0, 0),
    1: (255, 127, 0),
    2: (255, 255, 0),
    3: (0, 255, 0),
    4: (0, 0, 255)
}