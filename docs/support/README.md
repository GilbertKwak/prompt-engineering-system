# 🛠️ Support Modules — 공통 템플릿 & 루브릭

> **경로**: `docs/support/` | **관리자**: Gilbert Kwak | **업데이트**: 2026-04-09

[![Master Index](https://img.shields.io/badge/←%20Back-Master%20Index-gray)](../index.md)

이 디렉토리는 PE-1~5 에이전트 및 전체 시스템에서 공통으로 사용하는 **프롬프트 템플릿, 루브릭, 공통 모듈**을 관리합니다.

---

## 📁 파일 목록

| 파일 | 내용 | 상태 |
|------|------|------|
| *(예정)* `prompt-template-base.md` | 기본 프롬프트 템플릿 (역할·입력·출력·제약 포맷) | 🟡 작성 예정 |
| *(예정)* `rubric-standard.md` | PE-3 검증용 루브릭 기준표 | 🟡 작성 예정 |
| *(예정)* `common-constraints.md` | 공통 제약 조건 모음 (COT 규칙 등) | 🟡 작성 예정 |

---

## 📌 사용 지침

1. 새 에이전트 또는 프롬프트 작성 시 `prompt-template-base.md`를 기반으로 시작합니다.
2. 루브릭은 PE-3의 스코어링 기준(`docs/agent3/README.md`)과 동기화를 유지합니다.
3. 공통 제약 조건 변경 시 모든 에이전트 문서(agent1~5)에 반영 여부를 확인합니다.

---

> 관련 문서: [Master Index](../index.md) | [PE-3 자동검증](../agent3/README.md)
