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
        self.attack_images = {
            "phase1": load_image("boss_skilles", "boss_stage9_a.png", size=(40, 40)),
            "phase2": load_image("boss_skilles", "boss_stage9_b.png", size=(40, 40)),
            "phase3": load_image("boss_skilles", "boss_stage9_c.png", size=(40, 40)),
            "phase4": load_image("boss_skilles", "boss_stage9_d.png", size=(40, 40))
        }
        self.minion_attack_image = load_image("bosses", "boss_stage9_N.png", size=(20, 20))
        self.gem_image = load_image("items", "mob_Jewelry_9.png", size=(40, 40))

        self.max_boss_hp = 100
        self.boss_hp = self.max_boss_hp
        self.boss_pos = [640 - 90, 100]
        self.boss_active = False
        self.boss_defeated = False
        self.boss_appeared = False
        self.stage_cleared = False

        self.boss_attacks = []
        self.attack_cooldown = 1200
        self.last_attack_time = 0
        self.phase = 1
        self.boss_hit = False
        self.boss_hit_start_time = 0
        self.invincible_duration = 500
        self.boss_hit_duration = 100

        self.move_timer = 0
        self.gem_active = False
        self.gem_pos = None

        self.minions = []
        self.minion_spawn_interval = 4000
        self.last_minion_spawn_time = 0

    def check_appear(self, seconds, current_level):
        if current_level == 1 and not self.boss_active and seconds >= 10:
            self.boss_active = True
            self.boss_appeared = True
            self.move_timer = 0
            self.last_attack_time = pygame.time.get_ticks()
            self.last_minion_spawn_time = pygame.time.get_ticks()

    def update_phase(self):
        if self.boss_hp <= 25:
            self.phase = 4
        elif self.boss_hp <= 50:
            self.phase = 3
        elif self.boss_hp <= 75:
            self.phase = 2
        else:
            self.phase = 1

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
                angles = list(range(0, 360, 30))
            elif self.phase == 3:
                angles = list(range(0, 360, 15))
            else:
                offset = (current_time // 100) % 360
                angles = [i + offset for i in range(0, 360, 10)]
            for angle in angles:
                rad = math.radians(angle)
                dx, dy = math.cos(rad) * 6, math.sin(rad) * 6
                self.boss_attacks.append({
                    'pos': [cx, cy],
                    'dir': [dx, dy],
                    'angle': angle,
                    'image': self.attack_images[f"phase{self.phase}"]
                })

    def spawn_minions(self, player_pos):
        if not self.boss_active:
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.last_minion_spawn_time >= self.minion_spawn_interval:
            self.last_minion_spawn_time = current_time
            for _ in range(self.phase):
                x = random.randint(100, 1100)
                y = random.randint(100, 600)
                mtype = random.choice(["A", "B", "C"])
                minion = {
                    'type': mtype,
                    'pos': [x, y],
                    'hp': 2,
                    'angle': random.randint(0, 360),
                    'center': [x, y],
                    'radius': random.randint(40, 80),
                    'last_attack_time': current_time,
                    'attacks': []
                }
                self.minions.append(minion)

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
                    {'pos': minion['pos'][:], 'dir': [-5, 3]}
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

    def update_attacks(self, player_pos):
        hit = 0
        new_attacks = []
        for atk in self.boss_attacks:
            atk['pos'][0] += atk['dir'][0]
            atk['pos'][1] += atk['dir'][1]
            if self.check_energy_ball_collision(atk['pos'], player_pos):
                hit += 1
            elif 0 <= atk['pos'][0] <= 1280 and 0 <= atk['pos'][1] <= 720:
                new_attacks.append(atk)
        self.boss_attacks = new_attacks

        for minion in self.minions:
            for atk in minion['attacks']:
                if self.check_energy_ball_collision(atk['pos'], player_pos):
                    hit += 1
        return hit

    def check_hit(self, attacks):
        current_time = pygame.time.get_ticks()
        if self.boss_hit and current_time - self.boss_hit_start_time < self.invincible_duration:
            return
        for atk in attacks:
            start, end, _, _ = atk
            if self.check_attack_collision(start, end, self.boss_pos, 180):
                self.boss_hp -= 1
                self.boss_hit = True
                self.boss_hit_start_time = current_time
                if self.boss_hp <= 0:
                    self.boss_defeated = True
                    self.boss_active = False
                    self.gem_active = True
                    self.gem_pos = [self.boss_pos[0] + 60, self.boss_pos[1] + 100]
                break
        self.update_phase()

        for minion in self.minions[:]:
            for atk in attacks:
                start, end, _, _ = atk
                if self.check_attack_collision(start, end, minion['pos'], 40):
                    minion['hp'] -= 1
                    if minion['hp'] <= 0:
                        self.minions.remove(minion)
                    break

    def draw(self, win):
        t = pygame.time.get_ticks()
        if self.boss_hit and (t - self.boss_hit_start_time < self.invincible_duration):
            if (t // self.boss_hit_duration) % 2 == 0:
                win.blit(self.boss_image, self.boss_pos)
        else:
            win.blit(self.boss_image, self.boss_pos)

    def draw_attacks(self, win):
        for atk in self.boss_attacks:
            angle = -atk['angle'] + 90
            rotated = pygame.transform.rotate(atk['image'], angle)
            rect = rotated.get_rect(center=atk['pos'])
            win.blit(rotated, rect)

    def draw_minion_attacks(self, win):
        for minion in self.minions:
            for atk in minion['attacks']:
                rotated = pygame.transform.rotate(self.minion_attack_image, 0)
                rect = rotated.get_rect(center=atk['pos'])
                win.blit(rotated, rect)

    def draw_gem(self, win):
        if self.gem_active:
            win.blit(self.gem_image, self.gem_pos)

    def draw_health_bar(self, win, font):
        if self.boss_active and self.boss_hp > 0:
            text = font.render("BOSS", True, (255, 255, 255))
            win.blit(text, (10, 680))
            ratio = self.boss_hp / self.max_boss_hp
            pygame.draw.rect(win, (50, 50, 50), (100, 680, 200, 30))
            pygame.draw.rect(win, (210, 20, 4), (100, 680, int(200 * ratio), 30))
            pygame.draw.rect(win, (255, 255, 255), (100, 680, 200, 30), 2)
        elif self.boss_hp <= 0 and self.boss_defeated:
            win.blit(font.render("BOSS DEFEATED", True, (255, 255, 255)), (10, 680))

    def check_energy_ball_collision(self, ball_pos, player_pos):
        px, py = player_pos
        bx, by = ball_pos
        return px < bx < px + 50 and py < by < py + 50

    def check_attack_collision(self, start, end, pos, size):
        rect = pygame.Rect(pos[0], pos[1], size, size)
        return rect.clipline(start, end)

    def check_gem_collision(self, player_pos):
        if self.gem_active:
            px, py = player_pos
            gx, gy = self.gem_pos
            return px < gx + 40 and px + 50 > gx and py < gy + 40 and py + 50 > gy
        return False

    def get_player_speed(self):
        return 10 

    def reset(self):
        self.__init__()
        self.boss_active = False
        self.boss_defeated = False
        self.boss_attacks.clear()
        self.stage_cleared = False
        self.gem_active = False
        self.minions.clear()
