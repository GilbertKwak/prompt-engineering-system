# 💾 SPU · Storage Processor Unit 전략 문서 + Auto-Validation v3.0

> **Status**: ✅ Active | **Created**: 2026-04-27 | **Manager**: GilbertKwak
> **Notion SSOT**: [SPU Notion Page](https://www.notion.so/34e55ed436f08122b7a3f2c632e69a12)
> **Parent**: AstraChips 통합 전략 허브 · AI 인프라스트럭처 디렉토리

---

## 개요

SPU(Storage Processor Unit)는 AI inference data path 전용 가속기로,
Storage와 GPU 사이의 데이터 흐름을 지능적으로 처리하는 독립 실행 계층입니다.

```
[NVMe SSD] -> [SPU: 압축해제 / 필터링 / 재정렬] -> [GPU HBM]
                     ^
           이 계층이 존재하지 않았다
           SPU = 신규 카테고리 창조
```

## 파일 구조

```
SPU/
├── README.md
├── SPU_001_analysis_engine.xml            # SPU_001 분석 엔진 프롬픃트
├── auto_validation_layer.py               # AUTO_VALIDATION_LAYER + Red Team
├── version_roadmap.md                     # v1 / v2 / v3 로드맵
└── e0n_integration.md                     # E-0N 연동 8주기
```

## 버전 로드맵

| 버전 | 코드명 | 포지셔닝 | 타깃 |
|------|-------|---------|------|
| v1 MVP | Minimal Correct SPU | AI inference data path 가속 | Hyperscaler |
| v2 | Compute-near-Data | Vector pre-filter + RAG | LLM SaaS |
| v3 | AI Data Plane | Storage↔Memory 경계 븄괴 | 국가 인프라 |

---
*Last updated: 2026-04-27 | Version: v3.0 Auto-Validation Integrated*
