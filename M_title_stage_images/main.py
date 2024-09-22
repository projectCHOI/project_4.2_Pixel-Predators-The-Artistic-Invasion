import pygame
import random
import math
import os
from bosses.Stage_1_Boss import Stage1Boss  # Stage_1_Boss 모듈 임포트

pygame.init()

# 기본 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_IMAGE_PATH = os.path.join(BASE_DIR, "assets", "images")
WIN_WIDTH, WIN_HEIGHT = 1280, 720
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Game Title")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# 폰트 설정
font_path = os.path.join(BASE_DIR, "assets", "fonts", "SLEIGothicOTF.otf")
font_size = 30
font = pygame.font.Font(font_path, font_size)

# 이미지 로드 함수
def load_image(*path_parts, size=None):
    path = os.path.join(BASE_IMAGE_PATH, *path_parts)
    image = pygame.image.load(path).convert_alpha()
    if size:
        image = pygame.transform.scale(image, size)
    return image

# 플레이어 설정
player_size = (40, 40)
player_image1 = load_image("players", "player1.png", size=player_size)
player_image2 = load_image("players", "player2.png", size=player_size)
player_image = player_image1
player_pos = [640 - player_size[0] // 2, 360 - player_size[1] // 2]
player_speed = 5
original_player_speed = player_speed

# 적 설정
enemy_images = {
    "up": load_image("enemies", "enemy_up.png", size=(40, 40)),
    "down": load_image("enemies", "enemy_down.png", size=(40, 40)),
    "left": load_image("enemies", "enemy_left.png", size=(40, 40)),
    "right": load_image("enemies", "enemy_right.png", size=(40, 40)),
}

# 아이템 이미지 로드
speed_item_image = load_image("items", "item_speed.png", size=(40, 40))
power_item_image = load_image("items", "item_power.png", size=(40, 40))
heal_item_images = [
    load_image("items", "item_heal_1.png", size=(40, 40)),
    load_image("items", "item_heal_2.png", size=(40, 40)),
]

# 배경 이미지 로드
stage_background_images = []
for i in range(1, 13):
    bg_image = load_image("backgrounds", f"stage_{i}.png", size=(WIN_WIDTH, WIN_HEIGHT))
    stage_background_images.append(bg_image)

# 기타 설정
clock = pygame.time.Clock()
run = True
game_active = False
game_over = False
game_over_reason = None
level = 1
max_level = 12
current_health = 3
max_health = 3
collected_stars = []
enemies_defeated = 0
attacks = []
energy_balls = []
invincible = False
invincible_start_time = 0
invincible_duration = 2000  # 2초 무적
collision_image = None
collision_effect_start_time = 0
collision_effect_duration = 0
collision_images = {
    1: {"image": load_image("effects", "collision1.png", size=player_size), "duration": 500},
    2: {"image": load_image("effects", "collision2.png", size=player_size), "duration": 500},
    3: {"image": load_image("effects", "collision3.png", size=player_size), "duration": 500},
}
speed_item_chance = 0.1
power_item_chance = 0.1
heal_item_chance = 0.1
speed_item_active = False
speed_item_start_time = 0
speed_item_duration = 5000  # 5초 지속
power_item_active = 0
power_item_pos = None
speed_item_pos = None
heal_item_pos = None
current_heal_item_image = None
bomb_stages = [4, 8, 12]
bomb_last_appear_time = 0
bomb_appear_interval = 10000  # 10초마다 폭탄 등장
start_ticks = pygame.time.get_ticks()  # 시작 시간
mouse_pos = (0, 0)

# 보스 인스턴스 생성
stage1_boss = Stage1Boss()

# 함수 정의
def intro_screen(level):
    # 레벨 시작 전 인트로 화면 표시
    intro_text = font.render(f"Stage {level}", True, WHITE)
    win.blit(stage_background_images[level - 1], (0, 0))
    win.blit(intro_text, (640 - intro_text.get_width() // 2, 360 - intro_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)

def title_screen():
    # 타이틀 화면 표시
    title_text = font.render("Game Title", True, WHITE)
    start_text = font.render("Press Enter to Start", True, WHITE)
    win.blit(stage_background_images[0], (0, 0))
    win.blit(title_text, (640 - title_text.get_width() // 2, 300))
    win.blit(start_text, (640 - start_text.get_width() // 2, 400))
    pygame.display.update()

def draw_dashboard():
    # 대시보드 그리기
    elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
    time_text = font.render(f"{elapsed_time}", True, WHITE)
    win.blit(time_text, (640 - time_text.get_width() // 2, 10))
    # 체력 표시
    for i in range(current_health):
        pygame.draw.rect(win, RED, (10 + i * 50, 10, 40, 40))
    # 제거된 적의 수 표시
    enemies_defeated_text = font.render(f"Defeated: {enemies_defeated}", True, WHITE)
    win.blit(enemies_defeated_text, (WIN_WIDTH - enemies_defeated_text.get_width() - 10, 10))

def draw_objects(player_pos, enemies, background_image, mouse_pos, collision_image=None, speed_item_pos=None, power_item_pos=None, heal_item_pos=None, heal_item_image=None):
    win.blit(background_image, (0, 0))
    win.blit(player_image, (player_pos[0], player_pos[1]))
    if collision_image:
        win.blit(collision_image, (player_pos[0], player_pos[1]))
    for enemy in enemies:
        enemy_pos, enemy_size, enemy_type, _, _, _, _, enemy_image, _ = enemy
        win.blit(enemy_image, (enemy_pos[0], enemy_pos[1]))
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
    # 대시보드 그리기
    draw_dashboard()

def draw_end_screen():
    if game_over_reason == "victory":
        image = load_image("screens", "victory.png", size=(WIN_WIDTH, WIN_HEIGHT))
    elif game_over_reason == "game_over":
        image = load_image("screens", "game_over.png", size=(WIN_WIDTH, WIN_HEIGHT))
    elif game_over_reason == "time_over":
        image = load_image("screens", "time_over.png", size=(WIN_WIDTH, WIN_HEIGHT))

    win.blit(image, (0, 0))
    text = font.render("Continue: Enter", True, WHITE)
    win.blit(text, (640 - text.get_width() // 2, 360 - text.get_height() // 2))

    # 획득한 보석 표시
    star_spacing = 60
    for idx, collected_star in enumerate(collected_stars):
        win.blit(collected_star, (640 - (len(collected_stars) * star_spacing) // 2 + idx * star_spacing, 450))

    # 총 플레이 시간 계산 및 표시
    minutes, seconds = calculate_total_play_time()
    total_time_text = font.render(f"Total play time: {minutes}m {seconds}s", True, WHITE)
    win.blit(total_time_text, (640 - total_time_text.get_width() // 2, 680))

    pygame.display.update()

def calculate_total_play_time():
    total_seconds = sum(time for time in stage_clear_times if time is not None)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return minutes, seconds

# 스테이지 클리어 시간 저장
stage_clear_times = [None] * 12  # 스테이지 1부터 12까지

def record_stage_clear_time(stage, time_taken):
    stage_clear_times[stage - 1] = time_taken

# 게임 루프
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
                        collected_stars = []
                        enemies_defeated = 0
                        player_speed = original_player_speed
                        power_item_active = 0
                        game_over = False
                        game_over_reason = None
                        stage_clear_times = [None] * 12
                        stage1_boss.reset()
                    game_active = True
                    player_pos = [640 - player_size[0] // 2, 360 - player_size[1] // 2]
                    enemies = []
                    attacks = []
                    energy_balls = []
                    speed_item_active = False
                    power_item_active = 0
                    speed_item_pos = None
                    power_item_pos = None
                    heal_item_pos = None
                    current_heal_item_image = None
                    start_ticks = pygame.time.get_ticks()
                    intro_screen(level)
    else:
        mouse_pos = pygame.mouse.get_pos()
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                attack_start = (player_pos[0] + player_size[0] // 2, player_pos[1] + player_size[1] // 2)
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

        # 플레이어 화면 이탈 방지
        if player_pos[0] < 0:
            player_pos[0] = 0
        if player_pos[0] > WIN_WIDTH - player_size[0]:
            player_pos[0] = WIN_WIDTH - player_size[0]
        if player_pos[1] < 0:
            player_pos[1] = 0
        if player_pos[1] > WIN_HEIGHT - player_size[1]:
            player_pos[1] = WIN_HEIGHT - player_size[1]

        # 보스 등장 체크
        stage1_boss.check_appear(seconds, level)

        # 보스가 활성화된 경우
        if stage1_boss.boss_active:
            # 보스 이동
            stage1_boss.move()

            # 보스 공격 생성
            stage1_boss.attack()

            # 보스 공격 업데이트 및 플레이어와의 충돌 체크
            if stage1_boss.update_attacks(player_pos):
                current_health -= stage1_boss.boss_damage
                if current_health <= 0:
                    game_active = False
                    game_over = True
                    game_over_reason = "game_over"

            # 플레이어의 공격이 보스에게 맞았는지 체크
            stage1_boss.check_hit(attacks)

        # 보스가 보석을 드롭했을 때
        if stage1_boss.gem_active:
            # 보석 그리기
            stage1_boss.draw_gem(win)

            # 플레이어가 보석을 획득했는지 체크
            if stage1_boss.check_gem_collision(player_pos):
                collected_stars.append(stage1_boss.gem_image)
                stage1_boss.gem_active = False
                stage1_boss.reset()

                # 스테이지 클리어 시간 기록
                record_stage_clear_time(level, seconds)
                level += 1

                if level > max_level:
                    game_active = False
                    game_over = True
                    game_over_reason = "victory"
                else:
                    # 다음 레벨을 위한 초기화
                    player_pos = [640 - player_size[0] // 2, 360 - player_size[1] // 2]
                    intro_screen(level)
                    start_ticks = pygame.time.get_ticks()
                    enemies = []
                    attacks = []
                    energy_balls = []
                    speed_item_active = False
                    power_item_active = 0
                    speed_item_pos = None
                    power_item_pos = None
                    heal_item_pos = None
                    current_heal_item_image = None
                    # 다음 스테이지의 보스 초기화 (필요한 경우)

        # 화면 그리기
        draw_objects(player_pos, [], stage_background_images[level - 1], mouse_pos, collision_image, speed_item_pos, power_item_pos, heal_item_pos, current_heal_item_image)

        # 보스 및 보스 공격 그리기
        if stage1_boss.boss_active:
            stage1_boss.draw(win)
            stage1_boss.draw_attacks(win)
            stage1_boss.draw_health_bar(win, font)

        # 보석 그리기
        if stage1_boss.gem_active:
            stage1_boss.draw_gem(win)

        pygame.display.update()
        clock.tick(30)

pygame.quit()
