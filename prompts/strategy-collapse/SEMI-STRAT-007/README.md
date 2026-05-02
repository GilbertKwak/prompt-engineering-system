# SEMI-STRAT-007 · StrategicMonitoringAgent v5.4

> C-33 PE-STRAT 라이브러리 · 첫 번째 항목 · 2026-05-02 등록

## 파일 구성

| 파일 | 유형 | PE-3 | 설명 |
|------|------|------|------|
| `SEMI-STRAT-007-v1.0-OPT.md` | Master | 97 | World A/B/C/D + 국가 파라미터 교체형 |
| `SEMI-STRAT-007-v1.0-KR.md` | Variant-A | 95 | 단일국가 KR 특화 (SK Hynix / Samsung) |
| `SEMI-STRAT-007-v1.0-GLOBAL.md` | Variant-B | 94 | 멀티국가 글로벌 비교형 (5개국) |

## 빠른 시작

### Master 실행
```
COUNTRY_CODE=KR
COUNTRY_NAME=South Korea
FOCUS_FIRMS=SK Hynix, Samsung Semiconductor
ANALYSIS_DATE=2026-05-02
```

### KR Variant 실행 (월간 SCP 업데이트)
```
FOCUS_FIRMS=SK Hynix, Samsung Semiconductor
ANALYSIS_DATE=2026-05-02
```

### GLOBAL Variant 실행 (분기 크로스 컨트리)
```
FOCUS_COUNTRIES=KR,TW,JP,US,CN
FOCUS_FIRMS=SK Hynix, Samsung, TSMC, Rapidus, Intel, NVIDIA, SMIC, Huawei
ANALYSIS_DATE=2026-05-02
```

## 연계 도메인

- [PE-AI (C-28)](../../README.md) — EW-AI-01, EW-AI-02
- [PE-SEMI (C-29)](../../README.md) — 전체 EW-SEMI
- [PE-EQP (C-22)](../../README.md) — EW-SEMI-01
- [PE-MIN (C-27)](../../README.md) — EW-SEMI-03
- [PE-DC (C-30)](../../README.md) — EW-AI-02

## knowledge_graph v4.6

- 누적: **140 nodes / 213 edges**
- 신규: +3 nodes / +6 edges
- 커밋: `feat(graph): knowledge_graph v4.6 — SEMI-STRAT-007 +3nodes/+6edges`

---

**등록일**: 2026-05-02 12:23 KST · **관리자**: Gilbert · **C-33 PE-STRAT**
