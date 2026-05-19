# Section A Runbook — AI Intel Weekly Pipeline

## 파이프라인 아키텍처

```
Step 1: ai_intel_collector.py
  └─ Perplexity sonar/sonar-pro API
  └─ 7개 도메인 × N쿼리 → intel_all.json
  └─ exit 2 = EW flag (hard failure 아님)

Step 2: ai_ew_detector.py
  └─ 3-tier: collector_flag → threshold → keyword heuristic
  └─ ew_report.json (ew_triggered, severity, domains)

Step 3: kg_delta_generator.py
  └─ 21개 엔티티 카탈로그 매칭
  └─ EW 도메인별 전용 엣지 타입 삽입
  └─ knowledge_graph_vX.XX_delta.json → auto-commit

Step 4: notion_c31_updater.py
  └─ 50블록 배치 append (기존 내용 보존)
  └─ EW 심각도 → callout 색상 자동 변경
  └─ Notion page ID: 34a55ed4...
```

## GitHub Secrets 설정

**위치:** `Settings → Secrets and variables → Actions → New repository secret`

| Secret 이름 | 값 | 발급 위치 |
|---|---|---|
| `PERPLEXITY_API_KEY` | `pplx-xxxx` | [perplexity.ai/settings/api](https://perplexity.ai/settings/api) |
| `NOTION_API_KEY` | `secret_xxxx` | [notion.so/my-integrations](https://www.notion.so/my-integrations) |

**Notion Integration 연결 필수:**
C-31 페이지 → `...` → Connections → Integration 추가
(미설정 시 403 오류)

## 로컬 테스트

```bash
export PERPLEXITY_API_KEY="pplx-xxxx"
export NOTION_API_KEY="secret_xxxx"
mkdir -p output/ai_intel

# Step 1: 단일 도메인 테스트
python automation/ai_intel_collector.py \
  --domain enterprise_deployment \
  --week 2026-W21 \
  --scope standard \
  --output output/ai_intel/intel_enterprise.json

# Step 2: EW 탐지
python automation/ai_ew_detector.py \
  --input-dir output/ai_intel \
  --week 2026-W21 \
  --output output/ai_intel/ew_report.json

# Step 3: KG 델타
python automation/kg_delta_generator.py \
  --intel-dir output/ai_intel \
  --current-version 4.25 --next-version 4.26 \
  --week 2026-W21 --run-date 2026-05-20 \
  --ew-signals "" \
  --output knowledge_graph_v4.26_delta.json

# Step 4: Notion 업데이트
python automation/notion_c31_updater.py \
  --page-id 34a55ed436f0814d9cffe6a2f0816e29 \
  --week 2026-W21 --run-date 2026-05-20 \
  --ew-triggered false --ew-count 0 \
  --ew-signals "" --ew-severity NONE \
  --kg-version 4.26 --node-count 5 --edge-count 3 \
  --intel-dir output/ai_intel
```

## GitHub Actions 수동 실행

`Actions → PE · AI Intel Weekly Digest → Run workflow`
- `intel_scope`: standard (기본) / deep / emergency
- `force_ew_check`: false
- `kg_version_override`: 비워두면 자동 증가

## Exit Code 규칙

| 코드 | 의미 | 처리 |
|---|---|---|
| `0` | 정상 | 다음 스텝 진행 |
| `1` | 하드 실패 | 워크플로 중단 |
| `2` | EW 플래그 | 경고 로그, 워크플로 계속 |

## 트러블슈팅

**429 Rate Limit** → 자동 지수 백오프 (5s, 10s, 20s, 최대 3회)
**JSON 파싱 실패** → 마크다운 fence 제거 → 첫 `{}`블록 추출 → None 반환
**Notion 403** → Integration 연결 확인 (Connections 탭)
**EW 탐지 오탐** → `EW_KEYWORD_HIT_THRESHOLD` 값 상향 (기본 2)
