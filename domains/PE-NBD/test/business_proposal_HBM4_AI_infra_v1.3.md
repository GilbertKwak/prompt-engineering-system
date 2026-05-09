# business_proposal_HBM4_AI_infra v1.3
# PE-NBD Full Chain 테스트용 입력 제안서 — v1.3 최종판
# 작성일: 2026-05-09 | 작성자: Gilbert Kwak
# 변경 이력: v1.0 → v1.1 → v1.2 → v1.3
# 보완 항목: [PE-NBD-02/PE-JV] JV 파트너 구조 + [PE-NBD-05] 고객 LOI 전략
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

## [SECTION 2] 시장 기회 (Market Opportunity) — v1.1 기준 유지

### 2-1. TAM / SAM / SOM

| 구분 | 정의 | 추정 규모 |
|------|------|-----------|
| TAM | 글로벌 HBM 전체 시장 (HBM3E + HBM4) | $3.17B (2025) → $12.44B (2030), CAGR ~26% |
| TAM2 | 글로벌 CoWoS 전체 수요 | 2024: 370K wpm → 2025: 670K wpm → 2026: 1,000K wpm |
| SAM | TSMC CoWoS oS 아웃소싱 물량 (OSAT 기회) | 2026년 240K~270K wpm/yr 아웃소싱 예정 (TSMC 발표) |
| SOM | 우리 JV 3년 내 한국 클러스터 포착 물량 | 24K~36K wpm/yr (2~3K wpm/월, 점유 ~9~13%) |

### 2-2. CoWoS oS ASP 단가 기준 (v1.1 추가)

| 패키징 유형 | ASP 범위 | OSAT 마진 | 근거 |
|------------|---------|-----------|------|
| CoWoS oS (Substrate-only) | $8,000~10,000/wpm | 35~40% | TrendForce 2026-04, GlobalSemiResearch 2025-12 |
| CoW + oS Full | $10,000~12,000/wpm | 40~45% | B200 패키징 ~$300~400/unit 기준 역산 |
| CoWoS-R (High-density RDL) | $12,000~15,000/wpm | ~50% | GlobalSemiResearch 2025-12 |
| HBM Test & Assembly | $400~600/unit | 25~30% | 업계 평균 기준 |

### 2-3. 수요 촉진 요인 (Demand Drivers)

1. **AI DC Capex 폭발**: 한국 정부 AI 예산 9.9조원(2026), hyperscaler 투자 $30B+ 확정
2. **HBM4 진입**: 2,048bit 인터페이스, 10GT/s 데이터레이트 → 고급 패키징 수요 급증
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
5. **IP 라이선스 수익**: 3계층 IP 포트폴리오 → Phase 3 라이선스 수익 $15~25M/yr

---

## [SECTION 4] 비즈니스 모델 검증 — PE-NBD-04 Unit Economics (v1.1)

### 4-1. wpm당 Revenue / Cost 분해

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

### 4-2. IRR / Payback Period 산출

| 시나리오 | 순 Capex | Y3 EBITDA | IRR | Payback |
|---------|---------|---------|-----|--------|
| Base | $1.65B | $224M | 31% | 4.6년 |
| Bull (ASP +10%, Util +5%) | $1.60B | $285M | 38% | 3.9년 |
| Bear (AI Capex 조정, Util -15%) | $1.70B | $148M | 21% | 6.1년 |

---

## [SECTION 5] 경쟁 분석 (Competition) — v1.1 기준 유지

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
| 삼성전자 인하우스화 | 삼성 外 Fabless·Hyperscaler 전용 서비스 포지셔닝, 경쟁 고객 집중 |
| 중국 OSAT 저가 공세 | 미국 수출통제 혜택 유지 + HBM4 특화 기술 IP + 프리미엄 포지션 유지 |

---

## [SECTION 6] 실행 로드맵 — Phase Gate 기준 (v1.1)

### Phase 1 — JV 설립 & 기반 구축 (0~18개월)

