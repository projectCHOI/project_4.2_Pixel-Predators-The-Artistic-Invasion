# asset_loader
import os
import pygame

def load_image(base_path, *path_parts, size=None):
    path = os.path.join(base_path, *path_parts)
    try:
        image = pygame.image.load(path).convert_alpha()
    except pygame.error as e:
        raise SystemExit(e)
    if size:
        image = pygame.transform.scale(image, size)
    return image
