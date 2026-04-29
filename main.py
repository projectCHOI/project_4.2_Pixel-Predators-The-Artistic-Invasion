import pygame
import sys
import os

pygame.init()
pygame.mixer.init()

try:
    from M_title_stage_images.config import WIN_WIDTH, WIN_HEIGHT, FPS, RED, BLACK, WHITE, YELLOW
except ImportError:
    WIN_WIDTH, WIN_HEIGHT = 1280, 720
    FPS = 30
    RED, BLACK, WHITE, YELLOW = (255,0,0), (0,0,0), (255,255,255), (255,255,0)

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("The Artistic Invasion")

try:
    from M_title_stage_images.resource_manager import ResourceManager
    from M_title_stage_images.game_manager import GameManager
    from M_title_stage_images.entities.player import Player
    from M_title_stage_images.entities.bullets import Bullet
    
    from M_title_stage_images.title_stage_images import title_image, stage_background_images
    from M_title_stage_images.enemy_behaviors.move_and_disappear import generate as gen_move_and_disappear
    
    print("모든 시스템과 이미지가 정상적으로 초기화되었습니다.")
except Exception as e:
    print(f"초기화 중 오류 발생: {e}")
    pygame.quit()
    sys.exit()

def main():
    clock = pygame.time.Clock()
    res = ResourceManager()
    manager = GameManager(res)
    player = None
    
    player_bullets = pygame.sprite.Group()
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
                    enemies = []
                    manager.start_game()
            
            elif manager.game_active and player:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    new_bullet = Bullet(player.rect.center, RED)
                    player_bullets.add(new_bullet)

