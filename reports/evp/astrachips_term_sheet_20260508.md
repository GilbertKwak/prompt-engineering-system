# AstraChips — Convertible Bond Term Sheet
**법무 검토 제출용 초안** | v1.0 | 2026-05-08

> **제출 기한**: 2026-05-15 | **법무 검토**: 필요
> **SSOT**: `prompts/PE-FIN/fin_07_evp.md` | **PE-3**: 93% ✅
> **Analyst**: Gilbert Kwak | **Fund**: AstraChips LP Fund
> **참조**: CB/Ratchet 설계서 `reports/evp/astrachips_cb_ratchet_20260508.md`

---

> ⚠️ **주의**: 본 Term Sheet는 투자 검토용 내부 초안입니다.
> 법적 구속력이 없으며, 컨파이덴션 후 정식 투자동의서(SPA/SHA) 로 교체됩니다.

---

## ■ PART 1. TRANSACTION OVERVIEW

| 항목 | 내용 |
|------|------|
| **Issuer** | AstraChips Inc. (이하 “회사”) |
| **Investor** | AstraChips LP Fund (이하 “투자자”) |
| **제도** | Convertible Bond (CB, 전환사채) |
| **투자 금액** | USD 65M ~ 130M (Tranche 구조, 협의 확정 시 지정) |
| **통화** | USD |
| **기준일** | 2026-05-08 |
| **제출 기한** | 2026-05-15 (법무 검토) |
| **목적** | Growth Equity 투자 — R&D 확대 / 영업 규모화 / IP 포트폸리오 강화 |

---

## ■ PART 2. CB 핵심 조건

### 2.1 기본 조건

| 조건 항목 | 설계값 | 비고 |
|---------|--------|------|
| **액면가** (Principal) | USD 65M ~ 130M | Tranche A: USD 65M (Close), Tranche B: USD 65M (Milestone) |
| **쿠폰 금리** | **3.5% p.a.** | 반년불 (Semi-annual), PIK 옵션 발행사 선택 |
| **만기** | **3년** | 2029-05-08 (Tranche A Close 기준) |
| **신탁** | Senior Unsecured |
| **준거법** | Delaware Law (State of Incorporation 확인 필요) |

### 2.2 Tranche 구조

| Tranche | 금액 | 실행 조건 | 타임라인 |
|---------|------|----------|----------|
| **Tranche A** | USD 65M | Close 컨디션 충족 시 | 2026-07-15 목표 |
| **Tranche B** | USD 65M | Milestone: 2026년 말 매출 USD 210M 달성 | 2027-Q1 조건부 |

---

## ■ PART 3. 전환 조건 (Conversion Terms)

### 3.1 전환가 (Conversion Price)

| 조건 | 수치 | 산출 근거 |
|------|------|----------|
| **기준 전환가** | **USD 8.50 / share** | Entry EV USD 950M ÷ 112M diluted shares |
| **Base 주당 가치 대비** | -15.3% 디스카운트 | Base 주당 USD 10.04 기준 (EVP 리포트) |
| **전환 주식 수** | USD 65M ÷ USD 8.50 = **7.647M shares** (Tranche A 기준) |

### 3.2 전환 권리

| 유형 | 조건 | 내용 |
|------|------|------|
| **임의 전환** | 언제든지 | 투자자 선택권 |
| **강제 전환** | IPO 공모가 ≥ USD 12.00 / share | P50 Base 달성 시 자동 전환 |
| **강제 전환 (M&A)** | M&A Exit EV ≥ USD 1,000M | Strategic Sale 시 자동 전환 |
| **전환 제한 기간** | 없음 | 만기까지 언제든지 행사 가능 |

### 3.3 가속 전환 조항 (Sweetener)

전환가 할인 주식 + 쿠폰 수령 동시 혜택 →
전환 실행 시 만기까지의 미수령 쿠폰 전액을 주식으로 전환하는 PIK 옵션 포함.

---

## ■ PART 4. PUT / CALL OPTION

### 4.1 Put Option (투자자 원금 보호)

| 항목 | 내용 |
|------|------|
| **행사 주체** | 투자자 |
| **행사 조건** | 만기일 (2029-05-08) 또는 Event of Default 발생 시 |
| **행사 금액** | 원금 + 누적 미지급 쿠폰 100% |
| **목적** | P10 시나리오 원금 손실 제로화 |

### 4.2 Call Option (발행사 콜 옵션)

| 항목 | 내용 |
|------|------|
| **행사 주체** | 발행사 (AstraChips) |
| **행사 가능 기간** | 발행 후 **2년 초과** (2028-07-15부터) |
| **행사 조건** | 주가 기준 전환가의 **130% 초과** (USD 11.05 / share) |
| **행사 금액** | 원금 + 누적 쿠폰 + **Call Premium 3%** |

### 4.3 Event of Default

