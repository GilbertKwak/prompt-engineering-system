# Multi-Agent Prompts

T-09 생태계 멀티에이전트 시스템 디렉토리.  
**MoE(Mixture-of-Experts) Router** 기반 8-Agent 병렬 분석 아키텍처 3종 수록.

---

## 프롬프트 인덱스

| 코드 | 이름 | PE-3 | 상태 | 특화 |
|------|------|------|------|------|
| [MA-MoE-8AGENT-v1.0-OPT](./MA-MoE-8AGENT-v1.0-OPT.md) | MultiAgent MoE 8-Agent — Master | **96** | ✅ Active | 범용 베이스라인 |
| [MA-MoE-8AGENT-v1.0-KR](./MA-MoE-8AGENT-v1.0-KR.md) | MultiAgent MoE — Variant-A KR 특화 | **94** | ✅ Active | 한국 4대 플레이어 + EW-KR/GEO + HBM 병목 |
| [MA-MoE-8AGENT-v1.0-GLOBAL](./MA-MoE-8AGENT-v1.0-GLOBAL.md) | MultiAgent MoE — Variant-B 글로벌 비교형 | **95** | ✅ Active | 5개국×8Agent 매트릭스 + World C/D 시나리오 |

---

## 아키텍처 개요

```
MoE Router (SkillRL 자동개선)
    ├── Agent-1: Market Intelligence
    │       Blue Ocean Value Curve + Six Path + KOTRA/KITA 정책 데이터
    ├── Agent-2: Technology Intelligence
    │       UltraRAG hybrid_dense_sparse (ArXiv/USPTO/IEEE) + TRL Matrix
    ├── Agent-3: Competitive Intelligence
    │       Porter 5F + BCG Matrix + Kano Model + KR/GLOBAL Player DB
    ├── Agent-4: Risk Intelligence
    │       Bayesian Beta(2,9) + Agentic AI Risk Layer + 대만해협 시나리오
    ├── Agent-5: Foresight Intelligence
    │       3시나리오 × 3구간 로드맵 + EW-GEO 트리거 시 가중치 재조정
    ├── Agent-6: BizDev Intelligence
    │       Blue Ocean ERRC Grid + Buyer Utility Map + 기회점수
    ├── Agent-7: Synthesis Intelligence
    │       Mermaid2GIF 시각화 + continuation_guard (checkpoint/resume)
    └── Agent-8: IP Intelligence
            Patent White Space Map + FTO 스크리닝 (USPTO/EPO/KIPRIS)

Shared Memory : Mastra Observational Memory OM-v1.0 (16K tokens)
Auto-Improve  : SkillRL Router 강화학습 자동개선
```

---

## Variant 비교

| 항목 | OPT (Master) | KR Variant | GLOBAL Variant |
|------|-------------|-----------|----------------|
| **PE-3** | 96 | 94 | 95 |
| **대상국** | Multi (파라미터) | KR 전용 | KR·TW·JP·US·CN 5개국 |
| **EW 세트** | EW-SEMI/AI/MKT | EW-KR-01/02 + EW-GEO-01 | EW-GLOBAL-01~03 + EW-GEO-01/02 |
| **HBM 특화** | 일반 타임라인 | HBM2E/3/4 병목 레이어 | 5개국 HBM 공급망 연쇄충격 |
| **플레이어 DB** | 글로벌 Tier1/2 | KR 4대(삼성·SK·한미·LX) | 5개국 × 국가별 Tier1 |
| **시나리오** | S1/S2/S3 | GEO-S1~S3 + KR 마일스톤 | World A~D + 블록화 시나리오 |
| **보고서 언어** | 영문 표준 | 한국어(MSIT) + 영문 | KR/EN/JP 3언어 |
| **정책 데이터** | N/A | KOTRA/KITA/MOTIE | IEA/OECD/WTO/각국 상무부 |
| **Notion 연계** | C-33 + T-09 | C-33 + **C-29(PE-SEMI)** + T-09 | C-33 + C-29 + **C-28(PE-AI)** + T-09 |

---

## EW 트리거 전체 맵

| EW ID | 소속 Variant | 트리거 조건 | 자동 응답 Agent |
|-------|------------|------------|----------------|
| EW-MKT-01 | OPT | TAM 추정 오차 ≥30% | Agent-1 출처 교차검증 |
| EW-MKT-02 | OPT | 단일 출처 의존도 ≥60% | Agent-1 대체 출처 3개 탐색 |
| EW-TECH-01 | OPT | TRL≥7 기술 상용화 경로 부재 | Agent-2 투자 재검토 플래그 |
| EW-KR-01 | KR | 한국 수출규제 신규 발동 | Agent-4 + Agent-3 우선 가동 |
| EW-KR-02 | KR | 한국 정부 지원정책 변경 | Agent-1 TAM 재산정 + Agent-6 |
| EW-GEO-01 | KR/GLOBAL | 대만해협 군사 긴장 | Agent-5 S3 0.25→0.40 + Agent-4 |
| EW-GLOBAL-01 | GLOBAL | 미중 신규 기술제재 | Agent-3/4 5개국 영향 병렬 |
| EW-GLOBAL-02 | GLOBAL | OECD 반도체 공급망 경고 발령 | Agent-1 전체 TAM 재산정 |
| EW-GLOBAL-03 | GLOBAL | 일본 소재·장비 수출 규제 강화 | Agent-2 TRL 경로 재분석 |
| EW-GEO-02 | GLOBAL | 중국 희토류·파비라닉 수출 봉쇄 | Agent-4 World-D 시나리오 전환 |

---

## 생태계 연계

| 연계 대상 | 경로 | 유형 | 관련 Variant |
|-----------|------|------|--------------|
| **C-33 PE-STRAT** | Notion | Primary 저장소 | OPT/KR/GLOBAL |
| **C-29 PE-SEMI** | Notion | 반도체 시장데이터 크로스참조 | KR/GLOBAL |
| **C-28 PE-AI** | Notion | AI 인프라 데이터 크로스참조 | GLOBAL |
| **C-27 PE-MIN** | Notion | 광물·소재 공급망 크로스참조 | OPT/GLOBAL |
| **T-09 PE-MASTER** | Notion | 마스터 페이지 참조 링크 | OPT/KR/GLOBAL |
| **KG v4.7+** | Knowledge Graph | 8노드 + 15엣지 자동 추가 예정 | OPT |
| **PE-OPT 자기진화** | Notion/GitHub | 자기진화 시스템 연동 | OPT |

---

## 변경 이력

| 날짜 | 변경 내용 | 커밋 |
|------|-----------|------|
| 2026-05-21 | MA-MoE-8AGENT-v1.0-OPT 신규 등록 (PE-3: 96) | `09e1a765` |
| 2026-05-21 | MA-MoE-8AGENT-v1.0-KR 증식 완료 (PE-3: 94) | `e2c8c44c` |
| 2026-05-21 | MA-MoE-8AGENT-v1.0-GLOBAL 증식 완료 (PE-3: 95) | (현재 커밋) |

---
_Last updated: 2026-05-21 KST_
