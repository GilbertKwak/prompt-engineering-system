# 📖 Master Documentation Index

> **관리자**: Gilbert Kwak | **최종 업데이트**: 2026-04-09 | **버전**: v1.4

[![Notion PE Hub](https://img.shields.io/badge/Notion-PE%20Hub-black?logo=notion)](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b)
[![Notion RCA](https://img.shields.io/badge/Notion-RCA%2FCAPA-orange?logo=notion)](https://www.notion.so/33d55ed436f081bfa2aeccc26f344de5)
[![RCA Closed](https://img.shields.io/badge/RCA-4%20Closed-brightgreen)](#-rcacapa-문서-docsrca-capa)
[![Version](https://img.shields.io/badge/System-v3.1-blue)](#-버전-이력)

---

## ⚡ Quick Navigation

| 목적 | 바로가기 |
|------|----------|
| 에이전트 설계 문서 | [docs/agent1~5 →](#-에이전트-문서-docsagent15) |
| 문제 원인 분석 | [docs/rca-capa →](#-rcacapa-문서-docsrca-capa) |
| 신규 기능 아이디어 | [docs/new →](./new/README.md) |
| 공통 템플릿·루브릭 | [docs/support →](./support/README.md) |
| KPI 지표 추적 | [dashboard/ →](../dashboard/README.md) |
| 전체 버전 이력 | [CHANGELOG →](../CHANGELOG.md) |

---

## 🗺️ 전체 레포지토리 구조

```
prompt-engineering-system/
├── README.md                        ← 진입점 (Mother)
├── CHANGELOG.md                     ← 버전 이력
│
├── docs/                            ← 📚 모든 설계·운영 문서
│   ├── index.md                     ← ★ 현재 파일 — Master Index v1.4
│   │
│   ├── agent1/README.md             ← PE-1 자동개선 엔진
│   ├── agent2/README.md             ← PE-2 자동증식 엔진
│   ├── agent3/README.md             ← PE-3 자동검증 엔진
│   ├── agent4/README.md             ← PE-4 실적용 케이스 매니저
│   ├── agent5/README.md             ← PE-5 마스터 오케스트레이터
│   │
│   ├── support/README.md            ← 공통 템플릿·루브릭·모듈
│   ├── new/README.md                ← 신규 기능 파이프라인
│   │
│   └── rca-capa/                    ← 🔧 근본원인 분석 & 시정
│       ├── README.md                ← RCA 허브 (등록부·워크플로우)
│       ├── RCA-001.md               ← 프롬프트 구조 복잡도
│       ├── RCA-002.md               ← 검증 기준 모호성
│       ├── RCA-003.md               ← 필수 고려사항 누락
│       └── RCA-004.md               ← 중복 출력 과다
│
├── dashboard/
│   ├── README.md                    ← 대시보드 안내
│   └── metrics.md                   ← KPI 추적 시트
│
├── engines/
│   ├── PE-1_auto-refinement/
│   ├── PE-2_auto-proliferation/
│   └── PE-3_auto-validation/
│
├── workflows/
│   └── 3engine_pipeline.md
│
└── applied-cases/
    └── 2026-04-05_upgrade-execution.md
```

---

## 🤖 에이전트 문서 (docs/agent1~5)

| 디렉토리 | ID | 역할 | 책임자 | 상태 |
|----------|----|------|--------|------|
| [docs/agent1/](./agent1/README.md) | PE-1 | 자동개선 (Auto-Refinement) | Gilbert | ✅ 운영 |
| [docs/agent2/](./agent2/README.md) | PE-2 | 자동증식 (Auto-Proliferation) | Gilbert | ✅ 운영 |
| [docs/agent3/](./agent3/README.md) | PE-3 | 자동검증 (Auto-Validation) | Gilbert | ✅ 운영 |
| [docs/agent4/](./agent4/README.md) | PE-4 | 실적용 케이스 매니저 | Gilbert | 🟡 개발 중 |
| [docs/agent5/](./agent5/README.md) | PE-5 | 마스터 오케스트레이터 | Gilbert | 🟡 개발 중 |

> 각 README는 에이전트 역할 카드 표준 포맷을 따릅니다 (목적·입력·출력·의존성·버전 이력).

---

## 🛠️ 지원 및 신규 문서

| 디렉토리 | 내용 | 파일 수 | 상태 |
|----------|------|---------|------|
| [docs/support/](./support/README.md) | 프롬프트 템플릿, 루브릭, 공통 모듈 | 1+ | 🟡 확장 중 |
| [docs/new/](./new/README.md) | 신규 기능 아이디어 파이프라인 | 1+ | 🟡 수집 중 |

---

## 🔧 RCA/CAPA 문서 (docs/rca-capa)

| ID | 제목 | 근본 원인 요약 | 해결 버전 | 상태 | Notion |
|----|------|--------------|---------|------|--------|
| [RCA-001](./rca-capa/RCA-001.md) | 프롬프트 구조 복잡도 | XML 파싱 기준 미정의 | v3.0 | ✅ Closed | [링크](https://www.notion.so/33d55ed436f081c593ede0347d2b581a) |
| [RCA-002](./rca-capa/RCA-002.md) | 검증 기준 모호성 | 스코어링 스펙 부재 | v3.1 | ✅ Closed | [링크](https://www.notion.so/33d55ed436f081d0a7a1d4a2a8de4a8f) |
| [RCA-003](./rca-capa/RCA-003.md) | 필수 고려사항 누락 | RISK 에이전트 미정의 | v3.1 | ✅ Closed | [링크](https://www.notion.so/33d55ed436f0817e83e0f3bc0f168316) |
| [RCA-004](./rca-capa/RCA-004.md) | 중복 출력 과다 | Orchestrator 역할 누락 | v3.1 | ✅ Closed | [링크](https://www.notion.so/33d55ed436f08195bd49cdd19f062644) |

➡️ **[docs/rca-capa/ RCA 허브 전체 보기 →](./rca-capa/README.md)**

---

## 📊 대시보드 (dashboard/)

| 파일 | 내용 | 비고 |
|------|------|------|
| [dashboard/README.md](../dashboard/README.md) | 대시보드 안내 및 활용 가이드 | |
| [dashboard/metrics.md](../dashboard/metrics.md) | KPI 추적 시트 (실시간 지표 추적) | 월 1회 업데이트 |

---

## 📁 파일 명명 규칙 (Naming Convention)

재현 가능한 연구 구조를 위해 아래 규칙을 따릅니다.

| 파일 유형 | 패턴 | 예시 |
|-----------|------|------|
| RCA 파일 | `RCA-NNN.md` (3자리 번호) | `RCA-005.md` |
| Applied Case | `YYYY-MM-DD_케이스명.md` | `2026-04-09_pe6-upgrade.md` |
| 에이전트 버전 스냅샷 | `PE-N_vX.Y.md` | `PE-1_v3.1.md` |
| 워크플로우 | `workflow_이름.md` | `workflow_3engine.md` |

> **규칙**: 소문자·하이픈 사용, 공백 금지, 날짜는 ISO 8601 (YYYY-MM-DD)

---

## 🔗 양방향 링크 맵 (Notion ↔ GitHub)

### Notion 페이지

| 페이지 | 타입 | URL |
|--------|------|-----|
| PE 허브 | Mother | [https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b) |
| RCA/CAPA 관리 | Mother | [https://www.notion.so/33d55ed436f081bfa2aeccc26f344de5](https://www.notion.so/33d55ed436f081bfa2aeccc26f344de5) |
| RCA-001 | Child | [https://www.notion.so/33d55ed436f081c593ede0347d2b581a](https://www.notion.so/33d55ed436f081c593ede0347d2b581a) |
| RCA-002 | Child | [https://www.notion.so/33d55ed436f081d0a7a1d4a2a8de4a8f](https://www.notion.so/33d55ed436f081d0a7a1d4a2a8de4a8f) |
| RCA-003 | Child | [https://www.notion.so/33d55ed436f0817e83e0f3bc0f168316](https://www.notion.so/33d55ed436f0817e83e0f3bc0f168316) |
| RCA-004 | Child | [https://www.notion.so/33d55ed436f08195bd49cdd19f062644](https://www.notion.so/33d55ed436f08195bd49cdd19f062644) |

### GitHub 핵심 경로

| 경로 | GitHub URL |
|------|------------|
| `docs/index.md` (★ 현재) | [blob/main/docs/index.md](https://github.com/GilbertKwak/prompt-engineering-system/blob/main/docs/index.md) |
| `docs/agent1~5/` | [tree/main/docs](https://github.com/GilbertKwak/prompt-engineering-system/tree/main/docs) |
| `docs/rca-capa/` | [tree/main/docs/rca-capa](https://github.com/GilbertKwak/prompt-engineering-system/tree/main/docs/rca-capa) |
| `dashboard/` | [tree/main/dashboard](https://github.com/GilbertKwak/prompt-engineering-system/tree/main/dashboard) |

---

## 📅 버전 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| v1.4 | 2026-04-09 | 재현 가능 연구 구조 기반 인덱스 강화: Quick Nav, 파일 명명 규칙, RCA 상태 컬럼 추가 |
| v1.3 | 2026-04-09 | RCA/CAPA 섹션 신설, 양방향 링크 맵 추가 |
| v1.2 | 2026-04-07 | 전체 레포지토리 구조 트리 추가 |
| v1.1 | 2026-04-06 | 에이전트 문서 테이블 추가 |
| v1.0 | 2026-04-05 | 최초 생성 |

---

> 최종 업데이트: 2026-04-09 | 다음 리뷰: 2026-05 | 관리자: Gilbert Kwak