**주요 마일스톤**
- M3: JV 파트너 확정 (대만 OSAT 1사 + 한국 대기업 1사)
- M6: 부지 선정 (경기 북부 또는 충청권 반도체 클러스터)
- M12: Pilot 라인 구축 착수 — WoS/oS 공정 ECD·RDL 라인
- M15: TSMC 아웃소싱 공식 파트너 인증 신청 (Qualified Supplier)
- M18: Pilot 라인 가동 개시, 1K wpm 목표

**장비 리드타임 리스크**
- TCB(Thermocompression Bonding) 장비: 주문~납품 18~24개월 → M0에 즉시 발주 필수
- ECD·RDL 라인: 12~15개월 리드타임 → M3 JV 확정 직후 발주
- 리스크 대응: 대만 파트너 기존 장비 임시 활용(Bridge) + 한국 라인 병행 구축

**Phase Gate 1 Go/No-Go 기준 (M18 평가)**

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

**Phase Gate 2 Go/No-Go 기준 (M36 평가)**

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
| 보유 특허 수 (v1.2) | 12건 출원 | 45건 등록 |
| IP 라이선스 수익 (v1.2) | — | $15~25M/yr |
| **JV 파트너 확정 (v1.3)** | **M3 완료** | **JV 안정 운영** |
| **LOI 확보 수 (v1.3)** | **≥2개사 (M18)** | **≥6개사** |

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
| IP 리스크 (v1.2) | TSMC/ASE 특허 침해 리스크 | 사전 FTO 분석 + 회피 설계 + 방어 특허 포트폴리오 구축 |
| **JV 파트너 리스크 (v1.3)** | **파트너 이탈·의사결정 교착** | **Exit 조항 사전 정의 + 캐스팅보트 조항 + IP 귀속 원칙 명문화** |
| **LOI 미확보 리스크 (v1.3)** | **Phase 1 내 고객 LOI ≥2개사 미달** | **TSMC 소개 루트 + 직접 영업 병행, NDA 선행 체결로 전환율 제고** |

---

## [SECTION 9] 기술 IP 전략 (v1.2) — 유지

### 9-1. IP 포트폴리오 3계층 구조

| 계층 | 목표 특허 수 (3년) | 핵심 기술 영역 | 전략 목적 |
|------|-----------------|--------------|---------||
| Layer 1 핵심원천특허 | 15건 | RDL Fine-line (<2μm), TCB 공정 최적화, HBM4 열관리 패키징 | 라이선스 수익 + 기술 차별화 지속성 확보 |
| Layer 2 방어특허 | 20건 | Substrate 재료 공정, Micro Bump 배열, ECD 도금 최적화 | TSMC·ASE 특허 회피 + 크로스 라이선스 협상 레버 |
| Layer 3 표준기여특허 | 10건 | CoPoS/TGV 차세대 패키징 선행, HBM5 인터페이스 패키징 | JEDEC·IEEE 표준 기여 → 업계 표준 영향력 |
| **합계** | **45건** | | |

### 9-2. IP 조기 확보 로드맵 (선제적 출원 전략)

**Phase 1 (0~18개월): 핵심원천특허 조기 출원**

| 기간 | 출원 목표 | 주요 기술 | 관할 |
|------|---------|---------|------|
| M0~M6 | 핵심 5건 긴급 출원 | RDL Fine-line (<2μm) 공정 방법, TCB 온도 프로파일 최적화 방법 | KR + PCT (미국·대만·일본 동시) |
| M6~M12 | 방어특허 8건 | Substrate-on-Wafer 본딩 구조, ECD 구리 도금 균일도 개선 | KR + US + TW |
| M12~M18 | 차세대 선행 5건 | CoPoS/TGV 유리기판 패키징 구조 (2026 트렌드 대응) | PCT 우선 |

**Phase 2~3: 방어 포트폴리오 강화 + 표준 기여 + IP 수익화**
- Phase 3: 핵심원천특허 기반 라이선스 수익 $15~25M/yr 목표
- 중국 OSAT(JCET·Tongfu) 대상 유료 라이선스 협상 (미국 제재 회피 수요 활용)

