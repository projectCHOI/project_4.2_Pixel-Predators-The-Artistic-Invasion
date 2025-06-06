# #Stage_2_Boss Back-up
# #Stage_2_Boss Back-up
# import pygame
# import os
# import math
# import random

# # BASE_DIR 설정: 현재 파일의 부모 디렉토리 기준으로 설정
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_IMAGE_PATH = os.path.join(BASE_DIR, "assets", "images")

# def load_image(*path_parts, size=None):
#     path = os.path.join(BASE_IMAGE_PATH, *path_parts)
#     try:
#         image = pygame.image.load(path).convert_alpha()
#     except pygame.error as e:
#         raise SystemExit(f"Cannot load image: {path}\n{e}")
#     if size:
#         image = pygame.transform.scale(image, size)
#     return image

# class Stage2Boss:
#     def __init__(self):
#         # 이미지 로드
#         self.boss_image = load_image("bosses", "boss_stage2.png", size=(240, 240))
#         self.boss_attack_images = {
#             "down": load_image("boss_skilles", "boss_stage2_a.png", size=(40, 40)),
#             "up": load_image("boss_skilles", "boss_stage2_b.png", size=(40, 40)),
#             "right": load_image("boss_skilles", "boss_stage2_c.png", size=(40, 40)),
#             "left": load_image("boss_skilles", "boss_stage2_d.png", size=(40, 40))
#         }
#         self.gem_image = load_image("items", "mob_Jewelry_2.png", size=(40, 40))
#         # 보스 속성 초기화
#         self.boss_appear_time = 10  # 보스 등장 시간 (초)
#         self.max_boss_hp = 20  # 보스의 최대 체력
#         self.boss_hp = self.max_boss_hp  # 현재 보스 체력
#         self.boss_damage = 2  # 보스의 공격력
#         self.boss_speed = 7  # 보스의 이동 속도
#         self.boss_pos = [640 - 60, 0]  # 보스의 초기 위치
#         self.boss_direction_x = 1  # 보스의 좌우 이동 방향
#         self.boss_direction_y = 1  # 보스의 상하 이동 방향
#         self.boss_active = False  # 보스 활성화 상태
#         self.boss_defeated = False  # 보스 패배 상태
#         self.boss_appeared = False  # 보스가 이미 등장했는지 여부
#         self.boss_move_phase = 1  # 보스의 이동 단계
#         self.boss_hit = False  # 보스 피격 상태
#         self.boss_hit_start_time = 0  # 보스 피격 시점
#         self.boss_hit_duration = 100  # 보스 피격 효과 지속 시간 (밀리초)
#         self.boss_attacks = []  # 보스의 공격 리스트
#         self.boss_attack_cooldown = 1000  # 보스 공격 간격 (밀리초)
#         self.boss_last_attack_time = 0  # 마지막 공격 시점
#         self.gem_pos = None  # 보석의 위치
#         self.gem_active = False  # 보석 활성화 상태
#         self.stage_cleared = False  # 스테이지 클리어 여부
#         self.boss_invincible_duration = 500  # 무적 상태 지속 시간(밀리초)

#     def check_appear(self, seconds, current_level):
#         if current_level == 2 and not self.boss_active and seconds >= self.boss_appear_time and not self.boss_appeared:
#             # 보스 등장 시 초기화
#             self.boss_active = True
#             self.boss_pos = [640 - 60, 0]
#             self.boss_hp = self.max_boss_hp
#             self.boss_appeared = True  # 보스가 등장했음을 표시
#             self.gem_active = False  # 보석을 비활성화 상태로 초기화
#             self.gem_pos = None
#             self.boss_defeated = False  # 보스가 등장하면 패배 상태를 False로 설정
#             self.stage_cleared = False

#     def move(self):
#         # 이동 후 위치 제한 함수 추가
#         def limit_position():
#             self.boss_pos[0] = max(0, min(self.boss_pos[0], 1280 - 120))
#             self.boss_pos[1] = max(0, min(self.boss_pos[1], 720 - 120))

