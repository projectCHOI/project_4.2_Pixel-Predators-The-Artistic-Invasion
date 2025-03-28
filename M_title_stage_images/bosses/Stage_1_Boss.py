import pygame
import os
import random
import math

# BASE_DIR 설정: 현재 파일의 부모 디렉토리 기준
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

class Stage1Boss:
    class GravityCore:
        def __init__(self, pos, duration=5000, radius=150):
            self.pos = pos
            self.duration = duration  # 지속 시간 (밀리초)
            self.radius = radius      # 중력 영향 범위
            self.spawn_time = pygame.time.get_ticks()

        def is_active(self):
            return pygame.time.get_ticks() - self.spawn_time < self.duration

        def draw(self, win):
            # 반투명 서피스를 생성하여 원형 중력 코어 효과 연출
            core_surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(core_surface, (100, 100, 255, 128), (self.radius, self.radius), self.radius)
            win.blit(core_surface, (self.pos[0] - self.radius, self.pos[1] - self.radius))

    def __init__(self):
        self.boss_image = load_image("bosses", "boss_stage8.png", size=(120, 120))
        self.boss_attack_images = {
            "high": load_image("boss_skilles", "boss_stage8_a.png", size=(40, 40)),
            "medium": load_image("boss_skilles", "boss_stage8_a.png", size=(40, 40)),
            "low": load_image("boss_skilles", "boss_stage8_a.png", size=(40, 40))
        }
        self.teleport_warning_image = load_image("stages", "Stage18_mist.png", size=(60, 60))
        self.gem_image = load_image("items", "mob_Jewelry_8.png", size=(40, 40))

        # 보스 속성 초기화
        self.max_boss_hp = 15
        self.boss_hp = self.max_boss_hp
        self.boss_damage = 2
        self.boss_pos = [640 - 60, 360 - 60]  # 화면 정중앙
        self.boss_active = False
        self.boss_attacks = []
        self.boss_last_attack_time = 0
        self.attack_interval = 1000
        self.teleport_interval = 4000
        self.last_teleport_time = 0
        self.gem_pos = None
        self.gem_active = False
        self.boss_defeated = False
        self.boss_appeared = False
        self.stage_cleared = False
        self.invincible = False
        self.invincible_duration = 500
        self.last_hit_time = 0
        self.boss_hit = False
        self.boss_hit_start_time = 0
        self.boss_hit_duration = 100

        # 중력 코어 관련 속성
        self.gravity_cores = []  # GravityCore 객체들을 저장하는 리스트
        self.core_spawn_interval = 6000  # 6초마다 새로운 중력 코어 생성
        self.last_core_spawn_time = 0

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
        if current_level == 1 and not self.boss_active and seconds >= 10 and not self.boss_appeared:
            self.boss_active = True
            self.boss_hp = self.max_boss_hp
            self.boss_appeared = True

    def move(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_teleport_time > self.teleport_interval:
            # 랜덤한 위치로 텔레포트
            self.boss_pos = [random.randint(0, 1280 - 120), random.randint(0, 720 - 120)]
            self.last_teleport_time = current_time
            # 텔레포트 후 공격 실행
            self.attack()

        # 중력 코어 업데이트 (생성 및 만료 체크)
        self.update_gravity_cores()

    def update_gravity_cores(self):
        # 활성화된 중력 코어만 남기기
        self.gravity_cores = [core for core in self.gravity_cores if core.is_active()]
        current_time = pygame.time.get_ticks()
        if current_time - self.last_core_spawn_time >= self.core_spawn_interval:
            self.last_core_spawn_time = current_time
            # 화면 내 일정 범위에서 중력 코어 생성
            new_core_pos = [random.randint(100, 1180), random.randint(100, 620)]
            self.gravity_cores.append(self.GravityCore(new_core_pos, duration=5000, radius=150))

    def apply_gravity(self, player_pos):
        """
        중력 코어들이 플레이어에 미치는 영향을 계산하여
        (x, y) 형태의 힘 벡터를 반환합니다.
        """
        total_force = [0, 0]
        gravity_factor = 2.0  # 조절 인자 (값을 높이면 끌어당김 강해짐)
        for core in self.gravity_cores:
            if core.is_active():
                dx = core.pos[0] - player_pos[0]
                dy = core.pos[1] - player_pos[1]
                dist = math.hypot(dx, dy)
                if dist < core.radius and dist > 0:
                    # 중력 효과: 코어 반경 내일수록 더 강하게 끌어당김
                    magnitude = gravity_factor * (core.radius - dist) / core.radius
                    total_force[0] += (dx / dist) * magnitude
                    total_force[1] += (dy / dist) * magnitude
        return total_force

    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.boss_last_attack_time > self.attack_interval:
            self.boss_last_attack_time = current_time
            num_shots = 3 + (self.max_boss_hp - self.boss_hp) // 3
            for i in range(num_shots):
                angle = random.uniform(0, 360)
                radian = math.radians(angle)
                dx = math.cos(radian) * 5
                dy = math.sin(radian) * 5
                attack_type = self.get_attack_type()
                self.boss_attacks.append({
                    'pos': [self.boss_pos[0] + 60, self.boss_pos[1] + 60],
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
            attack['time'] += 1  # 경과 시간 증가
            t = attack['time'] / 10.0
            # 기본 이동
            attack['pos'][0] += attack['dir'][0]
            attack['pos'][1] += attack['dir'][1]
            # 곡선 효과: x축에 sine 함수를 적용하여 흔들림 효과 부여
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
        # 보스 그리기 (피격 효과 포함)
        if self.boss_hp > 0:
            current_time = pygame.time.get_ticks()
            if self.boss_hit:
                if current_time - self.boss_hit_start_time >= self.invincible_duration:
                    self.boss_hit = False
                    win.blit(self.boss_image, self.boss_pos)
                else:
                    if (current_time // self.boss_hit_duration) % 2 == 0:
                        win.blit(self.boss_image, self.boss_pos)
            else:
                win.blit(self.boss_image, self.boss_pos)
        # 중력 코어 그리기
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
            pygame.draw.rect(win, (50, 50, 50), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
            pygame.draw.rect(win, (210, 20, 4), (health_bar_x, health_bar_y, current_health_width, health_bar_height))
            pygame.draw.rect(win, (255, 255, 255), (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)
        elif self.boss_hp <= 0 and self.boss_defeated:
            defeated_text = font.render("BOSS DEFEATED", True, (255, 255, 255))
            win.blit(defeated_text, (10, 680))

    def check_hit(self, attacks):
        current_time = pygame.time.get_ticks()
        if self.boss_hit and (current_time - self.boss_hit_start_time) < self.invincible_duration:
            return
        else:
            self.boss_hit = False
        for attack in attacks:
            start, end, thickness, color = attack
            if self.check_attack_collision(start, end, self.boss_pos, 120):
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

    def reset(self):
        self.boss_active = False
        self.boss_hp = self.max_boss_hp
        self.boss_pos = [640 - 120, 0]
        self.boss_defeated = False
        self.boss_appeared = False
        self.boss_attacks = []
        self.gem_active = False
        self.gem_pos = None
        self.boss_hit = False
        self.stage_cleared = False
        self.gravity_cores.clear()

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
        if rect.clipline(line):
            return True
        return False
