# AstraChips — Convertible Bond Term Sheet
**법무 검토 제출용 심층 확장본** | **v2.0** | 2026-05-08

> **제출 기한**: 2026-05-15 | **법무 검토**: 필요
> **SSOT**: `prompts/PE-FIN/fin_07_evp.md` | **PE-3**: 95% ✅
> **Analyst**: Gilbert Kwak | **Fund**: AstraChips LP Fund
> **참조**: CB/Ratchet 설계서 `reports/evp/astrachips_cb_ratchet_20260508.md`
> **PE-7 자동화 오류 수정**: E-01~E-10 반영 완료

---

> ⚠️ **주의**: 본 Term Sheet는 투자 검토용 내부 초안입니다.
> 법적 구속력이 없으며, 컨파이메이션 후 정식 투자동의서(SPA/SHA)로 교체됩니다.

---

## PE-7 오류 예측 & 사전 수정 로그 (v1.0 → v2.0)

| # | v1.0 오류/Gap | v2.0 수정 내용 | 위험도 |
|---|-------------|------------|------|
| E-01 | `타이트질량 확보` 오타 | **파운드리 물량 확보 (TSMC CoWoS)** 로 정정 | 🔴 |
| E-02 | `신탁: Senior Unsecured` 오용 표기 | **담보순위: Senior Unsecured Note** 로 정정 | 🔴 |
| E-03 | `기한이익 출실` 오타 | **기한이익 상실(喪失)** 로 정정 | 🟠 |
| E-04 | IRR 측정 기준일 미정의 | **투자 회수 완료일(Exit Date) 기준 XIRR** 명시 | 🔴 |
| E-05 | Ratchet 중복 발동 처리 규정 없음 | **투자자 유리 단일 조항 적용 (Not Cumulative)** 명문화 | 🔴 |
| E-06 | Tranche B Milestone 검증 주체 미정 | **독립 회계법인(Big4) 검증** 명시 | 🟠 |
| E-07 | Use of Proceeds 변경 절차 미정 | **투자자 사전 서면 동의 + 이사회 결의** 필요 명시 | 🟠 |
| E-08 | CFIUS 대응 절차 없음 | **CFIUS 클리어런스 Closing CP 항목 추가** | 🔴 |
| E-09 | Board Observer 소멸 조건 불완전 | **분기 KPI 3회 연속 미달 시 Observer 추가 권리 부여** 추가 | 🟠 |
| E-10 | FIN-02 자동 모니터링 연계 조항 없음 | **Section 12. FIN-02 연동 조항 신설** | 🟠 |

---

## ■ PART 1. TRANSACTION OVERVIEW

| 항목 | 내용 |
|------|------|
| **Issuer** | AstraChips Inc. (Delaware C-Corp) |
| **Investor** | AstraChips LP Fund (GP: Gilbert Kwak) |
| **공동 투자자** | [Co-Investor 여부 — DD 중 확인] |
| **제도** | Convertible Bond (CB, 전환사채) — Senior Unsecured Note |
| **투자 금액** | USD 65M (Tranche A) + USD 65M (Tranche B) = **최대 USD 130M** |
| **통화** | USD (환율 헤지 미적용, 환율 리스크 양사 부담) |
| **기준일** | 2026-05-08 |
| **제출 기한** | 2026-05-15 (법무 검토) |
| **Post-Money Valuation (Tranche A)** | Entry EV USD 950M + USD 65M = **USD 1,015M** |
| **Exit 목표** | 2029~2031년 IPO 또는 Strategic M&A |
| **목적** | HBM Interface IP 강화 · Hyperscaler 영업 확대 · TSMC CoWoS 물량 확보 · 운전자본 보강 |

---

## ■ PART 2. CB 핵심 조건

### 2.1 기본 조건

