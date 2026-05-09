# business_proposal_HBM4_AI_infra v1.0
# PE-NBD Full Chain 테스트용 입력 제안서
# 작성일: 2026-05-09 | 작성자: Gilbert Kwak
# 목적: PE-NBD-01 → 08 Full Chain 검증 + MECE-01 선행
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

## [SECTION 2] 시장 기회 (Market Opportunity)

### 2-1. TAM / SAM / SOM

| 구분 | 정의 | 추정 규모 |
|------|------|-----------|
| TAM | 글로벌 HBM 전체 시장 (HBM3E + HBM4) | $3.17B (2025) → $12.44B (2030), CAGR ~26% |
| TAM2 | 글로벌 고급 패키징 oS/CoW 아웃소싱 시장 | CoWoS oS portion 2026: ~5K wpm → 2027: ~8K wpm |
| SAM | TSMC 외부 아웃소싱 WoS/oS 수요 (OSAT 기회) | 전체 oS의 ASE/SPIL 65%+ 점유 → 나머지 35% 오픈 |
| SOM | 우리 JV가 3년 내 포착 가능한 한국 클러스터 물량 | 예상 oS 2~3K wpm 수준 (점유 ~20~30% 목표) |

> 근거:  
> - HBM 시장 CAGR 21.35~30% (2024→2033) — SK하이닉스 공식 전망 포함  
> - TSMC CoWoS: 2026년 13K wpm → 2027년 16K wpm 확대, WoS oS는 OSAT로 이관 가속  
> - Korea AI DC 투자 $30B+ (SK-AWS $5.1B, 현대 $6.3B 등 포함) — 한국 내 패키징 수요 직결

### 2-2. 수요 촉진 요인 (Demand Drivers)

1. **AI DC Capex 폭발**: 한국 정부 AI 예산 9.9조원(2026), hyperscaler 투자 $30B+ 확정
2. **HBM4 진입**: HBM4 인터페이스 2,048bit, BW 1.5~2TB/s — 전 세대 대비 ~2배 성능 → 고급 패키징 수요 급증
3. **TSMC 아웃소싱 전략**: CoWoS full flow 아웃소싱 2H26부터 본격화 예정 — OSAT 역할 확대
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

## [SECTION 4] 경쟁 분석 (Competition)

### 4-1. 주요 경쟁자 매트릭스

| 플레이어 | 포지션 | 강점 | 약점/기회 |
|----------|--------|------|----------|
| ASE/SPIL | 글로벌 OSAT 1위 (oS 65%+) | 규모·기술력·TSMC 관계 | 대만 집중 리스크, 한국 거점 부재 |
| Amkor Technology | OSAT 2위 | 미국·유럽 고객 기반, 다지역 | HBM 특화 패키징 역량 제한적 |
| PTI (Power Tech) | OSAT 3위 | 대만 로컬 | 규모 작음, 한국 진출 없음 |
| TSMC (자체) | CoW 전면 독점 | 기술·고객 신뢰 | Capex 부담으로 oS 아웃소싱 전략 선택 |
| **우리 JV** | **한국 신규 진입** | **한국 AI DC 근접성, HBM 공급망 proximity** | **초기 레퍼런스 부재 → 극복 전략 필요** |

### 4-2. 포지셔닝 전략 (2×2)

```
           고급 패키징 기술력
                 ↑ High
                 |  [TSMC]
                 |
      [ASE/SPIL] |         [우리 JV 목표 위치]
                 |
                 |  [Amkor] [PTI]
                 |________________________→
           Low               High
                   한국·AI DC 근접성
```

---

## [SECTION 5] 실행 로드맵 (Execution Roadmap)

### Phase 1 — JV 설립 & 기반 구축 (0~18개월)
- JV 파트너 확정 (대만 OSAT 1사 + 한국 대기업 1사)
- 부지 선정 (경기 북부 또는 충청권 반도체 클러스터)
- Pilot 라인 구축: WoS/oS 공정 — 1K wpm 목표
- TSMC 아웃소싱 공식 파트너 인증 획득 (Qualified Supplier)

### Phase 2 — 물량 확보 & 스케일업 (18~36개월)
- TSMC oS 아웃소싱 물량 수주 2~3K wpm
- 한국 AI DC 프로젝트(SK-AWS, 현대 등) HBM 패키징 직접 공급계약
- Capex Phase 2: 총 라인 5K wpm 수준으로 확장

### Phase 3 — IP·고마진 포트폴리오 (36~60개월)
- CoW/RDL 자체 IP 개발 + 라이선스 수익화
- HBM5 대비 차세대 패키징 선행 개발 착수
- 미국·일본 거점 검토 (CHIPS Act 활용)

---

## [SECTION 6] 핵심 지표 (KPIs)

| KPI | Year 1 목표 | Year 3 목표 |
|-----|------------|------------|
| Utilization Rate | 70% | 88% |
| oS Capacity | 1K wpm | 5K wpm |
| 수율 | 90% | 96% |
| Revenue | $150M | $800M |
| EBITDA Margin | 18% | 28% |
| TSMC 인증 완료 | Q4 Y1 | 유지 |
| 주요 고객사 수 | 2 | 6 |

---

## [SECTION 7] 리스크 및 대응 (Risks & Mitigation)

| 리스크 유형 | 내용 | Mitigation |
|------------|------|------------|
| 기술 리스크 | HBM4 패키징 수율 초기 낮음 | 대만 파트너 기술이전 + 파일럿 단계 수율 검증 |
| 수요 사이클 | AI Capex 2027~28 조정 가능성 | 장기 Capacity Reservation 계약 선행 |
| 경쟁 심화 | ASE 한국 진출 or 삼성 자체화 | 특화 서비스(한국 AI DC 전용) + JV 파트너십 고착화 |
| 지정학 | 미·중 규제, TSMC 아웃소싱 정책 변경 | 미국 CHIPS Act 인증 병행, 고객 다변화 |
| 자본 리스크 | Capex 초기 집중 | Phase-gate Capex + 정부 보조금(한국 AI R&D 예산) 병행 |

---

## [SECTION 8] 투자 포인트 요약 (Executive Summary)

**왜 지금인가:**
- AI DC $30B+ 한국 투자 확정 → 로컬 패키징 수요 구조적 발생
- TSMC CoWoS oS 아웃소싱 본격화 → OSAT 기회 윈도우 2026~28년이 최적 진입 시점
- HBM 글로벌 공급망 80%+가 한국에 집중 → 패키징까지 한국에서 완결하는 구조적 논리

**투자 포인트 (Top 3):**
1. AI DC Capex 사이클 최상단의 구조적 수혜 포지션
2. TSMC 아웃소싱 전략 직접 수혜 — 글로벌 OSAT 경쟁에서 한국 proximity가 차별화
3. 한국 정부 AI·반도체 예산($5.8B+) + 정책 금융 레버리지 가능

**핵심 리스크:**
- AI Capex 사이클 조정 시 Utilization 급락
- 초기 TSMC 인증·수율 확보 지연 리스크

---

## [CHAIN 메타데이터]

```yaml
chain_target: PE-NBD Full Chain + MECE-01
version: v1.0
created: 2026-05-09
author: Gilbert Kwak
next_chain: MECE-01 -> PE-NBD-01 -> PE-NBD-02 -> PE-NBD-MKT -> PE-NBD-TECH -> PE-NBD-04 -> PE-NBD-05 -> PE-NBD-06 -> PE-NBD-08
pe3_target_score: ">=92"
key_domain: PE-SEMI + PE-NBD + PE-FIN
test_status: READY
test_date: 2026-05-09
```
