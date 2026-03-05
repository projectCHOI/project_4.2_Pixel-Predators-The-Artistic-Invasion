# 플레이어 클래스
import pygame
from M_title_stage_images.config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, res_manager):
        super().__init__()
        self.res = res_manager
        
        # 이미지 로드 및 초기 설정
        self.size = (50, 50)
        self.img_right = self.res.load_image("player", "mob_me1_png.png", size=self.size)
        self.img_left = self.res.load_image("player", "mob_me2_png.png", size=self.size)
        
        # 충돌 시 이미지 (딕셔너리 형태로 관리 가능)
        self.collision_imgs = {
            3: self.res.load_image("player", "mob_death_1.png", size=self.size),
            2: self.res.load_image("player", "mob_death_2.png", size=self.size),
            1: self.res.load_image("player", "mob_death_3.png", size=self.size)
        }

        self.image = self.img_right
        self.rect = self.image.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
        
        # 상태 변수
        self.pos = list(self.rect.center)
        self.speed = 10
        self.health = PLAYER_START_HEALTH
        self.max_health = PLAYER_MAX_HEALTH
        
        # 무적 및 효과 관련
        self.invincible = False
        self.invincible_start_time = 0
        self.invincible_duration = INVINCIBLE_DURATION
        self.current_collision_img = None
        self.collision_effect_start_time = 0
        self.collision_effect_duration = 0

    def handle_input(self, input_reversed=False):
        keys = pygame.key.get_pressed()
        move_mult = -1 if input_reversed else 1
        dx, dy = 0, 0

        if keys[pygame.K_a]: dx -= self.speed * move_mult
        if keys[pygame.K_d]: dx += self.speed * move_mult
        if keys[pygame.K_w]: dy -= self.speed * move_mult
        if keys[pygame.K_s]: dy += self.speed * move_mult

        # 위치 업데이트 및 화면 밖 탈출 방지
        self.pos[0] = max(0, min(self.pos[0] + dx, WIN_WIDTH - self.size[0]))
        self.pos[1] = max(0, min(self.pos[1] + dy, WIN_HEIGHT - self.size[1]))
        self.rect.topleft = self.pos

        # 이미지 방향 전환
        if dx < 0: self.image = self.img_left
        elif dx > 0: self.image = self.img_right

    def take_damage(self, amount=1):
        if not self.invincible:
            self.health -= amount
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()
            
            # 충돌 효과 설정
            if self.health in self.collision_imgs:
                self.current_collision_img = self.collision_imgs[self.health]
                self.collision_effect_start_time = pygame.time.get_ticks()
                self.collision_effect_duration = 5000 # 5초 유지
            
            return True # 데미지 입음 성공
        return False
