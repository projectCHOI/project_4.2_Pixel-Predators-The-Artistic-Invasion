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

class Stage1Boss:
    def __init__(self):
        # 이미지 로드
        self.boss_image = load_image("bosses", "boss_stage1.png", size=(140, 140))
        self.boss_attack_image = load_image("boss_skilles", "boss_stage1_a.png", size=(40, 40))
        self.gem_image = load_image("items", "mob_Jewelry_1.png", size=(40, 40))

        # 보스 속성 초기화
        self.boss_appear_time = 10  # 보스 등장 시간 (초)
        self.max_boss_hp = 15  # 보스의 최대 체력
        self.boss_hp = self.max_boss_hp  # 현재 보스 체력
        self.boss_damage = 2  # 보스의 공격력
        self.boss_speed = 6  # 보스의 이동 속도
        self.boss_pos = [640 - 60, 0]  # 보스의 초기 위치
        self.boss_direction_x = 1  # 보스의 좌우 이동 방향
        self.boss_direction_y = 1  # 보스의 상하 이동 방향
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

        self.minions = []

    def spawn_minions(self):
        pass

    def update_minion_behavior(self):
        pass

    def update_minion_attacks(self):
        pass

    def draw_minion_attacks(self, win):
        pass    
    
    def check_appear(self, seconds, current_level):
        if current_level == 1 and not self.boss_active and seconds >= self.boss_appear_time and not self.boss_appeared:
            self.boss_active = True
            self.boss_pos = [640 - 60, 0]  # (640, 0)에서 등장
            self.boss_hp = self.max_boss_hp
            self.boss_move_phase = 2
            self.boss_appeared = True

    def move(self):
        def limit_position():
            self.boss_pos[0] = max(0, min(self.boss_pos[0], 1280 - 140))  # 보스1의 x, y 좌표 제한
            self.boss_pos[1] = max(0, min(self.boss_pos[1], 720 - 540))

        if self.boss_move_phase == 2:
            # 좌우 이동
            self.boss_pos[0] += self.boss_speed * self.boss_direction_x
            if self.boss_pos[0] <= 0 or self.boss_pos[0] >= 1280 - 140:
                self.boss_direction_x *= -1

            # 체력 조건 충족 시 상하 이동 활성화
            if self.boss_hp <= self.max_boss_hp * 0.5:
                self.boss_move_phase = 3

        elif self.boss_move_phase == 3:
            # 좌우 및 상하 이동
            self.boss_pos[0] += self.boss_speed * self.boss_direction_x
            self.boss_pos[1] += self.boss_speed * self.boss_direction_y
            if self.boss_pos[0] <= 0 or self.boss_pos[0] >= 1280 - 140:
                self.boss_direction_x *= -1
            if self.boss_pos[1] <= 0 or self.boss_pos[1] >= 720 - 540:
                self.boss_direction_y *= -1

        limit_position()

    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.boss_last_attack_time > self.boss_attack_cooldown:
            self.boss_last_attack_time = current_time
            attack_angles = []

            # 보스의 체력에 따른 공격 각도 설정
            if self.boss_hp > self.max_boss_hp * 0.75:
                # 체력 > 75%: 아래쪽으로만 공격 (에너지 볼 1개)
                attack_angles = [90]
            elif self.boss_hp > self.max_boss_hp * 0.5:
                # 체력 > 50%: 아래쪽 + 좌우 5도 공격 (에너지 볼 3개)
                attack_angles = [85, 90, 95]
            elif self.boss_hp > self.max_boss_hp * 0.25:
                # 체력 > 25%: 아래쪽 + 좌우 5도, 10도 공격 (에너지 볼 5개)
                attack_angles = [80, 85, 90, 95, 100]
            else:
                # 그 이하: 기존 공격 + 좌우 15도 공격 추가 (에너지 볼 7개)
                attack_angles = [75, 80, 85, 90, 95, 100, 105]

            attack_start_pos = [self.boss_pos[0] + 120, self.boss_pos[1] + 240]  # 보스 아래 중앙 위치

            # 각도에 따른 에너지 볼 생성
            for angle in attack_angles:
                radian = math.radians(angle)
                dx = math.cos(radian) * 10  # 속도 조절
                dy = math.sin(radian) * 10
                self.boss_attacks.append({
                    'pos': [attack_start_pos[0], attack_start_pos[1]],
                    'dir': [dx, dy],
                    'angle': angle
                })

    def update_attacks(self, player_pos, is_invincible=False):
        new_boss_attacks = []
        player_hit = False

        if is_invincible:
            for attack in self.boss_attacks:
                attack['pos'][0] += attack['dir'][0]
                attack['pos'][1] += attack['dir'][1]
                bx, by = attack['pos']
                if 0 <= bx <= 1280 and 0 <= by <= 720:
                    new_boss_attacks.append(attack)
            self.boss_attacks = new_boss_attacks
            return 0  # 데미지 없음

        for attack in self.boss_attacks:
            attack['pos'][0] += attack['dir'][0]
            attack['pos'][1] += attack['dir'][1]
            bx, by = attack['pos']
            if 0 <= bx <= 1280 and 0 <= by <= 720:
                if self.check_energy_ball_collision((bx, by), player_pos):
                    player_hit = True  # 플레이어 피격
                else:
                    new_boss_attacks.append(attack)

        self.boss_attacks = new_boss_attacks
        return self.boss_damage if player_hit else 0

    def draw(self, win):
        if self.boss_hp > 0:
            current_time = pygame.time.get_ticks()
            if self.boss_hit:
                if current_time - self.boss_hit_start_time >= self.boss_invincible_duration:
                    self.boss_hit = False
                    win.blit(self.boss_image, self.boss_pos)
                else:
                    if (current_time // self.boss_hit_duration) % 2 == 0:
                        win.blit(self.boss_image, self.boss_pos)
            else:
                win.blit(self.boss_image, self.boss_pos)

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
            attack_start, attack_end, thickness, color = attack
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
        self.boss_pos = [640 - 60, 0]
        self.boss_defeated = False
        self.boss_appeared = False
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

    def draw_minions(self, win):
        pass
    
    def check_minion_collision(self, player_pos):
        return 0

    def get_player_speed(self):
        return 10