import pygame
import sys
import os
import math

pygame.init()
pygame.mixer.init()

try:
    from M_title_stage_images.config import *
except ImportError:
    WIN_WIDTH, WIN_HEIGHT, FPS = 1280, 720, 30
    RED, BLACK, WHITE, YELLOW = (255,0,0), (0,0,0), (255,255,255), (255,255,0)

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("The Artistic Invasion")

try:
    from M_title_stage_images.resource_manager import ResourceManager
    from M_title_stage_images.game_manager import GameManager
    from M_title_stage_images.entities.player import Player
    from M_title_stage_images.entities.bullets import Bullet
    from M_title_stage_images.entities.items import spawn_item_by_chance
    from M_title_stage_images.title_stage_images import title_image, stage_background_images
    
    from M_title_stage_images.enemy_behaviors.move_and_disappear import generate as gen_move_and_disappear
    import M_title_stage_images.enemy_behaviors.bomb as enemy_bomb
    import M_title_stage_images.enemy_behaviors.group_unit as enemy_group
    import M_title_stage_images.enemy_behaviors.move_and_shoot as enemy_ambush
    from M_title_stage_images.assets.sounds.bgm_controller import BGMController
    
    # 🔍 전체 6개 스테이지 보스 모듈 완벽 연결!
    from M_title_stage_images.bosses.Stage_1_Boss import Stage1Boss
    from M_title_stage_images.bosses.Stage_2_Boss import Stage2Boss
    from M_title_stage_images.bosses.Stage_3_Boss import Stage3Boss
    from M_title_stage_images.bosses.Stage_4_Boss import Stage4Boss
    from M_title_stage_images.bosses.Stage_5_Boss import Stage5Boss
    from M_title_stage_images.bosses.Stage_6_Boss import Stage6Boss

    print("전체 보스모듈 연결")
except Exception as e:
    print(f"모듈 로드 중 오류 발생: {e}")
    pygame.quit()
    sys.exit()

def main():
    clock = pygame.time.Clock()
    res = ResourceManager()
    manager = GameManager(res)
    player = None
    
    stage_start_time = 0
    bgm = BGMController()
    bgm.set_game_state("title") 
    
    # 전체 보스 인스턴스 테이블 (스테이지 1~6)
    bosses = {
        1: Stage1Boss(res),
        2: Stage2Boss(res),
        3: Stage3Boss(res),
        4: Stage4Boss(res),
        5: Stage5Boss(res),
        6: Stage6Boss(res)
    }
    
    player_bullets = pygame.sprite.Group()
    items_group = pygame.sprite.Group()
    enemies = []
    purple_bullets = []
    
    last_spawn_times = {"normal": 0, "bomb": 0, "group": 0, "ambush": 0}
    intervals = {"normal": 3000, "bomb": 5000, "group": 8000, "ambush": 6000}
    last_manager_level = 1

    run = True
