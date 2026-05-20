# Perplexity 직접 실행 가이드

> **영구 기억**: 모든 로컬 Python 스크립트는 GitHub Actions로 래핑하여
> Perplexity MCP 도구(`push_files`)로 트리거 가능합니다.

---

## 사전 등록 필수 Secrets (GitHub Repo Settings → Secrets)

| Secret 이름 | 필요한 워크플로우 | 용도 |
|---|---|---|
| `PERPLEXITY_API_KEY` | ai-intel-weekly.yml, ai-intel-ew-emergency.yml | Perplexity AI 인텔 수집 |
| `NOTION_API_KEY` | ai-intel-weekly.yml, ai-intel-ew-emergency.yml | Notion C-31 업데이트 |
| `NOTION_C31_PAGE_ID` | ai-intel-weekly.yml | Notion 페이지 ID (선택) |

> **GITHUB_TOKEN**은 Actions에서 자동 제공 — 별도 등록 불필요

---

## Perplexity에서 실행하는 3가지 방법

### 방법 1: push_files로 run.json 수정 (가장 간단)

`.github/trigger/run.json` 파일을 수정하면 `perplexity-trigger.yml`이 자동 실행됩니다.

**Weekly Standard 실행:**
```json
{
  "target_workflow": "weekly",
  "intel_scope": "standard",
  "force_ew_check": "false",
  "dry_run": "false",
  "triggered_by": "perplexity",
  "triggered_at": "2026-05-20T12:00:00+09:00"
}
```

**EW Emergency 실행:**
```json
{
  "target_workflow": "ew-emergency",
  "ew_domain": "enterprise_deployment",
  "ew_severity": "HIGH",
  "ew_signals": "supply_shock,export_control",
  "dry_run": "false",
  "triggered_by": "perplexity",
  "triggered_at": "2026-05-20T12:00:00+09:00"
}
```

### 방법 2: Perplexity가 직접 dispatch (MCP 확장 시)

GitHub Actions URL:
- Weekly: `https://github.com/GilbertKwak/prompt-engineering-system/actions/workflows/ai-intel-weekly.yml`
- EW Emergency: `https://github.com/GilbertKwak/prompt-engineering-system/actions/workflows/ai-intel-ew-emergency.yml`
- Perplexity Trigger: `https://github.com/GilbertKwak/prompt-engineering-system/actions/workflows/perplexity-trigger.yml`

### 방법 3: Dry Run (파라미터 검증만)

`dry_run: "true"` 설정 → 실제 실행 없이 파라미터 확인

---

## 현재 등록 상태 체크리스트

```
□ PERPLEXITY_API_KEY  → GitHub Repo → Settings → Secrets → Actions
□ NOTION_API_KEY      → GitHub Repo → Settings → Secrets → Actions  
□ NOTION_C31_PAGE_ID  → GitHub Repo → Settings → Secrets → Actions (선택)
```

**등록 URL**: https://github.com/GilbertKwak/prompt-engineering-system/settings/secrets/actions

---

## 실행 플로우 다이어그램

```
Perplexity MCP
    │
    ├─ push_files(.github/trigger/run.json)
    │       │
    │       └─► perplexity-trigger.yml (자동 실행)
    │                   │
    │                   ├─► ai-intel-weekly.yml
    │                   └─► ai-intel-ew-emergency.yml
    │
    └─ 직접 workflow_dispatch (MCP GitHub API)
            │
            └─► 해당 워크플로우 직접 실행
```

---

## 주의사항

1. **Secret 값은 Perplexity에서 직접 설정 불가** — GitHub 웹 UI에서 직접 등록
2. `triggered_at` 값을 현재 시각으로 변경해야 push 이벤트 감지됨 (파일 내용이 달라야 함)
3. `dry_run: "false"` 설정 필수 (기본값은 `"true"` — 안전 장치)
