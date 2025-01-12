import pygame
import os
import math

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

class Stage8Boss:
    def __init__(self):
        # 플레이어 위치를 저장할 속성
        self.player_pos = None
        # 플레이어 위치 업데이트 메서드 추가
        def update_player_position(self, player_pos):
            self.player_pos = player_pos
        # 이미지 로드
        self.boss_image = load_image("bosses", "boss_stage8.png", size=(120, 120))
        self.boss_attack_image = load_image("boss_skilles", "boss_stage8_b.png", size=(40, 40))
        self.shield_drone_image = load_image("boss_skilles", "boss_stage8_a.png", size=(40, 40))
        self.gem_image = load_image("items", "mob_Jewelry_8.png", size=(40, 40))

        # 보스 속성 초기화
        self.boss_appear_time = 10  # 보스 등장 시간 (초)
        self.max_boss_hp = 15  # 보스의 최대 체력
        self.boss_hp = self.max_boss_hp  # 현재 보스 체력
        self.boss_damage = 5  # 보스의 공격력
        self.boss_speed = 1  # 보스의 이동 속도
        self.boss_pos = [640 - 120, 200]  # 보스의 초기 위치
        self.boss_active = False  # 보스 활성화 상태
        self.boss_defeated = False  # 보스 패배 상태
        self.boss_appeared = False  # 보스가 이미 등장했는지 여부
        self.boss_move_phase = 1  # 보스의 이동 단계
        self.boss_hit = False  # 보스 피격 상태
        self.boss_hit_start_time = 0  # 보스 피격 시점
        self.boss_hit_duration = 100  # 보스 피격 효과 지속 시간 (밀리초)
        self.boss_attacks = []  # 보스의 공격 리스트
        self.boss_attack_cooldown = 3000  # 보스 공격 간격 (밀리초)
        self.boss_last_attack_time = 0  # 마지막 공격 시점
        self.gem_pos = None  # 보석의 위치
        self.gem_active = False  # 보석 활성화 상태
        self.stage_cleared = False  # 스테이지 클리어 여부
        self.boss_invincible_duration = 500  # 무적 상태 지속 시간(밀리초)
        self.shields_active = True  # 방어막 활성화 상태
        self.shield_drones = []  # 방어막 드론 리스트

    def check_appear(self, seconds, current_level):
        if current_level == 8 and not self.boss_active and seconds >= self.boss_appear_time and not self.boss_appeared:
            self.boss_active = True
            self.boss_pos = [640 - 120, 200]
            self.boss_hp = self.max_boss_hp
            self.boss_appeared = True  # 보스가 등장했음을 표시

    def move(self):
        current_time = pygame.time.get_ticks()

        # 보스가 천천히 작은 원을 그리며 움직임
        self.boss_pos[0] += math.cos(current_time * 0.001) * self.boss_speed
        self.boss_pos[1] += math.sin(current_time * 0.001) * self.boss_speed

        # 방어막 드론 생성 및 이동
        if self.shields_active:
            self.shield_drones = []
            num_drones = 8
            radius = 100  # 드론이 보스를 중심으로 도는 반경
            for i in range(num_drones):
                angle = (current_time * 0.002 + (i * (2 * math.pi / num_drones))) % (2 * math.pi)
                dx = math.cos(angle) * radius
                dy = math.sin(angle) * radius
                drone_pos = [self.boss_pos[0] + 60 + dx, self.boss_pos[1] + 60 + dy]
                self.shield_drones.append(drone_pos)

    def attack(self):
        # player_pos를 self.player_pos에서 참조하도록 수정
        if self.player_pos is None:
            return  # 플레이어 위치가 없는 경우 공격하지 않음
        
        current_time = pygame.time.get_ticks()
        if current_time - self.boss_last_attack_time > self.boss_attack_cooldown:
            self.boss_last_attack_time = current_time
            attack_speed = 5 + (self.max_boss_hp - self.boss_hp) * 0.3

            # 항상 단일 투사체 발사
            dx = self.player_pos[0] - (self.boss_pos[0] + 60)
            dy = self.player_pos[1] - (self.boss_pos[1] + 60)
            distance = math.sqrt(dx ** 2 + dy ** 2)

            dx /= distance
            dy /= distance

            self.boss_attacks.append({
                'pos': [self.boss_pos[0] + 60, self.boss_pos[1] + 60],
                'dir': [dx * attack_speed, dy * attack_speed],
                'angle': math.degrees(math.atan2(-dy, dx))
            })

            # 체력이 25% 이하일 경우 추가 패턴 발사
            if self.boss_hp <= self.max_boss_hp * 0.65:
                self.shields_active = False
                num_shots = 12
                for i in range(num_shots):
                    angle = i * (360 / num_shots)
                    radian = math.radians(angle)
                    dx = math.cos(radian)
                    dy = math.sin(radian)
                    self.boss_attacks.append({
                        'pos': [self.boss_pos[0] + 60, self.boss_pos[1] + 60],
                        'dir': [dx * attack_speed, dy * attack_speed],
                        'angle': angle
                    })

# 투사체 이동 업데이트
    def update_attacks(self, player_pos):
        new_boss_attacks = []
        player_hit = False
        for attack in self.boss_attacks:
            # 투사체 이동
            attack['pos'][0] += attack['dir'][0]
            attack['pos'][1] += attack['dir'][1]

            # 화면 밖으로 나간 투사체 제거
            bx, by = attack['pos']
            if 0 <= bx <= 1280 and 0 <= by <= 720:
                if self.check_energy_ball_collision((bx, by), player_pos):
                    player_hit = True  # 플레이어가 피격됨
                else:
                    new_boss_attacks.append(attack)
        
        self.boss_attacks = new_boss_attacks
        return player_hit

    def draw(self, win):
        if self.boss_hp > 0:
            win.blit(self.boss_image, self.boss_pos)
            # 방어막 드론 그리기
            if self.shields_active:
                for drone_pos in self.shield_drones:
                    win.blit(self.shield_drone_image, drone_pos)

    def draw_attacks(self, win):
        for attack in self.boss_attacks:
            angle = -attack['angle'] + 90  # 이미지 회전을 위해 각도 조정
            rotated_image = pygame.transform.rotate(self.boss_attack_image, angle)
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
        self.boss_pos = [640 - 120, 200]
        self.boss_defeated = False
        self.boss_appeared = False  # 보스 등장 여부 재설정
        self.boss_attacks = []
        self.gem_active = False
        self.gem_pos = None
        self.boss_move_phase = 1
        self.boss_hit = False
        self.stage_cleared = False
        self.shields_active = True
        self.shield_drones = []

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