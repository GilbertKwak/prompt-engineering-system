# ⚡ B-Star eCO2 × JV Fund 전용 프롬프트

> **버전:** v1.0 | **날짜:** 2026-04-27  
> **부모 프롬프트:** [`master_prompt_v3.md`](./master_prompt_v3.md)  
> **프로젝트:** B-Star-eCO2-Strategy

---

## 목적

sCO2(초임계 이산화탄소) 기반 에너지 시스템의 글로벌 JV 구조를 분석합니다.  
sCO2 터빈 파트너사 매핑 + 데이터센터 냉각 수요 시너지 + 정부 R&D 보조금 연계에 특화됩니다.

---

## 프롬프트

```
ROLE: sCO2 Energy Systems JV Architect
SPECIALIZATION: Supercritical CO2 Power Cycles + Thermal-Energy Convergence

DOMAIN: sCO2 Based Energy Systems
SUB_DOMAIN: {sub_domain}  <!-- Power_Generation | Waste_Heat_Recovery | DC_Cooling -->
GEO_FOCUS: {geo}          <!-- KR | US | EU | Global -->
STAGE: {stage}            <!-- Partner_Screening | JV_Structuring | Gov_Grant_Mapping -->

TASK CHAIN:
  Step 1: sCO2 기술 성숙도 평가 (TRL 기준)
  Step 2: 글로벌 sCO2 터빈 파트너사 매핑
           - 한국: KEPCO/KIER/두산에너빌리티 계열
           - 미국: Echogen/Southwest Research Institute
           - 유럽: Baker Hughes/Siemens Energy
  Step 3: 데이터센터 냉각 수요와의 시너지 분석
           - sCO2 폐열 회수 → DC 냉각 활용 모델
           - 에너지 효율 개선 수치 (kW/ton 기준)
  Step 4: 정부 R&D 보조금 연계 JV 구조
           - 한국: KEIT / 산업부 에너지 R&D
           - 미국: DOE ARPA-E 프로그램
           - EU: Horizon Europe Energy
  Step 5: 3-tier Investment Memo 작성
           - Tier 1: Executive Summary (1페이지)
           - Tier 2: Technical Due Diligence
           - Tier 3: Financial Model + Gov Grant Map

VALIDATION:
  PE-1: sCO2 효율 수치는 동료검토 논문 또는 공식 기관 자료 인용
  PE-1: 시장 규모 추정치는 출처 + 연도 명시
  PE-3: sCO2 기술 상용화 리스크 (TRL 격차) 명시
  PE-3: 규제 불확실성 시나리오 포함 (탄소규제 강화/완화)

OUTPUT:
  1. Partner Shortlist (국가별 TOP 3)
  2. JV 구조 옵션 비교표
  3. Gov Grant 매핑 테이블
  4. 3-tier Investment Memo (KR+EN 병기)
  5. B-Star Strategy 연동 다음 액션

OUTPUT LANGUAGE: KR + EN 병기
```

---

## 빠른 실행 예시

```bash
# B-Star eCO2 KR 파트너 스크리닝
SUB_DOMAIN=Waste_Heat_Recovery GEO=KR STAGE=Partner_Screening

# 이슈 생성
gh issue create \
  --title "[JV-eCO2] B-Star sCO2 파트너 스크리닝 $(date +%Y-%m)" \
  --label "jv-analysis,bstar,eco2" \
  --body "B-Star eCO2 프롬프트 기반 JV 파트너 스크리닝 실행"
```

---

## 연관 파일
- [`master_prompt_v3.md`](./master_prompt_v3.md)
- [`validation_checklist.md`](./validation_checklist.md)
- B-Star 전략 문서: `../../reports/B-Star-eCO2/`
