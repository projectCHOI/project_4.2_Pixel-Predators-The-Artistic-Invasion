import pygame
import os
import random
import math

# BASE_DIR 로드: 현재 파일의 부모 디렉토리를 기준으로 설정
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

class Stage4Boss:
    def __init__(self):
        # 이미지 로드 (보스 이미지, 공격 이미지 3개)
        self.boss_image = load_image("bosses", "boss_stage4.png", size=(150, 150))
        self.boss_attack_images = {
            "high": load_image("boss_skilles", "boss_stage4_a.png", size=(30, 30)),
            "medium": load_image("boss_skilles", "boss_stage4_b.png", size=(30, 30)),
            "low": load_image("boss_skilles", "boss_stage4_c.png", size=(30, 30))
        }
        self.gem_image = load_image("items", "mob_Jewelry_4.png", size=(40, 40))

        # 보스 속성 초기화
        self.max_boss_hp = 18
        self.boss_hp = self.max_boss_hp
        self.boss_damage = 2
        self.boss_pos = [640 - 75, 360 - 75]  # 화면 중앙
        self.boss_active = False
        self.boss_attacks = []
        self.boss_last_attack_time = 0
        self.attack_interval = 1200
        self.boss_defeated = False
        self.boss_appeared = False
        self.stage_cleared = False
        self.gem_active = False
        self.gem_pos = None
        self.invincible = False
        self.invincible_duration = 500
        self.last_hit_time = 0
        self.boss_hit = False
        self.boss_hit_start_time = 0
        self.boss_hit_duration = 100
        self.boss_speed = 2
        self.acceleration = 0.1
        self.max_speed = 8
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]

        self.minions = []
    def draw_minion_attacks(self, win):
        pass
    def update_minion_behavior(self):
        pass
    def update_minion_attacks(self):
        pass
    def spawn_minions(self):
        pass

    def check_appear(self, seconds, current_level):
        if current_level == 4 and not self.boss_active and seconds >= 10 and not self.boss_appeared:
            self.boss_active = True
            self.boss_hp = self.max_boss_hp
            self.boss_appeared = True

    def move(self):
        # 보스가 시간에 따라 가속하며 이동
        self.boss_speed = min(self.boss_speed + self.acceleration, self.max_speed)
        self.boss_pos[0] += self.direction[0] * self.boss_speed
        self.boss_pos[1] += self.direction[1] * self.boss_speed

        # 화면 범위에 부딪혔을 때 방향 전환
        if self.boss_pos[0] <= 38 or self.boss_pos[0] >= 1242:
            self.direction[0] = -self.direction[0]  # X축 방향 반전
        if self.boss_pos[1] <= 38 or self.boss_pos[1] >= 682:
            self.direction[1] = -self.direction[1]  # Y축 방향 반전

        # 화면 범위 내로 위치 제한
        self.boss_pos[0] = max(38, min(self.boss_pos[0], 1242))
        self.boss_pos[1] = max(38, min(self.boss_pos[1], 682))

    def update_attacks(self, player_pos, is_invincible=False)::
        new_attacks = []
        for attack in self.boss_attacks:
            attack[0][0] += attack[1][0]
            attack[0][1] += attack[1][1]

            if 0 <= attack[0][0] <= 1280 and 0 <= attack[0][1] <= 720:
                new_attacks.append(attack)
                player_width, player_height = 40, 40
                if (player_pos[0] < attack[0][0] < player_pos[0] + player_width and
                    player_pos[1] < attack[0][1] < player_pos[1] + player_height):
                    return True
        self.boss_attacks = new_attacks
        return False

    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.boss_last_attack_time > self.attack_interval:
            self.boss_last_attack_time = current_time
            num_shots = 4 + (self.max_boss_hp - self.boss_hp) // 4  # 체력 감소 시 공격 횟수 증가
            for i in range(num_shots):
                angle = random.uniform(0, 360)
                radian = math.radians(angle)
                dx = math.cos(radian) * 6
                dy = math.sin(radian) * 6
                attack_type = self.get_attack_type()
                self.boss_attacks.append([self.boss_pos[:], [dx, dy], angle, attack_type])

    def get_attack_type(self):
        health_ratio = self.boss_hp / self.max_boss_hp
        if health_ratio > 0.6:
            return "low"
        elif health_ratio > 0.3:
            return "medium"
        else:
            return "high"

    def draw(self, win):
        if self.boss_hp > 0:
            current_time = pygame.time.get_ticks()
            if self.boss_hit:
                if current_time - self.boss_hit_start_time >= self.invincible_duration:
                    self.boss_hit = False  # 무적 상태 해제
                    win.blit(self.boss_image, self.boss_pos)
                else:
                    # 깜빡임 효과
                    if (current_time // self.boss_hit_duration) % 2 == 0:
                        win.blit(self.boss_image, self.boss_pos)
            else:
                win.blit(self.boss_image, self.boss_pos)

    def draw_attacks(self, win):
        for attack in self.boss_attacks:
            angle = -attack[2] + 90  # 이미지 회전을 위해 각도 조정
            attack_type = attack[3]
            rotated_image = pygame.transform.rotate(self.boss_attack_images[attack_type], angle)
            rect = rotated_image.get_rect(center=attack[0])
            win.blit(rotated_image, rect)

    def draw_gem(self, win):
        if self.gem_active:
            win.blit(self.gem_image, self.gem_pos)

    def draw_health_bar(self, win, font):
        if self.boss_active and self.boss_hp > 0:
            # "BOSS" 문자열 그림
            boss_text = font.render("BOSS", True, (255, 255, 255))
            text_x = 10
            text_y = 680
            win.blit(boss_text, (text_x, text_y))

            # 체력 바 설정
            health_bar_x = text_x + boss_text.get_width() + 10
            health_bar_y = 680
            health_bar_width = 200  # 체력 바의 전체 너비
            health_bar_height = 30

            # 체력 비율 계산
            health_ratio = self.boss_hp / self.max_boss_hp
            current_health_width = int(health_bar_width * health_ratio)

            # 체력 바 배경 그림
            pygame.draw.rect(win, (50, 50, 50), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

            # 현재 체력 바 그림
            pygame.draw.rect(win, (210, 20, 4), (health_bar_x, health_bar_y, current_health_width, health_bar_height))

            # 체력 바 테두리 그림
            pygame.draw.rect(win, (255, 255, 255), (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)
        elif self.boss_hp <= 0 and self.boss_defeated:
            # 보스가 제거되었을 때 메시지 표시 (옵션)
            defeated_text = font.render("BOSS DEFEATED", True, (255, 255, 255))
            win.blit(defeated_text, (10, 680))

    def check_hit(self, attacks):
        current_time = pygame.time.get_ticks()
        if self.boss_hit and (current_time - self.boss_hit_start_time) < self.invincible_duration:
            # 보스가 무적 상태일 때는 공격을 무시합니다.
            return
        else:
            self.boss_hit = False  # 무적 상태 해제

        for attack in attacks:
            attack_start, attack_end, thickness, color = attack
            if self.check_attack_collision(attack_start, attack_end, self.boss_pos, 150):
                self.boss_hp -= 1  # 데미지 적용
                if self.boss_hp < 0:
                    self.boss_hp = 0  # 체력이 음수가 되지 않도록
                self.boss_hit = True  # 보스가 공격받았음을 표시
                self.boss_hit_start_time = current_time  # 공격받은 시간 기록
                if self.boss_hp <= 0:
                    self.boss_active = False
                    self.gem_active = True
                    self.gem_pos = [self.boss_pos[0] + 50, self.boss_pos[1] + 50]
                    self.boss_defeated = True
                break  # 한 번에 하나의 공격만 처리

    def check_gem_collision(self, player_pos):
        if self.gem_active:
            px, py = player_pos
            gx, gy = self.gem_pos
            player_width, player_height = 50, 50  # 플레이어 크기
            gem_size = 40  # 보석 크기
            if px < gx + gem_size and px + player_width > gx and py < gy + gem_size and py + player_height > gy:
                self.gem_active = False
                self.stage_cleared = True  # 스테이지 클리어
                return True
        return False

    def reset(self):
        self.boss_active = False
        self.boss_hp = self.max_boss_hp
        self.boss_pos = [640 - 75, 360 - 75]
        self.boss_defeated = False
        self.boss_appeared = False  # 보스 등장 여부 재설정
        self.boss_attacks = []
        self.boss_hit = False
        self.stage_cleared = False
        self.gem_active = False
        self.gem_pos = None

    def check_attack_collision(self, attack_start, attack_end, boss_pos, boss_size):
        ex, ey = boss_pos
        sx, sy = attack_start
        ex2, ey2 = ex + boss_size, ey + boss_size

        # 공격 선분과 보스 사각형의 충돌 검증
        rect = pygame.Rect(ex, ey, boss_size, boss_size)
        line = (sx, sy), attack_end
        if rect.clipline(line):
            return True
        return False

    def get_player_speed(self):
        return 10