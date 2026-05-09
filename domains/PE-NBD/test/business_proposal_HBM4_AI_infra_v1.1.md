# business_proposal_HBM4_AI_infra v1.1
# PE-NBD Full Chain 테스트용 입력 제안서 — v1.1 보완판
# 작성일: 2026-05-09 | 작성자: Gilbert Kwak
# 변경 이력: v1.0(2026-05-09) → v1.1(2026-05-09)
# 보완 항목: [PE-NBD-04] Unit Economics + IRR, [PE-NBD-MKT] oS ASP, [PE-NBD-06] Phase Gate 기준
---

## [SECTION 1] 사업 정의 (Business Definition)

**제안 사업명**: Korea AI Infra OSAT JV
**한줄 요약**:
> 한국 내 AI 데이터센터 구축 붐과 TSMC CoWoS 아웃소싱 구조 전환을 동시에 포착하는
> 고급 패키징(WoS/CoW) 전문 OSAT JV 설립 및 Korea AI DC 생태계 내 포지션 확보

**사업 유형**: 합작법인(JV) 신설 + 전략적 생태계 진입
**주도 주체**: [한국 대기업 또는 반도체 관련 그룹사 — 특정 기업 오픈]
**목표 시장**: 글로벌 고급 패키징(CoWoS WoS/CoW/oS) + HBM3E/HBM4 Test & Assembly
**타깃 지역**: 한국(충청/경기권 클러스터), 대만(TSMC 파트너십 인접), 필요시 미국 거점

---

## [SECTION 2] 시장 기회 (Market Opportunity) ★ PE-NBD-MKT 보완

### 2-1. TAM / SAM / SOM

| 구분 | 정의 | 추정 규모 |
|------|------|-----------|
| TAM | 글로벌 HBM 전체 시장 (HBM3E + HBM4) | $3.17B (2025) → $12.44B (2030), CAGR ~26% |
| TAM2 | 글로벌 CoWoS 전체 수요 | 2024: 370K wpm → 2025: 670K wpm → 2026: 1,000K wpm |
| SAM | TSMC CoWoS oS 아웃소싱 물량 (OSAT 기회) | 2026년 240K~270K wpm/yr 아웃소싱 예정 (TSMC 발표) |
| SOM | 우리 JV 3년 내 한국 클러스터 포착 물량 | 24K~36K wpm/yr (2~3K wpm/월, 점유 ~9~13%) |

> 근거:
> - TSMC CoWoS 총 수요 2026년 1M wpm 돌파 예상 (TrendForce, 2026-04)
> - TSMC 2026년 OSAT 아웃소싱 240K~270K wpm/yr — Amkor 180~190K, SPIL 60~80K 배분 (GlobalSemiResearch, 2025-12)
> - TSMC 자체 월 115~125K wpm 생산 + OSAT 40K wpm → 총 155K~165K wpm/월 공급 계획 (2026년말)
> - Korea AI DC 투자 $30B+ (SK-AWS $5.1B, 현대 $6.3B 등) — 한국 내 패키징 수요 직결

### 2-2. ★ CoWoS oS ASP 단가 기준 (신규 추가)

| 패키징 유형 | ASP 범위 | OSAT 마진 | 근거 |
|------------|---------|-----------|------|
| CoWoS oS (Substrate-only) | $8,000~10,000/wpm | 35~40% | TrendForce 2026-04, GlobalSemiResearch 2025-12 |
| CoW + oS Full | $10,000~12,000/wpm | 40~45% | B200 패키징 ~$300~400/unit 기준 역산 |
| CoWoS-R (High-density RDL) | $12,000~15,000/wpm | ~50% | GlobalSemiResearch 2025-12 |
| HBM Test & Assembly | $400~600/unit | 25~30% | 업계 평균 기준 |

> ASE: 2026년 LEAP(고급 패키징) 매출 $3.2B으로 2배 성장 예상, 5~20% 단가 인상 계획 (2026년 공급 타이트)

### 2-3. 수요 촉진 요인 (Demand Drivers)

