# M_title_stage_images/entities/items.py
import pygame
import random
from M_title_stage_images.config import *

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, item_type, res_manager):
        super().__init__()
        self.res = res_manager
        self.type = item_type
        size = (30, 30)

        try:
            if self.type == 'heal':
                self.image = self.res.load_image("items", "mob_item_Life.png", size=size)
            elif self.type == 'power':
                self.image = self.res.load_image("items", "mob_item_Defense_2.png", size=size)
            elif self.type == 'speed':
                self.image = self.res.load_image("items", "mob_item_Quickly.png", size=size)
        except Exception as e:
            print(f"[경고] 아이템 이미지 로드 실패 ({self.type}): {e}")
            self.image = pygame.Surface(size, pygame.SRCALPHA)
            if self.type == 'heal':
                pygame.draw.circle(self.image, (0, 255, 0), (15, 15), 15)  # 녹색 원
            elif self.type == 'power':
                pygame.draw.circle(self.image, (255, 255, 0), (15, 15), 15) # 노란색 원
            elif self.type == 'speed':
                pygame.draw.circle(self.image, (0, 0, 255), (15, 15), 15)  # 파란색 원

        self.rect = self.image.get_rect(center=pos)
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > WIN_HEIGHT:
            self.kill()

    def apply_effect(self, player):
        if self.type == 'heal':
            if player.health < player.max_health:
                player.health += 1
                return "체력 회복!"
        elif self.type == 'power':
            # [수정] 최대 4단계까지 공격력 레벨 상승
            if player.power_level < player.max_power_level:
                player.power_level += 1
                return f"공격력 강화! (Level {player.power_level})"
            return "공격력 최대 치 도달!"
        elif self.type == 'speed':
            player.speed += 2
            return "이동 속도 증가!"
        return ""

def spawn_item_by_chance(pos, res_manager):
    rand_val = random.random()
    
    if rand_val < ITEM_CHANCE['speed']: # 0.1
        return Item(pos, 'speed', res_manager)
    elif rand_val < ITEM_CHANCE['speed'] + ITEM_CHANCE['power']: # 0.2
        return Item(pos, 'power', res_manager)
    elif rand_val < ITEM_CHANCE['speed'] + ITEM_CHANCE['power'] + ITEM_CHANCE['heal']: # 0.6
        return Item(pos, 'heal', res_manager)
    
    return None