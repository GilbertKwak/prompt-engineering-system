# PE-3 × ISSB S2 조인트 체크포인트 + SLB Step-Up 자동화

> **ID**: `FIN-PE3-ISSB-SLB` | **버전**: v1.0 | **작성일**: 2026-05-08  
> **연동**: FIN-SNBS-v4.0-ESG-OPT × FIN-MSIA-ESG v1.1 × PE-3 Validation Engine  
> **핵심 목표**: T+36M PE-3≥95점 AND ISSB S2≥78점 동시 달성 → SLB step-up 회피  
> **SLB 규모**: $200M | **Base Coupon**: 4.5% | **Investment Score**: 94.22/100 (A)

---

## ISSB S2 6-항목 점수 경로 (T+0 → T+60M)

| 항목 | 배점 | T+0 (Now) | T+6M | T+12M | T+24M | T+36M ★ | T+60M 목표 |
|---|---|---|---|---|---|---|---|
| ① Governance | /20 | 9.0 | 52.0 | 65.0 | 75.0 | 85.0 | 18.0 |
| ② Strategy | /20 | 9.9 | 53.0 | 67.0 | 77.0 | 87.0 | 18.0 |
| ③ Risk Management | /20 | 8.1 | 50.0 | 64.0 | 74.0 | 84.0 | 18.0 |
| ④ Metrics & Targets | /20 | 9.0 | 51.0 | 66.0 | 78.0 | 88.0 | 18.0 |
| ⑤ Transition Plan | /10 | 4.5 | 10.0 | 13.0 | 15.0 | 17.0 | 9.0 |
| ⑥ Physical Risk | /10 | 4.5 | 10.0 | 13.0 | 15.0 | 17.0 | 9.0 |
| **합계** | **/100** | **45.0** | 226→**50** | 288→**65** | 334→**72** | **78** ★ | **85+** |

> 해석 등급: 85+ = Ready · 65~84 = Partial · 40~64 = **Developing(현재)** · <40 = Non-Compliant

---

## 마일스톤별 체크포인트 전체 로드맵

| 마일스톤 | 날짜 | ISSB 목표 | 상태 및 핵심 KPI | SLB 트리거 조건 |
|---|---|---|---|---|
| T+0 | 2026-05 | 45점 | 베이스라인 측정. Scope 3 데이터 수집 착수 | 없음 |
| T+6M | 2026-11 | 50점 | Gap 분석 완료 + Scope 3 공시 초안 | 없음 |
| T+12M | 2027-05 | **65점** | KPI 1차: GHG 50,000t↓ \| VVB 제3자 검증 완료 | **GHG<50,000t → SLB +25bps** |
| T+24M | 2028-05 | 72점 | EU Taxonomy Aligned 확보 \| G-DETECT 재스캔 | ISSB<70 → PE-3 경고 발령 |
| **T+36M** | **2029-05** | **78점** ★ | **PE-3 × ISSB 조인트 검증 \| K-ETS 35,000t** | **ISSB<78 → SLB +50bps 자동트리거** |
| T+48M | 2030-05 | 82점 | SBTi 승인 목표 \| CBAM Savings $4.2M 확인 | SBTi 미승인 → LP 경보 발송 |
| T+60M | 2031-05 | **85+점** | ISSB S2 Ready \| SLB 만기 전 최종 검증 | **ISSB<85 → +100bps 또는 조기상환** |

---

## T+36M 조인트 검증 — PE-3 × ISSB S2 분기 트리

```
[T+36M 조인트 검증 실행]
        │
        ├─► PE-3 Score ≥95점?
        │       │
        │       ├─[YES]─► ISSB S2 ≥78점?
        │       │               │
        │       │               ├─[YES]─► ✅ BEST: Step-Up 없음
        │       │               │         IRR 88.51% 완전 유지
        │       │               │
        │       │               └─[NO]──► ⚠️  SLB +50bps 자동 트리거
        │       │                         비용 +$1.0M/yr | IRR -0.50pp
        │       │                         30일 이내 Action Plan 제출
        │       │
        │       └─[NO]──► ISSB S2 ≥78점?
        │                       │
        │                       ├─[YES]─► 🔶 PE-3 재검증 30일 유예
        │                       │         IRR -0.3%p 일시적
        │                       │
        │                       └─[NO]──► 🔴 Double: +50bps + PE-3 경고
        │                                 IRR -0.8%p | LP 통보 의무
        │
        └─► Extreme (ISSB<65 + PE-3 Fail)
                    +100bps 자동 + LP 즉시 통보
                    IRR -1.5%p 이상 | FIN-02 헤지 재검토
```

---

## SLB Step-Up 시나리오별 비용 및 IRR 영향

| 시나리오 | 스프레드 | 연간 비용 | 5년 누적 | IRR 충격 | Score | Grade |
|---|---|---|---|---|---|---|
| Base (전 KPI 달성) | 0bps | $0M | $0M | 0.00pp | **94.22** | **A** |
| Step-Up 1 (T+12M 미달) | +25bps | $0.5M | $2.5M | -0.25pp | **94.22** | **A** |
| Step-Up 2 (T+36M ISSB<78) | +50bps | $1.0M | $5.0M | -0.50pp | **94.22** | **A** |
| Double (T+12M+T+36M) | +75bps | $1.5M | $7.5M | -0.75pp | **94.22** | **A** |
| Max (T+60M ISSB<85) | +100bps | $2.0M | $10.0M | -1.00pp | **94.22** | **A** |

