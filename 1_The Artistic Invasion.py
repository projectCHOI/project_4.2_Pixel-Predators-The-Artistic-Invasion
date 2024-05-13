import pygame

pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Dodge a Red Box")

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # 배경 이미지를 화면에 그리기
    win.blit(background, (0, 0))

    # 화면 업데이트
    pygame.display.update()

pygame.quit()
