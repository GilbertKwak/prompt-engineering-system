# E2E TEST CASE 01: NovaMind AI
# GitHub SSOT: prompts/PE-DD/test_case_01_novamind_ai.md
# 목적: OPT-DD-FIN ↔ PE-FIN Trigger Engine 엔드-투-엔드 검증
# 수행일: 2026-05-07
# 버전: v1.0 (v1.2 정밀화 계기 케이스)

## ══ 테스트 케이스 요약 ══

| 항목 | 내용 |
|---|---|
| 기업명 | NovaMind AI (Fictional Test Case) |
| Stage | Series B |
| Domain | SaaS / AI |
| 요청 밸류에이션 | $120M (Post-Money) |
| 유치 목표 | $30M (Series B) |
| 테스트 목적 | Trigger Engine v1.0 실제 동작 확인 + v1.2 정밀화 계기 발굴 |

## ══ IR 핵심 주장 (Phase 0) ══

```
[IR 핵심 주장 3문장 요약]
1. NovaMind AI는 기업용 AI 워크플로우 자동화 SaaS로,
   ARR $8M에서 24개월 내 $80M 달성 예상(10x 성장),
   현재 Series B $30M 유치 중, Post-Money $120M 밸류에이션 요청.
2. 주요 고객사 3곳(Fortune 500 명칭 미공개)으로
   계약 $12M 파이프라인 확보 주장.
3. 한국/일본 AI 규제 환경에서 데이터 주권 솔루션으로
   경쟁우위 보유 주장.
```

## ══ OPT-DD 7-Layer 분석 결과 (Phase 1~7) ══

| Layer | 분석 항목 | 발견 사항 | 리스크 |
|---|---|---|---|
| L1 출처 신뢰성 | IR Deck 자체 제작, 3rd-party 감사 없음 | ARR $8M 자체 보고, 감사 미완료 | 🟡 |
| L2 숨겨진 의도 | 창업자 2차 세컨더리 $5M 내포 | $30M 중 $5M이 창업자 현금화 | 🔴 |
| L3 시장 현실성 | 기업 AI SaaS TAM $180B 주장 | SAM 실제 적용 가능 ~$2B 추정 | 🟡 |
| L4 고객 실재성 | 파이프라인 $12M, 계약 확정 $1.2M | 전환율 10%, 고객명 미공개 | 🔴 |
| L5 기술 실현 | "독자 LLM Fine-tuning" 주장 | 실제 OpenAI API 래퍼 구조 확인 | 🔴 |
| L6 정책·규제 | 일본 AI 규제(2025) 대응 주장 | 실제 인증 취득 없음, 로드맵만 존재 | 🟡 |
| L7 내부 논리 | 24개월 10x 성장 가정 | 과거 CAGR 180% vs 예측 1,000% 모순 | 🔴 |

## ══ Layer 8~9 재무 특화 분석 (Phase 2) ══

### Layer 8: 밸류에이션 현실성

| 지표 | NovaMind 주장 | 업계 평균 | 상위 25% | 괴리율 | 판정 |
|---|---|---|---|---|---|
| ARR Multiple | 15x | 6~8x | 10~12x | +50~150% | 🔴 과대평가 |
| Revenue Multiple | 12x | 4~6x | 8x | +50~200% | 🔴 과대평가 |
| Hockey-Stick 근거 | 과거 CAGR 180% → 예측 1,000% | 유사 SaaS p75: 250% | — | 4x 괴리 | 🔴 근거 없음 |

### Layer 9: 재무 건전성

| 지표 | NovaMind | 기준치 | 등급 |
|---|---|---|---|
| Burn Rate | 월 $1.8M | — | — |
| Runway | **10개월** | 18개월+ | 🔴 |
| LTV/CAC | **2.1x** | 3x+ (SaaS) | 🔴 |
| Gross Margin | 61% | 72% (업계 평균) | 🟡 |
| 숨겨진 CB | $4M (IR 미기재) | 없어야 정상 | 🔴 |

## ══ Risk Scoring Matrix (Phase 3) ══

### v1.0 단순 평균 방식
| 항목 | 점수 | 구분 |
|---|---|---|
| L1 출처 | 6 | Standard |
| L2 의도 | 7 | Critical |
| L3 시장 | 5 | Standard |
| L4 고객 | 7 | Critical |
| L5 기술 | 7 | Critical |
| L6 정책 | 5 | Standard |
| L7 논리 | 8 | Standard |
| **v1.0 종합** | **하래 6.43** | **(45/7)** |

