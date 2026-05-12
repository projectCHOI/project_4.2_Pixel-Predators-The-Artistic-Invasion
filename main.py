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
    import M_title_stage_images.enemy_behaviors.group_unit as enemy_group
    import M_title_stage_images.enemy_behaviors.move_and_shoot as enemy_ambush
    from M_title_stage_images.assets.sounds.bgm_controller import BGMController

    print("오디오 시스템(BGM)을 포함한 모든 모듈 연결 완료.")
except Exception as e:
    print(f"모듈 로드 중 오류 발생: {e}")
    pygame.quit()
    sys.exit()

def main():
    clock = pygame.time.Clock()
    res = ResourceManager()
    manager = GameManager(res)
    player = None
    
    bgm = BGMController()
    bgm.set_game_state("title") 
    
    player_bullets = pygame.sprite.Group()
    items_group = pygame.sprite.Group()
    enemies = []
    purple_bullets = []
    
    last_spawn_times = {"normal": 0, "bomb": 0, "group": 0, "ambush": 0}
    intervals = {"normal": 3000, "bomb": 5000, "group": 8000, "ambush": 6000}
    last_manager_level = 1

    run = True
    while run:
        now = pygame.time.get_ticks()

        # [1] 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False
            
            if not manager.game_active:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    player = Player(res)
                    player_bullets.empty()
                    items_group.empty()
                    enemies = []
                    purple_bullets = []
                    manager.start_game()
                    bgm.set_game_state(f"stage_{manager.level}")
                    last_manager_level = manager.level
            elif manager.game_active and player:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

        if manager.game_active and player:
            if manager.level != last_manager_level:
                bgm.set_game_state(f"stage_{manager.level}")
                last_manager_level = manager.level

            player.handle_input()
            player.update()
            player_bullets.update()
            items_group.update()
            
            item_hits = pygame.sprite.spritecollide(player, items_group, True)
            for item in item_hits:
                item.apply_effect(player)
            
            # 적 스폰
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
                if now - last_spawn_times["ambush"] > intervals["ambush"]:
                    enemies.extend(enemy_ambush.generate(manager.level, WIN_WIDTH, WIN_HEIGHT))
                    last_spawn_times["ambush"] = now

            purple_bullets = enemy_bomb.update_purple_bullets(purple_bullets, now, WIN_WIDTH, WIN_HEIGHT)

            updated_enemies = []
            for enemy in enemies:
                if enemy[2] == "move_and_shoot":
                    target = enemy[5]
                    dist_to_target = math.hypot(target[0] - enemy[0][0], target[1] - enemy[0][1])
                    if dist_to_target > 5:
                        enemy[0][0] += enemy[3][0] * enemy[4]
                        enemy[0][1] += enemy[3][1] * enemy[4]
                    else:
                        enemy[4] = 0
                elif enemy[2] == "group_unit":
                    t = (now - enemy[14]) / 500
                    enemy[0][0] = enemy[13][0] + 50 * math.sin(t + enemy[12])
                    enemy[0][1] = enemy[13][1] + enemy[4] * (now - enemy[14]) / 16
                else:
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

                if not hit and -100 < enemy[0][0] < WIN_WIDTH + 100 and -100 < enemy[0][1] < WIN_HEIGHT + 100:
                    updated_enemies.append(enemy)
            
            enemies = updated_enemies
            manager.update(player)

            if manager.game_over:
                if manager.game_over_reason == "victory":
                    bgm.set_game_state("victory")
                else:
                    bgm.set_game_state("gameover")
        # [3] 화면 그리기
        if not manager.game_active:
            if manager.game_over:
                win.fill(BLACK)
            else:
                win.blit(title_image, (0, 0))
        else:
            bg_idx = manager.level - 1
            if bg_idx < len(stage_background_images):
                win.blit(stage_background_images[bg_idx], (0, 0))
            else:
                win.fill(BLACK)
            
            # 2. 적 및 탄환 그리기
            for pb in purple_bullets:
                win.blit(pb["image"], pb["pos"])
            for enemy in enemies:
                win.blit(enemy[7], (enemy[0][0], enemy[0][1]))
            
            player_bullets.draw(win)
            items_group.draw(win)

            # 3. 플레이어 및 라이프 UI 그리기
            player.draw(win)
            player.draw_ui(win)

            # 4. KILLS UI (우측 상단)
            font = pygame.font.SysFont("arial", 30, bold=True)
            kill_text = font.render(f"KILLS: {manager.enemies_defeated}", True, WHITE)
            win.blit(kill_text, (WIN_WIDTH - kill_text.get_width() - 20, 20))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()