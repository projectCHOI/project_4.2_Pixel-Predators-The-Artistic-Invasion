import pygame

pygame.init()

# 윈도우 설정
win = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("The Artistic Invasion")

# 배경 이미지 불러오기
background = pygame.image.load(r"C:\Users\HOME\Desktop\새싹_교육\GitHub_CHOI\project_4.2_Pixel Predators-The Artistic Invasion\project4.2_world\WorldGrassland-J.jpg")

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
