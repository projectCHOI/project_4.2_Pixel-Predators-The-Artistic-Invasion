# 모듈 테스트
import pygame
import random
import math
print

# Import the Stage_1_Boss module
from Stage_Boss.Stage_1_Boss import Stage1Boss

pygame.init()

# 윈도우 설정
win = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("The Artistic Invasion")

# 이미지 로드
title_image = pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_cover/Cover_The_Artistic_Invasion_Bright_1210x718.JPG")
title_image = pygame.transform.scale(title_image, (1280, 720))

stage_images = [
    (r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage1_World_A.JPG",
     r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage1_World_B.JPG"),
    # Add other stage images here...
]

# 화면 크기에 맞게 이미지 스케일 조정
stage_intro_images = [pygame.transform.scale(pygame.image.load(img[0]), (1280, 720)) for img in stage_images]
stage_background_images = [pygame.transform.scale(pygame.image.load(img[1]), (1280, 720)) for img in stage_images]

# 플레이어 설정
player_image1 = pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_me1_png.png")
player_image2 = pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_me2_png.png")
player_image1 = pygame.transform.scale(player_image1, (40, 40))
player_image2 = pygame.transform.scale(player_image2, (40, 40))
player_image = player_image1

player_speed = 10
original_player_speed = player_speed

# Set up the Stage 1 Boss
stage1_boss = Stage1Boss()

# Other game settings and variables
run = True
game_active = False
game_over = False
game_over_reason = None
current_health = 4
level = 1
max_level = 12
player_pos = [640 - 20, 360 - 20]

# Function to draw objects (Updated for boss)
def draw_objects():
    win.blit(stage_background_images[level - 1], (0, 0))  # 배경을 전체 화면에 그리기
    
    # Draw player
    win.blit(player_image, (player_pos[0], player_pos[1]))

    # Draw boss
    stage1_boss.draw(win)
    stage1_boss.draw_attacks(win)
    
    pygame.display.update()

# Main game loop
while run:
    if not game_active:
        if not game_over:
            win.blit(title_image, (0, 0))
            pygame.display.update()
        else:
            # Handle game over
            pass
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Reset the game
                    game_active = True
                    level = 1
                    current_health = 4
                    stage1_boss.reset()
                    player_pos = [640 - 20, 360 - 20]
                    start_ticks = pygame.time.get_ticks()

    else:
        mouse_pos = pygame.mouse.get_pos()
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000  # 초 계산
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Handle player attacks (add to a list or modify as needed)
                pass

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_pos[0] -= player_speed
        if keys[pygame.K_d]:
            player_pos[0] += player_speed
        if keys[pygame.K_w]:
            player_pos[1] -= player_speed
        if keys[pygame.K_s]:
            player_pos[1] += player_speed

        # Keep the player on screen
        player_pos[0] = max(0, min(player_pos[0], 1240))
        player_pos[1] = max(0, min(player_pos[1], 680))

        # Update Stage 1 boss
        stage1_boss.check_appear(seconds)
        stage1_boss.move()
        stage1_boss.attack()
        stage1_boss.update_attacks(player_pos)

        # Draw everything
        draw_objects()

        pygame.time.delay(30)

pygame.quit()
