import pygame
import sys
import os

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
BLUE = (00, 000, 255)

# 폰트 설정
font_path = os.path.join(os.path.dirname(__file__), "..", "project4.2_cover", "서평원 꺾깎체", "TTF", "SLEIGothicTTF.ttf")
try:
    font = pygame.font.Font(font_path, 30)  # 사용자 지정 폰트 적용
except FileNotFoundError:
    font = pygame.font.SysFont("malgungothic", 30)  # 기본 한글 폰트로 대체

text = font.render("apple", True, WHITE)
text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))

# 추가 텍스트 설정
text_f9 = font.render("F9 : 스테이지 선택 화면으로 이동", True, BLUE)
text_f10 = font.render("F10 : 관리자 모드로 이동", True, BLUE)
text_f11 = font.render("F11 : 게임 실행", True, BLUE)

text_f9_rect = text_f9.get_rect(topleft=(20, 20))
text_f10_rect = text_f10.get_rect(topleft=(20, 50))
text_f11_rect = text_f11.get_rect(topleft=(20, 80))

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 화면 채워기
    screen.fill(BLACK)
    
    # 텍스트 그리기
    screen.blit(text, text_rect)
    screen.blit(text_f9, text_f9_rect)
    screen.blit(text_f10, text_f10_rect)
    screen.blit(text_f11, text_f11_rect)
    
    # 화면 업데이트
    pygame.display.flip()

# 종료
pygame.quit()
sys.exit()
