# 📖 Master Documentation Index

> **관리자**: Gilbert Kwak | **최종 업데이트**: 2026-04-09 | **버전**: v1.3

[![Notion PE Hub](https://img.shields.io/badge/Notion-PE%20Hub-black?logo=notion)](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b)
[![Notion RCA](https://img.shields.io/badge/Notion-RCA%2FCAPA-orange?logo=notion)](https://www.notion.so/33d55ed436f081bfa2aeccc26f344de5)

---

## 🗺️ 전체 레포지토리 구조

```
prompt-engineering-system/
├── README.md                        ← 진입점 (Mother)
├── CHANGELOG.md                    ← 버전 이력
├── docs/
│   ├── index.md                 ← 현재 파일 — Master Index
│   ├── agent1/                  ← PE-1 자동개선 엔진
│   │   └── README.md
│   ├── agent2/                  ← PE-2 자동증식 엔진
│   │   └── README.md
│   ├── agent3/                  ← PE-3 자동검증 엔진
│   │   └── README.md
│   ├── agent4/                  ← PE-4 실적용 케이스 매니저
│   │   └── README.md
│   ├── agent5/                  ← PE-5 마스터 오케스트레이터
│   │   └── README.md
│   ├── support/                 ← 지원 모듈 (프롬프트 템플릿, 루브릭 등)
│   │   └── README.md
│   ├── new/                     ← 신규 기능 파이프라인
│   │   └── README.md
│   └── rca-capa/                ← 근본원인 분석 & 시정
│       ├── README.md
│       ├── RCA-001.md
│       ├── RCA-002.md
│       ├── RCA-003.md
│       └── RCA-004.md
├── dashboard/
│   ├── README.md                ← 대시보드 안내
│   └── metrics.md               ← KPI 추적 시트
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

## 🤖 에이전트 문서 (docs/agent1~5)

| 디렉토리 | 에이전트 ID | 역할 | 상태 |
|----------|---------|------|------|
| [docs/agent1/](./agent1/README.md) | PE-1 | 자동개선 (Auto-Refinement) | ✅ 운영 |
| [docs/agent2/](./agent2/README.md) | PE-2 | 자동증식 (Auto-Proliferation) | ✅ 운영 |
| [docs/agent3/](./agent3/README.md) | PE-3 | 자동검증 (Auto-Validation) | ✅ 운영 |
| [docs/agent4/](./agent4/README.md) | PE-4 | 실적용 케이스 매니저 | 🟡 개발 중 |
| [docs/agent5/](./agent5/README.md) | PE-5 | 마스터 오케스트레이터 | 🟡 개발 중 |

---

## 🛠️ 지원 및 신규 문서

| 디렉토리 | 내용 | 상태 |
|----------|------|------|
| [docs/support/](./support/README.md) | 프롬프트 템플릿, 루브릭, 공통 모듈 | 🟡 파일 업로드 예정 |
| [docs/new/](./new/README.md) | 신규 기능 아이디어 파이프라인 | 🟡 수쉇 중 |

---

## 🔧 RCA/CAPA 문서 (docs/rca-capa)

| ID | 제목 | 근본 원인 | 해결 버전 | Notion |
|----|------|---------|---------|--------|
| [RCA-001](./rca-capa/RCA-001.md) | 프롬프트 구조 복잡도 | XML 파싱 기준 미정의 | v3.0 | [Notion](https://www.notion.so/33d55ed436f081c593ede0347d2b581a) |
| [RCA-002](./rca-capa/RCA-002.md) | 검증 기준 모호성 | 스코어링 스펙 부재 | v3.1 | [Notion](https://www.notion.so/33d55ed436f081d0a7a1d4a2a8de4a8f) |
| [RCA-003](./rca-capa/RCA-003.md) | 필수 고려사항 누락 | RISK 에이전트 미정의 | v3.1 | [Notion](https://www.notion.so/33d55ed436f0817e83e0f3bc0f168316) |
| [RCA-004](./rca-capa/RCA-004.md) | 중복 출력 과다 | Orchestrator 역할 누락 | v3.1 | [Notion](https://www.notion.so/33d55ed436f08195bd49cdd19f062644) |

➡️ **[docs/rca-capa/ 전체 보기](./rca-capa/README.md)**

---

## 📊 대시보드 (dashboard/)

| 파일 | 내용 |
|------|------|
| [dashboard/README.md](../dashboard/README.md) | 대시보드 안내 및 활용 가이드 |
| [dashboard/metrics.md](../dashboard/metrics.md) | KPI 추적 시트 (실시간 지표 추적) |

---

## 🔗 양방향 링크 맵

### Notion

| 페이지 | 타입 | URL |
|------|------|-----|
| PE 허브 | Mother | [https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b) |
| RCA/CAPA 관리 | Mother | [https://www.notion.so/33d55ed436f081bfa2aeccc26f344de5](https://www.notion.so/33d55ed436f081bfa2aeccc26f344de5) |
| RCA-001 | Child | [https://www.notion.so/33d55ed436f081c593ede0347d2b581a](https://www.notion.so/33d55ed436f081c593ede0347d2b581a) |
| RCA-002 | Child | [https://www.notion.so/33d55ed436f081d0a7a1d4a2a8de4a8f](https://www.notion.so/33d55ed436f081d0a7a1d4a2a8de4a8f) |
| RCA-003 | Child | [https://www.notion.so/33d55ed436f0817e83e0f3bc0f168316](https://www.notion.so/33d55ed436f0817e83e0f3bc0f168316) |
| RCA-004 | Child | [https://www.notion.so/33d55ed436f08195bd49cdd19f062644](https://www.notion.so/33d55ed436f08195bd49cdd19f062644) |

### GitHub 핵심 경로

| 경로 | 렬더링 URL |
|------|-----|
| `docs/agent1~5/` | [tree/main/docs](https://github.com/GilbertKwak/prompt-engineering-system/tree/main/docs) |
| `docs/rca-capa/` | [tree/main/docs/rca-capa](https://github.com/GilbertKwak/prompt-engineering-system/tree/main/docs/rca-capa) |
| `dashboard/` | [tree/main/dashboard](https://github.com/GilbertKwak/prompt-engineering-system/tree/main/dashboard) |

---

> 최종 업데이트: 2026-04-09 | 다음 리뷰: 2026-05
