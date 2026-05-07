# PE-STRAT Prompt Version History

| Version | Code | Date | PE-3 | Description |
|---------|------|------|------|-------------|
| v1.1 | OPT-GHCRA | 2026-05-07 | ~96 | F1 HANDOFF수신+PE-FIN라우팅 / F2 PE-3자동검증 / F3 Worked Example |
| v1.1 | OPT-CSGS | 2026-05-07 | ~96 | F1 HANDOFF수신/발신 / F2 PE-3자동검증 / F3 HoldCo-K연속예시 |
| v1.1 | OPT-AOCRS | 2026-05-07 | ~97 | F1 HANDOFF_PACKET신설 / F2 PE-3자동검증 / F3 Worked Example |
| v1.0 | OPT-GHCRA | 2026-05-07 | ~94 | Global Hedge Fund & Regulatory Control Risk Analysis — PE-1 3-Loop |
| v1.0 | OPT-CSGS | 2026-05-07 | ~94 | Chaebol Succession & Global Control Simulation — PE-1 3-Loop |
| v1.0 | OPT-AOCRS | 2026-05-07 | ~95 | Advanced Ownership Control Risk Strategy — PE-1 3-Loop |
| v1.0 | OPT-SFA | 2026-05-07 | ~93 | Strategic Forecasting Agent — PE-1 3-Loop |
| v1.0 | OPT-AIF | 2026-05-07 | ~94 | Advanced Insight Forecasting — PE-1 3-Loop |
| v2.0 | pe_strat_01 | 2026-05-05 | — | PE-STRAT 기존 전략 프롬프트 v2.0 |
| v3.1 | SAuRP | 2026-05-05 | — | SAuRP Strategy Unified Research Prompt |
| v2.0 | PHFA | 2026-05-05 | — | Predictive Horizon Forecasting Agent |
| v2.0 | GIPA | 2026-05-05 | — | Global Intelligence & Prediction Agent |
| v1.0 | AUTOPLUS | 2026-05-05 | — | Auto Plus Strategy |

## F1~F3 HIGH 우선순위 변경 요약 (2026-05-07)

### [F1] Cross-prompt 자동 데이터 흐름 강제화
- HANDOFF_PACKET 표준 YAML 구조 신설
- AOCRS → CSGS → GHCRA → PE-FIN 자동 전파
- DD_PACKET 전체 파이프라인 릴레이 보장
- 중간 재입력 불필요 (`--from-aocrs`, `--from-csgs` 플래그)

### [F2] PE-3 자동검증 트리거 내장
- 각 프롬프트 Output Contract에 5항목 체크리스트 추가
- SCORE_GATE: 90 미만 시 `/rerun --loop1` 자동 발동
- AUTO_SCORE: X/5 → PE-3 점수 추정 자동 연산

### [F3] 실사용 예제(Worked Example) 내장
- 가상 기업 HoldCo-K 기반 연속 실행 사례
- AOCRS(Layer 1-4) → CSGS(Stage 2 상속세) → GHCRA(Module 3 스코어카드) → PE-FIN 라우팅
- 입력→분석→HANDOFF→검증 전 과정 샘플 제공

## Pipeline Architecture (2026-05-07 현재)
```
[PE-DD: 실사 검증]
      ↓ DD_GATE + DD_PACKET
[OPT-AIF: 인사이트 추출·시나리오]     ← 전략 예측 단발
      ↓ Insight ID
[OPT-SFA: 장기 추적·수정 에이전트]    ← 지속 추적
      ↓ HANDOFF_PACKET
[OPT-AOCRS v1.1: 지배구조 위험·공격방어] ← 오너십 위험
      ↓ HANDOFF_PACKET (F1)
[OPT-CSGS v1.1: 재벌 승계·통제 시뮬레이션] ← 승계 위험
      ↓ HANDOFF_PACKET (F1)
[OPT-GHCRA v1.1: 국가별 규제·헤지펀드 공격] ← 글로벌 위험
      ↓ PE_FIN_ROUTING_PACKET (F1)
[PE-FIN: FIN-07/08 재무 모델링]       ← 최종 가치 판단
```
