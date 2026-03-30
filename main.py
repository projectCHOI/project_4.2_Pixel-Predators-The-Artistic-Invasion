import pygame
import random
import math
import os
import sys

# 모듈 임포트
from M_title_stage_images.config import *
from M_title_stage_images.resource_manager import ResourceManager
from M_title_stage_images.game_manager import GameManager
from M_title_stage_images.entities.player import Player
from M_title_stage_images.assets.sounds.bgm_controller import BGMController

# 초기화
pygame.init()
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("The Artistic Invasion")
clock = pygame.time.Clock()

# 매니저 및 리소스 로더 초기화
res = ResourceManager()
player = Player(res)
bgm = BGMController()
manager = GameManager(res)

# 스프라이트 그룹 설정
all_sprites = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
all_sprites.add(player)

# 외부 데이터 임포트
try:
    from M_title_stage_images.title_stage_images import title_image, stage_intro_images, stage_background_images
except ImportError:
    print("이미지 모듈을 찾을 수 없습니다.")
    pygame.quit()
    sys.exit()

from M_title_stage_images.bosses import (
    Stage_1_Boss, Stage_2_Boss, Stage_3_Boss, Stage_4_Boss, Stage_5_Boss,
    Stage_6_Boss, Stage_7_Boss, Stage_8_Boss, Stage_9_Boss
)
BOSS_MAP = {1: Stage_1_Boss.Stage1Boss, 2: Stage_2_Boss.Stage2Boss, 3: Stage_3_Boss.Stage3Boss,
            4: Stage_4_Boss.Stage4Boss, 5: Stage_5_Boss.Stage5Boss, 6: Stage_6_Boss.Stage6Boss,
            7: Stage_7_Boss.Stage7Boss, 8: Stage_8_Boss.Stage8Boss, 9: Stage_9_Boss.Stage9Boss}

def reset_for_new_stage():
    enemy_group.empty()
    player_bullets.empty()
    item_group.empty()
    player.pos = [WIN_WIDTH // 2, WIN_HEIGHT // 2]

# 초기 상태 설정
bgm.set_game_state("title")

run = True
while run:
    # A. 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if not manager.game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # 1. BGM을 로딩 상태로 변경
                bgm.set_game_state("loading")
                
                # 2. 스테이지 준비
                manager.start_game()
                reset_for_new_stage()
                
                # 3. (옵션) 인트로 화면이 있다면 여기서 대기 로직 가능
                # 4. 실제 스테이지 BGM 시작
                bgm.set_game_state(f"stage_{manager.level}")

    # B. 게임 로직 (활성화 상태)
    if manager.game_active:
        now = pygame.time.get_ticks()