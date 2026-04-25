import pygame
import sys

# --- 1. 외부 모듈 임포트 ---
try:
    from M_title_stage_images.config import *
    from M_title_stage_images.resource_manager import ResourceManager
    from M_title_stage_images.game_manager import GameManager
    from M_title_stage_images.title_stage_images import title_image, stage_background_images
    # 플레이어 클래스 추가
    from M_title_stage_images.entities.player import Player
    
    print("플레이어를 포함한 모든 시스템 연결 완료.")
except ImportError as e:
    print(f"연결 오류 발생: {e}")
    sys.exit()

def main():
    # 2. 초기화
    pygame.init()
    pygame.mixer.init()
    
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("The Artistic Invasion")
    clock = pygame.time.Clock()

    # 3. 객체 생성
    res = ResourceManager()
    manager = GameManager(res)
    # 플레이어는 일단 None으로 설정 후 게임 시작 시 생성
    player = None

    # 메인 루프
    run = True
    while run:
        # --- A. 이벤트 처리 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if not manager.game_active:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # 게임 시작 시 플레이어 초기화
                    player = Player(res)
                    manager.start_game()
                    print("게임 시작! 플레이어 생성 완료.")

        # --- B. 게임 로직 ---
        if manager.game_active and player:
            # 1. 플레이어 입력 처리 (보스의 입력 반전 효과 등은 추후 manager 연동)
            player.handle_input(input_reversed=False)
            
            # 2. 플레이어 상태 업데이트 (무적 시간 등)
            player.update()
            
            # 3. 게임 매니저 업데이트 (플레이어 체력 체크 등)
            manager.update(player)

        # --- C. 화면 그리기 ---
        if not manager.game_active:
            if manager.game_over:
                win.fill(BLACK)
                font = pygame.font.SysFont("malgungothic", 50)
                msg = "MISSION COMPLETE" if manager.game_over_reason == "victory" else "GAME OVER"
                text = font.render(msg, True, YELLOW if msg == "MISSION COMPLETE" else RED)
                win.blit(text, (WIN_WIDTH // 2 - 200, WIN_HEIGHT // 2 - 50))
                
                retry_text = font.render("Press ENTER to Restart", True, WHITE)
                win.blit(retry_text, (WIN_WIDTH // 2 - 250, WIN_HEIGHT // 2 + 50))
            else:
                win.blit(title_image, (0, 0))
        
        else:
            # 배경 그리기
            bg_idx = manager.level - 1
            if bg_idx < len(stage_background_images):
                win.blit(stage_background_images[bg_idx], (0, 0))
            
            # 플레이어 그리기
            player.draw(win)

            # 간단 UI (체력 및 레벨)
            font = pygame.font.SysFont("arial", 30)
            ui_text = font.render(f"STAGE {manager.level}  |  LIFE: {player.health}", True, WHITE)
            win.blit(ui_text, (20, 20))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

