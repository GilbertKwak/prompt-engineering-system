# decision-opt — 의사결정 최적화 프롬프트 디렉토리

## 개요

Operations Research + Decision Theory + Game Theory + MCDM 통합 엔진 기반의
전략적 의사결정 포트폴리오 프롬프트 모음.

## 파일 목록

| 파일 | ID | PE-3 | 역할 |
|---|---|---|---|
| `ADOA-SDP-MASTER-v1.0-OPT.md` | ADOA-SDP-MASTER-v1.0-OPT | 95+ | 9엔진 통합 지루 에이전트 |

## Notion 연계

- **C-23 PE-OPT (ADOA):** https://www.notion.so/35255ed436f0810f830be1feb1512c28
- **C-33 PE-STRAT:** STRAT-OS-MASTER 위임 수신 대상
- **PE-11 (C-06):** Multi-Agent 실행 위임
- **PE-3 (C-03):** 평가 루프

## 엔진 맵

```
E1 DecisionTree     → 순차 분기 + EV
E2 BEP_Risk         → 고정비/변동비 구조
E3 AHP              → 다기준 정성
E4 ANP              → 상호의존 복잡계
E5 GameTheory       → 경쟁·협상
E6 MarkovChain      → 상태전이 안정성
E7 MonteCarlo       → 분포 기반 리스크 (N≥1000)
E8 SensitivityWhatIf → 민감도·What-If
E9 GoalSeek         → 목표 역산
```

## 업데이트 이력

| 날짜 | 버전 | 변경 내용 |
|---|---|---|
| 2026-05-05 | v1.0-OPT | 디렉토리 신설 + ADOA-SDP-MASTER 최초 커밋 |
