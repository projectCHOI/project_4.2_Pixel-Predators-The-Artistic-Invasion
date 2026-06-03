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
    
    # 타이머 및 BGM 컨트롤러 초기화
    stage_start_time = 0
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

            # --- [1] 이벤트 처리 ---
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
                        
                        # 타이머 및 BGM 동기화 초기화
                        stage_start_time = pygame.time.get_ticks()
                        bgm.set_game_state(f"stage_{manager.level}")
                        last_manager_level = manager.level
                        
                elif manager.game_active and player:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        from M_title_stage_images.entities.bullets import EnergyBall
                        
                        # 플레이어의 파워 레벨 설정 매핑
                        power_configs = {
                            0: {"count": 1, "spread": 0},
                            1: {"count": 3, "spread": 15},
                            2: {"count": 5, "spread": 12},
                            3: {"count": 7, "spread": 10},
                            4: {"count": 9, "spread": 8}
                        }
                        
                        config = power_configs.get(player.power_level, {"count": 1, "spread": 0})
                        count = config["count"]
                        spread_interval = config["spread"]
                        
                        # 부채꼴 중앙 정렬 각도 계산 루프 사격
                        for i in range(count):
                            if count == 1:
                                offset = 0
                            else:
                                offset = (i - (count - 1) / 2) * spread_interval
                            
                            new_ball = EnergyBall(player.rect.center, res, mouse_pos, angle_offset=offset)
                            player_bullets.add(new_ball)

# --- [2] 게임 로직 업데이트 ---
        if manager.game_active and player:
            # 실시간 스테이지 변경 체크 및 타이머 초기화 리셋
            if manager.level != last_manager_level:
                bgm.set_game_state(f"stage_{manager.level}")
                last_manager_level = manager.level
                stage_start_time = now  # 스테이지 전환 시 타이머 0초 초기화

            player.handle_input()
            player.update()
            player_bullets.update()
            items_group.update()
            
            # 아이템 획득 메커니즘
            item_hits = pygame.sprite.spritecollide(player, items_group, True)
            for item in item_hits:
                item.apply_effect(player)
            
            # 적 스폰 매니징
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

            # 적 객체 핸들링 및 탄환 충돌
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

        # --- [3] 화면 그리기 ---
        if not manager.game_active:
            if manager.game_over:
                win.fill(BLACK)
            else:
                win.blit(title_image, (0, 0))
        else:
            # 1. 배경 출력
            bg_idx = manager.level - 1
            if bg_idx < len(stage_background_images):
                win.blit(stage_background_images[bg_idx], (0, 0))
            else:
                win.fill(BLACK)

            # 2. 엔티티 및 스플래시 탄환 그리기
            for pb in purple_bullets:
                win.blit(pb["image"], pb["pos"])
            for enemy in enemies:
                win.blit(enemy[7], (enemy[0][0], enemy[0][1]))
            
            player_bullets.draw(win)
            items_group.draw(win)

            # 3. 플레이어 기체 및 하트 라이프 UI 출력
            player.draw(win)
            player.draw_ui(win)
