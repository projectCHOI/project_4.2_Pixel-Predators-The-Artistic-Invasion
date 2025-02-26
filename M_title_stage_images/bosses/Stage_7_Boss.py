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

class Stage7Boss:
    def __init__(self):
        self.boss_image = load_image("bosses", "boss_stage7.png", size=(120, 120))
        self.boss_attack_image1 = load_image("boss_skilles", "boss_stage7_a.png", size=(40, 40))
        self.boss_attack_image2 = load_image("boss_skilles", "boss_stage7_b.png", size=(40, 40))
        self.gem_image = load_image("items", "mob_Jewelry_7.png", size=(40, 40))

        # 보스 속성 초기화
        self.boss_appear_time = 10  # 보스 등장 시간 (초)
        self.max_boss_hp = 10  # 보스의 최대 체력
        self.boss_hp = self.max_boss_hp  # 현재 보스 체력
        self.boss_damage = 2  # 보스의 공격력
        self.boss_speed = 5  # 보스의 이동 속도
        self.boss_pos = [640 - 120, 0]  # 보스의 초기 위치 (화면 상단 중앙)
        self.boss_direction_x = 1  # 보스의 좌우 이동 방향
        self.boss_active = False  # 보스 활성화 상태
        self.boss_defeated = False  # 보스 패배 상태
        self.boss_appeared = False  # 보스가 이미 등장했는지 여부
        self.boss_move_phase = 1  # 보스의 이동 단계
        self.boss_hit = False  # 보스 피격 상태
        self.boss_hit_start_time = 0  # 보스 피격 시점
        self.boss_hit_duration = 100  # 보스 피격 효과 지속 시간 (밀리초)
        self.boss_attacks = []  # 보스의 공격 리스트
        self.boss_attack_cooldown = 1000  # 보스 공격 간격 (밀리초)
        self.boss_last_attack_time = 0  # 마지막 공격 시점
        self.gem_pos = None  # 보석의 위치
        self.gem_active = False  # 보석 활성화 상태
        self.stage_cleared = False  # 스테이지 클리어 여부
        self.boss_invincible_duration = 500  # 무적 상태 지속 시간(밀리초)

    def check_appear(self, seconds, current_level):
        if current_level == 7 and not self.boss_active and seconds >= self.boss_appear_time and not self.boss_appeared:
            self.boss_active = True
            self.boss_pos = [640 - 120, 0]
            self.boss_hp = self.max_boss_hp
            self.boss_appeared = True  # 보스가 등장했음을 표시

    def move(self):
        current_time = pygame.time.get_ticks()
        if not hasattr(self, 'move_start_time'):
            self.move_start_time = current_time
        elapsed_time = (current_time - self.move_start_time) / 1000  # 초 단위

        # 8자(lemniscate) 곡선으로 움직임
        a = 150  # 8자 곡선의 크기 조절 변수
        b = 75
        x = a * math.sin(elapsed_time)
        y = b * math.sin(2 * elapsed_time) / 2

        self.boss_pos[0] = 640 + x  # 중앙 기준 X 이동
        self.boss_pos[1] = 300 + y  # 중앙 기준 Y 이동

        # 경계 제한 설정
        self.boss_pos[0] = max(38, min(self.boss_pos[0], 1242))
        self.boss_pos[1] = max(38, min(self.boss_pos[1], 682))

    def attack(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.boss_last_attack_time > self.boss_attack_cooldown:
            self.boss_last_attack_time = current_time
            # 보스의 체력에 따라 웨이브 크기 설정
            if self.boss_hp > self.max_boss_hp * 0.75:
                wave_size = 5  # 체력 > 75%
            elif self.boss_hp > self.max_boss_hp * 0.5:
                wave_size = 10  # 체력 > 50%
            elif self.boss_hp > self.max_boss_hp * 0.25:
                wave_size = 15  # 체력 > 25%
            else:
                wave_size = 20  # 체력 <= 25%

            # 공격 시작 위치: 보스 중앙
            attack_start_pos = [
                self.boss_pos[0] + self.boss_image.get_width() // 2,
                self.boss_pos[1] + self.boss_image.get_height() // 2
            ]

            # 웨이브 패턴으로 에너지 볼 생성
            for i in range(wave_size):
                angle = i * (360 / wave_size)  # 웨이브 형태의 각도 계산
                radian = math.radians(angle)
                dx = math.cos(radian) * 3  # 속도 조절
                dy = math.sin(radian) * 3
                attack_image = self.boss_attack_image1 if dx < 0 else self.boss_attack_image2
                self.boss_attacks.append({
                    'pos': [attack_start_pos[0], attack_start_pos[1]],
                    'dir': [dx, dy],
                    'angle': angle,
                    'image': attack_image
                })

    def update_attacks(self, player_pos):
        new_boss_attacks = []
        player_hit = False
        for attack in self.boss_attacks:
            # 에너지 볼 이동
            attack['pos'][0] += attack['dir'][0]
            attack['pos'][1] += attack['dir'][1]

            bx, by = attack['pos']
            if 0 <= bx <= 1280 and 0 <= by <= 720:
                if self.check_energy_ball_collision((bx, by), player_pos):
                    player_hit = True  # 플레이어에게 맞음
                else:
                    new_boss_attacks.append(attack)
            # 화면 밖으로 나가면 공격 제거
        self.boss_attacks = new_boss_attacks
        return player_hit

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
            angle = -attack['angle'] + 90  # 이미지 회전을 위해 각도 조정
            rotated_image = pygame.transform.rotate(attack['image'], angle)
            rect = rotated_image.get_rect(center=attack['pos'])
            win.blit(rotated_image, rect)

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
                    self.gem_pos = [self.boss_pos[0] + 100, self.boss_pos[1] + 100]
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
                self.stage_cleared = True  # 스테이지 클리어
                return True
        return False

    def reset(self):
        self.boss_active = False
        self.boss_hp = self.max_boss_hp
        self.boss_pos = [640 - 120, 0]
        self.boss_defeated = False
        self.boss_appeared = False  # 보스 등장 여부 재설정
        self.boss_attacks = []
        self.gem_active = False
        self.gem_pos = None
        self.boss_move_phase = 1
        self.boss_hit = False
        self.stage_cleared = False

    def check_energy_ball_collision(self, ball_pos, player_pos):
        bx, by = ball_pos
        px, py = player_pos
        player_width, player_height = 50, 50  # 플레이어 크기
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