# prompts/strategy-collapse/

> **PE-STRAT · 반도체·AI 국가전략 붕괴 감시 에이전트 라이브러리 v1.0**  
> C-33 | knowledge_graph v4.4 반영 | 2026-04-30

## 포함 프롬프트

| 파일명 | 버전 | 분류 | PE-3 목표 |
|--------|------|------|-----------|
| `semi_strat_001_v6.2_opt_master.md` | v6.2 | Master (World A/B 병렬 평가) | 96 |
| `semi_strat_001_v6.0_opt_variant_a.md` | v6.0 | Variant-A (단일국가 경량) | 91 |
| `semi_strat_001_v6.1_opt_variant_b.md` | v6.1 | Variant-B (멀티국가 비교) | 93 |

## 연계 도메인

- **PE-AI** (C-28) — AI 플랫폼 전략 붕괴 감시
- **PE-SEMI** (C-29) — 반도체 전략 붕괴 감시
- **PE-EQP** (C-22) — 첨단 장비 전략 붕괴 감시
- **PE-MIN** (C-27) — 핵심광물 전략 붕괴 감시
- **PE-DC** (C-30) — AI 데이터센터 인프라 전략 붕괴 감시
- **PE-7** — AI 자동화 설계 및 구현

## 핵심 구조

- **World A/B 병렬 평가**: 정책 시나리오 A(현상 유지) vs B(붕괴 가속) 동시 추적
- **Bayesian SCP**: Beta(2,9) prior → 공급망 붕괴 확률 실시간 업데이트
- **EW 5종**: SEMI 3종 + AI 2종 조기경보 트리거
- **Collapse Typology**: CT-1(기술탈취) / CT-2(수출통제) / CT-3(생태계 분리)
- **Notion 페이지**: https://app.notion.com/p/35255ed436f0810f830be1feb1512c28
