# project_4.2_Pixel-Predators-The-Artistic-Invasion
 
## project 4.2 주제 선정 이유
- 기존 project4의 개선 파이썬과 파이게임을 이용해 속도감 있는 2D 슈팅 게임을 제작했습니다.
- 빠른 반응과 전략적인 아이템 수집을 통해 10분 내외의 긴장감 넘치는 게임 경험을 제공 하는 것이 목표입니다.

## Tech Stack
- **Language**: Python
- **Game Library**: Pygame
- **IDE**: Visual Studio Code
- **Assets**
  - Images: `assets/images`
  - Sounds & BGM: `assets/sounds`
  - Fonts: `assets/fonts`

## Game Overview 
### 조작 방법
- 이동: `W A S D`
- 공격: **마우스 좌클릭**  
  - 플레이어 중심 → 마우스 위치 방향으로 공격 라인(투사체)이 이동
- 시작: 타이틀 화면에서 `Enter`
- 종료 화면:
  - 선택 이동: `A` (Main), `D` (Continue)
  - 선택 확정: `Space`

## Game Flow
1. **Title**
   - 게임 시작 대기 상태
2. **Stage Intro**
   - 스테이지 시작 전 인트로 이미지 출력
3. **Stage Play**
   - 일반 적 지속 스폰
   - 일정 시간 후 보스 등장
4. **Boss Battle**
   - 보스 패턴 + 특수 기믹 대응
5. **Clear / Game Over**
   - 보석 획득 시 다음 스테이지
   - Stage 9 클리어 시 Victory

## Core Systems
### 1. Main Loop Architecture (`main.py`)
- 게임 상태 관리
  - `title / loading / stage / gameover / victory`
- 스테이지 진행 및 레벨 관리 (Stage 1 ~ 9)
- 적 생성 및 제거
- 충돌 판정 (플레이어 ↔ 적 / 탄환)
- 아이템 처리
- 보스 연동 및 상태 전환
- BGM 상태 기반 자동 전환

`main.py`는 **게임 흐름 제어와 통합 관리**에 집중하며,  
적/보스의 세부 로직은 개별 모듈로 분리되어 있습니다.

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
또한 각 적 타입은 `enemy_spawn_intervals` 기반으로 **타입별 독립 쿨타임 생성**을 수행합니다.

---

### 2) 보스 시스템 (Stage 1 ~ Stage 9)
각 스테이지는 별도의 보스 클래스를 가지며, 보스는 다음과 같은 기능을 수행합니다.

- 등장 조건 체크: `boss.check_appear(total_seconds, level)`
- 이동: `boss.move()`
- 공격 생성/업데이트: `boss.attack()`, `boss.update_attacks(player_pos, invincible)`
- 피격 판정: `boss.check_hit(attacks)`
- 보석(클리어 아이템) 시스템: `boss.gem_active`, `boss.check_gem_collision(player_pos)`

추가로 일부 스테이지는 특수 효과가 존재합니다.
- Boss8: `boss.get_player_speed()`로 플레이어 속도에 영향
- Boss9: 입력 반전 상태(`is_input_reversed`) 지원

---
### 3) 아이템 시스템 (Speed / Power / Heal)

#### Speed Item
- 적 처치 시 확률적으로 드랍
- 획득 시 **일정 시간 동안 적 속도 감소**
- 지속시간: 20초

#### Power Item
- 공격력(공격 라인 수/확산)을 증가
- 최대 4단계까지 강화 (`power_item_active`)
## 코드의 구성
- 코드를 효율적으로 관리하기 위해 기능 분리

#### Heal Item
- HP가 최대치보다 낮을 때 확률적으로 드랍
- 획득 시 체력 1 회복

---
### 4) 충돌 / 무적 처리 (Damage & Invincibility)
- 플레이어 피격 시 `invincible_duration = 3000ms` 동안 무적
- 피격 시 체력 단계별 이미지 오버레이를 통해 시각적 피드백 제공
- 충돌 판정 종류:
  - 적 본체 충돌
  - 에너지볼(원형 탄) 충돌
  - bomb 파괴 시 생성되는 보라색 탄환(purple bullets) 충돌
  - 보스 미니언 및 미니언 공격 충돌

---
### 5) 사운드 / BGM 시스템
- `BGMController`를 통해 상태 기반 BGM 전환
  - `title`, `loading`, `stage_1` ... `stage_9`, `gameover`, `victory`
- 효과음:
  - `player_wound.wav` : 플레이어 피격
  - `Attack_sound.wav` : 플레이어 공격
  - `enemy_die.wav` : 일반 적 처치
  - `boom_die.wav` : bomb 적 처치
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
