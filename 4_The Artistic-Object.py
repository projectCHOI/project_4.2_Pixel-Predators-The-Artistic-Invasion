import pygame
import random
import math

# Pygame 초기화
pygame.init()

# 윈도우 설정
win = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("The Artistic Invasion")

# 이미지 로드
title_image = pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_cover/Cover_The_Artistic_Invasion_Bright_1210x718.JPG")
title_image = pygame.transform.scale(title_image, (1280, 720))

stage_images = [
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage1_World_A.JPG",
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage1_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage2_World_A.JPG",
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage2_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage3_World_A.JPG",
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage3_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage4_World_A.JPG",
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage4_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage5_World_A.JPG",
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage5_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage6_World_A.JPG",
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage6_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage7_World_A.JPG",
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage7_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage8_World_A.JPG",
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage8_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage9_World_A.JPG",
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage9_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage10_World_A.JPG",
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage10_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage11_World_A.JPG",
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage11_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage12_World_A.JPG",
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage12_World_B.JPG")
]

# 화면 크기에 맞게 이미지 스케일 조정
stage_intro_images = [pygame.transform.scale(pygame.image.load(img[0]), (1280, 720)) for img in stage_images]
stage_background_images = [pygame.transform.scale(pygame.image.load(img[1]), (1280, 720)) for img in stage_images]

# 이미지 크기 설정
image_size = (40, 40)
player_width, player_height = image_size

# 플레이어 이미지 로드
player_image1 = pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_me1_png.png")
player_image2 = pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_me2_png.png")
player_image1 = pygame.transform.scale(player_image1, image_size)
player_image2 = pygame.transform.scale(player_image2, image_size)

