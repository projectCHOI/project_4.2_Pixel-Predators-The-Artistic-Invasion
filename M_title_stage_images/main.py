import pygame
import random
import math
import os
import sys

pygame.init()

# 윈도우 설정
win = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("The Artistic Invasion")

# BASE_DIR은 프로젝트의 루트 디렉토리를 가리킵니다.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 이미지의 기본 경로를 정의합니다.
BASE_IMAGE_PATH = os.path.join(BASE_DIR, "assets", "images")

# 이미지 로딩 함수
def load_image(*path_parts, size=None):
    path = os.path.join(BASE_IMAGE_PATH, *path_parts)
    image = pygame.image.load(path).convert_alpha()
    if size:
        image = pygame.transform.scale(image, size)
    return image

# 모듈에서 타이틀 및 스테이지 이미지 임포트
from title_stage_images import title_image, stage_intro_images, stage_background_images

# 보스 클래스를 동적으로 임포트하는 함수
def get_boss_class(stage):
    module_name = f"bosses.Stage_{stage}_Boss"
    class_name = f"Stage{stage}Boss"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    bosses_dir = os.path.join(current_dir, "bosses")
    if bosses_dir not in sys.path:
        sys.path.append(bosses_dir)
    try:
        module = __import__(module_name, fromlist=[class_name])
        boss_class = getattr(module, class_name)
        return boss_class
    except (ImportError, AttributeError) as e:
        print(f"Error importing boss class: {e}")
        return None

# 이미지 크기 설정
image_size = (40, 40)
player_width, player_height = image_size

# 플레이어 이미지 로드
player_image1 = load_image("player", "mob_me1_png.png", size=image_size)
player_image2 = load_image("player", "mob_me2_png.png", size=image_size)

# 초기 플레이어 이미지
player_image = player_image1

# 플레이어 설정
player_speed = 10  # 속도 조정
original_player_speed = player_speed

