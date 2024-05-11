import pygame
pygame.init()
win = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("The Artistic Invasion")

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()