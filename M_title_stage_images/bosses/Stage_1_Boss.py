import pygame
import os
import math
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_IMAGE_PATH = os.path.join(BASE_DIR, "assets", "images")

def load_image(*path_parts, size=None):
    path = os.path.join(BASE_IMAGE_PATH, *path_parts)
    image = pygame.image.load(path).convert_alpha()
    if size:
        image = pygame.transform.scale(image, size)
    return image

class Stage1Boss:
    def __init__(self):
        self.boss_image = load_image("bosses", "boss_stage8.png", size=(120, 120))
        self.boss_attack_image = load_image("boss_skilles", "boss_stage8_a.png", size=(40, 40))
        self.gem_image = load_image("items", "mob_Jewelry_8.png", size=(40, 40))

        self.minion_images = {
            "A": load_image("boss_skilles", "boss_stage8_b1.png", size=(40, 40)),
            "B": load_image("boss_skilles", "boss_stage8_c1.png", size=(40, 40)),
            "C": load_image("boss_skilles", "boss_stage8_d1.png", size=(40, 40)),
        }
        self.minion_attack_images = {
            "A": load_image("boss_skilles", "boss_stage8_b2.png", size=(20, 20)),
            "B": load_image("boss_skilles", "boss_stage8_c2.png", size=(20, 20)),
            "C": load_image("boss_skilles", "boss_stage8_d2.png", size=(20, 20)),
        }

        self.player_pos = [640, 360] # 플레이어 위치 기본값

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

        self.movement_effects = {"B": False, "C": False}  # 이동 변화 상태
        self.original_player_speed = 10  # 기본 속도
        self.player_speed = 10  # 현재 속도

    def check_appear(self, seconds, current_level):
        if current_level == 1 and not self.boss_active and seconds >= self.boss_appear_time and not self.boss_appeared:
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

            min_x, max_x = 200, 1000
            min_y, max_y = 100, 600

            for _ in range(3):
                rand_x = random.randint(min_x, max_x)
                rand_y = random.randint(min_y, max_y)
                minion_type = random.choice(["A", "B", "C"])  # 타입 지정

                self.minions.append({
                    'type': minion_type,
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
            m_type = minion['type']
            mx, my = minion['pos']
            px, py = self.player_pos

            if m_type == "A":
                minion['pos'][0] += random.choice([-1, 0, 1]) * random.randint(0, 20)
                minion['pos'][1] += random.choice([-1, 0, 1]) * random.randint(0, 20)

            elif m_type == "B":
                dx = px - mx
                dy = py - my
                distance = math.hypot(dx, dy)
                if distance != 0:
                    dx /= distance
                    dy /= distance
                    minion['pos'][0] += dx * 1.5
                    minion['pos'][1] += dy * 1.5

            elif m_type == "C":
                if 'angle' not in minion:
                    minion['angle'] = random.randint(0, 360)
                    minion['radius'] = random.randint(30, 80)
                    minion['center'] = minion['pos'][:]
                minion['angle'] += 5
                rad = math.radians(minion['angle'])
                cx, cy = minion['center']
                r = minion['radius']
                minion['pos'][0] = cx + math.cos(rad) * r
                minion['pos'][1] = cy + math.sin(rad) * r

            minion['pos'][0] = max(0, min(1240, minion['pos'][0]))
            minion['pos'][1] = max(0, min(680, minion['pos'][1]))

            if current_time - minion['last_attack_time'] >= 2000:
                minion['last_attack_time'] = current_time
                mx, my = minion['pos']
                minion['attacks'] = []
                minion['attacks'].append({'pos': [mx, my], 'dir': [-5, 0]})
                minion['attacks'].append({'pos': [mx, my], 'dir': [-5, -3]})
                minion['attacks'].append({'pos': [mx, my], 'dir': [-5, 3]})

    def update_minion_attacks(self):
        for minion in self.minions:
            new_attacks = []
            for atk in minion['attacks']:
                atk['pos'][0] += atk['dir'][0]
                atk['pos'][1] += atk['dir'][1]
                if 0 <= atk['pos'][0] <= 1280 and 0 <= atk['pos'][1] <= 720:
                    new_attacks.append(atk)
            minion['attacks'] = new_attacks

    def update_attacks(self, player_pos):
        self.player_pos = player_pos
        new_boss_attacks = []
        player_hit = False
        hit_damage = 0  

        for attack in self.boss_attacks:
            attack['pos'][0] += attack['dir'][0]
            attack['pos'][1] += attack['dir'][1]
            bx, by = attack['pos']
            if 0 <= bx <= 1280 and 0 <= by <= 720:
                if self.check_energy_ball_collision((bx, by), player_pos):
                    player_hit = True
                    hit_damage = max(hit_damage, self.boss_damage)
                else:
                    new_boss_attacks.append(attack)
        self.boss_attacks = new_boss_attacks

        # 미니언 탄환 충돌 처리
        for minion in self.minions:
            for atk in minion['attacks']:
                if self.check_energy_ball_collision(atk['pos'], player_pos):
                    m_type = minion['type']
                    if m_type == "A":
                        self.last_player_hit_type = "A"
                        hit_damage = max(hit_damage, 2)
                    elif m_type == "B":
                        self.movement_effects["B"] = True
                        self.player_speed = 2
                        hit_damage = max(hit_damage, 0)
                    elif m_type == "C":
                        self.movement_effects["C"] = True
                        self.player_speed = 20
                        hit_damage = max(hit_damage, 0)
                    player_hit = True

        return hit_damage if player_hit else 0
    
    def get_player_speed(self):
        return self.player_speed if self.boss_active else self.original_player_speed

    def draw(self, win):
        win.blit(self.boss_image, self.boss_pos)
        for minion in self.minions:
            minion_type = minion['type']
            temp_image = self.minion_images[minion_type].copy()
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
            minion_type = minion['type']
            for atk in minion['attacks']:
                rotated_image = pygame.transform.rotate(self.minion_attack_images[minion_type], 0)
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
                    m_type = minion['type']
                    self.minions.remove(minion)

                    # 효과 해제
                    if m_type == "B":
                        self.movement_effects["B"] = False
                    elif m_type == "C":
                        self.movement_effects["C"] = False

                    # 속도 복구 조건
                    if not self.movement_effects["B"] and not self.movement_effects["C"]:
                        self.player_speed = self.original_player_speed

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
