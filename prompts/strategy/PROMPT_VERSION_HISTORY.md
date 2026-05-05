# PE-STRAT 프롬프트 버전 이력

**GitHub SSOT**: `prompts/strategy/`  
**Notion 연계**: PE Hub v2.0 > PE-STRAT 섹션

---

## 버전 인덱스

| ID | 파일 | 유형 | Temperature | PE-3 목표 | 버전 | 등록일 | 상태 |
|----|------|------|-------------|-----------|------|--------|------|
| PE-STRAT-01 | `pe_strat_01_v1.0.md` | 범용 전략 AI 아키텍트 (Porter×Ng×Pearl) | 0.1 / 0.0 | 90+ | v1.0 | 2026-05-05 | ✅ Active |
| PE-STRAT-02 | `pe_strat_02_v1.0.md` | 투자 특화 전략 AI 아키텍트 | 0.0 / 0.1 | 90+ | v1.0 | 2026-05-05 | ✅ Active |

---

## 상세 변경 이력

### PE-STRAT-01

| 버전 | 날짜 | 커밋 | 변경 내용 |
|------|------|------|-----------|
| v1.0 | 2026-05-05 | — | 최초 생성 — Porter×Ng×Pearl 통합, 8단계 워크플로우, RL 보상함수 |

### PE-STRAT-02

| 버전 | 날짜 | 커밋 | 변경 내용 |
|------|------|------|-----------|
| v1.0 | 2026-05-05 | — | 최초 생성 — 투자 특화 (VC/PE/M&A/LP), 9단계 워크플로우, Valuation Framework |

---

## 3-Engine 적용 결과 (목표)

| ID | PE-3 Before | PE-3 After (목표) | 개선폭 |
|----|-------------|-------------------|--------|
| PE-STRAT-01 | TBD | 90+ | TBD |
| PE-STRAT-02 | TBD | 90+ | TBD |

---

## 크로스 연계 맵

```
PE-STRAT-01 (범용 전략)
    ├── PE-IS-02 (전략 분석·AI 자동화)
    ├── PE-PM-03 (Phase Gate 체크리스트)
    ├── PE-FC (팩트체크)
    ├── PE-CON (컨설팅 보고서)
    └── P-07 (Recursive Decompose)

PE-STRAT-02 (투자 특화)
    ├── PE-9 AstraChips LP Fund
    ├── PE-FC (투자 수치 검증)
    ├── PE-CON (투자 보고서)
    ├── PE-STRAT-01 (상위 거시 전략)
    └── HBM Salvage Phase 1 Gate
```
