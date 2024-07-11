import pygame
import random
import math

pygame.init()

# 윈도우 설정
win = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("The Artistic Invasion")

# 이미지 로드
title_image = pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_cover/Cover_The_Artistic_Invasion_Bright_1210x718.JPG")
title_image = pygame.transform.scale(title_image, (1200, 700))

stage_images = [
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage1_World_A.JPG", 
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/world_night sky_0.jpg"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage2_World_A.JPG", 
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/world_night sky_0.jpg"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage3_World_A.JPG", 
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/world_night sky_0.jpg"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage4_World_A.JPG", 
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/world_night sky_0.jpg"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage5_World_A.JPG", 
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/world_night sky_0.jpg"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage6_World_A.JPG", 
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/world_night sky_0.jpg"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage7_World_A.JPG", 
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/world_night sky_0.jpg"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage8_World_A.JPG", 
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/world_night sky_0.jpg"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage9_World_A.JPG", 
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/world_night sky_0.jpg"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage10_World_A.JPG", 
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/world_night sky_0.jpg"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage11_World_A.JPG", 
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/world_night sky_0.jpg"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage12_World_A.JPG", 
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/world_night sky_0.jpg")
]

# 화면 크기에 맞게 이미지 스케일 조정
stage_intro_images = [pygame.transform.scale(pygame.image.load(img[0]), (1200, 700)) for img in stage_images]
stage_background_images = [pygame.transform.scale(pygame.image.load(img[1]), (1200, 700)) for img in stage_images]

# 플레이어 이미지 로드
player_width, player_height = 40, 40  # 크기
player_image1 = pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_me1_png.png")
player_image2 = pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_me2_png.png")
player_image1 = pygame.transform.scale(player_image1, (player_width, player_height))
player_image2 = pygame.transform.scale(player_image2, (player_width, player_height))

