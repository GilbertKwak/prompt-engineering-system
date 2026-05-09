# business_proposal_HBM4_AI_infra v1.2
# PE-NBD Full Chain 테스트용 입력 제안서 — v1.2 최종판
# 작성일: 2026-05-09 | 작성자: Gilbert Kwak
# 변경 이력: v1.0(2026-05-09) → v1.1(2026-05-09) → v1.2(2026-05-09)
# 보완 항목: [PE-NBD-02] 기술 특허/IP 조기 확보 전략 구체화
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

## [SECTION 2] 시장 기회 (Market Opportunity) ★ PE-NBD-MKT 보완 v1.1

### 2-1. TAM / SAM / SOM

| 구분 | 정의 | 추정 규모 |
|------|------|-----------|
| TAM | 글로벌 HBM 전체 시장 (HBM3E + HBM4) | $3.17B (2025) → $12.44B (2030), CAGR ~26% |
| TAM2 | 글로벌 CoWoS 전체 수요 | 2024: 370K wpm → 2025: 670K wpm → 2026: 1,000K wpm |
| SAM | TSMC CoWoS oS 아웃소싱 물량 (OSAT 기회) | 2026년 240K~270K wpm/yr 아웃소싱 예정 (TSMC 발표) |
| SOM | 우리 JV 3년 내 한국 클러스터 포착 물량 | 24K~36K wpm/yr (2~3K wpm/월, 점유 ~9~13%) |

### 2-2. ★ CoWoS oS ASP 단가 기준 (v1.1 추가)

| 패키징 유형 | ASP 범위 | OSAT 마진 | 근거 |
|------------|---------|-----------|------|
| CoWoS oS (Substrate-only) | $8,000~10,000/wpm | 35~40% | TrendForce 2026-04, GlobalSemiResearch 2025-12 |
| CoW + oS Full | $10,000~12,000/wpm | 40~45% | B200 패키징 ~$300~400/unit 기준 역산 |
| CoWoS-R (High-density RDL) | $12,000~15,000/wpm | ~50% | GlobalSemiResearch 2025-12 |
| HBM Test & Assembly | $400~600/unit | 25~30% | 업계 평균 기준 |

> ASP 근거: TrendForce 2026-04-27 "TSMC CoWoS Wafer ASP Reportedly Nears 7nm Levels"
> OSAT 아웃소싱 물량: GlobalSemiResearch 2025-12 (ASE/SPIL oS 65%+, 총 240K~270K wpm/yr)

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

## [SECTION 4] 비즈니스 모델 검증 ★ PE-NBD-04 Unit Economics v1.1

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
|------|---------|------|---------|------------|
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

### 5-2. ASE 한국 진출 방어 시나리오

| 시나리오 | 대응 전략 |
|---------|----------|
| ASE 한국 클러스터 진출 | JV Capacity Reservation 선계약으로 주요 고객 Lock-in (2~3년 계약) |
| 삼성전자 인하우스화 | 삼성 외 Fabless·Hyperscaler 전용 서비스 포지셔닝, 경쟁 고객 집중 |
| 중국 OSAT 저가 공세 | HBM4 특화 기술 IP + 미국 CHIPS Act 인증으로 프리미엄 포지션 유지 |

---

## [SECTION 6] 실행 로드맵 ★ PE-NBD-06 Phase Gate 기준 v1.1

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
| **보유 특허 수 (신규 v1.2)** | **12건 출원** | **45건 등록** |
| **IP 라이선스 수익 (신규 v1.2)** | **—** | **$15~25M/yr** |

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
| **IP 리스크 (신규 v1.2)** | **TSMC/ASE 특허 침해 리스크** | **사전 FTO 분석 + 회피 설계 + 방어 특허 포트폴리오 구축** |

---

## [SECTION 9] ★ 기술 IP 전략 (신규 v1.2) — PE-NBD-02 보완

### 9-1. IP 포트폴리오 3계층 구조

