# PE-DD · Strategic Due Diligence Prompt Library
# GitHub SSOT: prompts/PE-DD/
# 최초 생성: 2026-05-07

## 프롬프트 파일 인덱스

| ID | 파일 | 유형 | Temperature | PE-3 점수 | 버전 | 상태 |
|---|---|---|---|---|---|---|
| OPT-DD | opt_dd_v1.0.md | 범용 실사 (7-Layer + Pearl DAG) | 0.0/0.1 | 예상 93 | v1.0 | ✅ Active |
| OPT-DD-SEMI | opt_dd_semi_v1.0.md | 반도체/장비 특화 실사 | 0.0 | 예상 92 | v1.0 | ✅ Active |
| OPT-DD-FIN | opt_dd_fin_v1.0.md | 투자 IR/Pitch Deck 실사 | 0.0/0.1 | 예상 93 | v1.0 | ✅ Active |
| OPT-DD-POLICY | opt_dd_policy_v1.0.md | 정책/정부 문서 실사 | 0.0 | 예상 91 | v1.0 | ✅ Active |

## 3-Engine 적용 결과 (2026-05-07)

| 차원 | Before (원본 v5.0) | After (OPT-DD v1.0) | 개선폭 |
|---|---|---|---|
| 명확성 (Clarity) | 72 | 94 | +22 |
| 구조성 (Structure) | 78 | 95 | +17 |
| 특이성 (Specificity) | 65 | 93 | +28 |
| 실행가능성 (Actionability) | 68 | 93 | +25 |
| 적용가능성 (Applicability) | 70 | 92 | +22 |
| **PE-3 총점** | **70.6** | **~93.4** | **+22.8pts** |

## 생태계 포지셔닝

```
[외부 자료 입력]
       ↓
[PE-DD: 실사·검증 게이트] ← 유일한 DD 레이어
       ↓
[PE-STRAT / PE-DEEP: 전략 분석]
       ↓
[PE-FIN: 재무 모델링]
       ↓
[PE-3 자동검증]
```

## 버전 이력

| 버전 | 날짜 | 변경 내용 |
|---|---|---|
| v1.0 | 2026-05-07 | 🔍 PE-DD v1.0 신규 등록 — OPT-DD 범용 + SEMI/FIN/POLICY 3종 변형, StrategicDueDiligencePrompt v5.0 기반 PE-1 3-Loop 최적화, 원본 70.6 → 예상 93.4 (+22.8pts), Pearl DAG + 7-Layer + Risk Scoring Matrix 통합 |