#         if self.boss_move_phase == 1:
#             # 중앙으로 이동
#             target_pos = [640 - 60, 360 - 60]
#             direction = [target_pos[0] - self.boss_pos[0], target_pos[1] - self.boss_pos[1]]
#             length = math.hypot(direction[0], direction[1])
#             if length > self.boss_speed:
#                 direction = [direction[0] / length, direction[1] / length]
#                 self.boss_pos[0] += direction[0] * self.boss_speed
#                 self.boss_pos[1] += direction[1] * self.boss_speed
#             else:
#                 self.boss_pos = target_pos
#                 self.boss_move_phase = 2
#         elif self.boss_move_phase == 2:
#             # 좌우 이동
#             self.boss_pos[0] += self.boss_speed * self.boss_direction_x
#             if self.boss_pos[0] <= 0 or self.boss_pos[0] >= 1280 - 120:
#                 self.boss_direction_x *= -1  # 방향 전환
#             if self.boss_hp <= self.max_boss_hp / 2:
#                 self.boss_move_phase = 3
#         elif self.boss_move_phase == 3:
#             # 좌우 및 상하 이동
#             self.boss_pos[0] += self.boss_speed * self.boss_direction_x
#             self.boss_pos[1] += self.boss_speed * self.boss_direction_y
#             if self.boss_pos[0] <= 0 or self.boss_pos[0] >= 1280 - 120:
#                 self.boss_direction_x *= -1  # 좌우 방향 전환
#             if self.boss_pos[1] <= 0 or self.boss_pos[1] >= 720 - 120:
#                 self.boss_direction_y *= -1  # 상하 방향 전환

#         # 위치 제한 적용
#         limit_position()

#     def attack(self):
#         current_time = pygame.time.get_ticks()
#         if current_time - self.boss_last_attack_time > self.boss_attack_cooldown:
#             self.boss_last_attack_time = current_time
#             possible_directions = []

#             # 보스의 체력에 따른 공격 방향 설정
#             if self.boss_hp > self.max_boss_hp * 0.75:
#                 possible_directions = ["down"]
#             elif self.boss_hp > self.max_boss_hp * 0.5:
#                 possible_directions = ["down", "up"]
#             elif self.boss_hp > self.max_boss_hp * 0.25:
#                 possible_directions = ["down", "up", "right"]
#             else:
#                 possible_directions = ["down", "up", "right", "left"]

#             attack_direction = random.choice(possible_directions)
#             attack_start_pos = self.get_attack_start_pos(attack_direction)
#             self.boss_attacks.append([attack_start_pos[0], attack_start_pos[1], attack_direction])

#     def get_attack_start_pos(self, direction):
#         if direction == "down":
#             return [self.boss_pos[0] + 100, self.boss_pos[1] + 240]
#         elif direction == "up":
#             return [self.boss_pos[0] + 100, self.boss_pos[1]]
#         elif direction == "right":
#             return [self.boss_pos[0] + 240, self.boss_pos[1] + 100]
#         elif direction == "left":
#             return [self.boss_pos[0], self.boss_pos[1] + 100]

#     def update_attacks(self, player_pos):
#         new_boss_attacks = []
#         player_hit = False
#         for attack in self.boss_attacks:
#             if attack[2] == "down":
#                 attack[1] += 10
#             elif attack[2] == "up":
#                 attack[1] -= 10
#             elif attack[2] == "right":
#                 attack[0] += 10
#             elif attack[2] == "left":
#                 attack[0] -= 10

#             if 0 <= attack[0] <= 1280 and 0 <= attack[1] <= 720:
#                 if self.check_energy_ball_collision((attack[0], attack[1]), player_pos):
#                     player_hit = True  # 플레이어에게 맞음
#                 else:
#                     new_boss_attacks.append(attack)
#             else:
#                 pass  # 공격이 화면 밖으로 나가면 제거
#         self.boss_attacks = new_boss_attacks
#         return player_hit

#     def draw(self, win):
#         if self.boss_hp > 0:
#             current_time = pygame.time.get_ticks()
#             if self.boss_hit:
#                 if current_time - self.boss_hit_start_time >= self.boss_invincible_duration:
#                     self.boss_hit = False  # 무적 상태 및 깜박임 종료
#                     win.blit(self.boss_image, self.boss_pos)
#                 else:
#                     # 깜박임 효과
#                     if (current_time // self.boss_hit_duration) % 2 == 0:
#                         win.blit(self.boss_image, self.boss_pos)
#             else:
#                 win.blit(self.boss_image, self.boss_pos)

