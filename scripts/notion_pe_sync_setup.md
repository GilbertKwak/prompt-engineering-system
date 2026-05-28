# Notion PE Hub Sync — 설정 가이드

> **1순위 연동:** `prompt-engineering-system` ↔ Notion PE 허브
> GitHub Actions가 `PE-CON / PE-FIN / PE-IP` 변경을 감지해 Notion DB에 자동 Push

---

## 1. 전제 조건

| 항목 | 내용 |
|------|------|
| Notion Integration | 워크스페이스 내 Internal Integration 생성 필요 |
| 데이터베이스 권한 | Integration을 PE 허브 DB에 초대 (Share → 연결) |
| GitHub Secrets | `NOTION_TOKEN`, `NOTION_DATABASE_ID` 등록 필수 |

---

## 2. Notion Integration 생성 (1회)

```
1. https://www.notion.so/my-integrations 접속
2. "+ New integration" 클릭
3. Name: pe-hub-sync  /  Type: Internal
4. Capabilities: ✅ Read content  ✅ Update content  ✅ Insert content
5. Submit → "Internal Integration Token" 복사
```

---

## 3. Notion PE 허브 DB 설정

### 3-1. DB 컬럼 구조 (최소 요구)

| 컬럼명 | 타입 | 용도 |
|--------|------|------|
| **Name** | Title | 파일명 (stem) |
| **Engine** | Select | PE-CON / PE-FIN / PE-IP |
| **File Path** | Rich Text | repo 내 상대경로 |
| **SHA-256** | Rich Text | 변경 감지 해시 (앞 16자) |
| **Synced At** | Date | 마지막 동기화 시각 (UTC) |
| **Status** | Select | Active / Archived |
| **Content** | Rich Text | 파일 내용 앞 2,000자 |

### 3-2. DB ID 확인 방법

```
Notion 페이지 URL 예시:
https://www.notion.so/workspace/PE-Hub-abc123def456789...
                                          ^^^^^^^^^^^^^^^^^^^^^^^^
                                          이 부분 32자가 Database ID
```

---

## 4. GitHub Secrets 등록

```
Settings → Secrets and variables → Actions → New repository secret

NOTION_TOKEN        =  secret_xxxxxxxxxxxxxxxxxxxx  (Integration Token)
NOTION_DATABASE_ID  =  abc123def456789...           (32자 DB ID)
```

---

## 5. 로컬 테스트 실행

```bash
# .env 파일 생성 (레포 루트)
cp .env.example .env
# NOTION_TOKEN, NOTION_DATABASE_ID 값 직접 입력

# Dry-run (Notion 실제 호출 없이 미리보기)
export NOTION_TOKEN=secret_xxx
export NOTION_DATABASE_ID=abc123
python scripts/notion_pe_sync.py --engine ALL --dry-run

# 실제 동기화 (PE-FIN만)
python scripts/notion_pe_sync.py --engine PE-FIN
```

---

## 6. GitHub Actions 트리거 방법

| 트리거 | 조건 |
|--------|------|
| **자동 (Push)** | `main` 브랜치에 PE-CON/PE-FIN/PE-IP 파일 변경 시 즉시 실행 |
| **정기 (Cron)** | 매일 09:00 KST 전체 동기화 |
| **수동** | Actions 탭 → "Notion PE Hub Sync" → "Run workflow" → 엔진 선택 |

---

## 7. 파이프라인 흐름

```
Git Push (PE-CON/FIN/IP 변경)
         │
         ▼
  GitHub Actions 트리거
         │
         ▼
  notion_pe_sync.py 실행
         │
    ┌────┴────┐
    │  Notion DB 쿼리   ← 기존 페이지 + SHA 해시 로드
    └────┬────┘
         │
    SHA 비교
    ├─ 동일 → SKIP
    ├─ 변경 → UPDATE (patch page)
    └─ 신규 → CREATE (new page)
         │
         ▼
  실행 요약 출력 (Created/Updated/Skipped/Errors)
```

---

## 8. 확장 방법

- **scripts/financial_bridge_v1.py 결과 Push**: `sync_engine()` 함수 뒤에
  `output/` 디렉토리도 추가하여 IRR/NPV 결과 JSON을 자동 게시 가능
- **Slack 알림**: `.github/workflows/notion-pe-sync.yml` 하단 주석 해제
- **2순위·3순위 연동 확장**: 동일 패턴으로 `T09-master`, `HBM-Salvage-Reports` 대응
