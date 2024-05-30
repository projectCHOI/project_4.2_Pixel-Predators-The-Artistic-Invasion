import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Red Box the cookie")

# Load images
title_image = pygame.image.load("C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_cover/Cover_The_Artistic_Invasion_Bright_1210x718.JPG")
title_image = pygame.transform.scale(title_image, (500, 500))

stage_images = [
    ("C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage1_World_A.JPG", 
     "C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage1_World_B.JPG"),
    ("C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage2_World_A.JPG", 
     "C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage2_World_B.JPG"),
    ("C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage3_World_A.JPG", 
     "C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage3_World_B.JPG"),
    ("C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage4_World_A.JPG", 
     "C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage4_World_B.JPG"),
    ("C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage5_World_A.JPG", 
     "C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage5_World_B.JPG"),
    ("C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage6_World_A.JPG", 
     "C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage6_World_B.JPG"),
    ("C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage7_World_A.JPG", 
     "C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage7_World_B.JPG"),
    ("C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage8_World_A.JPG", 
     "C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage8_World_B.JPG"),
    ("C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage9_World_A.JPG", 
     "C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage9_World_B.JPG"),
    ("C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage10_World_A.JPG", 
     "C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage10_World_B.JPG"),
    ("C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage11_World_A.JPG", 
     "C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage11_World_B.JPG"),
    ("C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage12_World_A.JPG", 
     "C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage12_World_B.JPG")
]

# Scale images to fit the screen
stage_intro_images = [pygame.transform.scale(pygame.image.load(img[0]), (500, 500)) for img in stage_images]
stage_background_images = [pygame.transform.scale(pygame.image.load(img[1]), (500, 500)) for img in stage_images]

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Player settings
player_size = 20
player_pos = [250, 250]
player_speed = 10

# Enemy settings
enemy_size = 10
enemy_speed = 5

# Star settings
star_size = 30
star_pos = [random.randint(0, 500-star_size), random.randint(0, 500-star_size)]
star_appear_time = 10

# Game settings
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 35)
level = 1
max_level = 12
run = True
game_active = False

def draw_objects(player_pos, enemies, star_pos, show_star, background_image):
    win.blit(background_image, (0, 0))
    pygame.draw.rect(win, WHITE, (player_pos[0], player_pos[1], player_size, player_size))
    for enemy_pos in enemies:
        pygame.draw.rect(win, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
    if show_star:
        pygame.draw.rect(win, YELLOW, (star_pos[0], star_pos[1], star_size, star_size))
    pygame.display.update()

def check_collision(player_pos, enemies):
    for enemy_pos in enemies:
        if (player_pos[0] < enemy_pos[0] < player_pos[0] + player_size or enemy_pos[0] < player_pos[0] < enemy_pos[0] + enemy_size) and \
           (player_pos[1] < enemy_pos[1] < player_pos[1] + player_size or enemy_pos[1] < player_pos[1] < enemy_pos[1] + enemy_size):
            return True
    return False

# Title screen
def title_screen():
    win.blit(title_image, (0, 0))
    pygame.display.update()

# Intro screen
def intro_screen(stage):
    win.blit(stage_intro_images[stage - 1], (0, 0))
    pygame.display.update()
    pygame.time.delay(3000)

# Game loop
while run:
    if not game_active:
        title_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_active = True
                    start_ticks = pygame.time.get_ticks()  # Start tick
                    intro_screen(level)
    else:
        enemies = [[random.randint(0, 500-enemy_size), random.randint(0, 500-enemy_size)] for _ in range(level)]
        show_star = False

        while run and len(enemies) == level:
            seconds = (pygame.time.get_ticks() - start_ticks) // 1000  # Calculate seconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_pos[0] > 0:
                player_pos[0] -= player_speed
            if keys[pygame.K_RIGHT] and player_pos[0] < 500 - player_size:
                player_pos[0] += player_speed
            if keys[pygame.K_UP] and player_pos[1] > 0:
                player_pos[1] -= player_speed
            if keys[pygame.K_DOWN] and player_pos[1] < 500 - player_size:
                player_pos[1] += player_speed

            if seconds > star_appear_time:
                show_star = True

            if show_star and (player_pos[0] < star_pos[0] < player_pos[0] + player_size or star_pos[0] < player_pos[0] < star_pos[0] + star_size) and \
               (player_pos[1] < star_pos[1] < player_pos[1] + player_size or star_pos[1] < player_pos[1] < star_pos[1] + star_size):
                level += 1
                if level > max_level:
                    win.fill((0, 0, 0))
                    text = font.render("coooool", True, WHITE)
                    win.blit(text, (150, 250))
                    pygame.display.update()
                    pygame.time.delay(3000)
                    run = False
                elif level <= len(stage_intro_images):
                    intro_screen(level)
                    start_ticks = pygame.time.get_ticks()  # Restart tick for new level
                    break

            if check_collision(player_pos, enemies):
                win.fill((0, 0, 0))
                text = font.render("Game Over", True, WHITE)
                win.blit(text, (150, 250))
                pygame.display.update()
                pygame.time.delay(3000)
                run = False

            draw_objects(player_pos, enemies, star_pos, show_star, stage_background_images[level - 1])
            clock.tick(30)

pygame.quit()
