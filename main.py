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

# 기존의 적 생성 함수들 임포트
try:
    from M_title_stage_images.enemy_behaviors.move_and_disappear import generate as gen_move_and_disappear
    from M_title_stage_images.enemy_behaviors.move_and_shoot     import generate as gen_move_and_shoot
    from M_title_stage_images.enemy_behaviors.approach_and_shoot import generate as gen_approach_and_shoot
    from M_title_stage_images.enemy_behaviors.bomb               import generate as gen_bomb
    from M_title_stage_images.enemy_behaviors.group_unit         import generate as gen_group_unit
except ImportError as e:
    print(f"Import Error: 적 행동 모듈을 불러올 수 없습니다. {e}")

# 2. 초기화
pygame.init()
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("The Artistic Invasion")
clock = pygame.time.Clock()

res = ResourceManager()
manager = GameManager(res)
player = Player(res)
bgm = BGMController()

# 스프라이트 및 리스트 관리
all_sprites = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemies = []  # 기존 방식의 리스트 유지
energy_balls = []
purple_bullets = []
all_sprites.add(player)

# 데이터 로드
try:
    from M_title_stage_images.title_stage_images import title_image, stage_background_images
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

# 적 생성 타이머 (단위: ms)
enemy_last_spawn_time = {
    "move_and_disappear": 0, "move_and_shoot": 0,
    "approach_and_shoot": 0, "group_unit": 0, "bomb": 0
}
enemy_spawn_intervals = {
    "move_and_disappear": 3000, "move_and_shoot": 5000,
    "approach_and_shoot": 6000, "group_unit": 8000, "bomb": 10000
}

def reset_stage_elements():
    global enemies, energy_balls, purple_bullets
    enemies = []
    energy_balls = []
    purple_bullets = []
    player_bullets.empty()
    all_sprites.empty()
    all_sprites.add(player)
    player.rect.center = (WIN_WIDTH // 2, WIN_HEIGHT - 100)
    player.pos = [float(player.rect.x), float(player.rect.y)]

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

# 4. 메인 루프
run = True
while run:
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if not manager.game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                manager.start_game()
                reset_stage_elements()
                bgm.set_game_state(f"stage_{manager.level}")

    if manager.game_active:
        # 1. 플레이어 조작 및 탄환 생성
        input_rev = manager.boss.is_input_reversed() if (manager.boss_active and hasattr(manager.boss, 'is_input_reversed')) else False
        new_bullets = player.handle_input(input_reversed=input_rev)
        if new_bullets:
            if isinstance(new_bullets, list):
                for b in new_bullets: player_bullets.add(b); all_sprites.add(b)
            else:
                player_bullets.add(new_bullets); all_sprites.add(new_bullets)

        # 2. [해결] 적 생성 로직 (리스트 방식 복구)
        if not manager.boss_active:
            # move_and_disappear 타입 예시 (다른 타입도 동일한 방식으로 추가 가능)
            if now - enemy_last_spawn_time["move_and_disappear"] > enemy_spawn_intervals["move_and_disappear"]:
                new_data = gen_move_and_disappear(manager.level, WIN_WIDTH, WIN_HEIGHT)
                enemies.extend(new_data)
                enemy_last_spawn_time["move_and_disappear"] = now

        # 3. 보스 로직
        if not manager.boss_active and (now - manager.stage_start_ticks > manager.boss_spawn_delay):
            manager.spawn_boss(BOSS_MAP.get(manager.level))
            
        if manager.boss_active and manager.boss:
            manager.boss.move(); manager.boss.attack()
            manager.boss.check_hit(player_bullets)
            if hasattr(manager.boss, 'update_attacks'):
                dmg = manager.boss.update_attacks(player.rect.center, player.invincible)
                if dmg > 0: player.take_damage(dmg)

        # 4. 업데이트 (스프라이트 그룹 및 리스트 수동 업데이트)
        all_sprites.update()
        
        # [중요] 기존 방식의 적(enemies 리스트) 이동 처리 및 충돌 체크
        new_enemies = []
        for enemy in enemies:
            # 이전 코드의 이동 로직 적용 (단순화된 예시)
            pos, size, enemy_type, direction, speed = enemy[0], enemy[1], enemy[2], enemy[3], enemy[4]
            pos[0] += direction[0] * speed
            pos[1] += direction[1] * speed
            
            # 탄환과의 충돌 체크
            enemy_rect = pygame.Rect(pos[0], pos[1], size, size)
            hit = False
            for bullet in player_bullets:
                if enemy_rect.colliderect(bullet.rect):
                    bullet.kill()
                    manager.enemies_defeated += 1
                    hit = True; break
            
            if not hit and -100 < pos[0] < WIN_WIDTH + 100 and -100 < pos[1] < WIN_HEIGHT + 100:
                new_enemies.append(enemy)
        enemies = new_enemies

        manager.update(player)
        if manager.game_over:
            bgm.set_game_state("victory" if manager.game_over_reason == "victory" else "gameover")

    # --- C. 그리기 ---
    if not manager.game_active:
        if not manager.game_over:
            win.blit(title_image, (0, 0))
        else:
            win.fill(BLACK)
            msg = font.render("MISSION COMPLETE" if manager.game_over_reason == "victory" else "GAME OVER", True, YELLOW)
            win.blit(msg, (WIN_WIDTH // 2 - 120, WIN_HEIGHT // 2))
    else:
        bg_idx = max(0, manager.level - 1)
        win.blit(stage_background_images[bg_idx], (0, 0))
        
        # 적 리스트 그리기
        for enemy in enemies:
            win.blit(enemy[7], (enemy[0][0], enemy[0][1]))
            
        if manager.boss_active and manager.boss:
            manager.boss.draw(win)
            if hasattr(manager.boss, 'draw_attacks'): manager.boss.draw_attacks(win)
        
        all_sprites.draw(win)
        draw_ui()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()