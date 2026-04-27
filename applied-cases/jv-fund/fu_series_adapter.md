# 🔬 FU-Series × JV Fund 연동 프롬프트

> **버전:** v1.0 | **날짜:** 2026-04-27  
> **부모 프롬프트:** [`master_prompt_v3.md`](./master_prompt_v3.md)  
> **대상 보고서:** FU-001 ~ FU-025+

---

## 목적

FU-Series 기술 보고서의 시장분석/기술사양 섹션을 JV 타당성 분석에 자동 연결합니다.  
기술 데이터 → 투자 의사결정 브리지 역할을 수행합니다.

---

## 프롬프트

```
ROLE: JV Fund Analyst with FU-Series Technical Data Integration

CONTEXT:
  - Source Report: FU-Series #{FU_NUMBER} — {REPORT_TITLE}
  - Target Section: {SECTION}  <!-- Market_Analysis | Technical_Specs | Cost_Model -->
  - JV Stage: {JV_STAGE}       <!-- Screening | Due_Diligence -->

INPUT:
  아래 FU 보고서 섹션 내용을 그대로 붙여넣기:
  [FU 보고서 내용 삽입]

TASK CHAIN:
  Step 1: FU 보고서에서 시장 규모/성장률 수치 추출
  Step 2: 핵심 기술 사양을 JV 파트너 필요 역량으로 변환
  Step 3: JV 타당성 스코어 산출 (0-100)
           - 시장 매력도 (0-30)
           - 기술 시너지 (0-30)
           - 파트너 가용성 (0-20)
           - 규제 환경 (0-20)
  Step 4: 파트너사 후보 TOP 3 도출
  Step 5: 권장 JV 구조 초안 (지분/거버넌스)

VALIDATION:
  - PE-1: FU 보고서 수치 그대로 인용 (수정 금지)
  - PE-3: FU 기술 리스크를 JV 리스크 매트릭스에 반영

OUTPUT FORMAT:
  1. JV Screening Score Card (테이블)
  2. Partner Shortlist TOP 3
  3. Notion 업데이트 블록 (MD 형식)
  4. GitHub PR 본문 초안
  5. 다음 단계 권장 액션

OUTPUT LANGUAGE: KR + EN 병기
```

---

## 빠른 실행 예시

```bash
# FU-015 Thermal 보고서 연동 JV 분석
FU_NUMBER=015 SECTION=Market_Analysis JV_STAGE=Screening

# 이슈 생성
gh issue create \
  --title "[JV-FU] FU-${FU_NUMBER} 연동 JV Screening" \
  --label "jv-analysis,fu-series" \
  --body "FU-$(FU_NUMBER) 보고서 기반 JV 타당성 분석 요청"
```

---

## 연관 파일
- [`master_prompt_v3.md`](./master_prompt_v3.md)
- [`validation_checklist.md`](./validation_checklist.md)
- FU-Series 보고서: `../../reports/FU-Series/`
