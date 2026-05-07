# DD-FIN TRIGGER ENGINE v1.2
# GitHub SSOT: prompts/PE-DD/dd_fin_trigger_engine_v1.2.md
# 업그레이드: v1.0 → v1.2
# 변경: 가중치 차등 스코어링 + YELLOW Zone 세분화 + Domain별 임계값 + CRITICAL FLAG
# 작성일: 2026-05-07
# E2E 테스트: NovaMind AI (Series B SaaS) 구조적 문제 발갹 계기

## ══ OVERVIEW ══
# v1.0 대비 주요 변경 4가지:
# 1. 가중치 차등 스코어링 — Critical vs Standard 항목 분리
# 2. YELLOW Zone 세분화 — LIGHT(3.0~4.5) vs HEAVY(4.5~6.0)
# 3. Domain별 GREEN/YELLOW/RED 임계값 조정
# 4. CRITICAL FLAG — 단일 항목 구조적 결함 시 즉시 RED 전환

## ══ SCORING ENGINE v1.2 ══

### Step 1: Raw Score 수신 (Risk Scoring Matrix 7항목, 1~10)

```
RAW = {
  L1_source:     [1~10],   # 출처 신뢰성
  L2_intent:     [1~10],   # 숨겨진 의도 — CRITICAL
  L3_market:     [1~10],   # 시장 현실성
  L4_customer:   [1~10],   # 고객 실재성 — CRITICAL
  L5_tech:       [1~10],   # 기술 실현 가능성 — CRITICAL
  L6_policy:     [1~10],   # 정책·규제 리스크
  L7_logic:      [1~10],   # 내부 논리 괴리
}
```

### Step 2: CRITICAL FLAG 연산 (우선 체크)

```
# 단일 항목 구조적 결함 — 총점 무관 즉시 RED
IF RAW.L2_intent  >= 8:  FLAG_TRIGGER = TRUE  # 숨겨진 의도 구조적 사기 의심
IF RAW.L5_tech    >= 8:  FLAG_TRIGGER = TRUE  # 기술 허위 시해
IF RAW.L4_customer>= 9:  FLAG_TRIGGER = TRUE  # 고객 실재성 거의 없음

IF FLAG_TRIGGER == TRUE:
  RISK_ZONE  = RED
  GATE       = BLOCKED
  SKIP       → Step 3~4 실행 불필요
  ACTION     = BLOCK + OPT-DCA ESCALATE
  REASON     = "단일 항목 CRITICAL FLAG 발동"
```

### Step 3: Weighted Score 산출

```
# Critical 항목 (L2, L4, L5) — 가중치 1.5x
# Standard 항목 (L1, L3, L6, L7) — 가중치 1.0x

CRITICAL_SUM = (RAW.L2_intent + RAW.L4_customer + RAW.L5_tech) * 1.5
STANDARD_SUM = (RAW.L1_source + RAW.L3_market + RAW.L6_policy + RAW.L7_logic) * 1.0
WEIGHT_DENOM = (3 * 1.5) + (4 * 1.0)  # = 8.5

WEIGHTED_SCORE = (CRITICAL_SUM + STANDARD_SUM) / WEIGHT_DENOM
# 예시: NovaMind AI → (7+7+7)*1.5 + (6+5+5+8) = 31.5+24 = 55.5 / 8.5 = 6.53
```

### Step 4: Domain별 임계값 적용

```
DOMAIN_THRESHOLD = {
  "반도체 | 딥테크 | 바이오": { GREEN: 2.5, YELLOW_LIGHT: 4.0, YELLOW_HEAVY: 5.5 },
  "SaaS | AI | 소프트웨어":     { GREEN: 3.0, YELLOW_LIGHT: 4.5, YELLOW_HEAVY: 6.0 },
  "제조 | 에너지 | 범용":     { GREEN: 3.5, YELLOW_LIGHT: 5.0, YELLOW_HEAVY: 6.5 },
}

GREEN_THRESH       = DOMAIN_THRESHOLD[DOMAIN].GREEN
YELLOW_LIGHT_THRESH = DOMAIN_THRESHOLD[DOMAIN].YELLOW_LIGHT
YELLOW_HEAVY_THRESH = DOMAIN_THRESHOLD[DOMAIN].YELLOW_HEAVY
RED_THRESH         = YELLOW_HEAVY_THRESH  # 초과 시 RED
```

### Step 5: Zone 판정

```
IF FLAG_TRIGGER:                                  → RED (CRITICAL FLAG)
ELSE IF WEIGHTED_SCORE <= GREEN_THRESH:           → GREEN
ELSE IF WEIGHTED_SCORE <= YELLOW_LIGHT_THRESH:    → YELLOW-LIGHT
ELSE IF WEIGHTED_SCORE <= YELLOW_HEAVY_THRESH:    → YELLOW-HEAVY
ELSE:                                             → RED
```

## ══ 4-ZONE ROUTING MATRIX v1.2 ══

