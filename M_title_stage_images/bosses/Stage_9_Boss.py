import pygame
import os
import math
import random

# 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_IMAGE_PATH = os.path.join(BASE_DIR, "assets", "images")

def load_image(*path_parts, size=None):
    path = os.path.join(BASE_IMAGE_PATH, *path_parts)
    image = pygame.image.load(path).convert_alpha()
    if size:
        image = pygame.transform.scale(image, size)
    return image

class Stage9Boss:
    def __init__(self):
        # 이미지 로드
        self.boss_image = load_image("bosses", "boss_stage9_S.png", size=(180, 180))
        self.minion_attack_image = load_image("bosses", "boss_stage9_N.png", size=(60, 60))
        self.attack_images = {
            "phase1": load_image("boss_skilles", "boss_stage9_a.png", size=(40, 40)),
            "phase2": load_image("boss_skilles", "boss_stage9_b.png", size=(40, 40)),
            "phase3": load_image("boss_skilles", "boss_stage9_c.png", size=(40, 40)),
            "phase4": load_image("boss_skilles", "boss_stage9_d.png", size=(40, 40))
        }
        self.gem_image = load_image("items", "mob_Jewelry_9.png", size=(40, 40))

        # 기본 속성 설정
        self.boss_pos = [600, -100]
        self.boss_speed = 5
        self.boss_hp = 100
        self.max_boss_hp = 100
        self.boss_active = False
        self.boss_appeared = False
        self.boss_defeated = False
        self.stage_cleared = False

        # 보스 등장
        self.boss_move_state = "entering"
        self.enter_target_pos = [600, 160]
        self.patterns = [
            {"start": (600, 160), "end": (200, 300)},
            {"start": (600, 160), "end": (600, 300)},
            {"start": (600, 160), "end": (1000, 300)},
        ]
        self.current_pattern = None
        self.pattern_direction = "forward"
        self.pattern_start_time = 0
        self.pattern_duration = 0
        self.elapsed_pattern_time = 0
        self.wave_amplitude = 40
        self.wave_frequency = 0.01
        self.pattern_timer = pygame.time.get_ticks()

        # 공격 관련
        self.boss_attacks = []
        self.boss_phase = 1
        self.attack_cooldown = 2000
        self.last_attack_time = 0

        # 보석
        self.gem_active = False
        self.gem_pos = None

        # 피격 관련
        self.boss_hit = False
        self.boss_hit_start_time = 0
        self.boss_invincible_duration = 500

    def move(self):
        current_time = pygame.time.get_ticks()

        if self.boss_move_state == "entering":
            # 등장: 위에서 아래로 직선 이동
            if self.boss_pos[1] < self.enter_target_pos[1]:
                self.boss_pos[1] += self.boss_speed
            else:
                self.boss_pos[1] = self.enter_target_pos[1]
                self.boss_move_state = "choosing"
        
        elif self.boss_move_state == "choosing":
            self.current_pattern = random.choice(self.patterns)
            self.pattern_direction = "forward"
            self.pattern_timer = current_time
            self.boss_move_state = "patterning"
        
        elif self.boss_move_state == "patterning":
            start = self.current_pattern["start"]
            end = self.current_pattern["end"]
            if self.pattern_direction == "backward":
                start, end = end, start

            total_distance = end[0] - start[0]
            elapsed = (current_time - self.pattern_timer) / 1000  # 초 단위
            move_fraction = min(elapsed / 1.5, 1)  # 1.5초간 이동

            # 보스의 x 이동
            new_x = start[0] + (end[0] - start[0]) * move_fraction
            wave_offset = math.sin(current_time * self.wave_frequency) * self.wave_amplitude
            new_y = start[1] + (end[1] - start[1]) * move_fraction + wave_offset

            self.boss_pos = [new_x, new_y]

            if move_fraction >= 1:
                # 이동 종료 → 대기 상태로 전환
                self.boss_move_state = "waiting"
                self.pattern_timer = current_time
                self.pattern_duration = 3000 if self.pattern_direction == "forward" else 2000
        
        elif self.boss_move_state == "waiting":
            if current_time - self.pattern_timer >= self.pattern_duration:
                if self.pattern_direction == "forward":
                    self.pattern_direction = "backward"
                    self.boss_move_state = "patterning"
                    self.pattern_timer = current_time
                else:
                    # 패턴 종료 후 새 패턴 선택
                    self.boss_move_state = "choosing"
                    
    def draw(self, win):
        win.blit(self.boss_image, self.boss_pos)

    def draw_attacks(self, win):
        image = self.attack_images[f"phase{self.boss_phase}"]
        for attack in self.boss_attacks:
            rotated = pygame.transform.rotate(image, attack.get("angle", 0))
            rect = rotated.get_rect(center=attack["pos"])
            win.blit(rotated, rect)

    def draw_gem(self, win):
        if self.gem_active:
            win.blit(self.gem_image, self.gem_pos)

    def get_current_phase(self):
        if self.boss_hp > 75:
            return 1
        elif self.boss_hp > 50:
            return 2
        elif self.boss_hp > 25:
            return 3
        else:
            return 4

    def update_phase(self):
        self.boss_phase = self.get_current_phase()

    def reset(self):
        self.__init__()
