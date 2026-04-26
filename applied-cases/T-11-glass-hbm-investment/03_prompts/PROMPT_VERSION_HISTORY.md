# PROMPT_VERSION_HISTORY.md
# T-11 | Glass/HBM 투자전략 허브 — 프롬프트 버전 이력 마스터
# SSOT: applied-cases/T-11-glass-hbm-investment/03_prompts/
# Last Updated: 2026-04-26

---

## 버전 이력 테이블

| 버전 | 파일명 | 날짜 | 내용 요약 | PE-3 | 상태 |
|------|--------|------|-----------|------|------|
| v1.0 | v1_core_satellite_hedge.md | 2026-03-01 | Core/Satellite/Hedge 3축 전략 최초 설계. 티켓 사이즈·IRR·MOIC·리스크 시나리오 정의. Python 재무모델 scaffold. | 90/100 | 🟢 Active |
| v2.0 | v2_financial_model.md | 2026-03-01 | Python IRR/MOIC/NPV 모델 완성. 시나리오 4종(Conservative/Balanced/Aggressive/Geo-Hedge). 포트폴리오 배분 최적화. | 92/100 | 🟢 Active |
| v3.0 | agent_1_expanded_profile_v2.0.md | 2026-04-26 | Agent-1 확장 프로파일. 12국×10레이어 산업 데이터 수집 프레임워크. Sub-Agent 4종(1a/1b/1c/1d). BS/VS 공식 정의. OUTPUT 1.1~1.5 완성. G-01~G-10 해소. | 95/100 | 🟢 Active |
| v4.0 | agent_2_dependency_bottleneck_profile_v2.0.md | 2026-04-26 | Agent-2 완전판. DSM 매트릭스, Type A/B/C VS 완전 수치화, 포트폴리오 통합 노출도(1.785), 스트레스 테스트 5종, Agent-3 핸드오프 YAML, Validation Gate 7항목. E-04/E-07 해소. | 95/100 | 🟢 Active |
| **v5.0** | **agent_3_scenario_planning_profile_v1.0.md** | **2026-04-26** | **Agent-3 시나리오 플래닝 프로파일. Agent-2 Handoff YAML 수신. 4-World 프레임워크, 확률×수익 매트릭스, EV_MOIC 6.149x/EV_IRR 37.0%, Monte Carlo 500회(원금손실 7.3%), 동적 리밸런싱 5종, HBM 사이클 오버레이, Agent-4 핸드오프 YAML. OUTPUT 3.1~3.7 완성.** | **95/100** | **🟢 Active** |

---

## 다음 버전 예정

| 버전 | 예정 파일명 | 내용 | 목표 일정 |
|------|------------|------|-----------|
| v6.0 | agent_4_investment_execution_v1.0.md | Agent-4 투자 실행 모델 — DD 체크리스트, Term Sheet, Exit 구조 | 2026-04-26 (Agent-3 후속) |

---

## 파일 구조

```
03_prompts/
├── PROMPT_VERSION_HISTORY.md               ← 이 파일 (v5.0 갱신)
├── v1_core_satellite_hedge.md              ← v1.0
├── v2_financial_model.md                   ← v2.0
├── agent_1_expanded_profile_v2.0.md        ← v3.0 (PE-3 95/100)
├── agent_2_dependency_bottleneck_profile_v1.0.md  ← v4.0 구버전 보관
├── agent_2_dependency_bottleneck_profile_v2.0.md  ← v4.0 완전판 (PE-3 95/100)
└── agent_3_scenario_planning_profile_v1.0.md      ← v5.0 신규 ✅
```
