import pygame
import os
import math
import random

# BASE_DIR 설정: 현재 파일의 부모 디렉토리 기준으로 설정
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
        # 이미지 로드
        self.boss_image = load_image("bosses", "boss_stage2.png", size=(120, 120))
        self.boss_attack_images = {
            "down": load_image("boss_skilles", "boss_stage2_a.png", size=(40, 40)),
            "up": load_image("boss_skilles", "boss_stage2_b.png", size=(40, 40)),
            "right": load_image("boss_skilles", "boss_stage2_c.png", size=(40, 40)),
            "left": load_image("boss_skilles", "boss_stage2_d.png", size=(40, 40))
        }
        self.gem_image = load_image("items", "mob_Jewelry_1.png", size=(40, 40))
        # 보스 속성 초기화
        self.boss_appear_time = 20  # 보스 등장 시간 (초)
        self.max_boss_hp = 10  # 보스의 최대 체력
        self.boss_hp = self.max_boss_hp  # 현재 보스 체력
        self.boss_damage = 2  # 보스의 공격력
        self.boss_speed = 5  # 보스의 이동 속도
        self.boss_pos = [640 - 60, 0]  # 보스의 초기 위치
        self.boss_direction_x = 1  # 보스의 좌우 이동 방향
        self.boss_direction_y = 1  # 보스의 상하 이동 방향
        self.boss_active = False  # 보스 활성화 상태
        self.boss_defeated = False  # 보스 패배 상태
        self.boss_appeared = False  # 보스가 이미 등장했는지 여부 추가
        self.boss_move_phase = 1  # 보스의 이동 단계
        self.boss_hit = False  # 보스 피격 상태
        self.boss_hit_start_time = 0  # 보스 피격 시점
        self.boss_hit_duration = 100  # 보스 피격 효과 지속 시간 (밀리초)
        self.boss_attacks = []  # 보스의 공격 리스트
        self.boss_attack_cooldown = 1000  # 보스 공격 간격 (밀리초)
        self.boss_last_attack_time = 0  # 마지막 공격 시점
        self.gem_pos = None  # 보석의 위치
        self.gem_active = False  # 보석 활성화 상태
        self.boss_hit_duration = 100  # 깜박임 효과의 간격(밀리초)
        self.boss_invincible_duration = 500  # 무적 상태 지속 시간(밀리초)

    def check_appear(self, seconds, current_level):
        condition_level = (current_level == 1)
        condition_active = (not self.boss_active)
        condition_time = (seconds >= self.boss_appear_time)
        condition_not_appeared = (not self.boss_appeared)  # 수정된 부분

        if condition_level and condition_active and condition_time and condition_not_appeared:
            self.boss_active = True
            self.boss_pos = [640 - 60, 0]
            self.boss_hp = self.max_boss_hp
            self.boss_appeared = True  # 보스가 등장했음을 표시

    def move(self):
        # 이동 후 위치 제한 함수 추가
        def limit_position():
            self.boss_pos[0] = max(0, min(self.boss_pos[0], 1280 - 120))
            self.boss_pos[1] = max(0, min(self.boss_pos[1], 720 - 120))

        if self.boss_move_phase == 1:
            # 중앙으로 이동
            target_pos = [640 - 60, 360 - 60]
            direction = [target_pos[0] - self.boss_pos[0], target_pos[1] - self.boss_pos[1]]
            length = math.hypot(direction[0], direction[1])
            if length > self.boss_speed:
                direction = [direction[0] / length, direction[1] / length]
                self.boss_pos[0] += direction[0] * self.boss_speed
                self.boss_pos[1] += direction[1] * self.boss_speed
            else:
                self.boss_pos = target_pos
                self.boss_move_phase = 2
        elif self.boss_move_phase == 2:
            # 좌우 이동
            self.boss_pos[0] += self.boss_speed * self.boss_direction_x
            if self.boss_pos[0] <= 0 or self.boss_pos[0] >= 1280 - 120:
                self.boss_direction_x *= -1  # 방향 전환
            if self.boss_hp <= self.max_boss_hp / 2:
                self.boss_move_phase = 3
        elif self.boss_move_phase == 3:
            # 좌우 및 상하 이동
            self.boss_pos[0] += self.boss_speed * self.boss_direction_x
            self.boss_pos[1] += self.boss_speed * self.boss_direction_y
            if self.boss_pos[0] <= 0 or self.boss_pos[0] >= 1280 - 120:
                self.boss_direction_x *= -1  # 좌우 방향 전환
            if self.boss_pos[1] <= 0 or self.boss_pos[1] >= 720 - 120:
                self.boss_direction_y *= -1  # 상하 방향 전환

        # 위치 제한 적용
        limit_position()

    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.boss_last_attack_time > self.boss_attack_cooldown:
            self.boss_last_attack_time = current_time
            possible_directions = []

            # 보스의 체력에 따른 공격 방향 설정
            if self.boss_hp > self.max_boss_hp * 0.75:
                possible_directions = ["down"]
            elif self.boss_hp > self.max_boss_hp * 0.5:
                possible_directions = ["down", "up"]
            elif self.boss_hp > self.max_boss_hp * 0.25:
                possible_directions = ["down", "up", "right"]
            else:
                possible_directions = ["down", "up", "right", "left"]

            attack_direction = random.choice(possible_directions)
            attack_start_pos = self.get_attack_start_pos(attack_direction)
            self.boss_attacks.append([attack_start_pos[0], attack_start_pos[1], attack_direction])

    def get_attack_start_pos(self, direction):
        if direction == "down":
            return [self.boss_pos[0] + 40, self.boss_pos[1] + 120]
        elif direction == "up":
            return [self.boss_pos[0] + 40, self.boss_pos[1]]
        elif direction == "right":
            return [self.boss_pos[0] + 120, self.boss_pos[1] + 40]
        elif direction == "left":
            return [self.boss_pos[0], self.boss_pos[1] + 40]

    def update_attacks(self, player_pos):
        new_boss_attacks = []
        for attack in self.boss_attacks:
            if attack[2] == "down":
                attack[1] += 10
            elif attack[2] == "up":
                attack[1] -= 10
            elif attack[2] == "right":
                attack[0] += 10
            elif attack[2] == "left":
                attack[0] -= 10

            if 0 <= attack[0] <= 1280 and 0 <= attack[1] <= 720:
                if self.check_energy_ball_collision((attack[0], attack[1]), player_pos):
                    return True  # 플레이어에게 맞음
                else:
                    new_boss_attacks.append(attack)
            else:
                pass  # 공격이 화면 밖으로 나가면 제거
        self.boss_attacks = new_boss_attacks
        return False

    def draw(self, win):
        if self.boss_hp > 0:
            current_time = pygame.time.get_ticks()
            if self.boss_hit:
                if current_time - self.boss_hit_start_time >= self.boss_invincible_duration:
                    self.boss_hit = False  # 무적 상태 및 깜박임 종료
                    win.blit(self.boss_image, self.boss_pos)
                else:
                    # 깜박임 효과
                    if (current_time // self.boss_hit_duration) % 2 == 0:
                        win.blit(self.boss_image, self.boss_pos)
            else:
                win.blit(self.boss_image, self.boss_pos)

    def draw_attacks(self, win):
        for attack in self.boss_attacks:
            win.blit(self.boss_attack_images[attack[2]], (attack[0], attack[1]))

    def draw_gem(self, win):
        if self.gem_active:
            win.blit(self.gem_image, self.gem_pos)

    def draw_health_bar(self, win, font):
        if self.boss_active and self.boss_hp > 0:
            # "BOSS" 문자열 그리기
            boss_text = font.render("BOSS", True, (255, 255, 255))
            text_x = 10
            text_y = 680
            win.blit(boss_text, (text_x, text_y))

            # 체력 바 설정
            health_bar_x = text_x + boss_text.get_width() + 10
            health_bar_y = 680
            health_bar_width = 200  # 체력 바의 총 너비를 200으로 설정
            health_bar_height = 30

            # 체력 비율 계산
            health_ratio = self.boss_hp / self.max_boss_hp
            current_health_width = int(health_bar_width * health_ratio)

            # 체력 바 배경 그리기
            pygame.draw.rect(win, (50, 50, 50), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

            # 현재 체력 바 그리기
            pygame.draw.rect(win, (210, 20, 4), (health_bar_x, health_bar_y, current_health_width, health_bar_height))

            # 체력 바 테두리 그리기
            pygame.draw.rect(win, (255, 255, 255), (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)
        elif self.boss_hp <= 0 and self.boss_defeated:
            # 보스가 제거되었을 때 메시지 표시 (옵션)
            defeated_text = font.render("BOSS DEFEATED", True, (255, 255, 255))
            win.blit(defeated_text, (10, 680))

    def check_hit(self, attacks):
        current_time = pygame.time.get_ticks()
        if self.boss_hit and (current_time - self.boss_hit_start_time) < self.boss_invincible_duration:
            # 보스가 무적 상태일 때는 공격을 무시합니다.
            return
        else:
            self.boss_hit = False  # 무적 상태 해제

        for attack in attacks:
            attack_start, attack_end, thickness = attack
            if self.check_attack_collision(attack_start, attack_end, self.boss_pos, 120):
                self.boss_hp -= 1  # 데미지 적용
                if self.boss_hp < 0:
                    self.boss_hp = 0  # 체력이 음수가 되지 않도록
                self.boss_hit = True  # 보스가 공격을 받았음을 표시
                self.boss_hit_start_time = current_time  # 공격 받은 시간 기록
                if self.boss_hp <= 0:
                    self.boss_active = False
                    self.gem_pos = [self.boss_pos[0] + 40, self.boss_pos[1] + 40]
                    self.gem_active = True
                    self.boss_defeated = True
                break  # 한 번에 하나의 공격만 처리

    def check_gem_collision(self, player_pos):
        if self.gem_active:
            px, py = player_pos
            gx, gy = self.gem_pos
            player_width, player_height = 40, 40  # 플레이어 크기
            gem_size = 40  # 보석 크기
            if px < gx + gem_size and px + player_width > gx and py < gy + gem_size and py + player_height > gy:
                self.gem_active = False
                return True
        return False

    def reset(self):
        self.boss_active = False
        self.boss_hp = self.max_boss_hp
        self.boss_pos = [640 - 60, 0]
        #! self.boss_defeated = False  # boss_defeated를 재설정하지 않음
        self.boss_appeared = False  # 보스 등장 여부 재설정
        self.boss_attacks = []
        self.gem_active = False
        self.gem_pos = None
        self.boss_move_phase = 1
        self.boss_hit = False

    def check_energy_ball_collision(self, ball_pos, player_pos):
        bx, by = ball_pos
        px, py = player_pos
        player_width, player_height = 40, 40  # 플레이어 크기
        if px < bx < px + player_width and py < by < py + player_height:
            return True
        return False

    def check_attack_collision(self, attack_start, attack_end, boss_pos, boss_size):
        ex, ey = boss_pos
        sx, sy = attack_start
        ex2, ey2 = ex + boss_size, ey + boss_size

        # 공격 선분과 보스 사각형의 충돌 검사
        rect = pygame.Rect(ex, ey, boss_size, boss_size)
        line = (sx, sy), attack_end
        if rect.clipline(line):
            return True
        return False