| 사유 | 효과 |
|------|------|
| 지급불능 (원리금/쿠폰 30일 연체) | 전액 기한이익 출실 |
| 고의 보으 (Fraud) 확정 | 즉시 상환 청구권 |
| Change of Control (발행사 주식 50% 초과 이전) | 투자자 Put 제공 |
| 매출 2년 연속 전년 대비 -30% 이상 하락 | Ratchet 조항 자동 발동 |

---

## ■ PART 5. RATCHET 조항

### 5.1 IRR Ratchet

| IRR 실형 구간 | 투자자 추가 취득 지분 | 조정 후 총 지분율 |
|--------------|------------------|------------------|
| IRR ≥ 20% | 0%p (미발동) | 기준 지분율 유지 |
| 15% ≤ IRR < 20% | +1.5%p | 기준 + 1.5%p |
| 10% ≤ IRR < 15% | +3.0%p | 기준 + 3.0%p |
| **IRR < 10%** | **+5.0%p** | **기준 + 5.0%p** |

**주요 조건**:
- IRR 측정 기준일: 주식 툰스 (Exit, IPO, 기준일 중 빠른 날짜)
- 지분 조정 방식: 신규 주식 실점 발행 (Issuance of New Shares at par)
- IRR 계산 기준: USD-표시 Investment & Return (환율 헤지 미적용)
- 측정후 30일 이내 지분 이전 완료

### 5.2 MOIC Ratchet (전환가 하향 조정)

| MOIC 실형 구간 | 전환가 하향율 | 조정 후 전환가 |
|--------------|------------|----------------|
| MOIC ≥ 3.0× | 0% (미조정) | USD 8.50 |
| 2.0× ≤ MOIC < 3.0× | -10% | USD 7.65 |
| 1.5× ≤ MOIC < 2.0× | -20% | USD 6.80 |
| **MOIC < 1.5×** | **-30%** | **USD 5.95** |

**주요 조건**:
- MOIC 측정 기준: Gross MOIC (Fund 레벨, 코스트 차감 전)
- 전환가 조정은 다음 전환 시점에 적용
- IRR Ratchet과 MOIC Ratchet 중의 **투자자 유리한 조항 적용** (Not cumulative)

---

## ■ PART 6. ANTI-DILUTION

| 항목 | 내용 |
|------|------|
| **방식** | **Weighted-Average Broad-Based** |
| **발동 조건** | 후속 투자 발행가 < 기준 전환가 USD 8.50 (Down-round 방어) |
| **조정 공식** | CP_new = CP_old × (OS_old + Shares_at_CP) / (OS_old + New_Shares_issued) |
| **Carve-out (예외)** | ESOP 풀 확대 (Board 승인, 총 지분의 10% 이내), 기존 투자자 Pro-rata 형사권 |
| **Full-Ratchet 금지** | Full-Ratchet 방식 절충 불가 |

---

## ■ PART 7. 투자자 보호 조항

### 7.1 Information Rights

| 업데이트 유형 | 주기 | 전달 기한 | 형식 |
|------------|------|----------|------|
| 월간 KPI (매출/소진/현금) | 월간 | 다음 달 15일 | 요약표 |
| 분기 관리회계 (Mgmt Accounts) | 분기 | 다음 달 30일 | GAAP 준수 |
| 연간 감사보고서 (Audited) | 연간 | 4월 30일 | Big4 쫐사 |
| 예산 & 로드맵 | 연간 | 12월 15일 (전년도) | 이사회 승인본 |
| M&A / IPO / 주요 계약 | 이벤트 내 | 5영업일 이내 | 싦시고지 |

### 7.2 Board Observer

- 투자자는 이사회에 **1석 Observer** 파견 권리 (의결권 없음)
- Observer는 모든 이사회에 참석하며 자료를 이사와 동시에 수령
- Conflict of Interest 시스템으로 참석 제한 가능
- 투자 지분율이 5% 미만으로 하락 시 자동 소멸

### 7.3 승인권 (Consent Rights)

다음 이벤트는 투자자 서면 성동 필요:
- **후속 투자 라운드** (USD 50M 초과 신규 발행)
- **지분 가중 희석** (3% 초과 영리하 로 10%+ 에문의 희석화)
- **핵심 IP 양도** 또는 라이선스 (HBM 인터페이스 특허 포함)
- **설립자 / CTO 핵심 인력 계약 종료** (고의해지 제외)
- **부소 / 자회사 체인지 외 주요 자산 매각** (USD 5M 초과)

### 7.4 Drag-Along / Tag-Along

| 유형 | 조건 | 내용 |
|------|------|------|
| **Tag-Along** | M&A Exit 시 | 투자자는 동등 조건으로 함께 매각할 권리 |
| **Drag-Along** | 다수주주 (>50%) 상정 시 | 커버너스 조항 포함 시에만 적용 |
| **ROFR** | 주주 간 주식 양도 시 | 발행사 먼저, 투자자 다음 우선매수권 |

