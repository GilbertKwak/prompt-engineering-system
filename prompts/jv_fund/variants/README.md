# JV Fund — Domain Variants 디렉터리

> **Parent Prompt:** `../master_prompt_v3.md`  
> **생성일:** 2026-04-28  
> **Author:** Gilbert Kwak  
> **상태:** Active

---

## 개요

이 디렉터리는 **Global JV Fund Master Prompt v3**의 도메인별 파생(Variant) 프롬프트를 관리합니다.  
각 Variant는 Master Prompt의 구조(SYSTEM ROLE / CONTEXT PARAMETERS / TASK CHAIN / OUTPUT FORMAT / VALIDATION)를 계승하되,  
특정 사업 도메인에 최적화된 세부 분석 체계를 제공합니다.

---

## Variant 목록

| 파일 | 도메인 | 연결 레포 | 상태 |
|------|--------|-----------|------|
| [`variant_A_fu_series.md`](./variant_A_fu_series.md) | HBM Salvage / 반도체 열관리 (FU-Series) | `fu-semiconductor-thermal`, `HBM-Salvage-Value-Program` | ✅ Active |
| [`variant_B_bstar_eco2.md`](./variant_B_bstar_eco2.md) | sCO₂ 기반 에너지 시스템 (B-Star) | `B-Star-eCO2-Strategy`, `sCO2-Hub-IR-Docs` | ✅ Active |
| [`variant_C_ai_infra.md`](./variant_C_ai_infra.md) | AI 인프라 데이터센터 열관리 | `global-semiconductor-ai-research`, `AstraChips-Strategy` | ✅ Active |

---

## 사용 방법

### 기본 사용
```bash
# Variant A 사용 (FU-Series 연동)
# 1. FU 보고서 번호 지정
export FU_NUMBER="FU-015"
export STAGE="Due Diligence"
# 2. 프롬프트 파일 참조 후 AI에 입력
cat prompts/jv_fund/variants/variant_A_fu_series.md

# Variant B 사용 (B-Star eCO₂)
export PHASE="Pilot"
export APP="DataCenter"
cat prompts/jv_fund/variants/variant_B_bstar_eco2.md

# Variant C 사용 (AI Infrastructure)
export TECH="Hybrid"
export DC_TYPE="Hyperscale"
cat prompts/jv_fund/variants/variant_C_ai_infra.md
```

### GitHub Issue 생성 (각 Variant 실행 후)
```bash
# Variant A 실행 후 이슈 생성
gh issue create \
  --repo GilbertKwak/fu-semiconductor-thermal \
  --title "[JV] FU-${FU_NUMBER} 기반 JV 타당성 분석" \
  --label "jv-analysis,fu-series"

# Variant B 실행 후 이슈 생성
gh issue create \
  --repo GilbertKwak/B-Star-eCO2-Strategy \
  --title "[JV] B-Star sCO2 JV 구조 설계" \
  --label "jv-structure,eco2"

# Variant C 실행 후 이슈 생성
gh issue create \
  --repo GilbertKwak/global-semiconductor-ai-research \
  --title "[JV] AI IDC 열관리 JV 분석" \
  --label "jv-analysis,ai-infra"
```

---

## 버전 관리 규칙

- **Minor Update (v1.x):** 파트너사 정보, 시장 데이터 업데이트
- **Major Update (v2.0):** 구조 변경, 새 Task Chain 추가
- 모든 변경은 `CHANGELOG.md` (루트) 및 각 파일 하단 버전 기록에 반영

---

## 검증 기준

| 규칙 | 기준 | 적용 Variant |
|------|------|-------------|
| PE-1 | 출처 명시, 수치 연도 기재, 추정값 `(est.)` | A, B, C 전체 |
| PE-3 | 반대 시나리오(Bear Case) 1개 이상 포함 | A, B, C 전체 |

---

*JV Fund Variants README | v1.0 | 2026-04-28 | Gilbert Kwak*
