import pygame
import random
import math

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
    (r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage2_World_A.JPG",
     r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage2_World_B.JPG"),
    (r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage3_World_A.JPG",
     r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage3_World_B.JPG"),
    (r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage4_World_A.JPG",
     r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage4_World_B.JPG"),
    (r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage5_World_A.JPG",
     r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage5_World_B.JPG"),
    (r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage6_World_A.JPG",
     r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage6_World_B.JPG"),
    (r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage7_World_A.JPG",
     r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage7_World_B.JPG"),
    (r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage8_World_A.JPG",
     r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage8_World_B.JPG"),
    (r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage9_World_A.JPG",
     r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage9_World_B.JPG"),
    (r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage10_World_A.JPG",
     r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage10_World_B.JPG"),
    (r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage11_World_A.JPG",
     r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage11_World_B.JPG"),
    (r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage12_World_A.JPG",
     r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage12_World_B.JPG")
]

# 화면 크기에 맞게 이미지 스케일 조정
stage_intro_images = [pygame.transform.scale(pygame.image.load(img[0]), (1280, 720)) for img in stage_images]
stage_background_images = [pygame.transform.scale(pygame.image.load(img[1]), (1280, 720)) for img in stage_images]

# 이미지 크기 설정
image_size = (40, 40)
player_width, player_height = image_size

# 플레이어 이미지 로드
player_image1 = pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_me1_png.png")
player_image2 = pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_me2_png.png")
player_image1 = pygame.transform.scale(player_image1, image_size)
player_image2 = pygame.transform.scale(player_image2, image_size)

# 충돌 시 이미지 로드(duration=시간)
collision_images = {
    3: {"image": pygame.transform.scale(pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_death_1.png"), image_size), "duration": 5000},
    2: {"image": pygame.transform.scale(pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_death_2.png"), image_size), "duration": 5000},
    1: {"image": pygame.transform.scale(pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_death_3.png"), image_size), "duration": 5000}
}

# Health 설정
health_image = pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_Life.png")
health_image = pygame.transform.scale(health_image, image_size)
max_health = 7
current_health = 4

# 적들의 속도를 변경 아이템 설정
speed_item_image = pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_item_Slowly_2.PNG")
speed_item_image = pygame.transform.scale(speed_item_image, image_size)
speed_item_pos = None
speed_item_active = False
speed_item_start_time = 0
speed_item_duration = 20000  # 20초
speed_item_chance = 0.1  # 10% 확률

# 공격력 증가 아이템 설정
power_item_image = pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_item_Life_2.PNG")
power_item_image = pygame.transform.scale(power_item_image, image_size)
power_item_pos = None
power_item_active = 0  # 공격력 증가 아이템 획득 수
power_item_chance = 0.1  # 10% 확률

# 체력 회복 아이템 설정
heal_item_images = [
    pygame.transform.scale(pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_Fruit_a.png"), image_size),
    pygame.transform.scale(pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_Fruit_b.png"), image_size),
    pygame.transform.scale(pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_Fruit_c.png"), image_size),
    pygame.transform.scale(pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_Fruit_d.png"), image_size)
]
heal_item_pos = None
current_heal_item_image = None
heal_item_chance = 0.1  # 10% 확률

# 초기 플레이어 이미지
player_image = player_image1

# 적 이미지 로드 및 크기 조정
enemy_images = {
    "up": pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_enemy_Relentless Charger_1.png"),
    "down": pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_enemy_Relentless Charger_2.png"),
    "left": pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_enemy_Relentless Charger_3.png"),
    "right": pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_enemy_Relentless Charger_4.png")
}

# 크기 조정
enemy_images = {key: pygame.transform.scale(image, image_size) for key, image in enemy_images.items()}

# 새로운 적 이미지 로드 및 크기 조정
sentinel_shooter_right = pygame.image.load(r"C:/Users\boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_enemy_Sentinel Shooter_right.png")
sentinel_shooter_left = pygame.image.load(r"C:/Users\boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_enemy_Sentinel Shooter_left.png")
sentinel_shooter_right = pygame.transform.scale(sentinel_shooter_right, image_size)
sentinel_shooter_left = pygame.transform.scale(sentinel_shooter_left, image_size)

# 새로운 적 이미지 로드 및 크기 조정
ambush_striker_up = pygame.image.load(r"C:/Users\boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_enemy_Ambush Striker_1.png")
ambush_striker_down = pygame.image.load(r"C:/Users\boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_enemy_Ambush Striker_2.png")
ambush_striker_left = pygame.image.load(r"C:/Users\boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_enemy_Ambush Striker_3.png")
ambush_striker_right = pygame.image.load(r"C:/Users\boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_enemy_Ambush Striker_4.png")
ambush_striker_up = pygame.transform.scale(ambush_striker_up, image_size)
ambush_striker_down = pygame.transform.scale(ambush_striker_down, image_size)
ambush_striker_left = pygame.transform.scale(ambush_striker_left, image_size)
ambush_striker_right = pygame.transform.scale(ambush_striker_right, image_size)

# 자폭 적 이미지 로드 및 크기 조정
enemy_bomb_image = pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_item_bomb.png")
enemy_bomb_image = pygame.transform.scale(enemy_bomb_image, (40, 40))

# 보스 이미지 및 설정
boss_image = pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/Mob_Boss_A.png")
boss_image = pygame.transform.scale(boss_image, (120, 120))
boss_appear_time = 30  # 보스 등장 시간 (초)
boss_hp = 100
boss_speed = 5
boss_pos = [640 - 60, 0]  # 초기 보스 위치
boss_direction_x = 1  # 좌우 이동 방향 (1: 오른쪽, -1: 왼쪽)
boss_direction_y = 1  # 위아래 이동 방향 (1: 아래, -1: 위)
boss_active = False
boss_defeated = False  # 보스가 제거되었는지 여부를 추적
boss_move_phase = 1  # 1: 중앙 이동, 2: 좌우 이동, 3: 좌우+위아래 이동
boss_hit = False  # 보스가 타격을 받았는지 여부
boss_hit_start_time = 0  # 보스가 타격을 받은 시작 시간
boss_hit_duration = 500  # 보스가 점멸할 시간 (밀리초)

# 보스 공격 이미지 로드
boss_attack_images = {
    "down": pygame.transform.scale(pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/Mob_Boss_A_a.png"), (40, 40)),
    "up": pygame.transform.scale(pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/Mob_Boss_A_b.png"), (40, 40)),
    "right": pygame.transform.scale(pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/Mob_Boss_A_c.png"), (40, 40)),
    "left": pygame.transform.scale(pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/Mob_Boss_A_d.png"), (40, 40))
}
boss_attack_cooldown = 1000  # 보스 공격 간격 (밀리초)
boss_last_attack_time = 0
boss_attacks = []

# 보석 이미지
gem_image = pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_mob/mob_Jewelry_1.png")
gem_image = pygame.transform.scale(gem_image, (40, 40))
gem_pos = None  # 보석 위치
gem_active = False

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

# bomb 적 등장 설정
bomb_stages = [2, 3, 5, 7, 11]
bomb_appear_interval = 10000  # 10초 간격으로 등장
bomb_last_appear_time = 0
bomb_directions = ["left", "right", "up", "down"]

# 게임 설정
clock = pygame.time.Clock()
font_path = r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_cover/서평원 꺾깎체/OTF/SLEIGothicOTF.otf"
font_size = 30  # 폰트 크기
font = pygame.font.Font(font_path, font_size) #폰트 설정
level = 1
max_level = 12
run = True
game_active = False
stage_duration = 60  # 스테이지 진행 시간 (초)
invincible = False
invincible_start_time = 0
invincible_duration = 3000  # 무적 시간 (밀리초)
player_blinking = False  # 깜빡임 효과를 위한 변수 추가
player_blink_start_time = 0  # 깜빡임 효과 시작 시간
blink_duration = 1500  # 깜빡임 지속 시간
blink_interval = 100  # 깜빡임 간격

# 충돌 효과 설정
collision_effect_start_time = 0
collision_image = None
collision_effect_duration = 0

# 공격 설정
attacks = []
attack_speed = 20
attack_power = 1  # 플레이어의 공격력
enemies_defeated = 0  # 제거된 적의 수

# 마우스 클릭 추적
mouse_down_time = 0
mouse_held = False

# 게임 오버 상태 및 이유
game_over = False
game_over_reason = None  # "victory", "game_over", "time_over"

# 게임 종료 상태 이미지 로드
victory_image = pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage14_Victory.JPG")
victory_image = pygame.transform.scale(victory_image, (1280, 720))

game_over_image = pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage15_GameOver.JPG")
game_over_image = pygame.transform.scale(game_over_image, (1280, 720))

time_over_image = pygame.image.load(r"C:/Users/boss3/OneDrive/바탕 화면/GitHub/project_4.2_Pixel-Predators-The-Artistic-Invasion/project4.2_world/Stage16_TimeOver.JPG")
time_over_image = pygame.transform.scale(time_over_image, (1280, 720))

# 획득한 보석들을 저장할 리스트
collected_gems = []

def draw_objects(player_pos, enemies, background_image, mouse_pos, collision_image=None, speed_item_pos=None, power_item_pos=None, heal_item_pos=None, heal_item_image=None, boss_pos=None, boss_attacks=None, gem_pos=None):
    win.blit(background_image, (0, 0))  # 배경을 전체 화면에 그리기
    
    # 플레이어 깜빡임 처리
    if player_blinking:
        current_time = pygame.time.get_ticks()
        if (current_time - player_blink_start_time) // blink_interval % 2 == 0:
            win.blit(player_image, (player_pos[0], player_pos[1]))  # 플레이어 이미지를 화면에 그리기
    else:
        win.blit(player_image, (player_pos[0], player_pos[1]))  # 플레이어 이미지를 화면에 그리기
    
    if collision_image:
        win.blit(collision_image, (player_pos[0], player_pos[1]))
    for enemy in enemies:
        enemy_pos, enemy_size, enemy_type, direction, speed, target_pos, shots_fired, enemy_image, original_speed, enemy_hp = enemy
        win.blit(enemy_image, (enemy_pos[0], enemy_pos[1]))
    if boss_pos:
        if boss_hit:
            # 보스가 공격을 받았을 때 점멸 효과
            current_time = pygame.time.get_ticks()
            if (current_time - boss_hit_start_time) // 100 % 2 == 0:
                win.blit(boss_image, boss_pos)
        else:
            win.blit(boss_image, boss_pos)
    if boss_attacks:
        for attack in boss_attacks:
            win.blit(boss_attack_images[attack[2]], (attack[0], attack[1]))
    if speed_item_pos:
        win.blit(speed_item_image, speed_item_pos)
    if power_item_pos:
        win.blit(power_item_image, power_item_pos)
    if heal_item_pos and heal_item_image:
        win.blit(heal_item_image, heal_item_pos)
    if gem_pos:
        win.blit(gem_image, gem_pos)
    
    # 에너지 볼 그리기
    for ball in energy_balls:
        color = YELLOW if ball[2] == "yellow" else GREEN
        pygame.draw.circle(win, color, (ball[0], ball[1]), 5)
    
    # 공격 그리기
    for attack in attacks:
        pygame.draw.line(win, RED, attack[0], attack[1], attack[2])
    
    # 마우스 위치 그리기
    pygame.draw.circle(win, RED, mouse_pos, 5)
    
    # 대시보드 그리기 함수 호출
    draw_dashboard()  # 대시보드 그리기
    pygame.display.update()

# bomb 적 추가 함수
def add_bomb_enemy():
    direction = random.choice(bomb_directions)
    size = 40
    pos = None
    if direction == "left":
        pos = [0, random.randint(0, 680)]
    elif direction == "right":
        pos = [1240, random.randint(0, 680)]
    elif direction == "up":
        pos = [random.randint(0, 1240), 0]
    elif direction == "down":
        pos = [random.randint(0, 1240), 680]
    target_pos = [640, 360]  # 중심을 향하도록 설정
    direction = [target_pos[0] - pos[0], target_pos[1] - pos[1]]
    length = math.hypot(direction[0], direction[1])
    direction = [direction[0] / length, direction[1] / length]
    enemies.append([pos, size, "bomb", direction, 9, None, 0, enemy_bomb_image, 9, 1])  # enemy_bomb 체력 1 추가

# 적과 플레이어의 충돌 체크 함수
def check_collision(player_pos, enemies):
    for enemy in enemies:
        enemy_pos, enemy_size, enemy_type = enemy[:3]
        if (player_pos[0] < enemy_pos[0] < player_pos[0] + player_width or enemy_pos[0] < player_pos[0] < enemy_pos[0] + enemy_size) and \
           (player_pos[1] < enemy_pos[1] < player_pos[1] + player_height or player_pos[1] < enemy_pos[1] < player_pos[1] + enemy_size):
            if enemy_type == "bomb":
                return "bomb"  # bomb 충돌 시
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
    if px < bx < px + player_width and py < by < player_height:
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
            image = enemy_images["up"] if size == 40 else sentinel_shooter_left if size == 60 else ambush_striker_up
        elif direction == (0, -1):  # 하단에서
            pos = [random.randint(0, 1200-size), 700-size]
            image = enemy_images["down"] if size == 40 else sentinel_shooter_left if size == 60 else ambush_striker_down
        elif direction == (1, 0):  # 좌측에서
            pos = [0, random.randint(0, 700-size)]
            image = enemy_images["left"] if size == 40 else sentinel_shooter_right if size == 60 else ambush_striker_left
        elif direction == (-1, 0):  # 우측에서
            pos = [1200-size, random.randint(0, 700-size)]
            image = enemy_images["right"] if size == 40 else sentinel_shooter_right if size == 60 else ambush_striker_right
        
        if size == 40:
            enemy_type = "move_and_disappear"
            hp = 1  # 체력 1
        elif size == 60:
            target_pos = [random.randint(100, 1100), random.randint(100, 600)]  # 랜덤한 화면 내 특정 장소
            enemy_type = "move_and_shoot"
            direction = [target_pos[0] - pos[0], target_pos[1] - pos[1]]
            length = math.hypot(direction[0], direction[1])
            direction = [direction[0] / length, direction[1] / length]
            hp = 2  # 체력 2
        elif size == 20:
            enemy_type = "approach_and_shoot"
            hp = 1  # 체력 1
        enemies.append([pos, size, enemy_type, direction, speed, target_pos if size == 60 else None, 0, image, speed, hp])  # 이미지, 원래 속도 및 HP 추가

    return enemies

# 대시보드 그리기 함수
def draw_dashboard():
    # 플레이 시간 표시
    elapsed_time = seconds
    time_text = font.render(f"{elapsed_time}", True, WHITE)
    win.blit(time_text, (640 - time_text.get_width() // 2, 10))  # 화면 중앙에 맞춤
    
    # 체력 표시
    for i in range(current_health):
        win.blit(health_image, (10 + i * 50, 10))
    
    # 제거된 적의 수 표시
    enemies_defeated_text = font.render(f"제거: {enemies_defeated}", True, WHITE)
    win.blit(enemies_defeated_text, (1280 - enemies_defeated_text.get_width() - 10, 10))  # 오른쪽에 맞춤
    
    # 보스 체력바 표시
    if boss_active:
        draw_boss_health_bar(boss_hp, 100)  # 보스 체력바 그리기

def draw_boss_health_bar(boss_hp, max_boss_hp, bar_color=YELLOW):
    # 체력바의 위치와 크기 설정
    bar_x = 150
    bar_y = 680
    bar_width = 10
    bar_height = 10
    bars = boss_hp // 2

    # "BOSS LIFE" 텍스트 표시
    boss_life_text = font.render("BOSS LIFE:", True, WHITE)
    win.blit(boss_life_text, (10, 675))

    # 체력바 그리기
    for i in range(bars):
        pygame.draw.rect(win, bar_color, (bar_x + i * (bar_width + 2), bar_y, bar_width, bar_height))

# 각 스테이지 클리어 시간을 저장하는 리스트
stage_clear_times = [None] * 12  # 스테이지 1부터 12까지의 클리어 시간을 저장

# 스테이지를 클리어할 때마다 클리어 시간을 기록하는 함수
def record_stage_clear_time(stage, time_taken):
    stage_clear_times[stage - 1] = time_taken

# 총 플레이 시간을 계산하는 함수
def calculate_total_play_time():
    total_seconds = sum(time for time in stage_clear_times if time is not None)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return minutes, seconds

# 획득한 보석을 화면에 시각화하는 함수
def draw_collected_gems():
    x_offset = 640 - (len(collected_gems) * 25)
    y_offset = 420
    for i, gem in enumerate(collected_gems):
        win.blit(gem_image, (x_offset + i * 50, y_offset))

# 게임 종료 화면 그리기 함수 수정
def draw_end_screen():
    if game_over_reason == "victory":
        image = victory_image
    elif game_over_reason == "game_over":
        image = game_over_image
    elif game_over_reason == "time_over":
        image = time_over_image

    win.blit(image, (0, 0))
    text = font.render("continue : enter", True, WHITE)
    win.blit(text, (640 - text.get_width() // 2, 360 - text.get_height() // 2))  # 화면 중앙에 맞춤

    # 획득한 보석 시각화
    draw_collected_gems()

    # 총 플레이 시간 계산 및 표시
    minutes, seconds = calculate_total_play_time()
    total_time_text = font.render(f"Total play time : {minutes}m' {seconds}s", True, WHITE)
    win.blit(total_time_text, (640 - total_time_text.get_width() // 2, 680))  # 화면 하단 중앙에 맞춤
    
    pygame.display.update()

# Boss Logic for Stage 1
def stage1_boss(seconds, player_pos, attacks, energy_balls):
    global boss_active, boss_pos, boss_hp, boss_move_phase, boss_direction_x, boss_direction_y, boss_last_attack_time, boss_attacks, boss_hit, boss_hit_start_time, gem_pos, gem_active, boss_defeated, current_health, game_active, game_over, game_over_reason
    
    # 보스 등장 조건 체크
    if not boss_active and seconds >= boss_appear_time and not boss_defeated:
        boss_active = True
        boss_pos = [640 - 60, 0]
        boss_hp = 100  # 보스 체력 초기화

    if boss_active:
        # 보스 이동 패턴
        if boss_move_phase == 1:  # 중앙으로 이동
            target_pos = [640 - 60, 360 - 60]
            direction = [target_pos[0] - boss_pos[0], target_pos[1] - boss_pos[1]]
            length = math.hypot(direction[0], direction[1])
            if length > boss_speed:
                direction = [direction[0] / length, direction[1] / length]
                boss_pos[0] += direction[0] * boss_speed
                boss_pos[1] += direction[1] * boss_speed
            else:
                boss_pos = target_pos
                boss_move_phase = 2

        elif boss_move_phase == 2:  # 좌우 이동
            if boss_hp > 50:
                boss_pos[0] += boss_speed * boss_direction_x
                if boss_pos[0] <= 60 or boss_pos[0] >= 1280 - 180:
                    boss_direction_x *= -1  # 방향 전환
            else:
                boss_move_phase = 3

        elif boss_move_phase == 3:  # 좌우+위아래 이동
            boss_pos[0] += boss_speed * boss_direction_x
            boss_pos[1] += boss_speed * boss_direction_y
            if boss_pos[0] <= 60 or boss_pos[0] >= 1280 - 180:
                boss_direction_x *= -1  # 좌우 방향 전환
            if boss_pos[1] <= 60 or boss_pos[1] >= 720 - 180:
                boss_direction_y *= -1  # 위아래 방향 전환

        # 보스 공격
        if pygame.time.get_ticks() - boss_last_attack_time > boss_attack_cooldown:
            boss_last_attack_time = pygame.time.get_ticks()

            possible_directions = []

            # 보스의 체력에 따른 공격 방향 설정
            if boss_hp <= 100 and boss_hp > 80:
                possible_directions = ["down"]
            elif boss_hp <= 80 and boss_hp > 60:
                possible_directions = ["down", "up"]
            elif boss_hp <= 60 and boss_hp > 40:
                possible_directions = ["down", "up", "right"]
            elif boss_hp <= 40 and boss_hp > 0:
                possible_directions = ["down", "up", "right", "left"]

            # 가능한 방향 중에서 랜덤으로 선택
            if possible_directions:
                attack_direction = random.choice(possible_directions)

                if attack_direction == "down":
                    attack_start_pos = [boss_pos[0] + 60, boss_pos[1] + 120]
                elif attack_direction == "up":
                    attack_start_pos = [boss_pos[0] + 60, boss_pos[1]]
                elif attack_direction == "right":
                    attack_start_pos = [boss_pos[0] + 120, boss_pos[1] + 60]
                elif attack_direction == "left":
                    attack_start_pos = [boss_pos[0], boss_pos[1] + 60]

                boss_attacks.append([attack_start_pos[0], attack_start_pos[1], attack_direction])

    # 보스 공격 이동 및 충돌 처리
    new_boss_attacks = []
    for attack in boss_attacks:
        if attack[2] == "down":
            attack[1] += 10
        elif attack[2] == "up":
            attack[1] -= 10
        elif attack[2] == "right":
            attack[0] += 10
        elif attack[2] == "left":
            attack[0] -= 10

        if 0 <= attack[0] <= 1280 and 0 <= attack[1] <= 720:
            if check_energy_ball_collision((attack[0], attack[1]), player_pos):
                current_health -= 2  # 보스 공격에 맞으면 2의 데미지를 입음
                if current_health <= 0:
                    game_active = False
                    game_over = True
                    game_over_reason = "game_over"
            else:
                new_boss_attacks.append(attack)

    boss_attacks = new_boss_attacks

    # 플레이어의 공격이 보스에게 충돌하는지 확인
    for attack in attacks:
        attack_start, attack_end, thickness = attack
        if check_attack_collision(attack_start, attack_end, boss_pos, 120):
            boss_hp -= attack_power
            boss_hit = True  # 보스가 공격을 받았음을 표시
            boss_hit_start_time = pygame.time.get_ticks()  # 점멸 시작 시간 기록
            if boss_hp <= 0:
                boss_active = False
                boss_hp = 0  # 보스 체력을 0으로 유지
                gem_pos = [boss_pos[0] + 40, boss_pos[1] + 40]
                gem_active = True
                boss_defeated = True  # 보스가 제거된 것으로 표시
                break  # 보스가 사라지면 공격을 멈춥니다

    # 보스 점멸 지속 시간 체크
    if boss_hit and pygame.time.get_ticks() - boss_hit_start_time > boss_hit_duration:
        boss_hit = False  # 점멸 효과 해제

# Main game loop
while run:
    if not game_active:
        if not game_over:
            title_screen()
        else:
            draw_end_screen()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if game_over:
                        # 게임 초기화
                        level = 1
                        current_health = 3
                        enemies_defeated = 0
                        player_speed = original_player_speed
                        power_item_active = 0
                        game_over = False
                        game_over_reason = None
                        stage_clear_times = [None] * 12  # 클리어 시간 초기화
                        boss_active = False
                        boss_hp = 100
                        boss_attacks = []
                        gem_active = False
                        boss_defeated = False  # 보스 초기화
                        collected_gems = []  # 보석 초기화
                    game_active = True
                    player_pos = [640 - player_width // 2, 360 - player_height // 2]  # 플레이어를 중앙에 위치
                    enemies = []
                    start_ticks = pygame.time.get_ticks()  # 시작 시간
                    intro_screen(level)

                    # 새로운 스테이지 시작 시 공격 및 에너지 볼 리스트 초기화
                    attacks = []
                    energy_balls = []

    else:
        mouse_pos = pygame.mouse.get_pos()
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000  # 초 계산
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                attack_start = (player_pos[0] + player_width // 2, player_pos[1] + player_height // 2)
                attack_end = mouse_pos
                attack_thickness = 3
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
        if player_pos[0] > 1240:
            player_pos[0] = 1240
        if player_pos[1] < 0:
            player_pos[1] = 0
        if player_pos[1] > 680:
            player_pos[1] = 680

        if seconds >= 300:
            game_active = False
            game_over = True
            game_over_reason = "time_over"

        if random.random() < 0.02:  # 2% 확률로 적 생성
            new_enemies = generate_enemies(level)
            enemies.extend(new_enemies)

        # bomb 적 생성
        if level in bomb_stages and pygame.time.get_ticks() - bomb_last_appear_time > bomb_appear_interval:
            add_bomb_enemy()
            bomb_last_appear_time = pygame.time.get_ticks()

        # Handle Stage 1 boss
        if level == 1:
            stage1_boss(seconds, player_pos, attacks, energy_balls)

        # 적 이동 및 충돌 처리
        for enemy in enemies:
            enemy_pos, enemy_size, enemy_type, direction, speed, target_pos, shots_fired, enemy_image, original_speed, enemy_hp = enemy
            if enemy_type == "move_and_disappear":
                enemy_pos[0] += direction[0] * speed
                enemy_pos[1] += direction[1] * speed
            elif enemy_type == "move_and_shoot":
                if target_pos:
                    distance_to_target = math.hypot(target_pos[0] - enemy_pos[0], target_pos[1] - enemy_pos[1])
                    if distance_to_target > speed:
                        enemy_pos[0] += direction[0] * speed
                        enemy_pos[1] += direction[1] * speed
                    else:
                        enemy_pos[0], enemy_pos[1] = target_pos
                        enemy[5] = None  # target_pos를 None으로 설정하여 적이 멈추게 함
                        direction = [0, 0]  # 위치를 고정
                else:
                    if shots_fired < 5:
                        if pygame.time.get_ticks() % 1000 < 50:  # 1초마다 공격
                            attack_dir = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
                            energy_balls.append([enemy_pos[0] + enemy_size // 2, enemy_pos[1] + enemy_size // 2, "yellow", attack_dir])
                            enemy[6] += 1  # 공격 횟수 증가
            elif enemy_type == "approach_and_shoot":
                if pygame.time.get_ticks() % 5000 < 2500:
                    target_pos = [player_pos[0], player_pos[1]]
                    direction = [target_pos[0] - enemy_pos[0], target_pos[1] - enemy_pos[1]]
                    length = math.hypot(direction[0], direction[1])
                    direction = [direction[0] / length, direction[1] / length]
                    enemy_pos[0] += direction[0] * speed
                    enemy_pos[1] += direction[1] * speed
                    if length < 100: # 플레이어에게 접근
                        energy_balls.append([enemy_pos[0], enemy_pos[1], "green", direction])
                else:
                    direction = [random.choice([-1, 1]), random.choice([-1, 1])]
                    enemy_pos[0] += direction[0] * speed
                    enemy_pos[1] += direction[1] * speed
            elif enemy_type == "bomb":
                target_pos = [player_pos[0], player_pos[1]]
                direction = [target_pos[0] - enemy_pos[0], target_pos[1] - enemy_pos[1]]
                length = math.hypot(direction[0], direction[1])
                direction = [direction[0] / length, direction[1] / length]
                enemy_pos[0] += direction[0] * speed
                enemy_pos[1] += direction[1] * speed

        if not invincible:
            collision = check_collision(player_pos, [(enemy[0], enemy[1], enemy[2]) for enemy in enemies])
            if collision:
                if collision == "bomb":  # bomb 충돌 시 즉시 사망
                    current_health = 0
                    collision_image = collision_images[1]["image"]
                    collision_effect_duration = collision_images[1]["duration"]
                    game_active = False
                    game_over = True
                    game_over_reason = "game_over"
                else:
                    current_health -= 1
                    invincible = True
                    invincible_start_time = pygame.time.get_ticks()
                    collision_effect_start_time = pygame.time.get_ticks()
                    if current_health <= 0:
                        collision_image = collision_images[1]["image"]
                        collision_effect_duration = collision_images[1]["duration"]
                        game_active = False
                        game_over = True
                        game_over_reason = "game_over"
                    elif current_health == 2:
                        collision_image = collision_images[3]["image"]
                        collision_effect_duration = collision_images[3]["duration"]
                    elif current_health == 1:
                        collision_image = collision_images[2]["image"]
                        collision_effect_duration = collision_images[2]["duration"]

                    # 체력이 4 이상일 때 깜빡임 효과 추가
                    if current_health >= 4:
                        player_blinking = True
                        player_blink_start_time = pygame.time.get_ticks()

        if invincible and pygame.time.get_ticks() - invincible_start_time > invincible_duration:
            invincible = False

        # 플레이어 깜빡임 지속 시간 체크
        if player_blinking and pygame.time.get_ticks() - player_blink_start_time > blink_duration:
            player_blinking = False

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
            if 0 <= new_end[0] <= win_width and 0 <= new_end[1] <= win_height:
                new_attacks.append((new_end, (new_end[0] + direction[0], new_end[1] + direction[1]), thickness))
        attacks = new_attacks

        # 공격이 적이나 보스에게 충돌하는지 확인
        new_enemies = []
        for enemy in enemies:
            enemy_pos, enemy_size, enemy_type, direction, speed, target_pos, shots_fired, enemy_image, original_speed, enemy_hp = enemy
            hit = False
            for attack in attacks:
                attack_start, attack_end, thickness = attack
                if check_attack_collision(attack_start, attack_end, enemy_pos, enemy_size):
                    enemy_hp -= attack_power  # 공격력 적용
                    if enemy_hp <= 0:
                        hit = True
                        enemies_defeated += 1  # 제거된 적의 수 증가
                        # 적들의 속도를 변경 아이템 생성
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

        if boss_active:
            draw_boss_health_bar(boss_hp, 100)  # 보스 체력바 그리기
            for attack in attacks:
                attack_start, attack_end, thickness = attack
                if check_attack_collision(attack_start, attack_end, boss_pos, 120):
                    boss_hp -= attack_power
                    boss_hit = True  # 보스가 공격을 받았음을 표시
                    boss_hit_start_time = pygame.time.get_ticks()  # 점멸 시작 시간 기록
                    if boss_hp <= 0:
                        boss_active = False
                        boss_hp = 0  # 보스 체력을 0으로 유지
                        gem_pos = [boss_pos[0] + 40, boss_pos[1] + 40]
                        gem_active = True
                        boss_defeated = True  # 보스가 제거된 것으로 표시
                        break  # 보스가 사라지면 공격을 멈춥니다

            # 보스 점멸 지속 시간 체크
            if boss_hit and pygame.time.get_ticks() - boss_hit_start_time > boss_hit_duration:
                boss_hit = False  # 점멸 효과 해제

        if gem_active and gem_pos:
            if player_pos[0] < gem_pos[0] < player_pos[0] + player_width and player_pos[1] < gem_pos[1] < player_pos[1] + player_height:
                gem_active = False
                collected_gems.append(gem_pos)  # 획득한 보석을 리스트에 추가
                # 스테이지 클리어
                record_stage_clear_time(level, seconds)
                level += 1
                if level > max_level:
                    game_active = False
                    game_over = True
                    game_over_reason = "victory"
                else:
                    player_pos = [640 - player_width // 2, 360 - player_height // 2]  # 레벨 시작 시 플레이어를 중앙에 위치
                    intro_screen(level)
                    start_ticks = pygame.time.get_ticks()  # 새로운 레벨 시작 시간 초기화
                    enemies = []
                    attacks = []
                    energy_balls = []
                    boss_active = False
                    boss_hp = 100
                    boss_attacks = []
                    gem_active = False
                    gem_pos = None  # 보석 위치 초기화

        # 적들의 속도를 변경 아이템 획득 체크
        if speed_item_pos and player_pos[0] < speed_item_pos[0] < player_pos[0] + player_width and player_pos[1] < speed_item_pos[1] < player_pos[1] + player_height:
            speed_item_active = True
            speed_item_start_time = pygame.time.get_ticks()
            # 적들의 속도를 7로 변경
            for enemy in enemies:
                enemy[4] = 7
            speed_item_pos = None

        # 적들의 속도를 변경 아이템 지속시간 체크
        if speed_item_active and pygame.time.get_ticks() - speed_item_start_time > speed_item_duration:
            speed_item_active = False
            # 적들의 속도를 원래 속도로 복원
            for enemy in enemies:
                enemy[4] = enemy[8]  # original_speed로 복원

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
            if 0 <= ball[0] <= 1280 and 0 <= ball[1] <= 720:
                if check_energy_ball_collision((ball[0], ball[1]), player_pos):
                    current_health -= 1
                    if current_health <= 0:
                        game_active = False
                        game_over = True
                        game_over_reason = "game_over"
                else:
                    new_energy_balls.append(ball)
        energy_balls = new_energy_balls

        draw_objects(player_pos, enemies, stage_background_images[level - 1], mouse_pos, collision_image, speed_item_pos, power_item_pos, heal_item_pos, current_heal_item_image, boss_pos if boss_active else None, boss_attacks, gem_pos)
        clock.tick(30)

pygame.quit()
