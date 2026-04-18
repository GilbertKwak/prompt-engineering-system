# 🔄 Auto-Sync Log — Notion × GitHub 자동 연동 이력

> **관리자**: Gilbert Kwak | **최초 작성**: 2026-04-15 | **버전**: v1.2  
> **Notion 연동 페이지**: [🔧 RCA/CAPA 문제 해결 관리 시스템](https://www.notion.so/33d55ed436f081bfa2aeccc26f344de5)  
> **Mother 페이지**: [🧠 프롬프트 엔지니어링 시스템 허브 v2.0](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b)

---

## 🎯 자동 연동 체계 개요

```
[문제 발생 & RCA 분석]
        ↓
[CAPA 해결방안 수립]
        ↓
┌─────────────────────────────────────┐
│  Perplexity AI MCP 자동 실행         │
│  ① Notion Child 페이지 직접 업데이트  │
│  ② GitHub 커밋·파일 직접 업데이트    │
│  ③ Mother 페이지 버전 이력 자동 갱신  │
└─────────────────────────────────────┘
        ↓
[양방향 링크 & 버전 태그 완료]
```

### 적용 원칙
- 모든 RCA/CAPA는 Notion Child 페이지 + GitHub `docs/rca-capa/` 동시 반영
- Mother 페이지 버전 이력은 매 업데이트마다 자동 갱신
- GitHub 커밋 메시지 형식: `sync(notion): <내용>` 또는 `sync(notion+github): <내용>`
- 단방향(Notion only / GitHub only) 업데이트 금지 — 반드시 양방향 동기화

---

## 📋 연동 이력

| 날짜 | 버전 | 작업 내용 | Notion | GitHub | 담당 |
|------|------|-----------|--------|--------|------|
| **2026-04-18** | **v1.2** | **auto_validate.py 실행 분석** — knowledge_graph.json 미존재로 KG 체크 SKIP 처리, reports/ MD 파일 RCA-001~004 검증 기준 분석, AUTO_VALIDATE_RUN.md 신규 생성, Notion RCA/CAPA 허브 v1.2 갱신 | ✅ | ✅ | Perplexity AI |
| 2026-04-15 | v1.1 | 자동 Notion·GitHub 직접 연동 체계 첫 적용 — AUTO_SYNC_LOG.md 생성, RCA/CAPA 허브 v1.1 갱신, Mother 허브 v2.0 자동 업데이트 체계 구축 | ✅ | ✅ | Perplexity AI |
| 2026-04-09 | v1.0 | 최초 생성 — RCA-001~004 문서화 완료, docs/rca-capa/ 구조 수립 | ✅ | ✅ | Perplexity AI |

---

## 🗂️ RCA/CAPA 현황 스냅샷 (2026-04-18 기준)

| RCA ID | 제목 | 상태 | Notion | GitHub |
|--------|------|------|--------|--------|
| RCA-001 | 프롬프트 구조 복잡도 (XML→Markdown 전환) | ✅ 완료 | [링크](https://www.notion.so/33d55ed436f081c593ede0347d2b581a) | `docs/rca-capa/RCA-001.md` |
| RCA-002 | 검증 기준 모호성 (정량적 스코어 전환) | ✅ 완료 | [링크](https://www.notion.so/33d55ed436f081d0a7a1d4a2a8de4a8f) | `docs/rca-capa/RCA-002.md` |
| RCA-003 | 필수 고려사항 누락 (RISK 에이전트 개선) | ✅ 완료 | [링크](https://www.notion.so/33d55ed436f0817e83e0f3bc0f168316) | `docs/rca-capa/RCA-003.md` |
| RCA-004 | 중복 출력 과다 (에이전트 Scope 경계 명확화) | ✅ 완료 | [링크](https://www.notion.so/33d55ed436f08195bd49cdd19f062644) | `docs/rca-capa/RCA-004.md` |

### auto_validate.py 최근 실행 결과 (2026-04-18)

| 항목 | 상태 | 비고 |
|------|------|------|
| `knowledge_graph.json` | ❌ SKIP | 파일 미존재 — KG 체크 전체 건너뜀 |
| `reports/` MD 파일 검증 | ✅ 실행됨 | RCA-001~004 규칙 적용 |
| RCA-001 메타데이터 헤더 완전성 | 🔍 검증 대상 | title·date·version·status 필드 |
| RCA-002 섹션 구조 일관성 | 🔍 검증 대상 | H2/H3 템플릿 순서 |
| RCA-003 크로스 레퍼런스 유효성 | ⚠️ 부분 검증 | KG 미존재로 심층 탐지 불가 |
| RCA-004 언어 일관성 (KO/EN) | 🔍 검증 대상 | KO↔EN 섹션 수 일치 여부 |

**누적 성과**
- 구조적 일관성: **+40%p**
- 스코어링 편차: **-80%**
- 실행 완주율: **+45%p**

---

## 🔧 KG SKIP 해소 권장 커맨드

```bash
# Step 1: KG 생성
python scripts/build_kg.py --input reports/ --output knowledge_graph.json

# Step 2: 전체 검증 재실행
python auto_validate.py --full --report-dir reports/ --kg knowledge_graph.json

# Step 3: 실패 항목만 필터링
python auto_validate.py --filter FAIL --export validation_report.csv
```

---

## 🔗 연관 리소스

### Notion 페이지 맵
```
🧠 Mother: 프롬프트 엔지니어링 시스템 허브 v2.0
└── 🔧 RCA/CAPA 문제 해결 관리 시스템 (v1.2)
    ├── 📋 RCA-001 프롬프트 구조 복잡도
    ├── 📋 RCA-002 검증 기준 모호성
    ├── 📋 RCA-003 필수 고려사항 누락
    └── 📋 RCA-004 중복 출력 과다
```

### GitHub 파일 맵
```
prompt-engineering-system/
├── README.md
├── IMPROVEMENT_LOG.md
└── docs/
    ├── index.md
    └── rca-capa/
        ├── AUTO_SYNC_LOG.md       ← 이 파일 (v1.2)
        ├── AUTO_VALIDATE_RUN.md   ← 신규 (2026-04-18)
        ├── RCA-001.md
        ├── RCA-002.md
        ├── RCA-003.md
        └── RCA-004.md
```

---

*최종 업데이트: 2026-04-18 | 다음 리뷰: 2026-05*