# 충돌 시 이미지 로드(duration=시간)
collision_images = {
    3: {"image": pygame.transform.scale(pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_death_1.png"), image_size), "duration": 5000},
    2: {"image": pygame.transform.scale(pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_death_2.png"), image_size), "duration": 5000},
    1: {"image": pygame.transform.scale(pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_death_3.png"), image_size), "duration": 5000}
}

# Health 설정
health_image = pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_Life.png")
health_image = pygame.transform.scale(health_image, image_size)
max_health = 7
current_health = 4

# 스피드 아이템 설정
speed_item_image = pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_item_Quickly.png")
speed_item_image = pygame.transform.scale(speed_item_image, image_size)
speed_item_pos = None
speed_item_active = False
speed_item_start_time = 0
speed_item_duration = 20000  # 20초
speed_item_chance = 0.1  # 10% 확률

# 공격력 증가 아이템 설정
power_item_image = pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_item_Defense_2.PNG")
power_item_image = pygame.transform.scale(power_item_image, image_size)
power_item_pos = None
power_item_active = 0  # 공격력 증가 아이템 획득 수
power_item_chance = 0.1  # 10% 확률

# 체력 회복 아이템 설정
heal_item_images = [
    pygame.transform.scale(pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_Fruit_a.png"), image_size),
    # 추가 이미지...
]
heal_item_pos = None
current_heal_item_image = None
heal_item_chance = 0.1  # 10% 확률

# 초기 플레이어 이미지
player_image = player_image1

# 적 이미지 로드 및 크기 조정
enemy_images = {
    "up": pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_enemy_Relentless Charger_1.png"),
    # 추가 이미지...
}

# 크기 조정
enemy_images = {key: pygame.transform.scale(image, image_size) for key, image in enemy_images.items()}

# 보석 이미지
gem_image = pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_Jewelry_1.png")
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
font_path = r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_cover/서평원 꺾깎체/OTF/SLEIGothicOTF.otf"
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
victory_image = pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage14_Victory.JPG")
victory_image = pygame.transform.scale(victory_image, (1280, 720))

game_over_image = pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage15_GameOver.JPG")
game_over_image = pygame.transform.scale(game_over_image, (1280, 720))

time_over_image = pygame.image.load(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage16_TimeOver.JPG")
time_over_image = pygame.transform.scale(time_over_image, (1280, 720))

# 획득한 보석들을 저장할 리스트
collected_gems = []

# 보스 클래스 정의
class Boss:
    def __init__(self, stage, image_paths, attack_image_paths, appear_time, max_hp, speed):
        self.stage = stage
        self.images = {key: pygame.transform.scale(pygame.image.load(path), (120, 120)) for key, path in image_paths.items()}
        self.attack_images = {key: pygame.transform.scale(pygame.image.load(path), (40, 40)) for key, path in attack_image_paths.items()}
        self.appear_time = appear_time
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.speed = speed
        self.position = [640 - 60, 0]  # 초기 위치
        self.direction_x = 1
        self.direction_y = 1
        self.active = False
        self.defeated = False
        self.move_phase = 1
        self.hit = False
        self.hit_start_time = 0
        self.hit_duration = 500  # 밀리초
        self.attack_cooldown = 1000  # 밀리초
        self.last_attack_time = 0
        self.attacks = []

# 보스 관리
## 스테이지 1 보스
stage_1_boss = Boss(
    stage=1,
    image_paths={
        "default": r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/Mob_Boss_A.png"
    },
    attack_image_paths={
        "down": r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/Mob_Boss_A_a.png",
        "up": r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/Mob_Boss_A_b.png",
        "right": r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/Mob_Boss_A_c.png",
        "left": r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/Mob_Boss_A_d.png"
    },
    appear_time=30,  # 초
    max_hp=100,
    speed=5
)

# 모든 보스를 관리하는 딕셔너리
bosses = {
    1: stage_1_boss,
}

# 함수 정의
def check_boss_appearance(current_stage, elapsed_time):
    boss = bosses.get(current_stage)
    if boss and not boss.active and not boss.defeated and elapsed_time >= boss.appear_time:
        boss.active = True
        boss.position = [640 - 60, 0]  # 보스 초기 위치 재설정
        boss.current_hp = boss.max_hp  # 보스 체력 초기화

def move_boss(boss):
    if boss.move_phase == 1:  # 중앙으로 이동
        target_pos = [640 - 60, 360 - 60]
        direction = [target_pos[0] - boss.position[0], target_pos[1] - boss.position[1]]
        length = math.hypot(direction[0], direction[1])
        if length > boss.speed:
            direction = [direction[0] / length, direction[1] / length]
            boss.position[0] += direction[0] * boss.speed
            boss.position[1] += direction[1] * boss.speed
        else:
            boss.position = target_pos
            boss.move_phase = 2

    elif boss.move_phase == 2:  # 좌우 이동
        if boss.current_hp > boss.max_hp * 0.5:
            boss.position[0] += boss.speed * boss.direction_x
            if boss.position[0] <= 60 or boss.position[0] >= 1280 - 180:
                boss.direction_x *= -1  # 방향 전환
        else:
            boss.move_phase = 3

    elif boss.move_phase == 3:  # 좌우 + 위아래 이동
        boss.position[0] += boss.speed * boss.direction_x
        boss.position[1] += boss.speed * boss.direction_y
        if boss.position[0] <= 60 or boss.position[0] >= 1280 - 180:
            boss.direction_x *= -1  # 좌우 방향 전환
        if boss.position[1] <= 60 or boss.position[1] >= 720 - 180:
            boss.direction_y *= -1  # 위아래 방향 전환

def boss_attack(boss, current_time):
    if current_time - boss.last_attack_time > boss.attack_cooldown:
        boss.last_attack_time = current_time

        possible_directions = []

        # 보스의 체력에 따른 공격 방향 설정
        hp_ratio = boss.current_hp / boss.max_hp
        if hp_ratio > 0.8:
            possible_directions = ["down"]
        elif 0.6 < hp_ratio <= 0.8:
            possible_directions = ["down", "up"]
        elif 0.4 < hp_ratio <= 0.6:
            possible_directions = ["down", "up", "right"]
        else:
            possible_directions = ["down", "up", "right", "left"]

        attack_direction = random.choice(possible_directions)
        if attack_direction == "down":
            attack_start_pos = [boss.position[0] + 60, boss.position[1] + 120]
        elif attack_direction == "up":
            attack_start_pos = [boss.position[0] + 60, boss.position[1]]
        elif attack_direction == "right":
            attack_start_pos = [boss.position[0] + 120, boss.position[1] + 60]
        elif attack_direction == "left":
            attack_start_pos = [boss.position[0], boss.position[1] + 60]

        boss.attacks.append({
            "position": attack_start_pos,
            "direction": attack_direction
        })

def update_boss_attacks(boss, player_pos):
    new_attacks = []
    for attack in boss.attacks:
        pos = attack["position"]
        direction = attack["direction"]

        if direction == "down":
            pos[1] += 10
        elif direction == "up":
            pos[1] -= 10
        elif direction == "right":
            pos[0] += 10
        elif direction == "left":
            pos[0] -= 10

        if 0 <= pos[0] <= 1280 and 0 <= pos[1] <= 720:
            if check_energy_ball_collision(pos, player_pos):
                global current_health
                current_health -= 2  # 보스 공격에 맞으면 2의 데미지를 입음
                if current_health <= 0:
                    global game_active, game_over, game_over_reason
                    game_active = False
                    game_over = True
                    game_over_reason = "game_over"
            else:
                new_attacks.append(attack)
    boss.attacks = new_attacks

def draw_boss_health_bar(boss):
    bar_x = 150
    bar_y = 680
    bar_width = 10
    bar_height = 10
    total_bars = boss.max_hp // 2
    current_bars = boss.current_hp // 2

    boss_life_text = font.render("BOSS LIFE:", True, WHITE)
    win.blit(boss_life_text, (10, 675))

    for i in range(current_bars):
        pygame.draw.rect(win, YELLOW, (bar_x + i * (bar_width + 2), bar_y, bar_width, bar_height))

def draw_boss(boss):
    if boss.hit:
        current_time = pygame.time.get_ticks()
        if (current_time - boss.hit_start_time) // 100 % 2 == 0:
            win.blit(boss.images["default"], boss.position)
    else:
        win.blit(boss.images["default"], boss.position)

    # 보스 공격 그리기
    for attack in boss.attacks:
        image = boss.attack_images[attack["direction"]]
        win.blit(image, attack["position"])

# 함수 정의: 에너지 볼과 플레이어 충돌 체크
def check_energy_ball_collision(ball_pos, player_pos):
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_width, player_height)
    return player_rect.collidepoint(ball_pos)

# 함수 정의: 적 생성
def generate_enemies(level):
    new_enemies = []
    for i in range(level):
        enemy_pos = [random.randint(0, 1280 - 40), random.randint(0, 720 - 40)]
        enemy_speed = random.randint(2, 5)
        enemy_direction = random.choice(["up", "down", "left", "right"])
        enemy_image = enemy_images[enemy_direction]
        new_enemies.append([enemy_pos, enemy_speed, enemy_direction, enemy_image])
    return new_enemies

# 함수 정의: 폭탄 적 생성
def add_bomb_enemy():
    enemy_pos = [random.randint(0, 1280 - 40), random.randint(0, 720 - 40)]
    enemy_speed = random.randint(2, 5)
    enemy_direction = random.choice(["up", "down", "left", "right"])
    enemy_image = pygame.transform.scale(pygame.image.load(r"C:/path/to/bomb_enemy_image.png"), (40, 40))  # 폭탄 적 이미지 설정
    enemies.append([enemy_pos, enemy_speed, enemy_direction, enemy_image])

# 함수 정의: 공격이 보스와 충돌하는지 확인
def check_attack_collision(attack_start, attack_end, boss_pos, boss_size):
    boss_rect = pygame.Rect(boss_pos[0], boss_pos[1], boss_size, boss_size)
    return boss_rect.clipline(attack_start, attack_end)

# 함수 정의: 대시보드 그리기 (생략된 경우)
def draw_dashboard():
    # 예시로 대시보드에 표시할 텍스트나 이미지 등을 추가
    health_text = font.render(f"Health: {current_health}", True, WHITE)
    win.blit(health_text, (10, 10))
    # 추가 정보들을 여기에 그릴 수 있습니다.

# draw_objects 함수 정의 (위에서 수정했으므로 생략)

# 게임 루프
while run:
    if not game_active:
        if not game_over:
            win.blit(title_image, (0, 0))
            pygame.display.update()
        else:
            if game_over_reason == "victory":
                win.blit(victory_image, (0, 0))
            elif game_over_reason == "game_over":
                win.blit(game_over_image, (0, 0))
            elif game_over_reason == "time_over":
                win.blit(time_over_image, (0, 0))

            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if game_over:
                        # 게임 초기화
                        level = 1
                        current_health = 4
                        enemies_defeated = 0
                        player_speed = original_player_speed
                        power_item_active = 0
                        game_over = False
                        game_over_reason = None
                        stage_clear_times = [None] * 12  # 클리어 시간 초기화
                        for boss in bosses.values():
                            boss.active = False
                            boss.defeated = False
                        collected_gems = []  # 보석 초기화
                    game_active = True
                    player_pos = [640 - player_width // 2, 360 - player_height // 2]  # 플레이어를 중앙에 위치
                    enemies = []
                    start_ticks = pygame.time.get_ticks()  # 시작 시간
                    win.blit(stage_intro_images[level - 1], (0, 0))
                    pygame.display.update()
                    pygame.time.delay(3000)

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

        # 보스 등장 체크
        current_boss = bosses.get(level)
        check_boss_appearance(level, seconds)

        if current_boss and current_boss.active:
            # 보스 이동
            move_boss(current_boss)

            # 보스 공격
            boss_attack(current_boss, pygame.time.get_ticks())

            # 보스 공격 업데이트 및 충돌 처리
            update_boss_attacks(current_boss, player_pos)

            # 플레이어 공격과 보스의 충돌 처리
            new_attacks = []
            for attack in attacks:
                attack_start, attack_end, thickness = attack
                if check_attack_collision(attack_start, attack_end, current_boss.position, 120):
                    current_boss.current_hp -= attack_power
                    current_boss.hit = True
                    current_boss.hit_start_time = pygame.time.get_ticks()
                    if current_boss.current_hp <= 0:
                        current_boss.active = False
                        current_boss.defeated = True
                        gem_pos = [current_boss.position[0] + 40, current_boss.position[1] + 40]
                        gem_active = True
                        break  # 보스가 사라지면 공격을 멈춤
                else:
                    new_attacks.append(attack)
            attacks = new_attacks

            # 보스 피격 효과 지속 시간 체크
            if current_boss.hit and pygame.time.get_ticks() - current_boss.hit_start_time > current_boss.hit_duration:
                current_boss.hit = False

            # 보스 체력바 그리기
            draw_boss_health_bar(current_boss)

            # 보스 그리기
            draw_boss(current_boss)

        draw_objects(player_pos, enemies, stage_background_images[level - 1], mouse_pos, collision_image, speed_item_pos, power_item_pos, heal_item_pos, current_heal_item_image, current_boss.position if current_boss and current_boss.active else None, current_boss.attacks if current_boss and current_boss.active else None, gem_pos)
        clock.tick(30)

pygame.quit()