#     def draw_attacks(self, win):
#         for attack in self.boss_attacks:
#             win.blit(self.boss_attack_images[attack[2]], (attack[0], attack[1]))

#     def draw_gem(self, win):
#         if self.gem_active:
#             win.blit(self.gem_image, self.gem_pos)

#     def draw_health_bar(self, win, font):
#         if self.boss_active and self.boss_hp > 0:
#             # "BOSS" 문자열 그리기
#             boss_text = font.render("BOSS", True, (255, 255, 255))
#             text_x = 10
#             text_y = 680
#             win.blit(boss_text, (text_x, text_y))

#             # 체력 바 설정
#             health_bar_x = text_x + boss_text.get_width() + 10
#             health_bar_y = 680
#             health_bar_width = 200  # 체력 바의 총 너비를 200으로 설정
#             health_bar_height = 30

#             # 체력 비율 계산
#             health_ratio = self.boss_hp / self.max_boss_hp
#             current_health_width = int(health_bar_width * health_ratio)

#             # 체력 바 배경 그리기
#             pygame.draw.rect(win, (50, 50, 50), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

#             # 현재 체력 바 그리기
#             pygame.draw.rect(win, (210, 20, 4), (health_bar_x, health_bar_y, current_health_width, health_bar_height))

#             # 체력 바 테두리 그리기
#             pygame.draw.rect(win, (255, 255, 255), (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)
#         elif self.boss_hp <= 0 and self.boss_defeated:
#             # 보스가 제거되었을 때 메시지 표시 (옵션)
#             defeated_text = font.render("BOSS DEFEATED", True, (255, 255, 255))
#             win.blit(defeated_text, (10, 680))

#     def check_hit(self, attacks):
#         current_time = pygame.time.get_ticks()
#         if self.boss_hit and (current_time - self.boss_hit_start_time) < self.boss_invincible_duration:
#             # 보스가 무적 상태일 때는 공격을 무시합니다.
#             return
#         else:
#             self.boss_hit = False  # 무적 상태 해제

#         for attack in attacks:
#             attack_start, attack_end, thickness = attack
#             if self.check_attack_collision(attack_start, attack_end, self.boss_pos, 240):
#                 self.boss_hp -= 1  # 데미지 적용
#                 if self.boss_hp < 0:
#                     self.boss_hp = 0  # 체력이 음수가 되지 않도록
#                 self.boss_hit = True  # 보스가 공격을 받았음을 표시
#                 self.boss_hit_start_time = current_time  # 공격 받은 시간 기록
#                 if self.boss_hp <= 0:
#                     self.boss_active = False
#                     self.boss_defeated = True  # 보스가 패배했음을 표시
#                     self.gem_pos = [self.boss_pos[0] + 95, self.boss_pos[1] + 95]
#                     self.gem_active = True
#                 break  # 한 번에 하나의 공격만 처리

#     def check_gem_collision(self, player_pos):
#         if self.gem_active:
#             px, py = player_pos
#             gx, gy = self.gem_pos
#             player_width, player_height = 40, 40  # 플레이어 크기
#             gem_size = 40  # 보석 크기
#             if px < gx + gem_size and px + player_width > gx and py < gy + gem_size and py + player_height > gy:
#                 self.gem_active = False
#                 self.stage_cleared = True  # 스테이지 클리어
#                 return True
#         return False

#     def reset(self):
#         # 보스 초기화 로직 추가
#         self.boss_active = False
#         self.boss_hp = self.max_boss_hp
#         self.boss_pos = [640 - 120, 0]
#         self.boss_defeated = False
#         self.boss_appeared = False  # 보스 등장 여부 재설정
#         self.boss_attacks = []
#         self.gem_active = False  # 보석 비활성화
#         self.gem_pos = None
#         self.boss_move_phase = 1
#         self.boss_hit = False
#         self.stage_cleared = False
#         if hasattr(self, 'phase_start_time'):
#             del self.phase_start_time  # 단계 시작 시간 초기화

