# B-Star eCO2 Strategy Prompt v1.0

> **Version**: v1.0  
> **Date**: 2026-04-27  
> **Parent**: `master_prompt_v3.md`  
> **Purpose**: sCO2 기반 에너지 시스템 B-Star 전략 특화 JV 분석  

---

## [CONTEXT]

```yaml
domain: sCO2
strategy: B-Star
focus_areas:
  - sCO2 터빈 파트너사 매핑 (한국/미국/유럽)
  - 데이터센터 냉각 수요와 시너지 분석
  - 정부 R&D 보조금 연계 JV 구조
  - 폐열 회수(Waste Heat Recovery) 비즈니스 케이스
```

---

## [TASK]

```
1. sCO2 터빈/사이클 기술 보유 파트너사 매핑
   - 국내: POSCO, KEPCO, Doosan Enerbility, KAIST 스핀오프
   - 미국: GTI Energy, Southwest Research Institute, Echogen
   - 유럽: Siemens Energy, Baker Hughes

2. AI 데이터센터 냉각 수요와의 시너지 분석
   - 데이터센터 PUE 개선 효과 (수치 근거 필수)
   - sCO2 냉각 vs 기존 냉각 비용 비교
   - HBM/GPU 발열 밀도와 sCO2 냉각 적용 가능성

3. 정부 R&D 연계 JV 구조 설계
   - 한국: 산업부 / KETEP / KIAT 보조금 프로그램
   - 미국: DOE ARPA-E / NREL
   - EU: Horizon Europe / EIC

4. 3-tier Investment Memo 작성
   - Tier 1: 기술 검증 단계 (TRL 6-7)
   - Tier 2: 파일럿 구축 단계 (TRL 7-8)
   - Tier 3: 상업화 단계 (TRL 8-9)
```

---

## [CHAIN]

```
Step 1 → sCO2 시장 현황 분석
  - 글로벌 시장 규모 및 CAGR
  - 주요 플레이어 경쟁 구도
  - 기술 성숙도 (TRL) 현황

Step 2 → B-Star 포지셔닝
  - 차별화 요소 3가지
  - 진입 장벽 분석
  - 특허 포트폴리오 현황

Step 3 → JV 구조 옵션
  - Option A: 국내 중심 JV + 해외 기술 라이선스
  - Option B: 한미 공동 JV (기술 개발 분담)
  - Option C: 유럽 인증 우선 JV

Step 4 → 리스크 및 정부 보조금 전략
  - 규제 리스크 (에너지 법규 각국 비교)
  - 보조금 수령 조건 및 타임라인

Step 5 → 3-tier Investment Memo
```

---

## [OUTPUT FORMAT]

```markdown
## B-Star eCO2 JV Investment Memo

### Executive Summary (KR/EN 병기)
**KR**: ...
**EN**: ...

### 시장 현황
| 항목 | 수치 | 출처 |
|---|---|---|
| 글로벌 TAM | | |
| CAGR (2024-2030) | | |
| 데이터센터 냉각 시장 | | |

### 파트너사 매핑
| 파트너 | 국가 | 핵심 역량 | JV 적합도 |
|---|---|---|---|

### 3-Tier Investment Memo
| Tier | 단계 | 투자 규모 | TRL | 기간 |
|---|---|---|---|---|
| Tier 1 | 기술 검증 | | 6-7 | |
| Tier 2 | 파일럿 | | 7-8 | |
| Tier 3 | 상업화 | | 8-9 | |
```

---

## [VALIDATION]

- [ ] PE-1: 모든 수치에 출처 및 연도 명시
- [ ] PE-3: Bear Case (sCO2 상업화 지연 시나리오) 포함
- [ ] 에너지 법규 리스크 플래그
- [ ] 보조금 의존도 리스크 경고
