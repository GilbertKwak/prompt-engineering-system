# DD-FIN TRIGGER ENGINE v1.3
# GitHub SSOT: prompts/PE-DD/dd_fin_trigger_engine_v1.3.md
# 업그레이드: v1.2 → v1.3
# 변경: 3-케이스 E2E 전경로 검증 완료 → 라우팅 매트릭스 확정판
# 작성일: 2026-05-07

## ══ CHANGELOG v1.3 ══

| 버전 | 날짜 | 내용 |
|---|---|---|
| v1.0 | 2026-05-07 | 최초 생성 — 3-Zone, Stage×Domain, Context Injection |
| v1.2 | 2026-05-07 | NovaMind AI E2E 기반: 가중치 차등, YELLOW 2단계, Domain 임계값, CRITICAL FLAG |
| v1.3 | 2026-05-07 | 3-케이스 전경로 검증 완료 → 라우팅 매트릭스 확정, CRITICAL FLAG 의의 명문화 |

## ══ ARCHITECTURE OVERVIEW v1.3 ══

```
[INPUT]
  IR 자료 / Pitch Deck / 정부 문서 / 범용 요청
        ↓
[OPT-DD-FIN v1.1]
  Phase 1~9: 7-Layer + 재무 특화 + Risk Scoring
        ↓
[TRIGGER ENGINE v1.3]
  Step 1: Raw Score 수신 (7항목)
  Step 2: CRITICAL FLAG 우선 체크 → 즉시 RED 가능
  Step 3: Weighted Score 산출 (Critical×1.5 / Standard×1.0)
  Step 4: Domain별 임계값 적용
  Step 5: 4-Zone 판정
        ↓
[PE-FIN ROUTER v1.0]
  Stage × Domain → 최적 PE-FIN 프롬프트 디스패치
        ↓
[PE-FIN 01~10 실행]
  → Investment Memo 자동 생성 (GREEN 한정)
```

## ══ SCORING ENGINE v1.3 (확정판) ══

### Step 1: Raw Score 정의

```
RAW = {
  L1_source:     [1~10]  # 출처 신뢰성 — Standard
  L2_intent:     [1~10]  # 숨겨진 의도 — CRITICAL ⚡
  L3_market:     [1~10]  # 시장 현실성 — Standard
  L4_customer:   [1~10]  # 고객 실재성 — CRITICAL ⚡
  L5_tech:       [1~10]  # 기술 실현 가능성 — CRITICAL ⚡
  L6_policy:     [1~10]  # 정책·규제 리스크 — Standard
  L7_logic:      [1~10]  # 내부 논리 괴리 — Standard
}
```

### Step 2: CRITICAL FLAG (우선 체크 — Instant RED)

```python
# 임계값 근거: E2E 케이스 02~04 검증 완료
# L2≥8: 창업자 사기적 의도 (세컨더리 은폐, 자금 유용)
# L5≥8: 기술 허위 표기 (케이스 04 QuantumLeap Bio로 검증)
# L4≥9: 고객 실재성 전무 (MOU만 있고 유료 계약 0)

if RAW['L2_intent']   >= 8: FLAG = True  # 의도 구조적 사기
if RAW['L5_tech']     >= 8: FLAG = True  # 기술 허위 (케이스 04 확인)
if RAW['L4_customer'] >= 9: FLAG = True  # 고객 실재성 전무

if FLAG:
    return {zone: 'RED', gate: 'INSTANT_BLOCK', skip_steps: [3,4,5]}
```

### Step 3: Weighted Score

```python
CRITICAL_SUM = (RAW['L2'] + RAW['L4'] + RAW['L5']) * 1.5
STANDARD_SUM = (RAW['L1'] + RAW['L3'] + RAW['L6'] + RAW['L7']) * 1.0
WEIGHTED     = (CRITICAL_SUM + STANDARD_SUM) / 8.5
```

### Step 4: Domain 임계값

```python
THRESHOLD = {
    '반도체|딥테크|바이오': {'GREEN': 2.5, 'YL': 4.0, 'YH': 5.5},
    'SaaS|AI|소프트웨어':  {'GREEN': 3.0, 'YL': 4.5, 'YH': 6.0},
    '제조|에너지|범용':    {'GREEN': 3.5, 'YL': 5.0, 'YH': 6.5},
}
# 케이스 02(제조 1.94→GREEN) / 03(SaaS 3.41→YL) 로 임계값 검증 완료
```

### Step 5: Zone 판정

```python
if FLAG:                         zone = 'RED_FLAG'
elif W <= T['GREEN']:             zone = 'GREEN'
elif W <= T['YL']:                zone = 'YELLOW_LIGHT'
elif W <= T['YH']:                zone = 'YELLOW_HEAVY'
else:                             zone = 'RED'
```

## ══ ROUTING MATRIX v1.3 (확정판) ══

### 🟢 GREEN — FULL PIPELINE

