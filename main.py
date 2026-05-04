import pygame
import sys
import os
import math

# --- [STEP 1] 기초 초기화 및 화면 설정 ---
pygame.init()
pygame.mixer.init()

try:
    from M_title_stage_images.config import *
except ImportError:
    WIN_WIDTH, WIN_HEIGHT, FPS = 1280, 720, 30
    RED, BLACK, WHITE, YELLOW = (255,0,0), (0,0,0), (255,255,255), (255,255,0)

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("The Artistic Invasion")

# --- [STEP 2] 모듈 임포트 ---
try:
    from M_title_stage_images.resource_manager import ResourceManager
    from M_title_stage_images.game_manager import GameManager
    from M_title_stage_images.entities.player import Player
    from M_title_stage_images.entities.bullets import Bullet
    from M_title_stage_images.entities.items import spawn_item_by_chance
    from M_title_stage_images.title_stage_images import title_image, stage_background_images
    from M_title_stage_images.enemy_behaviors.move_and_disappear import generate as gen_move_and_disappear
    import M_title_stage_images.enemy_behaviors.bomb as enemy_bomb
    
    # 새로운 연결: 군집형 적 로직
    import M_title_stage_images.enemy_behaviors.group_unit as enemy_group
    
    print("모든 적 시스템(일반, 폭탄, 군집)이 연결되었습니다.")
except Exception as e:
    print(f"모듈 로드 중 오류 발생: {e}")
    pygame.quit()
    sys.exit()

def main():
    clock = pygame.time.Clock()
    res = ResourceManager()
    manager = GameManager(res)
    player = None
    
    player_bullets = pygame.sprite.Group()
    items_group = pygame.sprite.Group()
    enemies = []
    purple_bullets = []
    
    # 스폰 타이머 관리
    last_spawn_times = {"normal": 0, "bomb": 0, "group": 0}
    intervals = {"normal": 3000, "bomb": 5000, "group": 8000} # 군집 적은 8초마다 시도

    run = True
    while run:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
            
            if not manager.game_active:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    player = Player(res)
                    player_bullets.empty()
                    items_group.empty()
                    enemies = []
                    purple_bullets = []
                    manager.start_game()
            elif manager.game_active and player:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    player_bullets.add(Bullet(player.rect.center, RED))

        if manager.game_active and player:
            player.handle_input()
            player.update()
            player_bullets.update()
            items_group.update()
            
            # 1. 적 스폰 (일반, 폭탄, 군집)
            if not manager.boss_active:
                if now - last_spawn_times["normal"] > intervals["normal"]:
                    enemies.extend(gen_move_and_disappear(manager.level, WIN_WIDTH, WIN_HEIGHT))
                    last_spawn_times["normal"] = now
                if now - last_spawn_times["bomb"] > intervals["bomb"]:
                    enemies.extend(enemy_bomb.generate(manager.level, WIN_WIDTH, WIN_HEIGHT, player.rect.center))
                    last_spawn_times["bomb"] = now
                if now - last_spawn_times["group"] > intervals["group"]:
                    enemies.extend(enemy_group.generate(manager.level, WIN_WIDTH, WIN_HEIGHT))
                    last_spawn_times["group"] = now

            purple_bullets = enemy_bomb.update_purple_bullets(purple_bullets, now, WIN_WIDTH, WIN_HEIGHT)

            # 2. 적 업데이트 및 충돌
            updated_enemies = []
            for enemy in enemies:
                # [특수 로직] 군집형 적의 사인파 이동 처리
                if enemy[2] == "group_unit":
                    amplitude = 50
                    t = (now - enemy[14]) / 500
                    # x = 기준x + 진폭 * sin(시간 + 개별오프셋)
                    enemy[0][0] = enemy[13][0] + amplitude * math.sin(t + enemy[12])
                    # y = 기준y + 속도 * 시간
                    enemy[0][1] = enemy[13][1] + enemy[4] * (now - enemy[14]) / 16 # 16ms 기준 보정
                else:
                    # 일반/폭탄 적 이동
                    enemy[0][0] += enemy[3][0] * enemy[4]
                    enemy[0][1] += enemy[3][1] * enemy[4]
                
                enemy_rect = pygame.Rect(enemy[0][0], enemy[0][1], enemy[1], enemy[1])
                hit = False
                
                for bullet in player_bullets:
                    if enemy_rect.colliderect(bullet.rect):
                        bullet.kill()
                        manager.enemies_defeated += 1
                        if enemy[2] == "bomb":
                            purple_bullets.extend(enemy_bomb.generate_purple_bullets(enemy_rect.center))
                        new_item = spawn_item_by_chance(enemy_rect.center, res)
                        if new_item: items_group.add(new_item)
                        hit = True
                        break
                
                if not hit and enemy_rect.colliderect(player.rect):
                    player.take_damage(1)
                    if enemy[2] == "bomb":
                        purple_bullets.extend(enemy_bomb.generate_purple_bullets(enemy_rect.center))
                    hit = True

                if not hit and -200 < enemy[0][1] < WIN_HEIGHT + 200:
                    updated_enemies.append(enemy)
            
            enemies = updated_enemies
            
            # 파편 충돌 및 아이템 획득
            for pb in purple_bullets[:]:
                if pygame.Rect(pb["pos"][0], pb["pos"][1], 20, 20).colliderect(player.rect):
                    player.take_damage(1)
                    purple_bullets.remove(pb)
            
            pygame.sprite.spritecollide(player, items_group, True)
            manager.update(player)

        # --- C. 화면 그리기 ---
        if not manager.game_active:
            # (게임 오버/타이틀 그리기 생략 - 이전과 동일)
            if manager.game_over: win.fill(BLACK)
            else: win.blit(title_image, (0, 0))
        else:
            bg_idx = manager.level - 1
            if bg_idx < len(stage_background_images): win.blit(stage_background_images[bg_idx], (0, 0))
            
            for pb in purple_bullets: win.blit(pb["image"], pb["pos"])
            for enemy in enemies: win.blit(enemy[7], (enemy[0][0], enemy[0][1]))
            
            player_bullets.draw(win)
            items_group.draw(win)
            player.draw(win)
            
            # UI (KILLS 표시 포함)
            font = pygame.font.SysFont("arial", 25)
            ui_text = font.render(f"STAGE {manager.level} | KILLS: {manager.enemies_defeated} | LIFE: {player.health}", True, WHITE)
            win.blit(ui_text, (20, 20))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()