#     def check_energy_ball_collision(self, ball_pos, player_pos):
#         bx, by = ball_pos
#         px, py = player_pos
#         player_width, player_height = 50, 50  # 플레이어 크기
#         if px < bx < px + player_width and py < by < py + player_height:
#             return True
#         return False

#     def check_attack_collision(self, attack_start, attack_end, boss_pos, boss_size):
#         ex, ey = boss_pos
#         sx, sy = attack_start
#         ex2, ey2 = ex + boss_size, ey + boss_size

#         # 공격 선분과 보스 사각형의 충돌 검사
#         rect = pygame.Rect(ex, ey, boss_size, boss_size)
#         line = (sx, sy), attack_end
#         if rect.clipline(line):
#             return True
#         return False

# #Stage_4_Boss Back-up
# #Stage_4_Boss Back-up
# import pygame
# import os
# import math
# import random

# # BASE_DIR 설정: 현재 파일의 부모 디렉토리 기준으로 설정
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_IMAGE_PATH = os.path.join(BASE_DIR, "assets", "images")

# def load_image(*path_parts, size=None):
#     path = os.path.join(BASE_IMAGE_PATH, *path_parts)
#     try:
#         image = pygame.image.load(path).convert_alpha()
#     except pygame.error as e:
#         raise SystemExit(f"Cannot load image: {path}\n{e}")
#     if size:
#         image = pygame.transform.scale(image, size)
#     return image

# class Stage4Boss:
#     def __init__(self):
#         # 이미지 로드
#         self.screen_center = [640, 360]
#         self.boss_image = load_image("bosses", "boss_stage4.png", size=(120, 120))
#         self.boss_attack_images = {
#             "down": load_image("boss_skilles", "boss_stage4_a.png", size=(40, 40)),
#             "up": load_image("boss_skilles", "boss_stage4_b.png", size=(40, 40)),
#             "right": load_image("boss_skilles", "boss_stage4_c.png", size=(40, 40)),
#             "left": load_image("boss_skilles", "boss_stage4_d.png", size=(40, 40))
#         }
#         self.gem_image = load_image("items", "mob_Jewelry_4.png", size=(40, 40))

#         # 보스 속성 초기화
#         self.boss_appear_time = 10  # 보스 등장 시간 (초)
#         self.max_boss_hp = 10  # 보스의 최대 체력
#         self.boss_hp = self.max_boss_hp  # 현재 보스 체력
#         self.boss_damage = 2  # 보스의 공격력
#         self.boss_speed = 3  # 보스의 이동 속도
#         self.boss_pos = [640 - 60, 300 - 60]  # 보스의 초기 위치 (화면 중앙)
#         self.boss_direction_x = 1  # 보스의 좌우 이동 방향
#         self.boss_active = False  # 보스 활성화 상태
#         self.boss_defeated = False  # 보스 패배 상태
#         self.boss_appeared = False  # 보스가 이미 등장했는지 여부
#         self.boss_move_phase = 2  # 보스의 이동 단계 (바로 원형 운동 시작)
#         self.boss_hit = False  # 보스 피격 상태
#         self.boss_hit_start_time = 0  # 보스 피격 시점
#         self.boss_hit_duration = 100  # 보스 피격 효과 지속 시간 (밀리초)
#         self.boss_attacks = []  # 보스의 공격 리스트
#         self.boss_attack_cooldown = 1000  # 보스 공격 간격 (밀리초)
#         self.boss_last_attack_time = 0  # 마지막 공격 시점
#         self.gem_pos = None  # 보석의 위치
#         self.gem_active = False  # 보석 활성화 상태
#         self.stage_cleared = False  # 스테이지 클리어 여부
#         self.boss_invincible_duration = 500  # 무적 상태 지속 시간(밀리초)
#         self.angle = 0  # 원 운동을 위한 초기 각도
#         self.radius = 100  # 원 운동 반지름
#         self.radius_change_direction = 1  # 반지름 증가/감소 방향
#         self.radius_change_speed = 0.2  # 반지름 변화 속도