| 조건 항목 | 설계값 | 협상 레드라인 | 산출 근거 |
|---------|--------|------------|--------|
| **액면가 (Tranche A)** | USD 65M | 최소 USD 50M | IRR 민감도 분석 기반 |
| **액면가 (Tranche B)** | USD 65M | 최소 USD 40M | Milestone 조건부 |
| **쿠폰 금리** | **3.5% p.a.** | 최저 2.5% | HY Index 기준, 전환옵션 가치 차감 |
| **이자 지급 방식** | 반년불 (Semi-annual) | PIK 옵션은 발행사 선택권 | Cash 우선, PIK 허용 |
| **만기** | **3년** (2029-05-08) | 최장 4년 | IPO 전 Exit 가정 |
| **담보순위** | Senior Unsecured Note | Secured 절대 불가 | 기존 부채 구조 확인 후 |
| **준거법** | Delaware 주법 | 변경 불가 | AstraChips 설립지 기준 |

### 2.2 전환가 상세

| 조건 | 수치 | 산출 근거 |
|------|------|----------|
| **기준 전환가** | **USD 8.50 / share** | Entry EV USD 950M ÷ 112M diluted shares |
| **Base 주당 가치 대비** | -15.3% 디스카운트 | Base 주당 USD 10.04 기준 (EVP 리포트) |
| **전환 주식수 (Tranche A)** | USD 65M ÷ USD 8.50 = **7,647,059 shares** | Fully Diluted 기준 약 6.4% |
| **전환 주식수 (Tranche B)** | USD 65M ÷ USD 8.50 = **7,647,059 shares** | 추가 약 5.7% (Ratchet 전) |

### 2.3 전환 권리

| 유형 | 조건 | 전환 주체 |
|------|------|----------|
| **임의 전환** | 언제든지 가능 | 투자자 선택 |
| **자동 강제 전환 (IPO)** | IPO 공모가 ≥ USD 12.00 / share | 자동 |
| **자동 강제 전환 (M&A)** | M&A Exit EV ≥ USD 1,000M | 자동 |
| **Call 행사 시 전환 선택** | 발행사 Call 통보 후 15영업일 이내 | 투자자 선택 |

---

## ■ PART 3. Tranche 구조

| 항목 | Tranche A | Tranche B |
|------|---------|----------|
| **금액** | USD 65M | USD 65M |
| **실행 조건** | Closing Conditions 충족 | Milestone 달성 독립 검증 |
| **Milestone** | CP 충족 (8개 항목) | **2026년 말 매출 USD 210M** |
| **타임라인** | 2026-07-15 목표 | 2027-Q1 (최장 2027-06-30) |
| **검증 주체** | — | **독립 회계법인(Big4: PwC/Deloitte/EY/KPMG 중 1개)** |
| **검증 기간** | — | Milestone 확정일 후 **45일 이내** |
| **Milestone 미달 시** | — | Tranche B 자동 소멸 또는 투자자 재협상 권리 |

---

## ■ PART 4. PUT / CALL OPTION

### 4.1 Put Option (투자자 원금 보호)

| 항목 | 내용 |
|------|------|
| **행사 주체** | 투자자 (AstraChips LP Fund) |
| **행사 조건 ①** | 만기일 (2029-05-08) |
| **행사 조건 ②** | Event of Default 발생 후 10영업일 이내 미치유 |
| **행사 조건 ③** | IPO 미달성 (만기 시까지 IPO 미진행) |
| **행사 금액** | 원금 100% + 누적 미지급 쿠폰 전액 |
| **지급 기한** | Put 행사 통보 후 **30영업일 이내** |
| **지급 불이행 시** | 연체 이자 Prime Rate + 2% 부과 |

### 4.2 Call Option (발행사)

| 항목 | 내용 |
|------|------|
| **행사 주체** | 발행사 (AstraChips Inc.) |
| **행사 가능 시점** | 발행 후 **24개월 초과** (2028-07-15부터) |
| **행사 조건** | 연속 **20 거래일** 주가 ≥ USD 11.05 (전환가 × 130%) |
| **행사 금액** | 원금 + 누적 쿠폰 + **Call Premium 3%** |
| **투자자 선택권** | Call 통보 후 **15영업일 이내** 전환 또는 상환 선택 |

### 4.3 Event of Default (상세화)

