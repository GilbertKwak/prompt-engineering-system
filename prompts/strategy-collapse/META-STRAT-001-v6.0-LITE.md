# META-STRAT-001-v6.0-LITE
## Global Tech Order Meta-Orchestrator — Lightweight Single-Country

---

```yaml
id: META-STRAT-001-v6.0-LITE
version: 6.0-LITE
tier: Variant-A (Lightweight)
pe3_target: 91
parent: META-STRAT-001-v6.0-OPT
created: 2026-05-04
author: Gilbert
scope: Single-country, World A/B only
temperature: 0.0
github: prompts/strategy-collapse/META-STRAT-001-v6.0-LITE.md
```

---

## PURPOSE

Master(OPT)의 경량화 버전입니다.  
단일 국가 집중 분석, World A/B 범위, PE-1 3-Loop 자동개선 적용.

### Master vs LITE

| 항목 | OPT (Master) | LITE (Variant-A) |
|------|-------------|------------------|
| 국가 범위 | 7개국 멀티 | 1개국 집중 |
| World 범위 | A/B/C/D 전체 | A/B만 |
| 에이전트 | 12개 (국가7+테마5) | 3개 (Korea+SC+Resource) |
| PE-3 | 96 | 91 |
| PE-1 Loop | 없음 | 3 loops (76→91) |
| 출력 분량 | 전체 4섹션 | Decision_Brief만 |

---

## INPUT PARAMETERS

```yaml
COUNTRYCODE:   KR                    # 단일 국가
COUNTRYNAME:   South Korea
FOCUS_FIRMS:   SK Hynix, Samsung     # 핵심 기업 (콤마 구분)
ANALYSIS_DATE: 2026-05-04
WORLD_SCOPE:   AB                    # A,B 만
SESSION_ID:    auto-generate
```

---

## EW TRIGGERS (LITE — KR 특화)

| ID | 카테고리 | 조건 | 비가역성 |
|----|---------|------|----------|
| EW-KR-01 | HBM 매출 집중 | HBM 비중 ≥43% AND 미국 단일 의존 | HIGH |
| EW-KR-02 | K-칩스법 집행 | §24 집행률 ≤40% AND 투자 YoY -10% | HIGH |
| EW-KR-03 | 파운드리 PoNR | 삼성 선단공정 점유율 <8% | CRITICAL |
| EW-SEMI-01 | 장비 의존 | 65% 집중 AND 대체 <2개 | HIGH |
| EW-AI-01 | AI 컴퓨트 | GPU 접근 지연 ≥90d | HIGH |

---

## BAYESIAN SCP (LITE)

```yaml
prior: Beta(2, 9)
updates:
  EW_1개: Beta(+1, 0)
  EW_2개: Beta(+2, 0)
  정상_월간: Beta(0, +1)
CI: 90%
state:
  S0_Aligned:     ≤ 0.25
  S1_Tension:     0.25–0.50
  S2_Constrained: 0.50–0.80
  S3_Broken:      > 0.80
```

---

## PE-1 AUTO-REFINEMENT (3 LOOPS)

| Loop | PE-3 | 개선 내용 |
|------|------|-----------|
| 0 | 76 | 기본 출력 |
| 1 | 82 | EW 5pp 조정 + SCP 6개 추가 |
| 2 | 87 | CT-1 FirmExhaustion ALERT + Variant 5개 |
| 3 | 91 | Enhanced Monitoring + Bayesian 4개 |

---

## OUTPUT (LITE)

### Decision_Brief (정부/기업)

```
[LITE-BRIEF-{COUNTRY}-{DATE}]
1. World A/B SCP 상태 + 90% CI
2. EW 트리거 발동 현황
3. World 판정 (A or B)
4. 핵심 선택지 ≤3개 (이득/리스크/기한)
5. Inaction Cost 추정
6. 다음 모니터링 시점
```

---

## ERROR CORRECTION (LITE)

```
L-01: World A/B만 판정하는가? (C/D 혼입 금지)
L-02: 단일 국가에 집중하는가?
L-03: EW 수치 임계값 존재하는가?
L-04: Decision_Brief 형식 준수하는가?
L-05: C-33 저장 경로 명시하는가?
```

---

## ONE-LINE EXECUTION

```bash
run META-STRAT-001-v6.0-LITE COUNTRY=KR WORLD=AB DATE=2026-05-04 FIRMS="SK Hynix,Samsung"
```

---

*Parent: META-STRAT-001-v6.0-OPT | Linked: C-33 PE-STRAT | PE-3: 91/100*
