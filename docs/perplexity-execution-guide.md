# Perplexity MCP 실행 가이드

> 모든 로컬 Python 스크립트 → GitHub Actions로 래핑,  
> Perplexity MCP 도구(push_files)로 트리거 가능

---

## 아키텍처

```
[Perplexity MCP]
      │
      │ push_files → .github/trigger/run.json
      ▼
[perplexity-trigger.yml]  ← push 이벤트 감지
      │
      ├─ target: weekly    →  ai-intel-weekly.yml
      └─ target: ew-emergency → ai-intel-ew-emergency.yml
```

---

## 실행 시나리오

### 1. Weekly Intel 수집 (표준)

```json
{
  "_last_triggered": "2026-05-20T12:00:00+09:00",
  "target_workflow": "weekly",
  "intel_scope": "standard",
  "force_ew_check": "false",
  "dry_run": "false"
}
```

### 2. Deep Intel 수집

```json
{
  "_last_triggered": "2026-05-20T12:00:00+09:00",
  "target_workflow": "weekly",
  "intel_scope": "deep",
  "force_ew_check": "true",
  "dry_run": "false"
}
```

### 3. EW Emergency 탐지

```json
{
  "_last_triggered": "2026-05-20T12:00:00+09:00",
  "target_workflow": "ew-emergency",
  "ew_domain": "geopolitical_risk",
  "ew_severity": "HIGH",
  "ew_signals": "supply_chain_disruption,export_control",
  "dry_run": "false"
}
```

### 4. Dry Run (파라미터 검증만)

```json
{
  "_last_triggered": "2026-05-20T12:00:00+09:00",
  "target_workflow": "weekly",
  "intel_scope": "deep",
  "dry_run": "true"
}
```

---

## Secrets 설정 현황

| Secret | 상태 | 비고 |
|---|---|---|
| `PERPLEXITY_API_KEY` | 수동 등록 필요 | Perplexity API 대시보드에서 발급 |
| `NOTION_API_KEY` | 수동 등록 필요 | Notion Integration에서 발급 |
| `GITHUB_TOKEN` | 자동 제공 | 별도 등록 불필요 |

### 등록 URL
https://github.com/GilbertKwak/prompt-engineering-system/settings/secrets/actions

---

## 워크플로우 파일 구조

| 파일 | 트리거 | 역할 |
|---|---|---|
| `perplexity-trigger.yml` | push / workflow_dispatch | Perplexity MCP 진입점 |
| `ai-intel-weekly.yml` | workflow_dispatch | 주간 Intel 수집 메인 |
| `ai-intel-ew-emergency.yml` | workflow_dispatch | EW 긴급 탐지 |

---

## 주의사항

- `_last_triggered` 값은 매 트리거마다 변경 필수 (GitHub diff 감지용)
- Secrets 미등록 시 워크플로우가 API 호출 단계에서 실패함
- `dry_run: true`로 먼저 파라미터 검증 후 실제 실행 권장
