import pygame
import sys
import os
import random

# 1. 커스텀 모듈 임포트
from M_title_stage_images.config import *
from M_title_stage_images.resource_manager import ResourceManager
from M_title_stage_images.game_manager import GameManager
from M_title_stage_images.entities.player import Player
from M_title_stage_images.assets.sounds.bgm_controller import BGMController

# 2. 초기화
pygame.init()
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("The Artistic Invasion")
clock = pygame.time.Clock()

res = ResourceManager()
manager = GameManager(res)
player = Player(res)
bgm = BGMController()

# 스프라이트 그룹
all_sprites = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
all_sprites.add(player)

# 3. 데이터 로드
try:
    from M_title_stage_images.title_stage_images import title_image, stage_background_images
except ImportError:
    print("Error: title_stage_images 모듈을 찾을 수 없습니다.")
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

enemy_spawn_timer = 0
spawn_delay = 1000

def reset_stage_elements():
    global enemy_spawn_timer
    enemy_group.empty()
    player_bullets.empty()
    item_group.empty()
    all_sprites.empty()
    all_sprites.add(player)
    player.rect.center = (WIN_WIDTH // 2, WIN_HEIGHT - 100)
    player.pos = [float(player.rect.x), float(player.rect.y)]
    enemy_spawn_timer = pygame.time.get_ticks()

def draw_ui():
    health_img = res.load_image("player", "mob_Life.png", size=(30, 30))
    if health_img:
        for i in range(max(0, player.health)):
            win.blit(health_img, (20 + i * 35, 20))
    
    elapsed = (pygame.time.get_ticks() - manager.stage_start_ticks) // 1000
    timer_text = font.render(f"TIME: {elapsed}s", True, WHITE)
    enemy_text = font.render(f"KILLS: {manager.enemies_defeated}", True, WHITE)
    win.blit(timer_text, (WIN_WIDTH // 2 - 50, 20))
    win.blit(enemy_text, (WIN_WIDTH - 150, 20))

bgm.set_game_state("title")

# 4. 메인 게임 루프
run = True
while run:
    # --- A. 이벤트 처리 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if not manager.game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                manager.start_game()
                reset_stage_elements()
                bgm.set_game_state(f"stage_{manager.level}")

    # --- B. 게임 로직 (Active) ---
    if manager.game_active:
        now = pygame.time.get_ticks()
        
        # 1. 플레이어 업데이트 및 탄환 발사 로직 (보완)
        input_rev = manager.boss.is_input_reversed() if (manager.boss_active and hasattr(manager.boss, 'is_input_reversed')) else False
        
        new_bullets = player.handle_input(input_reversed=input_rev)
        if new_bullets:
            if isinstance(new_bullets, list):
                for b in new_bullets:
                    player_bullets.add(b)
                    all_sprites.add(b)
            else:
                player_bullets.add(new_bullets)
                all_sprites.add(new_bullets)

        # 2. 일반 적 생성 로직 (AttributeError 방지)
        if not manager.boss_active and Enemy is not None:
            if now - enemy_spawn_timer > spawn_delay:
                new_enemy = Enemy(res, level=manager.level) 
                enemy_group.add(new_enemy)
                all_sprites.add(new_enemy)
                enemy_spawn_timer = now
