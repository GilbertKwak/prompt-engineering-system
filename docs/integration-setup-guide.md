# 🔧 Integration Setup Guide — 완전 자동화 셋업 절차

> **작성일**: 2026-04-26  
> **버전**: v1.0  
> **목적**: GCP · Slack · Notion · GitHub Secrets 5종 등록 → 완전 자동화 활성화  
> **연계**: PE-7 AI 자동화 설계 및 구현 v2.0

---

## 📋 전체 순서 요약

```
[1] GCP     → 서비스 계정 생성 → Sheets API 활성화 → JSON 키 발급
[2] Slack   → App 생성 → Incoming Webhooks 활성화 → URL 복사
[3] Notion  → Integration 생성 → KPI DB에 Integration 공유 → DB ID 복사
[4] GitHub  → gh secret set 명령으로 5종 시크릿 등록
[5] Actions → workflow_dispatch로 수동 실행 테스트
```

---

## STEP 1 · GCP 서비스 계정 + Sheets API

### 1-1. 서비스 계정 생성

```
GCP Console (console.cloud.google.com)
  └── IAM & Admin
      └── Service Accounts
          └── [+ CREATE SERVICE ACCOUNT]
              ├── 이름: pe7-automation
              ├── 역할: Editor (또는 Sheets API 전용 역할)
              └── [DONE]
```

### 1-2. Sheets API 활성화

```
APIs & Services → Library
  └── "Google Sheets API" 검색 → [ENABLE]
  └── "Google Drive API" 검색 → [ENABLE]  ← 파일 목록 접근 필요
```

### 1-3. JSON 키 발급

```
Service Accounts → pe7-automation → [KEYS 탭]
  └── Add Key → Create new key → JSON → [CREATE]
  → ~/Downloads/pe7-automation-xxxx.json 다운로드
```

> ⚠️ **보안 주의**: JSON 파일은 절대 Git에 커밋하지 말 것. `.gitignore`에 `*.json` 추가 확인.

---

## STEP 2 · Slack Incoming Webhook

### 2-1. Slack App 생성

```
https://api.slack.com/apps
  └── [Create New App] → From scratch
      ├── App Name: PE-7 AutoBot
      └── Workspace: [본인 워크스페이스 선택]
```

### 2-2. Incoming Webhooks 활성화

```
App Settings → Incoming Webhooks → Toggle ON
  └── [Add New Webhook to Workspace]
      └── 채널 선택: #pe7-alerts (또는 원하는 채널)
      └── [Allow]
  → Webhook URL 복사
     https://hooks.slack.com/services/T.../B.../xxxxxxxx
```

### 2-3. 테스트

```bash
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"🟢 PE-7 AutoBot 연결 테스트!"}' \
  https://hooks.slack.com/services/T.../B.../xxxxxxxx
```

---

## STEP 3 · Notion Integration + DB ID

### 3-1. Integration 생성

```
https://www.notion.so/my-integrations
  └── [+ New integration]
      ├── Name: PE-7 AutoSync
      ├── Logo: (선택)
      └── Capabilities:
          ├── ✅ Read content
          ├── ✅ Update content
          └── ✅ Insert content
  → Internal Integration Token 복사
     secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3-2. KPI DB에 Integration 공유

```
Notion KPI Database 페이지 열기
  └── 우상단 [···] 메뉴 → Connections → [PE-7 AutoSync] 선택
```

### 3-3. DB ID 추출

```
KPI DB URL 예시:
https://www.notion.so/workspace/KPI-Database-abcdef1234567890abcdef1234567890
                                              ↑ 이 32자리 = NOTION_KPI_DB_ID

※ 하이픈 포함 UUID 형식인 경우:
https://www.notion.so/...?v=12345678-1234-1234-1234-123456789012
→ v= 파라미터는 View ID (별개), URL의 32자리 path segment가 DB ID
```

---

## STEP 4 · GitHub Secrets 5종 등록

### 필요 시크릿 목록

| Secret 명 | 값 출처 | 사용 스크립트 |
|---|---|---|
| `NOTION_TOKEN` | Notion Integration Token (`secret_xxx`) | `ssot_sync.py`, `sheets_exporter.py` |
| `NOTION_KPI_DB_ID` | Notion KPI DB URL 32자리 | `sheets_exporter.py` |
| `GOOGLE_SHEETS_ID` | Sheets URL `/d/` 뒤 ID | `sheets_exporter.py` |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | GCP JSON 키 파일 전체 내용 | `sheets_exporter.py` |
| `SLACK_WEBHOOK_URL` | Slack Incoming Webhook URL | `error_classifier.py`, `pe7_daily_pipeline.yml` |

### CLI 일괄 등록

```bash
# GitHub CLI 설치 확인
gh auth status