#     def check_appear(self, seconds, current_level):
#         if current_level == 4 and not self.boss_active and seconds >= self.boss_appear_time and not self.boss_appeared:
#             self.boss_active = True
#             self.boss_pos = [640 - 60, 300 - 60]
#             self.boss_hp = self.max_boss_hp
#             self.boss_appeared = True  # 보스가 등장했음을 표시

#     def move(self):
#         if self.boss_move_phase == 2:
#             # 화면 중앙을 기준으로 원 운동 시작
#             if self.boss_hp > self.max_boss_hp * 0.6:
#                 self.angle += 0.05
#             elif self.boss_hp > self.max_boss_hp * 0.3:
#                 self.angle += 0.07
#             else:
#                 self.angle += 0.09

#             # 반지름 동적 변화
#             self.radius += self.radius_change_direction * self.radius_change_speed
#             if self.radius >= 150 or self.radius <= 50:  # 반지름의 범위 제한
#                 self.radius_change_direction *= -1

#             self.boss_pos[0] = 640 - 60 + self.radius * math.cos(self.angle)
#             self.boss_pos[1] = 360 - 60 + self.radius * math.sin(self.angle)

#     def attack(self):
#         current_time = pygame.time.get_ticks()
#         if current_time - self.boss_last_attack_time >= self.boss_attack_cooldown:
#             # 보스의 총알을 나선형으로 발사
#             bullets = 5  # 총알 개수
#             angle_offset = 0
#             angle_increase = 360 / bullets

#             for i in range(bullets):
#                 angle = math.radians(angle_offset + i * angle_increase)
#                 dx = math.cos(angle) * 3 # 총알 속도(기본은 5)
#                 dy = math.sin(angle) * 3 # 총알 속도(낮으면 느려짐)
#                 self.boss_attacks.append({
#                     'pos': self.boss_pos[:],
#                     'dir': [dx, dy],
#                     'angle': angle_offset + i * angle_increase
#                 })

#             # 체력이 줄어들수록 더 자주 발사
#             self.boss_attack_cooldown = max(200, 3000 - (self.max_boss_hp - self.boss_hp) * 80)
#             self.boss_last_attack_time = current_time

#     def update_attacks(self, player_pos):
#         new_boss_attacks = []
#         player_hit = False
#         for attack in self.boss_attacks:
#             # 에너지 볼 이동
#             attack['pos'][0] += attack['dir'][0]
#             attack['pos'][1] += attack['dir'][1]

#             bx, by = attack['pos']
#             if 0 <= bx <= 1280 and 0 <= by <= 720:
#                 if self.check_energy_ball_collision((bx, by), player_pos):
#                     player_hit = True  # 플레이어에게 맞음
#                 else:
#                     new_boss_attacks.append(attack)
#             # 화면 밖으로 나가면 공격 제거
#         self.boss_attacks = new_boss_attacks
#         return player_hit

#     def draw(self, win):
#         if self.boss_hp > 0:
#             current_time = pygame.time.get_ticks()
#             if self.boss_hit:
#                 if current_time - self.boss_hit_start_time >= self.boss_invincible_duration:
#                     self.boss_hit = False  # 무적 상태 및 깜박임 종료
#                     win.blit(self.boss_image, self.boss_pos)
#                 else:
#                     # 깜박임 효과
#                     if (current_time // self.boss_hit_duration) % 2 == 0:
#                         win.blit(self.boss_image, self.boss_pos)
#             else:
#                 win.blit(self.boss_image, self.boss_pos)

#     def draw_attacks(self, win):
#         for attack in self.boss_attacks:
#             angle = -attack['angle'] + 90  # 이미지 회전을 위해 각도 조정
#             direction = 'down'  # 기본 방향을 'down'으로 설정하거나 다른 조건에 따라 변경 가능
#             rotated_image = pygame.transform.rotate(self.boss_attack_images[direction], angle)
#             rect = rotated_image.get_rect(center=attack['pos'])
#             win.blit(rotated_image, rect)

#     def draw_gem(self, win):
#         if self.gem_active:
#             win.blit(self.gem_image, self.gem_pos)

