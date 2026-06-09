# M_title_stage_images/entities/bullets.py
import pygame
import math
from M_title_stage_images.config import *

class Bullet(pygame.sprite.Sprite):
    """마우스 클릭 방향으로 날아가는 일반 탄환 (도형 방식)"""
    def __init__(self, pos, color, target_pos):
        super().__init__()
        self.radius = 5
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=pos)
        
        self.speed = 15
        
        mx, my = target_pos
        px, py = pos
        angle = math.atan2(my - py, mx - px)
        
        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if (self.rect.bottom < 0 or self.rect.top > WIN_HEIGHT or 
            self.rect.right < 0 or self.rect.left > WIN_WIDTH):
            self.kill()


class EnergyBall(pygame.sprite.Sprite):
    """마우스 클릭 방향으로 날아가는 푸른색 에너지볼 (부채꼴 오프셋 지원)"""
    # 🔍 핵심 교정: angle_offset=0 이 부분이 반드시 존재해야 main.py의 요청을 받을 수 있습니다.
    def __init__(self, pos, res_manager, target_pos, angle_offset=0):
        super().__init__()
        self.res = res_manager # 기존 코드 호환성 유지용
        
        # 반지름 크기 (원하는 대로 조절 가능)
        self.radius = 12 
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        
        # 외곽 푸른빛 투명 구체 + 내부 하얀색 코어 겹쳐 그리기
        pygame.draw.circle(self.image, (0, 191, 255, 150), (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.image, (255, 255, 255, 255), (self.radius, self.radius), self.radius - 5)
        
        self.rect = self.image.get_rect(center=pos)
        self.speed = 12
        
        mx, my = target_pos
        px, py = pos
        # 마우스 커서와의 기준 각도 구하기 (라디안 단위)
        base_angle = math.atan2(my - py, mx - px)
        
        # 기준 각도에 main.py에서 넘겨받은 부채꼴 오프셋 각도(라디안 변환)를 더해줍니다.
        final_angle = base_angle + math.radians(angle_offset)
        
        self.vx = math.cos(final_angle) * self.speed
        self.vy = math.sin(final_angle) * self.speed
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if (self.rect.bottom < 0 or self.rect.top > WIN_HEIGHT or 
            self.rect.right < 0 or self.rect.left > WIN_WIDTH):
            self.kill()