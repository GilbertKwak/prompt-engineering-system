# E2E TEST CASE 02: GreenZone — 제조업 GREEN Zone
# GitHub SSOT: prompts/PE-DD/test_case_02_greenzone_manufacturing.md
# 목적: Stage×Domain 매트릭스 6개 코드 전체 검증 (제조업 GREEN Zone)
# 수행일: 2026-05-07 | 버전: v1.0

## ══ 테스트 케이스 요약 ══

| 항목 | 내용 |
|---|---|
| 기업명 | KoraTech Industries (Fictional Test Case) |
| Stage | Series A |
| Domain | 제조 / 전통 |
| 요청 밸류에이션 | $45M (Post-Money) |
| 유치 목표 | $10M |
| 테스트 목적 | GREEN Zone → Stage×Domain 매트릭스 전체 경로 검증 |

## ══ IR 핵심 주장 ══

```
1. KoraTech Industries: 산업용 정밀부품 제조 (반도체 장비 서브컴포넌트)
   연매출 $12M, 영업이익률 18%, YoY 성장률 35%
2. 주요 고객사: 삼성전자·TSMC 협력사 2곳 (계약서 첨부), 수주잔고 $8M
3. Series A $10M 조달 목적: CAPA 2x 증설 (신규 CNC 라인 3기)
```

## ══ OPT-DD 7-Layer 분석 ══

| Layer | 발견 사항 | 리스크 | 점수 | 구분 |
|---|---|---|---|---|
| L1 출처 | 독립 감사 완료 (Ernst & Young), 3개년 FS 제출 | 🟢 | 2 | Standard |
| L2 의도 | 창업자 세컨더리 없음, 전액 설비투자 목적 | 🟢 | 1 | Critical |
| L3 시장 | 반도체 장비 부품 시장 TAM $28B — 신뢰 가능한 Gartner 인용 | 🟢 | 2 | Standard |
| L4 고객 | 주요 고객 계약서 2건 확인, 수주잔고 $8M 실재 | 🟢 | 2 | Critical |
| L5 기술 | 정밀 CNC 가공 — 표준 기술, 특허 2건 보유 | 🟢 | 2 | Critical |
| L6 정책 | 반도체 수출규제 영향 최소 (부품 tier-3 수준) | 🟡 | 3 | Standard |
| L7 논리 | 35% YoY 성장 지속 가정 — CAPA 증설 근거로 논리적 | 🟢 | 2 | Standard |

## ══ v1.2 Weighted Score 산출 ══

```
Critical (L2=1, L4=2, L5=2) × 1.5 = 7.5
Standard (L1=2, L3=2, L6=3, L7=2) × 1.0 = 9.0
Weighted = (7.5 + 9.0) / 8.5 = 16.5 / 8.5 = 1.94

Domain Threshold (제조/범용): GREEN ≤ 3.5
CRITICAL FLAG 체크: L2=1, L4=2, L5=2 → 모두 기준값 미만 → FLAG 미발동

→ 🟢 GREEN ZONE (1.94 ≤ 3.5)
```

## ══ Trigger Engine 판정 + Stage×Domain 라우팅 ══

```
ZONE:        🟢 GREEN
GATE:        PASSED (Weighted: 1.94)
MEMO_AUTO:   TRUE
STAGE:       Series A
DOMAIN:      제조/전통

Stage×Domain 매트릭스 → 제조/Series A → FIN-04 + FIN-02

PRIMARY:    pe_fin_04_manufacturing_v2.0
SECONDARY:  pe_fin_02_advanced_fpa_v2.0
```

## ══ Context Injection Packet ══

```json
{
  "entity":          "KoraTech Industries",
  "stage":           "Series A",
  "domain":          "제조/전통",
  "dd_risk_score":   "1.94 (Weighted v1.2)",
  "dd_risk_flags":   ["L6: 반도체 수출규제 모니터링 권고"],
  "valuation_claim": "$45M Post-Money",
  "capex_plan":      "CNC 라인 3기 증설 ($8M)",
  "backlog":         "$8M 수주잔고 확인",
  "hockey_stick":    "없음 (35% YoY 선형 성장)",
  "hidden_intent":   "없음",
  "scenario":        "base_case"
}
```

## ══ 실행 명령어 ══

```bash
/pe-fin run PROMPT="pe_fin_04_manufacturing_v2.0" \
  ENTITY="KoraTech Industries" STAGE="Series A" DOMAIN="제조" \
  DD_GATE="PASSED (Weighted: 1.94)" \
  DD_PACKET="{backlog:8M, capex:8M, yoy_growth:35%}" \
  SCENARIO="base_case" MEMO_AUTO=TRUE
```

## ══ 검증 결과 ══

| 검증 항목 | 기대값 | 실제값 | 통과 |
|---|---|---|---|
| Zone 판정 | GREEN | GREEN (1.94) | ✅ |
| CRITICAL FLAG | 미발동 | 미발동 | ✅ |
| Stage×Domain 라우팅 | FIN-04+02 | FIN-04+02 | ✅ |
| MEMO_AUTO | TRUE | TRUE | ✅ |
| Domain 임계값 적용 | ≤3.5 | 1.94 < 3.5 | ✅ |

## CHANGELOG
| 버전 | 날짜 | 내용 |
|---|---|---|
| v1.0 | 2026-05-07 | 최초 생성 — GREEN Zone 제조업 검증 완료 |
