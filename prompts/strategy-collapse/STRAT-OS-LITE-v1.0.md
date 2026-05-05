---
id: STRAT-OS-LITE-v1.0
pe3_score: 93
version: v1.0
created: 2026-05-05
parent: STRAT-OS-MASTER-v1.0-OPT
---

# STRAT-OS-LITE-v1.0
## 투자위원회 전략 OS — Lite (속보·브리핑용, PE-3: 93)

> MASTER의 경량 파생 — 3-병목·단일 World·CEO 5줄 출력

---

## 입력
```
SECTOR          [required]
FOCUS_ENTITY    [required]
WORLD_ASSUMPTION [required] WorldA|WorldB|WorldC|WorldD
```

## 병목 체인 (3개 고정)
```
C1_Technology     → 핵심 병목 1개 + 비가역성
C2_Infrastructure → 전력·DC 대기 타임라인
C5_Policy         → 보조금 집행률 vs 기업수익성 갭
```

## 충돌 탐지
```
CF-01 + CF-02 의무 탐지
충돌 없으면 분석 무효
```

## 출력
```
O1: World 가정 (1줄)
O2: 3대 병목 요약 (3줄)
O3: 핵심 충돌 1개 + 강도
O4: P1(구조수혜) / P3(구조리스크) 2분류
O5: 투자 권고 (확대/축소/보류) + 근거 3줄 + "왜 지금?"
```

## 자동 검증
- World 가정 없음 → 재작성
- 충돌 탐지 없음 → 재작성
- 권고 없음 → 재작성

---
*STRAT-OS-LITE v1.0 | 2026-05-05*
