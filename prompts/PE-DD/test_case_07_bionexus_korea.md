# TC-07 | BioNexus Korea (BNK) — Bio/헬스케어 Series B 실전 검증

> **파일**: `prompts/PE-DD/test_case_07_bionexus_korea.md`  
> **등록 일시**: 2026-05-10  
> **검증 프롬프트**: OPT-DD-FIN v1.1 + DD-012 Bio/Pharma Module + Trigger Engine v1.3  
> **PE-3 Score**: 94/100  
> **SSOT 연계**: Notion PE-DD Library → PE-DD-03 / BN-01\~03 바인딩  

---

## 📋 검증 대상 개요

| 항목 | 내용 |
|---|---|
| **기업명** | BioNexus Korea (BNK) |
| **도메인** | Bio/헬스케어 — 항암 면역치료제 (CAR-T 플랫폼) |
| **투자 단계** | Series B (Pre-IPO) |
| **입력 자료** | IR Deck v3.2 + 임상 2상 중간 결과 보고서 + 기술 특허 포트폴리오 요약 |
| **검증 목적** | PE-DD Gate 통과 여부 판정 + PE-FIN IRR Hurdle 산출 |

---

## 🔎 7-Layer DD 분석 결과

| Layer | 분석 항목 | 점수 (0-10) | 주요 발견 |
|---|---|---|---|
| L1 출처 신뢰도 | IR Deck 자기 보고 + 미감사 임상 데이터 | 6.5 | 독립 감사 부재 — 조건부 신뢰 |
| L2 숨은 의도 | Series B 밸류에이션 극대화 목적 IR 구성 | 7.2 | TAM 과장 (+35%) 플래그 |
| L3 시장 현실 | 글로벌 CAR-T 시장 TAM $28B → BNK 주장 $45B | 5.8 | L7 내부 모순 교차 확인 |
| L4 고객 수요 | 병원 네트워크 MOU 3건 — WTP 미검증 | 6.0 | 계약 구속력 없는 LOI 수준 |
| **L5 기술 가능성** | CAR-T 임상 2상 ORR 62% (n=24, 단일 기관) | **8.1** ⚠️ | **소규모 단일 기관 — 다기관 재현 미확인 · FDA 패스트트랙 미획득** |
| **L6 정책·규제** | 식약처 조건부 허가 + FDA IND 진행 중 | **7.6** ⚠️ | **미국 임상 3상 CapEx $120M+ 미반영 · EMA 규제 불확실성** |
| L7 내부 논리 | 2028 BEP vs. 임상 타임라인 충돌 | 6.9 | BEP 달성 가정이 FDA 승인 전제 — 순환논리 |

**L5 + L6 이중 CRITICAL FLAG 발동** → BIO Module 페널티 자동 적용 (+0.8 RS 가산)

---

## 📊 Risk Register 산출

### BN-01 · Market Risk

| Risk ID | 리스크 | 유형 | 심각도 | RS 기여 |
|---|---|---|---|---|
| BN-01-BNK-01 | TAM 과장 — 실제 SAM $8.2B vs. 주장 $45B | [scale][market] | H | +0.9 |
| BN-01-BNK-02 | MOU 3건 → 실제 구매 계약 전환율 미검증 | [perf][market] | M | +0.5 |
| BN-01-BNK-03 | 경쟁사 (Kite/Novartis CAR-T) 가격 압박 | [scale][competitive] | H | +0.7 |

**BN-01 RS: 2.1** → 🟢 GREEN-LIGHT

### BN-02 · Technical Limit Risk

| Risk ID | 리스크 | 유형 | 심각도 | RS 기여 |
|---|---|---|---|---|
| BN-02-BNK-01 | 임상 2상 n=24 소규모 — 다기관 재현성 미확인 | [perf][theoretical] | **H** | +1.1 |
| BN-02-BNK-02 | CAR-T 생산 공정 스케일업 미검증 (현 배치 12건/월) | [perf][implementation] | H | +0.8 |
| BN-02-BNK-03 | CRS Grade 3+ 발생률 8.3% — 안전성 모니터링 필요 | [stability][clinical] | M | +0.6 |

**BN-02 RS: 2.5** → 🟢 GREEN-LIGHT

### BN-03 · Regulatory & Geo Risk

