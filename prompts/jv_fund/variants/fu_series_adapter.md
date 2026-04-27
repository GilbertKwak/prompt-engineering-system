# JV Fund Prompt — FU-Series 연동 어댑터

> **버전**: v1.0 | **작성일**: 2026-04-27  
> **부모 프롬프트**: `../master_prompt_v3.md`  
> **연동 레포**: [fu-semiconductor-thermal](https://github.com/GilbertKwak/fu-semiconductor-thermal)

---

## [CONTEXT OVERRIDE]

```yaml
DOMAIN: HBM | Thermal Management | Advanced Packaging
STAGE:  Technical Due Diligence → JV Structuring
SPECIAL: FU-Series 보고서 데이터 직접 인용 허용
```

---

## [TASK — FU-Series 데이터 기반 JV 타당성 검증]

```
INPUT:
  - FU 보고서 번호: FU-{NUMBER}
  - 인용 섹션: "Market Analysis" | "Technical Specs" | "Competitive Landscape"

TASK:
  1. FU 보고서 핵심 데이터 추출 (TAM · 기술 성숙도 · 경쟁사 현황)
  2. JV 파트너 후보 매핑 (FU 보고서 내 기업 목록 활용)
  3. 기술 리스크 재평가 (FU 데이터 기반)
  4. JV 타당성 스코어 산출 (0~100)

OUTPUT:
  - Notion 페이지 업데이트 초안
  - GitHub PR 본문 초안
  - JV 타당성 스코어: {SCORE}/100
```

---

## [FU-Series 연동 매핑 테이블]

| FU 번호 | 주제 | JV 연관성 | 우선순위 |
|---|---|---|---|
| FU-008 | HBM4-GPU 열관리 | 고 (Direct-on-Die Cooling IP) | 🔴 High |
| FU-009~015 | 첨단 패키징 TIM | 중 (소재 JV 가능) | 🟡 Mid |
| FU-016~025 | AI 가속기 냉각 | 고 (데이터센터 JV) | 🔴 High |

---

## [PE-3 검증 — FU 특화]

- [ ] FU 보고서 인용 시 보고서 번호 + 섹션 명시
- [ ] 기술 TRL(Technology Readiness Level) 수준 기재
- [ ] 특허 현황 반영 여부 확인
- [ ] AstraChips 전략과의 시너지 명시
