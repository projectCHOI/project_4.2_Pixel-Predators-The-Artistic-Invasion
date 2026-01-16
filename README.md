# project_4.2_Pixel-Predators-The-Artistic-Invasion
 
## project 4.2 주제 선정 이유
- 기존 project4의 개선 
- 파이썬과 파이게임을 이용해 속도감 있는 2D 슈팅 게임을 제작했습니다.
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

### 2. Boss System (Example: Stage 9)
각 스테이지는 독립된 보스 클래스를 가지고 있습니다.
#### 보스 설계 특징
- 클래스 단위 분리 (Stage1Boss ~ Stage9Boss)
- 상태 머신 기반 이동 패턴
- 공격 / 피격 / 무적 / 클리어(보석) 로직 캡슐화
#### Stage 9 핵심 기믹
- 유도형 보스 탄환 피격 시:
  - **플레이어 입력 반전 디버프 5초 적용**
- 미니언 소환 + 탄막 패턴 병행
- 보스 처치 후 보석 획득 시 게임 최종 클리어

#### 보스 책임 분리
- `check_appear()` : 등장 조건
- `move()` : 이동 패턴
- `attack()` / `update_attacks()` : 공격 및 디버프
- `spawn_minions()` / `update_minion_behavior()` : 미니언 관리
- `check_hit()` : 피격 판정
- `check_gem_collision()` : 스테이지 클리어

---
## Enemy Behaviors (`enemy_behaviors`)

적 AI는 모두 모듈 단위로 분리되어 있으며,  
`main.py`는 스테이지 레벨에 따라 적을 조합하여 사용합니다.

### 공통 구조
- 모든 적은 `generate()` 함수로 생성
- 리스트 기반 데이터 구조 사용
- `enemy_type` 문자열로 행동 분기

---
### Enemy Types
#### 1) move_and_disappear
- 직선 돌진 후 화면 밖으로 이탈
- 기본 전투 밀도 유지용 적
- 대량 스폰으로 회피 압박 제공
---
#### 2) move_and_shoot
- 목표 지점까지 이동 후 정지
- 일정 주기로 사격
- 플레이어 이동 경로 차단 역할
---
#### 3) approach_and_shoot
- 플레이어에게 접근 후 일정 거리 유지
- 유도형 탄환 발사
- 10초 주기 패턴:
  - 전반: 접근 + 공격
  - 후반: 퇴장
---
#### 4) bomb
- 플레이어를 향해 고속 돌진
- 처치 시 **8방향 보라색 파편 탄 생성**
- 처치 이후에도 위험 요소 유지
---
#### 5) group_unit
- 1 Front + 4 Back 유닛 구성
- 사인파 이동 기반 편대 행동
- Front: 8방향 공격
- Back: 좌/우 공격
- 지속적인 탄막 밀도 형성

---
## Item System
### Speed Item
- 적 처치 시 확률 드랍
- 일정 시간 동안 **모든 적 속도 감소**
### Power Item
- 공격 라인 확장
- 최대 4단계 강화
### Heal Item
- 체력 회복 아이템
- 체력 최대치 미만일 때만 획득 가능

---
## Damage & Invincibility
- 피격 시:
  - 체력 감소
  - 3초 무적 상태 적용
  - 체력 단계별 피격 이미지 출력
- 충돌 유형:
  - 적 본체
  - 에너지 탄
  - 폭탄 파편
  - 보스 미니언 및 미니언 공격