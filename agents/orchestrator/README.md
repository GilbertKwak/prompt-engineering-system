# 🎼 Orchestrator Agent

> PE-7 멀티에이전트 파이프라인 마스터 오케스트레이터

## 역할

전체 4단계 파이프라인을 순서대로 실행·모니터링합니다.

```
ai_intel_collector → ew_detector → kg_builder → notion_sync
```

## 실행

```bash
python agents/orchestrator/run_pipeline.py \
  --week 2026-W21 \
  --run-date 2026-05-20 \
  --scope standard
```

## 옵션

| 옵션 | 설명 | 기본값 |
|---|---|---|
| `--week` | ISO 주차 | 필수 |
| `--run-date` | 실행일 YYYY-MM-DD | 필수 |
| `--scope` | standard \| deep \| emergency | standard |
| `--domains` | 수집 도메인 목록 | 4개 전체 |
| `--skip-collect` | 수집 스킵 (기존 파일 재사용) | false |
| `--skip-notion` | Notion 동기화 스킵 | false |

## EW Emergency 모드

EW CRITICAL 감지 시 `--scope emergency` 로 재실행하면
자동으로 `sonar-pro` 모델로 전환됩니다.

## 로그

실행 요약 → `logs/orchestrator/pipeline_run_{week}_{date}.json`
