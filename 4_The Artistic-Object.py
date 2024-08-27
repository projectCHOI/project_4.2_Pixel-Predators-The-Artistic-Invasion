import pygame
import random
import math

# 기본 설정
pygame.init()

# 윈도우 설정
win = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("The Artistic Invasion")
clock = pygame.time.Clock()

# 색상 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# 상수 정의
PLAYER_SPEED = 10
MAX_HEALTH = 7
STAGE_DURATION = 60  # 스테이지 진행 시간 (초)
INVINCIBLE_DURATION = 3000  # 무적 시간 (밀리초)
BLINK_DURATION = 1500  # 깜빡임 지속 시간
BLINK_INTERVAL = 100  # 깜빡임 간격
BOSS_APPEAR_TIME = 30  # 보스 등장 시간 (초)
BOSS_HP = 100
BOSS_SPEED = 5

# 경로 설정
font_path = r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_cover/서평원 꺾깎체/OTF/SLEIGothicOTF.otf"
font_size = 30  # 폰트 크기

# 이미지 로드 함수
def load_and_scale_image(path, size):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, size)

# 텍스트 렌더링 함수
def render_text(text, position, color=WHITE):
    font = pygame.font.Font(font_path, font_size)
    text_surface = font.render(text, True, color)
    win.blit(text_surface, position)

# 대시보드 그리기 함수
def draw_dashboard(health, enemies_defeated, seconds):
    render_text(f"{seconds}", (640, 10))
    for i in range(health):
        win.blit(health_image, (10 + i * 50, 10))
    render_text(f"제거: {enemies_defeated}", (1280 - 100, 10))

class GameObject:
    def __init__(self, pos, size, image):
        self.pos = pos
        self.size = size
        self.image = image

    def draw(self):
        win.blit(self.image, self.pos)

