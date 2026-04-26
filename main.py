import pygame
import sys
import os

pygame.init()
pygame.mixer.init()

try:
    from M_title_stage_images.config import WIN_WIDTH, WIN_HEIGHT, FPS, RED, BLACK, WHITE, YELLOW
except ImportError:
    WIN_WIDTH, WIN_HEIGHT = 1280, 720
    FPS = 30
    RED, BLACK, WHITE, YELLOW = (255,0,0), (0,0,0), (255,255,255), (255,255,0)


win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("The Artistic Invasion")
