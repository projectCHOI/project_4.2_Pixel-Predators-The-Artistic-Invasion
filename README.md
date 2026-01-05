# project_4.2_Pixel-Predators-The-Artistic-Invasion
 
## project 4.2 주제 선정 이유
- 기존 project4의 개선 파이썬과 파이게임을 이용해 속도감 있는 2D 슈팅 게임을 제작했습니다.
- 빠른 반응과 전략적인 아이템 수집을 통해 10분 내외의 긴장감 넘치는 게임 경험을 제공 하는 것이 목표입니다.

## Tech Stack 
- **Language**: Python
- **Game Library**: Pygame
- **IDE/Tooling**: VSCode (또는 Python 실행 환경)
- **Assets**
  - Images: `M_title_stage_images/assets/images`
  - Sounds/BGM: `M_title_stage_images/assets/sounds`
  - Fonts: `M_title_stage_images/assets/fonts`

## Game Overview 
### 조작 방법
- 이동: `W A S D`
- 공격: **마우스 좌클릭**  
  - 플레이어 중심 → 마우스 위치 방향으로 공격 라인(투사체)이 이동
- 시작: 타이틀 화면에서 `Enter`
- 종료 화면:
  - 선택 이동: `A` (Main), `D` (Continue)
  - 선택 확정: `Space`

### 진행 방식
- 총 **Stage 1 ~ Stage 9**
- 스테이지마다 일반 적이 지속적으로 생성되며, 일정 시간이 지나면 **보스가 등장**
- 보스 처치 후 등장하는 **보석(Gem)** 을 획득하면 다음 스테이지로 진행
- Stage 9 클리어 시 `Victory`

### 게임 종료 조건
- **Game Over**: 체력(HP)이 0이 되면 종료
- **Victory**: Stage 9 클리어 시 종료
- (구현상 `time_over` 이미지 리소스는 준비되어 있으나, main.py 기준 시간 종료 판정은 확장 여지가 있음)

---

## Features
### 1) 스테이지별 적 조합 (Dynamic Enemy Composition)
스테이지에 따라 서로 다른 적 생성 모듈을 조합하여 난이도와 패턴을 변화시킵니다.

- `move_and_disappear`
- `move_and_shoot`
- `approach_and_shoot`
- `group_unit`
- `bomb`  

스테이지별 구성(요약):
- Stage 1: move_and_disappear
- Stage 2~3: move_and_disappear + move_and_shoot + bomb
- Stage 4: move_and_disappear + move_and_shoot + group_unit
- Stage 5: Stage4 + bomb
- Stage 6: move_and_disappear + move_and_shoot + group_unit
- Stage 7: Stage6 + bomb
- Stage 8: Stage6
- Stage 9: Stage6 + bomb
## 코드의 구성
- 코드를 효율적으로 관리하기 위해 기능 분리

### 메인코드 기능 "main"

### 보스코드 기능

### 유닛코드 기능

### 지원코드 기능

## 음악 제작 코드
- 음악 제작의도 :
-  
-
### 외부 음악 제작
- Drum Pad Machine ver2.24.1을 사용하여 무료 비트를 제작하여 사용.

## 개선할 점
- 테스트

## 시각화
- PPT
