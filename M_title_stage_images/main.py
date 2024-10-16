import pygame
import random
import math
import os

from bosses.Stage_1_Boss import Stage1Boss
from bosses.Stage_2_Boss import Stage2Boss

pygame.init()

# 윈도우 설정
win_width, win_height = 1280, 720
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("The Artistic Invasion")

# BASE_DIR은 프로젝트의 루트 디렉토리
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 이미지의 기본 경로를 정의합니다.
BASE_IMAGE_PATH = os.path.join(BASE_DIR, "assets", "images")

# 이미지 로딩 함수
def load_image(*path_parts, size=None):
    path = os.path.join(BASE_IMAGE_PATH, *path_parts)
    try:
        image = pygame.image.load(path).convert_alpha()
    except pygame.error as e:
        raise SystemExit(e)
    if size:
        image = pygame.transform.scale(image, size)
    return image

# 모듈에서 타이틀 및 스테이지 이미지 임포트
try:
    from title_stage_images import title_image, stage_intro_images, stage_background_images
except ImportError:
    pygame.quit()
    exit()

# 이미지 크기 설정
image_size = (40, 40)
player_width, player_height = image_size

# 플레이어 이미지 로드
player_image1 = load_image("player", "mob_me1_png.png", size=image_size)
player_image2 = load_image("player", "mob_me2_png.png", size=image_size)

# 충돌 시 이미지 로드(duration=시간)
collision_images = {
    3: {"image": load_image("player", "mob_death_1.png", size=image_size), "duration": 5000},
    2: {"image": load_image("player", "mob_death_2.png", size=image_size), "duration": 5000},
    1: {"image": load_image("player", "mob_death_3.png", size=image_size), "duration": 5000}
}

# Health 설정
health_image = load_image("player", "mob_Life.png", size=image_size)
max_health = 5
current_health = 3

# 스피드 아이템 설정
speed_item_image = load_image("items", "mob_item_Slowly_2.PNG", size=image_size)
speed_item_pos = None
speed_item_active = False
speed_item_start_time = 0
speed_item_duration = 20000  # 20초
speed_item_chance = 0.1  # 10% 확률

# 공격력 증가 아이템 설정
power_item_image = load_image("items", "mob_item_Life_2.PNG", size=image_size)
power_item_pos = None
power_item_active = 0  # 공격력 증가 아이템 획득 수
power_item_chance = 0.1  # 10% 확률

# 체력 회복 아이템 설정
heal_item_images = [
    load_image("items", "mob_Fruit_a.png", size=image_size),
    load_image("items", "mob_Fruit_b.png", size=image_size),
    load_image("items", "mob_Fruit_c.png", size=image_size),
    load_image("items", "mob_Fruit_d.png", size=image_size)
]
heal_item_pos = None
current_heal_item_image = None
heal_item_chance = 0.2  # 20% 확률

# 초기 플레이어 이미지
player_image = player_image1

# 적 이미지 로드 및 크기 조정
enemy_images = {
    "up": load_image("enemies", "mob_enemy_Relentless Charger_1.png", size=image_size),
    "down": load_image("enemies", "mob_enemy_Relentless Charger_2.png", size=image_size),
    "left": load_image("enemies", "mob_enemy_Relentless Charger_3.png", size=image_size),
    "right": load_image("enemies", "mob_enemy_Relentless Charger_4.png", size=image_size)
}

# 새로운 적 이미지 로드 및 크기 조정
sentinel_shooter_right = load_image("enemies", "mob_enemy_Sentinel Shooter_right.png", size=image_size)
sentinel_shooter_left = load_image("enemies", "mob_enemy_Sentinel Shooter_left.png", size=image_size)

ambush_striker_up = load_image("enemies", "mob_enemy_Ambush Striker_1.png", size=image_size)
ambush_striker_down = load_image("enemies", "mob_enemy_Ambush Striker_2.png", size=image_size)
ambush_striker_left = load_image("enemies", "mob_enemy_Ambush Striker_3.png", size=image_size)
ambush_striker_right = load_image("enemies", "mob_enemy_Ambush Striker_4.png", size=image_size)