| Risk ID | 리스크 | 유형 | 심각도 | RS 기여 |
|---|---|---|---|---|
| BN-03-BNK-01 | FDA IND 진행 중 — 임상 3상 개시 불확실 | [scale][regulatory] | **H** | +1.4 |
| BN-03-BNK-02 | 미국 임상 3상 CapEx $120M 미반영 → 자금 갭 | [scale][regulatory] | **H** | +1.2 |
| BN-03-BNK-03 | IP 이전 구조 불명확 — 창업자 개인 특허 보유 의혹 | [scale][implementation] | H | +1.1 |
| BN-03-BNK-04 | EMA 규제 동향 — CAR-T 자동화 생산 규정 미확정 | [scale][regulatory] | M | +0.5 |

**BN-03 RS: 4.2** → 🟡 YELLOW-HEAVY

### BN 종합 판정

| BN | 도메인 | RS | Zone | PE-FIN 라우팅 |
|---|---|---|---|---|
| BN-01 Market | Bio/헬스케어 | **2.1** | 🟢 GREEN-LIGHT | FIN-05+01 |
| BN-02 Technical | Bio/딥테크 | **2.5** | 🟢 GREEN-LIGHT | FIN-09+02 CRITICAL 모니터링 |
| BN-03 Regulatory | Bio/지정학 | **4.2** | 🟡 YELLOW-HEAVY | PE-STRAT C-33 + FIN-04+09 |
| **가중 평균** | — | **4.21** (BIO Module +0.8 페널티 포함) | 🟡 **YELLOW-HEAVY** | FIN-04+09 복합 + PE-STRAT |

> **BIO Module 페널티 근거**: L5 ≥ 8.0 (임상 재현성 미확인) + L6 ≥ 7.5 (FDA 미승인 + CapEx 갭) → +0.8 RS 자동 가산

---

## 💰 PE-FIN IRR Gate 산출

| 항목 | 값 | 산출 근거 |
|---|---|---|
| **RS (Weighted)** | **4.21** | BN-01 × 0.25 + BN-02 × 0.35 + BN-03 × 0.40 + BIO 페널티 |
| **Base IRR Hurdle** | 25% | Bio Series B 기준선 |
| **RS 페널티** | +3.65% | RS 4.21 × 0.87%/pt |
| **IRR Hurdle (Final)** | **28.65%** | 투자 진행 최소 수익률 |
| **Max Entry EV** | **890억 원** | 14.2x Rev Multiple (YELLOW Zone 조정) |
| **Scenario Weight** | Conservative 40% / Base 40% / Optimistic 20% | RS ≥ 4.0 YELLOW-HEAVY 적용 |

---

## 🚦 최종 판정 & PE-DD Gate 결과

```
╔══════════════════════════════════════════════════════╗
║  TC-07 · BioNexus Korea (BNK) · Bio Series B         ║
║  RS (Weighted): 4.21  →  🟡 YELLOW-HEAVY             ║
║  IRR Hurdle:  28.65%  |  Max EV: 890억 (14.2x Rev)   ║
║  PE-DD Gate:  ⚠️ CONDITIONAL PASS                    ║
║  조건: FDA IND 업데이트 확인 + IP 이전 구조 정밀 검토 ║
╚══════════════════════════════════════════════════════╝
```

### 핵심 조건부 사항 (3가지)

1. **FDA IND 진행 현황** — 임상 3상 개시 전 IND 승인 확인서 제출 필수
2. **IP 이전 완결** — 창업자 개인 보유 특허 전량 법인 이전 + 법률 의견서 수령
3. **자금 조달 플랜** — $120M 임상 3상 CapEx 커버 가능한 후속 투자 로드맵 확인

### PE-FIN 자동 라우팅 명령어

```javascript
/dd-fin run TARGET="BioNexus Korea" STAGE="Series B" DOMAIN="BIO" \
  RS="4.21" ZONE="YELLOW-HEAVY" TRIGGER_ENGINE=ON \
  FIN_ROUTE="FIN-04+09" SCENARIO="conservative_heavy" \
  IRR_HURDLE="28.65" MAX_EV="890B_KRW" \
  CONDITION_FLAGS="FDA_IND|IP_TRANSFER|CAPEX_PLAN"
```

---

## 🏷️ 메타데이터

| 항목 | 값 |
|---|---|
| **TC ID** | TC-07 |
| **등록 일시** | 2026-05-10 |
| **검증 프롬프트** | OPT-DD-FIN v1.1 + DD-012 Bio/Pharma + Trigger Engine v1.3 |
| **PE-3 Score** | 94/100 |
| **RS** | 4.21 (YELLOW-HEAVY) |
| **IRR Hurdle** | 28.65% |
| **Max Entry EV** | 890억 원 (14.2x Rev) |
| **Gate 결과** | ⚠️ CONDITIONAL PASS |
| **Notion 연계** | PE-DD Library → PE-DD-03 |
| **이전 TC** | [TC-06](test_case_06_aiflow_analytics.md) |
