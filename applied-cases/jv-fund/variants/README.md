# JV Fund Domain Variants — variants/

<!-- Version: v3.6 | Date: 2026-04-28 | Base: master_prompt_v3.md -->

> **SSOT:** 이 폴더는 `master_prompt_v3.md` 기반의 도메인 특화 파생 프롬프트 3종을 관리합니다.  
> **Notion Hub:** [PE-JV · Global JV Fund Prompt Library v3.6](https://www.notion.so/34f55ed436f08150b07dc7f5f800311b)

---

## 📁 파일 구성

| 파일명 | 도메인 | 버전 | 설명 |
|---|---|---|---|
| `variant_01_fu_series.md` | HBM / Thermal Management | v3.6 | FU-Series 보고서 ↔ JV 타당성 연동 어댑터 |
| `variant_02_bstar_eco2.md` | sCO2 에너지 시스템 | v3.6 | B-Star eCO2 전략 전용 JV 분석 |
| `variant_03_ai_infra.md` | AI 데이터센터 열관리 | v3.6 | AI Infrastructure JV 파트너 스크리닝 |

---

## 🔗 연관 파일

- [`../master_prompt_v3.md`](../master_prompt_v3.md) — 마스터 프롬프트 (Base)
- [`../validation_checklist.md`](../validation_checklist.md) — PE-1/PE-3 검증 체크리스트
- [`../CHANGELOG.md`](../CHANGELOG.md) — 전체 변경 이력

---

## ⚡ 빠른 사용법

```bash
# Variant 01 — FU-Series 연동 분석 이슈 생성
gh issue create --title "[JV-VAR-01] FU-{FU_NUMBER} Feasibility" --label "jv-analysis,fu-series,variant"

# Variant 02 — B-Star eCO2 JV 분석 이슈 생성
gh issue create --title "[JV-VAR-02] B-Star eCO2 JV Screening" --label "jv-analysis,bstar,eco2,variant"

# Variant 03 — AI Infra 파트너 스크리닝 이슈 생성
gh issue create --title "[JV-VAR-03] AI-Infra Partner Shortlist" --label "jv-analysis,ai-infra,variant"

# 전체 variant 검증
python ../../automation/auto_validate.py --dir applied-cases/jv-fund/variants/ --rules PE-1,PE-3
```

---

## 📋 버전 이력

| 버전 | 날짜 | 변경 내용 |
|---|---|---|
| v3.6 | 2026-04-28 | variants/ 폴더 최초 생성 — 3종 전체 v3.6 기준 Full Spec 업로드 |
