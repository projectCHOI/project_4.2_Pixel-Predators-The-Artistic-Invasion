import pygame
import random
import math

pygame.init()

# 윈도우 설정
win = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("The Artistic Invasion")

# 타이틀 커버 이미지 불러오기
cover_image = pygame.image.load(r"C:\Users\HOME\Desktop\새싹_교육\GitHub_CHOI\project_4.2_Pixel Predators-The Artistic Invasion\project4.2_cover\Cover_The_Artistic_Invasion_Bright_1200x700.png")

# 배경 이미지 불러오기
background = pygame.image.load(r"C:\Users\HOME\Desktop\새싹_교육\GitHub_CHOI\project_4.2_Pixel Predators-The Artistic Invasion\project4.2_world\WorldAtollReef -J.jpg")

# 종료 시 표시될 이미지
end_image = pygame.image.load(r"C:\Users\HOME\Desktop\새싹_교육\GitHub_CHOI\project_4.2_Pixel Predators-The Artistic Invasion\project4.2_world\WorldCave-J.jpg")

# 플레이어 설정
player_size = 30  # 크기
player_color = (255, 255, 255)  # 색상
player_x = win.get_width() // 2
player_y = win.get_height() // 2
player_speed = 10  # 속도

# 적 이미지 불러오기 및 크기 변경
enemy_image = pygame.image.load(r"C:\Users\HOME\Desktop\새싹_교육\GitHub_CHOI\project_4.2_Pixel Predators-The Artistic Invasion\project4.2_mob\mob_me1_png.png")
enemy_width, enemy_height = 60, 60  # 적 이미지 크기 설정
enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))
enemy_speed = 20

# 적 리스트
enemies = []

# 적 생성 함수
def create_enemy():
    angle = random.uniform(0, 2 * math.pi)  # 랜덤한 각도 생성
    x = win.get_width() // 2 + 600 * math.cos(angle)  # 각도에 따른 x 위치 계산
    y = win.get_height() // 2 + 600 * math.sin(angle)  # 각도에 따른 y 위치 계산
    direction = math.atan2(win.get_height() // 2 - y, win.get_width() // 2 - x)  # 중앙을 향한 방향 벡터 계산
    enemies.append([x, y, direction])

# 폰트 설정 (글씨 크기를 72로 키움)
font = pygame.font.Font(None, 72)

# 게임 시작 여부
game_started = False
game_over = False

# 게임 루프
run = True
clock = pygame.time.Clock()

while run:
    clock.tick(30)  # FPS 설정

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if not game_started:
                if event.key == pygame.K_RETURN:
                    game_started = True
                    game_over = False
                    player_x = win.get_width() // 2
                    player_y = win.get_height() // 2
                    enemies.clear()
            elif game_over:
                if event.key == pygame.K_RETURN:
                    game_started = True
                    game_over = False
                    player_x = win.get_width() // 2
                    player_y = win.get_height() // 2
                    enemies.clear()

    if not game_started:
        win.blit(cover_image, (0, 0))
        text = font.render("Start the game : Enter", True, (255, 255, 255))
        text_rect = text.get_rect(center=(win.get_width() // 2, win.get_height() - 50))
        win.blit(text, text_rect)
        pygame.display.update()
        continue

    if game_over:
        win.blit(end_image, (0, 0))
        text = font.render("Revenge the game : Enter", True, (128, 0, 128))  # 자주색으로 변경
        text_rect = text.get_rect(center=(win.get_width() // 2, win.get_height() // 2))  # 위치 중앙으로 변경
        win.blit(text, text_rect)
        pygame.display.update()
        continue

    # 키 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # 플레이어 경계 처리
    if player_x < 0:
        player_x = 0
    if player_x > win.get_width() - player_size:
        player_x = win.get_width() - player_size
    if player_y < 0:
        player_y = 0
    if player_y > win.get_height() - player_size:
        player_y = win.get_height() - player_size

    # 적 생성 및 이동
    if random.randint(1, 20) == 1:
        create_enemy()

    for enemy in enemies:
        enemy[0] += enemy_speed * math.cos(enemy[2])  # x 방향으로 이동
        enemy[1] += enemy_speed * math.sin(enemy[2])  # y 방향으로 이동
        if (enemy[0] < 0 or enemy[0] > win.get_width() or 
            enemy[1] < 0 or enemy[1] > win.get_height()):
            enemies.remove(enemy)

    # 충돌 검사
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
        if player_rect.colliderect(enemy_rect):
            game_over = True

    # 화면 그리기
    win.blit(background, (0, 0))
    pygame.draw.rect(win, player_color, (player_x, player_y, player_size, player_size))
    for enemy in enemies:
        win.blit(enemy_image, (enemy[0], enemy[1]))
    pygame.display.update()

pygame.quit()
