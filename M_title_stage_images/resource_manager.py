import pygame
import sys
import os

try:
    from M_title_stage_images.resource_manager import ResourceManager
    print("ResourceManager를 성공적으로 불러왔습니다.")
except ImportError as e:
    print(f"모듈 로드 오류: {e}")
    sys.exit()

WIN_WIDTH = 800
WIN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)

def main():
    # 2. 초기화
    pygame.init()
    pygame.mixer.init()
    
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("The Artistic Invasion - Resource Ready")
    clock = pygame.time.Clock()

    res = ResourceManager()

    # 메인 루프
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        win.fill(WHITE)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()