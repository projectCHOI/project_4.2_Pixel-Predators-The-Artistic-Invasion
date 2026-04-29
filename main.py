import pygame
import sys
import os

# --- [STEP 1] 기초 초기화 및 화면 설정 (최우선) ---
pygame.init()
pygame.mixer.init()

# 기본 설정값 (임포트 오류 방지용 예외처리 포함)
try:
    from M_title_stage_images.config import WIN_WIDTH, WIN_HEIGHT, FPS, RED, BLACK, WHITE, YELLOW
except ImportError:
    WIN_WIDTH, WIN_HEIGHT = 1280, 720
    FPS = 30
    RED, BLACK, WHITE, YELLOW = (255,0,0), (0,0,0), (255,255,255), (255,255,0)

# 화면 생성 - 이 코드가 아래의 리소스 임포트보다 먼저 실행되어야 함
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("The Artistic Invasion")

# --- [STEP 2] 리소스 및 클래스 모듈 임포트 ---
try:
    from M_title_stage_images.resource_manager import ResourceManager
    from M_title_stage_images.game_manager import GameManager
    from M_title_stage_images.entities.player import Player
    from M_title_stage_images.entities.bullets import Bullet, EnergyBall # 새 연결
    from M_title_stage_images.title_stage_images import title_image, stage_background_images
    from M_title_stage_images.enemy_behaviors.move_and_disappear import generate as gen_move_and_disappear
    
    print("공격 시스템을 포함한 모든 모듈이 정상적으로 로드되었습니다.")
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
    enemy_projectiles = pygame.sprite.Group() # EnergyBall 등을 위한 그룹
    enemies = []
    
    enemy_last_spawn_time = 0
    enemy_spawn_interval = 3000

    run = True
    while run:
        now = pygame.time.get_ticks()

        # --- A. 이벤트 처리 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if not manager.game_active:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    player = Player(res)
                    player_bullets.empty()
                    enemy_projectiles.empty()
                    enemies = []
                    manager.start_game()
            
            elif manager.game_active and player:
                # 일반 탄환 발사
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    new_bullet = Bullet(player.rect.center, RED)
                    player_bullets.add(new_bullet)

        # --- B. 게임 로직 ---
        if manager.game_active and player:
            player.handle_input()
            player.update()
            
            # 모든 투사체 업데이트
            player_bullets.update()
            enemy_projectiles.update()
            
            # 적 스폰 로직
            if not manager.boss_active:
                if now - enemy_last_spawn_time > enemy_spawn_interval:
                    try:
                        new_enemies_data = gen_move_and_disappear(manager.level, WIN_WIDTH, WIN_HEIGHT)
                        enemies.extend(new_enemies_data)
                    except Exception as spawn_error:
                        print(f"적 생성 오류: {spawn_error}")
                    enemy_last_spawn_time = now

            # 적 업데이트 및 충돌 체크
            updated_enemies = []
            for enemy in enemies:
                enemy[0][0] += enemy[3][0] * enemy[4]
                enemy[0][1] += enemy[3][1] * enemy[4]
                
                enemy_rect = pygame.Rect(enemy[0][0], enemy[0][1], enemy[1], enemy[1])
                hit = False
                
                # 플레이어 탄환 vs 적
                for bullet in player_bullets:
                    if enemy_rect.colliderect(bullet.rect):
                        bullet.kill()
                        manager.enemies_defeated += 1
                        hit = True
                        break
                
                # 적 vs 플레이어 직접 충돌
                if not hit and enemy_rect.colliderect(player.rect):
                    player.take_damage(1)
                    hit = True

                if not hit:
                    if -100 < enemy[0][0] < WIN_WIDTH + 100 and -100 < enemy[0][1] < WIN_HEIGHT + 100:
                        updated_enemies.append(enemy)
            
            enemies = updated_enemies
            manager.update(player)

        # --- C. 화면 그리기 ---
        if not manager.game_active:
            if manager.game_over:
                win.fill(BLACK)
                # (중략: 게임 오버 텍스트 출력)
            else:
                win.blit(title_image, (0, 0))
        else:
            # 배경
            bg_idx = manager.level - 1
            if bg_idx < len(stage_background_images):
                win.blit(stage_background_images[bg_idx], (0, 0))
            
            # 적군
            for enemy in enemies:
                win.blit(enemy[7], (enemy[0][0], enemy[0][1]))
            
            # 투사체 및 플레이어
            player_bullets.draw(win)
            enemy_projectiles.draw(win)
            player.draw(win)

            # UI
            font = pygame.font.SysFont("arial", 25)
            ui_text = font.render(f"STAGE {manager.level} | LIFE: {player.health} | KILLS: {manager.enemies_defeated}", True, WHITE)
            win.blit(ui_text, (20, 20))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()