| # | EoD 사유 | 유예 기간 | 효과 |
|---|---------|---------|------|
| 1 | 이자 미지급 | 30일 | 전액 기한이익 **상실(喪失)** |
| 2 | 원금 상환 불이행 | 5영업일 | 전액 즉시 상환 청구권 |
| 3 | 고의 보우(Fraud) / 중요 허위진술 | 없음 (즉시) | 즉시 상환 청구권 + 손해배상 |
| 4 | Change of Control (주식 50% 초과 이전) | 30일 투자자 선택 | 투자자 Put 또는 전환 선택 |
| 5 | 매출 2년 연속 전년 대비 -30% 이상 하락 | 다음 분기 KPI 확인 | Ratchet 조항 자동 발동 |
| 6 | 핵심 IP 무단 양도 (투자자 동의 없음) | 없음 (즉시) | 즉시 상환 청구권 + 금지청구 |
| 7 | 파산 신청 / 청산 결의 | 없음 (즉시) | 전액 즉시 상환 청구권 |
| 8 | 준거 법규 중대 위반 (OFAC, CFIUS 등) | 60일 치유 | 치유 불가 시 Put 행사 |

---

## ■ PART 5. RATCHET 조항

### 5.1 IRR Ratchet — IRR 측정 기준 명확화 (E-04 수정)

**IRR 측정 정의**:
- **측정 시점**: 투자 회수 완료일(Exit Date) — 주식 매각 완료, IPO Lock-up 해제, Put 상환 완료 중 가장 빠른 날
- **계산 방식**: XIRR 함수 적용 (현금흐름 가중 내부수익률, USD 기준)
- **검증 주체**: 독립 회계법인 (양사 합의, 분쟁 시 제3 Big4 결정)
- **검증 기간**: 회수 완료 후 60일 이내
- **지분 이전**: 측정 확정 후 30일 이내 완료

| IRR 실형 구간 | 추가 취득 지분 | 적용 |
|------------|------------|------|
| IRR ≥ 20% | 0%p | 미발동 |
| 15% ≤ IRR < 20% | +1.5%p | 경미 발동 |
| 10% ≤ IRR < 15% | +3.0%p | 발동 |
| **IRR < 10%** | **+5.0%p** | **강발동 (P10 해당)** |

> P10 적용 시: 기준 지분율 10% + 5.0%p = **15.0%** → 실효 IRR 12.1% (WACC 11.0% 상회 ✅)

### 5.2 MOIC Ratchet

| MOIC 실형 구간 | 전환가 하향률 | 조정 전환가 |
|-------------|-----------|----------|
| MOIC ≥ 3.0× | 0% | USD 8.50 |
| 2.0× ≤ MOIC < 3.0× | -10% | USD 7.65 |
| 1.5× ≤ MOIC < 2.0× | -20% | USD 6.80 |
| **MOIC < 1.5×** | **-30%** | **USD 5.95** |

### 5.3 Ratchet 중복 발동 처리 (E-05 수정)

- IRR Ratchet과 MOIC Ratchet **동시 발동 시** → **투자자에게 유리한 단일 조항만 적용 (Not Cumulative)**
- 중복 누적 적용 절대 금지 — 투자자 선택으로 어느 하나만 행사

---

## ■ PART 6. ANTI-DILUTION

| 항목 | 내용 |
|------|------|
| **방식** | **Weighted-Average Broad-Based** |
| **발동 조건** | 후속 투자 발행가 < 전환가 USD 8.50 (Down-round 방어) |
| **조정 공식** | CP_new = CP_old × (OS_old + Agg.Consideration/CP_old) / (OS_old + New_Shares_Issued) |
| **Broad-Based 기준** | Fully Diluted Cap Table 전체 기준 (ESOP 포함) |
| **Full-Ratchet 금지** | Full-Ratchet 방식 어떠한 상황에서도 절대 불허 |
| **Carve-out ①** | ESOP 풀 확대 (이사회 승인, 총 지분의 10% 이내) |
| **Carve-out ②** | 기존 투자자 Pro-rata 형사권 행사 (지분 유지 목적) |
| **Carve-out ③** | 전략적 파트너십 주식 발행 (이사회 + 투자자 동의, 총 지분 3% 이내) |
| **Carve-out ④** | CB 전환 실행 자체 (자기 참조 제외) |

