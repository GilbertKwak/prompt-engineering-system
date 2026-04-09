# 🧠 프롬프트 엔지니어링 시스템 — 자동개선·자동증식·자동검증

> **Gilbert Kwak** | 최초 생성: 2026-04-05 | 현재 버전: **v1.2**

[![Version](https://img.shields.io/badge/version-v1.2-blue)](https://github.com/GilbertKwak/prompt-engineering-system/releases)
[![Status](https://img.shields.io/badge/status-active-green)]()
[![Notion Hub](https://img.shields.io/badge/Notion-PE%20Hub-black?logo=notion)](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b)
[![Notion RCA](https://img.shields.io/badge/Notion-RCA%2FCAPA-orange?logo=notion)](https://www.notion.so/33d55ed436f081bfa2aeccc26f344de5)

---

## 📌 개요

본 저장소는 **3개 핵심 엔지으로 구성된 프롬프트 자동화 시스템**을 관리하며, 시스템 운영 중 도출된 RCA/CAPA 문서를 포함합니다.

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
├── CHANGELOG.md                    ← 버전 이력
├── docs/
│   ├── index.md                 ← 해 형식 문서 허브
│   └── rca-capa/
│       ├── README.md            ← RCA/CAPA 인덱스
│       ├── RCA-001.md           ← 프롬프트 구조 복잡도
│       ├── RCA-002.md           ← 검증 기준 모호성
│       ├── RCA-003.md           ← 필수 고려사항 누락
│       └── RCA-004.md           ← 중복 출력 과다
├── engines/
│   ├── PE-1_auto-refinement/
│   ├── PE-2_auto-proliferation/
│   └── PE-3_auto-validation/
├── workflows/
│   └── 3engine_pipeline.md
└── applied-cases/
    └── 2026-04-05_upgrade-execution.md
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
└──────────┤
           ↓
┌─────────────────────────────┐
│  PE-2: 자동증식 엔진         │
│  - 목적별 변형 버전 생성      │
│  - 도메인·난이도·포맷 다변화  │
└──────────┤
           ↓
┌─────────────────────────────┐
│  PE-3: 자동검증 엔진         │
│  - 5개 차원 품질 채점         │
│  - 합격/재처리 판정           │
└──────────┤
           ↓
  [최종 검증 완료 프롬프트 라이브러리]
```

---

## 🔧 RCA/CAPA 문서

시스템 운영 중 도출된 문제의 근본 원인(RCA)과 시정/예방 조치(CAPA)를 체계적으로 관리합니다.

| ID | 제목 | 근본 원인 키워드 | 개선 | 상태 |
|----|------|---------|------|------|
| [RCA-001](./docs/rca-capa/RCA-001.md) | 프롬프트 구조 복잡도 | XML 파싱 기준 미정의 | 파싱에러 -75%p | ✅ |
| [RCA-002](./docs/rca-capa/RCA-002.md) | 검증 기준 모호성 | 스코어링 스펙 부재 | 편차 -80% | ✅ |
| [RCA-003](./docs/rca-capa/RCA-003.md) | 필수 고려사항 누락 | RISK 에이전트 미정의 | 위험승인 -100% | ✅ |
| [RCA-004](./docs/rca-capa/RCA-004.md) | 중복 출력 과다 | Orchestrator 역할 누락 | 중복 -43%p | ✅ |

➡️ **[docs/rca-capa/ 전체 보기](./docs/rca-capa/README.md)** | **[docs/index.md 전체 허브](./docs/index.md)**

---

## 📈 버전 이력

| 버전 | 날짜 | 내용 |
|------|------|------|
| v1.0 | 2026-04-05 | 최초 생성 — 3-Engine 프레임워크 정립 |
| v1.1 | 2026-04-05 | 업그레이드 실행 — 전체 엔진 파일 구조 수립 |
| v1.2 | 2026-04-09 | docs/ 구조 신설, RCA/CAPA 4건 정식 등록, Notion 양방향 링크 |

---

## 🔗 연계 저장소

| 저장소 | 목적 |
|--------|------|
| [multi-agent-system-v3-hybrid](https://github.com/GilbertKwak/multi-agent-system-v3-hybrid) | 분석 시스템 v3.0 |
| [master-agent-v4.0b](https://github.com/GilbertKwak/master-agent-v4.0b) | 분석 시스템 v4.0 |
| [global-semiconductor-ai-research](https://github.com/GilbertKwak/global-semiconductor-ai-research) | 반도체 AI 연구 |

---

## 📚 Notion 문서

| Notion 페이지 | 타입 | URL |
|--------------|------|-----|
| 프롬프트 엔지니어링 허브 | Mother | [https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b) |
| 🔧 RCA/CAPA 관리 시스템 | Mother | [https://www.notion.so/33d55ed436f081bfa2aeccc26f344de5](https://www.notion.so/33d55ed436f081bfa2aeccc26f344de5) |
| 📋 RCA-001 프롬프트 구조 | Child | [https://www.notion.so/33d55ed436f081c593ede0347d2b581a](https://www.notion.so/33d55ed436f081c593ede0347d2b581a) |
| 📋 RCA-002 검증 기준 | Child | [https://www.notion.so/33d55ed436f081d0a7a1d4a2a8de4a8f](https://www.notion.so/33d55ed436f081d0a7a1d4a2a8de4a8f) |
| 📋 RCA-003 필수 고려사항 | Child | [https://www.notion.so/33d55ed436f0817e83e0f3bc0f168316](https://www.notion.so/33d55ed436f0817e83e0f3bc0f168316) |
| 📋 RCA-004 중복 출력 | Child | [https://www.notion.so/33d55ed436f08195bd49cdd19f062644](https://www.notion.so/33d55ed436f08195bd49cdd19f062644) |

---

> 관리자: Gilbert Kwak | 다음 리뷰: 2026-05 (v1.3 — 실적용 사례 확장)
