# 📋 TODO — Workflow 진행 항목 트래커
> 마지막 업데이트: 2026-05-20
> "진행해야할 항목" 명령 시 → **제목 + 진행항목** 자동 출력

---

## 🔴 [PENDING] ai-intel-ew-emergency.yml — EW 탐지 Job 구조 개선

### 현재까지 완료된 내용
- [x] `collect-intel` Job: step-level `env` 분리 (`PERPLEXITY_API_KEY` + `FORCE_MODEL`)
- [x] `ew-detection` Job: step-level `env` 분리 (`PERPLEXITY_API_KEY` + `FORCE_EW`)
- [x] `notion-update` Job: step-level `env` 분리 (`NOTION_API_KEY`)
- [x] `ai-intel-ew-emergency.yml` EW deep-collect Job의 step env 동일 방식 수정

### ⏳ 진행해야 할 항목

#### 1. `ai-intel-ew-emergency.yml` — workflow-level env → step-level env 전환
- **파일**: `.github/workflows/ai-intel-ew-emergency.yml`
- **대상**: 현재 `env:` 블록이 workflow 최상단(global)에 선언되어 있음
  ```yaml
  # 현재 (global env — 변경 전)
  env:
    PERPLEXITY_API_KEY: ${{ secrets.PERPLEXITY_API_KEY }}
    NOTION_API_KEY: ${{ secrets.NOTION_API_KEY }}
    PYTHONUNBUFFERED: "1"
  ```
- **목표**: 각 step이 실제로 사용하는 키만 step-level `env:`로 내려서 최소 권한 원칙 적용
  - `ew-deep-collect` job → `EW Deep Intel — sonar-pro` step에만 `PERPLEXITY_API_KEY`
  - `ew-notion-alert` job → `Update Notion C-31 with EW alert` step에만 `NOTION_API_KEY`
  - `PYTHONUNBUFFERED: "1"` → 모든 python 실행 step에 공통 추가
- **우선순위**: 🟡 MEDIUM

#### 2. `ai-intel-weekly.yml` — EW 탐지 Job step env 전환 검토
- **파일**: `.github/workflows/ai-intel-weekly.yml`
- **목표**: weekly 워크플로우 내 EW 탐지 관련 step도 동일한 step-level env 패턴 적용 여부 확인 및 수정
- **우선순위**: 🟡 MEDIUM

#### 3. Python 스크립트 — `automation/ai_intel_collector.py` EW 전용 파라미터 검토
- **파일**: `automation/ai_intel_collector.py`
- **목표**: `--scope deep` 옵션 동작 확인, EW 트리거 시 sonar-pro 모델 강제 지정 로직 보강
- **우선순위**: 🟢 LOW

#### 4. Python 스크립트 — `automation/kg_delta_generator.py` EW 시그널 처리 검토
- **파일**: `automation/kg_delta_generator.py`
- **목표**: `--ew-signals` 파라미터가 comma-separated 문자열로 전달될 때 파싱 로직 검증
- **우선순위**: 🟢 LOW

---

## 📌 진행 항목 요약 (빠른 참조)

| # | 제목 | 파일 | 우선순위 | 상태 |
|---|------|------|----------|------|
| 1 | EW Emergency workflow-level env → step-level 전환 | `ai-intel-ew-emergency.yml` | 🟡 MEDIUM | ⏳ 대기 |
| 2 | Weekly workflow EW Job step env 패턴 검토 | `ai-intel-weekly.yml` | 🟡 MEDIUM | ⏳ 대기 |
| 3 | `ai_intel_collector.py` EW scope deep / sonar-pro 보강 | `automation/ai_intel_collector.py` | 🟢 LOW | ⏳ 대기 |
| 4 | `kg_delta_generator.py` ew-signals 파싱 검증 | `automation/kg_delta_generator.py` | 🟢 LOW | ⏳ 대기 |

---

> 💡 다음 세션에서 "진행해야할 항목"이라고 명령하면 이 파일 기준으로 **제목 + 진행항목** 을 출력합니다.
