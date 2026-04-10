# HBM Salvage Value Program — Chapter 1
## HBM 수율 손실의 수익 전환 전략 | Turning HBM Yield Loss into Revenue

**버전**: v1.1 (Upgraded + Auto-Verified)  
**작성일**: 2026-04-10  
**관리자**: Gilbert Kwak  
**검증 방식**: PE-3 자동검증 엔진 (3-Engine 통합 파이프라인)  
**파일 형식**: KO·EN 병렬 보고서

---

## 📋 작성 규칙 (Writing Rules — 본 보고서 적용 기준)

> **🔒 규칙 제정일**: 2026-04-10 | 모든 후속 챕터에 동일 규칙 적용

### R-1. Notion & GitHub 사전 확인 의무
- 보고서 작성 시작 전 **Notion 허브** 및 **GitHub PE-4-HBM-Salvage 폴더** 현황 반드시 확인
- 기존 챕터 내용과의 중복·모순 여부 사전 점검
- 진행 상태(완료/진행 중/미착수) 확인 후 작성 순서 결정

### R-2. 한국어 先 → 영문 後 작성 순서
- KO 초안 완성 → PE-3 검증 → KO 확정 → EN 재표현 순서 준수
- 직역 금지: EN은 KO 기반 재표현 + 글로벌 독자 최적화

### R-3. PE-3 자동검증 체크리스트 필수 포함
- 모든 챕터 말미에 검증 체크리스트 테이블 첨부
- 7개 검증 항목 기준: 시장 데이터 정합성, 수율 수치 일관성, 산정 공식, 불량 유형 완전성, 타이밍 논거, 경쟁 구도, 데이터 경고 사항

### R-4. 작성 완료 후 Notion + GitHub 동기화 의무
- 작성 완료 즉시 GitHub `applied-cases/PE-4-HBM-Salvage/` 폴더에 커밋
- Notion 허브 버전 이력 테이블 업데이트
- 진행 현황 표(전체 목록 / 완료 / 미착수) 출력 필수

### R-5. 챕터 간 연속성 보장
- 매 챕터 말미 "다음 장 Bridge" 섹션 포함
- 전 챕터 핵심 결론 → 현 챕터 첫 문단에서 요약 연결

---

## 1.1 Executive Summary

**[KO]** HBM(High Bandwidth Memory) 시장은 2026년 BofA 추산 **$54.6B** 규모로 전년 대비 **58% 급성장**하는 구조적 슈퍼사이클에 진입했다. 이 폭발적 성장은 동시에 업계에서 거의 다뤄지지 않는 역설적 기회를 만들어낸다 — SK hynix의 수율 ~90% 대비 Samsung의 수율 60~70% 격차에서 발생하는 **연간 $2.7~4.0B 규모의 잠재 Salvage 가치**가 바로 그것이다.

**[EN]** The HBM market has entered a structural supercycle, with BofA estimating its 2026 size at **$54.6 billion** — a 58% year-over-year surge. This explosive growth simultaneously creates a paradoxical opportunity that the industry has scarcely addressed: the **$2.7–4.0B annual Salvage value potential** arising from the 20–30 percentage-point yield gap between SK hynix (~90%) and Samsung (60–70%).

---

## 1.2 HBM 시장 거시 지형 | Macro Market Landscape

**[KO]** 2026년은 HBM3E가 시장의 약 **67%**를 지배하는 가운데 HBM4가 점진적으로 진입하는 전환기다. Goldman Sachs는 ASIC용 HBM 수요가 **82% 급증**해 전체 시장의 1/3을 차지할 것으로 전망하며, 월 웨이퍼 생산량은 전 업체 합산 **250,000매(+47% YoY)**에 달한다.

**[EN]** 2026 marks a transition year in which HBM3E commands approximately **67%** of the market while HBM4 begins its gradual ramp-up. Goldman Sachs projects that ASIC-driven HBM demand will surge **82%**, capturing one-third of the total market, with combined monthly wafer output reaching **250,000 wafers (+47% YoY)**.

### 공급 측 양강 구도 | Duopoly Supply Structure