1. **AI DC Capex 폭발**: 한국 정부 AI 예산 9.9조원(2026), hyperscaler 투자 $30B+ 확정
2. **HBM4 진입**: 2,048bit 인터페이스, 10GT/s 데이터레이트, HBM3E 대비 ~25% 초과 BW → 고급 패키징 수요 급증
3. **TSMC 아웃소싱 전략**: CoWoS oS 2026년 OSAT 비중 70~80%로 상승 예상 (NVIDIA 주도)
4. **공급망 리스킹**: 대만 리스크 헤지를 위한 한국 거점 고급 패키징 수요 구조적 증가

---

## [SECTION 3] 핵심 사업 모델 (Business Model)

### 3-1. Revenue Streams

| 스트림 | 내용 | 마진 프로파일 |
|--------|------|--------------|
| CoWoS oS/WoS 위탁 서비스 | TSMC 아웃소싱 물량 수주 + 직접 고객(삼성·SK하이닉스·Fabless) | 고정 공정비 + 수율 인센티브 |
| HBM Test & Assembly | HBM3E/HBM4 최종 패키징·테스트 | 물량 × ASP |
| Capacity Reservation Fee | AI DC 사업자·Hyperscaler 선계약 | 선수금 + 유지료 |
| JV IP/기술 라이선스 | CoW/oS 관련 자체 IP 개발 후 라이선싱 (중장기) | High margin |

### 3-2. Cost Structure

- Capex: 첨단 패키징 라인(ECD, RDL, Micro Bump, TCB 장비) — 초기 $1.5~2B 예상
- OpEx: 엔지니어 인력(패키징 공정 전문가), 소모품, 에너지
- 핵심 레버: Utilization Rate (목표 85%+), 수율 (목표 95%+)

### 3-3. 차별화 포인트 (USP)

1. **한국 로컬리티 우위**: HBM 생산(SK하이닉스·삼성)과 동일 클러스터 → 물류 리드타임 최소화
2. **AI DC 수요 직접 연결**: SK-AWS, 현대 Saemangeum 등 메가 AI DC 프로젝트 proximity
3. **지정학 헤지**: 대만 CoWoS 병목 대안으로서 미국·일본·유럽 바이어의 소싱 다변화 수요 포착
4. **TSMC 파트너십 포지셔닝**: JV에 대만 OSAT 파트너(ASE/PTI 등) 포함 시 기술이전 + 물량 연계 가능

---

## [SECTION 4] 비즈니스 모델 검증 ★ PE-NBD-04 Unit Economics 보완

### 4-1. ★ Unit Economics — wpm당 Revenue / Cost 분해

**기준 가정**
- CoWoS oS ASP: $9,000/wpm (시장 범위 $8K~10K 중간값)
- OSAT 마진 (Gross): 37% (oS 기준 35~40% 범위 중간값)
- Utilization: Y1 70% → Y3 88%
- 수율: Y1 90% → Y3 96%

| 항목 | Y1 (1K wpm/월) | Y3 (5K wpm/월) | 비고 |
|------|--------------|--------------|------|
| Gross Revenue/wpm | $9,000 | $9,450 (+5% 단가 인상) | 공급 타이트 반영 |
| 재료비·공정비/wpm | $3,150 | $3,000 | 스케일 효율 |
| 인건비·에너지/wpm | $1,200 | $900 | 고정비 분산 |
| Gross Profit/wpm | $4,650 (51.7%) | $5,550 (58.7%) | |
| D&A/wpm | $1,800 | $1,200 | Capex $2B, 10년 감가 |
| EBIT/wpm | $2,850 (31.7%) | $4,350 (46.0%) | |

**월별 Revenue 추정**

| 시점 | 가동 wpm | Util | 유효 wpm | Revenue/월 |
|------|---------|------|---------|----------|
| Y1 평균 | 1,000 | 70% | 700 | $6.3M |
| Y2 평균 | 3,000 | 80% | 2,400 | $22.7M |
| Y3 평균 | 5,000 | 88% | 4,400 | $41.6M |

> Y3 연환산 Revenue: $41.6M × 12 ≈ **$499M** (HBM T&A 포함 시 ~$800M 달성 가능)

### 4-2. ★ IRR / Payback Period 산출

