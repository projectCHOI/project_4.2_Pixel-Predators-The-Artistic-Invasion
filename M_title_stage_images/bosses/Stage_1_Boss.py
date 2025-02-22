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

class Stage1Boss:
    def __init__(self):
        # ----- 보스 이미지 로드 -----
        self.boss_image_left = load_image("bosses", "boss_stage5_Left.png", size=(120, 120))
        self.boss_image_right = load_image("bosses", "boss_stage5_Right.png", size=(120, 120))
        self.boss_attack_image = load_image("boss_skilles", "boss_stage5_a.png", size=(40, 40))
        self.gem_image = load_image("items", "mob_Jewelry_5.png", size=(40, 40))

        # ----- 보스 기본 속성 -----
        self.max_boss_hp = 20       # 보스 최대 체력
        self.boss_hp = self.max_boss_hp
        self.boss_damage = 2        # 플레이어에게 주는 데미지 (충돌 시 등)
        self.boss_invincible_duration = 500  # 피격 무적 시간 (ms)
        self.boss_hit_duration = 100         # 피격 깜빡임 주기 (ms)
        self.side = random.choice(["left", "right"])

        if self.side == "left":
            self.boss_pos = [-100, 400]
            self.boss_image = self.boss_image_left
        else:
            self.boss_pos = [1380, 400]
            self.boss_image = self.boss_image_right

        self.boss_attacks = []      # 보스가 발사하는 에너지 볼 목록
        self.boss_active = False
        self.boss_appeared = False     
        self.boss_defeated = False  # 보스가 체력 0으로 사망했는지 여부
        self.gem_active = False     # 보스 사망 시 보석 드롭 후 활성화 여부
        self.gem_pos = None         # 보석 위치

        self.state = "appear"
        self.state_start_time = pygame.time.get_ticks()
        self.vertical_moves_done = 0
        self.going_forward = True 
        self.attack_cooldown = 1000 
        self.last_attack_time = 0
        self.boss_hit = False
        self.boss_hit_start_time = 0

    def check_appear(self, seconds, current_level):
        pass  # 현재는 따로 처리 안 함

    # 보스 이동 및 상태 전환
    def move(self):
        if self.boss_defeated:
            return

        current_time = pygame.time.get_ticks()
        time_in_state = current_time - self.state_start_time

        # 1) appear 상태
        if self.state == "appear":
            speed = 3
            if self.side == "left":
                self.boss_pos[0] += speed
                if self.boss_pos[0] >= 170:
                    self.boss_pos[0] = 170
                    self._change_state("wait1")
            else:
                self.boss_pos[0] -= speed
                if self.boss_pos[0] <= 1110:
                    self.boss_pos[0] = 1110
                    self._change_state("wait1")

        # 2) wait1 상태
        elif self.state == "wait1":
            if time_in_state >= 2000:  # 2초
                self._change_state("act")

        # 3) act(행동) 상태
        elif self.state == "act":
            if self.side == "left":
                self._move_left_side()  # 좌우 이동(왕복)
            else:
                self._move_right_side() # 상하 이동(5회 반복)

        # 4) wait2 상태
        elif self.state == "wait2":
            if time_in_state >= 2000:  # 2초
                self._change_state("leave")

        # 5) leave(퇴장) 상태
        elif self.state == "leave":
            speed = 6
            if self.side == "left":
                self.boss_pos[0] -= speed
                if self.boss_pos[0] <= -100:
                    self.boss_pos[0] = -100
                    self._change_state("wait3")
            else:
                self.boss_pos[0] += speed
                if self.boss_pos[0] >= 1380:
                    self.boss_pos[0] = 1380
                    self._change_state("wait3")

        elif self.state == "wait3":
            if time_in_state >= 2000:  # 2초
                self.reset(reinit_side=True)
                self._change_state("appear")

    # 행동(act) 상태에서의 이동 로직 분리
    def _move_left_side(self):
        current_time = pygame.time.get_ticks()
        self.attack()
        if self.going_forward:
            self.boss_pos[0] += 3
            if self.boss_pos[0] >= 820:
                self.boss_pos[0] = 820
                self.going_forward = False
        else:
            self.boss_pos[0] -= 5
            if self.boss_pos[0] <= 170:
                self.boss_pos[0] = 170
                self._change_state("wait2")

    def _move_right_side(self):
        self.attack()
        speed = 6
        target_up = 320
        target_down = 480

        y = self.boss_pos[1]
        moving_up = (self.vertical_moves_done % 2 == 0)  # 짝수 번째에는 위로 이동

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

        # 5회(위->아래가 1회) 반복 후 원점 복귀
        if self.vertical_moves_done >= 10:  # 위->아래 =1회로 계산하면 총 10번 도달
            if self.boss_pos[1] > 400:
                self.boss_pos[1] -= speed  # 위쪽으로 이동해서 400에 맞춤
                if self.boss_pos[1] <= 400:
                    self.boss_pos[1] = 400
                    self._change_state("wait2")
            elif self.boss_pos[1] < 400:
                self.boss_pos[1] += speed
                if self.boss_pos[1] >= 400:
                    self.boss_pos[1] = 400
                    self._change_state("wait2")
            else:
                self._change_state("wait2")

    # 보스 상태 전환을 간소화하는 헬퍼 함수
    def _change_state(self, new_state):
        self.state = new_state
        self.state_start_time = pygame.time.get_ticks()

    # 보스 공격
    def attack(self):
        if self.state != "act":
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = current_time

            # 발사 각도 설정
            if self.side == "left":
                angle_deg = 0   # 오른쪽 방향
            else:
                angle_deg = 180 # 왼쪽 방향

            rad = math.radians(angle_deg)
            dx = math.cos(rad) * 10
            dy = math.sin(rad) * 10

            # 보스 총알 생성 위치(보스 중앙 정도로 가정)
            # 이미지 크기가 120×120 이므로 대략 가운데 위치를 잡아줌
            start_x = self.boss_pos[0] + 60
            start_y = self.boss_pos[1] + 60

            self.boss_attacks.append({
                'pos': [start_x, start_y],
                'dir': [dx, dy],
                'angle': angle_deg
            })

    # 보스 에너지 볼 업데이트(이동 및 플레이어 충돌 체크)
    def update_attacks(self, player_pos):
        new_boss_attacks = []
        player_hit = False
        for attack in self.boss_attacks:
            # 에너지 볼 이동
            attack['pos'][0] += attack['dir'][0]
            attack['pos'][1] += attack['dir'][1]

            bx, by = attack['pos']
            # 화면 내부에 있으면 충돌 체크, 아니면 제거
            if 0 <= bx <= 1280 and 0 <= by <= 720:
                if self.check_energy_ball_collision((bx, by), player_pos):
                    player_hit = True  # 플레이어가 맞음
                else:
                    new_boss_attacks.append(attack)
        self.boss_attacks = new_boss_attacks
        return player_hit

    # 보스 그리기
    def draw(self, win):
        if not self.boss_defeated and self.boss_hp > 0:
            current_time = pygame.time.get_ticks()
            if self.boss_hit:
                # 피격 후 무적(깜빡임) 처리
                if current_time - self.boss_hit_start_time < self.boss_invincible_duration:
                    # 깜빡임: 깜빡임 주기(self.boss_hit_duration)에 따라 숨김/표시
                    if (current_time // self.boss_hit_duration) % 2 == 0:
                        win.blit(self.boss_image, self.boss_pos)
                else:
                    self.boss_hit = False
                    win.blit(self.boss_image, self.boss_pos)
            else:
                # 평상시 그대로 그림
                win.blit(self.boss_image, self.boss_pos)

    # 보스 발사체 그리기
    def draw_attacks(self, win):
        for attack in self.boss_attacks:
            angle = -attack['angle'] + 90  # 이미지 회전을 위해 각도 조정
            rotated_image = pygame.transform.rotate(self.boss_attack_image, angle)
            rect = rotated_image.get_rect(center=attack['pos'])
            win.blit(rotated_image, rect)

    # 보석 그리기
    def draw_gem(self, win):
        if self.gem_active and self.gem_pos:
            win.blit(self.gem_image, self.gem_pos)

    # 보스 체력 표시
    def draw_health_bar(self, win, font):
        if self.boss_active and not self.boss_defeated and self.boss_hp > 0:
            # "BOSS" 문자열
            boss_text = font.render("BOSS", True, (255, 255, 255))
            text_x = 10
            text_y = 680
            win.blit(boss_text, (text_x, text_y))

            # 체력 바
            health_bar_x = text_x + boss_text.get_width() + 10
            health_bar_y = 680
            health_bar_width = 200
            health_bar_height = 30

            # 체력 비율
            health_ratio = self.boss_hp / self.max_boss_hp
            current_health_width = int(health_bar_width * health_ratio)

            # 배경
            pygame.draw.rect(win, (50, 50, 50), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
            # 현재 체력
            pygame.draw.rect(win, (210, 20, 4), (health_bar_x, health_bar_y, current_health_width, health_bar_height))
            # 테두리
            pygame.draw.rect(win, (255, 255, 255), (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)
        elif self.boss_hp <= 0 and self.boss_defeated:
            # BOSS DEFEATED 메시지 (옵션)
            defeated_text = font.render("BOSS DEFEATED", True, (255, 255, 255))
            win.blit(defeated_text, (10, 680))

    # 보스 피격 처리
    def check_hit(self, attacks):
        current_time = pygame.time.get_ticks()

        # 이미 무적 상태면 공격 무시
        if self.boss_hit and (current_time - self.boss_hit_start_time) < self.boss_invincible_duration:
            return

        for attack in attacks:
            attack_start, attack_end, thickness = attack
            if self.check_attack_collision(attack_start, attack_end, self.boss_pos, 120):
                self.boss_hp -= 1
                if self.boss_hp < 0:
                    self.boss_hp = 0

                self.boss_hit = True
                self.boss_hit_start_time = current_time

                if self.boss_hp <= 0:
                    # 사망 처리
                    self.boss_defeated = True
                    self.boss_active = False
                    self.boss_attacks.clear()
                    self.gem_pos = [self.boss_pos[0] + 40, self.boss_pos[1] + 40]
                    self.gem_active = True
                break

    # 플레이어가 보석을 주웠는지 체크
    def check_gem_collision(self, player_pos):
        """
        보스 사망 후 드롭된 보석을 플레이어가 획득하면 True 반환
        """
        if self.gem_active and self.gem_pos:
            px, py = player_pos
            gx, gy = self.gem_pos
            player_width, player_height = 50, 50
            gem_size = 40
            if px < gx + gem_size and px + player_width > gx and py < gy + gem_size and py + player_height > gy:
                self.gem_active = False
                return True
        return False

    # 보스 상태/데이터 리셋
    def reset(self, reinit_side=False):
        if self.boss_defeated:
            return  # 이미 사망했다면 재등장 없음

        self.boss_hp = self.max_boss_hp
        self.boss_hit = False
        self.boss_hit_start_time = 0
        self.boss_attacks.clear()

        # side 다시 랜덤
        if reinit_side:
            self.side = random.choice(["left", "right"])

        # 위치도 초기화
        if self.side == "left":
            self.boss_pos = [-100, 400]
            self.boss_image = self.boss_image_left
        else:
            self.boss_pos = [1380, 400]
            self.boss_image = self.boss_image_right

        # 오른쪽 행동 로직 변수를 리셋
        self.vertical_moves_done = 0
        self.going_forward = True

        self.gem_active = False
        self.gem_pos = None
        self.boss_active = True

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
        ex2, ey2 = ex + boss_size, ey + boss_size

        rect = pygame.Rect(ex, ey, boss_size, boss_size)
        line = (sx, sy), attack_end
        if rect.clipline(line):
            return True
        return False
