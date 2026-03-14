# 스테이지 관리, 게임 상태(Over/Victory) 관리
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
        self.game_over_reason = None # "victory", "game_over", "time_over"
