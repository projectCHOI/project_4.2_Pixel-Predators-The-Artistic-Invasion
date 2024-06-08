import pygame
import random
import math

pygame.init()

# 윈도우 설정
win = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("The Artistic Invasion")

# Load images
title_image = pygame.image.load("C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_cover/Cover_The_Artistic_Invasion_Bright_1210x718.JPG")
title_image = pygame.transform.scale(title_image, (1200, 700))

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
stage_duration = 30  # 스테이지 진행 시간 (초)
invincible = False
invincible_start_time = 0
invincible_duration = 2000  # 무적 시간 (밀리초)

def draw_objects(player_pos, enemies, star_pos, show_star, background_image):
    win.blit(background_image, (0, 0))
    win.blit(player_image, (player_pos[0], player_pos[1]))  # 플레이어 이미지를 화면에 그리기
    for enemy_pos, enemy_size in enemies:
        pygame.draw.rect(win, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
    if show_star:
        pygame.draw.rect(win, YELLOW, (star_pos[0], star_pos[1], star_size, star_size))
    
    # Draw health
    for i in range(current_health):
        win.blit(health_image, (10 + i * 50, 650))
    
    pygame.display.update()

def check_collision(player_pos, enemies):
    for enemy_pos, enemy_size in enemies:
        if (player_pos[0] < enemy_pos[0] < player_pos[0] + player_width or enemy_pos[0] < player_pos[0] < enemy_pos[0] + enemy_size) and \
           (player_pos[1] < enemy_pos[1] < player_pos[1] + player_height or enemy_pos[1] < player_pos[1] < enemy_pos[1] + enemy_size):
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

# 스테이지 설정에 따라 적을 생성하는 함수
def generate_enemies(level):
    if level == 1:
        speed = 10
        directions = [(0, 1)]
        sizes = [40]
        num_enemies = random.randint(1, 2)
    elif level == 2:
        speed = 10
        directions = [(0, 1)]
        sizes = [40]
        num_enemies = random.randint(1, 3)
    elif level == 3:
        speed = 10
        directions = [(0, 1), (0, -1)]
        sizes = [40, 60]
        num_enemies = random.randint(1, 4)
    elif level == 4:
        speed = random.randint(10, 12)
        directions = [(0, 1), (0, -1)]
        sizes = [40, 60]
        num_enemies = random.randint(3, 8)
    elif level == 5:
        speed = random.randint(10, 12)
        directions = [(1, 0), (-1, 0)]
        sizes = [20, 40]
        num_enemies = random.randint(6, 16)
    elif level == 6:
        speed = random.randint(10, 14)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        sizes = [20, 40]
        num_enemies = random.randint(6, 20)
    elif level == 7:
        speed = random.randint(10, 16)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        sizes = [20, 40, 60]
        num_enemies = random.randint(6, 24)
    elif level == 8:
        speed = random.randint(10, 18)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        sizes = [20, 40, 60]
        num_enemies = random.randint(6, 26)
    elif level == 9:
        speed = random.randint(10, 18)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        sizes = [20, 40, 60]
        num_enemies = random.randint(8, 30)
    elif level == 10:
        speed = random.randint(10, 20)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        sizes = [20, 40, 60]
        num_enemies = random.randint(8, 30)
    elif level == 11:
        speed = random.randint(10, 20)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        sizes = [20, 40, 60]
        num_enemies = random.randint(10, 32)
    elif level == 12:
        speed = random.randint(10, 20)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        sizes = [20, 40, 60]
        num_enemies = random.randint(15, 32)

    enemies = []
    for _ in range(num_enemies):
        direction = random.choice(directions)
        size = random.choice(sizes)
        if direction == (0, 1):  # 상단에서
            pos = [random.randint(0, 1200-size), 0]
        elif direction == (0, -1):  # 하단에서
            pos = [random.randint(0, 1200-size), 700-size]
        elif direction == (1, 0):  # 좌측에서
            pos = [0, random.randint(0, 700-size)]
        elif direction == (-1, 0):  # 우측에서
            pos = [1200-size, random.randint(0, 700-size)]
        elif direction == (1, 1):  # 좌측 상단에서
            pos = [0, 0]
        elif direction == (1, -1):  # 좌측 하단에서
            pos = [0, 700-size]
        elif direction == (-1, 1):  # 우측 상단에서
            pos = [1200-size, 0]
        elif direction == (-1, -1):  # 우측 하단에서
            pos = [1200-size, 700-size]
        enemies.append((pos, size, direction, speed))

    return enemies

# 게임 루프
while run:
    if not game_active:
        title_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_active = True
                    player_pos = [600, 350]  # 플레이어를 중앙에 위치
                    enemies = []
                    show_star = False
                    star_pos = [random.randint(0, 1200 - star_size), random.randint(0, 700 - star_size)]
                    start_ticks = pygame.time.get_ticks()  # 시작 시간
                    intro_screen(level)
    else:
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000  # 초 계산
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_pos[0] -= player_speed
            player_image = player_image2
        if keys[pygame.K_d]:
            player_pos[0] += player_speed
            player_image = player_image1
        if keys[pygame.K_w]:
            player_pos[1] -= player_speed
            player_image = player_image1
        if keys[pygame.K_s]:
            player_pos[1] += player_speed
            player_image = player_image2

        if seconds > star_appear_time:
            show_star = True

        if show_star and (player_pos[0] < star_pos[0] < player_pos[0] + player_width or star_pos[0] < player_pos[0] < star_pos[0] + star_size) and \
           (player_pos[1] < star_pos[1] < player_pos[1] + player_height or star_pos[1] < player_pos[1] < star_pos[1] + star_size):
            level += 1
            if level > max_level:
                win.fill((0, 0, 0))
                text = font.render("Cool", True, WHITE)
                win.blit(text, (450, 350))
                pygame.display.update()
                pygame.time.delay(3000)
                run = False
            else:
                player_pos = [600, 350]  # 레벨 시작 시 플레이어를 중앙에 위치
                intro_screen(level)
                start_ticks = pygame.time.get_ticks()  # 새로운 레벨 시작 시간 초기화
                enemies = []
                show_star = False
                star_pos = [random.randint(0, 1200 - star_size), random.randint(0, 700 - star_size)]

        if seconds < stage_duration:
            if random.random() < 0.02:  # 2% 확률로 적 생성
                new_enemies = generate_enemies(level)
                enemies.extend(new_enemies)

        for enemy in enemies:
            pos, size, direction, speed = enemy
            pos[0] += direction[0] * speed
            pos[1] += direction[1] * speed

        if not invincible and check_collision(player_pos, [(enemy[0], enemy[1]) for enemy in enemies]):
            current_health -= 1
            invincible = True
            invincible_start_time = pygame.time.get_ticks()
            if current_health <= 0:
                win.fill((0, 0, 0))
                text = font.render("Game Over", True, WHITE)
                win.blit(text, (450, 350))
                pygame.display.update()
                pygame.time.delay(3000)
                run = False

        if invincible and pygame.time.get_ticks() - invincible_start_time > invincible_duration:
            invincible = False

        draw_objects(player_pos, [(enemy[0], enemy[1]) for enemy in enemies], star_pos, show_star, stage_background_images[level - 1])
        clock.tick(30)

pygame.quit()