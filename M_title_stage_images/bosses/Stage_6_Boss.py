import pygame
import os
import random
import math

# BASE_DIR 로드: 현재 파일의 부모 디렉토리를 기준으로 설정
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

class Stage6Boss: 
    def __init__(self):
        self.boss_image = load_image("bosses", "boss_stage6.png", size=(300, 300))
        self.gem_image = load_image("items", "mob_Jewelry_6.png", size=(40, 40))
        self.boss_attack_images = {
            "high": load_image("boss_skilles", "boss_stage6_a.png", size=(30, 30)),
            "medium": load_image("boss_skilles", "boss_stage6_b.png", size=(30, 30)),
            "low": load_image("boss_skilles", "boss_stage6_c.png", size=(30, 30))
        }

        # 보스 속성 초기화
        self.max_boss_hp = 18
        self.boss_hp = self.max_boss_hp
        self.boss_damage = 2
        self.boss_pos = [1000, 600]
        self.boss_active = False
        self.boss_appearing = False
        self.boss_waiting = False
        self.boss_disappearing = False
        self.boss_appeared = False
        self.boss_moving = False
        self.boss_returning = False
        self.move_target = None
        self.boss_speed = 2
        self.wait_time = 0
        self.boss_attacks = []
        self.boss_last_attack_time = 0
        self.attack_interval = 1200
        self.boss_defeated = False
        self.stage_cleared = False
        self.gem_active = False
        self.gem_pos = None
        self.invincible_duration = 500
        self.boss_hit_duration = 100
        self.boss_hit = False
        self.boss_hit_start_time = 0
        self.minions = []

    def check_attack_collision(self, attack_start, attack_end, boss_pos, boss_size):
        rect = pygame.Rect(boss_pos[0], boss_pos[1], boss_size, boss_size)
        return rect.clipline((attack_start, attack_end))

    def draw_minion_attacks(self, win):
        pass

    def update_minion_behavior(self):
        pass

    def update_minion_attacks(self):
        pass

    def spawn_minions(self):
        pass

    def get_attack_type(self):
        health_ratio = self.boss_hp / self.max_boss_hp
        if health_ratio > 0.6:
            return "low"
        elif health_ratio > 0.3:
            return "medium"
        else:
            return "high"

    def check_appear(self, seconds, current_level):
        if current_level == 6 and not self.boss_active and seconds >= 10 and not self.boss_appeared:
            self.boss_active = True
            self.boss_appearing = True
            self.boss_hp = self.max_boss_hp
            self.boss_appeared = True

    def move(self):
        if self.boss_appearing:
            self.boss_pos[1] -= self.boss_speed
            if self.boss_pos[1] <= 400:
                self.boss_appearing = False
                self.boss_waiting = True
                self.wait_time = pygame.time.get_ticks()
        elif self.boss_waiting:
            if pygame.time.get_ticks() - self.wait_time >= 3000:
                self.boss_waiting = False
                self.boss_moving = True
                self.move_target = self.boss_pos[0] - 300
        elif self.boss_moving:
            if self.boss_pos[0] > self.move_target:
                self.boss_pos[0] -= self.boss_speed
            else:
                self.boss_moving = False
                self.boss_returning = True
        elif self.boss_returning:
            if self.boss_pos[0] < 1000:
                self.boss_pos[0] += self.boss_speed
            else:
                self.boss_returning = False
                self.boss_disappearing = True
        elif self.boss_disappearing:
            self.boss_pos[1] += self.boss_speed
            if self.boss_pos[1] >= 600:
                self.boss_disappearing = False
                self.boss_appearing = True

    def attack(self):
        if not self.boss_moving and not self.boss_returning:
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.boss_last_attack_time > self.attack_interval:
            self.boss_last_attack_time = current_time
            attack_type = self.get_attack_type()
            num_shots = {"low": 12, "medium": 24, "high": 36}[attack_type]
            speed = {"low": 5, "medium": 6, "high": 7}[attack_type]
            image = self.boss_attack_images[attack_type]
            angle_step = 360 / num_shots
            for i in range(num_shots):
                angle = angle_step * i
                radian = math.radians(angle)
                dx = math.cos(radian) * speed
                dy = math.sin(radian) * speed
                self.boss_attacks.append([self.boss_pos[:], [dx, dy], angle, image])

    def update_attacks(self, player_pos, is_invincible=False):
        new_attacks = []
        player_width, player_height = 40, 40
        hit = False
        for attack in self.boss_attacks:
            attack[0][0] += attack[1][0]
            attack[0][1] += attack[1][1]
            if 0 <= attack[0][0] <= 1280 and 0 <= attack[0][1] <= 720:
                if player_pos[0] < attack[0][0] < player_pos[0] + player_width and                    player_pos[1] < attack[0][1] < player_pos[1] + player_height:
                    hit = True
                else:
                    new_attacks.append(attack)
        self.boss_attacks = new_attacks
        return hit           

    def draw(self, win):
        if self.boss_hp > 0:
            current_time = pygame.time.get_ticks()
            if self.boss_hit and (current_time - self.boss_hit_start_time) < self.invincible_duration:
                if (current_time // self.boss_hit_duration) % 2 == 0:
                    win.blit(self.boss_image, self.boss_pos)
            else:
                win.blit(self.boss_image, self.boss_pos)

    def draw_attacks(self, win):
        for attack in self.boss_attacks:
            angle = -attack[2] + 90
            rotated_image = pygame.transform.rotate(attack[3], angle)
            rect = rotated_image.get_rect(center=attack[0])
            win.blit(rotated_image, rect)

    def draw_health_bar(self, win, font):
        if self.boss_active and self.boss_hp > 0:
            # "BOSS" 문자열 그림
            boss_text = font.render("BOSS", True, (255, 255, 255))
            text_x = 10
            text_y = 680
            win.blit(boss_text, (text_x, text_y))

            # 체력 바 설정
            health_bar_x = text_x + boss_text.get_width() + 10
            health_bar_y = 680
            health_bar_width = 200  # 체력 바의 전체 너비
            health_bar_height = 30

            # 체력 비율 계산
            health_ratio = self.boss_hp / self.max_boss_hp
            current_health_width = int(health_bar_width * health_ratio)

            # 체력 바 배경 그림
            pygame.draw.rect(win, (50, 50, 50), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

            # 현재 체력 바 그림
            pygame.draw.rect(win, (210, 20, 4), (health_bar_x, health_bar_y, current_health_width, health_bar_height))

            # 체력 바 테두리 그림
            pygame.draw.rect(win, (255, 255, 255), (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)
        elif self.boss_hp <= 0 and self.boss_defeated:
            # 보스가 제거되었을 때 메시지 표시 (옵션)
            defeated_text = font.render("BOSS DEFEATED", True, (255, 255, 255))
            win.blit(defeated_text, (10, 680))

    def check_hit(self, attacks):
        if self.boss_disappearing:
            return
        current_time = pygame.time.get_ticks()
        if self.boss_hit and (current_time - self.boss_hit_start_time) < self.invincible_duration:
            return
        self.boss_hit = False
        for attack in attacks:
            start, end, _, _ = attack
            if self.check_attack_collision(start, end, self.boss_pos, 150):
                self.boss_hp -= 1
                if self.boss_hp <= 0:
                    self.boss_hp = 0
                    self.boss_active = False
                    self.boss_defeated = True
                    self.gem_active = True
                    self.gem_pos = [self.boss_pos[0] + 50, self.boss_pos[1] + 50]
                self.boss_hit = True
                self.boss_hit_start_time = current_time
                break

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
    
    def draw_gem(self, win):
        if self.gem_active and self.gem_pos:
            win.blit(self.gem_image, self.gem_pos)

    def reset(self):
        self.boss_active = False
        self.boss_hp = self.max_boss_hp
        self.boss_pos = [1000, 600]
        self.boss_appearing = True
        self.boss_defeated = False
        self.boss_attacks = []
        self.boss_hit = False
        self.stage_cleared = False
        self.gem_active = False
        self.gem_pos = None

    def check_attack_collision(self, attack_start, attack_end, boss_pos, boss_size):
        ex, ey = boss_pos
        sx, sy = attack_start
        ex2, ey2 = ex + boss_size, ey + boss_size

        # 공격 선분과 보스 사각형의 충돌 검증
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
