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

class Stage9Boss:
    def __init__(self):
        self.boss_image = load_image("bosses", "boss_stage9.png", size=(180, 180))
        self.attack_images = {
            "phase1": load_image("boss_skilles", "boss_stage9_a.png", size=(40, 40)),
            "phase2": load_image("boss_skilles", "boss_stage9_b.png", size=(40, 40)),
            "phase3": load_image("boss_skilles", "boss_stage9_c.png", size=(40, 40)),
            "phase4": load_image("boss_skilles", "boss_stage9_d.png", size=(40, 40)),
        }
        self.gem_image = load_image("items", "mob_Jewelry_9.png", size=(40, 40))

        self.max_boss_hp = 100
        self.boss_hp = self.max_boss_hp
        self.boss_pos = [640 - 90, 100]
        self.boss_active = False
        self.boss_attacks = []
        self.attack_cooldown = 1200
        self.last_attack_time = 0
        self.phase = 1
        self.gem_pos = None
        self.gem_active = False
        self.boss_defeated = False
        self.stage_cleared = False
        self.boss_hit = False
        self.boss_hit_start_time = 0
        self.invincible_duration = 500
        self.boss_hit_duration = 100

        self.minions = []
        self.last_minion_spawn_time = 0
        self.minion_spawn_interval = 4000  # 4초마다 소환

    def check_appear(self, seconds, current_level):
        if current_level == 9 and not self.boss_active and seconds >= 10:
            self.boss_active = True

    def update_phase(self):
        if self.boss_hp <= 25:
            self.phase = 4
        elif self.boss_hp <= 50:
            self.phase = 3
        elif self.boss_hp <= 75:
            self.phase = 2
        else:
            self.phase = 1

    def attack(self):
        if not self.boss_active:
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = current_time
            cx, cy = self.boss_pos[0] + 90, self.boss_pos[1] + 90
            if self.phase == 1:
                angles = [random.randint(0, 360) for _ in range(6)]
            elif self.phase == 2:
                angles = [i for i in range(0, 360, 30)]
            elif self.phase == 3:
                angles = [i for i in range(0, 360, 15)]
            else:
                angles = [i + (current_time // 100) % 360 for i in range(0, 360, 10)]
            for angle in angles:
                rad = math.radians(angle)
                dx = math.cos(rad) * 6
                dy = math.sin(rad) * 6
                self.boss_attacks.append({
                    'pos': [cx, cy],
                    'dir': [dx, dy],
                    'angle': angle,
                    'image': self.attack_images[f"phase{self.phase}"]
                })

    def move(self, player_pos=None):
        if not self.boss_active:
            return
        self.move_timer += 1
        if self.phase == 1:
            radius, speed = 100, 0.02
        elif self.phase == 2:
            radius, speed = 150, 0.03
        elif self.phase == 3:
            radius = 100 + 50 * math.sin(self.move_timer * 0.05)
            speed = 0.04
        else:
            if player_pos:
                px, py = player_pos
                radius, speed = 80, 0.05
                self.boss_pos[0] = px + math.cos(self.move_timer * speed) * radius
                self.boss_pos[1] = py + math.sin(self.move_timer * speed) * radius
                return
        center_x, center_y = 640, 360
        self.boss_pos[0] = center_x + math.cos(self.move_timer * speed) * radius
        self.boss_pos[1] = center_y + math.sin(self.move_timer * speed) * radius

    def spawn_minions(self, player_pos):
        if not self.boss_active:
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.last_minion_spawn_time >= self.minion_spawn_interval:
            self.last_minion_spawn_time = current_time
            minion_count = self.phase
            for _ in range(minion_count):
                offset_x = random.randint(-100, 100)
                offset_y = random.randint(-100, 100)
                spawn_x = max(0, min(1240, self.boss_pos[0] + offset_x))
                spawn_y = max(0, min(680, self.boss_pos[1] + offset_y))
                minion_type = random.choice(["A", "B", "C"])
                self.minions.append({
                    'type': minion_type,
                    'pos': [spawn_x, spawn_y],
                    'hp': 2,
                    'last_attack_time': current_time,
                    'angle': 0,
                    'center': [spawn_x, spawn_y],
                    'radius': 50,
                    'attacks': []
                })

    def update_minion_behavior(self, player_pos):
        for minion in self.minions:
            mtype = minion['type']
            if mtype == "A":
                minion['pos'][0] += random.randint(-2, 2)
                minion['pos'][1] += random.randint(-2, 2)
                minion['attacks'] = [{'pos': minion['pos'][:], 'dir': [-4, 0]}]
            elif mtype == "B":
                dx = player_pos[0] - minion['pos'][0]
                dy = player_pos[1] - minion['pos'][1]
                dist = math.hypot(dx, dy)
                if dist:
                    dx /= dist
                    dy /= dist
                    minion['pos'][0] += dx * 2
                    minion['pos'][1] += dy * 2
            elif mtype == "C":
                minion['angle'] += 5
                rad = math.radians(minion['angle'])
                cx, cy = minion['center']
                r = minion['radius']
                minion['pos'][0] = cx + math.cos(rad) * r
                minion['pos'][1] = cy + math.sin(rad) * r
                minion['attacks'] = [
                    {'pos': minion['pos'][:], 'dir': [-5, 0]},
                    {'pos': minion['pos'][:], 'dir': [-5, -3]},
                    {'pos': minion['pos'][:], 'dir': [-5, 3]},
                ]

    def update_minion_attacks(self):
        for minion in self.minions:
            new_attacks = []
            for atk in minion['attacks']:
                atk['pos'][0] += atk['dir'][0]
                atk['pos'][1] += atk['dir'][1]
                if 0 <= atk['pos'][0] <= 1280 and 0 <= atk['pos'][1] <= 720:
                    new_attacks.append(atk)
            minion['attacks'] = new_attacks

    def draw_minion_attacks(self, win):
        for minion in self.minions:
            for atk in minion['attacks']:
                rotated_image = pygame.transform.rotate(self.minion_attack_image, 0)
                rect = rotated_image.get_rect(center=atk['pos'])
                win.blit(rotated_image, rect)

    def update_attacks(self, player_pos, is_invincible=False):
        new_attacks = []
        player_hit = False
        for atk in self.boss_attacks:
            atk['pos'][0] += atk['dir'][0]
            atk['pos'][1] += atk['dir'][1]
            if 0 <= atk['pos'][0] <= 1280 and 0 <= atk['pos'][1] <= 720:
                if self.check_energy_ball_collision(atk['pos'], player_pos):
                    player_hit = True
                else:
                    new_attacks.append(atk)
        self.boss_attacks = new_attacks
        return player_hit

    def draw(self, win):
        current_time = pygame.time.get_ticks()
        if self.boss_hit and (current_time - self.boss_hit_start_time < self.invincible_duration):
            if (current_time // self.boss_hit_duration) % 2 == 0:
                win.blit(self.boss_image, self.boss_pos)
        else:
            win.blit(self.boss_image, self.boss_pos)

    def draw_attacks(self, win):
        for atk in self.boss_attacks:
            angle = -atk['angle'] + 90
            rotated = pygame.transform.rotate(atk['image'], angle)
            rect = rotated.get_rect(center=atk['pos'])
            win.blit(rotated, rect)

    def draw_health_bar(self, win, font):
        if self.boss_active and self.boss_hp > 0:
            boss_text = font.render("BOSS", True, (255, 255, 255))
            win.blit(boss_text, (10, 680))
            bar_x = 10 + boss_text.get_width() + 10
            bar_y = 680
            bar_w = 200
            bar_h = 30
            ratio = self.boss_hp / self.max_boss_hp
            cur_w = int(bar_w * ratio)
            pygame.draw.rect(win, (50, 50, 50), (bar_x, bar_y, bar_w, bar_h))
            pygame.draw.rect(win, (210, 20, 4), (bar_x, bar_y, cur_w, bar_h))
            pygame.draw.rect(win, (255, 255, 255), (bar_x, bar_y, bar_w, bar_h), 2)
        elif self.boss_hp <= 0 and self.boss_defeated:
            text = font.render("BOSS DEFEATED", True, (255, 255, 255))
            win.blit(text, (10, 680))

    def draw_gem(self, win):
        if self.gem_active:
            win.blit(self.gem_image, self.gem_pos)

    def check_hit(self, attacks):
        current_time = pygame.time.get_ticks()
        if self.boss_hit and (current_time - self.boss_hit_start_time < self.invincible_duration):
            return
        for attack in attacks:
            start, end, _, _ = attack
            if self.check_attack_collision(start, end, self.boss_pos, 180):
                self.boss_hp -= 1
                if self.boss_hp <= 0:
                    self.boss_hp = 0
                    self.boss_defeated = True
                    self.boss_active = False
                    self.gem_pos = [self.boss_pos[0] + 70, self.boss_pos[1] + 180]
                    self.gem_active = True
                self.boss_hit = True
                self.boss_hit_start_time = current_time
                break
        self.update_phase()

    def check_gem_collision(self, player_pos):
        if self.gem_active:
            px, py = player_pos
            gx, gy = self.gem_pos
            if px < gx + 40 and px + 50 > gx and py < gy + 40 and py + 50 > gy:
                self.gem_active = False
                self.stage_cleared = True
                return True
        return False

    def check_energy_ball_collision(self, ball_pos, player_pos):
        bx, by = ball_pos
        px, py = player_pos
        return px < bx < px + 50 and py < by < py + 50

    def check_attack_collision(self, attack_start, attack_end, boss_pos, boss_size):
        rect = pygame.Rect(boss_pos[0], boss_pos[1], boss_size, boss_size)
        return rect.clipline((attack_start, attack_end))

    def reset(self):
        self.__init__()
        self.boss_active = False
        self.boss_defeated = False
        self.gem_active = False
        self.boss_attacks = []
        self.stage_cleared = False
