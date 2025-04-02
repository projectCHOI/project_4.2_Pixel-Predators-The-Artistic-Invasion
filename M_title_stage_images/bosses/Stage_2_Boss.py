import pygame
import os
import math
import random

# BASE_DIR 설정: 현재 파일의 부모 디렉토리 기준으로 설정
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

class Stage2Boss: 
    def __init__(self):
        # 이미지 로드
        self.boss_image = load_image("bosses", "boss_stage2.png", size=(120, 120))
        self.boss_attack_images = load_image("boss_skilles", "boss_stage2_a.png", size=(40, 40))
        self.gem_image = load_image("items", "mob_Jewelry_2.png", size=(40, 40))
        
        # 보스 속성 초기화
        self.max_boss_hp = 20
        self.boss_hp = self.max_boss_hp
        self.boss_damage = 2
        self.boss_speed = 5
        self.boss_pos = [640 - 120, 0]
        self.boss_direction = [1, 1]  # 대각선 이동
        self.boss_active = False
        self.boss_attacks = []
        self.boss_last_attack_time = 0
        self.attack_interval = 1000  # 방향 전환 시마다 공격
        self.gem_pos = None
        self.gem_active = False
        self.boss_defeated = False
        self.boss_appeared = False
        self.stage_cleared = False
        
        # 점멸 효과 및 무적 상태
        self.boss_hit = False
        self.invincible = False
        self.invincible_duration = 500  # 무적 상태 지속 시간 (밀리초)
        self.last_hit_time = 0

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
        if current_level == 2 and not self.boss_active and seconds >= 10 and not self.boss_appeared:
            self.boss_active = True
            self.boss_pos = [640 - 120, 0]
            self.boss_hp = self.max_boss_hp
            self.boss_appeared = True

    def move(self):
        # 화면에서 바운스하는 대각선 이동
        self.boss_pos[0] += self.boss_speed * self.boss_direction[0]
        self.boss_pos[1] += self.boss_speed * self.boss_direction[1]

        # 경계에 닿으면 방향 전환 및 공격
        if self.boss_pos[0] <= 0 or self.boss_pos[0] >= 1280 - 240:
            self.boss_direction[0] *= -1
            self.attack()  # 방향 전환 시 공격
        if self.boss_pos[1] <= 0 or self.boss_pos[1] >= 720 - 240:
            self.boss_direction[1] *= -1
            self.attack()  # 방향 전환 시 공격

    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.boss_last_attack_time > self.attack_interval:
            self.boss_last_attack_time = current_time
            
            # 플레이어를 향해 발사할 단일 타겟 샷 수 결정
            num_shots = 1 + (self.max_boss_hp - self.boss_hp) // 5  # 체력 감소 시 공격 횟수 증가
            for _ in range(num_shots):
                target_x, target_y = random.randint(100, 1180), random.randint(100, 620)
                dx, dy = target_x - self.boss_pos[0], target_y - self.boss_pos[1]
                length = math.hypot(dx, dy)
                if length > 0:
                    direction = (dx / length, dy / length)
                    self.boss_attacks.append([self.boss_pos[0] + 60, self.boss_pos[1] + 60, direction])

    def update_attacks(self, player_pos):
        new_attacks = []
        player_hit = False
        for attack in self.boss_attacks:
            attack[0] += attack[2][0] * 10
            attack[1] += attack[2][1] * 10
            if 0 <= attack[0] <= 1280 and 0 <= attack[1] <= 720:
                if self.check_energy_ball_collision((attack[0], attack[1]), player_pos):
                    player_hit = True
                else:
                    new_attacks.append(attack)
        self.boss_attacks = new_attacks
        return player_hit

    def check_hit(self, attacks):
        current_time = pygame.time.get_ticks()
        if self.invincible and (current_time - self.last_hit_time) < self.invincible_duration:
            return

        for attack in attacks:
            start, end, thickness, color = attack  
            if self.check_attack_collision(start, end):
                self.boss_hp -= 1
                self.invincible = True
                self.boss_hit = True
                self.last_hit_time = current_time
                if self.boss_hp <= 0:
                    self.boss_active = False
                    self.gem_pos = [self.boss_pos[0] + 40, self.boss_pos[1] + 40]
                    self.gem_active = True
                    self.boss_defeated = True
                break

    def draw(self, win):
        if self.boss_hp > 0:
            current_time = pygame.time.get_ticks()
            if self.boss_hit:
                if current_time - self.last_hit_time >= self.invincible_duration:
                    self.boss_hit = False  # 무적 상태 및 깜박임 종료
                    win.blit(self.boss_image, self.boss_pos)
                else:
                    # 깜박임 효과
                    if (current_time // 100) % 2 == 0:  # 100ms 간격으로 깜박임
                        win.blit(self.boss_image, self.boss_pos)
            else:
                win.blit(self.boss_image, self.boss_pos)

    def draw_attacks(self, win):
        for attack in self.boss_attacks:
            win.blit(self.boss_attack_images, (attack[0], attack[1]))

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
        elif self.boss_hp <= 0 and self.stage_cleared:
            defeated_text = font.render("BOSS DEFEATED", True, (255, 255, 255))
            win.blit(defeated_text, (10, 680))

    def draw_gem(self, win):
        if self.gem_active:
            win.blit(self.gem_image, self.gem_pos)

    def reset(self):
        self.boss_active = False
        self.boss_hp = self.max_boss_hp
        self.boss_pos = [640 - 120, 0]
        self.boss_defeated = False
        self.boss_appeared = False
        self.gem_active = False
        self.gem_pos = None
        self.stage_cleared = False

    def check_attack_collision(self, attack_start, attack_end):
        # 사각형 충돌을 통해 보스와 공격의 충돌 여부 체크
        boss_rect = pygame.Rect(self.boss_pos[0], self.boss_pos[1], 120, 120)
        attack_line = (attack_start, attack_end)
        return boss_rect.clipline(attack_line)

    def check_energy_ball_collision(self, ball_pos, player_pos):
        bx, by = ball_pos
        ball_rect = pygame.Rect(bx, by, 10, 10)  # 에너지 볼의 크기를 가정하여 설정 (10x10 예시)
        px, py = player_pos
        player_rect = pygame.Rect(px, py, 50, 50)  # 플레이어 크기 (50x50)

        return player_rect.colliderect(ball_rect)

    def check_gem_collision(self, player_pos):
        if self.gem_active:
            px, py = player_pos
            player_rect = pygame.Rect(px, py, 50, 50)  # 플레이어 크기 (50x50)
            gx, gy = self.gem_pos
            gem_rect = pygame.Rect(gx, gy, 40, 40)  # 보석 크기 (40x40)

            if player_rect.colliderect(gem_rect):
                self.gem_active = False
                self.stage_cleared = True
                return True
        return False
    
    def get_player_speed(self):
        return 10