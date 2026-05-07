# M_title_stage_images/entities/player.py
import pygame
from M_title_stage_images.config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, res_manager):
        super().__init__()
        self.res = res_manager
        
        # 1. 이미지 로드 및 초기 설정
        self.size = (50, 50)
        self.img_right = self.res.load_image("player", "mob_me1_png.png", size=self.size)
        self.img_left = self.res.load_image("player", "mob_me2_png.png", size=self.size)
        
        # [추가] UI용 라이프 이미지 로드
        self.life_icon = self.res.load_image("player", "mob_Life.png", size=(30, 30))
        
        # 충돌 시 이미지
        self.collision_imgs = {
            3: self.res.load_image("player", "mob_death_1.png", size=self.size),
            2: self.res.load_image("player", "mob_death_2.png", size=self.size),
            1: self.res.load_image("player", "mob_death_3.png", size=self.size)
        }

        self.image = self.img_right
        self.rect = self.image.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
        
        # 상태 변수
        self.pos = [float(self.rect.x), float(self.rect.y)]
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
        self.rect.topleft = (int(self.pos[0]), int(self.pos[1]))

        # 이미지 방향 전환
        if dx < 0: self.image = self.img_left
        elif dx > 0: self.image = self.img_right

    def take_damage(self, amount=1):
        if not self.invincible:
            self.health -= amount
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()
            
            if self.health in self.collision_imgs:
                self.current_collision_img = self.collision_imgs[self.health]
                self.collision_effect_start_time = pygame.time.get_ticks()
                self.collision_effect_duration = 5000 
            
            return True 
        return False
    
    def update(self):
        now = pygame.time.get_ticks()
        if self.invincible and now - self.invincible_start_time > self.invincible_duration:
            self.invincible = False
        if self.current_collision_img and now - self.collision_effect_start_time >= self.collision_effect_duration:
            self.current_collision_img = None

    def draw(self, screen):
        if self.invincible and (pygame.time.get_ticks() // 200) % 2 == 0:
            pass 
        else:
            screen.blit(self.image, self.rect)
        
        if self.current_collision_img:
            screen.blit(self.current_collision_img, self.rect)

    def draw_ui(self, screen):
        for i in range(max(0, self.health)):
            # x: 20px부터 50px 간격, y: 하단에서 50px 위
            screen.blit(self.life_icon, (20 + (i * 50), WIN_HEIGHT - 50))