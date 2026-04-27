# 🧠 프롬프트 엔지니어링 시스템 — 자동개선·자동증식·자동검증

> **Gilbert Kwak** | 최초 생성: 2026-04-05 | 현재 버전: **v1.7** | 최종 업데이트: **2026-04-27**

[![Version](https://img.shields.io/badge/version-v1.7-blue)](https://github.com/GilbertKwak/prompt-engineering-system/releases)
[![Status](https://img.shields.io/badge/status-active-green)]()
[![Notion Hub](https://img.shields.io/badge/Notion-PE%20Hub%20v2.0-black?logo=notion)](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b)
[![Notion RCA](https://img.shields.io/badge/Notion-RCA%2FCAPA-orange?logo=notion)](https://www.notion.so/33d55ed436f081bfa2aeccc26f344de5)
[![PE-7](https://img.shields.io/badge/Notion-PE--7%20v2.7-purple?logo=notion)](https://www.notion.so/34955ed436f081149dd6de25dba027d7)
[![SSOT](https://img.shields.io/badge/SSOT-Workspace%20Hub-gray?logo=notion)](https://www.notion.so/f392046f06ff491698ca249849f03a40)

---

## 📌 개요

본 저장소는 **5엔진 프롬프트 자동화 시스템**을 관리하며, 재현 가능한 연구 프로젝트 구조를 따릅니다.
PE-7 AI 자동화 설계·구현 엔진(v2.7)과 연계되어 **E-0N 오류 예측·자동 수정** 파이프라인이 통합 운영됩니다.

| 엔진 | ID | 기능 | 버전 | 문서 |
|------|----|------|------|------|
| 자동개선 | PE-1 | 프롬프트 약점 탐지 → 재작성 루프 (max 3회) | v2.0 | [docs/agent1/](./docs/agent1/README.md) |
| 자동증식 | PE-2 | 도메인·난이도·포맷 3축 증식 | v2.0 | [docs/agent2/](./docs/agent2/README.md) |
| 자동검증 | PE-3 | 5차원 품질 채점 + 합격/재처리 판정 | v2.0 | [docs/agent3/](./docs/agent3/README.md) |
| 케이스 매니저 | PE-4 | 실적용 기록 | v1.0 | [docs/agent4/](./docs/agent4/README.md) |
| 마스터 오케스트레이터 | PE-5 | 엔진 통합 조율 | v1.0 | [docs/agent5/](./docs/agent5/README.md) |
| AI 자동화 설계 | **PE-7** | AI 자동화 아키텍트 + E-0N 오류 예측 | **v2.7** | [engines/PE-7_ai-automation-design/](./engines/PE-7_ai-automation-design/) |

---

## 📂 P-00~P-06 마스터 프롬프트 인덱스

| ID | 파일 | 기능 | 상태 |
|----|------|------|------|
| **P-00** | [prompts/P-00_master-orchestrator.md](./prompts/P-00_master-orchestrator.md) | 세션 진입점 — 전체 파이프라인 오케스트레이션 | 🟢 Active |
| **P-01** | [prompts/P-01_ssot-sync.md](./prompts/P-01_ssot-sync.md) | Notion ↔ GitHub SSOT 동기화 | 🟢 Active |
| **P-02** | [prompts/P-02_error-classifier.md](./prompts/P-02_error-classifier.md) | E-0N 오류 자동 분류 및 수정 | 🟢 Active |
| **P-03** | [prompts/P-03_auto-refinement.md](./prompts/P-03_auto-refinement.md) | PE-1 자동개선 실행 프롬프트 | 🟢 Active |
| **P-04** | [prompts/P-04_auto-proliferation.md](./prompts/P-04_auto-proliferation.md) | PE-2 자동증식 실행 프롬프트 | 🟢 Active |
| **P-05** | [prompts/P-05_auto-validation.md](./prompts/P-05_auto-validation.md) | PE-3 자동검증 실행 프롬프트 | 🟢 Active |
| **P-06** | [prompts/P-06_report-generator.md](./prompts/P-06_report-generator.md) | 보고서 자동 생성 (DOCX/Notion) | 🟢 Active |

---

## 🗂️ 레포지토리 구조

```
prompt-engineering-system/
├── README.md                        ← 진입점 (Mother) [v1.7]
├── CHANGELOG.md
├── P1_EXECUTION_MANIFEST.md
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
│       ├── RCA-001.md ~ RCA-004.md
├── engines/
│   ├── PE-1_auto-refinement/
│   ├── PE-2_auto-proliferation/
│   ├── PE-3_auto-validation/
│   └── PE-7_ai-automation-design/  ← PE-7 v2.7 [NEW]
├── prompts/
│   ├── P-00_master-orchestrator.md  ← [NEW v1.7]
│   ├── P-01_ssot-sync.md            ← [NEW v1.7]
│   ├── P-02_error-classifier.md     ← [NEW v1.7]
│   ├── P-03_auto-refinement.md      ← [NEW v1.7]
│   ├── P-04_auto-proliferation.md   ← [NEW v1.7]
│   ├── P-05_auto-validation.md      ← [NEW v1.7]
│   ├── P-06_report-generator.md     ← [NEW v1.7]
│   └── info-structuring/
├── scripts/
│   ├── build_knowledge_graph.py
│   ├── ssot_sync.py
│   └── error_classifier.py
├── workflows/
│   └── 3engine_pipeline.md
├── pe2/                             ← 자동증식 3종
├── dashboard/
│   ├── README.md
│   └── metrics.md
└── applied-cases/
```

---

## 🚨 E-0N 오류 예측 시스템

PE-7 v2.7 기반 자동 오류 분류·수정 파이프라인 (`scripts/error_classifier.py`):

| 코드 | 오류 유형 | 자동 처리 | 심각도 |
|------|-----------|-----------|--------|
| E-01 | SHA 불일치 | SHA 자동 갱신 | 🟡 Medium |
| E-02 | 상태값 누락 | "Draft"로 초기화 | 🟡 Medium |
| E-03 | 버전 역행 | 롤백 차단 + 경고 | 🔴 High |
| E-04 | 구조 불일치 | diff 리포트 생성 | 🟡 Medium |
| E-05 | API 응답 없음 | Fallback → 로컬 캐시 | 🟠 Warning |
| E-06 | 중복 페이지 | 최신 1개 유지·archive | 🟡 Medium |
| E-07 | 필수 필드 누락 | 템플릿 자동 삽입 | 🟢 Low |
| E-08 | 인코딩 오류 | 자동 변환 후 재저장 | 🟢 Low |

---

## 🔧 KG 빌드 & 검증 실행

```bash
# Step 1 — Knowledge Graph 생성
python scripts/build_knowledge_graph.py \
  --input docs engines applied-cases workflows dashboard prompts \
  --full --sha \
  --output knowledge_graph.json

# Step 2 — 전체 검증 실행
python auto_validate.py --full \
  --report-dir reports/ \
  --kg knowledge_graph.json

# E-0N 오류 분류·자동 수정 실행
python scripts/error_classifier.py --auto-fix --report
```

---

## 🔧 RCA/CAPA 문서

| ID | 제목 | 개선 | 상태 |
|----|------|------|------|
| [RCA-001](./docs/rca-capa/RCA-001.md) | 프롬프트 구조 복잡도 | 파싱에러 -75%p | ✅ |
| [RCA-002](./docs/rca-capa/RCA-002.md) | 검증 기준 모호성 | 편차 -80% | ✅ |
| [RCA-003](./docs/rca-capa/RCA-003.md) | 필수 고려사항 누락 | 위험승인 -100% | ✅ |
| [RCA-004](./docs/rca-capa/RCA-004.md) | 중복 출력 과다 | 중복 -43%p | ✅ |

---

## 📈 버전 이력

| 버전 | 날짜 | 내용 |
|------|------|------|
| v1.0 | 2026-04-05 | 3-Engine 프레임워크 |
| v1.1 | 2026-04-05 | 엔진 파일 구조 수립 |
| v1.2 | 2026-04-09 | docs/rca-capa + Notion 양방향 링크 |
| v1.3 | 2026-04-09 | 재현 가능 연구 구조 전체 수립 |
| v1.4 | 2026-04-10 | 3-Engine 업그레이드 (CoT, 크로스오버) |
| v1.5 | 2026-04-10 | 자동개선·자동증식·자동검증 방식 업그레이드 |
| v1.6 | 2026-04-18 | KG 빌드 스크립트 방법 B 공식화 |
| **v1.7** | **2026-04-27** | **오타 수정(엔진니어링→엔지니어링) + P-00~P-06 인덱스 추가 + PE-7 v2.7 연계 명시 + E-0N 테이블 통합 (E-01/E-04 resolved)** |

---

## 📚 Notion 연계 문서

| Notion 페이지 | 타입 | URL |
|--------------|------|-----|
| Workspace SSOT Hub | Master | [링크](https://www.notion.so/f392046f06ff491698ca249849f03a40) |
| PE 허브 v2.0 | Mother | [링크](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b) |
| PE-7 AI 자동화 v2.7 | Engine | [링크](https://www.notion.so/34955ed436f081149dd6de25dba027d7) |
| RCA/CAPA 관리 | Mother | [링크](https://www.notion.so/33d55ed436f081bfa2aeccc26f344de5) |

---

## 🔗 연계 저장소

| 저장소 | 목적 |
|--------|------|
| [multi-agent-system-v3-hybrid](https://github.com/GilbertKwak/multi-agent-system-v3-hybrid) | 분석 시스템 v3.0 |
| [master-agent-v4.0b](https://github.com/GilbertKwak/master-agent-v4.0b) | 분석 시스템 v4.0 |
| [global-semiconductor-ai-research](https://github.com/GilbertKwak/global-semiconductor-ai-research) | 반도체 AI 연구 |
| [ip-rnd-master-hub](https://github.com/GilbertKwak/ip-rnd-master-hub) | IP-R&D 마스터 허브 |
| [parallel-process-hub](https://github.com/GilbertKwak/parallel-process-hub) | 병렬 프로세스 허브 |

---

> 관리자: Gilbert Kwak | 최종 업데이트: 2026-04-27 (v1.7) | 다음 리뷰: 2026-05 (v1.8)