---

## ■ PART 7. 투자자 보호 조항

### 7.1 Information Rights

| 보고 유형 | 주기 | 전달 기한 | 형식 | 미제출 시 패널티 |
|---------|------|---------|------|-------------|
| 월간 KPI 대시보드 | 월간 | 다음 달 **15일** | 표준 템플릿 | 경고 → 3회 미달 시 Board Meeting 소집 권리 |
| 분기 관리회계 (GAAP) | 분기 | 다음 달 **30일** | GAAP 준수, 전분기 대비 분석 포함 | 경고 → 2회 미달 시 EoD 가능성 검토 |
| 연간 감사보고서 | 연간 | **4월 30일** | Big4 감사 의견 포함 | 60일 초과 시 EoD 트리거 검토 |
| 예산 & 사업 로드맵 | 연간 | **12월 15일** (전년도) | 이사회 승인본 | — |
| M&A / IPO / 주요 계약 | 이벤트 내 | **5영업일 이내** | 즉시 통보 | 미통보 시 동의권 행사 간주 취소 |
| FIN-02 KPI 알림 (자동) | 실시간 | 발동 즉시 | 자동화 파이프라인 연동 | — |

### 7.2 Board Observer (E-09 수정 — 강화)

| 항목 | 내용 |
|------|------|
| **Observer 수** | 1석 (기본) |
| **조건부 추가 권리** | 분기별 KPI 3회 연속 미달 시 추가 1석 권리 부여 |
| **의결권** | 없음 |
| **자료 수령** | 이사와 동시 + FIN-02 자동 알림 수신 |
| **소멸 조건** | 지분 5% 미만 OR 투자자 자발적 포기 |

### 7.3 승인권 (Consent Rights)

| # | 이벤트 | 최저 기준값 |
|---|--------|----------|
| 1 | 후속 투자 신규 발행 | USD 50M 초과 |
| 2 | 핵심 IP 양도 / 라이선스 | HBM 인터페이스 특허 포함 |
| 3 | 설립자 / CTO 핵심 인력 계약 종료 | 고의 해지 제외 |
| 4 | 주요 자산 매각 / 담보 설정 | USD 5M 초과 |
| 5 | M&A / 합병 / 분사 | 규모 무관 |
| 6 | 배당 선언 / 자사주 매입 | Close 후 IPO 전 전면 금지 |
| 7 | 기업 지배구조 변경 (정관 개정) | CB 투자자 권리 영향 시 |
| 8 | Use of Proceeds 허용 범위 초과 변경 | 항목별 기준 초과 시 |

### 7.4 Drag-Along / Tag-Along / ROFR

| 유형 | 발동 조건 | 세부 내용 |
|------|---------|----------|
| **Tag-Along** | M&A Exit 시 | 동등 조건(가격·구조·시기)으로 함께 매각 권리 |
| **Drag-Along** | 다수주주(>50%) 합의 시 | 거버넌스 조항 포함 + 투자자 최소 회수 보장 전제 |
| **ROFR** | 주주 간 주식 양도 시 | 발행사 먼저(10영업일) → 투자자 다음(10영업일) |
| **Pro-rata Right** | 후속 투자 라운드 | 기존 지분율 유지를 위한 참여 권리 |

---

## ■ PART 8. 운용 용도 제한 (Use of Proceeds) — E-07 수정

| 항목 | Tranche A | 비율 | 변경 가능 여부 |
|------|---------|------|-------------|
| R&D 확대 (HBM IF IP 강화) | USD 25M | 38% | ±5% 이내 이사회 결의 / 초과 시 투자자 동의 |
| 영업팀 인원 확대 (Hyperscaler 타겟팀) | USD 15M | 23% | ±3% 이내 이사회 결의 |
| **파운드리 물량 확보 (TSMC CoWoS)** | USD 15M | 23% | ±3% 이내 이사회 결의 |
| 운전자본 보강 | USD 10M | 16% | ±2% 이내 CFO 결정 |
| **합계 (Tranche A)** | **USD 65M** | **100%** | |