# 개별 등록
gh secret set NOTION_TOKEN \
  -R GilbertKwak/prompt-engineering-system
# → 프롬프트에 값 붙여넣기

gh secret set NOTION_KPI_DB_ID \
  -R GilbertKwak/prompt-engineering-system

gh secret set GOOGLE_SHEETS_ID \
  -R GilbertKwak/prompt-engineering-system

# JSON 파일 직접 stdin으로 등록
gh secret set GOOGLE_SERVICE_ACCOUNT_JSON \
  -R GilbertKwak/prompt-engineering-system \
  < ~/Downloads/pe7-automation-xxxx.json

gh secret set SLACK_WEBHOOK_URL \
  -R GilbertKwak/prompt-engineering-system
```

### 등록 확인

```bash
gh secret list -R GilbertKwak/prompt-engineering-system

# 예상 출력:
# NOTION_TOKEN                   Updated 2026-04-26
# NOTION_KPI_DB_ID               Updated 2026-04-26
# GOOGLE_SHEETS_ID               Updated 2026-04-26
# GOOGLE_SERVICE_ACCOUNT_JSON    Updated 2026-04-26
# SLACK_WEBHOOK_URL              Updated 2026-04-26
```

---

## STEP 5 · GitHub Actions 수동 실행 테스트

### workflow_dispatch 수동 실행

```
GitHub.com → GilbertKwak/prompt-engineering-system
  └── Actions 탭
      └── pe7_e0n_validate (또는 pe7_daily_pipeline)
          └── [Run workflow] → Branch: main → [Run workflow]
```

또는 CLI:

```bash
# E-0N 검증 워크플로우 수동 실행
gh workflow run pe7_e0n_validate.yml \
  -R GilbertKwak/prompt-engineering-system \
  --ref main

# 실행 상태 모니터링
gh run list -R GilbertKwak/prompt-engineering-system --limit 5
gh run watch -R GilbertKwak/prompt-engineering-system
```

### 예상 실행 흐름 (약 2분)

```
[Job 1] checkout & setup-python (20s)
[Job 2] install dependencies    (15s)
[Job 3] run ssot_sync.py        (30s) → Notion-GitHub SHA 정합 확인
[Job 4] run error_classifier.py (30s) → E-01~E-08 스캔
[Job 5] send Slack notification  (5s)  → #pe7-alerts 채널 결과 전송
```

---

## ✅ 완료 체크리스트

- [ ] GCP 서비스 계정 생성 완료
- [ ] Google Sheets API + Drive API 활성화
- [ ] JSON 키 다운로드 완료
- [ ] Slack App 생성 및 Webhook URL 복사
- [ ] Notion Integration 생성 및 KPI DB 공유
- [ ] Notion KPI DB ID 추출 완료
- [ ] GitHub Secrets 5종 전체 등록 (`gh secret list` 확인)
- [ ] Actions workflow_dispatch 수동 실행 성공
- [ ] Slack 채널에 결과 알림 수신 확인

---

## 🔗 연계 파일

| 파일 | 역할 |
|---|---|
| `scripts/ssot_sync.py` | Notion-GitHub SSOT 정합 동기화 |
| `scripts/sheets_exporter.py` | Notion KPI DB → Google Sheets 내보내기 |
| `scripts/error_classifier.py` | E-0N 오류 자동 분류 및 Slack 알림 |
| `.github/workflows/pe7_daily_pipeline.yml` | 일일 자동 파이프라인 (KST 08:00) |
| `.github/workflows/pe7_e0n_validate.yml` | E-0N 검증 워크플로우 |

---

> **관리자**: Gilbert Kwak  
> **최초 작성**: 2026-04-26  
> **다음 업데이트**: Secrets 등록 완료 후 실행 결과 기록
