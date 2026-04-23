import pygame
import sys
import os

try:
    from M_title_stage_images.resource_manager import ResourceManager
    from M_title_stage_images.title_stage_images import title_image, stage_background_images
    print("모든 모듈이 성공적으로 로드되었습니다.")
except ImportError as e:
    print(f"모듈 로드 중 오류 발생: {e}")
    sys.exit()

WIN_WIDTH = 1280
WIN_HEIGHT = 720
FPS = 60
WHITE = (255, 255, 255)

def main():
    pygame.init()
    pygame.mixer.init()
    
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("The Artistic Invasion")
    clock = pygame.time.Clock()


    res = ResourceManager()

    game_state = 0 

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = 1

        if game_state == 0:
            win.blit(title_image, (0, 0))
        else:
            if stage_background_images:
                win.blit(stage_background_images[0], (0, 0))
            else:
                win.fill(WHITE)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()