| 지표 | SK hynix | Samsung | 비고 |
|---|---|---|---|
| HBM 시장 점유율 (Q1 '26) | **62%** | ~16% → 35% 목표 | 점유율 역전 진행 중 |
| 수율 / Yield | **~90%** | 60–70% | 20–30%p 격차 |
| 공정 기술 | 1b-nm (성숙) | 1c-nm (초기 불안정) | MR-MUF vs TC-NCF |
| 월 웨이퍼 (추정) | ~100,000매 | ~80,000매 | 250K 전체 중 배분 |

---

## 1.3 수율 손실 규모 정량화 | Quantifying the Yield-Loss Pool

**[KO]** Samsung의 월 불량 다이 수는 약 **280만 개**로 추산되며, Salvage 단가($80~120/die, 정상품 ASP의 약 10%)를 적용하면 월 $224M~336M, **연간 $2.7~4.0B**의 잠재 Salvage 가치가 발생한다. SK hynix 기준으로도 연간 $1.0~1.4B의 잠재 가치가 존재하나, 수율이 높아 상대적으로 회수 물량이 적다.

**[EN]** Samsung's monthly defective die count is estimated at approximately **2.8 million units**. Applying a Salvage price of $80–120 per die (~10% of prime ASP), this translates to $224M–336M monthly latent revenue, or **$2.7–4.0B annually**. SK hynix, with higher yields, generates $1.0–1.4B in annual potential.

### 불량 유형별 회수 가능률 | Defect-Type Recovery Matrix

| 불량 유형 | 빈도 | SK hynix | Samsung | Salvage 회수율 |
|---|---|---|---|---|
| Test BW / 채널 불량 | High | 일부 재분류 | 다수 발생 | **60–80% ← 최우선** |
| Thermal stress | Low | 패키지 설계 성숙 | 일부 보완 중 | 50–70% |
| Micro-bump bonding | Med | MR-MUF 선도 | TC-NCF 병행 | 40–60% |
| DRAM Cell 불량 | High | 1b-nm 성숙 → 낮음 | 1c-nm 초기 → 높음 | 30–50% |
| TSV open/short | Med | 안정적 | 개선 진행 중 | 20–40% |
| Stacking misalignment | Med-High | 1c-nm warpage 이슈 | warpage 이슈 多 | 10–30% |

---

## 1.4 왜 지금인가 | Why Now

1. **수율 격차 피크** — Samsung 1c-nm 안정화 전(2027~2028) 불량 풀 최대
2. **HBM4 전환기** — 중간 등급 시장 공백 → Salvage HBM 유일한 대안
3. **AI 스타트업 비용 압박** — HBM 비중 30~40%, 50~60% 할인 대안 수요
4. **ESG 자원 효율화 압력** — 그린 제조 이니셔티브 포지셔닝 가능

---

## 1.5 경쟁 구도 | Competitive Landscape

**선점 윈도우: 18개월 (2026 Q2 ~ 2027 Q4)**

| 플레이어 | 현황 | Salvage 사업화 가능성 |
|---|---|---|
| Micron | HBM3E 진입 초기, 불량 물량 적음 | 낮음 |
| Samsung | MR-MUF 전환·수율 개선 집중 | 미확인 — 선점 기회 존재 |
| SK hynix | 브랜드 보호 중심, Salvage 비공개 | 내부 검토 단계 추정 |
| ASE / Amkor | 재패키징 기술 보유 | 파트너 채널 활용 가능 |

---

## 1.6 PE-3 자동검증 체크리스트

| 검증 항목 | 상태 | 근거 |
|---|---|---|
| ✅ 시장 데이터 정합성 | PASS | BofA $54.6B, GS +82% — KO·EN 일치 |
| ✅ 수율 수치 일관성 | PASS | SKH ~90%, Samsung 60~70% — 양파일 동일 |
| ✅ Salvage 가치 산정 공식 | PASS | (1-수율)×웨이퍼×100다이×단가 재현 가능 |
| ✅ 불량 유형 완전성 | PASS | 6개 유형 전체 포함, 회수율 명시 |
| ✅ 타이밍 논거 4항목 | PASS | ①②③④ KO·EN 정렬 완료 |
| ✅ 경쟁 구도 4개 플레이어 | PASS | Micron/Samsung/SKH/ASE 전체 포함 |
| ⚠️ HBM4 점유율 데이터 | CAVEAT | 2026년 실시간 데이터 추가 검증 권고 |

---

## 1.7 다음 장 Bridge

**다음 챕터 예정**: Chapter 2 — HBM 불량 구조 분석  
**내용**: 공정 단계별 불량 유형 분해, Samsung vs. SK hynix 불량 프로파일 정량 비교

---
*작성일: 2026-04-10 | Version: v1.1 | 검증: PE-3 자동검증 완료*