---

## ■ PART 8. 운용 용도 제한 (Use of Proceeds)

| 항목 | 금액 | 비율 |
|------|------|------|
| R&D 확대 (HBM IF IP 강화) | USD 25M | 38% |
| 영업팀 인원 확대 (Hyperscaler 타겟팀) | USD 15M | 23% |
| 타이튰짜량 확보 (TSMC CoWoS) | USD 15M | 23% |
| 운전자본 보강 | USD 10M | 16% |
| **합계 (Tranche A)** | **USD 65M** | **100%** |

---

## ■ PART 9. 체제 요건 & 클로징 컨디션

### 9.1 장적시행 요건 (Conditions Precedent)

| # | 요건 | 담당 |
|---|------|------|
| 1 | 주주 투자 계약 (SHA) 체결 및 사본 제출 | 법무 |
| 2 | 회사 정관 확인 (Certificate of Incorporation) | 법무 |
| 3 | IP 수유 현황 확인 (Patent Schedule 첨부) | DD |
| 4 | 재무제표 (3년치 + 최근 분기) 제선 | DD |
| 5 | 경영진 한도 확인 (Key Person 종료 금지 Lock-up) | 법무 |
| 6 | 기존 주주 동의서 (Existing Investor Consent) | 법무 |
| 7 | 거래 규제 승인 (CFIUS / 해당 시) | 규제 |
| 8 | Material Adverse Change (MAC) 미발생 | DD |

### 9.2 Closing 타임라인

| 단계 | 기간 | 담당 |
|------|------|------|
| Term Sheet 제시 | 2026-05-08 | Gilbert |
| 법무 검토 제출 | **2026-05-15** | 법무팀 |
| LOI / MOU 체결 | 2026-05-20 | 양사 |
| Due Diligence 완료 | 2026-06-15 | DD 팀 |
| SHA / SPA 작성 | 2026-06-15 ~ 07-15 | 법무 |
| 최종 컨파이메이션 | 2026-07-15 | 양사 |
| **Tranche A Close** | **2026-07-15** | Fund Admin |
| Tranche B (Milestone 확인 후) | 2027-Q1 | Gilbert |

---

## ■ PART 10. 기타 조항

| 조항 | 내용 |
|------|------|
| **독점협상 (Exclusivity)** | Term Sheet 서명일로부터 **45일** 동안 제3자 투자자 마케팅 금지 |
| **비밀유지 (NDA)** | 기체결 독립 NDA 요청, 본 Term Sheet는 NDA 담보 |
| **비용 부담** | 양사 자부담 (단, DD 공통요청 실사의로 비용은 회사 부담) |
| **준거법** | Delaware 주법 (State Court 관할) |
| **분쟁해결** | 중재 (AAA Rules, 뉴욕) |
| **양도금지** | Close 전 투자자 사전 동의 없이 CB 양도 불가 |
| **보안성** | 본 Term Sheet는 기밀이며 내부 배포 제한 |

---

## ■ PART 11. 서명 & 제출

### 투자자 (AstraChips LP Fund)

```
서명: ________________________________
재리자: Gilbert Kwak
날짜: 2026-05-08
연락처: [gilbert@astrachips-fund.com]
```

### 발행사 (AstraChips Inc.)

```
서명: ________________________________
재리자: [CEO 이름]
날짜: __________________
연락처: [legal@astrachips.com]
```

---

## ■ PART 12. 법무 검토 체크리스트

| 위험 영역 | 검토 포인트 | 우선순위 |
|----------|----------|----------|
| **CB 구조** | 전환가 디스카운트 적정성 / 쿠폰 겹제미 선정 | 포커스 |
| **Ratchet 조항** | IRR 측정 근거 명확화 / Dilution 상한 검토 | 포커스 |
| **Anti-Dilution** | Broad-Based 공식 적용 범위 확인 | 포커스 |
| **Event of Default** | 매출 조항 트리거 값 적정성 토론 | 높음 |
| **CFIUS 리스크** | 미국 반도체 산업 대상 제약 여부 | 높음 |
| **세무** | CB 이자 소득 경인, 전환사채 데인 계산 | 중등 |
| **노동 / IP** | 핵심 인력 Lock-up 기간 적정성 | 높음 |

---

## 📋 버전 이력

| 버전 | 날짜 | 내용 | 작성자 |
|------|------|------|--------|
| v1.0 | 2026-05-08 | 최초 초안 (법무 검토 제출용) | Gilbert Kwak |

---
*SSOT: `prompts/PE-FIN/fin_07_evp.md` | CB/Ratchet: `reports/evp/astrachips_cb_ratchet_20260508.md`*
*다음 단계: 법무 검토 후 v1.1 린터치 배포 (2026-05-15 목표)*
