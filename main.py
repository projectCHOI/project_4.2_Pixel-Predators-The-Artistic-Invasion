import pygame
import random
import math
import os
import sys

# 1. 분리된 모듈들 임포트
from M_title_stage_images.config import *
from M_title_stage_images.resource_manager import ResourceManager
from M_title_stage_images.game_manager import GameManager
from M_title_stage_images.entities.player import Player
from M_title_stage_images.assets.sounds.bgm_controller import BGMController