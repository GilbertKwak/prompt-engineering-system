# Multi-Agent Prompts

T-09 생태계 멀티에이전트 시스템 디렉토리.

## 프롬프트 인덱스

| 코드 | 이름 | PE-3 | 상태 |
|------|------|------|------|
| [MA-MoE-8AGENT-v1.0-OPT](./MA-MoE-8AGENT-v1.0-OPT.md) | MultiAgent MoE 8-Agent Analysis System — Master | 96 | ✅ Active |
| [MA-MoE-8AGENT-v1.0-KR](./MA-MoE-8AGENT-v1.0-KR.md) | MultiAgent MoE System — Variant-A (KR 특화) | 94 (예정) | 🔜 증식 예정 |
| [MA-MoE-8AGENT-v1.0-GLOBAL](./MA-MoE-8AGENT-v1.0-GLOBAL.md) | MultiAgent MoE System — Variant-B (글로벌 비교형) | 95 (예정) | 🔜 증식 예정 |

## 아키텍처 개요

```
MoE Router
    ├── Agent-1: Market Intelligence     (Blue Ocean Value Curve)
    ├── Agent-2: Technology Intelligence  (UltraRAG + TRL Matrix)
    ├── Agent-3: Competitive Intelligence (Porter 5F + BCG + Kano)
    ├── Agent-4: Risk Intelligence        (Bayesian Beta(2,9) + Agentic AI Risk)
    ├── Agent-5: Foresight Intelligence   (3시나리오 × 3구간 로드맵)
    ├── Agent-6: BizDev Intelligence      (ERRC Grid + Buyer Utility Map)
    ├── Agent-7: Synthesis Intelligence   (Mermaid2GIF + continuation_guard)
    └── Agent-8: IP Intelligence          (Patent White Space Map + FTO)

Shared Memory: Mastra OM-v1.0 (16K tokens)
Auto-Improve:  SkillRL Router
```

## 생태계 연계

- **Notion Primary**: C-33 PE-STRAT 라이브러리
- **Notion Secondary**: PE-OPT 자기진화 시스템
- **Master 연계**: T-09 PE-MASTER v10.0
- **KG**: v4.7+ 노드 8개 + 엣지 15개 추가 예정

---
_Last updated: 2026-05-21 KST_
