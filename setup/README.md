# setup/ — PE-7 초기 설정 스크립트

## 파일 목록

| 파일 | 용도 |
|---|---|
| `register_secrets.sh` | GitHub Secrets 5종 일괄 등록 |

## 사용법

```bash
# 1. 실행 권한 부여
chmod +x setup/register_secrets.sh

# 2. 실행 (대화형 입력)
./setup/register_secrets.sh
```

## 필요 준비물

1. `gh` CLI 설치 및 로그인
   ```bash
   brew install gh  # macOS
   gh auth login
   ```
2. GCP 서비스 계정 JSON 키 (`pe7-automation-xxxx.json`)
   - 기본 경로: `~/.config/pe7/service-account.json`
3. Slack App Incoming Webhook URL
4. Notion Integration Token
5. KPI Database ID (32자리)

## 참조

- Notion: [🔐 완전 자동화 Integration 설정 가이드](https://notion.so/34e55ed436f081d09a51fb6a95e5e6d6)
- GitHub Secrets: `Settings → Secrets and variables → Actions`