# 충돌 시 이미지 로드(duration=시간)
collision_images = {
    3: {"image": pygame.transform.scale(pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_death_1.png"), (player_width, player_height)), "duration": 5000},
    2: {"image": pygame.transform.scale(pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_death_2.png"), (player_width, player_height)), "duration": 5000},
    1: {"image": pygame.transform.scale(pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_death_3.png"), (player_width, player_height)), "duration": 5000}
}

# Health 설정
health_image = pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_Life.png")
health_image = pygame.transform.scale(health_image, (40, 40))
max_health = 5
current_health = 3

# 스피드 아이템 설정
speed_item_image = pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_4_Quickly.png")
speed_item_image = pygame.transform.scale(speed_item_image, (40, 40))
speed_item_pos = None
speed_item_active = False
speed_item_start_time = 0
speed_item_duration = 20000  # 20초
speed_increase_amount = 10  # 스피드 증가량
speed_item_chance = 0.1  # 10% 확률

# 공격력 증가 아이템 설정
power_item_image = pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_1_Life.png")
power_item_image = pygame.transform.scale(power_item_image, (30, 30))
power_item_pos = None
power_item_active = 0  # 공격력 증가 아이템 획득 수
power_item_chance = 0.1  # 10% 확률

# 체력 회복 아이템 설정
heal_item_images = [
    pygame.transform.scale(pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_Fruit_a.png"), (60, 60)),
    pygame.transform.scale(pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_Fruit_b.png"), (60, 60)),
    pygame.transform.scale(pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_Fruit_c.png"), (60, 60)),
    pygame.transform.scale(pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_Fruit_d.png"), (60, 60))
]
heal_item_pos = None
current_heal_item_image = None
heal_item_chance = 0.1  # 10% 확률

# 초기 플레이어 이미지
player_image = player_image1

# 색상 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)  # 색상을 검은색으로 설정

# 플레이어 설정
player_speed = 10  # 속도 조정
original_player_speed = player_speed

# 에너지 볼 설정
energy_balls = []

# 별 설정
star_size = 60  # 크기를 더 크게 조정
star_images = [
    r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_1_RJewelry.png",
    r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_png.png",
    r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_2_OJewelry.png",
    r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_png.png",
    r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_3_YJewelry.png",
    r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_png.png",
    r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_4_GJewelry.png",
    r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_png.png",
    r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_5_BJewelry.png",
    r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_png.png",
    r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_6_IJewelry.png",
    r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_png.png",
    r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_7_VJewelry.png"
]
star_appear_time = 10

# 게임 설정
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 50)  # 폰트 크기를 50으로 설정
level = 1
max_level = 12
run = True
game_active = False
stage_duration = 60  # 스테이지 진행 시간 (초)
invincible = False
invincible_start_time = 0
invincible_duration = 3000  # 무적 시간 (밀리초)

# 충돌 효과 설정
collision_effect_start_time = 0
collision_image = None
collision_effect_duration = 0

# 공격 설정
attacks = []
attack_speed = 20
enemies_defeated = 0  # 제거된 적의 수

# 마우스 클릭 추적
mouse_down_time = 0
mouse_held = False

# 획득한 별 이미지 추적
collected_stars = []

def draw_objects(player_pos, enemies, star_pos, show_star, background_image, mouse_pos, star_image, collision_image=None, speed_item_pos=None, power_item_pos=None, heal_item_pos=None, heal_item_image=None):
    win.blit(background_image, (0, 0))
    win.blit(player_image, (player_pos[0], player_pos[1]))  # 플레이어 이미지를 화면에 그리기
    if collision_image:
        win.blit(collision_image, (player_pos[0], player_pos[1]))
    for enemy in enemies:
        enemy_pos, enemy_size, enemy_type = enemy[:3]
        if enemy_type == "move_and_shoot":
            pygame.draw.rect(win, YELLOW, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
        else:
            pygame.draw.rect(win, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
    if show_star:
        win.blit(star_image, (star_pos[0], star_pos[1]))
    if speed_item_pos:
        win.blit(speed_item_image, speed_item_pos)
    if power_item_pos:
        win.blit(power_item_image, power_item_pos)
    if heal_item_pos and heal_item_image:
        win.blit(heal_item_image, heal_item_pos)
    
    # 에너지 볼 그리기
    for ball in energy_balls:
        color = YELLOW if ball[2] == "yellow" else GREEN
        pygame.draw.circle(win, color, (ball[0], ball[1]), 5)
    
    # 공격 그리기
    for attack in attacks:
        pygame.draw.line(win, RED, attack[0], attack[1], attack[2])
    
    # 마우스 위치 그리기
    pygame.draw.circle(win, RED, mouse_pos, 5)
    
    # 체력 그리기
    for i in range(current_health):
        win.blit(health_image, (10 + i * 50, 650))
    
    # 제거된 적의 수 그리기
    text = font.render(f"{enemies_defeated}", True, BLACK)
    win.blit(text, (1100, 10))
    
    # 획득한 별 그리기
    for idx, collected_star in enumerate(collected_stars):
        win.blit(collected_star, (10 + idx * (star_size + 5), 10))
    
    pygame.display.update()

def check_collision(player_pos, enemies):
    for enemy_pos, enemy_size, _ in enemies:
        if (player_pos[0] < enemy_pos[0] < player_pos[0] + player_width or enemy_pos[0] < player_pos[0] < enemy_pos[0] + enemy_size) and \
           (player_pos[1] < enemy_pos[1] < player_pos[1] + player_height or player_pos[1] < enemy_pos[1] < player_pos[1] + enemy_size):
            return True
    return False

def check_attack_collision(attack_start, attack_end, enemy_pos, enemy_size):
    ex, ey = enemy_pos
    sx, sy = attack_start
    ex2, ey2 = ex + enemy_size, ey + enemy_size

    # 광선과 적의 충돌 체크
    if min(sx, attack_end[0]) <= ex2 and max(sx, attack_end[0]) >= ex and \
       min(sy, attack_end[1]) <= ey2 and max(sy, attack_end[1]) >= ey:
        return True
    return False

def check_energy_ball_collision(ball_pos, player_pos):
    bx, by = ball_pos
    px, py = player_pos
    if px < bx < px + player_width and py < by < py + player_height:
        return True
    return False

# 타이틀 화면
def title_screen():
    win.blit(title_image, (0, 0))
    pygame.display.update()

# 인트로 화면
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
        if size == 40:
            enemy_type = "move_and_disappear"
        elif size == 60:
            target_pos = [random.randint(100, 1100), random.randint(100, 600)]  # 랜덤한 화면 내 특정 장소
            enemy_type = "move_and_shoot"
            direction = [target_pos[0] - pos[0], target_pos[1] - pos[1]]
            length = math.hypot(direction[0], direction[1])
            direction = [direction[0] / length, direction[1] / length]
        elif size == 20:
            enemy_type = "approach_and_shoot"
        enemies.append([pos, size, enemy_type, direction, speed, target_pos if size == 60 else None, 0])  # list로 변경 및 target_pos 및 공격 횟수 추가

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
                    star_image = pygame.transform.scale(pygame.image.load(star_images[level - 1]), (star_size, star_size))
                    start_ticks = pygame.time.get_ticks()  # 시작 시간
                    intro_screen(level)
    else:
        mouse_pos = pygame.mouse.get_pos()
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000  # 초 계산
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_down_time = pygame.time.get_ticks()
                mouse_held = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_held = False
                hold_duration = pygame.time.get_ticks() - mouse_down_time
                attack_start = (player_pos[0] + player_width // 2, player_pos[1] + player_height // 2)
                attack_end = mouse_pos
                attack_thickness = 6 if hold_duration >= 2000 else 3
                if power_item_active == 0:
                    attacks.append((attack_start, attack_end, attack_thickness))
                elif power_item_active == 1:
                    offset = 5
                    attacks.append((attack_start, (attack_end[0] + offset, attack_end[1] + offset), attack_thickness))
                    attacks.append((attack_start, (attack_end[0] - offset, attack_end[1] - offset), attack_thickness))
                elif power_item_active == 2:
                    offset = 10
                    attacks.append((attack_start, (attack_end[0] + offset, attack_end[1] + offset), attack_thickness))
                    attacks.append((attack_start, attack_end, attack_thickness))
                    attacks.append((attack_start, (attack_end[0] - offset, attack_end[1] - offset), attack_thickness))
                elif power_item_active == 3:
                    offset = 15
                    attacks.append((attack_start, (attack_end[0] + offset, attack_end[1] + offset), attack_thickness))
                    attacks.append((attack_start, (attack_end[0] + offset // 2, attack_end[1] + offset // 2), attack_thickness))
                    attacks.append((attack_start, (attack_end[0] - offset // 2, attack_end[1] - offset // 2), attack_thickness))
                    attacks.append((attack_start, (attack_end[0] - offset, attack_end[1] - offset), attack_thickness))

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

        # 플레이어가 화면 밖으로 나가지 않도록 위치 조정
        if player_pos[0] < 0:
            player_pos[0] = 0
        if player_pos[0] > 1200 - player_width:
            player_pos[0] = 1200 - player_width
        if player_pos[1] < 0:
            player_pos[1] = 0
        if player_pos[1] > 700 - player_height:
            player_pos[1] = 700 - player_height

        if seconds > star_appear_time:
            show_star = True

        if show_star and (player_pos[0] < star_pos[0] < player_pos[0] + player_width or star_pos[0] < player_pos[0] < star_pos[0] + star_size) and \
           (player_pos[1] < star_pos[1] < player_pos[1] + player_height or player_pos[1] < star_pos[1] < star_pos[1] + star_size):
            collected_stars.append(star_image)  # 획득한 별 이미지 추가
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
                star_image = pygame.transform.scale(pygame.image.load(star_images[level - 1]), (star_size, star_size))

        if seconds < stage_duration:
            if random.random() < 0.02:  # 2% 확률로 적 생성
                new_enemies = generate_enemies(level)
                enemies.extend(new_enemies)

        for enemy in enemies:
            pos, size, enemy_type, direction, speed, target_pos, shots_fired = enemy
            if enemy_type == "move_and_disappear":
                pos[0] += direction[0] * speed
                pos[1] += direction[1] * speed
            elif enemy_type == "move_and_shoot":
                if target_pos:
                    distance_to_target = math.hypot(target_pos[0] - pos[0], target_pos[1] - pos[1])
                    if distance_to_target > speed:
                        pos[0] += direction[0] * speed
                        pos[1] += direction[1] * speed
                    else:
                        pos[0], pos[1] = target_pos
                        enemy[5] = None  # target_pos를 None으로 설정하여 적이 멈추게 함
                        direction = [0, 0]  # 위치를 고정
                else:
                    if shots_fired < 5:
                        if pygame.time.get_ticks() % 1000 < 50:  # 1초마다 공격
                            attack_dir = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
                            energy_balls.append([pos[0] + size // 2, pos[1] + size // 2, "yellow", attack_dir])
                            enemy[6] += 1  # 공격 횟수 증가
            elif enemy_type == "approach_and_shoot":
                if pygame.time.get_ticks() % 5000 < 2500:
                    target_pos = [player_pos[0], player_pos[1]]
                    direction = [target_pos[0] - pos[0], target_pos[1] - pos[1]]
                    length = math.hypot(direction[0], direction[1])
                    direction = [direction[0] / length, direction[1] / length]
                    pos[0] += direction[0] * speed
                    pos[1] += direction[1] * speed
                    if length < 50:
                        energy_balls.append([pos[0], pos[1], "green", direction])
                else:
                    direction = [random.choice([-1, 1]), random.choice([-1, 1])]
                    pos[0] += direction[0] * speed
                    pos[1] += direction[1] * speed

        if not invincible and check_collision(player_pos, [(enemy[0], enemy[1], enemy[2]) for enemy in enemies]):
            current_health -= 1
            invincible = True
            invincible_start_time = pygame.time.get_ticks()
            collision_effect_start_time = pygame.time.get_ticks()
            if current_health <= 0:
                collision_image = collision_images[1]["image"]
                collision_effect_duration = collision_images[1]["duration"]
                win.fill((0, 0, 0))
                text = font.render("Game Over", True, WHITE)
                win.blit(text, (450, 350))
                win.blit(collision_image, (player_pos[0], player_pos[1]))  # 충돌 이미지 그리기
                pygame.display.update()
                pygame.time.delay(collision_effect_duration)
                run = False
            elif current_health == 2:
                collision_image = collision_images[3]["image"]
                collision_effect_duration = collision_images[3]["duration"]
            elif current_health == 1:
                collision_image = collision_images[2]["image"]
                collision_effect_duration = collision_images[2]["duration"]

        if invincible and pygame.time.get_ticks() - invincible_start_time > invincible_duration:
            invincible = False

        # 충돌 이미지 표시 시간 체크
        if pygame.time.get_ticks() - collision_effect_start_time < collision_effect_duration:
            collision_image = collision_image
        else:
            collision_image = None

        # 마우스 클릭
        new_attacks = []
        for attack in attacks:
            start, end, thickness = attack
            direction = (end[0] - start[0], end[1] - start[1])
            length = math.hypot(direction[0], direction[1])
            if length == 0:
                continue
            direction = (direction[0] / length * attack_speed, direction[1] / length * attack_speed)
            new_end = (start[0] + direction[0], start[1] + direction[1])
            if 0 <= new_end[0] <= 1200 and 0 <= new_end[1] <= 700:
                new_attacks.append((new_end, (new_end[0] + direction[0], new_end[1] + direction[1]), thickness))
        attacks = new_attacks

        # 공격이 적에게 충돌하는지 확인
        new_enemies = []
        for enemy in enemies:
            enemy_pos, enemy_size, _, _, _, _, _ = enemy
            hit = False
            for attack in attacks:
                attack_start, attack_end, thickness = attack
                if check_attack_collision(attack_start, attack_end, enemy_pos, enemy_size):
                    hit = True
                    enemies_defeated += 1  # 제거된 적의 수 증가
                    # 스피드 아이템 생성
                    if enemy_size == 20 and random.random() < speed_item_chance and not speed_item_active:
                        speed_item_pos = (enemy_pos[0], enemy_pos[1])
                    # 공격력 증가 아이템 생성
                    if enemy_size == 40 and random.random() < power_item_chance and power_item_active < 3:
                        power_item_pos = (enemy_pos[0], enemy_pos[1])
                    # 체력 회복 아이템 생성
                    if enemy_size == 20 and random.random() < heal_item_chance and current_health < max_health:
                        heal_item_pos = (enemy_pos[0], enemy_pos[1])
                        current_heal_item_image = random.choice(heal_item_images)
                    break
            if not hit:
                new_enemies.append(enemy)
        enemies = new_enemies

        # 스피드 아이템 획득 체크
        if speed_item_pos and player_pos[0] < speed_item_pos[0] < player_pos[0] + player_width and player_pos[1] < speed_item_pos[1] < player_pos[1] + player_height:
            speed_item_active = True
            speed_item_start_time = pygame.time.get_ticks()
            player_speed = original_player_speed + speed_increase_amount
            speed_item_pos = None

        # 스피드 아이템 지속시간 체크
        if speed_item_active and pygame.time.get_ticks() - speed_item_start_time > speed_item_duration:
            speed_item_active = False
            player_speed = original_player_speed

        # 공격력 증가 아이템 획득 체크
        if power_item_pos and player_pos[0] < power_item_pos[0] < player_pos[0] + player_width and player_pos[1] < power_item_pos[1] < player_pos[1] + player_height:
            power_item_active += 1
            power_item_pos = None

        # 체력 회복 아이템 획득 체크
        if heal_item_pos and player_pos[0] < heal_item_pos[0] < player_pos[0] + player_width and player_pos[1] < heal_item_pos[1] < player_pos[1] + player_height:
            if current_health < max_health:
                current_health += 1
            heal_item_pos = None

        # 에너지 볼 이동 및 충돌 체크
        new_energy_balls = []
        for ball in energy_balls:
            if ball[2] == "yellow":
                ball[0] += ball[3][0] * 5
                ball[1] += ball[3][1] * 5
            elif ball[2] == "green":
                ball[0] += ball[3][0] * 5
                ball[1] += ball[3][1] * 5
            if 0 <= ball[0] <= 1200 and 0 <= ball[1] <= 700:
                if check_energy_ball_collision((ball[0], ball[1]), player_pos):
                    current_health -= 1
                    if current_health <= 0:
                        win.fill((0, 0, 0))
                        text = font.render("Game Over", True, WHITE)
                        win.blit(text, (450, 350))
                        pygame.display.update()
                        pygame.time.delay(3000)
                        run = False
                else:
                    new_energy_balls.append(ball)
        energy_balls = new_energy_balls

        draw_objects(player_pos, enemies, star_pos, show_star, stage_background_images[level - 1], mouse_pos, star_image, collision_image, speed_item_pos, power_item_pos, heal_item_pos, current_heal_item_image)
        clock.tick(30)

pygame.quit()