# 자폭 적 이미지 로드 및 크기 조정
enemy_bomb_image = load_image("enemies", "mob_item_bomb.png", size=image_size)

# 색상 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# 플레이어 설정
player_speed = 10  # 속도 조정
original_player_speed = player_speed

# 보스 초기화
boss = Stage1Boss()

# 에너지 볼 설정
energy_balls = []

# 게임 설정
clock = pygame.time.Clock()
font_path = os.path.join(BASE_DIR, "assets", "fonts", "SLEIGothicOTF.otf")
font_size = 30  # 폰트 크기
try:
    font = pygame.font.Font(font_path, font_size)  # 폰트 설정
except FileNotFoundError:
    pygame.quit()
    exit()

level = 1
max_level = 12
run = True
game_active = False
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
attack_power = 1  # 플레이어의 공격력 추가
enemies_defeated = 0  # 제거된 적의 수

# 마우스 클릭 추적
mouse_down_time = 0
mouse_held = False

# 게임 오버 상태 및 이유
game_over = False
game_over_reason = None  # "victory", "game_over", "time_over"

# 게임 종료 상태 이미지 로드
victory_image = load_image("stages", "Stage14_Victory.JPG", size=(1280, 720))
game_over_image = load_image("stages", "Stage15_GameOver.JPG", size=(1280, 720))
time_over_image = load_image("stages", "Stage16_TimeOver.JPG", size=(1280, 720))