```
Layer 1: 핵심 원천특허 (Core IP) — 직접 수익화 + 경쟁 진입 장벽
Layer 2: 방어 특허 (Defensive IP) — 소송 리스크 대응 + 크로스 라이선스 협상력
Layer 3: 표준 기여 특허 (Standard IP) — 업계 영향력 + 생태계 포지셔닝
```

| 계층 | 목표 특허 수 (3년) | 핵심 기술 영역 | 전략 목적 |
|------|-----------------|--------------|---------|
| Layer 1 핵심 원천특허 | 15건 | RDL Fine-line (<2μm), TCB 공정 최적화, HBM4 열관리 패키징 | 라이선스 수익 + 기술 차별화 지속성 확보 |
| Layer 2 방어 특허 | 20건 | Substrate 재료 공정, Micro Bump 배열, ECD 도금 최적화 | TSMC·ASE 특허 회피 + 크로스 라이선스 협상 레버 |
| Layer 3 표준 기여 특허 | 10건 | CoPoS/TGV 차세대 패키징 선행, HBM5 인터페이스 패키징 | JEDEC·IEEE 표준 기여 → 업계 표준 영향력 |
| **합계** | **45건** | | |

### 9-2. IP 조기 확보 로드맵 (선제적 출원 전략)

**Phase 1 (0~18개월): 핵심 원천특허 조기 출원**

| 기간 | 출원 목표 | 주요 기술 | 관할 |
|------|---------|---------|------|
| M0~M6 | 핵심 5건 긴급 출원 | RDL Fine-line (<2μm) 공정 방법, TCB 온도 프로파일 최적화 방법 | KR + PCT (미국·대만·일본 동시) |
| M6~M12 | 방어 특허 8건 | Substrate-on-Wafer 본딩 구조, ECD 구리 도금 균일도 개선 | KR + US + TW |
| M12~M18 | 차세대 선행 5건 | CoPoS/TGV 유리기판 패키징 구조 (2026 트렌드 대응) | PCT 우선 |

**Phase 2 (18~36개월): 방어 포트폴리오 강화 + 표준 기여**

| 기간 | 출원 목표 | 주요 기술 | 전략적 의미 |
|------|---------|---------|----------|
| M18~M24 | 방어 특허 7건 | Micro Bump 고밀도 배열, 열방산 패키징 구조 | ASE·Amkor 특허 회피 설계 완료 |
| M24~M30 | HBM4 특화 5건 | HBM4 Base Die 패키징 최적화, 2,048bit 인터페이스 패키징 | HBM 공급망 내 IP 포지션 확보 |
| M30~M36 | 표준 기여 5건 | JEDEC HBM5 패키징 표준 기여 | 차세대 표준 선점 |

**Phase 3 (36~60개월): IP 라이선스 수익화 본격화**
- 핵심 원천특허 기반 라이선스 수익 $15~25M/yr 목표
- 중국 OSAT(JCET·Tongfu) 대상 유료 라이선스 협상 (미국 제재 회피 수요 활용)
- HBM5 대비 선행 IP 포트폴리오로 차세대 경쟁 우위 유지

### 9-3. IP 출원 전략 세부 사항

**한국 특허청 패스트트랙 + PCT 동시 출원**
- 한국 특허청 우선심사 (반도체 국가전략기술): 심사기간 12개월 → 6개월로 단축
- PCT 출원으로 30개월 내 미국·대만·일본·EU 국내 단계 진입
- 비용: 건당 KR $15K + PCT $40K → 45건 총 IP 예산 ~$3.5M (3년)

**경쟁사 IP 침해 리스크 매핑**

| 경쟁사 | 핵심 특허 영역 | FTO 리스크 | 회피 설계 방향 |
|--------|-------------|----------|--------------|
| TSMC | CoW 구조, 실리콘 인터포저 배열 | ⚠️ 고위험 | oS 기반 기술에 집중, CoW 구조 직접 복제 회피 |
| ASE | 고밀도 Substrate 본딩 | ⚠️ 중위험 | 독자적 본딩 온도 프로파일 + ECD 공정 차별화 |
| Amkor | Fan-out 패키징 | ℹ️ 저위험 | Fan-out 영역 회피, CoWoS oS 전문화 |
| 삼성전자 | HBM Base Die 패키징 | ⚠️ 중위험 | 크로스 라이선스 협상 (JV 파트너 가능성) |