### 9-3. 경쟁사 FTO 리스크 매핑

| 경쟁사 | 핵심 특허 영역 | FTO 리스크 | 회피 설계 방향 |
|--------|-------------|----------|--------------||
| TSMC | CoW 구조, 실리콘 인터포저 배열 | ⚠️ 고위험 | oS 기반 기술에 집중, CoW 구조 직접 복제 회피 |
| ASE | 고밀도 Substrate 본딩 | ⚠️ 중위험 | 독자적 본딩 온도 프로파일 + ECD 공정 차별화 |
| Amkor | Fan-out 패키징 | ℹ️ 저위험 | Fan-out 영역 회피, CoWoS oS 전문화 |
| 삼성전자 | HBM Base Die 패키징 | ⚠️ 중위험 | 크로스 라이선스 협상 (JV 파트너 가능성) |

---

## [SECTION 10] ★ JV 파트너 구조 (신규 v1.3) — PE-NBD-02 / PE-JV

### 10-1. 대만 OSAT 파트너 선택 기준 매트릭스

**평가 대상**: ASE Group / PTI (Power Tech International) / SPIL (Siliconware Precision)

| 평가 항목 | 가중치 | ASE | PTI | SPIL |
|---------|------|-----|-----|------|
| CoWoS oS 기술 보유 수준 | 30% | ★★★★★ | ★★★☆☆ | ★★★★☆ |
| TSMC Qualified Supplier 지위 | 25% | ★★★★★ | ★★★★☆ | ★★★★★ |
| 한국 JV 협력 의향 (추정) | 20% | ★★★☆☆ | ★★★★★ | ★★★☆☆ |
| JV 지분 참여 유연성 | 15% | ★★☆☆☆ | ★★★★★ | ★★★☆☆ |
| 기술 이전 가능 범위 | 10% | ★★★☆☆ | ★★★★☆ | ★★★★☆ |
| **종합 점수** | | **74점** | **88점** | **78점** |

> **PTI 우선 협상 대상 권고** — 규모 대비 협력 유연성 최고, TSMC Qualified, 기술이전 가능 범위 양호
> **ASE 2순위** — 기술력 최강이나 한국 JV 참여 유인 낮음 (자체 한국 진출 가능성 모니터링 필요)
> **SPIL 보완 고려** — ASE 계열사이나 독립적 협상 채널 존재

### 10-2. 지분 구조 시나리오 3안 비교

| 구분 | 시나리오 A (50:50) | 시나리오 B (51:49) | 시나리오 C (40:60) |
|------|----------------|----------------|----------------|
| 구조 | 한국 주도사 50% : 대만 OSAT 50% | 한국 주도사 51% : 대만 OSAT 49% | 한국 주도사 40% : 대만 OSAT 60% |
| 의사결정 | 동등 — 교착 위험 높음 | 한국 측 경영 주도권 | 대만 OSAT 주도 |
| 기술이전 인센티브 | 중간 | 낮음 (대만 측 동기 약화) | 높음 (대만 측 주도권 확보) |
| TSMC 관계 레버 | 중간 | 낮음 | **높음** (대만 파트너 TSMC 채널 적극 활용) |
| 한국 정부 보조금 적격 | ✅ 가능 | ✅ 가능 | ⚠️ 심사 필요 (외국인 지분 60% 초과 시 제한 가능) |
| IP 귀속 | 공동 소유 (50:50) | 한국 주도 (의결권 기준) | 대만 OSAT 우선권 → 분쟁 가능성 |
| **권고** | **교착 방지 조항 필수** | **가장 균형적 — 권고안** | **기술이전 최대화 시 고려** |

> **최종 권고: 시나리오 B (51:49)** — 한국 측 경영 주도권 확보 + 정부 보조금 적격 + IP 귀속 명확
> 단, 대만 파트너(PTI) 동기 부여를 위해 **이익배분은 50:50 기준 별도 협의** 조항 병기

