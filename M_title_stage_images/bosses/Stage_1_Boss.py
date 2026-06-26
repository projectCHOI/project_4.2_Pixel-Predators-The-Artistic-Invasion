# M_title_stage_images/bosses/Stage_1_Boss.py
import pygame
import os
import math
from M_title_stage_images.config import *

class Stage1Boss:
    def __init__(self, res_manager):
        self.res = res_manager

        # 이미지 로드 (ResourceManager 활용 구조로 전면 통일)
        self.boss_image = self.res.load_image("bosses", "boss_stage1.png", size=(140, 140))
        self.boss_attack_image = self.res.load_image("boss_skilles", "boss_stage1_a.png", size=(40, 40))
        self.gem_image = self.res.load_image("items", "mob_Jewelry_1.png", size=(40, 40))

        # 보스 기본 속성
        self.boss_appear_time = 10     # 보스 등장 조건 (스테이지 타이머 기준 10초)
        self.max_boss_hp = 15
        self.boss_hp = self.max_boss_hp
        self.boss_damage = 1           # main.py 라이프 시스템과 밸런스를 맞추기 위해 1로 조절
        self.boss_speed = 6
        self.boss_pos = [640 - 70, 0]  # 중앙 정렬 (140 크기의 절반)
        
        self.boss_direction_x = 1
        self.boss_direction_y = 1
        
        self.boss_active = False       # 현재 전투 활성화 상태
        self.boss_defeated = False     # 쓰러졌는지 여부
        self.boss_appeared = False     # 이 스테이지에서 한번이라도 나왔었는지 체크
        self.boss_move_phase = 1       # 이동 패턴 단계
        
        # 피격 및 무적 관리
        self.boss_hit = False
        self.boss_hit_start_time = 0
        self.boss_hit_duration = 100
        self.boss_invincible_duration = 200 # 쾌적한 피격을 위해 무적 프레임 최적화밀리초

        # 탄막 제어
        self.boss_attacks = []
        self.boss_attack_cooldown = 1000
        self.boss_last_attack_time = 0

        # 클리어 키 아이템 보석 변수
        self.gem_pos = None
        self.gem_active = False
        self.stage_cleared = False

    def check_appear(self, seconds, current_level):
        """매 초 타이머와 레벨을 체크하여 보스 활성화"""
        if current_level == 1 and not self.boss_active and seconds >= self.boss_appear_time and not self.boss_appeared:
            self.boss_active = True
            self.boss_pos = [640 - 70, 20]
            self.boss_hp = self.max_boss_hp
            self.boss_move_phase = 2
            self.boss_appeared = True

    def move(self):
        """보스 페이즈별 이동 패턴 알고리즘"""
        if not self.boss_active or self.boss_hp <= 0:
            return

        def limit_position():
            self.boss_pos[0] = max(0, min(self.boss_pos[0], WIN_WIDTH - 140))
            self.boss_pos[1] = max(0, min(self.boss_pos[1], WIN_HEIGHT - 350))

        if self.boss_move_phase == 2:
            # Phase 2: 좌우로만 왕복 이동
            self.boss_pos[0] += self.boss_speed * self.boss_direction_x
            if self.boss_pos[0] <= 0 or self.boss_pos[0] >= WIN_WIDTH - 140:
                self.boss_direction_x *= -1

            # 체력이 50% 이하가 되면 대각선 광폭 이동 시작
            if self.boss_hp <= self.max_boss_hp * 0.5:
                self.boss_move_phase = 3

        elif self.boss_move_phase == 3:
            # Phase 3: 좌우 상하 사방 바운스 이동
            self.boss_pos[0] += self.boss_speed * self.boss_direction_x
            self.boss_pos[1] += self.boss_speed * self.boss_direction_y
            if self.boss_pos[0] <= 0 or self.boss_pos[0] >= WIN_WIDTH - 140:
                self.boss_direction_x *= -1
            if self.boss_pos[1] <= 0 or self.boss_pos[1] >= WIN_HEIGHT - 350:
                self.boss_direction_y *= -1

        limit_position()

    def attack(self):
        """체력 잔량별 부채꼴 탄막 제어 알고리즘"""
        if not self.boss_active or self.boss_hp <= 0:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.boss_last_attack_time > self.boss_attack_cooldown:
            self.boss_last_attack_time = current_time
            attack_angles = []

            # 보스 잔여 체력 비례 탄환 가닥수 계산
            if self.boss_hp > self.max_boss_hp * 0.75:
                attack_angles = [90]  # 1발 수직 하강
            elif self.boss_hp > self.max_boss_hp * 0.5:
                attack_angles = [85, 90, 95]  # 3발 산탄
            elif self.boss_hp > self.max_boss_hp * 0.25:
                attack_angles = [80, 85, 90, 95, 100]  # 5발 산탄
            else:
                attack_angles = [75, 80, 85, 90, 95, 100, 105]  # 7발 일제 광폭 사격

            # 보스의 아래쪽 중앙에서 발사 위치 정렬
            attack_start_pos = [self.boss_pos[0] + 70, self.boss_pos[1] + 120]

            for angle in attack_angles:
                radian = math.radians(angle)
                dx = math.cos(radian) * 8  # 탄속 8 최적화
                dy = math.sin(radian) * 8
                self.boss_attacks.append({
                    'pos': [attack_start_pos[0], attack_start_pos[1]],
                    'dir': [dx, dy],
                    'angle': angle
                })

    def update_attacks(self, player_rect, is_invincible=False):
        """보스 공격 탄환 업데이트 및 플레이어 충돌 구동부"""
        new_boss_attacks = []
        player_hit = False

        for attack in self.boss_attacks:
            attack['pos'][0] += attack['dir'][0]
            attack['pos'][1] += attack['dir'][1]
            bx, by = attack['pos']
            
            # 화면 범위 유효성 검사
            if -50 <= bx <= WIN_WIDTH + 50 and -50 <= by <= WIN_HEIGHT + 50:
                # 보스 탄환 충돌용 가상 Rect (사이즈 25x25 가정)
                bullet_rect = pygame.Rect(bx - 12, by - 12, 25, 25)
                
                if not is_invincible and bullet_rect.colliderect(player_rect):
                    player_hit = True # 플레이어 적중
                else:
                    new_boss_attacks.append(attack)

        self.boss_attacks = new_boss_attacks
        return self.boss_damage if player_hit else 0

    def check_hit(self, player_bullets_group):
        """[중요교정] main.py의 EnergyBall 스프라이트 그룹과 보스 본체의 충돌 정밀 처리"""
        if not self.boss_active or self.boss_hp <= 0:
            return

        current_time = pygame.time.get_ticks()
        # 무적 타이밍이면 피격 연산 생략
        if self.boss_hit and (current_time - self.boss_hit_start_time) < self.boss_invincible_duration:
            return

        self.boss_hit = False
        boss_rect = pygame.Rect(self.boss_pos[0], self.boss_pos[1], 140, 140)

        # 플레이어 탄환 그룹 순회 체크
        for bullet in player_bullets_group:
            if boss_rect.colliderect(bullet.rect):
                bullet.kill() # 적중한 플레이어 에너지볼 소멸
                self.boss_hp -= 1
                self.boss_hit = True
                self.boss_hit_start_time = current_time
                
                # 보스 격침 이벤트 처리
                if self.boss_hp <= 0:
                    self.boss_hp = 0
                    self.boss_active = False
                    self.boss_defeated = True
                    self.gem_pos = [self.boss_pos[0] + 50, self.boss_pos[1] + 50] # 보석 드롭
                    self.gem_active = True
                break

    def check_gem_collision(self, player_rect):
        """드롭된 클리어 보석과 플레이어의 충돌 처리"""
        if self.gem_active:
            gem_rect = pygame.Rect(self.gem_pos[0], self.gem_pos[1], 40, 40)
            if gem_rect.colliderect(player_rect):
                self.gem_active = False
                self.stage_cleared = True
                return True
        return False

    def draw(self, win):
        """보스 기체 렌더링 (피격 시 깜빡임 이펙트 구현)"""
        if self.boss_active and self.boss_hp > 0:
            current_time = pygame.time.get_ticks()
            if self.boss_hit:
                if (current_time // self.boss_hit_duration) % 2 == 0:
                    win.blit(self.boss_image, self.boss_pos)
            else:
                win.blit(self.boss_image, self.boss_pos)

    def draw_attacks(self, win):
        """보스 탄환 렌더링 및 각도 회전 매핑"""
        for attack in self.boss_attacks:
            angle = -attack['angle'] + 90
            rotated_image = pygame.transform.rotate(self.boss_attack_image, angle)
            rect = rotated_image.get_rect(center=attack['pos'])
            win.blit(rotated_image, rect)

    def draw_gem(self, win):
        if self.gem_active:
            win.blit(self.gem_image, self.gem_pos)

    def draw_health_bar(self, win):
        """[화면 하단] 보스 전용 HP Gauge UI 바 렌더링"""
        if self.boss_active and self.boss_hp > 0:
            font = pygame.font.SysFont("arial", 20, bold=True)
            boss_text = font.render("BOSS LV.1", True, (255, 255, 255))
            
            # 하단 정중앙 배치를 위한 좌표 연산
            bar_width = 600
            bar_height = 20
            bar_x = (WIN_WIDTH // 2) - (bar_width // 2)
            bar_y = WIN_HEIGHT - 80
            
            win.blit(boss_text, (bar_x, bar_y - 25))

            # 체력 비율 계산 및 바 드로잉
            health_ratio = self.boss_hp / self.max_boss_hp
            current_health_width = int(bar_width * health_ratio)

            # 배경블록(어두운 회색) -> 체력게이지(선명한 빨간색) -> 아웃라인 테두리(흰색)
            pygame.draw.rect(win, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(win, (230, 20, 20), (bar_x, bar_y, current_health_width, bar_height))
            pygame.draw.rect(win, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

    def reset(self):
        self.boss_active = False
        self.boss_hp = self.max_boss_hp
        self.boss_pos = [640 - 70, 0]
        self.boss_defeated = False
        self.boss_appeared = False
        self.boss_attacks = []
        self.gem_active = False
        self.gem_pos = None
        self.boss_move_phase = 1
        self.boss_hit = False
        self.stage_cleared = False
