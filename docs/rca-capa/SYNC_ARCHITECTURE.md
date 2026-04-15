# ⚙️ Auto-Sync Architecture — Notion × GitHub 연동 설계

> **버전**: v1.0 | **작성일**: 2026-04-15  
> **목적**: Perplexity AI MCP 도구를 활용한 Notion·GitHub 자동 직접 연동 체계 정의

---

## 🏗️ 아키텍처 개요

### 연동 방식: MCP(Model Context Protocol) 직접 연동

```
┌─────────────────────────────────────────────────────────────┐
│                    Perplexity AI (Agent)                     │
├─────────────────────┬───────────────────────────────────────┤
│   Notion MCP Tool   │         GitHub MCP Tool                │
│  ┌───────────────┐  │  ┌──────────────────────────────────┐  │
│  │ search        │  │  │ get_file_contents                │  │
│  │ fetch         │  │  │ push_files                       │  │
│  │ update_page   │  │  │ create_or_update_file            │  │
│  │ create_pages  │  │  │ list_commits                     │  │
│  └───────────────┘  │  └──────────────────────────────────┘  │
└─────────────────────┴───────────────────────────────────────┘
        │                              │
        ▼                              ▼
┌───────────────┐              ┌───────────────┐
│  Notion       │              │  GitHub       │
│  Workspace    │◄────────────►│  Repository   │
│               │  양방향 링크  │               │
│  Mother Page  │              │  README.md    │
│  └ Child Pages│              │  docs/        │
│    └ RCA-001  │              │  └ rca-capa/  │
│    └ RCA-002  │              │    └ *.md     │
│    └ RCA-003  │              │               │
│    └ RCA-004  │              │               │
└───────────────┘              └───────────────┘
```

---

## 📐 Mother-Child 페이지 구조 업데이트 규칙

### 규칙 1: Child 우선, Mother 후
```
1. Child 페이지 내용 업데이트 (Notion)
2. GitHub docs/ 대응 파일 업데이트
3. Mother 페이지 버전 이력 갱신
4. GitHub SYNC_LOG 갱신
```

### 규칙 2: 버전 명명 규칙
| 변경 유형 | 버전 증분 | 예시 |
|-----------|-----------|------|
| 새 RCA 추가 | Minor +0.1 | v1.0 → v1.1 |
| 기존 RCA 수정 | Patch +0.0.1 | v1.1 → v1.1.1 |
| 아키텍처 변경 | Major +1.0 | v1.x → v2.0 |

### 규칙 3: 커밋 메시지 형식
```
sync(notion+github): <작업 요약> — <날짜>
sync(notion): <Notion only 작업>
sync(github): <GitHub only 작업>
feat(rca-capa): <새 RCA 추가>
fix(rca-<id>): <기존 RCA 수정>
```

---

## 🔄 업데이트 트리거 조건

| 트리거 | 처리 방식 | 우선순위 |
|--------|-----------|----------|
| 새 문제 발생 | 새 RCA Child 페이지 생성 + GitHub 파일 추가 | 🔴 즉시 |
| CAPA 해결 완료 | Child 페이지 상태 업데이트 + SYNC_LOG 갱신 | 🟠 당일 |
| 효과 측정 결과 | Child 페이지 성과 섹션 업데이트 | 🟡 주간 |
| 정기 리뷰 | 전체 현황 표 갱신 + Mother 버전 업 | 🟢 월간 |

---

## ✅ 품질 체크리스트

업데이트 후 확인 항목:
- [ ] Notion Child 페이지 최신 내용 반영됨
- [ ] GitHub `docs/rca-capa/` 파일 동기화됨
- [ ] Mother 페이지 버전 이력 갱신됨
- [ ] `AUTO_SYNC_LOG.md` 이력 추가됨
- [ ] Notion ↔ GitHub 양방향 링크 유효함
- [ ] 버전 번호 일관성 확인됨

---

*작성: 2026-04-15 | Perplexity AI Auto-Sync 체계 v1.0*