### 10-3. JV 거버넌스 Term Sheet 수준 정의

**이사회 구성**
- 총 이사 7인: 한국 주도사 4인 + 대만 OSAT 3인
- 캐스팅보트: 의장(한국 측 지명) → 동수 시 의장 결정권
- 필수 만장일치 사항: Capex $100M 초과 투자, JV 지분 양도, IP 매각·대규모 라이선싱

**경영진 구성**
- CEO: 한국 측 추천 (이사회 승인)
- CTO: 대만 OSAT 추천 (기술이전·공정 주도)
- CFO: 한국 측 추천 (재무·보조금 관리)
- Chief IP Officer: 외부 독립 전문가 (IP 분쟁 중립성 확보)

**Exit 조항**
- Lock-up 기간: JV 설립 후 5년 (Phase 2 완료 시점까지)
- 우선매수권(ROFR): 일방이 지분 매각 시 상대방 우선매수권 6개월 행사 가능
- 강제매각(Drag-along): 외부 전략적 투자자 유치 시 양방 동의 하 전체 지분 매각 허용
- 기술이전 무효화 조항: 대만 파트너 조기 Exit 시 이전 기술 사용권 5년 유예 보장 (분쟁 방지)

**IP 귀속 원칙**
- JV 내 공동 개발 IP: JV 공동 소유 (수익 배분 60%:40% = 한국:대만)
- 파트너별 기여 기술: 원소유자 귀속 후 JV에 독점 라이선스
- JV 해산 시: IP 공동 소유 → 양측 비독점 라이선스로 전환 (제3자 매각 불허)

---

## [SECTION 11] ★ 고객 LOI 확보 전략 (신규 v1.3) — PE-NBD-05

### 11-1. 타깃 고객 3계층 구조

```
[Tier 1 — TSMC 소개 루트] ────────────────────────── 전환율 高, 물량 大
  대상: TSMC 기존 CoWoS 고객 (NVIDIA, AMD, Broadcom, Marvell)
  접근: JV 내 대만 OSAT 파트너(PTI)의 TSMC 채널 활용
  타임라인: M3 JV 확정 → M6 첫 미팅 → M12 NDA → M15 LOI

[Tier 2 — 한국 AI DC 직접 영업] ──────────────────── 전환율 中, 지속성 高
  대상: SK-AWS JV, 현대 Saemangeum AI DC, KT, LG CNS
  접근: 한국 주도사 네트워크 + 정부 AI DC 사업 인허가 채널
  타임라인: M1 접촉 → M6 NDA → M12 LOI → M24 공급계약

[Tier 3 — 글로벌 Hyperscaler 직접 파트너십] ────────── 전환율 低, 전략적 가치 最高
  대상: AWS Korea, Microsoft Azure Korea, Google Cloud Korea
  접근: CHIPS Act 공급망 다변화 + 지정학 헤지 포지셔닝
  타임라인: M6 접촉 → M12 NDA → M18 Capacity Reservation MOU → M30 LOI
```

### 11-2. 고객별 접근 경로 및 NDA→LOI 전환 타임라인

| 고객 | 접근 루트 | 핵심 셀링포인트 | NDA | LOI 목표 |
|------|---------|-------------|-----|---------|
| **NVIDIA** (Tier 1) | PTI → TSMC 채널 | GB300/B300 HBM4 패키징 병목 해소, 대만 외 소싱 옵션 | M6 | M15 |
| **AMD** (Tier 1) | PTI → TSMC 채널 | MI400 시리즈 CoWoS oS 용량 확보 | M9 | M18 |
| **SK-AWS** (Tier 2) | 한국 주도사 직접 | 군산 AI DC 로컬 패키징 proximity, 물류비 절감 | M3 | M12 |
| **현대 Saemangeum** (Tier 2) | 한국 주도사 직접 | AI DC 패키징 공급망 국산화, 정부 협력 채널 | M3 | M12 |
| **Broadcom** (Tier 1) | PTI → TSMC 채널 | 커스텀 ASIC CoWoS oS 용량 예약 | M9 | M18 |
| **Microsoft Azure** (Tier 3) | CHIPS Act 채널 | 지정학 헤지 + 대만 外 공급망 | M12 | M30 |

