import pygame
import sys
import os
import random
import math

# 1. 커스텀 모듈 임포트
from M_title_stage_images.config import *
from M_title_stage_images.resource_manager import ResourceManager
from M_title_stage_images.game_manager import GameManager
from M_title_stage_images.entities.player import Player
from M_title_stage_images.assets.sounds.bgm_controller import BGMController

# 적 행동 패턴 생성 함수들 임포트
from M_title_stage_images.enemy_behaviors.move_and_disappear import generate as gen_move_and_disappear
from M_title_stage_images.enemy_behaviors.move_and_shoot     import generate as gen_move_and_shoot
from M_title_stage_images.enemy_behaviors.approach_and_shoot import generate as gen_approach_and_shoot
from M_title_stage_images.enemy_behaviors.bomb               import generate as gen_bomb
from M_title_stage_images.enemy_behaviors.group_unit         import generate as gen_group_unit

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
enemy_group = pygame.sprite.Group()  # 이제 리스트가 아닌 그룹으로 관리
all_sprites.add(player)

# 3. 데이터 로드 (title_stage_images 모듈 활용)
try:
    from M_title_stage_images.title_stage_images import title_image, stage_intro_images, stage_background_images
except ImportError:
    print("Error: 이미지를 로드할 수 없습니다.")
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

# 적 생성을 위한 변수
enemy_spawn_timer = 0
spawn_interval = 3000 # 3초마다 적군 소환

def reset_stage():
    """스테이지 전환 및 초기화"""
    enemy_group.empty()
    player_bullets.empty()
    all_sprites.empty()
    all_sprites.add(player)
    player.rect.center = (WIN_WIDTH // 2, WIN_HEIGHT - 100)
    player.pos = [float(player.rect.x), float(player.rect.y)]

def draw_ui():
    # 체력 표시
    health_img = res.load_image("player", "mob_Life.png", size=(30, 30))
    for i in range(max(0, player.health)):
        win.blit(health_img, (20 + i * 35, 20))
    
    elapsed = (pygame.time.get_ticks() - manager.stage_start_ticks) // 1000
    timer_text = font.render(f"TIME: {elapsed}s", True, WHITE)
    enemy_text = font.render(f"KILLS: {manager.enemies_defeated}", True, WHITE)
    win.blit(timer_text, (WIN_WIDTH // 2 - 50, 20))
    win.blit(enemy_text, (WIN_WIDTH - 150, 20))

bgm.set_game_state("title")

# 4. 메인 루프
run = True
while run:
    now = pygame.time.get_ticks()

    # --- A. 이벤트 처리 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if not manager.game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                manager.start_game()
                reset_stage()
                bgm.set_game_state(f"stage_{manager.level}")

    # --- B. 게임 로직 ---
    if manager.game_active:
        # 1. 플레이어 입력 및 탄환 생성 (마우스/키보드 통합)
        # 보스의 입력 반전 상태 확인
        input_rev = manager.boss.is_input_reversed() if (manager.boss_active and hasattr(manager.boss, 'is_input_reversed')) else False
        
        # [핵심] player.handle_input에서 생성된 탄환들을 그룹에 추가
        new_bullets = player.handle_input(input_reversed=input_rev)
        if new_bullets:
            if isinstance(new_bullets, list):
                for b in new_bullets:
                    player_bullets.add(b)
                    all_sprites.add(b)
            else:
                player_bullets.add(new_bullets)
                all_sprites.add(new_bullets)

        # 2. 적 생성 로직 (함수형 generate_enemies 활용)
        if not manager.boss_active:
            if now - enemy_spawn_timer > spawn_interval:
                # 기존의 gen_ 함수들을 사용하여 적 데이터 생성
                # 여기서는 예시로 move_and_disappear 패턴 적을 생성하여 그룹에 추가하는 방식
                # (주의: gen_ 함수가 Sprite 객체가 아닌 리스트를 반환한다면 Sprite로 변환 로직이 필요할 수 있음)
                # 만약 Sprite 객체를 반환한다면 아래와 같이 사용:
                # new_enemies = gen_move_and_disappear(manager.level, WIN_WIDTH, WIN_HEIGHT)
                # enemy_group.add(new_enemies)
                # all_sprites.add(new_enemies)
                enemy_spawn_timer = now

        # 3. 보스 로직
        if not manager.boss_active and (now - manager.stage_start_ticks > manager.boss_spawn_delay):
            manager.spawn_boss(BOSS_MAP.get(manager.level))

        if manager.boss_active and manager.boss:
            manager.boss.move()
            manager.boss.attack()
            manager.boss.check_hit(player_bullets)
            
            # 보스 공격 데미지 판정
            if hasattr(manager.boss, 'update_attacks'):
                dmg = manager.boss.update_attacks(player.rect.center, player.invincible)
                if dmg > 0: player.take_damage(dmg)

        # 4. 업데이트 및 충돌
        all_sprites.update()
        
        # 탄환 vs 적 충돌
        hits = pygame.sprite.groupcollide(enemy_group, player_bullets, True, True)
        if hits:
            manager.enemies_defeated += len(hits)

        # 플레이어 vs 적 본체 충돌
        if not player.invincible:
            if pygame.sprite.spritecollide(player, enemy_group, True):
                player.take_damage()

        manager.update(player)

        if manager.game_over:
            bgm.set_game_state("victory" if manager.game_over_reason == "victory" else "gameover")

    # --- C. 화면 그리기 ---
    if not manager.game_active:
        if not manager.game_over:
            win.blit(title_image, (0, 0))
        else:
            # 엔드 스크린 (이전 코드의 draw_end_screen 로직 적용 가능)
            win.fill(BLACK)
            txt = "MISSION COMPLETE" if manager.game_over_reason == "victory" else "GAME OVER"
            result = font.render(txt, True, YELLOW)
            win.blit(result, (WIN_WIDTH // 2 - 100, WIN_HEIGHT // 2))
    else:
        # 배경
        bg_idx = max(0, manager.level - 1)
        win.blit(stage_background_images[bg_idx], (0, 0))
        
        # 보스 및 공격
        if manager.boss_active and manager.boss:
            manager.boss.draw(win)
            if hasattr(manager.boss, 'draw_attacks'): manager.boss.draw_attacks(win)
        
        # 모든 스프라이트 (플레이어, 탄환, 적)
        all_sprites.draw(win)
        
        draw_ui()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()