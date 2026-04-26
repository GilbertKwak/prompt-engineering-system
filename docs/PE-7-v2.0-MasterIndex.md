# PE-7 v2.0 — 마스터 인덱스 (SSOT 기준)

> **최종 업데이트:** 2026-04-26 10:13 KST | **코립:** `f39c8d52` | **상태:** 프로덕션 ✅

---

## 📋 전체 파일 맵

### 핵심 스크립트 (6개)

| 파일 | Track | 위치 | E-0N |
|---|---|---|---|
| `sheets_exporter.py` | A-1 | `scripts/pe7/` | E-05 |
| `supply_chain_collector.py` | B-1 | `scripts/pe7/` | E-05, E-08 |
| `sentiment_analyzer.py` | B-3 | `scripts/pe7/` | E-05 |
| `markowitz.py` | C-2 | `scripts/pe7/` | E-03 |
| `black_litterman.py` | C-3 | `scripts/pe7/` | E-03, E-07 |
| `monthly_ppt_gen.py` | D-2 | `scripts/pe7/` | E-07 |

### 검증 시스템 (3개)

| 파일 | 역할 | 위치 |
|---|---|---|
| `e0n_integration_test.py` | E-0N 통합검증 | `scripts/pe7/validate/` |
| `notion_ssot_updater.py` | Notion SSOT 자동반영 | `scripts/pe7/validate/` |
| `validation_report_gen.py` | PE-3 리포트 생성 | `scripts/pe7/validate/` |

### 셀티 스크립트 (3개)

| 파일 | 역할 | 위치 |
|---|---|---|
| `register_secrets.sh` | Secrets 일괄 등록 | `scripts/pe7/setup/` |
| `verify_setup.py` | 실행 전 사전 점검 | `scripts/pe7/setup/` |

### GitHub Actions 워크플로우 (4개)

| 파일 | 트리거 | KST 실행 시간 |
|---|---|---|
| `pe7_daily_pipeline.yml` | Cron + 수동 | 매일 08:00 |
| `pe7_monthly_report.yml` | Cron + 수동 | 매월 말 07:00 |
| `pe7_e0n_validate.yml` | Push/PR + 수동 | 실시간 |
| `build_kg.yml` | Push | 실시간 |

### 문서 (5개)

| 파일 | 내용 |
|---|---|
| `PE-7-v2.0-Section6-ValidationReport.md` | E-0N 섹션 6 완료 보고서 |
| `PE-7-NextSteps-SecretsGuide.md` | Secrets 8개 등록 가이드 |
| `PE-7-RunbookManual.md` | 수동 실행 런북 + 스케줄 |
| `PE-7-v2.0-MasterIndex.md` | 마스터 인덱스 (SSOT) |
| `PE-7-v2.0-6gae-seukeuribteu-wanjeon-guhyeon-bangan.md` | 원본 심층 프롬프트 |

---

## 📊 실행 수순 (Next Steps 기준)

```
Step 1: bash scripts/pe7/setup/register_secrets.sh     # Secrets 8개 등록
Step 2: python scripts/pe7/setup/verify_setup.py       # 사전 점검
Step 3: gh workflow run pe7_e0n_validate.yml            # 첫 수동 검증
Step 4: gh workflow run pe7_daily_pipeline.yml          # 데일리 테스트
Step 5: 매일 KST 08:00 Slack 알림 확인
```

---

## 📌 Notion SSOT 연결

| 페이지 | ID | URL |
|---|---|---|
| PE-7 메인 | `34955ed4-36f0-8114` | https://www.notion.so/34955ed436f081149dd6de25dba027d7 |
| 허브 v2.0 | `33955ed4-36f0-81cc` | https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b |

---

## ✅ 세션 완료 체크리스트

- [x] 셀르 1: `sheets_exporter.py` 구현
- [x] 셀르 2: `supply_chain_collector.py` 구현
- [x] 셀르 3: `sentiment_analyzer.py` 구현
- [x] 셀르 4: `markowitz.py` 구현
- [x] 셀띴 5: `black_litterman.py` 구현
- [x] 셀르 6: `monthly_ppt_gen.py` 구현
- [x] 셀르 7: GitHub Actions 3종
- [x] 셀르 8: E-0N 통합검증 + Notion SSOT
- [x] **Next Steps: Secrets 가이드 + 런북 + verify_setup.py**

> 🎉 **PE-7 v2.0 전체 구현 + 듰스타팡 100% 완료**

---
*PE-7 v2.0 마스터 인덱스 | GitHub SSOT | Gilbert Kwak | 2026-04-26*
