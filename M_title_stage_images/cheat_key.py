# cheat_key.py
import pygame

# 디버그 모드 활성화 변수
debug_mode = False
input_code = ""

def handle_debug_mode(event, debug_mode, input_code, level, max_level, initialize_boss, intro_screen, game_active, current_health):
    # F12로 디버그 모드 활성화
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_F12:
            debug_mode = not debug_mode
            input_code = ""

        # 디버그 모드에서 숫자 입력 처리
        elif debug_mode and pygame.K_0 <= event.key <= pygame.K_9:
            input_code += chr(event.key)
            if len(input_code) == 3:  # 3자리 코드 입력 완료
                level = int(input_code)
                if 1 <= level <= max_level:
                    current_health = 10
                    boss = initialize_boss(level)
                    enemies = []
                    start_ticks = pygame.time.get_ticks()
                    game_active = True
                    intro_screen(level)
                input_code = ""
    return debug_mode, input_code, level, game_active, current_health