> FTO(Freedom-to-Operate) 분석: JV 설립 M0~M3 내 국내외 특허법인 용역 착수 필수
> 예산: FTO 분석 $500K + IP 소송 준비금 $2M (Phase 1~2)

**IP 거버넌스 구조**
- JV IP위원회 설치: 각 JV 파트너 IP 책임자 + 외부 IP 전문가 2인
- 원천특허 소유권: JV 공동 소유 (단, 파트너별 기여 기술은 원소유자 귀속 후 JV 독점 라이선스)
- 라이선스 수익 배분: JV 내부 재투자 60% + 파트너 배분 40%

### 9-4. 차세대 패키징 IP 선점 — CoPoS/TGV 로드맵

> TSMC가 2026년 Q1 CoPoS(유리기판 + TGV) Pilot 라인 착공, 2028년 양산 예정 (TrendForce 2026-05)
> Intel EMIB 유리기판 800μm 샘플 이미 2026년 초 공개 → 차세대 IP 확보 시급

| 기술 영역 | IP 확보 목표 | 타이밍 | 전략 의미 |
|---------|------------|------|---------|
| TGV(Through-Glass Via) 공정 | 3건 선행특허 | M12~M18 | CoPoS 양산 시 TSMC 의존 탈피 + 독자 역량 구축 기반 |
| 유리기판 RDL Fine-line | 3건 선행특허 | M18~M24 | 2028년 CoPoS 시장 진입 시 IP 포지션 선점 |
| 패널 레벨 패키징(PLP) 구조 | 2건 선행특허 | M24~M30 | TSMC CoPoS 대비 원가경쟁력 확보 |

> 차세대 IP 전략 핵심: 현재 CoWoS oS로 수익 창출 → IP 수익 재투자 → CoPoS 시대 선점

---

## [SECTION 10] 투자 포인트 요약 (Executive Summary)

**왜 지금인가:**
- AI DC $30B+ 한국 투자 확정 → 로컬 패키징 수요 구조적 발생
- TSMC CoWoS oS 아웃소싱 2026년 240K~270K wpm/yr 본격화 → OSAT 기회 윈도우 2026~28년 최적
- HBM 글로벌 공급망 80%+가 한국에 집중 → 패키징까지 한국에서 완결하는 구조적 논리
- CoWoS ASP $10,000/wpm 수준 → 고급 패키징이 7nm 로직과 동등한 고부가가치 영역 진입

**투자 포인트 (Top 4):**
1. AI DC Capex 사이클 최상단의 구조적 수혜 포지션 — Base IRR 31%, Payback 4.6년
2. TSMC 아웃소싱 전략 직접 수혜 — 글로벌 OSAT 경쟁에서 한국 proximity가 차별화
3. 한국 정부 AI·반도체 예산($5.8B+) → 순 Capex 15~20% 절감, IRR +3~5%p 레버리지
4. **IP 포트폴리오 3계층 전략 → Phase 3 라이선스 수익 $15~25M/yr + 차세대 CoPoS 선점 (신규)**

**핵심 리스크 및 Bear 시나리오:**
- AI Capex 2027~28 조정 시 → Bear IRR 21%, Payback 6.1년 (여전히 양의 IRR, 사업성 유지)
- TCB 장비 리드타임 지연 시 → Phase 2 6개월 지연, Revenue Y2 $80M 하락 예상
- IP 소송 리스크(SK Hynix ITC 사례 참조) → FTO 분석 + 방어 특허 포트폴리오로 대응

---

## [CHANGE LOG]

