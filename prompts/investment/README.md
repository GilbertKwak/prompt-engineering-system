# Investment Prompts — 전략 투자심사 프롬프트 라이브러리

> **경로**: `prompts/investment/`
> **목적**: 대기업 전략기획실 및 투자심의위원회용 투자심사 AI 프롬프트 관리

## 파일 목록

| 파일 | 버전 | 설명 | 최종수정 |
|------|------|------|----------|
| `STRATEGIC_INVESTMENT_REVIEW_v1.md` | v1.0 | 4-in-1 통합 최적화 프롬프트 (Multi-Agent) | 2026-05-19 |

## 프롬프트 계보

원본 4개 프롬프트 → 통합 최적화:
1. `StrategicInvestmentReviewPrompt` (기본 투자검토)
2. `StrategicInvestmentDecisionPrompt` (의사결정 중심)
3. `StrategicInvestmentReviewPrompt` (산업별 특화)
4. `StrategicInvestmentAgentSystem` (Multi-Agent 시스템)

**통합 원칙**:
- 중복 역할/원칙 제거 (약 40% 축약)
- 의사결정 중심으로 재구조화
- Multi-Agent + 산업별 가중치 유지
- Self-check 6개 항목으로 통합

## 적용 가이드

```
단일 투자안 → STRATEGIC_INVESTMENT_REVIEW_v1.md
복수 투자안 비교 → 동일 프롬프트 (PortfolioAgent 자동 활성화)
```

## 생태계 연계

```
GitHub prompts/investment/ ←→ Notion PE-FIN 데이터베이스
                           ←→ AI Intel Weekly (산업 인텔 피드)
                           ←→ Knowledge Graph (투자 대상 노드)
```
