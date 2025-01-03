import pygame
import sys
import os
import subprocess

# Pygame 초기화
pygame.init()

# 화면 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Master Screen")

# 색상 설정
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
HOVER_COLOR = (255, 255, 255)

# 폰트 설정
font_path = os.path.join(os.path.dirname(__file__), "..", "project4.2_cover", "서평원 꺾깎체", "TTF", "SLEIGothicTTF.ttf")
try:
    font = pygame.font.Font(font_path, 30)  # 사용자 지정 폰트 적용
except FileNotFoundError:
    font = pygame.font.SysFont("malgungothic", 30)  # 기본 한글 폰트로 대체

# 버튼 설정
buttons = []
button_width = 80
button_height = 40
padding = 20
rows = 4
cols = 4
for i in range(13):
    row = i // cols
    col = i % cols
    x = 50 + col * (button_width + padding)
    y = 50 + row * (button_height + padding)
    rect = pygame.Rect(x, y, button_width, button_height)
    buttons.append((f"# {i+1}", rect))

# 추가 텍스트 설정
text_f10 = font.render("F10 : 관리자 모드로 이동", True, BLUE)
text_f11 = font.render("F11 : 게임 실행", True, BLUE)

text_f10_rect = text_f10.get_rect(topleft=(20, 50))
text_f11_rect = text_f11.get_rect(topleft=(20, 80))

admin_mode = False

# 게임 루프
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                subprocess.run(["python", "C:\\Users\\boss3\\OneDrive\\바탕 화면\\GitHub\\project_4.2_Pixel-Predators-The-Artistic-Invasion\\M_title_stage_images\\main.py"])
            elif event.key == pygame.K_F10:
                admin_mode = not admin_mode

    # 화면 채우기
    screen.fill(BLACK)

    if admin_mode:
        for text, rect in buttons:
            color = HOVER_COLOR if rect.collidepoint(mouse_pos) else BLUE
            pygame.draw.rect(screen, color, rect)
            label = font.render(text, True, BLACK)
            screen.blit(label, label.get_rect(center=rect.center))
    else:
        screen.blit(text_f10, text_f10_rect)
        screen.blit(text_f11, text_f11_rect)

    # 화면 업데이트
    pygame.display.flip()

# 종료
pygame.quit()
sys.exit()