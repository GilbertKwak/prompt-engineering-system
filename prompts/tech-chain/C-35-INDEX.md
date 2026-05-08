---
title: "C-35 PE-TECH · 기술해설-진단-설계 통합 라이브러리 v1.0"
cluster: C-35
domain: PE-TECH
version: "1.0"
pe3_target: 93
status: active
created: 2026-05-08
linked_clusters: [C-34, C-08, PE-11]
prompts:
  - SP-TECH-EXPLAIN-001 v2.0
  - SP-TECH-DIAGNOSE-001 v2.0
  - SP-TECH-SOLUTION-001 v2.0
kg_delta: "+3 nodes / +7 edges"
kg_rebuild: scheduled
notion_ssot: C-35
---

# ⚙️ C-35 PE-TECH · 기술해설-진단-설계 통합 라이브러리 v1.0

> **클러스터**: C-35 | **도메인**: PE-TECH | **PE-3 목표**: 93+  
> **생성일**: 2026-05-08 | **상태**: 🟢 Active

---

## 📋 라이브러리 개요

기술 도메인 전반의 **해설(Explain) → 진단(Diagnose) → 설계/해결(Solution)** 3단계
체인 프롬프트를 통합 관리하는 클러스터 허브. PE-ARCH(C-34)의 아키텍처 레이어와
연동하며, PE-EDU(C-08)의 교육 출력 포맷을 공유한다.

---

## 🗂️ 포함 프롬프트 인덱스

| ID | 버전 | 역할 | 파일 | PE-3 목표 |
|----|------|------|------|-----------|
| SP-TECH-EXPLAIN-001 | v2.0 | 기술 개념·원리 해설 | `SP-TECH-EXPLAIN-001-v2.0.md` | 93 |
| SP-TECH-DIAGNOSE-001 | v2.0 | 기술 문제 진단·원인분석 | `SP-TECH-DIAGNOSE-001-v2.0.md` | 94 |
| SP-TECH-SOLUTION-001 | v2.0 | 기술 설계·해결방안 도출 | `SP-TECH-SOLUTION-001-v2.0.md` | 93 |

---

## 🔗 연계 클러스터

| 클러스터 | 역할 | 연결 유형 |
|---------|------|----------|
| **C-34 PE-ARCH** | 시스템 아키텍처 설계 프레임 | INPUT → TECH |
| **C-08 PE-EDU** | 교육·해설 출력 포맷 공유 | FORMAT SHARE |
| **PE-11 오케스트레이터** | 멀티체인 실행 조율 | ORCHESTRATE |

---

## 📊 Knowledge Graph 업데이트 예약

```yaml
kg_update:
  nodes_add: 3
  edges_add: 7
  nodes:
    - id: SP-TECH-EXPLAIN-001
      type: prompt
      cluster: C-35
    - id: SP-TECH-DIAGNOSE-001
      type: prompt
      cluster: C-35
    - id: SP-TECH-SOLUTION-001
      type: prompt
      cluster: C-35
  edges:
    - [C-35, CONTAINS, SP-TECH-EXPLAIN-001]
    - [C-35, CONTAINS, SP-TECH-DIAGNOSE-001]
    - [C-35, CONTAINS, SP-TECH-SOLUTION-001]
    - [C-34, FEEDS_INTO, C-35]
    - [C-08, SHARES_FORMAT, C-35]
    - [PE-11, ORCHESTRATES, C-35]
    - [SP-TECH-EXPLAIN-001, CHAINS_TO, SP-TECH-DIAGNOSE-001]
  rebuild_command: "pe-graph --rebuild --delta C-35"
  scheduled: 2026-05-08
```

---

## ⚡ 에러 예측 및 사전 검증

| 위험 유형 | 발생 조건 | 대응 방안 |
|----------|----------|----------|
| PE-3 미달 | 기술 도메인 특이성 누락 | DIAGNOSE → SOLUTION 체인 재실행 |
| 체인 단절 | EXPLAIN 출력이 DIAGNOSE 입력 미충족 | Chain Handoff 변수 `{{tech_context}}` 명시 |
| 지식 그래프 충돌 | 기존 노드 ID 중복 | `--dry-run` 후 커밋 |
| Notion 미동기 | SSOT 갱신 누락 | 세션 종료 전 Notion 페이지 확인 |

---

*작성: Perplexity AI Assistant | 2026-05-08 15:29 KST*