class Player(GameObject):
    def __init__(self, pos):
        super().__init__(pos, (40, 40), player_image1)
        self.speed = PLAYER_SPEED
        self.health = MAX_HEALTH
        self.blinking = False
        self.invincible = False
        self.blink_start_time = 0
        self.invincible_start_time = 0
        self.blink_duration = BLINK_DURATION
        self.blink_interval = BLINK_INTERVAL
        self.attacks = []

    def move(self, direction):
        if direction == "left":
            self.pos[0] -= self.speed
        elif direction == "right":
            self.pos[0] += self.speed
        elif direction == "up":
            self.pos[1] -= self.speed
        elif direction == "down":
            self.pos[1] += self.speed
        self.pos[0] = max(0, min(self.pos[0], 1240))
        self.pos[1] = max(0, min(self.pos[1], 680))

    def shoot(self, target_pos, power_level):
        attack_start = (self.pos[0] + self.size[0] // 2, self.pos[1] + self.size[1] // 2)
        offset = power_level * 5
        self.attacks.append((attack_start, target_pos, 3))
        if power_level > 0:
            self.attacks.append((attack_start, (target_pos[0] + offset, target_pos[1] + offset), 3))
            self.attacks.append((attack_start, (target_pos[0] - offset, target_pos[1] - offset), 3))

    def check_collision(self, enemies):
        for enemy in enemies:
            if (self.pos[0] < enemy.pos[0] < self.pos[0] + self.size[0] or
                enemy.pos[0] < self.pos[0] < enemy.pos[0] + enemy.size[0]) and \
                (self.pos[1] < enemy.pos[1] < self.pos[1] + self.size[1] or
                 self.pos[1] < enemy.pos[1] < self.pos[1] + self.size[1]):
                return True
        return False

    def take_damage(self, damage):
        if not self.invincible:
            self.health -= damage
            if self.health <= 0:
                return False
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()
            self.blinking = True
            self.blink_start_time = pygame.time.get_ticks()
        return True

    def update_invincibility(self):
        current_time = pygame.time.get_ticks()
        if self.invincible and current_time - self.invincible_start_time > INVINCIBLE_DURATION:
            self.invincible = False
        if self.blinking and current_time - self.blink_start_time > self.blink_duration:
            self.blinking = False

    def draw(self):
        if self.blinking:
            if (pygame.time.get_ticks() - self.blink_start_time) // self.blink_interval % 2 == 0:
                win.blit(self.image, self.pos)
        else:
            win.blit(self.image, self.pos)

class Enemy(GameObject):
    def __init__(self, pos, size, image, speed, direction, hp):
        super().__init__(pos, size, image)
        self.speed = speed
        self.direction = direction
        self.hp = hp

    def move(self):
        self.pos[0] += self.direction[0] * self.speed
        self.pos[1] += self.direction[1] * self.speed

    def check_collision_with_attack(self, attack_start, attack_end):
        ex, ey = self.pos
        sx, sy = attack_start
        ex2, ey2 = ex + self.size[0], ey + self.size[1]
        if min(sx, attack_end[0]) <= ex2 and max(sx, attack_end[0]) >= ex and \
           min(sy, attack_end[1]) <= ey2 and max(sy, attack_end[1]) >= ey:
            return True
        return False

class Boss(GameObject):
    def __init__(self, pos, hp):
        super().__init__(pos, (120, 120), boss_image)
        self.hp = hp
        self.speed = BOSS_SPEED
        self.move_phase = 1
        self.direction_x = 1
        self.direction_y = 1
        self.attacks = []

    def move(self):
        if self.move_phase == 1:  # 중앙으로 이동
            target_pos = [640 - 60, 360 - 60]
            direction = [target_pos[0] - self.pos[0], target_pos[1] - self.pos[1]]
            length = math.hypot(direction[0], direction[1])
            if length > self.speed:
                direction = [direction[0] / length, direction[1] / length]
                self.pos[0] += direction[0] * self.speed
                self.pos[1] += direction[1] * self.speed
            else:
                self.pos = target_pos
                self.move_phase = 2
        elif self.move_phase == 2:  # 좌우 이동
            self.pos[0] += self.speed * self.direction_x
            if self.pos[0] <= 60 or self.pos[0] >= 1280 - 180:
                self.direction_x *= -1
            if self.hp <= 50:
                self.move_phase = 3
        elif self.move_phase == 3:  # 좌우+위아래 이동
            self.pos[0] += self.speed * self.direction_x
            self.pos[1] += self.speed * self.direction_y
            if self.pos[0] <= 60 or self.pos[0] >= 1280 - 180:
                self.direction_x *= -1
            if self.pos[1] <= 60 or self.pos[1] >= 720 - 180:
                self.direction_y *= -1

    def attack(self):
        possible_directions = []
        if self.hp <= 100 and self.hp > 80:
            possible_directions = ["down"]
        elif self.hp <= 80 and self.hp > 60:
            possible_directions = ["down", "up"]
        elif self.hp <= 60 and self.hp > 40:
            possible_directions = ["down", "up", "right"]
        elif self.hp <= 40 and self.hp > 0:
            possible_directions = ["down", "up", "right", "left"]

        if possible_directions:
            attack_direction = random.choice(possible_directions)
            if attack_direction == "down":
                attack_start_pos = [self.pos[0] + 60, self.pos[1] + 120]
            elif attack_direction == "up":
                attack_start_pos = [self.pos[0] + 60, self.pos[1]]
            elif attack_direction == "right":
                attack_start_pos = [self.pos[0] + 120, self.pos[1] + 60]
            elif attack_direction == "left":
                attack_start_pos = [self.pos[0], self.pos[1] + 60]

            self.attacks.append([attack_start_pos[0], attack_start_pos[1], attack_direction])

    def check_collision_with_attack(self, attack_start, attack_end):
        return check_attack_collision(attack_start, attack_end, self.pos, 120)

    def draw_health_bar(self):
        bar_x = 150
        bar_y = 680
        bar_width = 10
        bar_height = 10
        bars = self.hp // 2
        render_text("BOSS LIFE:", (10, 675))
        for i in range(bars):
            pygame.draw.rect(win, YELLOW, (bar_x + i * (bar_width + 2), bar_y, bar_width, bar_height))

class Game:
    def __init__(self):
        self.level = 1
        self.max_level = 12
        self.player = Player([640 - 20, 360 - 20])
        self.enemies = []
        self.boss = None
        self.seconds = 0
        self.start_ticks = pygame.time.get_ticks()
        self.game_active = False
        self.game_over = False
        self.game_over_reason = None
        self.stage_clear_times = [None] * 12  # 스테이지 1부터 12까지의 클리어 시간을 저장
        self.enemies_defeated = 0

    def intro_screen(self, stage):
        win.blit(stage_intro_images[stage - 1], (0, 0))
        pygame.display.update()
        pygame.time.delay(3000)

    def title_screen(self):
        win.blit(title_image, (0, 0))
        pygame.display.update()

    def draw_objects(self):
        win.blit(stage_background_images[self.level - 1], (0, 0))
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        if self.boss:
            self.boss.draw()
            self.boss.draw_health_bar()
        draw_dashboard(self.player.health, self.enemies_defeated, self.seconds)
        pygame.display.update()

    def generate_enemies(self):
        level_config = [
            (10, [(0, 1)], [40], random.randint(1, 2)),
            (10, [(0, 1)], [40], random.randint(1, 3)),
            (10, [(0, 1), (0, -1)], [40, 60], random.randint(1, 4)),
            (random.randint(10, 12), [(0, 1), (0, -1)], [40, 60], random.randint(3, 8)),
            (random.randint(10, 12), [(1, 0), (-1, 0)], [20, 40], random.randint(6, 16)),
            (random.randint(10, 14), [(0, 1), (0, -1), (1, 0), (-1, 0)], [20, 40], random.randint(6, 20)),
            (random.randint(10, 16), [(0, 1), (0, -1), (1, 0), (-1, 0)], [20, 40, 60], random.randint(6, 24)),
            (random.randint(10, 18), [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)], [20, 40, 60], random.randint(6, 26)),
            (random.randint(10, 18), [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)], [20, 40, 60], random.randint(8, 30)),
            (random.randint(10, 20), [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)], [20, 40, 60], random.randint(8, 30)),
            (random.randint(10, 20), [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)], [20, 40, 60], random.randint(10, 32)),
            (random.randint(10, 20), [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)], [20, 40, 60], random.randint(15, 32))
        ]
        speed, directions, sizes, num_enemies = level_config[self.level - 1]
        new_enemies = []
        for _ in range(num_enemies):
            direction = random.choice(directions)
            size = random.choice(sizes)
            if direction == (0, 1):
                pos = [random.randint(0, 1200-size), 0]
                image = enemy_images["up"] if size == 40 else sentinel_shooter_left if size == 60 else ambush_striker_up
            elif direction == (0, -1):
                pos = [random.randint(0, 1200-size), 700-size]
                image = enemy_images["down"] if size == 40 else sentinel_shooter_left if size == 60 else ambush_striker_down
            elif direction == (1, 0):
                pos = [0, random.randint(0, 700-size)]
                image = enemy_images["left"] if size == 40 else sentinel_shooter_right if size == 60 else ambush_striker_left
            elif direction == (-1, 0):
                pos = [1200-size, random.randint(0, 700-size)]
                image = enemy_images["right"] if size == 40 else sentinel_shooter_right if size == 60 else ambush_striker_right

            if size == 40:
                enemy_type = "move_and_disappear"
                hp = 1
            elif size == 60:
                target_pos = [random.randint(100, 1100), random.randint(100, 600)]
                direction = [target_pos[0] - pos[0], target_pos[1] - pos[1]]
                length = math.hypot(direction[0], direction[1])
                direction = [direction[0] / length, direction[1] / length]
                hp = 2
            elif size == 20:
                enemy_type = "approach_and_shoot"
                hp = 1
            new_enemies.append(Enemy(pos, size, image, speed, direction, hp))
        return new_enemies

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                target_pos = pygame.mouse.get_pos()
                self.player.shoot(target_pos, power_item_active)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not self.game_active:
                        if self.game_over:
                            self.reset_game()
                        else:
                            self.start_game()
        return True

    def start_game(self):
        self.level = 1
        self.game_active = True
        self.start_ticks = pygame.time.get_ticks()
        self.intro_screen(self.level)
        self.player.attacks = []
        self.enemies = []
        self.boss = None

    def reset_game(self):
        self.level = 1
        self.game_active = True
        self.game_over = False
        self.player.health = MAX_HEALTH
        self.enemies_defeated = 0
        self.start_ticks = pygame.time.get_ticks()
        self.stage_clear_times = [None] * 12
        self.player.attacks = []
        self.enemies = []
        self.boss = None
        self.intro_screen(self.level)

    def update(self):
        self.seconds = (pygame.time.get_ticks() - self.start_ticks) // 1000
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player.move("left")
        if keys[pygame.K_d]:
            self.player.move("right")
        if keys[pygame.K_w]:
            self.player.move("up")
        if keys[pygame.K_s]:
            self.player.move("down")

        self.player.update_invincibility()

        if self.seconds >= 300:
            self.end_game("time_over")
        
        # 적 충돌 처리 및 업데이트
        for attack in self.player.attacks:
            new_enemies = []
            for enemy in self.enemies:
                if enemy.check_collision_with_attack(attack[0], attack[1]):
                    enemy.hp -= 1
                    if enemy.hp <= 0:
                        self.enemies_defeated += 1
                    else:
                        new_enemies.append(enemy)
                else:
                    new_enemies.append(enemy)
            self.enemies = new_enemies

        # 보스 처리
        if self.boss:
            if self.boss.check_collision_with_attack(attack[0], attack[1]):
                self.boss.hp -= 1
                if self.boss.hp <= 0:
                    self.boss = None
                    gem_pos = [self.boss.pos[0] + 40, self.boss.pos[1] + 40]
                    self.end_game("victory")

            self.boss.move()
            self.boss.attack()

        if self.player.check_collision(self.enemies):
            if not self.player.take_damage(1):
                self.end_game("game_over")

    def end_game(self, reason):
        self.game_active = False
        self.game_over = True
        self.game_over_reason = reason

    def draw_end_screen(self):
        if self.game_over_reason == "victory":
            image = victory_image
        elif self.game_over_reason == "game_over":
            image = game_over_image
        elif self.game_over_reason == "time_over":
            image = time_over_image

        win.blit(image, (0, 0))
        render_text("continue : enter", (640, 360))
        pygame.display.update()

    def run(self):
        while True:
            if not self.game_active:
                if not self.game_over:
                    self.title_screen()
                else:
                    self.draw_end_screen()
            else:
                self.update()
                self.draw_objects()

            if not self.handle_events():
                break

            clock.tick(30)

