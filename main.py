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