> **Phase 1 내 LOI ≥2개사 확보 필수 타깃**: SK-AWS(M12) + NVIDIA(M15) — 두 개사 합산 물량 1K~1.5K wpm/월 이상

### 11-3. LOI 조건 협상 포인트

**물량 보장 조항 (Volume Commitment)**
- 최소 연간 물량: LOI 기준 Y2 500~1,000 wpm/월, Y3 1,500~2,000 wpm/월
- Take-or-Pay: 최소 물량 미달 시 고객이 차액의 60~70% 보상
- 물량 초과 시: JV가 6개월 전 사전 통보 의무 (증설 계획 공유)

**ASP 연동 조항 (Price Escalation)**
- 기준 ASP: $9,000/wpm (CoWoS oS, 계약 시점 기준)
- 연간 인상 한도: ±5% (TrendForce 시장 지수 연동)
- 수율 인센티브: 수율 ≥95% 달성 시 ASP +3% 상향 협상 권리

**독점 조항 (Exclusivity)**
- 고객별 물량 기준 독점: 연간 1,500 wpm 이상 수주 고객에 한해 한국 OSAT 독점 공급 우선권 6개월
- 경쟁사 제한: JV는 동일 고객의 직접 경쟁 제품 동시 패키징 불가 (분리 라인 운영 허용)

**Capacity Reservation Fee**
- 선수금: LOI 체결 시 연간 예약 물량의 10~15% 선납 → JV 초기 운전자금 확보
- 환불 조건: Phase Gate No-Go 발생 시 선수금 80% 환불 (20%는 위약금)

### 11-4. Phase 1 내 LOI ≥2개사 확보 실행 플랜

```
[M0~M3] 영업 준비
  □ 한국 주도사 IR 자료 + JV Teaser 덱 완성
  □ PTI와 JV MOU 체결 → TSMC 채널 접근 권한 확보
  □ SK-AWS, 현대 AI DC 담당 임원 첫 미팅 일정 확정

[M3~M6] 첫 접촉 & NDA
  □ SK-AWS: NDA 체결 → Capacity 수요 확인 미팅
  □ 현대 Saemangeum: NDA 체결 → AI DC 장기 공급 수요 논의
  □ NVIDIA (PTI 채널): 첫 미팅 → 기술 역량 발표

[M6~M12] 협상 & LOI 초안
  □ SK-AWS: Take-or-Pay 조건 협상 → LOI 초안 교환
  □ 현대: LOI 초안 → M12 서명 목표
  □ NVIDIA: NDA 체결 → 기술 실사(Technical Due Diligence)

[M12~M18] LOI 확정 & Phase Gate 준비
  □ SK-AWS LOI 서명 완료 (M12)
  □ 현대 LOI 서명 완료 (M12)
  □ NVIDIA LOI 목표 (M15) — Phase Gate 1 Go 조건 충족
  □ AMD 첫 접촉 → NDA (M18 목표)
```

### 11-5. LOI 확보 리스크 및 대응

| 리스크 | 확률 | 대응 |
|--------|------|------|
| SK-AWS 내부 승인 지연 | 중(40%) | AWS Korea + 본사 공급망팀 동시 접근, 한국 정부 AI DC 채널 활용 |
| NVIDIA TSMC 채널 접근 실패 | 중(35%) | PTI JV 확정 선행 + TSMC 직접 소개 요청 (JV Qualified Supplier 신청 연계) |
| 고객 독점 조항 거부 | 고(60%) | 독점 조항 완화 → 우선공급권(Right of First Refusal) 대안 제시 |
| Take-or-Pay 조건 협상 결렬 | 중(45%) | 최소 물량 보장 하한 하향 조정 (500 wpm/월 → 300 wpm/월) + 선수금 비율 협상 |