# 이미지 로드 및 스케일
title_image = load_and_scale_image(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_cover/Cover_The_Artistic_Invasion_Bright_1210x718.JPG", (1280, 720))

stage_images = [
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage1_World_A.JPG",
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage1_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage2_World_A.JPG",
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage2_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage3_World_A.JPG",
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage3_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage4_World_A.JPG",
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage4_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage5_World_A.JPG",
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage5_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage6_World_A.JPG",
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage6_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage7_World_A.JPG",
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage7_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage8_World_A.JPG",
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage8_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage9_World_A.JPG",
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage9_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage10_World_A.JPG",
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage10_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage11_World_A.JPG",
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage11_World_B.JPG"),
    (r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage12_World_A.JPG",
     r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage12_World_B.JPG")
]

stage_intro_images = [load_and_scale_image(img[0], (1280, 720)) for img in stage_images]
stage_background_images = [load_and_scale_image(img[1], (1280, 720)) for img in stage_images]

player_image1 = load_and_scale_image(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_me1_png.png", (40, 40))
player_image2 = load_and_scale_image(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_me2_png.png", (40, 40))

collision_images = {
    3: {"image": load_and_scale_image(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_death_1.png", (40, 40)), "duration": 5000},
    2: {"image": load_and_scale_image(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_death_2.png", (40, 40)), "duration": 5000},
    1: {"image": load_and_scale_image(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_death_3.png", (40, 40)), "duration": 5000}
}

health_image = load_and_scale_image(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_Life.png", (40, 40))
boss_image = load_and_scale_image(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/Mob_Boss_A.png", (120, 120))

victory_image = load_and_scale_image(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage14_Victory.JPG", (1280, 720))
game_over_image = load_and_scale_image(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage15_GameOver.JPG", (1280, 720))
time_over_image = load_and_scale_image(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_world/Stage16_TimeOver.JPG", (1280, 720))

enemy_images = {
    "up": load_and_scale_image(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_enemy_Relentless Charger_1.png", (40, 40)),
    "down": load_and_scale_image(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_enemy_Relentless Charger_2.png", (40, 40)),
    "left": load_and_scale_image(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_enemy_Relentless Charger_3.png", (40, 40)),
    "right": load_and_scale_image(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_enemy_Relentless Charger_4.png", (40, 40))
}

sentinel_shooter_right = load_and_scale_image(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_enemy_Sentinel Shooter_right.png", (40, 40))
sentinel_shooter_left = load_and_scale_image(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_enemy_Sentinel Shooter_left.png", (40, 40))

ambush_striker_up = load_and_scale_image(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_enemy_Ambush Striker_1.png", (40, 40))
ambush_striker_down = load_and_scale_image(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_enemy_Ambush Striker_2.png", (40, 40))
ambush_striker_left = load_and_scale_image(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_enemy_Ambush Striker_3.png", (40, 40))
ambush_striker_right = load_and_scale_image(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_enemy_Ambush Striker_4.png", (40, 40))

enemy_bomb_image = load_and_scale_image(r"C:/Users/HOME/Desktop/새싹_교육/GitHub_CHOI/project_4.2_Pixel Predators-The Artistic Invasion/project4.2_mob/mob_item_bomb.png", (40, 40))

# 게임 실행
game = Game()
game.run()