| 버전 | 날짜 | 변경 내용 |
|------|------|---------|
| v1.0 | 2026-05-09 | 최초 작성 — PE-NBD Full Chain 테스트 초안 |
| v1.1 | 2026-05-09 | [PE-NBD-MKT] CoWoS oS ASP $8K~10K/wpm 기재, TSMC 아웃소싱 물량 업데이트 |
| v1.1 | 2026-05-09 | [PE-NBD-04] Unit Economics 추가 (wpm당 분해), IRR/Payback 산출 (Base 31%/4.6yr) |
| v1.1 | 2026-05-09 | [PE-NBD-06] Phase Gate 1/2 Go/No-Go 기준 정의, 장비 리드타임 리스크 추가 |
| v1.1 | 2026-05-09 | [PE-NBD-05] 중국 OSAT 경쟁 시나리오, ASE 진출 방어 플레이북 신설 |
| **v1.2** | **2026-05-09** | **[PE-NBD-02] IP 포트폴리오 3계층 구조 (핵심/방어/표준 45건) 신설** |
| **v1.2** | **2026-05-09** | **[PE-NBD-02] IP 조기 출원 로드맵: M0~M6 핵심 5건 PCT 동시 출원 전략** |
| **v1.2** | **2026-05-09** | **[PE-NBD-02] 경쟁사 FTO 리스크 매핑 (TSMC·ASE·Amkor·삼성) + 회피 설계 방향** |
| **v1.2** | **2026-05-09** | **[PE-NBD-02] CoPoS/TGV 차세대 패키징 선행 IP 로드맵 (2026~2030) 추가** |
| **v1.2** | **2026-05-09** | **[PE-NBD-02] IP 거버넌스 구조 (JV IP위원회, 소유권·수익 배분 원칙) 정의** |
| **v1.2** | **2026-05-09** | **KPI에 특허 수(45건)/IP 라이선스 수익($15~25M/yr) 추가** |

---

## [CHAIN 메타데이터]

```yaml
chain_target: PE-NBD Full Chain + MECE-01
version: v1.2
created: 2026-05-09
author: Gilbert Kwak
version_history:
  - v1.0: 2026-05-09 (최초 작성)
  - v1.1: 2026-05-09 (Unit Economics + oS ASP + Phase Gate)
  - v1.2: 2026-05-09 (IP 전략 구체화 — PE-NBD-02 보완)
next_chain: MECE-01 -> PE-NBD-01 -> PE-NBD-02 -> PE-NBD-MKT -> PE-NBD-TECH -> PE-NBD-04 -> PE-NBD-05 -> PE-NBD-06 -> PE-NBD-08
pe3_target_score: ">=94"
expected_score: "94~95"
key_domain: PE-SEMI + PE-NBD + PE-FIN + PE-IP
test_status: READY
test_date: 2026-05-09
key_additions_v1.2:
  - IP 포트폴리오 3계층: 핵심원천(15건) + 방어(20건) + 표준기여(10건) = 45건
  - PCT 동시출원: KR + US + TW + JP + EU
  - FTO 분석: TSMC/ASE/Amkor/삼성 4개사 특허 회피 설계
  - 차세대 CoPoS/TGV 선행 IP: M12~M30 8건
  - IP 라이선스 수익: $15~25M/yr (Phase 3)
  - IP 예산: FTO $500K + 출원 $3.5M + 소송준비 $2M = ~$6M (3년)
market_data_sources:
  - TrendForce 2026-04-27 (CoWoS ASP ~$10,000/wpm)
  - TrendForce 2026-05-06 (CoPoS Pilot 2026 Q1 착공, 2028 양산)
  - GlobalSemiResearch 2025-12-27 (OSAT 아웃소싱 240K~270K wpm/yr)
  - Lumenci 2025-06 (Advanced Packaging 특허 출원 CAGR 12~15%)
  - PatSnap 2026-03 (Hybrid Bonding + 2.5D 인터포저 IP 랜드스케이프)
  - Korea JoongAng Daily 2026-03-31 (SK Hynix ITC 특허 분쟁 사례)
```
