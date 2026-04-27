# FU-Series JV Adapter Prompt v1.0

> **Parent:** `../master_prompt_v3.md` | **Domain:** HBM Thermal × JV Fund
> **Linked Repos:** `fu-semiconductor-thermal`, `HBM-Salvage-Value-Program`

---

## [CONTEXT OVERRIDE]

```yaml
DOMAIN: HBM / Thermal Management / Semiconductor Packaging
STAGE: 입력값 (FU 보고서 번호 기반 자동 판단)
FU_REPORT: "FU-{NUMBER}" # e.g. FU-001 ~ FU-025
INPUT_SECTION: "Market Analysis" | "Technical Specs" | "Business Strategy"
```

---

## [TASK CHAIN]

### Step 1: FU 보고서 데이터 추출
- 입력: FU-{NUMBER} 보고서의 `{INPUT_SECTION}` 섹션
- 추출 항목: 시장 규모, 기술 성숙도, 경쟁사 현황, 원가 구조

### Step 2: JV 타당성 재검증
- Master Prompt v3의 Step 4 (Fund Sizing) 데이터와 크로스체크
- HBM Salvage Value와 JV 수익 구조 정합성 확인
- AstraChips 전략과의 시너지 분석

### Step 3: 파트너사 매핑
- 국내: SK하이닉스, 삼성전자 (OSAT), 한화
- 해외: Micron, TSMC 패키징 파트너, NVIDIA 공급망
- sCO2 냉각 연계: B-Star 파트너십 가능성

### Step 4: 산출물 생성
- Notion 페이지 업데이트 초안
- GitHub PR 본문 초안
- FU 보고서 부록 섹션 (JV 시사점)

---

## [OUTPUT]

```markdown
## JV 타당성 요약 (FU-{NUMBER} 기반)

| 항목 | 내용 | 출처 |
|---|---|---|
| 시장 규모 | USD XXXm (20XX) | FU-{NUMBER} |
| JV 적합 단계 | {STAGE} | 분석 기준 |
| 추천 파트너 타입 | {LP_TYPE} | 매핑 결과 |
| 리스크 수준 | H/M/L | PE-3 시나리오 |

## 다음 액션
1. FU-{NUMBER} 시장 데이터 → JV Term Sheet 초안 작성
2. AstraChips LP 피치덱 섹션 업데이트
3. GitHub Issue: `[FU-JV] FU-{NUMBER} JV Feasibility`
```

---

## [LINKED RESOURCES]

- Notion: [FU-Series Mother Page](https://www.notion.so/)
- GitHub: [fu-semiconductor-thermal](https://github.com/GilbertKwak/fu-semiconductor-thermal)
- GitHub: [AstraChips-Strategy](https://github.com/GilbertKwak/AstraChips-Strategy)

---

*v1.0 | 2026-04-27 | FU-Series JV Adapter | Gilbert Kwak*
