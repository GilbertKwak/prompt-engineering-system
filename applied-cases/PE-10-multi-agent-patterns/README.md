# PE-10 · 멀티에이전트 패턴 프롬프트 시스템 v1.0

> **SSOT 위치**: `prompt-engineering-system/applied-cases/PE-10-multi-agent-patterns/`  
> **생성일**: 2026-04-26  
> **버전**: v1.0  
> **상태**: ✅ Active  
> **연계 시스템**: master-agent-v4.0b / multi-agent-system-v3-hybrid

---

## 📌 개요

본 디렉토리는 **4개 멀티에이전트 디자인 패턴** (Inception / Brainstorming / Ralph Loop / Recursive Delegation)에서 실제 적용된 **9개 핵심 프롬프트**의 SSOT(Single Source of Truth)입니다.

---

## 🗂️ 프롬프트 인덱스

| ID | 파일 | 패턴 | 유형 | Temperature | 버전 |
|---|---|---|---|---|---|
| P-01 | `prompts/p01_inception_error_detect.md` | Inception | 에러 감지 | 0.0 | v1.0 |
| P-02 | `prompts/p02_inception_recovery_inject.md` | Inception | 복구 주입 | — | v1.0 |
| P-03 | `prompts/p03_brainstorming_requirements.md` | Brainstorming | 요구사항 명확화 | 0.3 | v1.0 |
| P-04 | `prompts/p04_brainstorming_plan.md` | Brainstorming | 계획 생성 | 0.3 | v1.0 |
| P-05 | `prompts/p05_ralph_stage1_spec.md` | Ralph Loop | Spec 검증 | 0.0 | v1.0 |
| P-06 | `prompts/p06_ralph_stage2_quality.md` | Ralph Loop | Quality 검증 | 0.0 | v1.0 |
| P-07 | `prompts/p07_recursive_decompose.md` | Recursive | 태스크 분해 | 0.0 | v1.0 |
| P-08 | `prompts/p08_recursive_leaf_execute.md` | Recursive | Leaf 실행 | 0.3 | v1.0 |
| P-09 | `prompts/p09_recursive_synthesize.md` | Recursive | 결과 통합 | 0.3 | v1.0 |

---

## 🔄 실행 파이프라인

```
[사용자 요청]
     │
     ▼
P-03 요구사항 명확화 ──→ P-04 실행 계획 생성
                                │
                                ▼
                P-07 태스크 분해 (max_depth=2)
                ├── P-08 Leaf 실행 ×N (병렬)
                └── P-09 결과 통합 ×depth
                                │
             ┌──────── 에러 감지 루프 ────────┐
             │  P-01 에러 감지               │
             │  P-02 복구 주입 → 재실행      │
             └──────────────────────────────┘
                                │
                P-05 Spec Compliance 검증
                        │ FAIL → 재작업
                       PASS
                        │
                P-06 Quality 검증 (max 3회)
                        │ ITERATE → 재작업
                       SHIP
                        │
                [최종 산출물]
```

---

## 📊 버전 이력

| 버전 | 날짜 | 변경 내용 |
|---|---|---|
| **v1.0** | **2026-04-26** | **최초 생성 — 4개 패턴 9개 프롬프트 SSOT 수립** |

---

## 🔗 연계 링크

- **Notion PE Hub**: https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b
- **GitHub**: https://github.com/GilbertKwak/prompt-engineering-system
- **master-agent-v4.0b**: https://github.com/GilbertKwak/master-agent-v4.0b
- **multi-agent-system-v3-hybrid**: https://github.com/GilbertKwak/multi-agent-system-v3-hybrid