# 플레이어 위치 초기화
player_pos = [640 - player_width // 2, 360 - player_height // 2]

# Health 설정
health_image = load_image("player", "mob_Life.png", size=image_size)
max_health = 5
current_health = 3

# 색상 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# 에너지 볼 설정
energy_balls = []

# 공격 설정
attacks = []
attack_speed = 20
enemies_defeated = 0  # 제거된 적의 수

# 마우스 클릭 추적
mouse_down_time = 0
mouse_held = False

# 게임 설정
clock = pygame.time.Clock()
font_path = os.path.join(BASE_DIR, "assets", "fonts", "SLEIGothicOTF.otf")
font_size = 30  # 폰트 크기
font = pygame.font.Font(font_path, font_size)  # 폰트 설정
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

# 획득한 별 이미지 추적
collected_stars = []

# 게임 오버 상태 및 이유
game_over = False
game_over_reason = None  # "victory", "game_over", "time_over"

# 게임 종료 상태 이미지 로드
victory_image = load_image("stages", "Stage14_Victory.JPG", size=(1280, 720))
game_over_image = load_image("stages", "Stage15_GameOver.JPG", size=(1280, 720))
time_over_image = load_image("stages", "Stage16_TimeOver.JPG", size=(1280, 720))

# 보스 관련 변수 초기화
boss_spawned = False
current_boss = None
boss_defeated = False
mob_jewelry_pos = None
show_mob_jewelry = False

# mob_Jewelry 이미지 로드
mob_jewelry_image = load_image("items", f"mob_Jewelry_{level}.png", size=(40, 40))

# 공격력 증가 아이템 설정
power_item_active = 0  # 공격력 증가 아이템 획득 수

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
    enemies_defeated_text = font.render(f"Defeated: {enemies_defeated}", True, WHITE)
    win.blit(enemies_defeated_text, (1280 - enemies_defeated_text.get_width() - 10, 10))  # 오른쪽에 맞춤

# 게임 종료 화면 그리기 함수
def draw_end_screen():
    if game_over_reason == "victory":
        image = victory_image
    elif game_over_reason == "game_over":
        image = game_over_image
    elif game_over_reason == "time_over":
        image = time_over_image

    win.blit(image, (0, 0))
    text = font.render("Press Enter to Continue", True, WHITE)
    win.blit(text, (640 - text.get_width() // 2, 360 - text.get_height() // 2))  # 화면 중앙에 맞춤

    # 획득한 별 표시
    star_spacing = 60  # 이미지 간격 60 픽셀
    for idx, collected_star in enumerate(collected_stars):
        win.blit(collected_star, (640 - (len(collected_stars) * star_spacing) // 2 + idx * star_spacing, 450))

    pygame.display.update()

# 타이틀 화면
def title_screen():
    win.blit(title_image, (0, 0))
    pygame.display.update()

# 인트로 화면
def intro_screen(stage):
    win.blit(stage_intro_images[stage - 1], (0, 0))
    pygame.display.update()
    pygame.time.delay(3000)

# 플레이어와 객체의 충돌 체크 함수
def player_collides_with(player_pos, obj_pos, obj_size):
    px, py = player_pos
    ox, oy = obj_pos
    player_rect = pygame.Rect(px, py, player_width, player_height)
    obj_rect = pygame.Rect(ox, oy, obj_size, obj_size)
    return player_rect.colliderect(obj_rect)

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
                        boss_spawned = False
                        boss_defeated = False
                        show_mob_jewelry = False
                        mob_jewelry_pos = None
                    game_active = True
                    player_pos = [640 - player_width // 2, 360 - player_height // 2]
                    # 보스 초기화
                    current_boss = None
                    boss_spawned = False
                    boss_defeated = False
                    show_mob_jewelry = False
                    mob_jewelry_pos = None
                    start_ticks = pygame.time.get_ticks()
                    intro_screen(level)
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
                # 공격력 증가 아이템에 따른 공격 생성
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

        # 보스 생성 및 관리
        if not boss_spawned:
            BossClass = get_boss_class(level)
            if BossClass:
                current_boss = BossClass()
                boss_spawned = True
                boss_defeated = False
            else:
                # 보스 클래스를 찾지 못한 경우 처리
                pass

        if current_boss:
            current_boss.check_appear(seconds)

            if current_boss.boss_active:
                # 보스 이동
                current_boss.move()
                # 보스 공격
                current_boss.attack()
                # 보스 그리기
                current_boss.draw(win)
                # 보스 공격 그리기
                current_boss.draw_attacks(win)
                # 보스 공격 업데이트 및 플레이어와의 충돌 체크
                boss_attack_result = current_boss.update_attacks(player_pos)
                if boss_attack_result == 2:
                    # 플레이어가 보스의 공격에 맞았을 때 처리
                    current_health -= 1
                    if current_health <= 0:
                        game_active = False
                        game_over = True
                        game_over_reason = "game_over"
                # 플레이어의 공격이 보스에게 맞았는지 체크
                current_boss.check_hit(attacks)
            elif current_boss.boss_defeated and not boss_defeated:
                # 보스가 패배한 후 처리
                mob_jewelry_pos = current_boss.gem_pos
                show_mob_jewelry = True
                boss_defeated = True
                current_boss = None  # 보스 객체 제거

        # 플레이어가 mob_Jewelry를 획득하면 다음 스테이지로 이동
        if show_mob_jewelry:
            win.blit(mob_jewelry_image, mob_jewelry_pos)
            if player_collides_with(player_pos, mob_jewelry_pos, 40):
                collected_stars.append(mob_jewelry_image)  # 획득한 별 이미지 추가
                level += 1
                if level > max_level:
                    game_active = False
                    game_over = True
                    game_over_reason = "victory"
                else:
                    # 다음 스테이지 초기화
                    boss_spawned = False
                    boss_defeated = False
                    show_mob_jewelry = False
                    mob_jewelry_pos = None
                    # mob_Jewelry 이미지 업데이트
                    mob_jewelry_image = load_image("items", f"mob_Jewelry_{level}.png", size=(40, 40))
                    # 필요한 초기화 작업 수행
                    intro_screen(level)
                    start_ticks = pygame.time.get_ticks()
                    player_pos = [640 - player_width // 2, 360 - player_height // 2]
                    attacks = []
                    energy_balls = []

        # 공격 업데이트
        new_attacks = []
        for attack in attacks:
            start, end, thickness = attack
            direction = (end[0] - start[0], end[1] - start[1])
            length = math.hypot(direction[0], direction[1])
            if length == 0:
                continue
            direction = (direction[0] / length * attack_speed, direction[1] / length * attack_speed)
            new_end = (start[0] + direction[0], start[1] + direction[1])
            if 0 <= new_end[0] <= 1280 and 0 <= new_end[1] <= 720:
                new_attacks.append((start, new_end, thickness))
        attacks = new_attacks

        # 화면 그리기
        draw_objects(player_pos, [], stage_background_images[level - 1], mouse_pos, collision_image)

        clock.tick(30)

pygame.quit()
