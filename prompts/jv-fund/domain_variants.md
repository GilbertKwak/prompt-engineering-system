# Global JV Fund — Domain Variants (파생 프롬프트 3종)

> **버전:** v1.0 | **날짜:** 2026-04-28  
> **부모 파일:** master_prompt_v3_optimized.md  
> **용도:** 특화 도메인별 즉시 적용 가능한 파생 프롬프트

---

## Variant A: FU-Series 연동 프롬프트

> **대상:** fu-semiconductor-thermal 레포 / HBM·열관리 FU 보고서 연동

```
[ROLE]
글로벌 JV 펀드 분석가 (반도체 열관리 전문)

[CONTEXT]
- 연동 보고서: FU-Series #{FU_NUMBER} (예: FU-008, FU-012)
- 분석 섹션: "Market Analysis" 또는 "Technical Specifications"
- 목적: FU 보고서 데이터 기반 JV 타당성 재검증

[TASK]
1. FU 보고서의 시장 데이터를 JV 펀드 사이징에 적용
2. 기술 파트너 후보 (OSAT/소재/장비) 매핑
3. IP 소유권 구조 설계 (한국 R&D Co + 싱가포르 HoldCo)
4. 투자 회수 경로 (M&A / IPO / 라이선싱) 시나리오 분석

[OUTPUT]
- Notion 페이지 업데이트용 MD 포맷
- GitHub PR 본문 초안
- 다음 FU 보고서 연계 액션 아이템 3개

[VALIDATION]
- PE-1: FU 보고서 섹션 및 페이지 번호 인용
- PE-3: 기술 상용화 실패 시나리오 포함
```

**적용 레포:** [fu-semiconductor-thermal](https://github.com/GilbertKwak/fu-semiconductor-thermal)

---

## Variant B: B-Star eCO2 전용 프롬프트

> **대상:** B-Star-eCO2-Strategy 레포 / sCO2 기반 JV 전략

```
[ROLE]
sCO2 에너지 시스템 상용화 전략가 + JV 펀드 설계 전문가

[CONTEXT]
- 도메인: sCO2 소형 분산형 발전·냉각 시스템
- 시장: 한국 데이터센터 + 산업용 폐열 회수
- 전략 레포: B-Star-eCO2-Strategy (Ch.1~)

[TASK]
1. sCO2 터빈 파트너사 매핑 (한국/미국/유럽 Top 5)
2. 데이터센터 냉각 수요와 sCO2 시스템 시너지 정량화
3. 정부 R&D 보조금 연계 JV 구조 설계
   (산업부 / KEIT / 에너지기술평가원)
4. 3-Tier 투자 구조:
   Tier-1: 기술 개발 (공공 R&D)
   Tier-2: 파일럿 사업화 (전략적 LP)
   Tier-3: 스케일업 (기관 LP)

[OUTPUT]
- 3-Tier Investment Memo (KR/EN 병기)
- LP 피치용 1페이지 요약
- 6개월 실행 로드맵

[VALIDATION]
- PE-1: sCO2 시장 규모 출처 명시 (IEA / BloombergNEF / 한국에너지공단)
- PE-3: 기술 경쟁자 등장 시 대응 전략 포함
```

**적용 레포:** [B-Star-eCO2-Strategy](https://github.com/GilbertKwak/B-Star-eCO2-Strategy)

---

## Variant C: AI Infrastructure JV 프롬프트

> **대상:** AstraChips-Strategy 레포 / AI 데이터센터 열관리 JV

```
[ROLE]
AI 인프라 투자 전문가 + 반도체 열관리 기술 분석가

[CONTEXT]
- 도메인: AI 가속기 (GPU/NPU) + HBM 패키지 열관리
- 시장: 글로벌 AI 데이터센터 냉각 솔루션
- 회사: AstraChips (Singapore HoldCo → Korea R&D → US Sales)

[TASK]
1. AI 데이터센터 열관리 시장 규모 분석
   (2024~2030 CAGR, TAM $XXB)
2. 전략적 파트너 후보 매핑:
   - Tier-1 CSP (AWS/Azure/GCP) 공급망 진입 전략
   - OSAT 파트너 (ASE/Amkor/JCET)
   - TIM 소재 공급사 (Honeywell/Indium/Shin-Etsu)
3. JV 구조:
   - Singapore HoldCo 중심 지주 구조
   - Korea R&D Co IP 소유권 설계
   - US Sales Co 수익 분배 메커니즘
4. 펀드 사이징:
   - Series A: $10-30M (기술 검증)
   - Series B: $50-100M (양산 준비)
   - 전략적 LP: 삼성전자벤처투자/SK하이닉스벤처스/TSMC

[OUTPUT]
- Executive Summary (영문, LP-facing)
- 기술 Due Diligence 체크리스트
- 3년 재무 모델 프레임 (매출/EBITDA/IRR 가정)

[VALIDATION]
- PE-1: AI 서버 시장 데이터 출처 (IDC / Gartner / Dell'Oro)
- PE-3: AI 투자 버블 붕괴 시나리오 포함
```

**적용 레포:** [AstraChips-Strategy](https://github.com/GilbertKwak/AstraChips-Strategy)

---

## 파생 프롬프트 선택 가이드

| 상황 | 사용 프롬프트 |
|---|---|
| FU 보고서 작성 후 JV 타당성 검토 | Variant A |
| B-Star eCO2 투자자 미팅 준비 | Variant B |
| AstraChips LP 피치 준비 | Variant C |
| 신규 도메인 분석 | master_prompt_v3_optimized.md (파라미터 조정) |
