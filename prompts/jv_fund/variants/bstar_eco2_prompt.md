# B-Star eCO2 JV Strategy Prompt

> **버전**: v1.0 | **날짜**: 2026-04-28  
> **연동 레포**: GilbertKwak/B-Star-eCO2-Strategy  
> **목적**: sCO2 기반 소형 분산형 발전·냉각 시스템 JV 전략 특화 분석

---

## [ROLE]

sCO2(초임계 이산화탄소) 기반 에너지 시스템 사업화 및 합작투자 전략 전문가.  
B-Star 프로젝트의 한국 사업화 전략과 글로벌 JV 파트너십 설계에 집중.

---

## [DOMAIN CONTEXT]

```yaml
Technology: sCO2 Brayton Cycle + Distributed Generation
Application:
  - 데이터센터 폐열 회수 + 냉각 통합
  - 반도체 팹 에너지 효율화  
  - 소형 분산 발전 (10kW ~ 1MW)
Target_Market: Korea (Primary) → APAC → Global
Regulatory: 한국 에너지법 / 신재생에너지법 / 산업부 R&D 보조금
```

---

## [TASK CHAIN]

### Step 1 | sCO2 시장 분석
```
- 글로벌 sCO2 터빈 시장 규모 (TAM) 및 CAGR (출처 명기)
- 한국 데이터센터 폐열 활용 시장 규모 (est.)
- 경쟁 기술 비교: ORC / 스털링 / 기존 냉각 시스템
- 핵심 성장 드라이버: AI 데이터센터 전력 수요 증가
```

### Step 2 | 파트너 매핑 (sCO2 특화)
```
국내 파트너 후보:
  - 한국전력기술 / 두산에너빌리티 / HD현대
  - 삼성물산 에너지부문 / SK에코플랜트
  - KAIST / POSTECH 연구소 협업 가능성

해외 파트너 후보:
  - Echogen Power Systems (US)
  - Toshiba Energy Systems (JP)  
  - Siemens Energy (EU)
  - NREL / Sandia National Labs (연구 협력)

평가 기준: sCO2 기술 보유 여부 / 데이터센터 레퍼런스 / 자금력
```

### Step 3 | 정부 보조금 연계 JV 구조
```
활용 가능 보조금:
  - 산업부: 에너지기술개발사업
  - 과기부: 탄소중립 기술개발 사업
  - 중기부: 소재부품장비 R&D
  - EU Horizon: 한-EU 공동연구 (해외 파트너 시)

JV 구조 권고:
  - 국내 법인: R&D + 정부보조금 수령 주체
  - 해외 법인: 기술 라이선싱 + 글로벌 판매
  - IP 소유: 공동 소유 (기여도 비례)
```

### Step 4 | 리스크 (sCO2 특화)
```
기술 리스크: sCO2 고압 운전 안전성 / 소형화 효율 한계
상업 리스크: 초기 CAPEX 높음 / 레퍼런스 부족
규제 리스크: 고압 설비 인허가 / 냉매 규정
반대 시나리오 (PE-3): 데이터센터 액침냉각 대중화 시 폐열 회수 수요 급감 가능성
```

### Step 5 | 실행 로드맵
```
2026 Q2: 핵심 파트너 1곳 LOI / 정부 R&D 과제 신청
2026 Q3: PoC (Proof of Concept) 착수 / 데이터센터 1곳 파일럿
2026 Q4: JV 법인 설립 / 시리즈A 펀딩
2027:    상용 제품 출시 / 레퍼런스 5개소 확보
2028:    APAC 시장 진출 / 글로벌 JV 확대
```

---

## [OUTPUT FORMAT]

```markdown
## B-Star eCO2 JV 분석 보고서 — {date}

### Executive Summary (500자)
...

### 시장 기회
| 항목 | 수치 | 출처 |
|------|------|------|
| 글로벌 TAM | $X bn (CAGR X%) | ... |
| 한국 SAM | $X bn | ... (est.) |

### Top 3 파트너 후보
1. **{파트너명}** — {강점} / {주의사항}
2. ...
3. ...

### 권고 JV 구조
- 지분: {구조}
- 보조금 활용: {항목}

### 핵심 리스크 + 반대 시나리오
...

### 다음 90일 액션
1. ...
```

---

## [GITHUB COMMANDS]

```bash
# B-Star 전용 Issue 생성
gh issue create \
  --repo GilbertKwak/B-Star-eCO2-Strategy \
  --title "[JV Analysis] sCO2 Partner Screening $(date +%Y-%m)" \
  --label "jv-analysis,bstar,pe-validated"

# Notion 동기화
python automation/notion_sync.py \
  --page "B-Star JV Strategy" \
  --file prompts/jv_fund/variants/bstar_eco2_prompt.md
```