### 🟢 GREEN — 투자 적합
```
ZONE: GREEN (score ≤ DOMAIN GREEN_THRESH)

ACTION    = FULL_PIPELINE_EXECUTE
MEMO_AUTO = TRUE

Routing → Stage × Domain 매트릭스 (v1.2 업데이트)

| Stage \ Domain       | SaaS | 반도체/제조 | AI | 범용 |
|---|---|---|---|---|
| Pre-Seed/Seed        | FIN-05+01 | FIN-04+05 | FIN-05+01 | FIN-05+01 |
| Series A~C+          | FIN-03+01 | FIN-04+02 | FIN-01+02 | FIN-01+02 |
| IPO                  | FIN-03+09 | FIN-04+09 | FIN-02+09 | FIN-01+09 |
| M&A/LBO              | FIN-07+06 | FIN-07+04 | FIN-07+06 | FIN-07+08 |

Secondary (GREEN 시 항상 추가)
→ pe_fin_02_advanced_fpa  (시나리오 Sensitivity)
→ pe_fin_10_ai_agent      (score ≤ GREEN_THRESH*0.8 시 자동 Memo 생성)
```

### 🟡 YELLOW-LIGHT — 세부 검토
```
ZONE: YELLOW-LIGHT (GREEN_THRESH < score ≤ YELLOW_LIGHT_THRESH)

ACTION    = STANDARD_CONDITIONAL
MEMO_AUTO = FALSE

Routing:
→ PRIMARY_FIN  = stage_router(STAGE, DOMAIN)   # GREEN과 동일 라우팅
→ SECONDARY    = pe_fin_02_advanced_fpa         # Sensitivity 필수
→ SCENARIO     = bear_case
FLAG = "YELLOW-LIGHT: 세부 검토 권고 — 발견 리스크 항목 명시"
```

### 🟡 YELLOW-HEAVY — 추가 실사 필수
```
ZONE: YELLOW-HEAVY (YELLOW_LIGHT_THRESH < score ≤ YELLOW_HEAVY_THRESH)

ACTION    = MANDATORY_STRESS_TEST
MEMO_AUTO = FALSE

Routing:
→ PRIMARY_FIN  = pe_fin_09_quant_v2.0           # VaR/Stress Test 우선
→ SECONDARY    = pe_fin_02_advanced_fpa         # Sensitivity
→ SCENARIO     = stress_test + downside
GATE = "필수 추가 실사 항목 해소 후 PE-FIN 전체 파이프라인 재실행"
REQUIRED_ITEMS = [HIGH_RISK 항목 목록 자동 출력]
```

### 🔴 RED — 투자 부적합
```
ZONE: RED (score > YELLOW_HEAVY_THRESH OR FLAG_TRIGGER)

ACTION    = BLOCK + ESCALATE
MEMO_AUTO = FALSE

BLOCK  → PE-FIN 전체 실행 중단
TRIGGER → OPT-DCA 심층 원인 분석
NOTIFY  = "투자 부적합 — 의사결정자 에스콜레이션"
RECHECK = "Weighted Score ≤ YELLOW_HEAVY_THRESH 달성 + CRITICAL FLAG 전부 해소 시 재진입"
```

## ══ EXECUTION COMMAND TEMPLATE v1.2 ══

```bash
# GREEN
/pe-fin run PROMPT="[stage_router 결과]" ENTITY="{{E}}" STAGE="{{S}}" DOMAIN="{{D}}" \
  DD_GATE="PASSED (Weighted: {{W}})" DD_PACKET="{{PKT}}" SCENARIO="base_case"

# YELLOW-LIGHT
/pe-fin run PROMPT="[stage_router 결과]" ENTITY="{{E}}" STAGE="{{S}}" DOMAIN="{{D}}" \
  DD_GATE="CONDITIONAL-LIGHT (Weighted: {{W}})" DD_PACKET="{{PKT}}" SCENARIO="bear_case"

# YELLOW-HEAVY
/pe-fin run PROMPT="pe_fin_09_quant_v2.0" ENTITY="{{E}}" STAGE="{{S}}" DOMAIN="{{D}}" \
  DD_GATE="CONDITIONAL-HEAVY (Weighted: {{W}}, Flags: {{FLAGS}})" DD_PACKET="{{PKT}}" \
  SCENARIO="stress_test"

# RED
/dd-fin escalate ENTITY="{{E}}" WEIGHTED_SCORE="{{W}}" TRIGGER="OPT-DCA" \
  REASON="{{HIGH_RISK_ITEMS}}" CRITICAL_FLAGS="{{FLAG_ITEMS}}"
```

## ══ SUMMARY TABLE ══

| Zone | Score 범위 (SaaS 기준) | Action | Memo | 주요 PE-FIN |
|---|---|---|---|---|
| 🟢 GREEN | ≤ 3.0 | FULL PIPELINE | ✅ 자동 | Stage×Domain 라우팅 |
| 🟡 YELLOW-LIGHT | 3.0~4.5 | CONDITIONAL | ❌ | Stage×Domain + bear_case |
| 🟡 YELLOW-HEAVY | 4.5~6.0 | STRESS TEST 필수 | ❌ | FIN-09 Quant 우선 |
| 🔴 RED | > 6.0 or FLAG | BLOCK | ❌ | OPT-DCA 에스콜레이션 |
| 🔴 RED (FLAG) | 단일 항목 구조적 결함 | INSTANT BLOCK | ❌ | OPT-DCA 에스콜레이션 |

## CHANGELOG
| 버전 | 날짜 | 내용 |
|---|---|---|
| v1.0 | 2026-05-07 | 최초 생성 — 3-Zone, Stage×Domain 매트릭스, Context Injection |
| v1.2 | 2026-05-07 | E2E 테스트(NovaMind AI) 기반 구조적 개선: 가중치 차등 스코어링, YELLOW 2단계 세분화, Domain믄 임계값, CRITICAL FLAG 로직 |
