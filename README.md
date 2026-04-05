# 🧠 프롬프트 엔지니어링 시스템 — 자동개선·자동증식·자동검증

> **Gilbert Kwak** | 최초 생성: 2026-04-05 | 현재 버전: **v1.1**

[![Version](https://img.shields.io/badge/version-v1.1-blue)](https://github.com/GilbertKwak/prompt-engineering-system/releases)
[![Status](https://img.shields.io/badge/status-active-green)]()
[![Notion](https://img.shields.io/badge/Notion-Hub-black?logo=notion)](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b)

---

## 📌 개요

본 저장소는 **3개 핵심 엔진**으로 구성된 프롬프트 자동화 시스템을 관리합니다.

| 엔진 | ID | 기능 |
|------|-----|------|
| 자동개선 (Auto-Refinement) | PE-1 | 프롬프트 약점 탐지 → 재작성 루프 |
| 자동증식 (Auto-Proliferation) | PE-2 | 단일 프롬프트 → 다목적 변형 버전 생성 |
| 자동검증 (Auto-Validation) | PE-3 | 5차원 품질 채점 → 합격/재처리 판정 |

---

## 🗂️ 저장소 구조

```
prompt-engineering-system/
├── README.md                        ← 본 파일 (Mother 문서)
├── engines/
│   ├── PE-1_auto-refinement/
│   │   ├── README.md                ← 자동개선 엔진 상세
│   │   ├── prompt_template.md       ← 프롬프트 템플릿
│   │   └── examples/
│   ├── PE-2_auto-proliferation/
│   │   ├── README.md                ← 자동증식 엔진 상세
│   │   ├── prompt_template.md
│   │   └── examples/
│   └── PE-3_auto-validation/
│       ├── README.md                ← 자동검증 엔진 상세
│       ├── scoring_rubric.md        ← 5차원 채점 기준표
│       └── examples/
├── workflows/
│   └── 3engine_pipeline.md          ← 통합 파이프라인 설계
├── applied-cases/
│   └── 2026-04-05_upgrade-execution.md  ← 오늘 실행 기록
└── CHANGELOG.md                     ← 버전 이력
```

---

## 🔄 3-Engine 통합 워크플로우

```
[사용자 초안 프롬프트]
        ↓
┌─────────────────────────────┐
│  PE-1: 자동개선 엔진         │
│  - 약점 탐지 → 재작성        │
│  - 반복 루프 (max 3회)       │
└──────────┬──────────────────┘
           ↓
┌─────────────────────────────┐
│  PE-2: 자동증식 엔진         │
│  - 목적별 변형 버전 생성      │
│  - 도메인·난이도·포맷 다변화  │
└──────────┬──────────────────┘
           ↓
┌─────────────────────────────┐
│  PE-3: 자동검증 엔진         │
│  - 5개 차원 품질 채점         │
│  - 합격/재처리 판정           │
└──────────┬──────────────────┘
           ↓
  [최종 검증 완료 프롬프트 라이브러리]
```

---

## 📋 버전 이력

| 버전 | 날짜 | 내용 |
|------|------|------|
| v1.0 | 2026-04-05 | 최초 생성 — 3-Engine 프레임워크 정립 |
| v1.1 | 2026-04-05 | 업그레이드 실행 — 전체 엔진 파일 구조 수립, applied-cases 추가 |

---

## 🔗 연계 저장소

| 저장소 | 목적 |
|--------|------|
| [multi-agent-system-v3-hybrid](https://github.com/GilbertKwak/multi-agent-system-v3-hybrid) | 분석 시스템 v3.0 |
| [master-agent-v4.0b](https://github.com/GilbertKwak/master-agent-v4.0b) | 분석 시스템 v4.0 |
| [global-semiconductor-ai-research](https://github.com/GilbertKwak/global-semiconductor-ai-research) | 반도체 AI 연구 |

---

## 📚 Notion 문서

- **Mother Page (Hub)**: [🧠 프롬프트 엔지니어링 시스템 허브 v1.0](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b)
- **PE-1 자동개선**: Notion Child Page PE-1
- **PE-2 자동증식**: Notion Child Page PE-2
- **PE-3 자동검증**: Notion Child Page PE-3
- **실행 기록**: [PE-4 HBM 적용 완전판](https://www.notion.so/33955ed436f0819f874ce48af92e207f)

---

> 관리자: Gilbert Kwak | 다음 리뷰: 2026-05 (v1.2 — 실적용 사례 확장)
