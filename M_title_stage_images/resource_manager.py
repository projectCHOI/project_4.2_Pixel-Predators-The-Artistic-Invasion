import pygame
import sys
import os

try:
    from M_title_stage_images.resource_manager import ResourceManager
    print("ResourceManager를 성공적으로 불러왔습니다.")
except ImportError as e:
    print(f"모듈 로드 오류: {e}")
    sys.exit()

WIN_WIDTH = 800
WIN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
