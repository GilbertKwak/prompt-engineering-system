# 🔷 B-Star eCO2 JV Prompt v1.0

> **파일**: `prompts/jv_fund/bstar_eco2_v1.md`  
> **버전**: v1.0 | **날짜**: 2026-04-27  
> **도메인**: sCO2 Based Energy Systems | B-Star Strategy  
> **검증룰**: PE-1 + sCO2 TRL 레벨 명시

---

## [PURPOSE]

B-Star eCO2 전략 프레임워크 내에서 sCO2 기반 에너지 시스템의 JV 파트너십 분석 및 투자 메모 작성.

---

## [PARAMETERS]

```
- [APPLICATION]  : Power Generation | DC Cooling | Industrial Heat | Hybrid  (필수)
- [STAGE]        : Screening | Due Diligence | Structuring  (필수)
- [REGION]       : KR | US | EU | Global  (기본값: Global)
- [LANG]         : KR | EN | Bilingual  (기본값: Bilingual)
```

---

## [TASK CHAIN]

### Step 1 | sCO2 기술 현황
- TRL 레벨 (1~9) 명시
- 주요 기술 플레이어 (터빈 / 열교환기 / 제어계)
- 상용화 타임라인

### Step 2 | 데이터센터 냉각 시너지
- AI DC 폐열 활용 가능성
- sCO2 냉각 vs 기존 냉각 비용 비교
- 통합 시스템 ROI 분석

### Step 3 | 정부 지원 연계
- 한국: 탄소중립 R&D 지원사업
- 미국: DOE sCO2 프로그램
- EU: Horizon Europe 에너지 프로그램
- JV 구조에서 보조금 수령 전략

### Step 4 | 파트너 스크리닝

| 파트너 유형 | 한국 후보 | 해외 후보 |
|---|---|---|
| 터빈 제조사 | | |
| EPC 업체 | | |
| 유틸리티 기업 | | |
| 데이터센터 운영사 | | |

---

## [OUTPUT — 3-Tier Investment Memo]

### Tier 1 | Executive Summary (1 page)
```
- sCO2 JV 기회 요약
- 핵심 파트너 후보 (Top 2)
- 예상 IRR 범위 (est.)
- 권장 액션 3가지
```

### Tier 2 | Technical Feasibility (3 pages)
```
- TRL 레벨 및 기술 갭 분석
- 파일럿 → 상용화 로드맵
- 핵심 기술 리스크
```

### Tier 3 | Financial Model + Risk Matrix (2 pages)
```
- CAPEX / OPEX 추정 (est.)
- IRR / NPV 시나리오 (Base / Bull / Bear)
- 리스크 매트릭스 (5x5)
```

---

## [VALIDATION]

- [ ] sCO2 TRL 레벨 명시 (1~9)
- [ ] PE-1: 수치 출처 및 연도 기재
- [ ] Bearish Case (Bear Scenario) 포함
- [ ] 정부 보조금 연계 가능성 검토 완료
- [ ] KR/EN 병기 확인
