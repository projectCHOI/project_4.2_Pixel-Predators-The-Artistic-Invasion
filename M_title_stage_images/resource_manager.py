# 이미지, 사운드, 폰트 로딩 전용
import pygame
import os

class ResourceManager:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.image_dir = os.path.join(self.base_dir, "M_title_stage_images", "assets", "images")
        self.sound_dir = os.path.join(self.base_dir, "M_title_stage_images", "assets", "sounds")
        self.font_dir = os.path.join(self.base_dir, "M_title_stage_images", "assets", "fonts")

    def load_image(self, *path_parts, size=None):
        path = os.path.join(self.image_dir, *path_parts)
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image

    def load_sound(self, filename, volume=1.0):
        path = os.path.join(self.sound_dir, filename)
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        return sound

    def get_font_path(self, filename):
        return os.path.join(self.font_dir, filename)