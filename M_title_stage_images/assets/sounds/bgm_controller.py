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


# M_title_stage_images/assets/sounds/bgm_controller.py

import pygame
import os

class BGMController:
    def __init__(self):
        pygame.mixer.init()
        self.base_path = os.path.dirname(os.path.abspath(__file__))  # sounds 폴더
        self.current_track = None

        self.tracks = {
            "title": "title.mp3",
            "loading": "stage_loading.mp3",
            "stage_1": "stage_1.mp3",
            "stage_2": "stage_2.mp3",
            "stage_3": "stage_3.mp3",
            "stage_4": "stage_4.mp3",
            "stage_5": "stage_5.mp3",
            "stage_6": "stage_6.mp3",
            "stage_7": "stage_7.mp3",
            "stage_8": "stage_8.mp3",
            "stage_9": "stage_9.mp3",
            "gameover": "gameover.mp3",
            "victory": "victory.mp3"
        }

    def play(self, name, loop=True, volume=1.0):
        if name not in self.tracks:
            print(f"[BGM] '{name}' 트랙 없음")
            return

        path = os.path.join(self.base_path, self.tracks[name])

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1 if loop else 0)
            self.current_track = name
            print(f"[BGM] Playing: {name}")
        except Exception as e:
            print(f"[BGM] 오류 발생: {e}")

    def stop(self):
        pygame.mixer.music.stop()
        self.current_track = None

    def is_playing(self):
        return pygame.mixer.music.get_busy()
