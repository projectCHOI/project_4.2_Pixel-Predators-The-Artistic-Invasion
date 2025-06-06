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

class Stage5Boss:
    def __init__(self):
        self.boss_image_left = load_image("bosses", "boss_stage5_Left.png", size=(500, 500))
        self.boss_image_right = load_image("bosses", "boss_stage5_Right.png", size=(500, 500))
        self.boss_attack_images = [
            load_image("boss_skilles", "boss_stage5_a.png", size=(40, 40)),
            load_image("boss_skilles", "boss_stage5_b.png", size=(40, 40)),
            load_image("boss_skilles", "boss_stage5_c.png", size=(40, 40)),
        ]
        self.gem_image = load_image("items", "mob_Jewelry_5.png", size=(40, 40))
        self.boss_effect_image = load_image("boss_skilles", "boss_stage5_d.png", size=(300, 300))
        self.effect_offsets = [(-200, -200), (200, -200), (-250, 250), (250, 250),
                               (-100, -100), (100, -100), (-100, 100), (100, 100),
                               (-200, 0), (0, -200), (200, 0), (0, 200),
                               (0, 0)]
        
        self.max_boss_hp = 20
        self.boss_hp = self.max_boss_hp
        self.boss_damage = 2
        self.boss_invincible_duration = 500
        self.boss_hit_duration = 100

        self.side = random.choice(["left", "right"])
        if self.side == "left":
            self.boss_pos = [-500, 200]
            self.boss_image = self.boss_image_left
        else:
            self.boss_pos = [1500, 250]
            self.boss_image = self.boss_image_right

        self.boss_attacks = []
        self.boss_active = False
        self.boss_appeared = False
        self.boss_defeated = False
        self.gem_active = False
        self.gem_pos = None

        self.state = "appear"
        self.state_start_time = pygame.time.get_ticks()

        self.attack_cooldown = 1000
        self.last_attack_time = pygame.time.get_ticks()
        self.boss_hit = False
        self.boss_hit_start_time = 0

        self.vertical_moves_done = 0
        self.going_forward = True

        self.minions = []
    def draw_minion_attacks(self, win):
        pass
    def update_minion_behavior(self):
        pass
    def update_minion_attacks(self):
        pass
    def spawn_minions(self):
        pass

    def check_appear(self, seconds, current_level):
        if current_level == 5 and not self.boss_active and seconds >= 10 and not self.boss_appeared:
            self.boss_active = True
            self.boss_appeared = True

    def move(self):
        if not self.boss_active:
            return

        current_time = pygame.time.get_ticks()
        time_in_state = current_time - self.state_start_time

        if self.state == "appear":
            speed = 3
            if self.side == "left":
                self.boss_pos[0] += speed
                if self.boss_pos[0] >= 120:
                    self.boss_pos[0] = 120
                    self._change_state("wait1")
            else:
                self.boss_pos[0] -= speed
                if self.boss_pos[0] <= 830:
                    self.boss_pos[0] = 830
                    self._change_state("wait1")

        elif self.state == "wait1":
            if time_in_state >= 2000:
                self._change_state("act")

        elif self.state == "act":
            if self.side == "left":
                self._move_left_side()
            else:
                self._move_right_side()

        elif self.state == "wait2":
            if time_in_state >= 2000:
                self._change_state("leave")

        elif self.state == "leave":
            speed = 6
            if self.side == "left":
                self.boss_pos[0] -= speed
                if self.boss_pos[0] <= -500:
                    self.boss_pos[0] = -500
                    self._change_state("wait3")
            else:
                self.boss_pos[0] += speed
                if self.boss_pos[0] >= 1500:
                    self.boss_pos[0] = 1500
                    self._change_state("wait3")

        elif self.state == "wait3":
            if time_in_state >= 2000:
                self.reset(reinit_side=True)
                self._change_state("appear")

    def _change_state(self, new_state):
        self.state = new_state
        self.state_start_time = pygame.time.get_ticks()

    def _move_left_side(self):
        self.attack()
        if self.going_forward:
            self.boss_pos[0] += 3
            if self.boss_pos[0] >= 520:
                self.boss_pos[0] = 520
                self.going_forward = False
        else:
            self.boss_pos[0] -= 5
            if self.boss_pos[0] <= 120:
                self.boss_pos[0] = 120
                self._change_state("wait2")

    def _move_right_side(self):
        self.attack()
        speed = 6
        target_up = 110
        target_down = 250

        moving_up = (self.vertical_moves_done % 2 == 0)
        if moving_up:
            self.boss_pos[1] -= speed
            if self.boss_pos[1] <= target_up:
                self.boss_pos[1] = target_up
                self.vertical_moves_done += 1
        else:
            self.boss_pos[1] += speed
            if self.boss_pos[1] >= target_down:
                self.boss_pos[1] = target_down
                self.vertical_moves_done += 1

        if self.vertical_moves_done >= 10:
            if self.boss_pos[1] > 250:
                self.boss_pos[1] -= speed
                if self.boss_pos[1] <= 250:
                    self.boss_pos[1] = 250
                    self._change_state("wait2")
            elif self.boss_pos[1] < 250:
                self.boss_pos[1] += speed
                if self.boss_pos[1] >= 250:
                    self.boss_pos[1] = 250
                    self._change_state("wait2")
            else:
                self._change_state("wait2")

    def attack(self):
        if self.state != "act":
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = current_time

            if self.boss_hp > self.max_boss_hp * 0.75:
                directions = [0]
                self.attack_cooldown = 800
            elif self.boss_hp > self.max_boss_hp * 0.5:
                directions = [-15, 0, 15]
                self.attack_cooldown = 600
            elif self.boss_hp > self.max_boss_hp * 0.25:
                directions = [-30, -15, 0, 15, 30]
                self.attack_cooldown = 500
            else:
                directions = [-45, -30, -15, 0, 15, 30, 45]
                self.attack_cooldown = 350

            for angle_offset in directions:
                angle_deg = 0 if self.side == "left" else 180
                angle_deg += angle_offset
                rad = math.radians(angle_deg)
                dx = math.cos(rad) * 10
                dy = math.sin(rad) * 10

                start_x = self.boss_pos[0] + 250
                start_y = self.boss_pos[1] + 60

                random_attack_image = random.choice(self.boss_attack_images)

                self.boss_attacks.append({
                    'pos': [start_x, start_y],
                    'dir': [dx, dy],
                    'angle': angle_deg,
                    'time': 0,
                    'image': random_attack_image
                })

    def update_attacks(self, player_pos, is_invincible=False):
        new_boss_attacks = []
        player_hit = self.check_player_collision(player_pos)

        if is_invincible:
            for attack in self.boss_attacks:
                attack['pos'][0] += attack['dir'][0]
                attack['pos'][1] += attack['dir'][1]
                bx, by = attack['pos']
                if 0 <= bx <= 1280 and 0 <= by <= 520:
                    new_boss_attacks.append(attack)
            self.boss_attacks = new_boss_attacks
            return 0

        for attack in self.boss_attacks:
            attack['pos'][0] += attack['dir'][0]
            attack['pos'][1] += attack['dir'][1]
            bx, by = attack['pos']
            if 0 <= bx <= 1280 and 0 <= by <= 520:
                if self.check_energy_ball_collision((bx, by), player_pos):
                    player_hit += 1
                else:
                    new_boss_attacks.append(attack)

        self.boss_attacks = new_boss_attacks
        return player_hit

    def check_player_collision(self, player_pos):
        px, py = player_pos
        player_rect = pygame.Rect(px, py, 50, 50)
        boss_rect = pygame.Rect(self.boss_pos[0], self.boss_pos[1], 300, 300)  # 보스 hitbox
        
        for (offset_x, offset_y) in self.effect_offsets:
            effect_x = self.boss_pos[0] + offset_x
            effect_y = self.boss_pos[1] + offset_y
            effect_rect = pygame.Rect(effect_x, effect_y, 100, 100)
            if player_rect.colliderect(effect_rect):
                return 3

        if player_rect.colliderect(boss_rect):  
            return 3

        return 0

    def draw(self, win):
        if not self.boss_active:
            return

        if not self.boss_defeated and self.boss_hp > 0:
            current_time = pygame.time.get_ticks()
            if self.boss_hit:
                if current_time - self.boss_hit_start_time < self.boss_invincible_duration:
                    if (current_time // self.boss_hit_duration) % 2 == 0:
                        win.blit(self.boss_image, self.boss_pos)
                else:
                    self.boss_hit = False
                    win.blit(self.boss_image, self.boss_pos)
            else:
                win.blit(self.boss_image, self.boss_pos)

        # 보스 스킬 (등장 상태 등에서 보이는 효과)
        if self.state in ("appear", "wait1", "wait2", "wait3", "leave"):
            boss_center_x = self.boss_pos[0]
            boss_center_y = self.boss_pos[1]
            for (offset_x, offset_y) in self.effect_offsets:
                effect_x = boss_center_x + offset_x
                effect_y = boss_center_y + offset_y
                win.blit(self.boss_effect_image, (effect_x, effect_y))

    def draw_attacks(self, win):
        if not self.boss_active:
            return

        for attack in self.boss_attacks:
            angle = -attack['angle'] + 90
            rotated_image = pygame.transform.rotate(attack['image'], angle)  # ← 각 공격의 이미지
            rect = rotated_image.get_rect(center=attack['pos'])
            win.blit(rotated_image, rect)

    def draw_gem(self, win):
        if self.gem_active and self.gem_pos:
            win.blit(self.gem_image, self.gem_pos)

    def draw_health_bar(self, win, font):
        if not self.boss_active:
            return

        if not self.boss_defeated and self.boss_hp > 0:
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
        if not self.boss_active:
            return
        # 특정 상태(`act`)에서만 공격을 받을 수 있도록 설정
        if self.state not in ["act"]:
            return

        current_time = pygame.time.get_ticks()

        if self.boss_hit and (current_time - self.boss_hit_start_time) < self.boss_invincible_duration:
            return
        
        boss_rect = pygame.Rect(self.boss_pos[0], self.boss_pos[1], 300, 300)
        
        for attack in attacks:
            attack_start, attack_end, thickness, color = attack

            if boss_rect.clipline(attack_start, attack_end):
                self.boss_hp -= 1
                
                if self.boss_hp <= 0:
                    self.boss_hp = 0
                    self.boss_defeated = True
                    self.boss_active = False
                    self.boss_attacks.clear()
                    self.gem_pos = [self.boss_pos[0] + 40, self.boss_pos[1] + 40]
                    self.gem_active = True
                    break

                self.boss_hit = True
                self.boss_hit_start_time = current_time
                break

    def check_gem_collision(self, player_pos):
        if self.gem_active and self.gem_pos:
            px, py = player_pos
            gx, gy = self.gem_pos
            player_width, player_height = 50, 50
            gem_size = 40
            if (px < gx + gem_size and px + player_width > gx and
                py < gy + gem_size and py + player_height > gy):
                self.gem_active = False
                return True
        return False

    def check_energy_ball_collision(self, ball_pos, player_pos):
        bx, by = ball_pos
        px, py = player_pos
        player_width, player_height = 50, 50
        if px < bx < px + player_width and py < by < py + player_height:
            return True
        return False

    def check_attack_collision(self, attack_start, attack_end, boss_pos, boss_size):
        ex, ey = boss_pos
        sx, sy = attack_start
        rect = pygame.Rect(ex, ey, boss_size, boss_size)
        line = (sx, sy), attack_end
        return rect.clipline(line)

    def reset(self, reinit_side=False):
        if self.boss_defeated:
            return

        self.boss_hit = False
        self.boss_hit_start_time = 0
        self.boss_attacks.clear()
        
        if reinit_side:
            self.side = random.choice(["left", "right"])

        if self.side == "left":
            self.boss_pos = [-500, 200]
            self.boss_image = self.boss_image_left
        else:
            self.boss_pos = [1500, 250]
            self.boss_image = self.boss_image_right

        self.vertical_moves_done = 0
        self.going_forward = True
        self.gem_active = False
        self.gem_pos = None
        self.boss_active = False
        self.boss_appeared = False
        self.state = "appear"
        self.state_start_time = pygame.time.get_ticks()

    def draw_minions(self, win):
        pass
    
    def check_minion_collision(self, player_pos):
        return 0
    
    def get_player_speed(self):
        return 10
