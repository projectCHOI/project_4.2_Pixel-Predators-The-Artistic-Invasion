import pygame
import sys
import os

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
    from M_title_stage_images.entities.items import Item, spawn_item_by_chance # 새 연결
    from M_title_stage_images.title_stage_images import title_image, stage_background_images
    from M_title_stage_images.enemy_behaviors.move_and_disappear import generate as gen_move_and_disappear
    
    print("아이템 시스템을 포함한 모든 모듈이 정상적으로 로드되었습니다.")
except Exception as e:
    print(f"모듈 로드 중 오류 발생: {e}")
    pygame.quit()
    sys.exit()

def main():
    clock = pygame.time.Clock()
    res = ResourceManager()
    manager = GameManager(res)
    player = None
    
    # 그룹 관리
    player_bullets = pygame.sprite.Group()
    items_group = pygame.sprite.Group() # 아이템 그룹 추가
    enemies = []
    
    enemy_last_spawn_time = 0
    enemy_spawn_interval = 3000
    
    run = True
    while run:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if not manager.game_active:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    player = Player(res)
                    player_bullets.empty()
                    items_group.empty() # 아이템 초기화
                    enemies = []
                    manager.start_game()
            
            elif manager.game_active and player:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    new_bullet = Bullet(player.rect.center, RED)
                    player_bullets.add(new_bullet)

        if manager.game_active and player:
            player.handle_input()
            player.update()
            player_bullets.update()
            items_group.update() # 아이템 이동 업데이트
            
            if not manager.boss_active:
                if now - enemy_last_spawn_time > enemy_spawn_interval:
                    try:
                        new_enemies_data = gen_move_and_disappear(manager.level, WIN_WIDTH, WIN_HEIGHT)
                        enemies.extend(new_enemies_data)
                    except Exception as e: print(f"Spawn Error: {e}")
                    enemy_last_spawn_time = now
            updated_enemies = []
            for enemy in enemies:
                enemy[0][0] += enemy[3][0] * enemy[4]
                enemy[0][1] += enemy[3][1] * enemy[4]
                
                enemy_rect = pygame.Rect(enemy[0][0], enemy[0][1], enemy[1], enemy[1])
                hit = False
                
                for bullet in player_bullets:
                    if enemy_rect.colliderect(bullet.rect):
                        bullet.kill()
                        manager.enemies_defeated += 1
                        
                        new_item = spawn_item_by_chance(enemy_rect.center, res)
                        if new_item:
                            items_group.add(new_item)
                        
                        hit = True
                        break
                
                if not hit and enemy_rect.colliderect(player.rect):
                    player.take_damage(1)
                    hit = True

                if not hit and -100 < enemy[0][0] < WIN_WIDTH + 100 and -100 < enemy[0][1] < WIN_HEIGHT + 100:
                    updated_enemies.append(enemy)
            
            enemies = updated_enemies
            item_hits = pygame.sprite.spritecollide(player, items_group, True)
            for item in item_hits:
                effect_msg = item.apply_effect(player)
                print(effect_msg) 
            manager.update(player)


if __name__ == "__main__":
    main()