**변경 절차**:
- 허용 범위 내: 이사회 결의 후 투자자 **사후 5영업일 이내 통보**
- 허용 범위 초과: **투자자 서면 사전 동의 필수**
- 미승인 변경 적발 시: **EoD 트리거 해당**

---

## ■ PART 9. 클로징 타임라인 & Conditions Precedent

### 9.1 Conditions Precedent (CP) — E-08 CFIUS 추가

| # | 선행 조건 | 담당 | 기한 | 미충족 시 |
|---|---------|------|------|----------|
| 1 | 주주투자계약(SHA) 체결 및 사본 제출 | 법무 | Close 전일 | Close 연기 |
| 2 | 회사 정관 (Certificate of Incorporation) 사본 제출 | 법무 | Close 전일 | Close 연기 |
| 3 | IP 보유 현황 확인 (특허 Schedule 첨부) | DD | 2026-06-15 | 재협상 |
| 4 | 재무제표 3년치 + 최근 분기 제선 | DD | 2026-06-15 | Close 연기 |
| 5 | 경영진 Lock-up 확인 (Key Person 종료 금지) | 법무 | Close 전일 | Close 연기 |
| 6 | 기존 주주 동의서 (Existing Investor Consent) | 법무 | Close 전일 | Close 연기 |
| 7 | **CFIUS 클리어런스** (해당 시) | 법무 + 규제 | **2026-06-30** | **Close 불가** |
| 8 | MAC (Material Adverse Change) 미발생 확인 | DD + 법무 | Close 전일 | Close 연기/취소 |
| 9 | Use of Proceeds 집행 계획서 이사회 승인 | CFO | 2026-07-01 | Close 연기 |
| 10 | Big4 감사인 선임 확인 (Tranche B 검증용) | CFO | 2026-07-01 | Tranche B 위험 |

### 9.2 클로징 타임라인

| 단계 | 기간 | 담당 | 비고 |
|------|------|------|------|
| Term Sheet 제시 | 2026-05-08 | Gilbert | ✅ 완료 |
| **법무 검토 제출** | **2026-05-15** | 법무팀 | 🟡 대기 중 |
| **CFIUS 사전 검토 착수** | 2026-05-08 ~ 05-30 | 법무팀 + 규제 | 🆕 v2.0 신규 |
| LOI / MOU 체결 | 2026-05-20 | 양사 | CFIUS 결과 반영 |
| Due Diligence 완료 | 2026-06-15 | DD 팀 | FIN-06-BFA 연계 |
| SHA / SPA 작성 | 2026-06-15 ~ 07-15 | 법무 | |
| 최종 컨파이메이션 | 2026-07-15 | 양사 | |
| **Tranche A Close** | **2026-07-15** | Fund Admin | 목표 |
| Tranche B Milestone 검증 | 2027-Q1 | Big4 독립 검증 | |
| Tranche B Close | 2027-Q1 (최장 Q2) | Fund Admin | Milestone 달성 전제 |
| Ratchet 1차 검토 | **2027-05-08** | Gilbert | IRR 실적 vs 기준 |
| Exit / IPO 목표 | 2029 ~ 2031 | 양사 | |

---

## ■ PART 10. 기타 조항

| 조항 | v2.0 내용 |
|------|----------|
| **독점협상 (Exclusivity)** | Term Sheet 서명일로부터 **45일** — 제3자 투자자 마케팅·협상·정보 공유 전면 금지 |
| **비밀유지 (NDA)** | 기체결 독립 NDA 적용, 위반 시 손해배상 (USD 5M 패널티) |
| **비용 부담** | 각자 부담 원칙 / DD 공통 실사 비용 → 발행사 부담 (최대 USD 500K 캡) |
| **준거법** | Delaware 주법 |
| **분쟁해결** | 1차: 경영진 협의(30일) → 2차: AAA Rules 중재(뉴욕) → 최종: 법원 |
| **양도금지** | Close 전 사전 동의 없는 CB 양도 절대 불가 / Close 후 Associated Fund로만 허용 |
| **수정 절차** | 양사 서면 합의 (전자서명 허용) |
| **가분성 조항** | 일부 조항 무효 시 나머지 조항 유효 유지 |
| **완전합의 조항** | 본 Term Sheet + SHA/SPA가 전체 합의를 구성 |

