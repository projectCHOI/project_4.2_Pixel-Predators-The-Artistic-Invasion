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
        self.boss_image = load_image("bosses", "boss_stage9_S.png", size=(180, 180))
        self.minion_image = load_image("boss_skilles", "boss_stage9_N.png", size=(60, 60))
        self.attack_image = load_image("boss_skilles", "boss_stage90_b.png", size=(60, 60))
        self.minion_attack_image = {
            "phase1": load_image("boss_skilles", "boss_stage9_a.png", size=(40, 40)),
            "phase2": load_image("boss_skilles", "boss_stage9_b.png", size=(40, 40)),
            "phase3": load_image("boss_skilles", "boss_stage9_c.png", size=(40, 40)),
            "phase4": load_image("boss_skilles", "boss_stage9_d.png", size=(40, 40))
        }
        self.gem_image = load_image("items", "mob_Jewelry_9.png", size=(40, 40))

        self.boss_pos = [600, -100]
        self.boss_speed = 5
        self.max_boss_hp = 100
        self.boss_hp = 100
        self.boss_active = False
        self.boss_defeated = False
        self.boss_appeared = False
        self.stage_cleared = False

        self.boss_move_state = "entering"
        self.enter_target_pos = [600, 160]
        self.patterns = [
            {"start": (600, 160), "end": (200, 300)},
            {"start": (600, 160), "end": (600, 300)},
            {"start": (600, 160), "end": (1000, 300)}
        ]
        # 미니언 리스트 초기화
        self.minions = []
        self.minion_phases = {
            1: {"start": (1300, 180), "stop": (1000, 350), "end": (1300, 520)},
            2: {"start": (1000, 850), "stop": (700, 500), "end": (1300, 850)},
            3: {"start": (125, -150), "stop": (620, 400), "end": (260, 850)},
            4: {"start": (-150, 400), "stop": (300, 540), "end": (520, 850)},
            5: {"start": (-150, 700), "stop": (330, 360), "end": (-150, 140)},
            }
        self.last_minion_spawn_time = pygame.time.get_ticks()

        self.current_pattern = None
        self.pattern_direction = "forward"
        self.pattern_timer = pygame.time.get_ticks()
        self.wave_amplitude = 40
        self.wave_frequency = 0.01

        self.boss_attacks = []
        self.boss_phase = 1
        self.attack_cooldown = 2000
        self.last_attack_time = 0

        self.boss_hit = False
        self.boss_hit_start_time = 0
        self.boss_invincible_duration = 500

        self.input_reversed_until = 0

        self.gem_active = False
        self.gem_pos = None
        self.minions = []

    def move(self):
        current_time = pygame.time.get_ticks()
        if self.boss_move_state == "entering":
            if self.boss_pos[1] < self.enter_target_pos[1]:
                self.boss_pos[1] += self.boss_speed
            else:
                self.boss_pos[1] = self.enter_target_pos[1]
                self.boss_move_state = "choosing"
        elif self.boss_move_state == "choosing":
            self.current_pattern = random.choice(self.patterns)
            self.pattern_direction = "forward"
            self.pattern_timer = current_time
            self.boss_move_state = "patterning"
        elif self.boss_move_state == "patterning":
            start = self.current_pattern["start"]
            end = self.current_pattern["end"]
            if self.pattern_direction == "backward":
                start, end = end, start

            elapsed = (current_time - self.pattern_timer) / 1000
            move_fraction = min(elapsed / 1.5, 1)
            new_x = start[0] + (end[0] - start[0]) * move_fraction
            wave_offset = math.sin(current_time * self.wave_frequency) * self.wave_amplitude
            new_y = start[1] + (end[1] - start[1]) * move_fraction + wave_offset
            self.boss_pos = [new_x, new_y]

            if move_fraction >= 1:
                self.boss_move_state = "waiting"
                self.pattern_timer = current_time
                self.pattern_duration = 3000 if self.pattern_direction == "forward" else 2000
        elif self.boss_move_state == "waiting":
            if current_time - self.pattern_timer >= self.pattern_duration:
                if self.pattern_direction == "forward":
                    self.pattern_direction = "backward"
                    self.boss_move_state = "patterning"
                    self.pattern_timer = current_time
                else:
                    self.boss_move_state = "choosing"

    def attack(self, player_pos):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = current_time
            bx, by = self.boss_pos[0] + 90, self.boss_pos[1] + 90
            px, py = player_pos
            dx, dy = px - bx, py - by
            dist = math.hypot(dx, dy)
            if dist != 0:
                dx, dy = dx / dist, dy / dist
            speed = 8
            self.boss_attacks.append({"pos": [bx, by], "dir": [dx * speed, dy * speed], "angle": math.degrees(math.atan2(dy, dx))})

    def update_attacks(self, player_pos, is_invincible=False):
        new_attacks = []
        player_hit = False
        effect_triggered = False
        current_time = pygame.time.get_ticks()

        for attack in self.boss_attacks:
            attack['pos'][0] += attack['dir'][0]
            attack['pos'][1] += attack['dir'][1]
            bx, by = attack['pos']

            if 0 <= bx <= 1280 and 0 <= by <= 720:
                if not is_invincible and self.check_energy_ball_collision((bx, by), player_pos):
                    player_hit = True
                    effect_triggered = True
                else:
                    new_attacks.append(attack)

        self.boss_attacks = new_attacks

        if effect_triggered:
            self.input_reversed_until = current_time + 5000
            return 1

        return 0

    def draw(self, win):
        if self.boss_hp > 0:
            current_time = pygame.time.get_ticks()
            if self.boss_hit and (current_time - self.boss_hit_start_time < self.boss_invincible_duration):
                if (current_time // 100) % 2 == 0:
                    win.blit(self.boss_image, self.boss_pos)
            else:
                win.blit(self.boss_image, self.boss_pos)

    def draw_attacks(self, win):
        for attack in self.boss_attacks:
            rotated = pygame.transform.rotate(self.attack_image, attack["angle"])
            rect = rotated.get_rect(center=attack["pos"])
            win.blit(rotated, rect)

    def draw_gem(self, win):
        if self.gem_active:
            win.blit(self.gem_image, self.gem_pos)

    def draw_health_bar(self, win, font):
        if self.boss_active and self.boss_hp > 0:
            text = font.render("BOSS", True, (255, 255, 255))
            win.blit(text, (10, 680))
            max_width = 200
            height = 30
            ratio = self.boss_hp / self.max_boss_hp
            pygame.draw.rect(win, (50, 50, 50), (80, 680, max_width, height))
            pygame.draw.rect(win, (210, 20, 4), (80, 680, int(max_width * ratio), height))
            pygame.draw.rect(win, (255, 255, 255), (80, 680, max_width, height), 2)

    # 미니언
    def spawn_minions(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_minion_spawn_time >= 5000:
            self.last_minion_spawn_time = current_time
            phase = random.randint(1, 5)
            p = self.minion_phases[phase]
            direction = self._get_direction(p["start"], p["stop"])
            minion = {
                "phase": phase,
                "pos": list(p["start"]),
                "state": "entering",
                "target_pos": p["stop"],
                "exit_pos": p["end"],
                "speed": 4,
                "direction": direction,
                 "wait_timer": None,
                 "attack_timer": current_time,
                 "shots_fired": 0,               
                 "attacks": []                  
            }
            self.minions.append(minion)

    def update_minion_behavior(self):
        current_time = pygame.time.get_ticks()
        for minion in self.minions[:]:
            pos = minion["pos"]
            speed = minion["speed"]
            phase = minion["phase"]

            if minion["state"] == "entering":
                # 이동 후 정지 상태 진입
                self._move_towards(minion, minion["target_pos"])
                if self._is_arrived(pos, minion["target_pos"]):
                    minion["state"] = "stopping"
                    minion["wait_timer"] = current_time
                    minion["attack_timer"] = current_time  # 공격 시작 시간 초기화
                    minion["shots_fired"] = 0            # 공격 횟수 초기화

            elif minion["state"] == "stopping":
                # 1초 정지 후 공격 시작
                if current_time - minion["wait_timer"] < 1000:
                    continue
                # 3회 공격
                if minion["shots_fired"] < 3:
                    if current_time - minion["attack_timer"] >= 1000:
                        self._minion_attack(minion)
                        minion["attack_timer"] = current_time
                        minion["shots_fired"] += 1
                else:
                    # 마지막 공격 후 1초 대기 후 퇴장
                    if current_time - minion["attack_timer"] >= 1000:
                        minion["state"] = "exiting"
                        minion["direction"] = self._get_direction(pos, minion["exit_pos"])

            elif minion["state"] == "exiting":
                # 퇴장 경로로 이동 후 제거
                self._move_towards(minion, minion["exit_pos"])
                if self._is_arrived(pos, minion["exit_pos"]):
                    self.minions.remove(minion)

    def _spawn_minion_attack(self, minion):
        speed = 6
        x, y = minion['pos']
        ph = minion['phase']
        bullets = []
        if ph == 1:
            for i in range(11):
                angle = 135 + i * (90 / 10)
                rad = math.radians(angle)
                bullets.append({'pos': [x, y], 'dir': [math.cos(rad) * speed, math.sin(rad) * speed]})
        elif ph == 2:
            for i in range(20):
                angle = i * 18
                rad = math.radians(angle)
                bullets.append({'pos': [x, y], 'dir': [math.cos(rad) * speed, math.sin(rad) * speed]})
        elif ph == 3:
            offset = (minion['attacks_done'] * 10) % 360
            for i in range(20):
                angle = offset + i * 18
                rad = math.radians(angle)
                bullets.append({'pos': [x, y], 'dir': [math.cos(rad) * speed, math.sin(rad) * speed]})
        elif ph == 4:
            for i in range(11):
                angle = -45 + i * (90 / 10)
                rad = math.radians(angle)
                bullets.append({'pos': [x, y], 'dir': [math.cos(rad) * speed, math.sin(rad) * speed]})
        elif ph == 5:
            for angle in [-15, 0, 15]:
                rad = math.radians(angle)
                bullets.append({'pos': [x, y], 'dir': [math.cos(rad) * speed, math.sin(rad) * speed]})
        minion['attacks'].extend(bullets)
    
    def _get_direction(self, start, end):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        dist = math.hypot(dx, dy)
        if dist == 0:
            return [0, 0]
        return [dx / dist, dy / dist]
    
    def update_minion_behavior(self):
        current_time = pygame.time.get_ticks()
        for minion in self.minions[:]:
            pos = minion["pos"]
            speed = minion["speed"]
            phase = minion["phase"]

            if minion["state"] == "entering":
                self._move_towards(minion, minion["target_pos"])
                if self._is_arrived(pos, minion["target_pos"]):
                    minion["state"] = "stopping"
                    minion["wait_timer"] = current_time
                    minion["attack_timer"] = current_time

            elif minion["state"] == "stopping":
                if current_time - minion["wait_timer"] >= 1000:
                    if minion["shots_fired"] < 3:
                        if current_time - minion["attack_timer"] >= 1000:
                            self._minion_attack(minion)
                            minion["attack_timer"] = current_time
                            minion["shots_fired"] += 1
                    else:
                        if current_time - minion["attack_timer"] >= 1000:
                            minion["state"] = "exiting"
                            minion["direction"] = self._get_direction(pos, minion["exit_pos"])

            elif minion["state"] == "exiting":
                self._move_towards(minion, minion["exit_pos"])
                if self._is_arrived(pos, minion["exit_pos"]):
                    self.minions.remove(minion)

    def _minion_attack(self, minion):
        phase = minion["phase"]
        cx, cy = minion["pos"]
        if phase == 1:
            angles = [-60 + i * 12 for i in range(11)]
        elif phase == 2:
            angles = [i * 18 for i in range(20)]
        elif phase == 3:
            base = pygame.time.get_ticks() % 360
            angles = [(base + i * 18) % 360 for i in range(20)]
        elif phase == 4:
            angles = [60 - i * 12 for i in range(11)]
        elif phase == 5:
            angles = [-30 + i * 30 for i in range(3)]
        else:
            angles = []

        for angle in angles:
            rad = math.radians(angle)
            dx = math.cos(rad) * 6
            dy = math.sin(rad) * 6
            minion["attacks"].append({"pos": [cx, cy], "dir": [dx, dy]})

    def update_minion_attacks(self):
        for minion in self.minions:
            new_attacks = []
            for atk in minion["attacks"]:
                atk["pos"][0] += atk["dir"][0]
                atk["pos"][1] += atk["dir"][1]
                if 0 <= atk["pos"][0] <= 1280 and 0 <= atk["pos"][1] <= 720:
                    new_attacks.append(atk)
            minion["attacks"] = new_attacks

    def _move_towards(self, minion, target):
        dir = minion["direction"]
        minion["pos"][0] += dir[0] * minion["speed"]
        minion["pos"][1] += dir[1] * minion["speed"]

    def _is_arrived(self, pos, target, tolerance=10):
        return math.hypot(pos[0] - target[0], pos[1] - target[1]) <= tolerance

    def check_minion_collision(self, player_pos):
        player_rect = pygame.Rect(player_pos[0], player_pos[1], 50, 50)
        for minion in self.minions:
            minion_rect = pygame.Rect(minion["pos"][0], minion["pos"][1], 60, 60)
            if player_rect.colliderect(minion_rect):
                return 2  # 데미지 2
        return 0

    def draw_minion_attacks(self, win):
        for minion in self.minions:
            phase_key = f"phase{minion["phase"]}"
            for atk in minion["attacks"]:
                rotated_image = pygame.transform.rotate(self.minion_attack_image[phase_key], 0)
                rect = rotated_image.get_rect(center=atk["pos"])
                win.blit(rotated_image, rect)

    def check_minion_attack_collision(self, player_pos):
        player_rect = pygame.Rect(player_pos[0], player_pos[1], 50, 50)
        for minion in self.minions:
            for atk in minion["attacks"]:
                if player_rect.collidepoint(atk["pos"]):
                    return 1
        return 0
    
    def check_hit(self, attacks):
        current_time = pygame.time.get_ticks()
        if self.boss_hit and (current_time - self.boss_hit_start_time < self.boss_invincible_duration):
            return
        for attack in attacks:
            if self.check_attack_collision(attack[0], attack[1], self.boss_pos, 140):
                self.boss_hp -= 1
                self.boss_hit = True
                self.boss_hit_start_time = current_time
                if self.boss_hp <= 0:
                    self.boss_hp = 0
                    self.boss_active = False
                    self.gem_pos = [self.boss_pos[0] + 90, self.boss_pos[1] + 90]
                    self.gem_active = True
                    self.boss_defeated = True
                break

    def check_gem_collision(self, player_pos):
        if self.gem_active:
            px, py = player_pos
            gx, gy = self.gem_pos
            if px < gx + 40 and px + 50 > gx and py < gy + 40 and py + 50 > gy:
                self.gem_active = False
                self.stage_cleared = True
                return True
        return False

    def is_input_reversed(self):
        return pygame.time.get_ticks() < self.input_reversed_until

    def check_energy_ball_collision(self, ball_pos, player_pos):
        bx, by = ball_pos
        px, py = player_pos
        return px < bx < px + 50 and py < by < py + 50

    def check_attack_collision(self, attack_start, attack_end, boss_pos, boss_size):
        rect = pygame.Rect(boss_pos[0], boss_pos[1], boss_size, boss_size)
        return rect.clipline(attack_start, attack_end)

    def reset(self):
        self.__init__()

    def check_appear(self, seconds, current_level):
        if current_level == 1 and not self.boss_active and seconds >= 10 and not self.boss_appeared:
            self.boss_active = True
            self.boss_appeared = True

    def get_player_speed(self):
        return 10