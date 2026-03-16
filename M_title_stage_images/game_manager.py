import pygame
from M_title_stage_images.config import *

class GameManager:
    def __init__(self, res_manager):
        self.res = res_manager
        self.level = 1
        self.max_level = 9
        
        # 게임 상태 관리
        self.game_active = False
        self.game_over = False
        self.game_over_reason = None
        
        # 시간 및 점수
        self.start_ticks = 0
        self.stage_start_ticks = 0
        self.enemies_defeated = 0
        self.game_end_time = None
        
        # 리소스
        self.collected_gems = []

    def start_game(self):
        self.level = 1
        self.enemies_defeated = 0
        self.collected_gems = []
        self.game_active = True
        self.game_over = False
        self.start_ticks = pygame.time.get_ticks()
        self.start_stage()

    def start_stage(self):
        self.stage_start_ticks = pygame.time.get_ticks()
        print(f"Stage {self.level} Started!")

    def update(self, player_health):
        if not self.game_active:
            return
        if player_health <= 0:
            self.end_game("game_over")

        elapsed = (pygame.time.get_ticks() - self.stage_start_ticks) // 1000
        stage_duration = self.get_stage_duration()
        if elapsed >= stage_duration:
            self.end_game("time_over")

    def get_stage_duration(self):
        base = 600
        reduction = (self.level - 1) * 5
        return max(300, base - reduction)

    def next_level(self):
        if self.level < self.max_level:
            self.level += 1
            self.start_stage()
        else:
            self.end_game("victory")

    def end_game(self, reason):
        self.game_active = False
        self.game_over = True
        self.game_over_reason = reason
        self.game_end_time = (pygame.time.get_ticks() - self.start_ticks) // 1000