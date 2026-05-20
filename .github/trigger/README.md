# Perplexity Trigger — MCP 직접 실행 가이드

## 개요

Perplexity MCP 도구(`push_files`)로 `run.json`을 수정·push하면
`perplexity-trigger.yml` 워크플로우가 자동 실행됩니다.

---

## 🚀 실행 방법 (Perplexity에서 직접)

### 방법 1 — run.json push (권장)

```json
// .github/trigger/run.json 을 아래 내용으로 push
{
  "_last_triggered": "<현재 시각 ISO8601>",
  "target_workflow": "weekly",
  "intel_scope": "standard",
  "force_ew_check": "false",
  "dry_run": "false"
}
```

`_last_triggered` 값을 매번 변경해야 GitHub가 diff를 감지합니다.

### 방법 2 — workflow_dispatch (MCP 도구 없이 GitHub UI)

GitHub Actions → `PE · Perplexity Trigger` → `Run workflow`

---

## 📋 파라미터 레퍼런스

| 파라미터 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `target_workflow` | `weekly` / `ew-emergency` | `weekly` | 실행할 워크플로우 |
| `intel_scope` | `standard` / `deep` / `emergency` | `standard` | 수집 깊이 (weekly 전용) |
| `force_ew_check` | `true` / `false` | `false` | EW 강제 재검사 |
| `ew_domain` | string | `enterprise_deployment` | EW 도메인 (ew-emergency 전용) |
| `ew_severity` | `MEDIUM` / `HIGH` / `CRITICAL` | `MEDIUM` | 심각도 |
| `ew_signals` | string (comma-sep) | `""` | EW 시그널 목록 |
| `dry_run` | `true` / `false` | `false` | 파라미터 검증만 (실행 안 함) |

---

## 🔐 필수 Secrets 등록

아래 Secrets는 GitHub 저장소 Settings → Secrets and variables → Actions에서 수동 등록 필요:

| Secret 이름 | 설명 | 등록 경로 |
|---|---|---|
| `PERPLEXITY_API_KEY` | Perplexity API 키 | [Settings → Secrets](https://github.com/GilbertKwak/prompt-engineering-system/settings/secrets/actions) |
| `NOTION_API_KEY` | Notion Integration 토큰 | 동일 경로 |

> `GITHUB_TOKEN`은 GitHub Actions가 자동 제공 — 별도 등록 불필요

---

## 📊 Variables (선택 등록)

Settings → Secrets and variables → Actions → Variables 탭:

| Variable 이름 | 기본값 | 설명 |
|---|---|---|
| `FORCE_MODEL` | `sonar-pro` | 기본 Perplexity 모델 |
| `DEFAULT_INTEL_SCOPE` | `standard` | 기본 수집 깊이 |

---

## ✅ 실행 확인

트리거 후 Actions 확인:
👉 https://github.com/GilbertKwak/prompt-engineering-system/actions
