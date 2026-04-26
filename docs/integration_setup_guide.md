# 🔐 완전 자동화 Integration 설정 가이드

> **버전**: v1.0 | **작성일**: 2026-04-26 | **관리자**: Gilbert Kwak  
> **연계**: PE-7 v2.7 → GitHub Secrets 등록 완료 후 전체 자동화 시작 가능

---

## 🗺️ 전체 진행 순서

| Step | 항목 | 소요 시간 |
|------|------|----------|
| 1 | GCP 서비스 계정 + JSON 키 | ~10분 |
| 2 | Slack App + Incoming Webhook | ~5분 |
| 3 | Notion Integration + DB 공유 | ~5분 |
| 4 | GitHub Secrets 5종 등록 | ~5분 |
| 5 | workflow_dispatch 테스트 | ~3분 |

---

## Step 1 · GCP 서비스 계정 + Sheets API

### 1-1. 서비스 계정 생성

1. [GCP Console](https://console.cloud.google.com) 접속
2. **IAM & Admin → Service Accounts → + CREATE SERVICE ACCOUNT**
3. 이름: `pe7-automation` | 역할: Editor
4. **DONE** 클릭

### 1-2. Sheets API 활성화

1. **APIs & Services → Library →** `Google Sheets API` → **Enable**
2. `Google Drive API` 도 활성화

### 1-3. JSON 키 발급

1. 서비스 계정 클릭 → **KEYS 탭 → ADD KEY → JSON → CREATE**
2. 다운로드 된 `pe7-automation-xxxx.json` 보관

> ⚠️ `private_key` 포함 파일 — GitHub에 직접 커밋 금지

### 1-4. Sheets에 서비스 계정 이메일 으로 편집자 공유

```bash
# Secret 등록
gh secret set GOOGLE_SERVICE_ACCOUNT_JSON \
  -R GilbertKwak/prompt-engineering-system \
  < ~/Downloads/pe7-automation-xxxx.json
```

---

## Step 2 · Slack App + Incoming Webhooks

1. [api.slack.com/apps](https://api.slack.com/apps) → **Create New App → From scratch**
2. App Name: `PE7-AutoBot` / Workspace 선택
3. **Incoming Webhooks → ON → Add New Webhook → 음 노 선택**
4. 생성된 URL 복사

```bash
# 동작 테스트
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"🟢 PE-7 AutoBot 테스트!"}' \
  https://hooks.slack.com/services/T.../B.../xxx

# Secret 등록
gh secret set SLACK_WEBHOOK_URL \
  -R GilbertKwak/prompt-engineering-system \
  --body "https://hooks.slack.com/services/T.../B.../xxx"
```

---

## Step 3 · Notion Integration + KPI DB 공유

### Integration 생성

1. [notion.so/my-integrations](https://www.notion.so/my-integrations) → **+ New integration**
2. 이름: `PE7-Automation` | Type: Internal
3. **Internal Integration Secret** 복사

### KPI DB ID 추출

```
Notion DB URL:
https://notion.so/workspace/KPI-DB-abcdef1234567890abcdef1234567890
                                      ↑ 이 32자리 = NOTION_KPI_DB_ID

?v= 파라미터가 있는 경우:
https://notion.so/...?v=abcdef12-3456-7890-abcd-ef1234567890
                       ↑ 하이픈 제거 후 32자리 사용
```

```bash
gh secret set NOTION_TOKEN -R GilbertKwak/prompt-engineering-system \
  --body "secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

gh secret set NOTION_KPI_DB_ID -R GilbertKwak/prompt-engineering-system \
  --body "abcdef1234567890abcdef1234567890"
```

---

## Step 4 · 5종 Secrets 일괄 등록

| Secret명 | 확보 경로 | 사용 스크립트 |
|---------|-----------|---------------|
| `NOTION_TOKEN` | notion.so/my-integrations | ssot_sync.py |
| `NOTION_KPI_DB_ID` | Notion DB URL 32자리 | sheets_exporter.py |
| `GOOGLE_SHEETS_ID` | Sheets URL /d/{ID}/ | sheets_exporter.py |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | GCP JSON 키 파일 전체 | sheets_exporter.py |
| `SLACK_WEBHOOK_URL` | Slack App Incoming Webhooks | notify.py |

```bash
# 일괄 등록
chmod +x scripts/pe7/setup/register_secrets.sh
./scripts/pe7/setup/register_secrets.sh

# 확인
gh secret list -R GilbertKwak/prompt-engineering-system
```

---

## Step 5 · GitHub Actions 테스트

```bash
# pe7_e0n_validate 수동 실행
gh workflow run pe7_e0n_validate.yml \
  -R GilbertKwak/prompt-engineering-system \
  --ref main

# 실시간 로그 모니터링
gh run watch -R GilbertKwak/prompt-engineering-system
```

### 성공 시 Slack 알림 예시

```
🟢 [PE-7] E-0N Validation 완료
✅ E-01 PASS / ✅ E-02 PASS / ✅ E-04 PASS
실행 시각: 2026-04-26 12:30 KST
```

---

## 📊 완료 체크리스트

- [ ] GCP 서비스 계정 생성 (`pe7-automation`)
- [ ] Sheets API + Drive API 활성화
- [ ] JSON 키 다운로드
- [ ] Sheets 편집자 공유
- [ ] Slack App 생성 (`PE7-AutoBot`)
- [ ] Incoming Webhooks ON + URL 복사
- [ ] curl 테스트 성공
- [ ] Notion Integration 생성
- [ ] KPI DB Integration 연결
- [ ] DB ID 32자리 복사
- [ ] 5종 Secrets 등록 (`register_secrets.sh`)
- [ ] `pe7_e0n_validate.yml` 수동 실행 성공
- [ ] Slack 알림 수신 ✅

---

## 🔗 관련 파일

| 파일 | 경로 |
|------|------|
| `register_secrets.sh` | `scripts/pe7/setup/` |
| `sheets_exporter.py` | `scripts/pe7/` |
| `ssot_sync.py` | `scripts/pe7/` |
| `error_classifier.py` | `scripts/pe7/` |
| `pe7_e0n_validate.yml` | `.github/workflows/` |
| `pe7_daily_pipeline.yml` | `.github/workflows/` |

---

*마지막 업데이트: 2026-04-26 | 연계 Notion: [Integration 설정 가이드](https://www.notion.so/34e55ed436f081d09a51fb6a95e5e6d6)*
