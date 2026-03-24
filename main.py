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
manager = GameManager(res)
player = Player(res)
bgm = BGMController()

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
BOSS_MAP = {1: Stage_1_Boss.Stage1Boss, 2: Stage_2_Boss.Stage2Boss, # ... 중략
            9: Stage_9_Boss.Stage9Boss}

def reset_for_new_stage():
    enemy_group.empty()
    player_bullets.empty()
    item_group.empty()
    player.pos = [WIN_WIDTH // 2, WIN_HEIGHT // 2]

run = True
while run:
    # A. 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if not manager.game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                manager.start_game()
                reset_for_new_stage()
                bgm.set_game_state(f"stage_{manager.level}")

    # B. 게임 로직 (활성화 상태)
    if manager.game_active:
        input_reversed = False
        player.handle_input(input_reversed=input_reversed)
        
        all_sprites.update()
        player_bullets.update()
        enemy_group.update()
        item_group.update()

        if not player.invincible:
            if pygame.sprite.spritecollide(player, enemy_group, False):
                player.take_damage()
        
        items_hit = pygame.sprite.spritecollide(player, item_group, True)
        for item in items_hit:
            item.apply_effect(player)

        manager.update(player.health)

    if not manager.game_active:
        if not manager.game_over:
            win.blit(title_image, (0, 0))
        else:
            pass
    else:
        bg_img = stage_background_images[manager.level-1]
        win.blit(bg_img, (0, 0))
        all_sprites.draw(win)
        enemy_group.draw(win)
        player_bullets.draw(win)
        item_group.draw(win)