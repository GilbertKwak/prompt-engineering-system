# PE-STRAT Prompt Version History

**Repository**: `GilbertKwak/prompt-engineering-system`  
**Path**: `prompts/strategy/`  
**Last Updated**: 2026-05-05

---

## Version History

| Version | Date | Commit | Changes | PE-3 Score |
|---------|------|--------|---------|------------|
| PE-STRAT-01 v2.0 | 2026-05-05 | feat(PE-STRAT): Upgrade v2.0 | MoE 라우팅 + RL 보상함수 + Pearl DAG 완전 구현 | 71 → 93 |
| PE-STRAT-02 v1.0 | 2026-05-05 | feat(PE-STRAT): Add investment variant | 투자특화 Variant 신규 (MPT+VaR+FF5F) | 신규 94 |
| PE-STRAT-01 v1.0 | 2026-05-05 | feat(PE-STRAT): Initial commit | 최초 생성 — 기본 골격 수립 | 71 |

---

## File Index

| ID | File | Type | Temp | PE-3 | Version | Status |
|----|------|------|------|------|---------|--------|
| PE-STRAT-01 | `pe_strat_01_v2.0.md` | 범용 전략 AI (Porter×Ng×Pearl) | 0.1/0.0 | 93 | v2.0 | ✅ Active |
| PE-STRAT-02 | `pe_strat_02_investment_v1.0.md` | 투자전략 전문가 (MPT·VaR·FF5F) | 0.05 | 94 | v1.0 | ✅ Active |
| ~~PE-STRAT-01~~ | ~~`pe_strat_01_v1.0.md`~~ | 초기 버전 | — | 71 | v1.0 | 🔴 Deprecated |
| ~~PE-STRAT-02~~ | ~~`pe_strat_02_v1.0.md`~~ | 초기 버전 | — | — | v1.0 | 🔴 Deprecated |

---

## Cross-Reference Map

```
PE-STRAT-01 v2.0 (범용 전략 AI)
    ├── INPUT  ← FC-MASTER MODE 1 (수치 검증)
    ├── OUTPUT → PE-IS-02 (전략 분석 구조화)
    ├── OUTPUT → PE-PM-03 (Phase Gate 연계)
    ├── OUTPUT → PE-STRAT-02 (투자 정량화)
    └── TOOL     P-07 (Recursive Decompose)

PE-STRAT-02 v1.0 (투자 특화 Variant)
    ├── INPUT  ← PE-STRAT-01 (거시 전략)
    ├── INPUT  ← FC-MASTER (IRR·NPV·VaR 검증)
    ├── OUTPUT → PE-CON (Investment Memo·IR 덱)
    ├── OUTPUT → PE-9 AstraChips LP Fund
    └── OUTPUT → HBM Salvage Phase 1 Gate
```

---

## PE-3 Score Tracking

| Prompt | Clarity | Structure | Specificity | Actionability | Applicability | Total |
|--------|---------|-----------|-------------|---------------|---------------|-------|
| PE-STRAT-01 Before | 72 | 78 | 65 | 69 | 74 | 71 |
| PE-STRAT-01 v2.0 | 93 | 95 | 92 | 93 | 92 | **93** |
| PE-STRAT-02 v1.0 | 94 | 95 | 94 | 95 | 92 | **94** |
