import pygame
import os
import math
import random

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
        self.boss_image = load_image("bosses", "boss_stage7.png", size=(280, 280))
        self.minion_image = load_image("boss_skilles", "boss_stage7_a.png", size=(60, 60))
        self.boss_attack_image = load_image("boss_skilles", "boss_stage7_b.png", size=(40, 40))
        self.direct_attack_image = load_image("boss_skilles", "boss_stage7_c.png", size=(40, 40))
        self.gem_image = load_image("items", "mob_Jewelry_7.png", size=(40, 40))

        self.boss_appear_time = 10  # 보스 등장 시간 (초)
        self.max_boss_hp = 15  # 보스의 최대 체력
        self.boss_hp = self.max_boss_hp  # 현재 보스 체력
        self.boss_damage = 2  # 보스의 공격력
        self.boss_speed = 4  # 보스의 이동 속도
        self.boss_pos = [1400, 350]  # 보스의 초기 위치
        self.boss_target_pos = [930, 350]  # 이동 목표 위치
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
        self.boss_attack_interval = 5000  # 5초 간격 공격
        self.minions = []
        self.minion_spawn_interval = 3000  # 3초 간격 소환
        self.last_minion_spawn_time = 0

    def check_appear(self, seconds, current_level):
        if current_level == 7 and not self.boss_active and seconds >= self.boss_appear_time and not self.boss_appeared:
            self.boss_active = True
            self.boss_appeared = True
            self.last_minion_spawn_time = pygame.time.get_ticks()

    def move(self):
        if self.boss_active:
            dx = self.boss_target_pos[0] - self.boss_pos[0]
            dy = self.boss_target_pos[1] - self.boss_pos[1]
            dist = math.hypot(dx, dy)
            if dist > self.boss_speed:
                self.boss_pos[0] += self.boss_speed * dx / dist
                self.boss_pos[1] += self.boss_speed * dy / dist
            else:
                self.boss_pos = self.boss_target_pos[:]

    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.boss_last_attack_time >= self.boss_attack_interval:
            self.boss_last_attack_time = current_time
            center_x = self.boss_pos[0] + 140
            center_y = self.boss_pos[1] + 140
            for angle in range(0, 360, 30):
                rad = math.radians(angle)
                dx = math.cos(rad) * 5
                dy = math.sin(rad) * 5
                self.boss_attacks.append({
                    'pos': [center_x, center_y],
                    'dir': [dx, dy],
                    'angle': angle
                })

    def spawn_minions(self):
        if not self.boss_active:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_minion_spawn_time >= self.minion_spawn_interval:
            self.last_minion_spawn_time = current_time

            # 생성 범위
            min_x, max_x = 200, 1000
            min_y, max_y = 100, 600

            for _ in range(3):  # 3마리 미니언 생성
                rand_x = random.randint(min_x, max_x)
                rand_y = random.randint(min_y, max_y)
                self.minions.append({
                    'pos': [rand_x, rand_y],
                    'opacity': 255,
                    'spawn_time': current_time,
                    'hp': 2,
                    'last_attack_time': current_time,
                    'direction': [random.choice([-1, 0, 1]), random.choice([-1, 0, 1])],
                    'attacks': []
                })

    def update_minion_behavior(self):
        current_time = pygame.time.get_ticks()
        for minion in self.minions:
            # 랜덤 이동 (작은 범위 내)
            minion['pos'][0] += random.choice([-1, 0, 1]) * random.randint(0, 20)
            minion['pos'][1] += random.choice([-1, 0, 1]) * random.randint(0, 20)

            # 화면 경계 안에서만 이동
            minion_speed = 3
            minion['pos'][0] = max(0, min(1240, minion['pos'][0]))
            minion['pos'][1] = max(0, min(680, minion['pos'][1]))

            # 공격
            if current_time - minion['last_attack_time'] >= 2000:  # 2초 간격
                minion['last_attack_time'] = current_time
                mx, my = minion['pos']
                minion['attacks'] = []
                minion['attacks'].append({'pos': [mx, my], 'dir': [-5, 0]}) # 왼쪽 직진
                minion['attacks'].append({'pos': [mx, my], 'dir': [-5, -3]}) # 왼쪽 위
                minion['attacks'].append({'pos': [mx, my], 'dir': [-5, 3]}) # 왼쪽 아래

    def update_minion_attacks(self):
        for minion in self.minions:
            new_attacks = []
            for atk in minion['attacks']:
                atk['pos'][0] += atk['dir'][0]
                atk['pos'][1] += atk['dir'][1]
                if 0 <= atk['pos'][0] <= 1280 and 0 <= atk['pos'][1] <= 720:
                    new_attacks.append(atk)
            minion['attacks'] = new_attacks

    def update_attacks(self, player_pos, is_invincible=False):
        new_boss_attacks = []
        player_hit = False
        for attack in self.boss_attacks:
            attack['pos'][0] += attack['dir'][0]
            attack['pos'][1] += attack['dir'][1]
            bx, by = attack['pos']
            if 0 <= bx <= 1280 and 0 <= by <= 720:
                if self.check_energy_ball_collision((bx, by), player_pos):
                    player_hit = True
                else:
                    new_boss_attacks.append(attack)
        self.boss_attacks = new_boss_attacks
        return player_hit

    def draw(self, win):
        win.blit(self.boss_image, self.boss_pos)
        for minion in self.minions:
            temp_image = self.minion_image.copy()
            alpha = max(100, minion['opacity'])
            temp_image.set_alpha(alpha)
            win.blit(temp_image, minion['pos'])

    def draw_attacks(self, win):
        for attack in self.boss_attacks:
            angle = -attack['angle'] + 90
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

    def draw_minion_attacks(self, win):
        for minion in self.minions:
            for atk in minion['attacks']:
                rotated_image = pygame.transform.rotate(self.direct_attack_image, 0)
                rect = rotated_image.get_rect(center=atk['pos'])
                win.blit(rotated_image, rect)

    def check_hit(self, attacks):
        current_time = pygame.time.get_ticks()
        if self.boss_hit and (current_time - self.boss_hit_start_time) < self.boss_invincible_duration:
            return
        else:
            self.boss_hit = False

        for attack in attacks:
            start, end, thickness, color = attack
            if self.check_attack_collision(start, end, self.boss_pos, 240):
                self.boss_hp -= 1
                if self.boss_hp < 0:
                    self.boss_hp = 0
                self.boss_hit = True
                self.boss_hit_start_time = current_time
                if self.boss_hp <= 0:
                    self.boss_active = False
                    self.gem_pos = [self.boss_pos[0] + 100, self.boss_pos[1] + 140]
                    self.gem_active = True
                    self.boss_defeated = True
                break

        for minion in self.minions[:]:
            for attack in attacks:
                start, end, thickness, color = attack
                if self.check_attack_collision(start, end, minion['pos'], 40):
                    minion['hp'] -= 1
                    if minion['hp'] <= 0:
                        self.minions.remove(minion)
                    break

    def check_gem_collision(self, player_pos):
        if self.gem_active:
            px, py = player_pos
            gx, gy = self.gem_pos
            player_width, player_height = 50, 50  # 플레이어 크기
            gem_size = 40  # 보석 크기
            if px < gx + gem_size and px + player_width > gx and py < gy + gem_size and py + player_height > gy:
                self.gem_active = False
                self.stage_cleared = True
                self.boss_attacks.clear()
                for minion in self.minions:
                    minion['attacks'].clear()
                return True


    def reset(self):
        self.__init__()
        self.boss_active = False
        self.boss_hp = self.max_boss_hp
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
        return 10  # 또는 보스 특성에 따라 조정