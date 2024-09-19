#title_stage_images
import pygame
import os

# BASE_DIR은 프로젝트의 루트 디렉토리를 가리킵니다.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 이미지의 기본 경로를 정의합니다.
BASE_IMAGE_PATH = os.path.join(BASE_DIR, "assets", "images")

# 이미지 로딩 함수
def load_image(*path_parts, size=None):
    path = os.path.join(BASE_IMAGE_PATH, *path_parts)
    image = pygame.image.load(path)
    if size:
        image = pygame.transform.scale(image, size)
    return image

# 타이틀 이미지 로드
title_image = load_image("title", "Cover_The_Artistic_Invasion_Bright_1210x718.JPG", size=(1280, 720))

# 스테이지 이미지 로드
stage_intro_images = []
stage_background_images = []

for stage_num in range(1, 13):
    intro_image_filename = f"Stage{stage_num}_World_A.JPG"
    background_image_filename = f"Stage{stage_num}_World_B.JPG"

    intro_image = load_image("stages", intro_image_filename, size=(1280, 720))
    background_image = load_image("stages", background_image_filename, size=(1280, 720))

    stage_intro_images.append(intro_image)
    stage_background_images.append(background_image)
