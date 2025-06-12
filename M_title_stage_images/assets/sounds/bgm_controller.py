import pygame
import os

class BGMController:
    def __init__(self):
        pygame.mixer.init()
        self.current_music = None
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.sound_dir = os.path.join(self.base_dir, "assets", "sounds")

    def play(self, filename, loop=True, volume=1.0):
        """ 음악 재생 (loop: True면 무한반복) """
        full_path = os.path.join(self.sound_dir, filename)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"음악 파일이 존재하지 않습니다: {full_path}")
        
        if self.current_music != full_path:
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1 if loop else 0)
            self.current_music = full_path

    def stop(self):
        pygame.mixer.music.stop()
        self.current_music = None

    def pause(self):
        pygame.mixer.music.pause()

    def resume(self):
        pygame.mixer.music.unpause()


import pygame
import os
import sys

# bgm_controller 모듈 임포트
sys.path.append(os.path.join(os.path.dirname(__file__), "assets", "sounds"))
from bgm_controller import BGMController

# Pygame 초기화
pygame.init()

# BGM 컨트롤러 생성
bgm = BGMController()

# 예시: 타이틀 화면 음악 재생
bgm.play("title")

# 예시: 스테이지 시작
def start_stage(stage_num):
    bgm.play(f"stage_{stage_num}")

# 예시: 게임 종료
def handle_gameover():
    bgm.play("gameover", loop=False)

# 예시: 게임 승리
def handle_victory():
    bgm.play("victory", loop=False)