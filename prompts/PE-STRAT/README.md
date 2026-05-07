# PE-STRAT — Strategic Analysis Prompt Library

## 디렉토리 구조

| 파일 | 버전 | PE-3 | 역할 | 연계 |
|------|------|------|------|------|
| `opt_aif_v1.0.md` | v1.0 | 94 | 6-Phase 인사이트 예측 분석 | PE-DD → AIF → SFA |
| `opt_sfa_v1.0.md` | v1.0 | 93 | 장기 추적·수정 에이전트 | AIF → SFA → PE-FIN |

## 생태계 포지셔닝

```
[외부 자료]
     ↓
[PE-DD: 실사 검증 게이트]  ← OPT-DD v1.0
     ↓
[PE-STRAT: 전략 분석]
  ├─ OPT-AIF v1.0  ← 핵심 인사이트 추출 + 시나리오 (단발)
  └─ OPT-SFA v1.0  ← 장기 추적 + 루프 업데이트 (지속)
     ↓
[PE-DEEP: 심층 분석]
     ↓
[PE-FIN: 재무 모델링]
     ↓
[PE-3: 자동 검증]
```

## 빠른 실행

```bash
# AIF 단발 분석
/aif run TARGET="[대상]" DOMAIN="[도메인]" DEPTH="Full" HORIZON="24M"

# SFA 연계 파이프라인
/aif run TARGET="[대상]" DEPTH="Full" | /sfa init --from-aif

# 업데이트
/sfa update INSIGHT_ID="[ID]" NEW_SIGNALS="[변화]"
```

## GitHub SSOT
- 커밋: `feat(PE-STRAT): Add OPT-AIF v1.0 + OPT-SFA v1.0`
- 등록일: 2026-05-07