---

## [SECTION 12] 투자 포인트 요약 (Executive Summary)

**왜 지금인가:**
- AI DC $30B+ 한국 투자 확정 → 로컬 패키징 수요 구조적 발생
- TSMC CoWoS oS 아웃소싱 2026년 240K~270K wpm/yr 본격화 → OSAT 기회 윈도우 2026~28년 최적
- HBM 글로벌 공급망 80%+가 한국에 집중 → 패키징까지 한국에서 완결하는 구조적 논리
- CoWoS ASP $10,000/wpm 수준 → 고급 패키징이 7nm 로직과 동등한 고부가가치 영역 진입

**투자 포인트 (Top 5):**
1. AI DC Capex 사이클 최상단의 구조적 수혜 포지션 — Base IRR 31%, Payback 4.6년
2. TSMC 아웃소싱 전략 직접 수혜 — 글로벌 OSAT 경쟁에서 한국 proximity가 차별화
3. 한국 정부 AI·반도체 예산($5.8B+) → 순 Capex 15~20% 절감, IRR +3~5%p 레버리지
4. IP 포트폴리오 3계층 전략 → Phase 3 라이선스 수익 $15~25M/yr + 차세대 CoPoS 선점 (v1.2)
5. **JV 거버넌스 51:49 구조 + LOI ≥2개사 Phase 1 확보 → 실행 가능성 최고 수준 (v1.3 신규)**

**핵심 리스크 및 Bear 시나리오:**
- AI Capex 2027~28 조정 시 → Bear IRR 21%, Payback 6.1년 (여전히 양의 IRR, 사업성 유지)
- TCB 장비 리드타임 지연 시 → Phase 2 6개월 지연, Revenue Y2 $80M 하락 예상
- JV 파트너 협상 교착 시 → PTI 1순위 / ASE 2순위 대안 존재, M3 기한 내 전환 가능 (v1.3)
- LOI ≥2개사 미달 시 → Phase Gate No-Go → Phase 2 Capex 보류, 영업 전략 재검토 (v1.3)

---

## [CHANGE LOG]

| 버전 | 날짜 | 변경 내용 |
|------|------|---------|
| v1.0 | 2026-05-09 | 최초 작성 — PE-NBD Full Chain 테스트 초안 |
| v1.1 | 2026-05-09 | [PE-NBD-MKT] CoWoS oS ASP $8K~10K/wpm 기재, TSMC 아웃소싱 물량 업데이트 |
| v1.1 | 2026-05-09 | [PE-NBD-04] Unit Economics 추가 (wpm당 분해), IRR/Payback 산출 (Base 31%/4.6yr) |
| v1.1 | 2026-05-09 | [PE-NBD-06] Phase Gate 1/2 Go/No-Go 기준 정의, 장비 리드타임 리스크 추가 |
| v1.1 | 2026-05-09 | [PE-NBD-05] 중국 OSAT 경쟁 시나리오, ASE 진출 방어 플레이북 신설 |
| v1.2 | 2026-05-09 | [PE-NBD-02] IP 포트폴리오 3계층 구조 (핵심/방어/표준 45건) 신설 |
| v1.2 | 2026-05-09 | [PE-NBD-02] IP 조기 출원 로드맵: M0~M6 핵심 5건 PCT 동시 출원 전략 |
| v1.2 | 2026-05-09 | [PE-NBD-02] 경쟁사 FTO 리스크 매핑 (TSMC·ASE·Amkor·삼성) + 회피 설계 방향 |
| v1.2 | 2026-05-09 | [PE-NBD-02] CoPoS/TGV 차세대 패키징 선행 IP 로드맵 (2026~2030) 추가 |
| **v1.3** | **2026-05-09** | **[PE-NBD-02/PE-JV] 대만 OSAT 파트너 선택 기준 매트릭스 (ASE/PTI/SPIL 비교 — PTI 권고)** |
| **v1.3** | **2026-05-09** | **[PE-JV] 지분 구조 3안 비교 (50:50 / 51:49 / 40:60) — 51:49 권고, 이익배분 50:50 별도** |
| **v1.3** | **2026-05-09** | **[PE-JV] JV 거버넌스 Term Sheet: 이사회 7인 구성, 캐스팅보트, Exit 조항, IP 귀속 원칙** |
| **v1.3** | **2026-05-09** | **[PE-NBD-05] 고객 LOI 3계층 전략 (TSMC 소개/한국 AI DC/글로벌 Hyperscaler)** |
| **v1.3** | **2026-05-09** | **[PE-NBD-05] 고객별 NDA→LOI 전환 타임라인 (NVIDIA M15 / SK-AWS M12 / 현대 M12)** |
| **v1.3** | **2026-05-09** | **[PE-NBD-05] LOI 조건 협상 포인트 (Take-or-Pay, ASP 연동, 독점 조항, Capacity Fee)** |
| **v1.3** | **2026-05-09** | **[PE-NBD-05] Phase 1 내 LOI ≥2개사 확보 월별 실행 플랜 (M0~M18)** |

