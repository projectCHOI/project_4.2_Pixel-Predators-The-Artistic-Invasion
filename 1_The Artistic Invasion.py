import pygame
import random
import math

pygame.init()

# 윈도우 설정
win = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("The Artistic Invasion")

# Load images
title_image = pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_cover/Cover_The_Artistic_Invasion_Bright_1210x718.JPG")
title_image = pygame.transform.scale(title_image, (1200, 700))

stage_images = [
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage1_World_A.JPG", 
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage1_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage2_World_A.JPG", 
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project4.2_world/Stage2_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage3_World_A.JPG", 
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage3_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage4_World_A.JPG", 
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage4_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage5_World_A.JPG", 
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project4.2_world/Stage5_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage6_World_A.JPG", 
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project4.2_world/Stage6_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage7_World_A.JPG", 
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project4.2_world/Stage7_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage8_World_A.JPG", 
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project4.2_world/Stage8_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage9_World_A.JPG", 
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project4.2_world/Stage9_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage10_World_A.JPG", 
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project4.2_world/Stage10_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage11_World_A.JPG", 
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project4.2_world/Stage11_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage12_World_A.JPG", 
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project4.2_world/Stage12_World_B.JPG")
]

# Scale images to fit the screen
stage_intro_images = [pygame.transform.scale(pygame.image.load(img[0]), (1200, 700)) for img in stage_images]
stage_background_images = [pygame.transform.scale(pygame.image.load(img[1]), (1200, 700)) for img in stage_images]

# Load player images
player_width, player_height = 40, 40  # 크기
player_image1 = pygame.image.load(r"C:\Users\HOME\Desktop\새싹_교육\GitHub_CHOI\project_4.2_Pixel Predators-The Artistic Invasion\project4.2_mob\mob_me1_png.png")
player_image2 = pygame.image.load(r"C:\Users\HOME\Desktop\새싹_교육\GitHub_CHOI\project_4.2_Pixel Predators-The Artistic Invasion\project4.2_mob\mob_me2_png.png")
player_image1 = pygame.transform.scale(player_image1, (player_width, player_height))
player_image2 = pygame.transform.scale(player_image2, (player_width, player_height))

# Health settings
health_image = pygame.image.load(r"C:\Users\HOME\Desktop\새싹_교육\GitHub_CHOI\project_4.2_Pixel Predators-The Artistic Invasion\project4.2_mob\mob_png.png")
health_image = pygame.transform.scale(health_image, (40, 40))
max_health = 5
current_health = 3

# Initial player image
player_image = player_image1

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Player settings
player_speed = 10  # 속도 조정

# Star settings
star_size = 60  # 크기를 더 크게 조정
star_appear_time = 10

# Game settings
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 70)  # 폰트 크기 조정
level = 1
max_level = 12
run = True
game_active = False
stage_duration = 60  # 스테이지 진행 시간 (초)
invincible = False
invincible_start_time = 0
invincible_duration = 2000  # 무적 시간 (밀리초)

# Attack settings
attacks = []
attack_speed = 20
enemies_defeated = 0  # 제거된 적의 수

def draw_objects(player_pos, enemies, star_pos, show_star, background_image, mouse_pos):
    win.blit(background_image, (0, 0))
    win.blit(player_image, (player_pos[0], player_pos[1]))  # 플레이어 이미지를 화면에 그리기
    for enemy_pos, enemy_size in enemies:
        pygame.draw.rect(win, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
    if show_star:
        pygame.draw.rect(win, YELLOW, (star_pos[0], star_pos[1], star_size, star_size))
    
    # Draw attacks
    for attack in attacks:
        pygame.draw.line(win, RED, attack[0], attack[1], 3)
    
    # Draw mouse position
    pygame.draw.circle(win, RED, mouse_pos, 5)
    
    # Draw health
    for i in range(current_health):
        win.blit(health_image, (10 + i * 50, 650))
    
    # Draw enemies defeated
    text = font.render(f"{enemies_defeated}", True, WHITE)
    win.blit(text, (1100, 10))
    
    pygame.display.update()

def check_collision(player_pos, enemies):
    for enemy_pos, enemy_size in enemies:
        if (player_pos[0] < enemy_pos[0] < player_pos[0] + player_width or enemy_pos[0] < player_pos[0] < enemy_pos