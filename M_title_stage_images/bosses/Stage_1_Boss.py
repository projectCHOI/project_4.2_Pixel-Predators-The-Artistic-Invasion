# M_title_stage_images/bosses/stage1_boss.py
import pygame
import os
import math
from M_title_stage_images.config import *

class Stage1Boss:
    def __init__(self, res_manager):
        # [교정] main.py의 자원 관리 시스템(res_manager)을 사용하여 일원화 및 경로 에러 방지
        self.res = res_manager
        
        # 이미지 로드 규격 최적화
        self.boss_image = self.res.load_image("bosses", "boss_stage1.png", size=(140, 140))
        self.boss_attack_image = self.res.load_image("boss_skilles", "boss_stage1_a.png", size=(40, 40))
        self.gem_image = self.res.load_image("items", "mob_Jewelry_1.png", size=(40, 40))

        # 보스 속성 설정
        self.boss_appear_time = 10     # 보스 등장 조건: 타이머 10초 이상일 때
        self.max_boss_hp = 15          # 최대 체력
        self.boss_hp = self.max_boss_hp
        self.boss_damage = 1           # 밸런스를 위해 데미지를 라이프 1칸 감소로 조정
        self.boss_speed = 6
        self.boss_pos = [640 - 70, 20] # (화면 중앙 상단 배치)
        self.boss_direction_x = 1
        self.boss_direction_y = 1
        
        # 상태 제어 스위치
        self.boss_active = False       
        self.boss_defeated = False     
        self.boss_appeared = False     
        self.boss_move_phase = 1       
        self.boss_hit = False          
        self.boss_hit_start_time = 0   
        self.boss_hit_duration = 100   
        self.boss_attacks = []         
        self.boss_attack_cooldown = 1000 
        self.boss_last_attack_time = 0 
        
        # 클리어 보석 설정
        self.gem_pos = None            
        self.gem_active = False        
        self.stage_cleared = False     
        self.boss_invincible_duration = 500 

        # 미니언 확장 슬롯 (유지)
        self.minions = []

    def spawn_minions(self): pass
    def update_minion_behavior(self): pass
    def update_minion_attacks(self): pass
    def draw_minion_attacks(self, win): pass    
    
    def check_appear(self, seconds, current_level):
        """매초 흐르는 시간과 현재 스테이지를 받아 조건 충족 시 보스 활성화"""
        if current_level == 1 and not self.boss_active and seconds >= self.boss_appear_time and not self.boss_appeared:
            self.boss_active = True
            self.boss_pos = [640 - 70, 20]
            self.boss_hp = self.max_boss_hp
            self.boss_move_phase = 2
            self.boss_appeared = True

    def move(self):
        """보스의 단계별 인공지능 이동 패턴"""
        def limit_position():
            self.boss_pos[0] = max(0, min(self.boss_pos[0], WIN_WIDTH - 140))
            self.boss_pos[1] = max(0, min(self.boss_pos[1], WIN_HEIGHT - 350)) # 플레이어 영역 확보를 위해 하한선 조절

        if self.boss_move_phase == 2:
            # Phase 2: 단순 좌우 왕복 이동
            self.boss_pos[0] += self.boss_speed * self.boss_direction_x
            if self.boss_pos[0] <= 0 or self.boss_pos[0] >= WIN_WIDTH - 140:
                self.boss_direction_x *= -1

            # 체력이 50% 이하로 떨어지면 대각선 상하좌우 난반사 이동으로 격상(Phase 3)
            if self.boss_hp <= self.max_boss_hp * 0.5:
                self.boss_move_phase = 3

        elif self.boss_move_phase == 3:
            # Phase 3: 전방위 폭주 기동
            self.boss_pos[0] += self.boss_speed * self.boss_direction_x
            self.boss_pos[1] += self.boss_speed * self.boss_direction_y
            if self.boss_pos[0] <= 0 or self.boss_pos[0] >= WIN_WIDTH - 140:
                self.boss_direction_x *= -1
            if self.boss_pos[1] <= 0 or self.boss_pos[1] >= WIN_HEIGHT - 350:
                self.boss_direction_y *= -1

        limit_position()

    def attack(self):
        """보스의 체력 연동형 다갈래 탄막 사격 함수"""
        current_time = pygame.time.get_ticks()
        if current_time - self.boss_last_attack_time > self.boss_attack_cooldown:
            self.boss_last_attack_time = current_time
            attack_angles = []

            # 보스의 잔여 HP 비율에 따라 탄환 개수 확장 (1 -> 3 -> 5 -> 7)
            if self.boss_hp > self.max_boss_hp * 0.75:
                attack_angles = [90]
            elif self.boss_hp > self.max_boss_hp * 0.5:
                attack_angles = [85, 90, 95]
            elif self.boss_hp > self.max_boss_hp * 0.25:
                attack_angles = [80, 85, 90, 95, 100]
            else:
                attack_angles = [75, 80, 85, 90, 95, 100, 105]

            # 보스 이미지 하단 중앙에서 탄환이 발사되도록 오프셋 수정
            attack_start_pos = [self.boss_pos[0] + 70, self.boss_pos[1] + 130]

            for angle in attack_angles:
                radian = math.radians(angle)
                dx = math.cos(radian) * 8  # 투사체 이동 속도
                dy = math.sin(radian) * 8
                self.boss_attacks.append({
                    'pos': [attack_start_pos[0], attack_start_pos[1]],
                    'dir': [dx, dy],
                    'angle': angle
                })

    def update_attacks(self, player_rect, is_invincible=False):
        """보스 탄환 이동 및 플레이어 기체와의 정밀 사각형 충돌 검사"""
        new_boss_attacks = []
        player_hit = False

        for attack in self.boss_attacks:
            attack['pos'][0] += attack['dir'][0]
            attack['pos'][1] += attack['dir'][1]
            bx, by = attack['pos']
            
            # 화면 범위 내에 있을 때만 탄환 유지
            if -50 <= bx <= WIN_WIDTH + 50 and -50 <= by <= WIN_HEIGHT + 50:
                # [교정] 점 충돌 대신 보스 총알 크기(40x40)를 반영한 Rect 충돌 판정으로 업그레이드
                bullet_rect = pygame.Rect(bx - 20, by - 20, 40, 40)
                if not is_invincible and bullet_rect.colliderect(player_rect):
                    player_hit = True
                else:
                    new_boss_attacks.append(attack)

        self.boss_attacks = new_boss_attacks
        return self.boss_damage if player_hit else 0

    def draw(self, win):
        """보스 본체 렌더링 (피격 시 무적 깜빡임 이펙트 내장)"""
        if self.boss_hp > 0:
            current_time = pygame.time.get_ticks()
            if self.boss_hit:
                if current_time - self.boss_hit_start_time >= self.boss_invincible_duration:
                    self.boss_hit = False
                    win.blit(self.boss_image, self.boss_pos)
                else:
                    if (current_time // self.boss_hit_duration) % 2 == 0:
                        win.blit(self.boss_image, self.boss_pos)
            else:
                win.blit(self.boss_image, self.boss_pos)

    def draw_attacks(self, win):
        """각도에 맞춰 회전된 보스 탄막 그리기"""
        for attack in self.boss_attacks:
            angle = -attack['angle'] + 90
            rotated_image = pygame.transform.rotate(self.boss_attack_image, angle)
            rect = rotated_image.get_rect(center=attack['pos'])
            win.blit(rotated_image, rect)

    def draw_gem(self, win):
        if self.gem_active:
            win.blit(self.gem_image, self.gem_pos)

    def draw_health_bar(self, win, font):
        """화면 하단에 시각적인 보스 대형 HP Bar 렌더링"""
        if self.boss_active and self.boss_hp > 0:
            boss_text = font.render("BOSS : STAGE 1", True, WHITE)
            text_x = 40
            text_y = WIN_HEIGHT - 100
            win.blit(boss_text, (text_x, text_y))

            health_bar_x = text_x
            health_bar_y = WIN_HEIGHT - 65
            health_bar_width = WIN_WIDTH - 80  # 화면 규격에 맞게 체력바 가로 확장
            health_bar_height = 20

            health_ratio = self.boss_hp / self.max_boss_hp
            current_health_width = int(health_bar_width * health_ratio)

            # 배경(어두운 회색) -> 체력(핏빛 빨간색) -> 테두리(흰색)
            pygame.draw.rect(win, (40, 40, 40), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
            pygame.draw.rect(win, (210, 20, 4), (health_bar_x, health_bar_y, current_health_width, health_bar_height))
            pygame.draw.rect(win, WHITE, (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)

    def check_hit(self, player_bullets):
        """[핵심 교정] 현재 아군의 Sprite 총알 그룹을 받아 보스 본체 Rect와의 충돌 검사 수행"""
        if not self.boss_active or self.boss_hp <= 0:
            return

        current_time = pygame.time.get_ticks()
        # 무적 타임 메커니즘 연동
        if self.boss_hit and (current_time - self.boss_hit_start_time) < self.boss_invincible_duration:
            return
        else:
            self.boss_hit = False

        boss_rect = pygame.Rect(self.boss_pos[0], self.boss_pos[1], 140, 140)
        
        # 아군 에너지볼 중 보스 몸체와 부딪힌 녀석이 있는지 검사
        for bullet in player_bullets:
            if boss_rect.colliderect(bullet.rect):
                bullet.kill() # 적중한 플레이어 총알 소멸
                self.boss_hp -= 1
                self.boss_hit = True
                self.boss_hit_start_time = current_time
                
                # 보스 파괴 판정 트리거
                if self.boss_hp <= 0:
                    self.boss_hp = 0
                    self.boss_active = False
                    self.boss_defeated = True
                    self.gem_pos = [self.boss_pos[0] + 50, self.boss_pos[1] + 50]
                    self.gem_active = True
                break

    def check_gem_collision(self, player_rect):
        """보석 습득 여부 체크"""
        if self.gem_active:
            gem_rect = pygame.Rect(self.gem_pos[0], self.gem_pos[1], 40, 40)
            if player_rect.colliderect(gem_rect):
                self.gem_active = False
                self.stage_cleared = True  
                return True
        return False

    def reset(self):
        self.boss_active = False
        self.boss_hp = self.max_boss_hp
        self.boss_pos = [640 - 70, 20]
        self.boss_defeated = False
        self.boss_appeared = False
        self.boss_attacks = []
        self.gem_active = False
        self.gem_pos = None
        self.boss_move_phase = 1
        self.boss_hit = False
        self.stage_cleared = False

    def draw_minions(self, win): pass
    def check_minion_collision(self, player_rect): return 0