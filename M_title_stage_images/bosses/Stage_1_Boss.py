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

class Stage7Boss:
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
        
        self.max_boss_hp = 15
        self.boss_hp = self.max_boss_hp
        self.boss_damage = 2
        self.boss_defeated = False
        self.boss_active = False
        self.boss_appeared = False
        self.stage_cleared = False

        self.boss_pos = [640, 360]  # 사인 이동의 중심
        self.wave_amplitude_x = 100  # x축 이동 폭
        self.wave_amplitude_y = 50   # y축 이동 폭
        self.wave_speed_x = 0.02     # x축 사인 주기
        self.wave_speed_y = 0.04     # y축 사인 주기
        self.move_timer = 0          # 사인 이동에 쓰일 시간(프레임 or tick)

        self.boss_attacks = []
        self.boss_last_attack_time = 0
        self.attack_interval = 1000  # ms 간격
        self.invincible = False
        self.invincible_duration = 500
        self.boss_hit = False
        self.boss_hit_start_time = 0
        self.boss_hit_duration = 100
        self.gravity_cores = []
        self.core_spawn_interval = 6000  # 6초마다 중력 코어 생성
        self.last_core_spawn_time = 0

        self.teleport_interval = 3000
        self.last_teleport_time = 0
        self.gem_pos = None
        self.gem_active = False
        self.minions = []

    def check_appear(self, seconds, current_level):
        if current_level == 8 and not self.boss_active and seconds >= 10 and not self.boss_appeared:
            self.boss_active = True
            self.boss_hp = self.max_boss_hp
            self.boss_appeared = True

    def move(self):
        if not self.boss_active or self.boss_defeated:
            return
        
        self.move_timer += 1  # 1 tick(프레임)마다 증가 (게임에 맞춰 조정)
        center_x, center_y = 640, 360  # 중심(고정)

        new_x = center_x + math.sin(self.move_timer * self.wave_speed_x) * self.wave_amplitude_x
        new_y = center_y + math.sin(self.move_timer * self.wave_speed_y) * self.wave_amplitude_y
        self.boss_pos = [new_x, new_y]

        current_time = pygame.time.get_ticks()
        if current_time - self.last_teleport_time > self.teleport_interval:
            self.boss_pos = [
                random.randint(100, 1180),
                random.randint(100, 620)
            ]
            self.last_teleport_time = current_time
            self.attack()  # 텔레포트 후 즉시 공격

        self.update_gravity_cores()

    def update_gravity_cores(self):
        self.gravity_cores = [core for core in self.gravity_cores if core.is_active()]

        current_time = pygame.time.get_ticks()
        if current_time - self.last_core_spawn_time >= self.core_spawn_interval:
            self.last_core_spawn_time = current_time
            new_core_pos = [random.randint(100, 1180), random.randint(100, 620)]
            self.gravity_cores.append(self.GravityCore(new_core_pos, duration=5000, radius=150))

    def apply_gravity(self, player_pos):
        total_force = [0, 0]
        gravity_factor = 2.0  # 중력 강도
        for core in self.gravity_cores:
            if core.is_active():
                dx = core.pos[0] - player_pos[0]
                dy = core.pos[1] - player_pos[1]
                dist = math.hypot(dx, dy)
                if dist < core.radius and dist > 0:
                    # 거리 짧을수록 더 강하게 끌어당김
                    magnitude = gravity_factor * (core.radius - dist) / core.radius
                    total_force[0] += (dx / dist) * magnitude
                    total_force[1] += (dy / dist) * magnitude
        return total_force


    def attack(self):
        if not self.boss_active or self.boss_defeated:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.boss_last_attack_time > self.attack_interval:
            self.boss_last_attack_time = current_time

            health_ratio = self.boss_hp / self.max_boss_hp
            if health_ratio > 0.6:
                bullet_speed = 4
                bullet_count = 4
            elif health_ratio > 0.3:
                bullet_speed = 5
                bullet_count = 8
            else:
                bullet_speed = 6
                bullet_count = 12

            center_x = self.boss_pos[0]
            center_y = self.boss_pos[1]

            angle_step = 360 / bullet_count
            for i in range(bullet_count):
                angle = i * angle_step
                rad = math.radians(angle)
                dx = math.cos(rad) * bullet_speed
                dy = math.sin(rad) * bullet_speed

                attack_type = self.get_attack_type()  # high/medium/low
                self.boss_attacks.append({
                    'pos': [center_x, center_y],
                    'dir': [dx, dy],
                    'angle': angle,
                    'type': attack_type,
                    'time': 0
                })

    def get_attack_type(self):
        health_ratio = self.boss_hp / self.max_boss_hp
        if health_ratio > 0.6:
            return "high"
        elif health_ratio > 0.3:
            return "medium"
        else:
            return "low"

    def update_attacks(self, player_pos):
        new_attacks = []
        player_hit = False
        for attack in self.boss_attacks:
            attack['time'] += 1
            t = attack['time'] / 10.0

            # 기본 이동
            attack['pos'][0] += attack['dir'][0]
            attack['pos'][1] += attack['dir'][1]

            # 곡선 효과 (x축 기준 2픽셀 정도 흔들기)
            attack['pos'][0] += math.sin(t) * 2

            bx, by = attack['pos']
            if 0 <= bx <= 1280 and 0 <= by <= 720:
                if self.check_energy_ball_collision((bx, by), player_pos):
                    player_hit = True
                else:
                    new_attacks.append(attack)

        self.boss_attacks = new_attacks
        return player_hit

    def draw(self, win):
        if self.boss_hp > 0:
            current_time = pygame.time.get_ticks()
            if self.boss_hit:
                if current_time - self.boss_hit_start_time >= self.invincible_duration:
                    self.boss_hit = False
                    win.blit(self.boss_image, (self.boss_pos[0] - 60, self.boss_pos[1] - 60))
                else:
                    if (current_time // self.boss_hit_duration) % 2 == 0:
                        win.blit(self.boss_image, (self.boss_pos[0] - 60, self.boss_pos[1] - 60))
            else:
                win.blit(self.boss_image, (self.boss_pos[0] - 60, self.boss_pos[1] - 60))

        for core in self.gravity_cores:
            core.draw(win)

    def draw_attacks(self, win):
        for attack in self.boss_attacks:
            angle = -attack['angle'] + 90
            attack_type = attack['type']
            rotated_image = pygame.transform.rotate(self.boss_attack_images[attack_type], angle)
            rect = rotated_image.get_rect(center=attack['pos'])
            win.blit(rotated_image, rect)

    def draw_gem(self, win):
        if self.gem_active:
            win.blit(self.gem_image, self.gem_pos)

    def draw_health_bar(self, win, font):
        if self.boss_active and self.boss_hp > 0:
            boss_text = font.render("BOSS", True, (255, 255, 255))
            text_x = 10
            text_y = 680
            win.blit(boss_text, (text_x, text_y))
            health_bar_x = text_x + boss_text.get_width() + 10
            health_bar_y = 680
            health_bar_width = 200
            health_bar_height = 30

            health_ratio = self.boss_hp / self.max_boss_hp
            current_health_width = int(health_bar_width * health_ratio)

            pygame.draw.rect(win, (50, 50, 50),
                             (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
            pygame.draw.rect(win, (210, 20, 4),
                             (health_bar_x, health_bar_y, current_health_width, health_bar_height))
            pygame.draw.rect(win, (255, 255, 255),
                             (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)
        elif self.boss_hp <= 0 and self.boss_defeated:
            defeated_text = font.render("BOSS DEFEATED", True, (255, 255, 255))
            win.blit(defeated_text, (10, 680))

    def check_hit(self, attacks):
        if not self.boss_active or self.boss_defeated:
            return
        current_time = pygame.time.get_ticks()
        if self.boss_hit and (current_time - self.boss_hit_start_time) < self.invincible_duration:
            return

        self.boss_hit = False
        boss_size = 120

        for attack in attacks:
            start, end, thickness, color = attack
            if self.check_attack_collision(start, end, (self.boss_pos[0] - 60, self.boss_pos[1] - 60), boss_size):
                self.boss_hp -= 1
                if self.boss_hp < 0:
                    self.boss_hp = 0

                self.boss_hit = True
                self.boss_hit_start_time = current_time

                if self.boss_hp <= 0:
                    self.boss_active = False
                    self.boss_defeated = True
                    # 보석 생성
                    self.gem_pos = [self.boss_pos[0], self.boss_pos[1] + 40]
                    self.gem_active = True
                break

    def check_gem_collision(self, player_pos):
        if self.gem_active:
            px, py = player_pos
            gx, gy = self.gem_pos
            player_width, player_height = 50, 50
            gem_size = 40
            if px < gx + gem_size and px + player_width > gx and py < gy + gem_size and py + player_height > gy:
                self.gem_active = False
                self.stage_cleared = True
                return True
        return False

    def check_energy_ball_collision(self, ball_pos, player_pos):
        bx, by = ball_pos
        px, py = player_pos
        player_width, player_height = 50, 50
        return (px < bx < px + player_width) and (py < by < py + player_height)

    def check_attack_collision(self, attack_start, attack_end, boss_pos, boss_size):
        ex, ey = boss_pos
        rect = pygame.Rect(ex, ey, boss_size, boss_size)
        line = (attack_start, attack_end)
        return rect.clipline(line)

    def reset(self):
        self.boss_active = False
        self.boss_hp = self.max_boss_hp
        self.boss_pos = [640, 360]
        self.boss_defeated = False
        self.boss_appeared = False
        self.boss_attacks = []
        self.gem_active = False
        self.gem_pos = None
        self.boss_hit = False
        self.stage_cleared = False
        self.gravity_cores.clear()
        self.move_timer = 0
        self.last_teleport_time = 0
        self.last_core_spawn_time = 0
        self.boss_last_attack_time = 0
