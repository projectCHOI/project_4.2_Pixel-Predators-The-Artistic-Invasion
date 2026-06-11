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
    
    # 🔍 보스 1 모듈 연동 성공!
    from M_title_stage_images.bosses.Stage_1_Boss import Stage1Boss

    print("보스 시스템을 포함한 모든 모듈 정상 연결 작동 중.")
except Exception as e:
    print(f"모듈 로드 중 오류 발생: {e}")
    pygame.quit()
    sys.exit()

def main():
    clock = pygame.time.Clock()
    res = ResourceManager()
    manager = GameManager(res)
    player = None
    
    # 타이머, 오디오, 보스 객체 바인딩 선언
    stage_start_time = 0
    bgm = BGMController()
    bgm.set_game_state("title") 
    
    # 보스 인스턴스화
    boss1 = Stage1Boss(res)
    
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

        # --- [1] 이벤트 처리 구역 ---
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
                    
                    # 상태 파라미터 완전 리셋
                    boss1.reset()
                    manager.boss_active = False
                    
                    stage_start_time = pygame.time.get_ticks()
                    bgm.set_game_state(f"stage_{manager.level}")
                    last_manager_level = manager.level
                    
            elif manager.game_active and player:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    from M_title_stage_images.entities.bullets import EnergyBall
                    
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
                    
                    for i in range(count):
                        offset = 0 if count == 1 else (i - (count - 1) / 2) * spread_interval
                        new_ball = EnergyBall(player.rect.center, res, mouse_pos, angle_offset=offset)
                        player_bullets.add(new_ball)

        # --- [2] 실시간 게임 메인 로직 업데이트 구역 ---
        if manager.game_active and player:
            if manager.level != last_manager_level:
                bgm.set_game_state(f"stage_{manager.level}")
                last_manager_level = manager.level
                stage_start_time = now
                boss1.reset()
                manager.boss_active = False

            player.handle_input()
            player.update()
            player_bullets.update()
            items_group.update()
            
            # 아이템 파싱 충돌 처리
            item_hits = pygame.sprite.spritecollide(player, items_group, True)
            for item in item_hits:
                item.apply_effect(player)
            
            # ⏰ 경과 시간 연산 처리 (초 단위)
            elapsed_seconds = (now - stage_start_time) // 1000

            # 🔍 보스 출격 타이밍 체크 센서 가동
            if manager.level == 1 and not manager.boss_active:
                boss1.check_appear(elapsed_seconds, manager.level)
                if boss1.boss_active:
                    manager.boss_active = True
                    enemies = [] # 필드의 잔여 몹들 완전 소거식 전환

            # [분기점 A] 보스전 활성화 시 로직 연산부
            if manager.boss_active and boss1.boss_active:
                boss1.move()
                boss1.attack()
                
                # 보스 공격 탄막이 플레이어에게 입힌 데미지 연산 받아오기
                dmg = boss1.update_attacks(player.rect, player.invincible)
                if dmg > 0:
                    player.take_damage(dmg)
                
                # 플레이어 에너지볼 탄환과 보스 본체의 피격 조건 검사 호출
                boss1.check_hit(player_bullets)
                
            # [분기점 B] 일반 필드 잡몹 스폰 파트
            elif not manager.boss_active:
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

            # 보스 사후 드롭된 보석 아이템 핸들링 및 스테이지 클리어 처리 구역
            if boss1.boss_defeated:
                boss1.update_attacks(player.rect, player.invincible) # 남은 잔여탄막 마저 이동처리
                if boss1.check_gem_collision(player.rect):
                    # 보석 획득 성공 -> 다음 스테이지 패스권 발급!
                    manager.level += 1
                    manager.boss_active = False

            # 일반 잡몹 객체 충돌 루프 연산
            purple_bullets = enemy_bomb.update_purple_bullets(purple_bullets, now, WIN_WIDTH, WIN_HEIGHT)
            updated_enemies = []
            for enemy in enemies:
                if enemy[2] == "move_and_shoot":
                    target = enemy[5]
                    dist = math.hypot(target[0] - enemy[0][0], target[1] - enemy[0][1])
                    if dist > 5:
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
                bgm.set_game_state("victory" if manager.game_over_reason == "victory" else "gameover")

        # --- [3] 화면 그래픽 자산 렌더링 그리기 구역 ---
        if not manager.game_active:
            if manager.game_over:
                win.fill(BLACK)
            else:
                win.blit(title_image, (0, 0))
        else:
            # 1. 고유 배경 출력
            bg_idx = manager.level - 1
            if bg_idx < len(stage_background_images):
                win.blit(stage_background_images[bg_idx], (0, 0))
            else:
                win.fill(BLACK)
            
            # 2. 오브젝트 리스트 드로잉
            for pb in purple_bullets:
                win.blit(pb["image"], pb["pos"])
            for enemy in enemies:
                win.blit(enemy[7], (enemy[0][0], enemy[0][1]))
            
            player_bullets.draw(win)
            items_group.draw(win)

            # 3. 보스전 그래픽 렌더링 파이프라인 연동
            if manager.boss_active:
                boss1.draw(win)
                boss1.draw_attacks(win)
                # boss1.draw_health_bar(win)
                boss_ui_font = pygame.font.SysFont("arial", 20, bold=True)
                boss1.draw_health_bar(win, boss_ui_font)         
            
            if boss1.boss_defeated:
                boss1.draw_gem(win)
                boss1.draw_attacks(win) # 보스 사후에도 남아 전진하는 유도탄 표시

            # 4. 플레이어 기체 및 하트 라이프 UI
            player.draw(win)
            player.draw_ui(win)

            # 5. KILLS 스코어 보드 (우측 상단)
            font = pygame.font.SysFont("arial", 30, bold=True)
            kill_text = font.render(f"KILLS: {manager.enemies_defeated}", True, WHITE)
            win.blit(kill_text, (WIN_WIDTH - kill_text.get_width() - 20, 20))

            # 6. 타임 타임 트래커 (상단 정중앙)
            elapsed_time = (now - stage_start_time) // 1000 
            mins, secs = elapsed_time // 60, elapsed_time % 60
            time_string = f"{mins:02d}:{secs:02d}"

            timer_font = pygame.font.SysFont("arial", 35, bold=True)
            timer_text = timer_font.render(time_string, True, YELLOW)
            win.blit(timer_text, ((WIN_WIDTH // 2) - (timer_text.get_width() // 2), 20))

        # --- [4] 그래픽 플립 반전 고정 조율 ---
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
