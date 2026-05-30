import pygame
import sys
import os
import math

# --- [STEP 1] 기초 초기화 및 화면 설정 ---
pygame.init()
pygame.mixer.init()

try:
    from M_title_stage_images.config import *
except ImportError:
    WIN_WIDTH, WIN_HEIGHT, FPS = 1280, 720, 30
    RED, BLACK, WHITE, YELLOW = (255,0,0), (0,0,0), (255,255,255), (255,255,0)

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("The Artistic Invasion")

# --- [STEP 2] 모듈 임포트 ---
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

    print("오디오 시스템(BGM)을 포함한 모든 모듈 연결 완료.")
except Exception as e:
    print(f"모듈 로드 중 오류 발생: {e}")
    pygame.quit()
    sys.exit()

def main():
    clock = pygame.time.Clock()
    res = ResourceManager()
    manager = GameManager(res)
    player = None
    
    # 타이머 및 BGM 컨트롤러 초기화
    stage_start_time = 0
    bgm = BGMController()
    bgm.set_game_state("title") 
    
    player_bullets = pygame.sprite.Group()
    items_group = pygame.sprite.Group()
    enemies = []
    purple_bullets = []
    
    last_spawn_times = {"normal": 0, "bomb": 0, "group": 0, "ambush": 0}
    intervals = {"normal": 3000, "bomb": 5000, "group": 8000, "ambush": 6000}
    last_manager_level = 1

    run = True
    while run:
            now = pygame.time.get_ticks()

            # --- [1] 이벤트 처리 ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    run = False
                
                if not manager.game_active:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        player = Player(res)
                        player_bullets.empty()
                        items_group.empty()
                        enemies = []
                        purple_bullets = []
                        manager.start_game()
                        
                        # 타이머 및 BGM 동기화 초기화
                        stage_start_time = pygame.time.get_ticks()
                        bgm.set_game_state(f"stage_{manager.level}")
                        last_manager_level = manager.level
                        
                elif manager.game_active and player:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        from M_title_stage_images.entities.bullets import EnergyBall
                        
                        # 플레이어의 파워 레벨 설정 매핑
                        power_configs = {
                            0: {"count": 1, "spread": 0},
                            1: {"count": 3, "spread": 15},
                            2: {"count": 5, "spread": 12},
                            3: {"count": 7, "spread": 10},
                            4: {"count": 9, "spread": 8}
                        }
                        
                        config = power_configs.get(player.power_level, {"count": 1, "spread": 0})
                        count = config["count"]
                        spread_interval = config["spread"]
                        
                        # 부채꼴 중앙 정렬 각도 계산 루프 사격
                        for i in range(count):
                            if count == 1:
                                offset = 0
                            else:
                                offset = (i - (count - 1) / 2) * spread_interval
                            
                            new_ball = EnergyBall(player.rect.center, res, mouse_pos, angle_offset=offset)
                            player_bullets.add(new_ball)