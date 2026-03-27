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
        self.level = 1
        self.enemies_defeated = 0
        self.collected_gems = []
        self.game_active = True
        self.game_over = False
        self.game_over_reason = None
        self.game_end_time = None
        self.start_ticks = pygame.time.get_ticks()
        self.start_stage()
        
    def start_stage(self):
        self.stage_start_ticks = pygame.time.get_ticks()
        self.boss_active = False
        self.boss = None
        print(f"--- Stage {self.level} Initialized ---")

    def spawn_boss(self, boss_class):
        if boss_class and not self.boss_active:
            self.boss = boss_class()
            self.boss_active = True
            if hasattr(self.boss, 'reset'):
                self.boss.reset()
            return self.boss
        return None

    def update(self, player):
        if not self.game_active:
            return
        now = pygame.time.get_ticks()
        if player.health <= 0:
            self.end_game("game_over")
            return

        elapsed_stage_sec = (now - self.stage_start_ticks) // 1000
        if elapsed_stage_sec >= self.get_stage_duration():
            self.end_game("time_over")
            return
        if self.boss_active and self.boss:
            if hasattr(self.boss, 'hp') and self.boss.hp <= 0:
                self.handle_boss_defeat()

    def handle_boss_defeat(self):
        if hasattr(self.boss, 'gem_image'):
            self.collected_gems.append(self.boss.gem_image) 
        if self.level < self.max_level:
            self.level += 1
            self.start_stage()
        else:
            self.end_game("victory")

    def get_stage_duration(self):
        base_duration = 600  # 기본 10분
        reduction = (self.level - 1) * 10  # 레벨당 10초씩 감소
        return max(300, base_duration - reduction)
