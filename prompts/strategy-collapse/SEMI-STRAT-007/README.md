# SEMI-STRAT-007 · StrategicMonitoringAgent v5.4

> C-33 PE-STRAT 라이브러리 | 2026-05-02 신규 등록 | Notion_007 쿼리 기반 생성 · 3-Engine 검증 완료

## 개요

| 항목 | 값 |
|------|----|
| 프롬프트 ID (Master) | SEMI-STRAT-007-v1.0-OPT |
| 프롬프트 ID (Variant-A) | SEMI-STRAT-007-v1.0-KR |
| 프롬프트 ID (Variant-B) | SEMI-STRAT-007-v1.0-GLOBAL |
| PE-3 점수 | Master **97** / KR **95** / GLOBAL **94** |
| Temperature | 0.0 |
| World 커버리지 | A/B/C/D 전체 (국가 파라미터 교체형) |
| 생성 방식 | Notion_007 쿼리 기반 · 3-Engine 검증 완료 |
| 등록일 | 2026-05-02 |
| 관리자 | Gilbert |

## 연계 도메인

| 코드 | 라이브러리 | 역할 |
|------|-----------|------|
| C-28 | PE-AI | EW-AI-01, EW-AI-02 연계 |
| C-29 | PE-SEMI | Fab State S0~S4 교차 검증 |
| C-22 | PE-EQP | 장비 공급 단절 교차 분석 |
| C-27 | PE-MIN | Ga/Ge/RE 수출통제 연계 |
| C-30 | PE-DC | 데이터센터 전력·냉각 연계 |

## 파일 구성

```
SEMI-STRAT-007/
├── README.md                          # 이 파일
├── SEMI-STRAT-007-v1.0-OPT.md        # Master (PE-3: 97)
├── SEMI-STRAT-007-v1.0-KR.md         # Variant-A KR 특화 (PE-3: 95)
└── SEMI-STRAT-007-v1.0-GLOBAL.md     # Variant-B 멀티국가 (PE-3: 94)
```

## knowledge_graph v4.6

```
+3 nodes:
  SEMI-STRAT-007-MASTER  (prompt_master)
  SEMI-STRAT-007-KR      (prompt_variant)
  SEMI-STRAT-007-GLOBAL  (prompt_variant)

+6 edges:
  SEMI-STRAT-007-MASTER → PE-STRAT-HUB      [BELONGS_TO]
  PE-STRAT-HUB → SEMI-STRAT-007-MASTER      [CONTAINS]
  PE-STRAT-HUB → SEMI-STRAT-007-KR          [CONTAINS]
  PE-STRAT-HUB → SEMI-STRAT-007-GLOBAL      [CONTAINS]
  SEMI-STRAT-007-MASTER → SEMI-STRAT-001-MASTER [CROSS_LINKS]
  SEMI-STRAT-007-MASTER → WORLD-AB-MODEL    [CROSS_LINKS]

누적: 140 nodes / 213 edges
```

## Parent 프롬프트

- [SEMI-STRAT-001-v6.2-OPT](../SEMI-STRAT-001-v6.2-OPT.md) — Master 계열 원형

## Notion

- C-33 PE-STRAT 라이브러리: https://app.notion.com/p/35255ed436f0810f830be1feb1512c28
- T-09 Mother Page v4.6: https://app.notion.com/p/34a55ed436f0814d9cffe6a2f0816e29
