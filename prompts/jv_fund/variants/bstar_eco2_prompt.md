# B-Star eCO2 JV 전략 특화 프롬프트 (Variant B)

> **버전**: v1.0 | **기준일**: 2026-04-27 | **기반**: master_prompt_v3.md  
> **PE-3 점수**: 89/100 | **연동 레포**: `B-Star-eCO2-Strategy`

---

## [목적]

sCO2(초임계 CO₂) 기반 소형 분산형 발전·냉각 시스템의 한국 사업화를 위한  
JV 펀드 구조 설계 및 파트너 매핑에 특화된 프롬프트입니다.

---

## [파라미터]

```yaml
SUBDOMAIN:    "{subdomain}"     # Power-Gen | Cooling | Both
APPLICATION:  "{application}"   # Data-Center | Industrial | Building | Grid
KOREA_STAGE:  "{korea_stage}"   # R&D | Pilot | Commercial | Scale-up
GOV_SUBSIDY:  "{gov_subsidy}"   # true | false  (정부 R&D 보조금 연계 여부)
SINGAPORE_HOLDCO: "{holdco}"   # true | false  (싱가포르 HoldCo 구조 적용 여부)
```

---

## [분석 프레임]

### sCO2 특화 시장 분석
```
- 글로벌 sCO2 터빈/열교환기 시장 규모 (2024~2030)
- 한국 데이터센터 냉각 수요 성장률
- 정부 탄소중립 정책과의 연계성
- 경쟁 기술 (칠러/히트펌프/액침냉각) 대비 우위
```

### 파트너 매핑 (sCO2 전문)
```
국내 파트너 후보:
  - 한국에너지기술연구원 (KIER) — R&D 파트너
  - 두산에너빌리티 — 터빈 제조 파트너
  - KT/SKT 데이터센터 사업부 — 수요처 파트너

해외 파트너 후보:
  - Echogen Power Systems (US) — sCO2 ORC 전문
  - Siemens Energy (EU) — 터빈 기술
  - Toshiba Energy (JP) — 아시아 공동 진출
```

### JV 구조 (B-Star 특화)
```
싱가포르 HoldCo:
  └── Korea R&D OpCo (KIER/두산 합작)
      ├── 기술 라이선스 → HoldCo
      └── 파일럿 플랜트 운영
  └── Korea/APAC Sales Co
      └── 데이터센터 고객사 계약
```

### 정부 보조금 연계 전략
```
- 과학기술정보통신부 sCO2 국책과제 연계
- 산업통상자원부 에너지 신산업 R&D 지원
- 기후테크 펀드 (한국벤처투자) 연계
- KETEP (에너지기술평가원) 연구비 활용
```

---

## [출력 포맷]

```markdown
## B-Star eCO2 JV Investment Memo v{version}

**도메인**: sCO2 {subdomain} | **응용처**: {application}  
**한국 사업화 단계**: {korea_stage}  
**PE-3 점수**: {pe3_score}/100 | **신뢰도**: {confidence_score}/100

### Executive Summary (KR)
{executive_summary}

### 시장 기회 (TAM/SAM/SOM)
| 구분 | 규모 | 출처 | 연도 |
|---|---|---|---|
| TAM | | | |
| SAM | | | |
| SOM | | | |

### 추천 JV 구조
{jv_structure_diagram}

### 리스크 매트릭스
{risk_matrix_table}

### 반대 시나리오 (PE-3)
{downside_scenario}

### 정부 보조금 로드맵
{subsidy_roadmap}

### 90일 실행 계획
{day90_plan}
```

---

## [검증 규칙]
- [ ] sCO2 시장 수치 출처 명시 (PE-1)
- [ ] 정부 보조금 프로그램 실제 공시 기반 (PE-1)
- [ ] 기술 성숙도 TRL 명시
- [ ] 경쟁 기술 대비 우위 근거 3가지 이상
- [ ] 반대 시나리오 (규제 변화 / 기술 실패) 포함 (PE-3)
