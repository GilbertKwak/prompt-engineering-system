# PE-7 P4: SMR Power Pipeline — GitHub Actions

## 개요

`pe7_smr_pipeline.yml`은 `plugins/finance/` 경로의 SMR 관련 파일 변경 시
자동으로 실행되는 4-Job CI/CD 파이프라인입니다.

## 아키텍처

```
push to main
  └─ plugins/finance/smr_power_model.py  ←─ 트리거 경로
  └─ plugins/finance/smr_power_config.yaml
  └─ plugins/finance/smr_viz.py
  └─ plugins/finance/notion_chart_uploader.py
        │
        ▼
  [Job 1] smr-model          →  smr_power_model.py 실행
        │                       → Sheet 8~9 Excel 생성
        │                       → artifact upload (30d)
        ▼
  [Job 2] chart-gen          →  smr_viz.py 실행
        │                       → 5개 PNG 생성
        │                       → artifact upload (90d)
        ▼
  [Job 3] notion-upload      →  notion_chart_uploader.py 실행
        │                       → Notion 페이지에 이미지 블록 추가
        │                       → 실행 헤더 + 차트 섹션 자동 구성
        ▼
  [Job 4] notify             →  GitHub Step Summary 기록
                                → Slack 알림 (SLACK_WEBHOOK_URL 설정 시)
```

## 트리거 조건

| 트리거 | 조건 |
|--------|------|
| `push` | `main` 브랜치, `plugins/finance/**` 경로 변경 시 |
| `workflow_dispatch` | 수동 실행 (dry_run, smr_scenario 파라미터 지원) |

## Required Secrets

| Secret | 설명 |
|--------|------|
| `NOTION_TOKEN` | Notion Integration Token |
| `NOTION_SMR_PAGE_ID` | SMR 결과 업로드 대상 Notion 페이지 ID |
| `SLACK_WEBHOOK_URL` | (선택) Slack Incoming Webhook URL |

### Secrets 설정 방법

```bash
# GitHub CLI 사용
gh secret set NOTION_TOKEN --body "secret_xxxxx"
gh secret set NOTION_SMR_PAGE_ID --body "your-page-id-here"
gh secret set SLACK_WEBHOOK_URL --body "https://hooks.slack.com/..."
```

## Manual Dispatch 파라미터

| 파라미터 | 옵션 | 기본값 |
|---------|------|-------|
| `dry_run` | `true` / `false` | `false` |
| `smr_scenario` | `all` / `partial` / `full` / `grid_only` | `all` |

## 생성 파일

| 파일 | 경로 | Retention |
|------|------|-----------|
| Excel (Sheet 8~9) | `reports/AstraChips_SMR_Model_{ts}.xlsx` | 30일 |
| Charts (5 PNG) | `output/charts/*.png` | 90일 |
| Notion 업로드 결과 | `/tmp/notion_upload_result.json` | 런타임 |

## 로컬 테스트

```bash
# 모델만 실행
python plugins/finance/smr_power_model.py \
  --config plugins/finance/smr_power_config.yaml \
  --output reports/test_smr.xlsx

# 차트만 생성
python plugins/finance/smr_viz.py \
  --config plugins/finance/smr_power_config.yaml \
  --output-dir output/charts \
  --timestamp $(date +%Y%m%d_%H%M%S) \
  --version v1.2

# Notion 업로드 (dry-run)
python plugins/finance/notion_chart_uploader.py \
  --charts-dir output/charts \
  --page-id YOUR_PAGE_ID \
  --timestamp $(date +%Y%m%d_%H%M%S) \
  --version v1.2 \
  --token $NOTION_TOKEN \
  --dry-run

# 전체 파이프라인 시뮬레이션
python plugins/finance/smr_viz.py --config plugins/finance/smr_power_config.yaml --output-dir output/charts --timestamp test --version v1.2 && \
python plugins/finance/notion_chart_uploader.py --charts-dir output/charts --page-id PAGE_ID --timestamp test --version v1.2 --token $NOTION_TOKEN --dry-run
```

## Concurrency 설정

동일 브랜치의 중복 실행을 방지합니다:

```yaml
concurrency:
  group: smr-pipeline-${{ github.ref }}
  cancel-in-progress: true
```

## 버전 히스토리

| 버전 | 내용 | 날짜 |
|------|------|------|
| v1.0 | 최초 생성 (P4) | 2026-04-26 |