---

## ■ PART 11. 법무 검토 체크리스트

| # | 위험 영역 | 검토 포인트 | 우선순위 |
|---|---------|----------|----------|
| 1 | **CFIUS 리스크** | 미국 반도체 외국인 투자 제한 여부 즉시 검토 | 🔴 즉시 |
| 2 | **CB 전환가 적정성** | -15.3% 디스카운트 현지 규제 적합성 | 🔴 즉시 |
| 3 | **IRR Ratchet 측정** | Exit Date 정의, XIRR 계산 독립 검증 | 🔴 즉시 |
| 4 | **Anti-Dilution 공식** | Broad-Based 수식 적용 범위 및 Carve-out | 🔴 즉시 |
| 5 | **Event of Default** | 매출 조항 트리거(-30%) 적정성 | 🟠 높음 |
| 6 | **핵심 인력 Lock-up** | 설립자/CTO Lock-up 기간 (최소 3년 권고) | 🟠 높음 |
| 7 | **IP 소유권** | HBM 인터페이스 특허 완전 소유 여부 | 🟠 높음 |
| 8 | **세무** | CB 이자 소득 경인 방식, 전환사채 세무 | 🟡 중등 |
| 9 | **Delaware 준거법** | 외국 LP Fund의 Delaware CB 발행 적격성 | 🟡 중등 |
| 10 | **Tranche B Milestone** | 독립 검증 주체 및 절차 명확화 | 🟡 중등 |

---

## ■ PART 12. FIN-02 자동 모니터링 연동 조항 (E-10 신설)

### FIN-02 KPI 트리거 기준값

| KPI | 경보 기준 (Yellow) | 위기 기준 (Red) | Ratchet 발동 조건 |
|-----|---------------|-------------|----------------|
| 매출 | < USD 200M (연간) | < USD 170M | Red 시 즉시 |
| EBITDA Margin | < 16% | < 12% | Red 시 즉시 |
| ROIC | < WACC 11% | < 8% | Red 시 즉시 |
| 현금 런웨이 | < 12개월 | < 6개월 | Red 시 즉시 |
| DSO | > 90일 | > 120일 | Yellow 지속 3분기 |

### 자동화 루프

```
📡 FIN-02 월간/분기 KPI 자동 수집
        ↓
   KPI Red 기준 초과 감지
        ↓
   IRR/MOIC 재산정 → Ratchet 재검토
        ↓
   EoD 트리거 해당 시 → Put Option 조기 행사 알림
        ↓
   GitHub Commit → Notion 자동 업데이트
   (PE-7 AI 자동화 파이프라인 실행)
```

---

## ■ PART 13. 서명 & 제출

### 투자자 (AstraChips LP Fund)

```
서명: ________________________________
대리자: Gilbert Kwak
날짜: 2026-05-08
연락처: [gilbert@astrachips-fund.com]
```

### 발행사 (AstraChips Inc.)

```
서명: ________________________________
대리자: [CEO 이름]
날짜: __________________
연락처: [legal@astrachips.com]
```

---

## 📋 버전 이력

| 버전 | 날짜 | 내용 | 작성자 |
|------|------|------|--------|
| v1.0 | 2026-05-08 | 최초 초안 — 법무 검토 제출용 | Gilbert Kwak |
| **v2.0** | **2026-05-08** | **PE-7 AI 자동화 오류수정 10개 반영 + CFIUS CP + FIN-02 연동 + Ratchet 측정 명확화** | **Gilbert Kwak / PE-7** |

---

*SSOT: `prompts/PE-FIN/fin_07_evp.md` | GitHub: `reports/evp/astrachips_term_sheet_20260508.md`*
*Notion: [AstraChips CB Term Sheet v1.0](https://www.notion.so/35a55ed436f08101ba95cb80361835ba)*
*다음 단계: 법무팀 2026-05-15 배포 → CFIUS 사전 검토 착수 → Tranche A Close 2026-07-15*
