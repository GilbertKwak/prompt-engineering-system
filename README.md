# 🧠 프롬프트 엔진니어링 시스템 — 자동개선·자동증식·자동검증

> **Gilbert Kwak** | 최초 생성: 2026-04-05 | 현재 버전: **v1.6**

[![Version](https://img.shields.io/badge/version-v1.6-blue)](https://github.com/GilbertKwak/prompt-engineering-system/releases)
[![Status](https://img.shields.io/badge/status-active-green)]()
[![Notion Hub](https://img.shields.io/badge/Notion-PE%20Hub-black?logo=notion)](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b)
[![Notion RCA](https://img.shields.io/badge/Notion-RCA%2FCAPA-orange?logo=notion)](https://www.notion.so/33d55ed436f081bfa2aeccc26f344de5)

---

## 📌 개요

본 저장소는 **5엔진 프롬프트 자동화 시스템**을 관리하며, 재현 가능한 연구 프로젝트 구조를 따릅니다.

| 엔진 | ID | 기능 | 업그레이드 (v1.5) | 문서 |
|------|-----|------|------|------|
| 자동개선 | PE-1 | 프롬프트 약점 탐지 → 재작성 | 약점탐지→재작성 루프 고도화 (max 3회) | [docs/agent1/](./docs/agent1/README.md) |
| 자동증식 | PE-2 | 다목적 변형 버전 생성 | 도메인·난이도·포맷 3축 증식 | [docs/agent2/](./docs/agent2/README.md) |
| 자동검증 | PE-3 | 5차원 품질 채점 | 5차원 스코어링 + 합격/재처리 판정 루프 | [docs/agent3/](./docs/agent3/README.md) |
| 케이스 매니저 | PE-4 | 실적용 기록 | — | [docs/agent4/](./docs/agent4/README.md) |
| 마스터 오케스트레이터 | PE-5 | 엔진 통합 조율 | — | [docs/agent5/](./docs/agent5/README.md) |

---

## 🗂️ 레포지토리 구조

```
prompt-engineering-system/
├── README.md                        ← 진입점 (Mother)
├── CHANGELOG.md
├── knowledge_graph.json             ← KG 빌드 산출물 (auto_validate.py 입력)
├── docs/
│   ├── index.md                 ← Master Index (접근점)
│   ├── agent1/README.md         ← PE-1 자동개선
│   ├── agent2/README.md         ← PE-2 자동증식
│   ├── agent3/README.md         ← PE-3 자동검증
│   ├── agent4/README.md         ← PE-4 케이스 매니저
│   ├── agent5/README.md         ← PE-5 오케스트레이터
│   ├── support/README.md        ← 지원 모듈
│   ├── new/README.md            ← 신규 기능 파이프라인
│   └── rca-capa/                ← 근본원인 분석
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
├── scripts/
│   └── build_knowledge_graph.py ← KG 빌드 스크립트 (방법 B 커맨드 지원)
├── workflows/
│   └── 3engine_pipeline.md
└── applied-cases/
    ├── 2026-04-05_upgrade-execution.md
    ├── 2026-04-10_3engine-upgrade-v1.4.md
    └── 2026-04-10_3engine-upgrade-v1.5.md
```

---

## 🔧 KG 빌드 & 검증 실행

> `knowledge_graph.json`이 없으면 `auto_validate.py`의 KG 체크가 **SKIP** 처리됩니다.  
> 완전한 검증을 위해 아래 순서로 실행하세요.

### Step 1 — Knowledge Graph 생성

```bash
# 방법 B: 원본 파일명 그대로 사용 (권장 — alias 불필요)
python scripts/build_knowledge_graph.py \
  --input docs engines applied-cases workflows dashboard \
  --full --sha \
  --output knowledge_graph.json
```

| 옵션 | 설명 |
|------|------|
| `--input` | 스캔할 디렉토리 목록 (5개 전체) |
| `--full` | `--sha` + `--version-extract` 동시 활성화 |
| `--sha` | 각 파일의 git blob SHA 자동 추출 |
| `--output` | 출력 경로 (기본값: `knowledge_graph.json`) |

### Step 2 — 전체 검증 실행

```bash
# KG 생성 후 완전 검증 (RCA-001~004 포함)
python auto_validate.py --full \
  --report-dir reports/ \
  --kg knowledge_graph.json

# 실패 항목만 필터링
python auto_validate.py --filter FAIL --export validation_report.csv
```

### KG SKIP 조건

`knowledge_graph.json`이 없을 경우 건너뛰어지는 검증:
- 파일 간 의존성 그래프 순환 참조 탐지
- 고립(orphan) 문서 탐지
- 태그 클러스터 일관성 검증

---

## 🔧 RCA/CAPA 문서

| ID | 제목 | 키 | 개선 | 상태 |
|----|------|-----|------|------|
| [RCA-001](./docs/rca-capa/RCA-001.md) | 프롬프트 구조 복잡도 | XML 기준 미정의 | 파싱에러 -75%p | ✅ |
| [RCA-002](./docs/rca-capa/RCA-002.md) | 검증 기준 모호성 | 스코어링 스펙 부재 | 편차 -80% | ✅ |
| [RCA-003](./docs/rca-capa/RCA-003.md) | 필수 고려사항 누락 | RISK 에이전트 미정의 | 위험승인 -100% | ✅ |
| [RCA-004](./docs/rca-capa/RCA-004.md) | 중복 출력 과다 | Orchestrator 누락 | 중복 -43%p | ✅ |

➡️ **[docs/rca-capa/ 전체](./docs/rca-capa/README.md)** | **[docs/index.md Master Index](./docs/index.md)** | **[dashboard/metrics.md KPI](./dashboard/metrics.md)**

---

## 📈 버전 이력

| 버전 | 날짜 | 내용 |
|------|------|------|
| v1.0 | 2026-04-05 | 3-Engine 프레임워크 |
| v1.1 | 2026-04-05 | 엔진 파일 구조 수립 |
| v1.2 | 2026-04-09 | docs/rca-capa + Notion 양방향 링크 |
| v1.3 | 2026-04-09 | 재현 가능 연구 구조 전체 수립 (agent1~5, support, new, dashboard) |
| v1.4 | 2026-04-10 | 3-Engine 업그레이드 적용 (CoT, 크로스오버, 신뢰도 가중치) |
| v1.5 | 2026-04-10 | 자동개선·자동증식·자동검증 방식 적용 업그레이드 실행 |
| **v1.6** | **2026-04-18** | **KG 빌드 스크립트 방법 B 공식화, README 구조 갱신** |

---

## 📚 Notion 문서

| Notion 페이지 | 타입 | URL |
|--------------|------|-----|
| PE 허브 | Mother | [https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b) |
| RCA/CAPA 관리 | Mother | [https://www.notion.so/33d55ed436f081bfa2aeccc26f344de5](https://www.notion.so/33d55ed436f081bfa2aeccc26f344de5) |
| RCA-001 | Child | [https://www.notion.so/33d55ed436f081c593ede0347d2b581a](https://www.notion.so/33d55ed436f081c593ede0347d2b581a) |
| RCA-002 | Child | [https://www.notion.so/33d55ed436f081d0a7a1d4a2a8de4a8f](https://www.notion.so/33d55ed436f081d0a7a1d4a2a8de4a8f) |
| RCA-003 | Child | [https://www.notion.so/33d55ed436f0817e83e0f3bc0f168316](https://www.notion.so/33d55ed436f0817e83e0f3bc0f168316) |
| RCA-004 | Child | [https://www.notion.so/33d55ed436f08195bd49cdd19f062644](https://www.notion.so/33d55ed436f08195bd49cdd19f062644) |

---

## 🔗 연계 저장소

| 저장소 | 목적 |
|--------|------|
| [multi-agent-system-v3-hybrid](https://github.com/GilbertKwak/multi-agent-system-v3-hybrid) | 분석 시스템 v3.0 |
| [master-agent-v4.0b](https://github.com/GilbertKwak/master-agent-v4.0b) | 분석 시스템 v4.0 |
| [global-semiconductor-ai-research](https://github.com/GilbertKwak/global-semiconductor-ai-research) | 반도체 AI 연구 |

---

> 관리자: Gilbert Kwak | 다음 리뷰: 2026-05 (v1.7 — support/ 세부 파일 완성)
