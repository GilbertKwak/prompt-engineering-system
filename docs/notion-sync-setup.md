# Notion PE Hub Sync — 설정 가이드

## 개요

`prompt-engineering-system` ↔ Notion PE 허브 자동 동기화 파이프라인 설정 문서.

**파이프라인 구조:**
```
GitHub push (engines/**, scripts/**, PE-*/**)
       │
       ▼
.github/workflows/notion-sync.yml
       │
       ├── Job: sync-engines → Notion PE 허브 DB
       ├── Job: sync-scripts → Notion Scripts DB
       └── Job: sync-reports → Notion Reports DB
```

---

## Step 1: Notion Integration 생성

1. [Notion 개발자 포털](https://www.notion.so/my-integrations) 접속
2. **+ New integration** 클릭
3. 설정:
   - Name: `GitHub PE Hub Sync`
   - Associated workspace: 본인 워크스페이스 선택
   - Capabilities: **Read content** + **Update content** + **Insert content** 체크
4. **Submit** → `Internal Integration Token` 복사

---

## Step 2: Notion 데이터베이스 3개 생성

### 2-1. PE 허브 DB (3-Engine 구조)

Notion에서 새 데이터베이스 생성 후 아래 속성 추가:

| 속성명 | 타입 | 설명 |
|--------|------|------|
| Name | Title | 엔진 표시명 |
| Engine ID | Text | PE-CON / PE-FIN / PE-IP |
| Domain | Select | 도메인 분류 |
| Status | Select | Active / Missing |
| File Count | Number | 파일 수 |
| Prompt Count | Number | 프롬프트 수 |
| Script Count | Number | 스크립트 수 |
| Description | Text | 요약 설명 |
| Last Modified | Date | 최근 수정일 |
| GitHub URL | URL | 원본 링크 |

### 2-2. Scripts DB

| 속성명 | 타입 |
|--------|------|
| Name | Title |
| File Path | Text |
| Description | Text |
| Arguments | Text |
| File Size (KB) | Number |
| Last Modified | Date |
| Engine Tag | Select |
| GitHub URL | URL |

### 2-3. Reports DB

| 속성명 | 타입 |
|--------|------|
| Name | Title |
| File Path | Text |
| Summary | Text |
| Engine Tag | Select |
| Last Modified | Date |
| Word Count | Number |
| GitHub URL | URL |

---

## Step 3: Integration을 각 DB에 연결

각 Notion 데이터베이스에서:
1. 우상단 **...** → **Add connections**
2. `GitHub PE Hub Sync` 선택 → **Confirm**

---

## Step 4: 데이터베이스 ID 추출

Notion DB URL 형식:
```
https://www.notion.so/workspace/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx?v=...
                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                이 32자리가 Database ID
```

ID에 하이픈 추가 (8-4-4-4-12 형식):
```
xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

---

## Step 5: GitHub Secrets 등록

[GitHub Repository Settings](https://github.com/GilbertKwak/prompt-engineering-system/settings/secrets/actions) → **New repository secret**

| Secret 이름 | 값 |
|-------------|----|
| `NOTION_TOKEN` | Notion Integration Token (Step 1) |
| `NOTION_PE_HUB_DB_ID` | PE 허브 DB ID |
| `NOTION_SCRIPTS_DB_ID` | Scripts DB ID |
| `NOTION_REPORTS_DB_ID` | Reports DB ID |

---

## Step 6: 파이프라인 첫 실행

### 옵션 A: 수동 실행 (권장 — 첫 테스트)

1. GitHub → **Actions** 탭
2. **Notion PE Hub Sync** 워크플로 선택
3. **Run workflow** → `dry_run: true` 체크 → **Run workflow**
   - Notion에 실제 쓰기 없이 구조 검증
4. 로그 확인 후 이상 없으면 `dry_run: false`로 재실행

### 옵션 B: 자동 트리거

`engines/`, `scripts/`, `PE-*/`, `reports/` 경로 내 파일 수정 후 `git push`하면 자동 실행.

---

## 문제 해결

### `APIResponseError: object_not_found`
- DB ID가 잘못되었거나 Integration이 DB에 연결되지 않은 상태
- Step 3 재확인

### `APIResponseError: unauthorized`
- `NOTION_TOKEN` Secret 값 오류
- Notion 통합 토큰 재생성 후 Secret 업데이트

### `Engine directory not found`
- `engines/PE-CON`, `engines/PE-FIN`, `engines/PE-IP` 디렉토리 없음
- 루트의 `PE-CON/`, `PE-FIN/`, `PE-IP/` 디렉토리를 자동으로 폴백 탐색함

---

## 동기화 주기

| 트리거 | 조건 |
|--------|------|
| **자동 (push)** | `engines/**`, `scripts/**`, `PE-*/**`, `reports/**` 변경 시 |
| **자동 (cron)** | 매일 09:00 KST (00:00 UTC) |
| **수동** | Actions 탭 → Run workflow |

---

## 파일 구조

```
.github/
├── workflows/
│   └── notion-sync.yml          # 메인 워크플로
└── scripts/
    ├── sync_engines_to_notion.py  # 3-Engine → PE 허브 DB
    ├── sync_scripts_to_notion.py  # scripts/ → Scripts DB
    └── sync_reports_to_notion.py  # reports/PE-* → Reports DB
docs/
└── notion-sync-setup.md          # 이 문서
```
