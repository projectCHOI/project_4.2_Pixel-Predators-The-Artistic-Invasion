import pygame
import sys

WIN_WIDTH = 1210
WIN_HEIGHT = 718
FPS = 60

WHITE = (255, 255, 255)

def main():
    pygame.init()
    
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("The Artistic Invasion - Base")
    
    clock = pygame.time.Clock()

    # 메인 루프
    run = True
    while run:
        # --- A. 이벤트 처리 ---
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