**가정**
- 총 Capex: $2.0B (Phase 1: $0.8B, Phase 2: $0.7B, Phase 3: $0.5B)
- 정부 보조금/세액공제: Capex의 15~20% (한국 AI·반도체 예산 활용) → 순 Capex $1.6~1.7B
- 운영 시작: Y2 1Q (Pilot 라인 가동)
- Terminal Growth Rate: 3%
- WACC: 9.5% (반도체 장치 섹터 기준)

| 시나리오 | 순 Capex | Y3 EBITDA | IRR | Payback |
|---------|---------|---------|-----|--------|
| Base | $1.65B | $224M | 31% | 4.6년 |
| Bull (ASP +10%, Util +5%) | $1.60B | $285M | 38% | 3.9년 |
| Bear (AI Capex 조정, Util -15%) | $1.70B | $148M | 21% | 6.1년 |

> **Base IRR 31%** — WACC 9.5% 대비 스프레드 21.5%p, 반도체 장치 투자 기준 매력적
> 정부 보조금 레버리지 핵심: 한국 AI R&D 예산(2026년 9.9조원) 중 패키징 인프라 지원분 활용 시 IRR +3~5%p 추가

---

## [SECTION 5] 경쟁 분석 (Competition)

### 5-1. 주요 경쟁자 매트릭스

| 플레이어 | 포지션 | 강점 | 약점/기회 |
|----------|--------|------|----------|
| ASE/SPIL | 글로벌 OSAT 1위 (oS 65%+) | 규모·기술력·TSMC 관계 | 대만 집중 리스크, 한국 거점 부재 |
| Amkor Technology | OSAT 2위 | 미국·유럽 고객 기반, 다지역 | HBM 특화 패키징 역량 제한적 |
| PTI (Power Tech) | OSAT 3위 | 대만 로컬 | 규모 작음, 한국 진출 없음 |
| JCET·Tongfu (중국) | 중국 OSAT 1~2위 | 저비용·중국 내수 | 미국 수출통제로 AI 고급 패키징 접근 제한 |
| TSMC (자체) | CoW 전면 독점 | 기술·고객 신뢰 | Capex 부담으로 oS 아웃소싱 전략 선택 |
| **우리 JV** | **한국 신규 진입** | **한국 AI DC 근접성, HBM 공급망 proximity** | **초기 레퍼런스 부재 → 극복 전략 필요** |

### 5-2. 포지셔닝 전략 (2×2)

```
           고급 패키징 기술력
                 ↑ High
                 |  [TSMC]
                 |
      [ASE/SPIL] |         [우리 JV 목표 위치]
                 |
      [JCET]     |  [Amkor] [PTI]
                 |________________________→
           Low               High
                   한국·AI DC 근접성
```

### 5-3. ASE 한국 진출 방어 시나리오

| 시나리오 | 대응 전략 |
|---------|----------|
| ASE 한국 클러스터 진출 | JV Capacity Reservation 선계약으로 주요 고객 Lock-in (2~3년 계약) |
| 삼성전자 인하우스화 | 삼성 외 Fabless·Hyperscaler 전용 서비스 포지셔닝, 경쟁 고객 집중 |
| 중국 OSAT 저가 공세 | HBM4 특화 기술 IP + 미국 CHIPS Act 인증으로 프리미엄 포지션 유지 |

---

## [SECTION 6] 실행 로드맵 ★ PE-NBD-06 Phase Gate 기준 보완

### Phase 1 — JV 설립 & 기반 구축 (0~18개월)

**주요 마일스톤**
- M3: JV 파트너 확정 (대만 OSAT 1사 + 한국 대기업 1사)
- M6: 부지 선정 (경기 북부 또는 충청권 반도체 클러스터)
- M12: Pilot 라인 구축 착수 — WoS/oS 공정 ECD·RDL 라인
- M15: TSMC 아웃소싱 공식 파트너 인증 신청 (Qualified Supplier)
- M18: Pilot 라인 가동 개시, 1K wpm 목표

**★ 장비 리드타임 리스크**
- TCB(Thermocompression Bonding) 장비: 주문~납품 18~24개월 → M0에 즉시 발주 필수
- ECD·RDL 라인: 12~15개월 리드타임 → M3 JV 확정 직후 발주
- 리스크 대응: 대만 파트너 기존 장비 임시 활용(Bridge) + 한국 라인 병행 구축

