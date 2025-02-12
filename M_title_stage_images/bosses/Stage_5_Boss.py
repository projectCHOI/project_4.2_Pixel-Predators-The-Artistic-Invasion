import pygame
import os
import random

# BASE_DIR 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_IMAGE_PATH = os.path.join(BASE_DIR, "assets", "images")

def load_image(*path_parts, size=None):
    path = os.path.join(BASE_IMAGE_PATH, *path_parts)
    try:
        image = pygame.image.load(path).convert_alpha()
    except pygame.error as e:
        raise SystemExit(f"Cannot load image: {path}\n{e}")
    if size:
        image = pygame.transform.scale(image, size)
    return image

class Stage5Boss:
    def __init__(self):
        # 보스 이미지 로드
        self.boss_image_left = load_image("bosses", "boss_stage5_Left.png", size=(120, 120))
        self.boss_image_right = load_image("bosses", "boss_stage5_Right.png", size=(120, 120))
        self.gem_image = load_image("items", "mob_Jewelry_5.png", size=(50, 50))

        # 속성 초기화
        self.max_boss_hp = 15
        self.boss_hp = self.max_boss_hp
        self.boss_active = False
        self.boss_appeared = False
        self.invincible = False
        self.invincible_duration = 500
        self.last_hit_time = 0

        # 보스 위치 및 상태
        self.direction = "right"  # 처음에는 오른쪽에서 등장
        self.boss_image = self.boss_image_right
        self.boss_pos = [1280 - 120, 720]  # 화면 우측 하단에서 시작
        self.appear_time = 0
        self.state = "entering"  # "entering", "waiting", "exiting", "cooldown"

    def check_appear(self, seconds, current_level):
        if current_level == 5 and not self.boss_active and seconds >= 10 and not self.boss_appeared:
            self.boss_active = True
            self.boss_hp = self.max_boss_hp
            self.boss_appeared = True
            self.state = "entering"
            self.appear_time = pygame.time.get_ticks()

    def move(self):
        current_time = pygame.time.get_ticks()

        if self.state == "entering":
            if self.boss_pos[1] > 360:  # 목표 위치까지 이동
                self.boss_pos[1] -= 2
            else:
                self.state = "waiting"
                self.appear_time = current_time  # 8초 대기 시작

        elif self.state == "waiting":
            if current_time - self.appear_time >= 8000:  # 8초 경과 후 퇴장
                self.state = "exiting"

        elif self.state == "exiting":
            if self.direction == "right":
                self.boss_pos[0] += 5  # 오른쪽으로 이동하여 퇴장
            else:
                self.boss_pos[0] -= 5  # 왼쪽으로 이동하여 퇴장

            if self.boss_pos[0] < -120 or self.boss_pos[0] > 1280:
                self.state = "cooldown"
                self.appear_time = current_time  # 2초 대기 시작

        elif self.state == "cooldown":
            if current_time - self.appear_time >= 2000:  # 2초 대기 후 재등장
                self.state = "entering"
                self.boss_hp = self.max_boss_hp
                self.direction = random.choice(["left", "right"])  # 랜덤 위치에서 등장
                if self.direction == "left":
                    self.boss_pos = [-120, 720]  # 왼쪽에서 등장
                    self.boss_image = self.boss_image_left
                else:
                    self.boss_pos = [1280 - 120, 720]  # 오른쪽에서 등장
                    self.boss_image = self.boss_image_right

    def draw(self, win):
        if self.boss_hp > 0:
            win.blit(self.boss_image, self.boss_pos)

    def check_hit(self, attacks):
        """ 보스가 'waiting' 또는 'exiting' 상태일 때만 데미지를 받음 """
        if self.state not in ["waiting", "exiting"]:
            return  # 보스가 'entering' 상태일 때는 데미지 없음

        current_time = pygame.time.get_ticks()
        if self.invincible and (current_time - self.last_hit_time) < self.invincible_duration:
            return  # 무적 상태일 경우 공격 무시
        
        for attack in attacks:
            attack_start, attack_end, thickness = attack
            if self.check_attack_collision(attack_start, attack_end, self.boss_pos, 120):
                self.boss_hp -= 1
                if self.boss_hp < 0:
                    self.boss_hp = 0
                self.invincible = True
                self.last_hit_time = current_time
                break

    def check_attack_collision(self, attack_start, attack_end, boss_pos, boss_size):
        ex, ey = boss_pos
        sx, sy = attack_start
        ex2, ey2 = ex + boss_size, ey + boss_size

        # 공격 선분과 보스 사각형의 충돌 검사
        rect = pygame.Rect(ex, ey, boss_size, boss_size)
        line = (sx, sy), attack_end
        return rect.clipline(line)

    def reset(self):
        self.boss_active = False
        self.boss_hp = self.max_boss_hp
        self.boss_appeared = False
        self.invincible = False
        self.state = "entering"
        self.appear_time = pygame.time.get_ticks()
        self.direction = "right"
        self.boss_image = self.boss_image_right
        self.boss_pos = [1280 - 120, 720]  # 처음엔 오른쪽에서 등장
