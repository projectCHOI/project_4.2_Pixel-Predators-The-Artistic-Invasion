import pygame
import sys

# --- 1. 외부 모듈 임포트 ---
try:
    from M_title_stage_images.config import *
    from M_title_stage_images.resource_manager import ResourceManager
    from M_title_stage_images.game_manager import GameManager
    from M_title_stage_images.title_stage_images import title_image, stage_background_images
    # 플레이어 클래스 추가
    from M_title_stage_images.entities.player import Player
    
    print("플레이어를 포함한 모든 시스템 연결 완료.")
except ImportError as e:
    print(f"연결 오류 발생: {e}")
    sys.exit()

def main():
    # 2. 초기화
    pygame.init()
    pygame.mixer.init()
    
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("The Artistic Invasion")
    clock = pygame.time.Clock()

    # 3. 객체 생성
    res = ResourceManager()
    manager = GameManager(res)
    # 플레이어는 일단 None으로 설정 후 게임 시작 시 생성
    player = None

