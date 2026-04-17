import pygame
import sys
import os
import math

pygame.init()

# 1. 설정 및 모듈 임포트
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

# 스프라이트 그룹 및 리스트 관리
all_sprites = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemies = []
attacks = [] # 마우스 레이저 리스트
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

# 2. 이미지 및 데이터 로드
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

# 적 스폰 설정
enemy_last_spawn_time = {"move_and_disappear": 0}
enemy_spawn_intervals = {"move_and_disappear": 3000}

def reset_game():
    """게임 상태 초기화"""
    global enemies, attacks
    enemies = []
    attacks = []
    player_bullets.empty()
    all_sprites.empty()
    all_sprites.add(player)
    player.rect.center = (WIN_WIDTH // 2, WIN_HEIGHT - 100)
    player.pos = [float(player.rect.x), float(player.rect.y)]
    # 플레이어 체력 등 초기화가 필요하면 여기서 수행 (예: player.health = 3)

def draw_ui():
    """상단 UI 대시보드 그리기"""
    health_img = res.load_image("player", "mob_Life.png", size=(30, 30))
    if health_img:
        for i in range(max(0, player.health)):
            win.blit(health_img, (20 + i * 35, 20))
    
    elapsed = (pygame.time.get_ticks() - manager.stage_start_ticks) // 1000
    timer_text = font.render(f"TIME: {elapsed}s", True, (255, 255, 255))
    enemy_text = font.render(f"KILLS: {manager.enemies_defeated}", True, (255, 255, 255))
    
    win.blit(timer_text, (WIN_WIDTH // 2 - 50, 20))
    win.blit(enemy_text, (WIN_WIDTH - 150, 20))

bgm.set_game_state("title")

# 3. 메인 루프
run = True
while run:
    now = pygame.time.get_ticks()
    mouse_pos = pygame.mouse.get_pos()

    # --- A. 이벤트 처리 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        # 타이틀/게임오버 상태에서 엔터키 입력 시 시작
        if not manager.game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                manager.start_game()
                reset_game()
                bgm.set_game_state(f"stage_{manager.level}")
        
        # 마우스 왼쪽 클릭 공격 (게임 활성화 상태)
        if manager.game_active and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if attack_sound: attack_sound.play(maxtime=400)
            
            atk_start = player.rect.center
            atk_end = mouse_pos
            # 플레이어의 파워 아이템 상태 연동 (없으면 기본값 0)
            p_level = getattr(player, 'power_item_active', 0)
            atk_color = attack_colors.get(p_level, (255, 255, 255))
            
            if p_level == 0:
                attacks.append([atk_start, atk_end, 3, atk_color])
            elif p_level == 1:
                for off in [0, 5, -5]:
                    attacks.append([atk_start, (atk_end[0]+off, atk_end[1]+off), 3, atk_color])
            else:
                for off in [0, 10, -10, 5, -5]:
                    attacks.append([atk_start, (atk_end[0]+off, atk_end[1]+off), 3, atk_color])

    # --- B. 게임 로직 (Active) ---
    if manager.game_active:
        # 1. 플레이어 업데이트 및 입력 처리
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
        # 2. 보스 소환 로직
            if not manager.boss_active:
                if now - manager.stage_start_ticks > manager.boss_spawn_delay:
                    boss_class = BOSS_MAP.get(manager.level)
                    if boss_class:
                        manager.spawn_boss(boss_class)
                        print(f"Stage {manager.level} Boss Spawned!")

        # 3. 일반 적 업데이트
            if not manager.boss_active and gen_move_and_disappear:
                if now - enemy_last_spawn_time["move_and_disappear"] > enemy_spawn_intervals["move_and_disappear"]:
                    try:
                        new_data = gen_move_and_disappear(manager.level, WIN_WIDTH, WIN_HEIGHT)
                        enemies.extend(new_data)
                    except Exception as e:
                        print(f"적 생성 실패: {e}")
                    enemy_last_spawn_time["move_and_disappear"] = now
        # 4. 보스 행동 업데이트
            all_sprites.update() 
            
            if manager.boss_active and manager.boss:
                manager.boss.move()
                manager.boss.attack()
                manager.boss.check_hit(player_bullets)
                
                boss_rect = getattr(manager.boss, 'rect', pygame.Rect(manager.boss.pos[0], manager.boss.pos[1], 100, 100))
                for atk in attacks:
                    if boss_rect.clipline(atk[0], atk[1]):
                        if hasattr(manager.boss, 'take_damage'):
                            manager.boss.take_damage(0.5)
                        elif hasattr(manager.boss, 'hp'):
                            manager.boss.hp -= 0.1
        # 5. 마우스 레이저 이동 로직
        all_sprites.update()
        new_line_attacks = []
        for atk in attacks:
                start, end, thick, color = atk
                dx, dy = end[0] - start[0], end[1] - start[1]
                dist = math.hypot(dx, dy)
                if dist < 1: continue # 정지 상태 제거
                
                vx, vy = (dx / dist) * attack_speed, (dy / dist) * attack_speed
                next_start = (start[0] + vx, start[1] + vy)
                next_end = (end[0] + vx, end[1] + vy)
                
                if -50 <= next_start[0] <= WIN_WIDTH + 50 and -50 <= next_start[1] <= WIN_HEIGHT + 50:
                    new_line_attacks.append([next_start, next_end, thick, color])
        attacks = new_line_attacks

        # 6. 일반 적 업데이트 및 충돌 체크
        updated_enemies = []
        for enemy in enemies:
            enemy[0][0] += enemy[3][0] * enemy[4]
            enemy[0][1] += enemy[3][1] * enemy[4]
            
            enemy_rect = pygame.Rect(enemy[0][0], enemy[0][1], enemy[1], enemy[1])
            hit = False
            
            # 키보드 탄환 충돌
            for bullet in player_bullets:
                if enemy_rect.colliderect(bullet.rect):
                    bullet.kill()
                    manager.enemies_defeated += 1
                    hit = True; break
            
            # 마우스 공격선 충돌
            if not hit:
                for atk in attacks:
                    if enemy_rect.clipline(atk[0], atk[1]):
                        manager.enemies_defeated += 1
                        hit = True; break
            
            if not hit and -100 < enemy[0][0] < WIN_WIDTH + 100 and -100 < enemy[0][1] < WIN_HEIGHT + 100:
                updated_enemies.append(enemy)
        enemies = updated_enemies

        # 매니저 상태 업데이트 (승리/패배 체크)
        manager.update(player)
        if manager.game_over:
            bgm.set_game_state("victory" if manager.game_over_reason == "victory" else "gameover")

    # --- C. 화면 그리기 ---
    if not manager.game_active:
        if not manager.game_over:
            win.blit(title_image, (0, 0))
        else:
            win.fill(BLACK)
            msg_text = "MISSION COMPLETE" if manager.game_over_reason == "victory" else "GAME OVER"
            msg = font.render(msg_text, True, YELLOW)
            win.blit(msg, (WIN_WIDTH // 2 - 120, WIN_HEIGHT // 2))
            retry_text = font.render("Press ENTER to Restart", True, WHITE)
            win.blit(retry_text, (WIN_WIDTH // 2 - 150, WIN_HEIGHT // 2 + 50))
    else:
        # 배경 그리기
        bg_idx = max(0, manager.level - 1)
        if bg_idx < len(stage_background_images):
            win.blit(stage_background_images[bg_idx], (0, 0))
        
        # 일반 적 그리기
        for enemy in enemies:
            win.blit(enemy[7], (enemy[0][0], enemy[0][1]))
            
        # 마우스 공격 레이저 그리기
        for atk in attacks:
            pygame.draw.line(win, atk[3], atk[0], atk[1], atk[2])

        # 보스 그리기
        if manager.boss_active and manager.boss:
            manager.boss.draw(win)
            if hasattr(manager.boss, 'draw_attacks'): manager.boss.draw_attacks(win)
            if hasattr(manager.boss, 'draw_health_bar'): manager.boss.draw_health_bar(win, font)
        
        all_sprites.draw(win)
        pygame.draw.circle(win, (255, 0, 0), mouse_pos, 5) # 에임
        draw_ui()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()