**★ Phase Gate 1 Go/No-Go 기준 (M18 평가)**

| 지표 | Go 기준 | No-Go 조건 |
|------|--------|----------|
| Pilot 수율 | ≥88% | <80% → Phase 2 진입 보류, 기술 재검토 |
| Utilization (Pilot) | ≥65% | <55% → 수요 재검증 필요 |
| TSMC Qualified Supplier 인증 | 완료 또는 심사 중 | 신청 미완료 → Phase 2 Capex 집행 보류 |
| 고객 LOI | ≥2개사 | 0개 → 전략 재검토 |
| 정부 보조금 승인 | ≥$200M 확정 | 미확정 → Phase 2 Capex 규모 하향 조정 |

### Phase 2 — 물량 확보 & 스케일업 (18~36개월)

**주요 마일스톤**
- M20: TSMC oS 아웃소싱 물량 수주 개시
- M24: 총 라인 3K wpm 달성
- M30: 한국 AI DC 프로젝트(SK-AWS, 현대 등) HBM 패키징 직접 공급계약 체결
- M36: 총 라인 5K wpm 달성

**★ Phase Gate 2 Go/No-Go 기준 (M36 평가)**

| 지표 | Go 기준 | No-Go 조건 |
|------|--------|----------|
| 수율 | ≥93% | <88% → 공정 최적화 후 재평가 (3개월 유예) |
| Utilization | ≥80% | <70% → Phase 3 Capex 집행 보류 |
| Revenue run-rate | ≥$400M/yr | <$300M → 사업 모델 재검토 |
| EBITDA Margin | ≥22% | <18% → 비용 구조 재검토 |
| 주요 고객 수 | ≥4개사 | <3개사 → 영업 전략 강화 |

### Phase 3 — IP·고마진 포트폴리오 (36~60개월)
- CoW/RDL 자체 IP 개발 + 라이선스 수익화
- HBM5 대비 차세대 패키징 선행 개발 착수
- 미국·일본 거점 검토 (CHIPS Act 활용)

**★ 인력 계획**

| 단계 | 총 인원 | 핵심 채용 |
|------|--------|----------|
| Phase 1 완료 | ~350명 | 패키징 공정 엔지니어 200명, 장비 엔지니어 100명, 관리 50명 |
| Phase 2 완료 | ~900명 | 추가 공정·QC 엔지니어 400명, R&D 150명 |
| Phase 3 완료 | ~1,400명 | IP 개발팀 200명, 해외 거점 100명 |

> 핵심 채용 리스크: 패키징 공정 전문가 국내 풀 제한 → 대만 파트너 전문가 파견(3년) + 대학 산학협력 병행

---

## [SECTION 7] 핵심 지표 (KPIs)

| KPI | Year 1 목표 | Year 3 목표 |
|-----|------------|------------|
| Utilization Rate | 70% | 88% |
| oS Capacity | 1K wpm | 5K wpm |
| 수율 | 90% | 96% |
| Revenue | $150M | $800M |
| EBITDA Margin | 18% | 28% |
| IRR (Base) | — | 31% |
| Payback Period | — | 4.6년 |
| TSMC 인증 완료 | Q4 Y1 | 유지 |
| 주요 고객사 수 | 2 | 6 |

---

## [SECTION 8] 리스크 및 대응 (Risks & Mitigation)

| 리스크 유형 | 내용 | Mitigation |
|------------|------|------------|
| 기술 리스크 | HBM4 패키징 수율 초기 낮음 | 대만 파트너 기술이전 + 파일럿 단계 수율 검증 (Phase Gate: ≥88%) |
| 장비 리드타임 | TCB 장비 18~24개월 → Phase 1 지연 위험 | M0 즉시 발주 + 대만 파트너 Bridge 장비 활용 |
| 수요 사이클 | AI Capex 2027~28 조정 가능성 | 장기 Capacity Reservation 계약 선행 + Bear 시나리오 IRR 21% 확인 |
| 경쟁 심화 | ASE 한국 진출 or 삼성 자체화 | LOI Lock-in + CHIPS Act 인증 + 기술 IP 차별화 |
| 중국 OSAT | JCET·Tongfu 저가 공세 | 미국 수출통제 혜택 유지 + HBM4 특화 프리미엄 포지셔닝 |
| 지정학 | 미·중 규제, TSMC 아웃소싱 정책 변경 | 미국 CHIPS Act 인증 병행, 고객 다변화 |
| 자본 리스크 | Capex 초기 집중 | Phase-gate Capex + 정부 보조금(한국 AI R&D 예산 15~20% Capex 커버) 병행 |

