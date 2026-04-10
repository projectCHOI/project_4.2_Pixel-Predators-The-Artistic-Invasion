import pygame
import sys
import os
import math

pygame.init()

from M_title_stage_images.config import *
from M_title_stage_images.resource_manager import ResourceManager
from M_title_stage_images.game_manager import GameManager
from M_title_stage_images.entities.player import Player
from M_title_stage_images.assets.sounds.bgm_controller import BGMController

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("The Artistic Invasion")
clock = pygame.time.Clock()

res = ResourceManager()
manager = GameManager(res)
player = Player(res)
bgm = BGMController()

all_sprites = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemies = []
attacks = [] 
attack_speed = 20
attack_colors = {
    0: (255, 0, 0),    # 빨강
    1: (255, 127, 0),  # 주황
    2: (255, 255, 0),  # 노랑
    3: (0, 255, 0),    # 초록
    4: (0, 0, 255)     # 파랑
}
attack_sound = res.load_sound("Attack_sound.wav", 0.4)

all_sprites.add(player)

try:
    from M_title_stage_images.title_stage_images import title_image, stage_background_images
except Exception as e:
    print(f"이미지 데이터 로드 중 오류 발생: {e}")
    pygame.quit()
    sys.exit()

from M_title_stage_images.bosses import (
    Stage_1_Boss, Stage_2_Boss, Stage_3_Boss, Stage_4_Boss, Stage_5_Boss,
    Stage_6_Boss, Stage_7_Boss, Stage_8_Boss, Stage_9_Boss
)
BOSS_MAP = {
    1: Stage_1_Boss.Stage1Boss, 2: Stage_2_Boss.Stage2Boss, 3: Stage_3_Boss.Stage3Boss,
    4: Stage_4_Boss.Stage4Boss, 5: Stage_5_Boss.Stage5Boss, 6: Stage_6_Boss.Stage6Boss,
    7: Stage_7_Boss.Stage7Boss, 8: Stage_8_Boss.Stage8Boss, 9: Stage_9_Boss.Stage9Boss
}

font = pygame.font.Font(res.get_font_path("SLEIGothicOTF.otf"), 30)

try:
    from M_title_stage_images.enemy_behaviors.move_and_disappear import generate as gen_move_and_disappear
except ImportError:
    gen_move_and_disappear = None

enemy_last_spawn_time = {"move_and_disappear": 0}
enemy_spawn_intervals = {"move_and_disappear": 3000}