# 게임 종료 화면 그리기 함수
def draw_end_screen():
    if game_over_reason == "victory":
        image = victory_image
    elif game_over_reason == "game_over":
        image = game_over_image
    elif game_over_reason == "time_over":
        image = time_over_image
    else:
        image = game_over_image  # 기본값 설정

    win.blit(image, (0, 0))
    text = font.render("Press Enter to Continue", True, WHITE)
    win.blit(text, (win_width // 2 - text.get_width() // 2, win_height // 2 - text.get_height() // 2))
    pygame.display.update()

# 스테이지 시작 시 시간 제한 함수
def get_stage_duration(level):
    base_duration = 600  # 기본 스테이지 시간 (초)
    reduction = (level - 1) * 5  # 레벨당 5초 감소
    return max(300, base_duration - reduction)  # 최소 30초

# 적과 플레이어의 충돌 체크 함수
def check_collision(player_pos, enemies):
    for enemy in enemies:
        enemy_pos, enemy_size, enemy_type = enemy[:3]
        if (player_pos[0] < enemy_pos[0] + enemy_size and player_pos[0] + player_width > enemy_pos[0] and
            player_pos[1] < enemy_pos[1] + enemy_size and player_pos[1] + player_height > enemy_pos[1]):
            if enemy_type == "bomb":
                return "bomb"  # bomb 충돌 시
            return True
    return False

# 공격이 적에게 충돌하는지 확인하는 함수
def check_attack_collision(attack_start, attack_end, enemy_pos, enemy_size):
    ex, ey = enemy_pos
    sx, sy = attack_start
    ex2, ey2 = ex + enemy_size, ey + enemy_size

    # 공격 선분의 직사각형 영역 계산
    line_rect = pygame.Rect(min(sx, attack_end[0]), min(sy, attack_end[1]),
                            abs(attack_end[0] - sx), abs(attack_end[1] - sy))
    enemy_rect = pygame.Rect(ex, ey, enemy_size, enemy_size)

    return line_rect.colliderect(enemy_rect)

# 에너지 볼과 플레이어의 충돌 체크 함수
def check_energy_ball_collision(ball_pos, player_pos):
    bx, by = ball_pos
    px, py = player_pos
    if px < bx < px + player_width and py < by < py + player_height:
        return True
    return False

# 타이틀 화면 그리기 함수
def title_screen():
    win.blit(title_image, (0, 0))
    pygame.display.update()

# 인트로 화면 그리기 함수
def intro_screen(stage):
    if stage - 1 < len(stage_intro_images):
        win.blit(stage_intro_images[stage - 1], (0, 0))
    else:
        win.fill(BLACK)  # 기본 배경 설정
    pygame.display.update()
    pygame.time.delay(3000)  # 3초 대기

# 스테이지 설정에 따라 적을 생성하는 함수
def generate_enemies(level):
    enemies = []
    num_enemies = 0
    speed = 10
    directions = [(0, 1)]  # 초기 방향: 아래쪽
    sizes = [40]

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
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                     (1, 1), (1, -1), (-1, 1), (-1, -1)]
        sizes = [20, 40, 60]
        num_enemies = random.randint(6, 26)
    elif level == 9:
        speed = random.randint(10, 18)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                     (1, 1), (1, -1), (-1, 1), (-1, -1)]
        sizes = [20, 40, 60]
        num_enemies = random.randint(8, 30)
    elif level == 10:
        speed = random.randint(10, 20)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                     (1, 1), (1, -1), (-1, 1), (-1, -1)]
        sizes = [20, 40, 60]
        num_enemies = random.randint(8, 30)
    elif level == 11:
        speed = random.randint(10, 20)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                     (1, 1), (1, -1), (-1, 1), (-1, -1)]
        sizes = [20, 40, 60]
        num_enemies = random.randint(10, 32)
    elif level == 12:
        speed = random.randint(10, 20)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                     (1, 1), (1, -1), (-1, 1), (-1, -1)]
        sizes = [20, 40, 60]
        num_enemies = random.randint(15, 32)

    for _ in range(num_enemies):
        direction = random.choice(directions)
        size = random.choice(sizes)
        pos = [0, 0]
        image = enemy_images["up"]

        if direction == (0, 1):  # 상단에서
            pos = [random.randint(0, win_width - size), 0]
            if size == 40:
                image = enemy_images["up"]
            elif size == 60:
                image = ambush_striker_up
            else:
                image = sentinel_shooter_left
        elif direction == (0, -1):  # 하단에서
            pos = [random.randint(0, win_width - size), win_height - size]
            if size == 40:
                image = enemy_images["down"]
            elif size == 60:
                image = ambush_striker_down
            else:
                image = sentinel_shooter_left
        elif direction == (1, 0):  # 좌측에서
            pos = [0, random.randint(0, win_height - size)]
            if size == 40:
                image = enemy_images["left"]
            elif size == 60:
                image = ambush_striker_left
            else:
                image = sentinel_shooter_right
        elif direction == (-1, 0):  # 우측에서
            pos = [win_width - size, random.randint(0, win_height - size)]
            if size == 40:
                image = enemy_images["right"]
            elif size == 60:
                image = ambush_striker_right
            else:
                image = sentinel_shooter_right

        if size == 40:
            enemy_type = "move_and_disappear"
        elif size == 60:
            target_pos = [random.randint(100, win_width - 100), random.randint(100, win_height - 100)]  # 랜덤한 화면 내 특정 장소
            direction_vector = [target_pos[0] - pos[0], target_pos[1] - pos[1]]
            length = math.hypot(direction_vector[0], direction_vector[1])
            direction_normalized = [direction_vector[0] / length, direction_vector[1] / length]
            enemy_type = "move_and_shoot"
            enemies.append([pos, size, enemy_type, direction_normalized, speed, target_pos, 0, image, speed])
            continue
        elif size == 20:
            enemy_type = "approach_and_shoot"

        enemies.append([pos, size, enemy_type, direction, speed, None, 0, image, speed])  # original_speed 추가

    return enemies

# bomb 적 등장 설정
bomb_stages = [2, 3, 5, 7, 11]
bomb_appear_interval = 10000  # 10초 간격으로 등장
bomb_last_appear_time = 0
bomb_directions = ["left", "right", "up", "down"]

