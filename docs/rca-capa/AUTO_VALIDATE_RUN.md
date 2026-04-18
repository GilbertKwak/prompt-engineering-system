# 🤖 Auto Validate Run Log — 실행 결과 분석

> **실행일**: 2026-04-18 20:22 KST | **버전**: v1.0  
> **실행 스크립트**: `auto_validate.py`  
> **Notion 연동**: [🔧 RCA/CAPA 문제 해결 관리 시스템](https://www.notion.so/33d55ed436f081bfa2aeccc26f344de5)  
> **작성**: Perplexity AI MCP Auto-Sync

---

## 📊 실행 환경 상태

| 항목 | 상태 | 비고 |
|------|------|------|
| `knowledge_graph.json` | ❌ 없음 | KG 체크 **SKIP** 처리 |
| `reports/` 폴더 | ✅ 존재 | MD 파일 대상 검증 진행 |
| RCA 검증 엔진 | ✅ 활성 | RCA-001 ~ 004 적용 |
| 전체 실행 모드 | ⚠️ PARTIAL | KG 제외 부분 실행 |

---

## 📋 RCA 규칙별 검증 기준

| 규칙 ID | 검증 항목 | 검사 대상 | 통과 조건 |
|---------|----------|----------|----------|
| **RCA-001** | 메타데이터 헤더 완전성 | 모든 `.md` 파일 | `title`, `date`, `version`, `status` 필드 존재 |
| **RCA-002** | 섹션 구조 일관성 | H2/H3 계층 | 정해진 섹션 템플릿 순서 준수 |
| **RCA-003** | 크로스 레퍼런스 유효성 | `[[링크]]` 또는 `[링크]()` | 참조 대상 파일 실존 여부 |
| **RCA-004** | 언어 일관성 (KO/EN) | 본문 전체 | KO 버전 ↔ EN 버전 섹션 수 일치 |

---

## ⚠️ KG SKIP 영향 범위

`knowledge_graph.json`이 없을 경우 건너뛰어지는 항목:

- **RCA-003 심층 검증** — 파일 간 의존성 그래프 순환 참조 탐지 불가
- **노드 연결도 검사** — 고립(orphan) 문서 탐지 불가
- **태그 클러스터 검증** — 토픽 일관성 자동 분류 불가

> 💡 **권장 액션**: `scripts/build_kg.py`를 먼저 실행하여 `knowledge_graph.json`을 생성한 뒤
> `auto_validate.py --full`로 재실행하면 완전한 검증 가능

---

## 🔧 즉시 실행 권장 커맨드

```bash
# Step 1: KG 생성
python scripts/build_kg.py --input reports/ --output knowledge_graph.json

# Step 2: 전체 검증 재실행
python auto_validate.py --full --report-dir reports/ --kg knowledge_graph.json

# Step 3: 실패 항목만 필터링
python auto_validate.py --filter FAIL --export validation_report.csv
```

---

## 🔁 다음 단계 액션 플랜

| 우선순위 | 액션 | 담당 | 기한 |
|---------|------|------|------|
| 🔴 HIGH | `scripts/build_kg.py` 실행 → `knowledge_graph.json` 생성 | Gilbert | 즉시 |
| 🔴 HIGH | `auto_validate.py --full` 재실행으로 완전 검증 확보 | Gilbert | KG 생성 후 |
| 🟡 MED | RCA-003 심층 검증 — 순환 참조 및 orphan 문서 점검 | Gilbert | 이번 주 내 |
| 🟡 MED | `validation_report.csv` 생성 → FAIL 항목 CAPA 등록 | Gilbert | 검증 후 |
| 🟢 LOW | KG 자동 갱신 GitHub Actions 워크플로우 구성 | Gilbert | 2026-05 |

---

## 🔗 연관 문서

- [AUTO_SYNC_LOG.md](./AUTO_SYNC_LOG.md) — 전체 연동 이력
- [RCA-001.md](./RCA-001.md) — 프롬프트 구조 복잡도
- [RCA-002.md](./RCA-002.md) — 검증 기준 모호성
- [RCA-003.md](./RCA-003.md) — 필수 고려사항 누락
- [RCA-004.md](./RCA-004.md) — 중복 출력 과다
- [README.md](./README.md) — RCA/CAPA 시스템 개요

---

*생성: 2026-04-18 | 다음 실행 예정: KG 생성 후 즉시*