---

## [SECTION 9] 투자 포인트 요약 (Executive Summary)

**왜 지금인가:**
- AI DC $30B+ 한국 투자 확정 → 로컬 패키징 수요 구조적 발생
- TSMC CoWoS oS 아웃소싱 2026년 240K~270K wpm/yr 본격화 → OSAT 기회 윈도우 2026~28년 최적
- HBM 글로벌 공급망 80%+가 한국에 집중 → 패키징까지 한국에서 완결하는 구조적 논리
- CoWoS ASP $10,000/wpm 수준 → 고급 패키징이 7nm 로직과 동등한 고부가가치 영역 진입

**투자 포인트 (Top 3):**
1. AI DC Capex 사이클 최상단의 구조적 수혜 포지션 — Base IRR 31%, Payback 4.6년
2. TSMC 아웃소싱 전략 직접 수혜 — 글로벌 OSAT 경쟁에서 한국 proximity가 차별화
3. 한국 정부 AI·반도체 예산($5.8B+) → 순 Capex 15~20% 절감, IRR +3~5%p 레버리지

**핵심 리스크 및 Bear 시나리오:**
- AI Capex 2027~28 조정 시 → Bear IRR 21%, Payback 6.1년 (여전히 양의 IRR, 사업성 유지)
- TCB 장비 리드타임 지연 시 → Phase 2 6개월 지연, Revenue Y2 $80M 하락 예상

---

## [CHANGE LOG]

| 버전 | 날짜 | 변경 내용 |
|------|------|---------|
| v1.0 | 2026-05-09 | 최초 작성 — PE-NBD Full Chain 테스트 초안 |
| v1.1 | 2026-05-09 | [PE-NBD-MKT] CoWoS oS ASP $8K~10K/wpm 기재, TSMC 아웃소싱 물량 240K~270K wpm/yr 업데이트 |
| v1.1 | 2026-05-09 | [PE-NBD-04] Unit Economics 추가 (wpm당 Revenue/Cost), IRR/Payback 산출 (Base 31%/4.6yr) |
| v1.1 | 2026-05-09 | [PE-NBD-06] Phase Gate 1/2 Go/No-Go 기준 정의, 장비 리드타임 리스크(TCB 18~24m) 추가, 인력 계획 포함 |
| v1.1 | 2026-05-09 | [PE-NBD-05] 중국 OSAT(JCET·Tongfu) 경쟁 시나리오 추가, ASE 한국 진출 방어 플레이북 신설 |

---

## [CHAIN 메타데이터]

```yaml
chain_target: PE-NBD Full Chain + MECE-01
version: v1.1
created: 2026-05-09
author: Gilbert Kwak
prev_version: v1.0
next_chain: MECE-01 -> PE-NBD-01 -> PE-NBD-02 -> PE-NBD-MKT -> PE-NBD-TECH -> PE-NBD-04 -> PE-NBD-05 -> PE-NBD-06 -> PE-NBD-08
pe3_target_score: ">=92"
key_domain: PE-SEMI + PE-NBD + PE-FIN
test_status: READY
test_date: 2026-05-09
market_data_sources:
  - TrendForce 2026-04-27 (CoWoS ASP ~$10,000/wpm)
  - GlobalSemiResearch 2025-12-27 (OSAT 아웃소싱 240K~270K wpm/yr, 마진 35~50%)
  - LinkedIn IsaiahResearch 2025-12 (ASE/SPIL oS 65%+ 점유)
  - 36kr.com 2025-12 (CoWoS 수요 2026: 1M wpm)
```
