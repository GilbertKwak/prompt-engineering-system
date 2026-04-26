# 🚀 PE-11 · Master Multi-Agent Prompt System v1.0

> **Prompt-Dev_00_15 시리즈 24개 파일 완전 통합 · 최종 최적화본**

---

## 📌 개요

| 항목 | 내용 |
|------|------|
| **버전** | v11.0 (PerformanceOptimizedMultiAgent) |
| **기반** | Prompt-Dev_00_15_00 ~ Prompt-Dev_00_15_23 (24개 파일, ~550,000자) |
| **작성일** | 2026-04-26 |
| **적용 시스템** | master-agent-v4.0b / multi-agent-system-v3-hybrid |
| **Notion 허브** | [PE-11 페이지](https://www.notion.so/34e55ed436f081fbaa48e9bda5882b2e) |

---

## 🗂️ 디렉토리 구조

```
PE-11-master-multi-agent/
├── README.md                          ← 이 파일 (인덱스·개요)
├── MASTER_PROMPT.md                   ← 최종 통합 마스터 프롬프트 (SSOT)
├── PROMPT_VERSION_HISTORY.md          ← 버전 이력
└── prompts/
    ├── L1_orchestrator/
    │   ├── p01_task_decomposer.md     ← 태스크 분해 오케스트레이터
    │   ├── p02_parallel_executor.md   ← 병렬 실행 제어
    │   └── p03_inception_error.md     ← Inception 에러 감지·복구
    ├── L2_analysis/
    │   ├── p04_domain_expert.md       ← 도메인 전문가 에이전트
    │   ├── p05_rag_agent.md           ← Zvec UltraRAG 검색 에이전트
    │   ├── p06_reasoning_agent.md     ← Bayesian CoT 추론 에이전트
    │   ├── p07_verification_agent.md  ← LOO-CV 검증 에이전트
    │   └── p08_devils_advocate.md     ← Devil's Advocate 교차 검증
    ├── L3_validation/
    │   ├── p09_ralph_stage1_spec.md   ← Ralph Loop Stage 1 (Spec)
    │   ├── p10_ralph_stage2_quality.md← Ralph Loop Stage 2 (Quality)
    │   ├── p11_knowledge_extractor.md ← Zettelkasten 지식 추출
    │   └── p12_conflict_resolver.md   ← 에이전트 간 충돌 해결
    ├── L4_reporting/
    │   ├── p13_report_planner.md      ← 보고서 플래너
    │   ├── p14_section_writer.md      ← 섹션 작성 에이전트
    │   ├── p15_visual_generator.md    ← Mermaid 시각화 생성
    │   └── p16_final_reviewer.md      ← 최종 검토·배포
    └── L5_infra/
        ├── p17_memory_manager.md      ← RLM/memU 메모리 관리
        ├── p18_workflow_optimizer.md  ← 워크플로우 최적화
        └── p19_notifier.md            ← Slack/Email 알림 시스템
```

---

## 🔄 실행 아키텍처

```
[사용자 요청]
      ↓
L1: 오케스트레이터 (Task Decomposer → Parallel Executor → Inception)
      ↓ 병렬 실행 (max 12 동시)
L2: 분석 에이전트 (Domain / RAG / Reasoning / Verification / Devil's Advocate)
      ↓
L3: 검증 에이전트 (Ralph Loop SHIP/REVISE, 지식 추출, 충돌 해결)
      ↓
L4: 보고서 에이전트 (Planner → Writer×5 → Visualizer → Reviewer)
      ↓
[최종 보고서] → GitHub SSOT 동기화 → Notion 업데이트
```

---

## 📊 성능 지표 (v10 → v11)

| 지표 | v10 | v11 | 개선 |
|------|-----|-----|------|
| 실행 시간 | 16.2분 | 12.5분 | **-23%** |
| API 토큰 | 9,000 | 5,500 | **-39%** |
| API 비용 | 기준 | -50% | memU+Zvec |
| 1회 통과율 | 65% | 78% | **+13%p** |
| 정확도 | 98.0% | 98.5% | +0.5%p |

---

## 🔗 연계 저장소

- [master-agent-v4.0b](https://github.com/GilbertKwak/master-agent-v4.0b)
- [multi-agent-system-v3-hybrid](https://github.com/GilbertKwak/multi-agent-system-v3-hybrid)
- [HBM-Salvage-Value-Program](https://github.com/GilbertKwak/HBM-Salvage-Value-Program)
