# CASH-04: JV Fund Cash Management Prompt v1.0

> **도메인**: PE-CASH | **카테고리**: Applied Cases — JV Fund
> **버전**: v1.0 | **생성일**: 2026-05-06
> **연계**: FIN-06-BFA-JV | **PE-3 목표**: 90점↑

---

## 1. 프롬프트 목적 (Objective)

JV(Joint Venture) 구조의 사모펀드 현금관리 프레임워크를 구축한다.  
파트너사별 현금 기여(Capital Call) 및 인출(Distribution) 구조를 정밀 추적하고,  
MOIC·DPI와 연동한 현금흐름 시뮬레이션을 통해 펀드 운영 투명성을 확보한다.

---

## 2. 입력 변수 (Input Variables)

```yaml
JV_FUND_PARAMS:
  fund_name: "[JV 펀드명]"
  total_commitment: "[총 약정액, KRW]"
  partners:
    - name: "[LP-A]"
      commitment_ratio: 0.40
      preferred_return: 0.08
    - name: "[LP-B]"
      commitment_ratio: 0.35
      preferred_return: 0.08
    - name: "[GP]"
      commitment_ratio: 0.25
      carried_interest: 0.20
  investment_period: "[투자기간, 년]"
  harvest_period: "[회수기간, 년]"
  hurdle_rate: 0.08
  benchmark_moic: 2.0
  target_dpi: 1.5
```

---

## 3. 핵심 분석 모듈

### 3-1. Capital Call 추적 (파트너사별)

```
[분석 지시]
다음 Capital Call 스케줄을 파트너사 비율에 따라 배분하고,
누적 기여액 대비 잔여 약정 한도를 실시간 계산하라:

| 구분 | Call 일자 | 금액 | LP-A | LP-B | GP | 누적 Drawn % |
|------|-----------|------|------|------|----|-------------|
| 1차 Call | ... | ... | ... | ... | ... | ... |

- 미납 Capital Call 발생 시 Penalty Interest (연 {rate}%) 자동 산출
- Default 시나리오 (LP 불이행) → GP 대체 납입 메커니즘 시뮬레이션
```

### 3-2. Distribution Waterfall (현금 인출 우선순위)

```
[지시] 아래 Waterfall 구조로 배분 가능 현금을 순서대로 배정하라:

1단계: Return of Capital   → LP 원금 전액 반환
2단계: Preferred Return    → LP 우선수익 (Hurdle Rate: {hurdle_rate}%)
3단계: GP Catch-Up         → GP 수익 보전 (Carry 비율의 100% 도달까지)
4단계: Carried Interest    → 초과수익의 {carried_interest}%를 GP 배분
5단계: Residual Split      → 잔여 수익 파트너 비율 기준 최종 배분

→ 각 단계별 현금 배분액, 누적 DPI, 파트너사별 IRR 출력
```

### 3-3. MOIC·DPI 연동 시뮬레이션

```
[시뮬레이션 지시]
FIN-06-BFA-JV 데이터와 연동하여 다음 3개 시나리오를 현금흐름으로 변환:

Base Case:    MOIC {base_moic}x → 연도별 Distribution 스케줄 → DPI 도달 시점 예측
Upside Case:  MOIC {upside_moic}x → 조기 Exit 시 LP 실수령액 증가분 계산
Downside Case: MOIC {downside_moic}x → Capital Impairment 발생 시
               → LP 손실 배분 구조 (Clawback 조건 포함)

출력: 연도별 Cash-In/Cash-Out Matrix, TVPI/DPI/RVPI Progression Chart
```

---

## 4. 리스크 체크리스트

- [ ] **Currency Mismatch**: 해외 JV 시 환노출 현금흐름 헤지 여부 확인
- [ ] **Tax Leakage**: 국가별 원천징수세 (Withholding Tax) 배분 전 차감 처리
- [ ] **GP Clawback**: 초과 Carry 선지급 시 회수 조건 충족 여부
- [ ] **Key Man Clause**: 핵심 운용역 이탈 시 Capital Call 동결 조항 확인
- [ ] **Liquidity Gate**: LP 대규모 Redemption 요청 시 Gate 발동 임계치 설정

---

## 5. 출력 포맷 (Output Format)

```markdown
## JV Fund Cash Flow Summary — {fund_name}

### [A] Capital Call 현황
- 총 약정: {total_commitment:,}원
- 기 납입: {drawn_amount:,}원 ({drawn_pct:.1f}%)
- 잔여 Dry Powder: {remaining:,}원

### [B] Distribution 실적
- 총 배분: {total_dist:,}원
- 현재 DPI: {dpi:.2f}x
- 목표 DPI 달성 예상 시점: {target_date}

### [C] 파트너사별 수익 현황
| 파트너 | 기여액 | 수취액 | Net MOIC | IRR |
|--------|--------|--------|----------|-----|
| LP-A   | ...    | ...    | ...      | ... |
| LP-B   | ...    | ...    | ...      | ... |
| GP     | ...    | ...    | ...      | ... |

### [D] 조기경보 신호
- DPI < 0.5x at Year 4: ⚠️ 조기경보 발동
- Capital Call 미납 LP: 🚨 Default 프로세스 개시
```

---

## 6. 연계 시스템

| 연계 모듈 | 용도 | 방향 |
|-----------|------|------|
| FIN-06-BFA-JV | JV 재무분석 기반 데이터 공급 | ← 입력 |
| CASH-01 현금주기 | 운영 현금흐름 정규화 | ↔ 양방향 |
| CASH-02 유동성 | LP 인출 요청 유동성 충격 평가 | ← 입력 |
| CASH-03 최적화 | Dry Powder 운용 최적화 | → 출력 |
| PE-3 QC Engine | 프롬프트 품질 자동 검증 | ↑ 검증 |

---

## 7. PE-3 검증 기준

```yaml
PE3_VALIDATION:
  target_score: 90
  criteria:
    specificity:    20  # JV 구조 특수성 반영도
    completeness:   20  # Waterfall 5단계 완결성
    quantifiability: 20 # MOIC/DPI/IRR 수치 출력 가능성
    risk_coverage:  20  # 5대 리스크 체크리스트
    actionability:  20  # 실무 즉시 적용 가능성
  auto_validate: true
  linked_rules: ["CASH-RULE-01", "CASH-RULE-02", "CASH-RULE-06"]
```

---

*최종 업데이트: 2026-05-06 | 담당: GilbertKwak | 다음 검토: 2026-06-06*
