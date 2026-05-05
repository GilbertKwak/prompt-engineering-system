# PE-STRAT 프롬프트 버전 이력 (SSOT)

> **경로**: `prompts/strategy/`  
> **최종 업데이트**: 2026-05-05  
> **관리 원칙**: GitHub = SSOT · Notion PE-STRAT 섹션과 동기화

---

## 📋 프롬프트 인덱스

| ID | 파일 | 유형 | Temp | PE-3 Before | PE-3 After | 버전 | 상태 |
|---|---|---|---|---|---|---|---|
| PE-STRAT-01 | `pe_strat_01_v2.0.md` | 범용 전략 AI 아키텍트 (Porter×Ng×Pearl · MoE · RL) | 0.1 / 0.0 | 71 | 93 | v2.0 | ✅ Active |
| PE-STRAT-02 | `pe_strat_02_investment_v1.0.md` | 투자전략 전문가 Variant (MPT · VaR · Fama-French 5F) | 0.05 | — | 94 | v1.0 | ✅ Active |

---

## 🔄 버전 변경 이력

### v2.0 — 2026-05-05
**변경 유형**: PE-STRAT-01 완전 최적화 업그레이드 + PE-STRAT-02 신규 등록

#### PE-STRAT-01 v2.0 변경 내역
- **역할 확장**: Porter 5-Forces + Ng 인과추론 + Pearl Causal DAG 완전 통합
- **MoE 라우팅**: 6개 도메인 동적 가중치 시스템 도입
  - market_research=0.25, risk_analysis=0.20, forecasting=0.20, new_business=0.15, investment=0.15, geopolitics=0.05
- **RL 보상함수**: Causal_Depth(β=0.35) + Logical_Consistency(γ=0.25) + Actionability(δ=0.20) + Evidence_Quality(ε=0.20)
- **확신도 등급**: HIGH/MEDIUM/LOW 3단계 기준 명시화
- **8단계 워크플로우**: 입력분류→에이전트실행→검증→업데이트 체계 구축
- **3-Engine 연계**: PE-1 자동개선 / PE-2 자동증식 / PE-3 자동검증 완전 연동
- **PE-3 점수**: 71 → 93 (+22 pts)
  - Clarity: 72 → 93
  - Structure: 78 → 95
  - Specificity: 65 → 92
  - Actionability: 69 → 93
  - Applicability: 74 → 92

#### PE-STRAT-02 v1.0 신규 등록
- **역할**: 글로벌 자산운용사 CIO + 헤지펀드 PM 역할 특화
- **핵심 프레임워크**: Markowitz MPT · Sharpe/Sortino Ratio · VaR(99%) · Fama-French 5-Factor
- **MoE 투자 가중치**: P(investment)=0.50 (투자 집중 특화)
- **출력 산출물**: Portfolio Allocation Table + Risk Dashboard + Investment Memo
- **Temperature**: 0.05 (포트폴리오 계산 정밀도 최우선)
- **RL 보상함수**: Quantitative_Rigor(α=0.30) + Risk_Accuracy(β=0.25) + Return_Precision(γ=0.25) + Execution_Clarity(δ=0.20)
- **PE-3 점수**: 94 (신규 등록)

**커밋**: `feat(PE-STRAT): Register PE-STRAT-01 v2.0 + PE-STRAT-02 v1.0 — PE-3 93/94 (2026-05-05)`

---

### v1.0 — 2026-05-05 (최초 생성)
- PE-STRAT-01 v1.0 초안 등록
- Porter 5-Forces 기반 기본 전략 프롬프트
- PE-3 점수: 71/100

---

## 🔗 연계 시스템

| 시스템 | 연결 경로 |
|---|---|
| Notion PE Hub | `프롬프트 엔지니어링 시스템 허브 v2.0` → PE-STRAT 섹션 |
| PE-1 자동개선 | 입력 최적화 루프 적용 |
| PE-2 자동증식 | 도메인별 변형 버전 생성 |
| PE-3 자동검증 | 5차원 품질 채점 (목표 90+) |
| PE-10 멀티에이전트 | P-07 Recursive Decompose 연계 |
| master-agent-v4.0b | 분석 시스템 v4.0 연동 |
| multi-agent-system-v3-hybrid | MoE 라우팅 실행 환경 |

---

## ⚠️ 오류 예방 체크리스트 (PE-STRAT 전용)

| # | 검증 항목 | 기준 | 담당 엔진 |
|---|---|---|---|
| 1 | MoE 가중치 합산 = 1.00 | Σ weights = 1.00 ± 0.001 | PE-3 수식 검증 |
| 2 | RL 보상함수 계수 합산 = 1.00 | α+β+γ+δ = 1.00 | PE-3 수식 검증 |
| 3 | Temperature 범위 | 0.0 ≤ T ≤ 0.3 (전략 도메인) | PE-1 파라미터 검증 |
| 4 | Pearl DAG 노드 최소 개수 | ≥ 5개 노드 | PE-3 구조 검증 |
| 5 | 출력 산출물 명시 여부 | 3개 이상 구체적 산출물 기술 | PE-3 완전성 검증 |
| 6 | PE Hub Notion 동기화 | 등록 후 24시간 이내 | 수동 확인 |
