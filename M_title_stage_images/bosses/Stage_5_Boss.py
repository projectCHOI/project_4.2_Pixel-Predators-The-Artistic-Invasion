import pygame
import os
import random
import math

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

class Stage5Boss:
    def __init__(self):
        # 이미지 로드 (총 4개 필요: 보스 이미지, 공격 이미지 3개, 경고 이미지)
        self.boss_image = load_image("bosses", "boss_stage5.png", size=(120, 120))
        self.boss_attack_images = {
            "high": load_image("boss_skilles", "boss_stage5_a.png", size=(40, 40)),
            "medium": load_image("boss_skilles", "boss_stage5_b.png", size=(40, 40)),
            "low": load_image("boss_skilles", "boss_stage5_c.png", size=(40, 40))
        }
        self.teleport_warning_image = load_image("stages", "Stage18_mist.png", size=(60, 60))
        self.gem_image = load_image("items", "mob_Jewelry_5.png", size=(40, 40))

        # 보스 속성 초기화
        self.max_boss_hp = 15
        self.boss_hp = self.max_boss_hp
        self.boss_pos = [640 - 60, 360 - 60]  # 화면 정중앙
        self.boss_active = False
        self.boss_appeared = False
        self.invincible = False  # 무적 상태 여부
        self.invincible_start_time = 0  # 무적 상태 시작 시간
        self.invincible_duration = 10000  # 무적 상태 지속 시간 (10초)
        self.boss_attacks = []
        self.boss_last_attack_time = 0
        self.attack_interval = 1000
        self.teleport_interval = 4000
        self.last_teleport_time = 0
        self.gem_pos = None
        self.gem_active = False
        self.boss_defeated = False
        self.stage_cleared = False

    # 상태 확인 및 갱신 메서드
    def check_appear(self, seconds, current_level):
        if current_level == 5 and not self.boss_active and seconds >= 10 and not self.boss_appeared:
            self.boss_active = True
            self.boss_hp = self.max_boss_hp
            self.boss_appeared = True
            self.invincible = True  # 출연 시 무적 상태 활성화
            self.invincible_start_time = pygame.time.get_ticks()  # 무적 상태 시작 시간 기록

    def update_invincibility(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.invincible_start_time >= self.invincible_duration:
                self.invincible = False  # 무적 상태 해제

    def update_attacks(self, player_pos):
        new_attacks = []
        player_hit = False
        for attack in self.boss_attacks:
            # 공격 위치 업데이트
            attack[0][0] += attack[1][0]  # x 좌표 업데이트
            attack[0][1] += attack[1][1]  # y 좌표 업데이트

            # 공격이 화면 안에 있는지 확인
            if 0 <= attack[0][0] <= 1280 and 0 <= attack[0][1] <= 720:
                # 플레이어와 충돌 확인
                if self.check_energy_ball_collision(attack[0], player_pos):
                    player_hit = True  # 플레이어가 공격에 맞음
                else:
                    new_attacks.append(attack)
        self.boss_attacks = new_attacks
        return player_hit

    # 상태 변화 메서드
    def move(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_teleport_time > self.teleport_interval:
            # 텔레포트 경고 표시
            self.show_teleport_warning(current_time)

            # 랜덤한 위치로 텔레포트
            self.boss_pos = [random.randint(0, 1280 - 120), random.randint(0, 720 - 120)]
            self.last_teleport_time = current_time
            # 텔레포트 후 공격
            self.attack()

    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.boss_last_attack_time > self.attack_interval:
            self.boss_last_attack_time = current_time
            num_shots = 3 + (self.max_boss_hp - self.boss_hp) // 3  # 체력 감소 시 공격 횟수 증가
            for i in range(num_shots):
                angle = random.uniform(0, 360)
                radian = math.radians(angle)
                dx = math.cos(radian) * 5
                dy = math.sin(radian) * 5
                attack_type = self.get_attack_type()
                self.boss_attacks.append([self.boss_pos[:], [dx, dy], angle, attack_type])

    def get_attack_type(self):
        """
        보스의 체력 상태에 따라 공격 유형을 반환합니다.
        """
        health_ratio = self.boss_hp / self.max_boss_hp
        if health_ratio > 0.6:
            return "high"
        elif health_ratio > 0.3:
            return "medium"
        else:
            return "low"

    def reset(self):
        self.boss_active = False
        self.boss_hp = self.max_boss_hp
        self.boss_pos = [640 - 120, 0]
        self.boss_defeated = False
        self.boss_appeared = False
        self.boss_attacks = []
        self.gem_active = False
        self.gem_pos = None
        self.invincible = False
        self.stage_cleared = False

    # 충돌 및 상태 확인 메서드
    def check_hit(self, attacks):
        self.update_invincibility()  # 무적 상태 업데이트

        if self.invincible:
            # 무적 상태일 때는 공격을 무시
            return

        for attack in attacks:
            attack_start, attack_end, thickness = attack
            if self.check_attack_collision(attack_start, attack_end, self.boss_pos, 120):
                self.boss_hp -= 1  # 데미지 적용
                if self.boss_hp <= 0:
                    self.boss_hp = 0
                    self.boss_active = False
                break  # 한 번에 하나의 공격만 처리

    def check_attack_collision(self, attack_start, attack_end, boss_pos, boss_size):
        ex, ey = boss_pos
        sx, sy = attack_start
        rect = pygame.Rect(ex, ey, boss_size, boss_size)
        line = (sx, sy), attack_end
        if rect.clipline(line):
            return True
        return False

    def check_energy_ball_collision(self, ball_pos, player_pos):
        bx, by = ball_pos
        px, py = player_pos
        player_width, player_height = 50, 50  # 플레이어 크기
        if px < bx < px + player_width and py < by < player_height:
            return True
        return False

    # 렌더링 메서드
    def draw(self, win):
        """
        보스 이미지를 화면에 그리는 메서드
        """
        if self.boss_hp > 0:  # 보스가 체력을 잃지 않은 경우
            if self.invincible:  # 무적 상태일 때 깜박임 효과
                current_time = pygame.time.get_ticks()
                if (current_time // 200) % 2 == 0:  # 200ms 간격으로 깜박임
                    return  # 이미지를 그리지 않음 (깜박임 효과)
            win.blit(self.boss_image, self.boss_pos)  # 보스 이미지를 화면에 표시

    def show_teleport_warning(self, current_time):
        # 텔레포트 전에 경고 이미지를 보여주는 로직
        warning_time = 500  # 500ms 동안 경고
        if current_time - self.last_teleport_time < warning_time:
            warning_pos = [self.boss_pos[0] + 30, self.boss_pos[1] + 30]  # 보스 위치에 경고 이미지 표시
            # win.blit(self.teleport_warning_image, warning_pos)  # 실제 화면에 표시할 때 사용
