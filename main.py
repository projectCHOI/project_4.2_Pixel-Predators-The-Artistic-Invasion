import pygame
import sys
import os

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

# 스프라이트 그룹 관리
all_sprites = pygame.sprite.Group()
player_bullets = pygame.sprite.Group() # 플레이어 탄환 그룹
enemy_group = pygame.sprite.Group()    # 일반 적 그룹
item_group = pygame.sprite.Group()
all_sprites.add(player)

# 3. 데이터 로드
try:
    from M_title_stage_images.title_stage_images import title_image, stage_intro_images, stage_background_images
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

def reset_stage_elements():
    enemy_group.empty()
    player_bullets.empty()
    item_group.empty()
    all_sprites.empty()
    all_sprites.add(player)
    player.rect.center = (WIN_WIDTH // 2, WIN_HEIGHT - 100)
    player.pos = [float(player.rect.x), float(player.rect.y)]

def draw_ui():
    health_img = res.load_image("player", "mob_Life.png", size=(30, 30))
    if health_img:
        for i in range(player.health):
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
        # 1. 플레이어 입력 및 탄환 생성 핵심 수정
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

        # 2. 일반 적 생성 로직 추가
        if not manager.boss_active:
            new_enemy = manager.spawn_enemy()
            if new_enemy:
                enemy_group.add(new_enemy)
                all_sprites.add(new_enemy)

        # 3. 보스 생성 및 로직
        if not manager.boss_active and (now - manager.stage_start_ticks > manager.boss_spawn_delay):
            manager.spawn_boss(BOSS_MAP.get(manager.level))
            enemy_group.empty() 
            
        if manager.boss_active and manager.boss:
            manager.boss.move()
            manager.boss.attack()
            if hasattr(manager.boss, 'update_attacks'):
                damage = manager.boss.update_attacks(player.rect.center, player.invincible)
                if damage > 0: player.take_damage(damage)
            manager.boss.check_hit(player_bullets)

        # 4. 업데이트
        all_sprites.update() 
        # (참고: all_sprites에 bullets, enemies가 포함되어 있다면 그룹별 update는 생략 가능)

        # 5. 충돌 체크
        # 플레이어 vs 적 탄환/적 본체
        if not player.invincible:
            if pygame.sprite.spritecollide(player, enemy_group, False):
                player.take_damage()
        
        # 플레이어 탄환 vs 일반 적
        hits = pygame.sprite.groupcollide(enemy_group, player_bullets, True, True)
        if hits:
            manager.enemies_defeated += len(hits)

        # 아이템 획득
        items_hit = pygame.sprite.spritecollide(player, item_group, True)
        for item in items_hit:
            item.apply_effect(player)

        manager.update(player)
        
        if manager.game_over:
            bgm.set_game_state("victory" if manager.game_over_reason == "victory" else "gameover")
    # --- C. 화면 그리기 (Draw) ---
    if not manager.game_active:
        if not manager.game_over:
            win.blit(title_image, (0, 0))
        else:
            win.fill(BLACK)
            msg = "MISSION COMPLETE" if manager.game_over_reason == "victory" else "GAME OVER"
            result_text = font.render(msg, True, YELLOW)
            win.blit(result_text, (WIN_WIDTH // 2 - 100, WIN_HEIGHT // 2))
            retry_text = font.render("Press ENTER to Restart", True, WHITE)
            win.blit(retry_text, (WIN_WIDTH // 2 - 130, WIN_HEIGHT // 2 + 50))
    else:
        bg_img = stage_background_images[manager.level-1]
        win.blit(bg_img, (0, 0))
        
        if manager.boss_active and manager.boss:
            manager.boss.draw(win)
            if hasattr(manager.boss, 'draw_attacks'): manager.boss.draw_attacks(win)
            if hasattr(manager.boss, 'draw_health_bar'): manager.boss.draw_health_bar(win, font)
        
        all_sprites.draw(win)
        draw_ui()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()