```
ACTION:   FULL_PIPELINE_EXECUTE
MEMO:     자동 생성

[Stage × Domain 확정 라우팅]
┌──────────────┬───────────┬───────────┬───────────┬───────────┐
│ Stage        │ SaaS      │ 반도체/제조│ AI        │ 범용      │
├──────────────┼───────────┼───────────┼───────────┼───────────┤
│ Pre-Seed     │ 05+01     │ 04+05     │ 05+01     │ 05+01     │
│ Series A~C+  │ 03+01 ✅  │ 04+02 ✅  │ 01+02     │ 01+02     │
│ IPO          │ 03+09     │ 04+09     │ 02+09     │ 01+09     │
│ M&A/LBO      │ 07+06     │ 07+04     │ 07+06     │ 07+08     │
└──────────────┴───────────┴───────────┴───────────┴───────────┘
✅ = 케이스 02(제조 Series A), 케이스 03(SaaS Series A) 검증 완료

SECONDARY (항상 추가):
→ FIN-02 Advanced FPA (시나리오 민감도)
→ FIN-10 AI Agent (Score ≤ GREEN×0.8 시 자동 Memo)
```

### 🟡 YELLOW-LIGHT — 조건부

```
ACTION:   PRIMARY + bear_case + 게이트 해소 요건 출력
GATE:     해소 후 GREEN 파이프라인 자동 재실행
✅ 케이스 03(ClearFlow SaaS 3.41) 검증 완료
```

### 🟡 YELLOW-HEAVY — Stress Test 필수

```
ACTION:   FIN-09 Quant 우선 + stress_test
GATE:     필수 추가 실사 목록 자동 출력
(미검증 — v1.4 테스트 케이스 예정)
```

### 🔴 RED — BLOCK + ESCALATE

```
ACTION:     OPT-DCA 에스컬레이션
RED_SCORE:  총점 초과 (케이스 01 NovaMind 6.53 검증 완료)
RED_FLAG:   CRITICAL FLAG 즉시 차단 (케이스 04 QuantumLeap L5=9 검증 완료)
```

## ══ VALIDATION SUMMARY v1.3 ══

| 경로 | 케이스 | 결과 | 상태 |
|---|---|---|---|
| 🟢 GREEN / 제조 Series A | Case 02: KoraTech (1.94) | FIN-04+02 ✅ | 검증 완료 |
| 🟡 YELLOW-LIGHT / SaaS | Case 03: ClearFlow (3.41) | FIN-03+01 bear_case ✅ | 검증 완료 |
| 🔴 RED / Score 초과 | Case 01: NovaMind (6.53) | BLOCK + OPT-DCA ✅ | 검증 완료 |
| 🔴 RED / CRITICAL FLAG | Case 04: QuantumLeap (L5=9) | INSTANT BLOCK ✅ | 검증 완료 |
| 🟡 YELLOW-HEAVY | 미검증 | — | v1.4 예정 |
| 🟢 GREEN / Pre-Seed | 미검증 | — | v1.4 예정 |
| 🟢 GREEN / IPO | 미검증 | — | v1.4 예정 |

## ══ EXECUTION COMMANDS (전체 Zone) ══

```bash
# 🟢 GREEN
/pe-fin run PROMPT="pe_fin_[04]_manufacturing_v2.0" ENTITY="{{E}}" STAGE="{{S}}" DOMAIN="{{D}}" \
  DD_GATE="PASSED (Weighted: {{W}})" DD_PACKET="{{PKT}}" SCENARIO="base_case" MEMO_AUTO=TRUE

# 🟡 YELLOW-LIGHT
/pe-fin run PROMPT="pe_fin_[03]_saas_v2.0" ENTITY="{{E}}" STAGE="{{S}}" DOMAIN="{{D}}" \
  DD_GATE="CONDITIONAL-LIGHT (Weighted: {{W}}, Flags: {{FLAGS}})" \
  DD_PACKET="{{PKT}}" SCENARIO="bear_case"

# 🟡 YELLOW-HEAVY
/pe-fin run PROMPT="pe_fin_09_quant_v2.0" ENTITY="{{E}}" STAGE="{{S}}" DOMAIN="{{D}}" \
  DD_GATE="CONDITIONAL-HEAVY (Weighted: {{W}})" DD_PACKET="{{PKT}}" SCENARIO="stress_test"

# 🔴 RED (Score)
/dd-fin escalate ENTITY="{{E}}" WEIGHTED_SCORE="{{W}}" TRIGGER="OPT-DCA" \
  REASON="{{HIGH_RISK_ITEMS}}"

# 🔴 RED (CRITICAL FLAG)
/dd-fin escalate ENTITY="{{E}}" TRIGGER="OPT-DCA" \
  CRITICAL_FLAGS="{{FLAG_ITEMS}}" REASON="구조적 결함 — 수치 스코어링 우선 차단"
```
