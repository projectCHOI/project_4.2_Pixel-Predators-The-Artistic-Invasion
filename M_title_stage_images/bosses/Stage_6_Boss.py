import pygame
import os
import random
import math

# BASE_DIR 로즈: 현재 파일의 부모 디렉토리를 기준으로 설정
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
        # 이미지 로드 (필요 이미지: 보스, 장애물, 보석)
        self.boss_image = load_image("bosses", "boss_stage6.png", size=(120, 120))
        self.obstacle_image = load_image("boss_skilles", "boss_stage6_d.png", size=(50, 50))
        self.gem_image = load_image("items", "mob_Jewelry_6.png", size=(40, 40))

        # 보스 속성 초기화
        self.max_boss_hp = 18
        self.boss_hp = self.max_boss_hp
        self.boss_damage = 2
        self.boss_pos = None  # 처음에는 None으로 설정
        self.boss_active = False
        self.gem_pos = None
        self.gem_active = False
        self.boss_defeated = False
        self.boss_appeared = False
        self.stage_cleared = False

        # 장애물 속성 초기화
        self.obstacles = []
        self.obstacle_active = False

    def check_appear(self, seconds, current_level):
        if current_level == 6 and not self.boss_active and seconds >= 10 and not self.boss_appeared:
            self.boss_active = True
            self.boss_hp = self.max_boss_hp
            self.boss_appeared = True
            self.boss_pos = [640 - 60, 360 - 60]  # 보스는 화면 정중앙에 나타남
            self.spawn_obstacles()

    def spawn_obstacles(self):
        # 화면 테두리에 장애물 생성
        self.obstacles = [
            [0, 0],  # 왼쪽 상단
            [0, 720 - 50],  # 왼쪽 하단
            [1280 - 50, 0],  # 오른쪽 상단
            [1280 - 50, 720 - 50]  # 오른쪽 하단
        ]
        self.obstacle_active = True

    def draw(self, win):
        if self.boss_active and self.boss_hp > 0:
            win.blit(self.boss_image, self.boss_pos)

    def draw_obstacles(self, win):
        if self.obstacle_active:
            for obstacle_pos in self.obstacles:
                win.blit(self.obstacle_image, obstacle_pos)

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

            pygame.draw.rect(win, (50, 50, 50), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
            pygame.draw.rect(win, (210, 20, 4), (health_bar_x, health_bar_y, current_health_width, health_bar_height))
            pygame.draw.rect(win, (255, 255, 255), (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)
        elif self.boss_hp <= 0 and self.boss_defeated:
            defeated_text = font.render("BOSS DEFEATED", True, (255, 255, 255))
            win.blit(defeated_text, (10, 680))

    def check_hit(self, attacks):
        for attack in attacks:
            attack_start, attack_end, thickness = attack
            if self.check_attack_collision(attack_start, attack_end, self.boss_pos, 120):
                self.boss_hp -= 1
                if self.boss_hp < 0:
                    self.boss_hp = 0
                if self.boss_hp <= 0:
                    self.boss_active = False
                    self.gem_pos = [self.boss_pos[0] + 100, self.boss_pos[1] + 100]
                    self.gem_active = True
                    self.boss_defeated = True
                break

    def check_gem_collision(self, player_pos):
        if self.gem_active:
            px, py = player_pos
            gx, gy = self.gem_pos
            player_width, player_height = 40, 40
            gem_size = 40
            if px < gx + gem_size and px + player_width > gx and py < gy + gem_size and py + player_height > gy:
                self.gem_active = False
                self.stage_cleared = True
                return True
        return False

    def reset(self):
        self.boss_active = False
        self.boss_hp = self.max_boss_hp
        self.boss_pos = None
        self.boss_defeated = False
        self.boss_appeared = False
        self.gem_active = False
        self.gem_pos = None
        self.stage_cleared = False
        self.obstacles = []
        self.obstacle_active = False

    def check_attack_collision(self, attack_start, attack_end, boss_pos, boss_size):
        ex, ey = boss_pos
        sx, sy = attack_start
        ex2, ey2 = ex + boss_size, ey + boss_size

        rect = pygame.Rect(ex, ey, boss_size, boss_size)
        line = (sx, sy), attack_end
        if rect.clipline(line):
            return True
        return False
