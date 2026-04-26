# PE-7 v2.0 — 수동 실행 런북 + 스케줄 컨필보드

> **Gilbert Kwak** | 2026-04-26 | PE-7 v2.0 전체 워크플로우 실행 기준

---

## 🚀 워크플로우 3종 현황

| 워크플로우 | 파일 | 트리거 | 실행 시간 |
|---|---|---|---|
| 일달리 파이프라인 | `pe7_daily_pipeline.yml` | Cron + 수동 | 매일 UTC 23:00 (KST 08:00) |
| 월간 리포트 | `pe7_monthly_report.yml` | Cron + 수동 | 매월 28일 UTC 22:00 |
| E-0N 검증 | `pe7_e0n_validate.yml` | Push/PR + 수동 | 실시간 (Push 시자동) |

---

## 🧪 Step 1 — pe7_e0n_validate.yml 첫 수동 실행

### 방법 A: GitHub 웹 UI (가장 간단)

```
1. https://github.com/GilbertKwak/prompt-engineering-system/actions 접속
2. 왼쪽 사이드바: [PE-7 E-0N Validation] 클릭
3. [▶ Run workflow] 버튼 클릭
4. Branch: main 확인
5. [Run workflow] 실행
6. 실행 화면에서 로그 모니터링
```

### 방법 B: gh CLI

```bash
# 수동 실행
gh workflow run pe7_e0n_validate.yml -R GilbertKwak/prompt-engineering-system

# 실행 상태 모니터링
gh run list -R GilbertKwak/prompt-engineering-system --workflow=pe7_e0n_validate.yml

# 로그 실시간 보기
gh run watch -R GilbertKwak/prompt-engineering-system
```

### 예상 실행 흐름

```
[1/5] 검증 환경 설정 (Python 3.11 + deps)       ~30초
[2/5] E-0N 통합 검증 실행                           ~60초
      ├─ A-1 syntax/import/fallback/output ✅
      ├─ B-1 syntax/import/E-08/fallback  ✅
      ├─ B-3 syntax/import/fallback/demo  ✅
      ├─ C-2 syntax/import/E-03/output    ✅
      ├─ C-3 syntax/import/E-03/E-07      ✅
      └─ D-2 syntax/import/E-07/output    ✅
[3/5] PE-3 리포트 생성 → reports/E0N_Validation_*.md  ~10초
[4/5] Notion SSOT 업데이트 (PE-7 + 허브 v2.0)       ~15초
[5/5] GitHub 리포트 아티팩트 업로드               ~10초

종료: 하이라이트는 'logs/e0n_validation_*.json'
        리포트 파일: 'reports/E0N_Validation_*.md'
```

### E-0N 검증 실패 시 대응

```
❌ FAIL 발생 시:
  1. Actions 탭에서 오류 로그 확인
  2. 해당 스크립트 파일 직접 점검
  3. 수동 실행 후 fallback 동작 확인

⚠️ WARN 시:
  → 스크립트 미실행 상태 (WARN = 누락, FAIL = 오류)
  → CI/CD는 통과하지만 Slack 알림 전송
```

---

## ⏰ Step 2 — pe7_daily_pipeline.yml Cron 시간 확인

```yaml
# .github/workflows/pe7_daily_pipeline.yml 내 Cron 설정
on:
  schedule:
    - cron: '0 23 * * *'   # UTC 23:00 = KST 08:00
  workflow_dispatch:        # 수동 실행 트리거
```

### KST 08:00 자동 실행 평일 예시 (4월 27일)

```
[KST 08:00] pe7_daily_pipeline.yml 시작
  ├─ Job 1: collect_data
  │     ├─ A-1 sheets_exporter.py     → data/sheets_export_20260427.csv
  │     ├─ B-1 supply_chain_collector.py → data/supply_chain_20260427.json
  │     └─ B-3 sentiment_analyzer.py  → data/sentiment_20260427.json
  ├─ Job 2: optimize_portfolio
  │     ├─ C-2 markowitz.py           → data/markowitz_result_20260427.json
  │     └─ C-3 black_litterman.py     → data/black_litterman_20260427.json
  ├─ Job 3: validate_e0n
  │     └─ e0n_integration_test.py    → logs/e0n_validation_20260427.json
  └─ Job 4: notify
        └─ Slack: "🟢 [PE-7] 20260427 자동 실행 완료"
```

### 수동 실행 (Dry-run 테스트)

```bash
gh workflow run pe7_daily_pipeline.yml \
  -R GilbertKwak/prompt-engineering-system \
  -f run_mode=test
```

---

## 📅 Step 3 — pe7_monthly_report.yml 스케줄

```yaml
on:
  schedule:
    - cron: '0 22 28-31 * *'  # 매월 28~31일 UTC 22:00
  workflow_dispatch:
```

### 월간 리포트 생성 흐름

```
매월 말 UTC 22:00 (KST 07:00)
  ├─ collect_monthly_data: data/*.csv + data/*.json 월별 취합
  ├─ generate_ppt: D-2 monthly_ppt_gen.py
  │     └─ reports/Monthly_Review_2026MM.pptx (5슬라이드)
  ├─ upload_artifact: GitHub Release v2026.MM
  └─ notify_slack: "📊 월간 리포트 생성 완료"
```

---

## 📊 실행 전 사전 점검 체크리스튨

```bash
# 전체 점검 스크립트 실행
python scripts/pe7/setup/verify_setup.py
```

| # | 점검 항목 | 명령 | 예상 결과 |
|---|---|---|---|
| 1 | Python 3.11+ | `python --version` | Python 3.11.x |
| 2 | 필수 패키지 | `pip check` | 오류 없음 |
| 3 | gh CLI 로그인 | `gh auth status` | ✅ Logged in |
| 4 | Secrets 8개 | `gh secret list` | 8줄 출력 |
| 5 | Workflows 활성화 | `gh workflow list` | 4개 활성 |
| 6 | Notion 연결 | `verify_setup.py` | HTTP 200 |
| 7 | 스크립트 존재 | `ls scripts/pe7/` | 6개 .py 파일 |
| 8 | 워크플로우 | `ls .github/workflows/` | 4개 .yml |

---

## 🔔 Slack 알림 예시

```
🟢 [PE-7 Daily] 2026-04-27 성공
│ 데이터 수집: ✅ 3개 스크립트 완료
│ 포트폴리오 최적화: ✅ C-2/C-3 완료
│ E-0N 검증: 🟢 ALL PASS (6/6)
└ 상세: https://github.com/GilbertKwak/prompt-engineering-system/actions

🟡 [PE-7 Daily] 2026-04-28 주의
│ B-3 sentiment_analyzer: WARN (Reddit 스로 저하 → demo data 사용)
└ 조치 필요: Reddit API 할당량 확인
```

---

## 📈 실행 성공 기준 (PE-3 검증)

| 지표 | 목표 | 실패 기준 |
|---|---|---|
| E-0N PASS율 | 100% (6/6) | 하나라도 FAIL 시 정지 |
| Secrets 등록 | 8/8 | 하나라도 누락 시 E-10 태깅 |
| 워크플로우 활성화 | 3/3 | 비활성 시 수동 활성화 |
| Notion 연결 | 2개 페이지 | 콘텍스트 업데이트 성공 |
| 첫 실행 완료 | < 5분 | timeout 시 E-05 코드 |

---

*PE-7 v2.0 런북 매뉴얼 | Gilbert Kwak | 2026-04-26*
