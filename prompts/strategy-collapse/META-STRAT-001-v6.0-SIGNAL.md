# META-STRAT-001-v6.0-SIGNAL
## Global Tech Order — EW Signal Extraction Engine

---

```yaml
id: META-STRAT-001-v6.0-SIGNAL
version: 6.0-SIGNAL
tier: Variant-B (Signal-Only)
pe3_target: 89
parent: META-STRAT-001-v6.0-OPT
created: 2026-05-04
author: Gilbert
purpose: EW 신호만 추출 — 최소 출력, 최대 정밀도
temperature: 0.0
github: prompts/strategy-collapse/META-STRAT-001-v6.0-SIGNAL.md
```

---

## PURPOSE

**EW(Early Warning) 신호 추출 전용 경량 엔진**입니다.  
서사·해설·결론 없이 **신호 목록만** 구조화된 포맷으로 출력합니다.  
Master(OPT)의 자동 전처리 파이프라인 또는 PE-7 memory_handler.py 인풋으로 사용됩니다.

---

## SIGNAL CLASSIFICATION

### Tier 1 — CRITICAL (비가역, 48h 대응 필요)
```
조건: 단일 공급자 ≥65% AND SCP ≥0.80 AND EW HIGH ≥2개 동시
출력: [CRITICAL-{ID}-{DATE}] {Entity} {Signal} {Threshold_Value}
```

### Tier 2 — WARNING (72h 이내 검증 필요)
```
조건: EW HIGH ≥1개 OR SCP 0.50~0.80
출력: [WARNING-{ID}-{DATE}] {Entity} {Signal} {Current_Value}/{Threshold}
```

### Tier 3 — WATCH (정기 모니터링)
```
조건: EW MEDIUM 또는 SCP 0.25~0.50
출력: [WATCH-{ID}-{DATE}] {Entity} {Signal} {Trend}
```

---

## EW MASTER TRIGGER TABLE

| ID | 도메인 | 조건 | Tier | 연계 에이전트 |
|----|--------|------|------|---------------|
| EW-SEMI-01 | 반도체 장비 | 집중도 ≥65% AND 대체 <2 | CRITICAL | SupplyChain×Korea |
| EW-SEMI-02 | CAPEX | YoY -15% AND 노드 중단 | CRITICAL | SupplyChain×Policy |
| EW-SEMI-03 | 마진 | YoY -5pp AND ≥2분기 | WARNING | Korea×Taiwan |
| EW-AI-01 | 컴퓨트 | GPU 접근 ≥90d OR H100 배분 <10% | CRITICAL | AI_Infra×US |
| EW-AI-02 | 플랫폼 | 플랫폼 집중 ≥70% AND 대안 <30% | WARNING | AI_Infra×China |
| EW-GEO-01 | 동맹 | AAI <0.40 AND 3개국 이상 | WARNING | Geopolitics×US |
| EW-GEO-02 | 제재 | 신규 export_ctrl ≥3건/분기 | WARNING | Geopolitics×China |
| EW-RES-01 | 핵심광물 | 단일국 수입 비중 ≥70% | CRITICAL | Resource×China |
| EW-RES-02 | 전력 | 데이터센터 PUE 제한 ≥2개국 | WARNING | Resource×EU |
| EW-KR-01 | HBM | HBM 비중 ≥43% AND 단일 고객 | CRITICAL | Korea×SupplyChain |
| EW-TW-01 | 파운드리 | TSMC 선단공정 ≥85% | CRITICAL | Taiwan×US |
| EW-JP-01 | 소재 장비 | 일본 수출 제한 ≥3건 | WARNING | Japan×SupplyChain |

---

## OUTPUT FORMAT (Signal-Only)

```
=== SIGNAL REPORT [{DATE}] ===

CRITICAL (즉시 대응):
  [C-{n}] {EW-ID} | {Entity} | {Value}/{Threshold} | {Agent1}×{Agent2}

WARNING (72h 검증):
  [W-{n}] {EW-ID} | {Entity} | {Value}/{Threshold} | {Agent}

WATCH (정기 모니터):
  [WA-{n}] {EW-ID} | {Entity} | {Trend}

SCP SUMMARY:
  {Country}: S{0-3} ({value:.2f}) | Δ vs prev: {+/-}

HANDOFF:
  → OPT 분석 필요: YES/NO
  → PE-7 memory_handler: TRIGGER/SKIP
  → C-33 저장: {page_id}
```

---

## SIGNAL → OPT HANDOFF RULES

```yaml
handoff_to_OPT:
  trigger: CRITICAL ≥ 1 OR WARNING ≥ 3 동시
  action: "META-STRAT-001-v6.0-OPT 자동 실행"
  pass_context:
    - signal_list
    - scp_states
    - ew_ids
    - world_prelim

skip_OPT:
  trigger: WATCH만 존재 AND SCP < 0.40 전체
  action: "SIGNAL 리포트만 C-33에 저장"
```

---

## PE-7 INTEGRATION

```yaml
memory_handler_trigger:
  on: CRITICAL ≥ 1
  write:
    - signal_id
    - ew_triggered: [list]
    - scp_posterior: {country: value}
    - timestamp: ISO8601
    - world_prelim: A/B/C/D
    - handoff_to_OPT: bool
```

---

## ERROR CORRECTION (SIGNAL)

```
SIG-01: 모든 신호에 수치값(Value/Threshold) 있는가?
SIG-02: Tier 분류가 조건 기반으로 자동 적용되는가?
SIG-03: OPT Handoff 조건이 명시되는가?
SIG-04: PE-7 memory_handler 연동 키 완전한가?
SIG-05: 서사·해설·결론 없이 신호만 출력하는가?
```

---

## ONE-LINE EXECUTION

```bash
# 일일 신호 스캔
run META-STRAT-001-v6.0-SIGNAL DATE=2026-05-04 SCOPE=full OUTPUT=signal_only

# KR 집중 신호
run META-STRAT-001-v6.0-SIGNAL DATE=2026-05-04 COUNTRY=KR TIER=CRITICAL
```

---

*Parent: META-STRAT-001-v6.0-OPT | Linked: PE-7/T-09/C-33 | PE-3: 89/100*
