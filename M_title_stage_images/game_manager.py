import pygame
from M_title_stage_images.config import *

class GameManager:
    def __init__(self, res_manager):
        self.res = res_manager
        self.level = 1
        self.max_level = 9
        self.game_active = False
        self.game_over = False
        self.game_over_reason = None  # "victory", "game_over", "time_over"    
        # 시간 및 기록 관리
        self.start_ticks = 0          # 전체 게임 시작 시간
        self.stage_start_ticks = 0    # 현재 스테이지 시작 시간
        self.enemies_defeated = 0     # 제거한 일반 적 수
        self.game_end_time = None     # 종료 시 기록된 시간
        # 보스 관련
        self.boss = None
        self.boss_active = False
        self.boss_spawn_delay = 20000  
        # 획득한 아이템/보석 기록
        self.collected_gems = []

    def start_game(self):
        """게임 전체를 처음부터 시작 (Level 1)"""
        self.level = 1
        self.enemies_defeated = 0
        self.collected_gems = []
        self.game_active = True
        self.game_over = False
        self.game_over_reason = None
        self.game_end_time = None
        self.start_ticks = pygame.time.get_ticks()
        self.start_stage()
