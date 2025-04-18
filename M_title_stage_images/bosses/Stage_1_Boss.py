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

    def spawn_minions(self):
        pass

    def update_minion_behavior(self):
        pass

    def update_minion_attacks(self):
        pass

    def draw_minion_attacks(self, win):
        pass
