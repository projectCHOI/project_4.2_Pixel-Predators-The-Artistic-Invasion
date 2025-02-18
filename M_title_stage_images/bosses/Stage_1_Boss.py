import pygame
import os
import random
import math

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

class Stage1Boss:
    def __init__(self):
        # 보스 이미지 로드
        self.boss_image_left = load_image("bosses", "boss_stage5_Left.png", size=(120, 120))
        self.boss_image_right = load_image("bosses", "boss_stage5_Right.png", size=(120, 120))
        self.boss_attack_image = load_image("boss_skilles", "boss_stage5_a.png", size=(40, 40))
        self.gem_image = load_image("items", "mob_Jewelry_5.png", size=(40, 40))

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
        self.boss_pos = [1280 - 120, 340]  # 화면 우측 하단에서 시작
        self.appear_time = 0
        self.state = "entering"  # "entering", "waiting", "exiting", "cooldown"

        # 보석 관련 속성
        self.gem_pos = None
        self.gem_active = False
        self.stage_cleared = False

        # 공격 관련 속성 추가
        self.boss_attacks = []  # 보스의 공격 리스트
        self.boss_attack_cooldown = 1000  # 보스 공격 간격 (밀리초)
        self.boss_last_attack_time = 0  # 마지막 공격 시점

    def check_appear(self, seconds, current_level):
        if current_level == 1 and not self.boss_active and seconds >= 10 and not self.boss_appeared:
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
                self.gem_active = False  # 보석 비활성화
                self.gem_pos = None  # 보석 위치 초기화
                self.stage_cleared = False  # 스테이지 클리어 상태 초기화
                self.direction = random.choice(["left", "right"])  # 랜덤 위치에서 등장
                if self.direction == "left":
                    self.boss_pos = [-120, 720]  # 왼쪽에서 등장
                    self.boss_image = self.boss_image_left
                else:
                    self.boss_pos = [1280 - 120, 720]  # 오른쪽에서 등장
                    self.boss_image = self.boss_image_right

    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.boss_last_attack_time > self.boss_attack_cooldown:
            self.boss_last_attack_time = current_time
            attack_angles = [90]  # 기본 아래로 발사

            if self.boss_hp <= self.max_boss_hp * 0.5:
                attack_angles.extend([80, 100])  # 좌우 추가

            attack_start_pos = [self.boss_pos[0] + 60, self.boss_pos[1] + 120]  # 보스 중앙에서 공격

            for angle in attack_angles:
                radian = math.radians(angle)
                dx = math.cos(radian) * 5
                dy = math.sin(radian) * 5
                self.boss_attacks.append({
                    'pos': [attack_start_pos[0], attack_start_pos[1]],
                    'dir': [dx, dy],
                    'angle': angle
                })

    def update_attacks(self, player_pos):
        new_attacks = []
        for attack in self.boss_attacks:
            attack['pos'][0] += attack['dir'][0]
            attack['pos'][1] += attack['dir'][1]

            if 0 <= attack['pos'][0] <= 1280 and 0 <= attack['pos'][1] <= 720:
                new_attacks.append(attack)

        self.boss_attacks = new_attacks

    def draw_attacks(self, win):
        for attack in self.boss_attacks:
            rotated_image = pygame.transform.rotate(self.boss_attack_image, -attack['angle'] + 90)
            rect = rotated_image.get_rect(center=attack['pos'])
            win.blit(rotated_image, rect)

    def draw(self, win):
        if self.boss_hp > 0:
            win.blit(self.boss_image, self.boss_pos)
        elif self.gem_active:
            win.blit(self.gem_image, self.gem_pos)

    def check_hit(self, attacks):
        if self.state not in ["waiting", "exiting"]:
            return  # 보스가 'entering' 상태일 때는 데미지 없음

        current_time = pygame.time.get_ticks()
        if self.invincible and (current_time - self.last_hit_time) < self.invincible_duration:
            return  # 무적 상태일 경우 공격 무시
        
        for attack in attacks:
            attack_start, attack_end, thickness = attack
            if self.check_attack_collision(attack_start, attack_end, self.boss_pos, 120):
                self.boss_hp -= 1
                if self.boss_hp <= 0:
                    self.boss_hp = 0
                    self.gem_active = True  # 보스가 죽으면 보석 활성화
                    self.gem_pos = [self.boss_pos[0] + 100, self.boss_pos[1] + 100]  # 보석 위치 설정
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
    
    def draw_health_bar(self, win, font):
        if self.boss_active and self.boss_hp > 0:
            # "BOSS" 텍스트 표시
            boss_text = font.render("BOSS", True, (255, 255, 255))
            text_x = 10
            text_y = 680
            win.blit(boss_text, (text_x, text_y))

            # 체력 바 위치 및 크기 설정
            health_bar_x = text_x + boss_text.get_width() + 10
            health_bar_y = 680
            health_bar_width = 200  # 체력 바 너비
            health_bar_height = 30  # 체력 바 높이

            # 체력 비율 계산
            health_ratio = self.boss_hp / self.max_boss_hp
            current_health_width = int(health_bar_width * health_ratio)

            # 체력 바 배경
            pygame.draw.rect(win, (50, 50, 50), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

            # 현재 체력 바
            pygame.draw.rect(win, (210, 20, 4), (health_bar_x, health_bar_y, current_health_width, health_bar_height))

            # 체력 바 테두리
            pygame.draw.rect(win, (255, 255, 255), (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)

    def check_gem_collision(self, player_pos):
        if self.gem_active:
            px, py = player_pos
            gx, gy = self.gem_pos
            player_width, player_height = 40, 40  # 플레이어 크기
            gem_size = 40  # 보석 크기
            if px < gx + gem_size and px + player_width > gx and py < gy + gem_size and py + player_height > gy:
                self.gem_active = False
                self.stage_cleared = True  # 스테이지 클리어
                return True
        return False
    
    def check_energy_ball_collision(self, ball_pos, player_pos):
        bx, by = ball_pos
        px, py = player_pos
        player_width, player_height = 40, 40  # 플레이어 크기
        if px < bx < px + player_width and py < by < py + player_height:
            return True
        return False
    
    def reset(self):
        self.boss_active = False
        self.boss_hp = self.max_boss_hp
        self.boss_appeared = False
        self.gem_active = False
        self.gem_pos = None
        self.stage_cleared = False
        self.state = "entering"
        self.appear_time = pygame.time.get_ticks()
        self.direction = "right"
        self.boss_image = self.boss_image_right
        self.boss_pos = [1280 - 120, 340]
        self.boss_attacks = []