---

## [CHAIN 메타데이터]

```yaml
chain_target: PE-NBD Full Chain + MECE-01
version: v1.3
created: 2026-05-09
author: Gilbert Kwak
version_history:
  - v1.0: 2026-05-09 (최초 작성)
  - v1.1: 2026-05-09 (Unit Economics + oS ASP + Phase Gate)
  - v1.2: 2026-05-09 (IP 전략 구체화 — PE-NBD-02 보완)
  - v1.3: 2026-05-09 (JV 파트너 구조 + 고객 LOI 전략 — PE-JV / PE-NBD-05 보완)
next_chain: MECE-01 -> PE-NBD-01 -> PE-NBD-02 -> PE-NBD-MKT -> PE-NBD-TECH -> PE-NBD-04 -> PE-NBD-05 -> PE-NBD-06 -> PE-NBD-08
pe3_target_score: ">=95"
expected_score: "95~96"
key_domain: PE-SEMI + PE-NBD + PE-FIN + PE-IP + PE-JV
test_status: READY
test_date: 2026-05-09
key_additions_v1.3:
  JV_partner:
    - 평가 대상: ASE / PTI / SPIL
    - 권고: PTI (종합 88점, 협력 유연성 최고)
    - 지분: 51:49 (한국:대만), 이익배분 50:50 별도 협의
    - 이사회: 7인 (한국 4 + 대만 3), 캐스팅보트 한국 측
    - Exit: Lock-up 5년, ROFR 6개월, Drag-along 양방 동의
    - IP: JV 공동 소유 60:40 수익 배분, 해산 시 비독점 라이선스 전환
  customer_LOI:
    - Tier1 TSMC루트: NVIDIA(M15), AMD(M18), Broadcom(M18)
    - Tier2 한국AI DC: SK-AWS(M12), 현대Saemangeum(M12)
    - Tier3 글로벌Hyperscaler: Microsoft Azure(M30)
    - Phase1 필수 LOI: SK-AWS(M12) + NVIDIA(M15) — 1K~1.5K wpm/월
    - LOI 조건: Take-or-Pay 60~70% / ASP ±5% 연동 / 선수금 10~15%
market_data_sources:
  - TrendForce 2026-04-27 (CoWoS ASP ~$10,000/wpm)
  - TrendForce 2026-05-06 (CoPoS Pilot 2026 Q1 착공, 2028 양산)
  - GlobalSemiResearch 2025-12-27 (OSAT 아웃소싱 240K~270K wpm/yr)
  - Lumenci 2025-06 (Advanced Packaging 특허 출원 CAGR 12~15%)
  - PatSnap 2026-03 (Hybrid Bonding + 2.5D 인터포저 IP 랜드스케이프)
  - Korea JoongAng Daily 2026-03-31 (SK Hynix ITC 특허 분쟁 사례)
```
