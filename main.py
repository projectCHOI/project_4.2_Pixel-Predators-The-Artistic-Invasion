import pygame
import sys
import os
import math

pygame.init()
pygame.mixer.init()

try:
    from M_title_stage_images.config import *
except ImportError:
    WIN_WIDTH, WIN_HEIGHT, FPS = 1280, 720, 30
    RED, BLACK, WHITE, YELLOW = (255,0,0), (0,0,0), (255,255,255), (255,255,0)

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("The Artistic Invasion")

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
    
    # 🔍 전체 6개 스테이지 보스 모듈 완벽 연결!
    from M_title_stage_images.bosses.Stage_1_Boss import Stage1Boss
    from M_title_stage_images.bosses.Stage_2_Boss import Stage2Boss
    from M_title_stage_images.bosses.Stage_3_Boss import Stage3Boss
    from M_title_stage_images.bosses.Stage_4_Boss import Stage4Boss
    from M_title_stage_images.bosses.Stage_5_Boss import Stage5Boss
    from M_title_stage_images.bosses.Stage_6_Boss import Stage6Boss

    print("전체 보스모듈 연결")
except Exception as e:
    print(f"모듈 로드 중 오류 발생: {e}")
    pygame.quit()
    sys.exit()

def main():
    clock = pygame.time.Clock()
    res = ResourceManager()
    manager = GameManager(res)
    player = None
    
    stage_start_time = 0
    bgm = BGMController()
    bgm.set_game_state("title") 
    
    # 전체 보스 인스턴스 테이블 (스테이지 1~6)
    bosses = {
        1: Stage1Boss(res),
        2: Stage2Boss(res),
        3: Stage3Boss(res),
        4: Stage4Boss(res),
        5: Stage5Boss(res),
        6: Stage6Boss(res)
    }
    
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
                    
                    for b in bosses.values():
                        b.reset()
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

        # --- [2] 게임 메인 로직 업데이트 ---
        if manager.game_active and player:
            current_boss = bosses.get(manager.level)

            if manager.level != last_manager_level:
                bgm.set_game_state(f"stage_{manager.level}")
                last_manager_level = manager.level
                stage_start_time = now
                if current_boss:
                    current_boss.reset()
                manager.boss_active = False

            player.handle_input()
            player.update()
            player_bullets.update()
            items_group.update()
            
            item_hits = pygame.sprite.spritecollide(player, items_group, True)
            for item in item_hits:
                item.apply_effect(player)
            
            elapsed_seconds = (now - stage_start_time) // 1000

            # 🔍 보스 출격 센서 체크
            if current_boss and not manager.boss_active:
                current_boss.check_appear(elapsed_seconds, manager.level)
                if current_boss.boss_active:
                    manager.boss_active = True
                    enemies = []

            # [분기 A] 보스전 업데이트
            if manager.boss_active and current_boss and current_boss.boss_active:
                current_boss.move()
                current_boss.attack()
                
                dmg = current_boss.update_attacks(player.rect, player.invincible)
                if dmg > 0:
                    player.take_damage(dmg)
                
                current_boss.check_hit(player_bullets)
                
            # [분기 B] 일반 잡몹 스폰
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

            if current_boss and current_boss.boss_defeated:
                current_boss.update_attacks(player.rect, player.invincible)
                if current_boss.check_gem_collision(player.rect):
                    if manager.level >= 6: # 마지막 6보스 격파 시 최종 승리!
                        manager.game_active = False
                        manager.game_over = True
                        manager.game_over_reason = "victory"
                    else:
                        manager.level += 1
                        manager.boss_active = False
