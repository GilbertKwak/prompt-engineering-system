# FU-PROMPT-01 · 보고서 분할 생성 시스템 v3.0

> **Status**: CURRENT — v3.0 | 2026-04-27  
> **Notion**: [FU-PROMPT-01 보고서 분할 생성 시스템 v3.0](https://www.notion.so/34f55ed436f081198135d78ca76d495f)  
> **연계**: [FU Series Master Hub](https://www.notion.so/33b55ed436f081d8b430eebc3b31fec2) · [PE Hub v2.0](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b)

## 개요

FU Series 보고서 작성을 **규모별(TIER) 3단계로 분리**하여 토큰 효율과 품질을 동시에 최적화하는 분할 생성 시스템.

## v3.0 핵심 변경사항

| 항목 | 변경 내용 |
|------|-----------|
| 역할 중복 제거 | GLOBAL_ROLE 1회 선언 → 토큰 50% 절감 |
| 품질 가드 통합 | GLOBAL_QUALITY_BLOCK 단일화 |
| 세션 복구 표준화 | 3-TIER 공통 SESSION_RECOVERY 블록 |
| 규모 분리 | TIER-1(1~4섹션) / TIER-2(5~9) / TIER-3(10+) |

## 디렉토리 구조

```
FU-PROMPT-01/
├── README.md                    # 본 파일
├── prompts/
│   ├── tier1_small_report.md    # TIER-1 프롬프트 (1~4섹션)
│   ├── tier2_medium_report.md   # TIER-2 프롬프트 (5~9섹션)
│   └── tier3_large_report.md   # TIER-3 프롬프트 (10+섹션)
└── templates/
    └── chunk_writing_template_v3.md  # Chunk Writing 템플릿
```

## TIER 선택 기준

| 기준 | TIER-1 | TIER-2 | TIER-3 |
|------|--------|--------|--------|
| 섹션 수 | 1~4 | 5~9 | 10+ |
| 토큰 예상 | ~8K | ~15K | 25K+ |
| QA 레벨 | STANDARD | ENHANCED | STRICT |
| 적합 보고서 | FU-001~005 | FU-006~008 | FU-008C/D+ |

## 버전 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| v3.0 | 2026-04-27 | 최초 생성 — TIER-1/2/3 분리, 역할 중복 제거, 품질 가드 통합, 세션 복구 표준화 |
