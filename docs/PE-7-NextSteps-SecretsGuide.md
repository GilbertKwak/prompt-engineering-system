# PE-7 v2.0 — GitHub Secrets 등록 완전 가이드

> **Gilbert Kwak** | 2026-04-26 | PE-7 v2.0 Next Steps 전체 실행베이스

---

## 🔑 등록해야 할 Secrets 8개

| # | Secret 이름 | 어디서 확보 | 사용 스크립트 |
|---|---|---|---|
| 1 | `NOTION_TOKEN` | Notion Settings → Integrations | 전체 |
| 2 | `NOTION_KPI_DB_ID` | KPI 데이터베이스 URL 내 32자리 ID | A-1, B-1 |
| 3 | `GOOGLE_SHEETS_ID` | Google Sheets URL `spreadsheets/d/{ID}` | A-1 |
| 4 | `GOOGLE_SERVICE_ACCOUNT_JSON` | GCP IAM → 서비스 계정 → 키 생성 | A-1 |
| 5 | `OPENAI_API_KEY` | platform.openai.com/api-keys | B-3, D-2 |
| 6 | `REDDIT_CLIENT_ID` | reddit.com/prefs/apps | B-3 |
| 7 | `REDDIT_SECRET` | reddit.com/prefs/apps | B-3 |
| 8 | `SLACK_WEBHOOK_URL` | Slack App → Incoming Webhooks | 전체 알림 |

---

## ℹ️ 스크릿 인터페이스(UI) 등록 절차

```
1. https://github.com/GilbertKwak/prompt-engineering-system/settings/secrets/actions 접속
2. [New repository secret] 클릭
3. Name: NOTION_TOKEN
   Value: secret_xxxxxxxxxxxx (Notion 인터그레이션 토큰)
4. [Add secret] 클릭
5. 위 2~4 단계를 나머지 7개에 대해 반복
```

---

## ⚡ gh CLI 일괄 등록 (권장)

> **사전 조건:** `gh auth login` 완료 상태

```bash
# scripts/pe7/setup/register_secrets.sh 실행
bash scripts/pe7/setup/register_secrets.sh
```

또는 직접 입력:

```bash
gh secret set NOTION_TOKEN              -r GilbertKwak/prompt-engineering-system
gh secret set NOTION_KPI_DB_ID         -r GilbertKwak/prompt-engineering-system
gh secret set GOOGLE_SHEETS_ID         -r GilbertKwak/prompt-engineering-system
gh secret set GOOGLE_SERVICE_ACCOUNT_JSON -r GilbertKwak/prompt-engineering-system < gcp_sa_key.json
gh secret set OPENAI_API_KEY           -r GilbertKwak/prompt-engineering-system
gh secret set REDDIT_CLIENT_ID         -r GilbertKwak/prompt-engineering-system
gh secret set REDDIT_SECRET            -r GilbertKwak/prompt-engineering-system
gh secret set SLACK_WEBHOOK_URL        -r GilbertKwak/prompt-engineering-system
```

### 등록 확인
```bash
gh secret list -r GilbertKwak/prompt-engineering-system
```

예상 출력:
```
NOTION_TOKEN              Updated 2026-04-26
NOTION_KPI_DB_ID          Updated 2026-04-26
GOOGLE_SHEETS_ID          Updated 2026-04-26
GOOGLE_SERVICE_ACCOUNT_JSON Updated 2026-04-26
OPENAI_API_KEY            Updated 2026-04-26
REDDIT_CLIENT_ID          Updated 2026-04-26
REDDIT_SECRET             Updated 2026-04-26
SLACK_WEBHOOK_URL         Updated 2026-04-26
```

---

## 🔍 NOTION_TOKEN 확보 방법

```
1. https://www.notion.so/profile/integrations 접속
2. [New integration] → 이름: PE-7-Automation
3. Capabilities: Read/Update/Insert content 체크
4. [Submit] → Internal Integration Token 복사 (secret_xxx...)
5. 각 Notion 페이지에서 [...] → Connections → PE-7-Automation 연동
   └ PE-7 메인 페이지: 34955ed4-36f0-8114
   └ 허브 v2.0:      33955ed4-36f0-81cc
```

---

## 🌐 GOOGLE_SERVICE_ACCOUNT_JSON 확보 방법

```
1. console.cloud.google.com → IAM 및 관리자 → 서비스 계정
2. [서비스 계정 만들기] → 이름: pe7-automation
3. 역할: Google Sheets API 편집자 (또는 편집자)
4. [키 만들기] → JSON 키 다운로드 → gcp_sa_key.json
5. Google Sheets 문서에 해당 서비스 계정 이메일 공유 (편집자)
6. gh secret set GOOGLE_SERVICE_ACCOUNT_JSON < gcp_sa_key.json
   └ JSON 파일 전체를 문자열 값으로 Secret에 저장
```

---

## ⚠️ E-10 사전 방지 체크리스트

```bash
# 등록 전 필수 확인
python scripts/pe7/setup/verify_setup.py
```

| 항목 | 확인 내용 | 포트 |
|---|---|---|
| GitHub Actions 활성화 | Settings → Actions → Allow all | 포트 80 |
| Secrets 등록 | 8개 전체 UPDATED 표시 | 등록 UI |
| Notion 연동 | 통합 토큰 유효 | Notion API |
| GCP API 활성화 | Google Sheets API 켜지게 | GCP Console |
| Reddit App | script 타입 앱 등록 | reddit.com/prefs/apps |

---

*PE-7 v2.0 Secrets 등록 가이드 | Gilbert Kwak | 2026-04-26*
