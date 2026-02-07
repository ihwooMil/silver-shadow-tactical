# 기획서: Project Silver-Shadow (슬더스류)

## 1. 개요
- **장르:** 중세 판타지 덱 빌딩 로그라이크
- **플랫폼:** Web (GitHub Pages 배포 타겟)
- **개발 환경:** Godot 4.2.1 (Compatibility 모드)

## 2. 핵심 메커니즘
- **Active Time Battle (Timebar):** 유닛별 Speed에 따라 타임라인이 전진하며 100% 도달 시 턴 획득.
- **다대다 전투:** 플레이어 팀과 적 팀의 팀 단위 교전.
- **카드 시스템:** 코스트 기반 카드 사용 (Strike, Defend, Bash 등).
- **에셋 활용:** `erin.jpg`, `isabel.jpg`, `lawrence.jpg` 등을 유닛 스프라이트로 활용.

## 3. 구조적 문제점 (현재)
- iOS 웹 브라우저에서 초기 씬 로드 실패 (무한 로딩/회전).
- 씬 전환 및 리소스 로딩 방식의 비동기 처리 부족 가능성.

---

# 기획서: Project Wall & Abyss (디펜스오펜스)

## 1. 개요
- **장르:** 디펜스 + 던전 탐험 하이브리드
- **플랫폼:** Web (GitHub Pages 배포 타겟)
- **개발 환경:** Godot 4.2.1 (Compatibility 모드)

## 2. 핵심 메커니즘
- **Phase Cycle:** 준비(Prep) -> 방어(Defense) -> 준비(Prep) -> 공격(Attack).
- **성벽(Wall) 시스템:** 체력을 가진 성벽을 방어하고 수리.
- **탐험:** 방을 이동하며 자원 획득 및 적 조우.

## 3. 구조적 문제점 (현재)
- iOS 웹 브라우저에서 초기 씬 로드 실패 (무한 로딩/회전).
- Autoload(GameManager)와 UI 초기화 순서 사이의 의존성 문제 가능성.