# bomb 적 추가 함수
def add_bomb_enemy():
    direction = random.choice(bomb_directions)
    size = 40
    pos = [0, 0]
    if direction == "left":
        pos = [0, random.randint(0, win_height - size)]
    elif direction == "right":
        pos = [win_width - size, random.randint(0, win_height - size)]
    elif direction == "up":
        pos = [random.randint(0, win_width - size), 0]
    elif direction == "down":
        pos = [random.randint(0, win_width - size), win_height - size]
    target_pos = [win_width // 2, win_height // 2]  # 중심을 향하도록 설정
    direction_vector = [target_pos[0] - pos[0], target_pos[1] - pos[1]]
    length = math.hypot(direction_vector[0], direction_vector[1])
    direction_normalized = [direction_vector[0] / length, direction_vector[1] / length]
    enemies.append([pos, size, "bomb", direction_normalized, 9, None, 0, enemy_bomb_image, 9])  # enemy_bomb 추가

# 대시보드 그리기 함수
def draw_dashboard(elapsed_stage_time):
    # 플레이 시간 표시
    time_text = font.render(f"Time: {elapsed_stage_time}s", True, WHITE)
    win.blit(time_text, (win_width // 2 - time_text.get_width() // 2, 10))  # 화면 중앙 상단에 표시

    # 체력 표시
    for i in range(current_health):
        win.blit(health_image, (10 + i * (health_image.get_width() + 10), 10))

    # 제거된 적의 수 표시
    enemies_defeated_text = font.render(f"Enemy: {enemies_defeated}", True, WHITE)
    win.blit(enemies_defeated_text, (win_width - enemies_defeated_text.get_width() - 10, 10))  # 오른쪽 상단에 표시

# 화면에 객체 그리기 함수
def draw_objects(player_pos, enemies, background_image, mouse_pos, elapsed_stage_time, collision_image=None, speed_item_pos=None, power_item_pos=None, heal_item_pos=None, heal_item_image=None):
    win.blit(background_image, (0, 0))  # 배경 그리기
    # 보스나 보스의 공격은 여기서 그리지 않습니다.
    # 적 그리기
    for enemy in enemies:
        enemy_pos, enemy_size, enemy_type, _, _, _, _, enemy_image, _ = enemy
        win.blit(enemy_image, (enemy_pos[0], enemy_pos[1]))
    # 아이템 및 플레이어 그리기
    if speed_item_pos:
        win.blit(speed_item_image, speed_item_pos)
    if power_item_pos:
        win.blit(power_item_image, power_item_pos)
    if heal_item_pos and heal_item_image:
        win.blit(heal_item_image, heal_item_pos)
    win.blit(player_image, (player_pos[0], player_pos[1]))
    if collision_image:
        win.blit(collision_image, (player_pos[0], player_pos[1]))
    # 에너지 볼 및 공격 그리기
    for ball in energy_balls:
        color = YELLOW if ball[2] == "yellow" else GREEN
        pygame.draw.circle(win, color, (int(ball[0]), int(ball[1])), 5)
    for attack in attacks:
        pygame.draw.line(win, RED, attack[0], attack[1], attack[2])
    # 마우스 위치 그리기
    pygame.draw.circle(win, RED, mouse_pos, 5)
    # 대시보드 그리기
    draw_dashboard(elapsed_stage_time)

    # 에너지 볼 그리기
    for ball in energy_balls:
        color = YELLOW if ball[2] == "yellow" else GREEN
        pygame.draw.circle(win, color, (int(ball[0]), int(ball[1])), 5)

    # 공격 그리기
    for attack in attacks:
        pygame.draw.line(win, RED, attack[0], attack[1], attack[2])

    # 마우스 위치 그리기
    pygame.draw.circle(win, RED, mouse_pos, 5)

    # 대시보드 그리기 함수 호출
    draw_dashboard(elapsed_stage_time)  # 대시보드 그리기

# 게임 루프
while run:
    if not game_active:
        if not game_over:
            title_screen()
        else:
            draw_end_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # 게임 루프 종료
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if game_over:
                        # 게임 상태 초기화
                        level = 1
                        current_health = 3
                        enemies_defeated = 0
                        player_speed = original_player_speed
                        power_item_active = 0
                        game_over = False
                        game_over_reason = None
                        start_ticks = pygame.time.get_ticks()  # 게임 시작 시간 기록 (게임 오버 시에만 초기화)
                    start_ticks = pygame.time.get_ticks()  # 게임 시작 시간 기록 (항상 초기화)
                    game_active = True  # 게임 시작
                    player_pos = [win_width // 2 - player_width // 2, win_height // 2 - player_height // 2]  # 플레이어 위치 초기화
                    enemies = []
                    stage_start_ticks = pygame.time.get_ticks()  # 스테이지 시작 시간 기록
                    intro_screen(level)  # 스테이지 인트로 화면 표시

                    # 공격 및 에너지 볼 리스트 초기화
                    attacks = []
                    energy_balls = []
                    # 보스 초기화
                    boss.reset()
                    # 스테이지 시간 설정
                    stage_duration = get_stage_duration(level)
    else:
        # 마우스 위치 가져오기
        mouse_pos = pygame.mouse.get_pos()
        total_seconds = (pygame.time.get_ticks() - start_ticks) // 1000  # 전체 게임 경과 시간
        elapsed_stage_time = (pygame.time.get_ticks() - stage_start_ticks) // 1000  # 스테이지 경과 시간

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # 게임 루프 종료
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

        # 플레이어 이동 처리
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

        # 플레이어가 화면 밖으로 나가지 않도록 제한
        player_pos[0] = max(0, min(player_pos[0], win_width - player_width))
        player_pos[1] = max(0, min(player_pos[1], win_height - player_height))

        # 적 생성
        if random.random() < 0.02:  # 2% 확률로 적 생성
            new_enemies = generate_enemies(level)
            enemies.extend(new_enemies)

        # bomb 적 생성
        if level in bomb_stages and pygame.time.get_ticks() - bomb_last_appear_time > bomb_appear_interval:
            add_bomb_enemy()
            bomb_last_appear_time = pygame.time.get_ticks()

        # 보스 등장 체크 및 행동 처리
        boss.check_appear(total_seconds, level)

        # 보스가 활성화된 경우 처리
        if boss.boss_active:
            boss.move()  # 보스 이동
            boss.attack()  # 보스 공격
            if boss.update_attacks(player_pos):  # 보스의 공격과 플레이어의 충돌 체크
                current_health -= 1
                if current_health <= 0:
                    game_active = False
                    game_over = True
                    game_over_reason = "game_over"

        # 적 이동 및 행동 처리
        for enemy in enemies:
            pos, size, enemy_type, direction, speed, target_pos, shots_fired, enemy_image, original_speed = enemy
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
                    direction_vector = [target_pos[0] - pos[0], target_pos[1] - pos[1]]
                    length = math.hypot(direction_vector[0], direction_vector[1])
                    if length != 0:
                        direction_normalized = [direction_vector[0] / length, direction_vector[1] / length]
                        pos[0] += direction_normalized[0] * speed
                        pos[1] += direction_normalized[1] * speed
                        if length < 100:  # 플레이어에게 접근
                            energy_balls.append([pos[0], pos[1], "green", direction_normalized])
                else:
                    direction_vector = [random.choice([-1, 1]), random.choice([-1, 1])]
                    pos[0] += direction_vector[0] * speed
                    pos[1] += direction_vector[1] * speed
            elif enemy_type == "bomb":
                target_pos = [player_pos[0], player_pos[1]]
                direction_vector = [target_pos[0] - pos[0], target_pos[1] - pos[1]]
                length = math.hypot(direction_vector[0], direction_vector[1])
                if length != 0:
                    direction_normalized = [direction_vector[0] / length, direction_vector[1] / length]
                    pos[0] += direction_normalized[0] * speed
                    pos[1] += direction_normalized[1] * speed

        # 공격 이동 및 위치 업데이트
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

        # 공격과 적의 충돌 처리
        new_enemies = []
        for enemy in enemies:
            enemy_pos, enemy_size, _, _, _, _, _, enemy_image, _ = enemy
            hit = False
            for attack in attacks:
                attack_start, attack_end, thickness = attack
                if check_attack_collision(attack_start, attack_end, enemy_pos, enemy_size):
                    hit = True
                    enemies_defeated += 1  # 제거된 적의 수 증가
                    # 아이템 생성 로직
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
                    break  # 한 번 맞으면 해당 적에 대한 충돌 체크 중단
            if not hit:
                new_enemies.append(enemy)
        enemies = new_enemies

        # 플레이어와 적의 충돌 체크
        if not invincible:
            collision = check_collision(player_pos, enemies)
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

        # 무적 시간 처리
        if invincible and pygame.time.get_ticks() - invincible_start_time > invincible_duration:
            invincible = False

        # 충돌 이미지 표시 시간 체크
        if pygame.time.get_ticks() - collision_effect_start_time >= collision_effect_duration:
            collision_image = None

        # 아이템 획득 체크
        # 스피드 아이템
        if speed_item_pos:
            speed_rect = pygame.Rect(speed_item_pos[0], speed_item_pos[1], speed_item_image.get_width(), speed_item_image.get_height())
            player_rect = pygame.Rect(player_pos[0], player_pos[1], player_width, player_height)
            if player_rect.colliderect(speed_rect):
                speed_item_active = True
                speed_item_start_time = pygame.time.get_ticks()
                # 적들의 속도를 감소
                for enemy in enemies:
                    enemy[4] = 7  # 속도를 7로 설정
                speed_item_pos = None

        # 스피드 아이템 지속시간 체크
        if speed_item_active and pygame.time.get_ticks() - speed_item_start_time > speed_item_duration:
            speed_item_active = False
            # 적들의 속도를 원래 속도로 복원
            for enemy in enemies:
                enemy[4] = enemy[8]  # original_speed로 복원

        # 공격력 증가 아이템 획득 체크
        if power_item_pos:
            power_rect = pygame.Rect(power_item_pos[0], power_item_pos[1], power_item_image.get_width(), power_item_image.get_height())
            player_rect = pygame.Rect(player_pos[0], player_pos[1], player_width, player_height)
            if player_rect.colliderect(power_rect):
                power_item_active += 1
                power_item_pos = None

        # 체력 회복 아이템 획득 체크
        if heal_item_pos and current_heal_item_image:
            heal_rect = pygame.Rect(heal_item_pos[0], heal_item_pos[1], current_heal_item_image.get_width(), current_heal_item_image.get_height())
            player_rect = pygame.Rect(player_pos[0], player_pos[1], player_width, player_height)
            if player_rect.colliderect(heal_rect):
                if current_health < max_health:
                    current_health += 1
                heal_item_pos = None
                current_heal_item_image = None

        # 에너지 볼 이동 및 충돌 체크
        new_energy_balls = []
        for ball in energy_balls:
            ball[0] += ball[3][0] * 5  # x 좌표 업데이트
            ball[1] += ball[3][1] * 5  # y 좌표 업데이트
            if 0 <= ball[0] <= win_width and 0 <= ball[1] <= win_height:
                if check_energy_ball_collision((ball[0], ball[1]), player_pos):
                    current_health -= 1
                    if current_health <= 0:
                        game_active = False
                        game_over = True
                        game_over_reason = "game_over"
                else:
                    new_energy_balls.append(ball)
        energy_balls = new_energy_balls

        # 보스와 플레이어 공격 간의 충돌 체크
        boss.check_hit(attacks)

        # 보석과 플레이어의 충돌 체크 및 다음 스테이지로 이동
        if boss.gem_active:
            if boss.check_gem_collision(player_pos):
                # 보석을 획득했을 때 다음 스테이지로 이동
                level += 1  # 다음 스테이지로 이동
                boss.reset()  # 보스 상태 초기화
                boss.boss_defeated = False  # 보스 처치 상태 재설정
                boss.boss_appeared = False  # 보스 등장 여부 재설정
                enemies = []  # 적 목록 초기화
                start_ticks = pygame.time.get_ticks()  # 스테이지 시작 시간 갱신
                stage_start_ticks = pygame.time.get_ticks()
                intro_screen(level)  # 다음 스테이지 인트로 화면 표시
                # 필요한 경우 추가 초기화 로직

        # 화면 업데이트
        background_image = stage_background_images[level - 1] if level - 1 < len(stage_background_images) else stage_background_images[0]
        draw_objects(player_pos, enemies, background_image, mouse_pos, elapsed_stage_time,
                     collision_image, speed_item_pos, power_item_pos, heal_item_pos, current_heal_item_image)
        
        # 보스와 그의 공격을 그리기
        if boss.boss_active and boss.boss_hp > 0:
            boss.draw(win)
            boss.draw_attacks(win)
            boss.draw_health_bar(win, font)
        elif boss.gem_active:
            boss.draw_gem(win)

        # 화면 업데이트
        pygame.display.update()

        # 프레임 설정
        clock.tick(30)

# 게임 종료
pygame.quit()
