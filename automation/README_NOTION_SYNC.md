# GitHub Actions → Notion PE Hub 자동 동기화 파이프라인

## 아키텍처

```
[GitHub push / workflow_dispatch]
         │
         ▼
┌──────────────────────────────────────────────┐
│  Job 1: run-pe-scripts                        │
│  ┌────────────┐ ┌────────────┐ ┌───────────┐ │
│  │ PE-FIN     │ │ PE-CON     │ │ PE-IP     │ │
│  │ financial  │ │ context    │ │ ip_engine │ │
│  │ _bridge.py │ │ _engine.py │ │ .py       │ │
│  └─────┬──────┘ └─────┬──────┘ └─────┬─────┘ │
│        └──────────────┴──────────────┘        │
│                       │ JSON artifacts        │
└───────────────────────┼──────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│  Job 2: push-to-notion                        │
│  automation/notion_pe_push.py                 │
│  - Upsert (run_id + engine 멱등성 보장)       │
│  - 3-Engine 결과 → Notion DB 레코드           │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
              Notion PE Hub DB
         ┌─────────────────────────┐
         │ Engine │ Status │ IRR   │
         │ PE-FIN │ ✅ OK  │ 48.3% │
         │ PE-CON │ ✅ OK  │ —     │
         │ PE-IP  │ ✅ OK  │ —     │
         └─────────────────────────┘
```

## 설정 방법 (5단계)

### 1. Notion Integration 생성
1. https://www.notion.so/my-integrations → **New integration**
2. 이름: `PE Hub GitHub Sync`
3. Capabilities: **Read content**, **Update content**, **Insert content** 체크
4. **Submit** → `Internal Integration Secret` 복사 (= `NOTION_TOKEN`)

### 2. Notion DB 연결
1. PE Hub 데이터베이스 열기
2. 우상단 `...` → **Connections** → 방금 만든 Integration 추가
3. DB URL에서 ID 복사:
   `https://notion.so/workspace/페이지명-{DB_ID}?v=...`
   → `DB_ID` 32자리 (= `NOTION_PE_HUB_DB_ID`)

### 3. Notion DB 스키마 확인
`notion_pe_push.py`의 `build_properties()`에서 사용하는 속성명:

| Notion 속성명 | 타입 | 설명 |
|---|---|---|
| `Name` | Title | `[엔진] Run ID` 형식 |
| `Engine` | Select | PE-FIN / PE-CON / PE-IP |
| `Status` | Select | OK / ERROR / SKIPPED |
| `Run ID` | Text | 실행 ID (멱등성 키) |
| `Synced At` | Date | Push 시각 (UTC) |
| `IRR (%)` | Number | PE-FIN 전용 |
| `NPV ($M)` | Number | PE-FIN 전용 |
| `CAPEX ($M)` | Number | PE-FIN 전용 |

> DB에 없는 속성은 Notion API가 자동 무시합니다. 필요한 컬럼만 생성하세요.

### 4. GitHub Secrets 등록
```
Settings > Secrets and variables > Actions > New repository secret

NOTION_TOKEN          = secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_PE_HUB_DB_ID  = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  (하이픈 없는 32자리)
```

### 5. 트리거
```bash
# 방법 A: scripts/ 폴더 파일 수정 후 push → 자동 실행
git add scripts/financial_bridge_v1.py && git commit -m "update" && git push

# 방법 B: GitHub UI → Actions → 🔄 Notion PE Hub Sync → Run workflow
#   engine: all | fin | con | ip
#   dry_run: true (Notion Push 생략, 스크립트만 실행)
```

## scripts/ 결과 JSON 포맷

`financial_bridge_v1.py` 등 scripts/ 하위 스크립트는
`--output_json` 인자를 받아 아래 형식으로 저장해야 합니다:

```json
{
  "engine": "PE-FIN",
  "status": "ok",
  "irr": 0.483,
  "npv": 6864.9,
  "capex": 2500,
  "scenarios": {
    "bull": "IRR 62.0%",
    "base": "IRR 48.3%",
    "bear": "IRR 32.9%"
  }
}
```

status가 `"ok"`이면 Notion에 정상 수치 기재,
`"error"`이면 오류 메시지만 기재합니다.

## 로컬 테스트

```bash
export NOTION_TOKEN=secret_xxx
export NOTION_PE_HUB_DB_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 결과 파일 직접 생성 후 Push 테스트
mkdir -p output/notion-sync
echo '{"engine":"PE-FIN","status":"ok","irr":0.483,"npv":6864.9,"capex":2500}' \
  > output/notion-sync/pe_fin_result.json

python automation/notion_pe_push.py \
  --results_dir output/notion-sync/ \
  --run_id run-local-test \
  --engine_scope fin
```