#     def draw_health_bar(self, win, font):
#         if self.boss_active and self.boss_hp > 0:
#             # "BOSS" 문자열 그리기
#             boss_text = font.render("BOSS", True, (255, 255, 255))
#             text_x = 10
#             text_y = 680
#             win.blit(boss_text, (text_x, text_y))

#             # 체력 바 설정
#             health_bar_x = text_x + boss_text.get_width() + 10
#             health_bar_y = 680
#             health_bar_width = 200  # 체력 바의 총 너비를 200으로 설정
#             health_bar_height = 30

#             # 체력 비율 계산
#             health_ratio = self.boss_hp / self.max_boss_hp
#             current_health_width = int(health_bar_width * health_ratio)

#             # 체력 바 배경 그리기
#             pygame.draw.rect(win, (50, 50, 50), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

#             # 현재 체력 바 그리기
#             pygame.draw.rect(win, (210, 20, 4), (health_bar_x, health_bar_y, current_health_width, health_bar_height))

#             # 체력 바 테두리 그리기
#             pygame.draw.rect(win, (255, 255, 255), (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)
#         elif self.boss_hp <= 0 and self.boss_defeated:
#             # 보스가 제거되었을 때 메시지 표시 (옵션)
#             defeated_text = font.render("BOSS DEFEATED", True, (255, 255, 255))
#             win.blit(defeated_text, (10, 680))

#     def check_hit(self, attacks):
#         current_time = pygame.time.get_ticks()
#         if self.boss_hit and (current_time - self.boss_hit_start_time) < self.boss_invincible_duration:
#             # 보스가 무적 상태일 때는 공격을 무시합니다.
#             return
#         else:
#             self.boss_hit = False  # 무적 상태 해제

#         for attack in attacks:
#             attack_start, attack_end, thickness = attack
#             if self.check_attack_collision(attack_start, attack_end, self.boss_pos, 120):
#                 self.boss_hp -= 1  # 데미지 적용
#                 if self.boss_hp < 0:
#                     self.boss_hp = 0  # 체력이 음수가 되지 않도록
#                 self.boss_hit = True  # 보스가 공격을 받았음을 표시
#                 self.boss_hit_start_time = current_time  # 공격 받은 시간 기록
#                 if self.boss_hp <= 0:
#                     self.boss_active = False
#                     self.gem_pos = [self.boss_pos[0] + 100, self.boss_pos[1] + 100]
#                     self.gem_active = True
#                     self.boss_defeated = True
#                 break  # 한 번에 하나의 공격만 처리

#     def check_gem_collision(self, player_pos):
#         if self.gem_active:
#             px, py = player_pos
#             gx, gy = self.gem_pos
#             player_width, player_height = 40, 40  # 플레이어 크기
#             gem_size = 40  # 보석 크기
#             if px < gx + gem_size and px + player_width > gx and py < gy + gem_size and py + player_height > gy:
#                 self.gem_active = False
#                 self.stage_cleared = True  # 스테이지 클리어
#                 return True
#         return False

#     def reset(self):
#         self.boss_active = False
#         self.boss_hp = self.max_boss_hp
#         self.boss_pos = [640 - 60, 300 - 60]
#         self.boss_defeated = False
#         self.boss_appeared = False  # 보스 등장 여부 재설정
#         self.boss_attacks = []
#         self.gem_active = False
#         self.gem_pos = None
#         self.boss_move_phase = 2
#         self.boss_hit = False
#         self.stage_cleared = False

#     def check_energy_ball_collision(self, ball_pos, player_pos):
#         bx, by = ball_pos
#         px, py = player_pos
#         player_width, player_height = 50, 50  # 플레이어 크기
#         if px < bx < px + player_width and py < by < py + player_height:
#             return True
#         return False

#     def check_attack_collision(self, attack_start, attack_end, boss_pos, boss_size):
#         ex, ey = boss_pos
#         sx, sy = attack_start
#         ex2, ey2 = ex + boss_size, ey + boss_size

#         # 공격 선분과 보스 사각형의 충돌 검사
#         rect = pygame.Rect(ex, ey, boss_size, boss_size)
#         line = (sx, sy), attack_end
#         if rect.clipline(line):
#             return True
#         return False
