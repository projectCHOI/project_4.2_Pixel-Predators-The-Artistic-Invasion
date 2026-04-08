import pygame
import sys
import os

# 1. 초기화 (가장 먼저 수행)
pygame.init()

# 2. 커스텀 모듈 임포트
from M_title_stage_images.config import *
from M_title_stage_images.resource_manager import ResourceManager
from M_title_stage_images.game_manager import GameManager
from M_title_stage_images.entities.player import Player
from M_title_stage_images.assets.sounds.bgm_controller import BGMController

# 3. 윈도우 설정 (이미지 로드보다 먼저 실행되어야 함)
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("The Artistic Invasion")
clock = pygame.time.Clock()

# 4. 리소스 매니저 및 객체 생성
res = ResourceManager()
manager = GameManager(res)
player = Player(res)
bgm = BGMController()

# 스프라이트 그룹 및 리스트
all_sprites = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemies = []
all_sprites.add(player)

# 5. 데이터 로드 (에러 방지를 위한 Try-Except)
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

# 폰트 설정
font = pygame.font.Font(res.get_font_path("SLEIGothicOTF.otf"), 30)

# 적 생성 관련 임포트
try:
    from M_title_stage_images.enemy_behaviors.move_and_disappear import generate as gen_move_and_disappear
except ImportError:
    gen_move_and_disappear = None

# 적 생성 타이머
enemy_last_spawn_time = {"move_and_disappear": 0}
enemy_spawn_intervals = {"move_and_disappear": 3000}

def reset_game():
    global enemies
    enemies = []
    player_bullets.empty()
    all_sprites.empty()
    all_sprites.add(player)
    player.rect.center = (WIN_WIDTH // 2, WIN_HEIGHT - 100)
    player.pos = [float(player.rect.x), float(player.rect.y)]

bgm.set_game_state("title")

def draw_ui():
    """상단 UI 대시보드 (체력, 시간, 적 처치 수) 그리기"""
    # 1. 체력 아이콘 표시
    health_img = res.load_image("player", "mob_Life.png", size=(30, 30))
    if health_img:
        for i in range(max(0, player.health)):
            win.blit(health_img, (20 + i * 35, 20))
    
    # 2. 시간 계산
    # manager.stage_start_ticks가 정의되어 있어야 합니다.
    elapsed = (pygame.time.get_ticks() - manager.stage_start_ticks) // 1000
    timer_text = font.render(f"TIME: {elapsed}s", True, (255, 255, 255)) # WHITE
    
    # 3. 적 처치 수
    enemy_text = font.render(f"KILLS: {manager.enemies_defeated}", True, (255, 255, 255)) # WHITE
    
    # 4. 화면에 출력
    win.blit(timer_text, (WIN_WIDTH // 2 - 50, 20))
    win.blit(enemy_text, (WIN_WIDTH - 150, 20))
    
# 6. 메인 루프
run = True
while run:
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if not manager.game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                manager.start_game()
                reset_game()
                bgm.set_game_state(f"stage_{manager.level}")

    if manager.game_active:
        # 플레이어 입력
        input_rev = manager.boss.is_input_reversed() if (manager.boss_active and hasattr(manager.boss, 'is_input_reversed')) else False
        new_bullets = player.handle_input(input_reversed=input_rev)
        if new_bullets:
            if isinstance(new_bullets, list):
                for b in new_bullets: player_bullets.add(b); all_sprites.add(b)
            else:
                player_bullets.add(new_bullets); all_sprites.add(new_bullets)

        # 적 생성 (오류 방지 로직 포함)
        if not manager.boss_active and gen_move_and_disappear:
            if now - enemy_last_spawn_time["move_and_disappear"] > enemy_spawn_intervals["move_and_disappear"]:
                try:
                    new_data = gen_move_and_disappear(manager.level, WIN_WIDTH, WIN_HEIGHT)
                    enemies.extend(new_data)
                except Exception as e:
                    print(f"적 생성 실패: {e}")
                enemy_last_spawn_time["move_and_disappear"] = now

        # 보스 로직
        if not manager.boss_active and (now - manager.stage_start_ticks > manager.boss_spawn_delay):
            manager.spawn_boss(BOSS_MAP.get(manager.level))
            
        if manager.boss_active and manager.boss:
            manager.boss.move()
            manager.boss.attack()
            manager.boss.check_hit(player_bullets)

        # 업데이트 및 충돌 체크
        all_sprites.update()
        
        # 적 리스트 업데이트 및 충돌 (수동)
        updated_enemies = []
        for enemy in enemies:
            # 이동 (기본 이동 방식)
            enemy[0][0] += enemy[3][0] * enemy[4]
            enemy[0][1] += enemy[3][1] * enemy[4]
            
            # 충돌 체크
            enemy_rect = pygame.Rect(enemy[0][0], enemy[0][1], enemy[1], enemy[1])
            hit = False
            for bullet in player_bullets:
                if enemy_rect.colliderect(bullet.rect):
                    bullet.kill()
                    manager.enemies_defeated += 1
                    hit = True
                    break
            
            if not hit and -100 < enemy[0][0] < WIN_WIDTH + 100 and -100 < enemy[0][1] < WIN_HEIGHT + 100:
                updated_enemies.append(enemy)
        enemies = updated_enemies

        manager.update(player)

    # --- C. 그리기 (Drawing) ---
    if not manager.game_active:
        if not manager.game_over:
            win.blit(title_image, (0, 0))
        else:
            # 엔드 스크린 (이전 코드의 draw_end_screen 로직 적용 가능)
            win.fill(BLACK)
            msg_text = "MISSION COMPLETE" if manager.game_over_reason == "victory" else "GAME OVER"
            msg = font.render(msg_text, True, YELLOW)
            win.blit(msg, (WIN_WIDTH // 2 - 120, WIN_HEIGHT // 2))
            retry_text = font.render("Press ENTER to Restart", True, WHITE)
            win.blit(retry_text, (WIN_WIDTH // 2 - 150, WIN_HEIGHT // 2 + 50))
    else:
        # 1. 배경 그리기
        bg_idx = max(0, manager.level - 1)
        if bg_idx < len(stage_background_images):
            win.blit(stage_background_images[bg_idx], (0, 0))
        
        # 2. 적 리스트(enemies) 그리기
        for enemy in enemies:
            # enemy[7]에 이미지 데이터가 있다고 가정 (이전 코드 구조)
            win.blit(enemy[7], (enemy[0][0], enemy[0][1]))
            
        # 3. 보스 및 보스 공격 그리기
        if manager.boss_active and manager.boss:
            manager.boss.draw(win)
            if hasattr(manager.boss, 'draw_attacks'):
                manager.boss.draw_attacks(win)
            if hasattr(manager.boss, 'draw_health_bar'):
                manager.boss.draw_health_bar(win, font)
        
        # 4. 플레이어 및 탄환 그리기 (스프라이트 그룹)
        all_sprites.draw(win)

        # 5. [핵심] UI 대시보드 그리기 (체력, 시간, 킬 카운트)
        draw_ui()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()