> ✅ **핵심 결론**: SLB Max Step-Up(+100bps, 5년 누적 $10M) 충격에서도  
> Investment Score **94.22점 (Grade A) 완전 유지** — IRR 버퍼 충분.

---

## 자동화 트리거 구현 명세 (Python 연동)

```python
# fin_pe3_issb_slb_trigger.py
class SLBStepUpEngine:
    """
    PE-3 × ISSB S2 조인트 체크포인트 자동화 엔진
    연동: FIN-MSIA-ESG v1.1 Step7 + FIN-SNBS-v4.0-ESG-OPT
    """
    THRESHOLDS = {
        "T+12M": {"ghg_reduction": 50_000, "issb_score": 60, "pe3_score": 90},
        "T+24M": {"issb_score": 70,  "pe3_score": 92},
        "T+36M": {"issb_score": 78,  "pe3_score": 95},  # ★ 핵심
        "T+48M": {"issb_score": 82,  "pe3_score": 95, "sbti_approved": True},
        "T+60M": {"issb_score": 85,  "pe3_score": 95},
    }
    STEP_UP = {
        "ghg_miss":   0.0025,   # +25bps
        "issb_miss":  0.0050,   # +50bps
        "pe3_miss":   0.0000,   # 유예 (30일)
        "double":     0.0075,   # +75bps
        "extreme":    0.0100,   # +100bps
    }
    SLB_PRINCIPAL = 200_000_000

    def evaluate(self, milestone: str, actuals: dict) -> dict:
        th = self.THRESHOLDS[milestone]
        issb_ok  = actuals.get("issb_score", 0)  >= th.get("issb_score", 0)
        pe3_ok   = actuals.get("pe3_score",  0)  >= th.get("pe3_score",  0)
        ghg_ok   = actuals.get("ghg_reduction", 999_999) >= th.get("ghg_reduction", 0)

        spread = 0.0
        actions = []
        if milestone == "T+12M" and not ghg_ok:
            spread += self.STEP_UP["ghg_miss"]
            actions.append("SLB +25bps: GHG T+12M 미달")
        if not issb_ok and not pe3_ok:
            spread += self.STEP_UP["double"]
            actions.append(f"SLB +75bps Double: ISSB+PE-3 동시미달")
        elif not issb_ok:
            spread += self.STEP_UP["issb_miss"]
            actions.append(f"SLB +50bps: ISSB {actuals.get('issb_score')} < {th['issb_score']}")
        elif not pe3_ok:
            actions.append("PE-3 재검증 30일 유예 (쿠폰 변동 없음)")
        if actuals.get("issb_score", 100) < 65 and not pe3_ok:
            spread = self.STEP_UP["extreme"]
            actions = ["SLB +100bps Extreme + LP 즉시 통보"]

        annual_penalty = self.SLB_PRINCIPAL * spread / 1e6
        return {
            "milestone": milestone,
            "spread_bps": spread * 10000,
            "annual_penalty_M": annual_penalty,
            "actions": actions,
            "grade": "PASS" if spread == 0 else "TRIGGER",
        }

# 실행 예시 — T+36M 검증
engine = SLBStepUpEngine()
result = engine.evaluate("T+36M", {"issb_score": 75, "pe3_score": 96})
# → ISSB 미달(75<78): SLB +50bps 자동 트리거, 연간 $1.0M 페널티
```

---

## PE-3 검증 연동 자동화 명령어

```bash
# T+36M 조인트 검증 실행
python automation/auto_validate.py \
  --file prompts/applied-cases/investment-decision/fin_snbs_v4.0_esg_optimal.md \
  --rules PE-1,PE-3,E-09 \
  --checkpoint T+36M \
  --issb-actual 78 \
  --pe3-actual 95 \
  --slb-engine ON \
  --slb-principal 200000000 \
  --slb-base-coupon 0.045

# SLB 트리거 시뮬레이션 (ISSB 미달 시나리오)
python automation/slb_trigger_sim.py \
  --milestone T+36M \
  --issb-score 72 \
  --pe3-score 96 \
  --action simulate

# 전체 로드맵 모니터링 (T+0 → T+60M)
python automation/issb_roadmap_monitor.py \
  --config fin_pe3_issb_slb_checkpoint.md \
  --notify slack,notion \
  --auto-trigger slb
```

---

## 크로스 레퍼런스

| 시스템 | 역할 |
|---|---|
| FIN-MSIA-ESG v1.1 | Step2[3C] ISSB S2 스코어링 엔진 + Step7 Impact KPI Roadmap |
| FIN-SNBS-v4.0-ESG-OPT | 모든 Bear 시나리오 Score 기준 (94.22/100, A) |
| PE-3 Validation Engine | T+36M 조인트 체크포인트 1차 게이트 |
| FIN-02 | SLB Extreme 시 에너지 헤지 자동 재검토 연동 |
| G-DETECT Module | T+12M / T+24M G1·G4 플래그 재스캔 의무 |
| IRIS+ v5.0 | PI7515(GHG) / PI5556(ISSB) KPI 측정 표준 |
| SBTi | T+48M 승인 목표 — 미달 시 LP 경보 트리거 |

---

## 변경 이력

| 버전 | 날짜 | 주요 변경 |
|---|---|---|
| v1.0 | 2026-05-08 | 최초 작성. PE-3 × ISSB S2 조인트 체크포인트 + SLB step-up 자동화 설계 |
