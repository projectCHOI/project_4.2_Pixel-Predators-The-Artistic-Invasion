import pygame
import os

class BGMController:
    def __init__(self):
        pygame.mixer.init()
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.current_track = None
        self.current_state = None
        pygame.mixer.music.set_volume(0.5)

        # BGM 목록
        self.tracks = {
            "title": "title.wav",
            "loading": "stage_loading.wav",
            "stage_1": "stage_1.wav",
            "stage_2": "stage_2.wav",
            "stage_3": "stage_3.wav",
            "stage_4": "stage_4.wav",
            "stage_5": "stage_5.wav",
            "stage_6": "stage_6.wav",
            "stage_7": "stage_7.wav",
            "stage_8": "stage_8.wav",
            "stage_9": "stage_9.wav",
            "gameover": "gameover.mp3",
            "victory": "victory.mp3"
        }

    def play(self, name_or_filename, loop=True, volume=1.0):
        if name_or_filename in self.tracks:
            filename = self.tracks[name_or_filename]
        else:
            filename = name_or_filename

        path = os.path.join(self.base_path, filename)

        if not os.path.exists(path):
            print(f"[BGM] 파일 없음: {path}")
            return

        if self.current_track != path:
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1 if loop else 0)
                self.current_track = path
                print(f"[BGM] 재생 시작: {filename}")
            except Exception as e:
                print(f"[BGM] 오류: {e}")

    def set_game_state(self, state_name):
        if state_name == self.current_state:
            return
        if state_name not in self.tracks:
            print(f"[BGM] 알 수 없는 상태: {state_name}")
            return
        self.current_state = state_name
        self.play(state_name)

    def stop(self):
        pygame.mixer.music.stop()
        self.current_track = None
        self.current_state = None 
        
    def pause(self):
        pygame.mixer.music.pause()

    def resume(self):
        pygame.mixer.music.unpause()

    def is_playing(self):
        return pygame.mixer.music.get_busy()