### v1.2 가중치 스코어링
| 항목 | 점수 | 가중치 | 가중치 적용 점수 |
|---|---|---|---|
| L1 출처 | 6 | 1.0x | 6.0 |
| L2 의도 | 7 | **1.5x** | 10.5 |
| L3 시장 | 5 | 1.0x | 5.0 |
| L4 고객 | 7 | **1.5x** | 10.5 |
| L5 기술 | 7 | **1.5x** | 10.5 |
| L6 정책 | 5 | 1.0x | 5.0 |
| L7 논리 | 8 | 1.0x | 8.0 |
| **v1.2 Weighted** | — | **/8.5** | **하래 6.53** |

**CRITICAL FLAG 확인:** L2=7, L4=7, L5=7 → 모두 8 미만 → FLAG 미발동

## ══ Trigger Engine 판정 결과 (Phase 4) ══

```
──────────────────────────────────────────────
[TRIGGER ENGINE v1.0 OUTPUT]
Risk Score (v1.0 단순평균): 6.43
Risk Zone:  🔴 RED
Gate:       BLOCKED
Action:     OPT-DCA Escalate
──────────────────────────────────────────────
[TRIGGER ENGINE v1.2 OUTPUT]
Weighted Score: 6.53 (CRITICAL Flag: 미발동, L2/L4/L5 모두 7로 기준값 8 미만)
Domain Threshold (SaaS): RED > 6.0
Risk Zone:  🔴 RED
Gate:       BLOCKED
Action:     OPT-DCA Escalate
──────────────────────────────────────────────
✔ v1.0 동일한 판정 — 구조적 문제(가업성 6.43, 가중 6.53) 확인 완료
⚠️ YELLOW-HEAVY 경계구역(4.5~6.0)에서 릴리시엉된 케이스 시
    v1.0는 단순평균으로 일괄 처리 → v1.2는 가중치로 사안 정확도 향상
```

## ══ Context Injection Packet (Phase 5) ══

```json
DD_TO_FIN_PACKET = {
  "entity":            "NovaMind AI",
  "stage":             "Series B",
  "domain":            "SaaS/AI",
  "dd_risk_score":     "6.53 (Weighted v1.2)",
  "dd_risk_flags":     ["L2: 창업자 세컨더리 $5M", "L4: 파이프라인 전환율 10%", "L5: API 래퍼를 독자 LLM로 허위 표기", "L7: Hockey-Stick 4x 괴리"],
  "valuation_claim":   "$120M Post-Money",
  "valuation_gap":     "ARR Multiple +50~150% 과대평가",
  "burn_rate":         "월 $1.8M",
  "runway":            "10개월 (부족)",
  "ltv_cac":           "2.1x (미달, 기준 3x)",
  "hockey_stick_flag": "있음 (4x 근거 부족)",
  "hidden_intent":     "유치자금 일부($5M) 창업자 세컨더리 목적으로 추정",
  "policy_risk":       "일본 AI 규제 인증 미확보 (로드맵만)",
  "pearl_dag":         "Hockey-Stick 성장 가정 → 높은 밸류에이션 → 세컨더리 기회 정당화"
}
```

## ══ 테스트 발견사항 + v1.2 개선 처방전 ══

| # | 발견사항 | v1.0 문제 | v1.2 해결 |
|---|---|---|---|
| 1 | Critical 항목 과소 반영 | L2/L4/L5 같은 가중 | 가중치 1.5x 적용 |
| 2 | YELLOW 단일 처리 경계 영역 블라인드 | YELLOW 엘리어 케이스도 HEAVY와 동일하게 Stress Test | YELLOW 2단계 분리 |
| 3 | 모든 도메인 동일 임계값 | 반도체 vs SaaS 진입장벽 동일 | Domain별 다른 임계값 |
| 4 | 단일 시해 항목 발겨 시 지연 차단 | 모든 항목 평시 후 종합 판단 | CRITICAL FLAG 우선 체크 |

## ══ 다음 테스트 케이스 권장 ══

| Priority | 케이스 유형 | 목적 |
|---|---|---|
| 항 1 | GREEN Zone (Score ~2.0) 제조업 | Stage×Domain 매트릭스 전체 검증 6 코드 |
| 항 2 | YELLOW-LIGHT SaaS 케이스 | 세럨한 조건부 게이트 동작 검증 |
| 항 3 | CRITICAL FLAG 발동 케이스 (L5=9) | 즉시 차단 동작 검증 |

## CHANGELOG
| 버전 | 날짜 | 내용 |
|---|---|---|
| v1.0 | 2026-05-07 | 최초 생성 — E2E 테스트 코퍼스 서류, Trigger Engine v1.0/v1.2 동시 실행 릴스어 비교 |
