# JV Fund Prompt Library

> **Version**: v3.0  
> **Date**: 2026-04-27  
> **Status**: Active  

---

## 개요

Global Joint Venture Fund 분석을 위한 프롬프트 라이브러리.
원본 `Global_Joint_Venture_Fund_Master_Prompt_v2.txt` → v3.0 완전 재구조화.

---

## 파일 구조

```
applied-cases/jv-fund/
├── README.md                  ← 이 파일
├── master_prompt_v3.md        ← 핵심 마스터 프롬프트 (v2 → v3 업그레이드)
├── fu_series_adapter.md       ← FU-Series 보고서 연동 서브프롬프트
├── bstar_eco2_prompt.md       ← B-Star sCO2 전략 특화
├── ai_infra_prompt.md         ← AI 인프라 데이터센터 특화
└── validation_checklist.md   ← PE-1/PE-3 공통 검증 체크리스트
```

---

## 빠른 사용법

```bash
# 1. 기본 JV 분석 (HBM 도메인, 스크리닝 단계)
# master_prompt_v3.md 파라미터 치환:
# domain=HBM / stage=Screening / lang=KR / depth=Full

# 2. FU-Series 연동 분석
# fu_series_adapter.md: FU_NUMBER=019, FU_SECTION=Market-Analysis

# 3. sCO2 전략 분석
# bstar_eco2_prompt.md: 별도 파라미터 없음, 그대로 사용

# 4. AI 인프라 분석
# ai_infra_prompt.md: fund_size 및 lp_types 파라미터 설정

# 5. 검증 실행
python ../../automation/auto_validate.py --file master_prompt_v3.md --rules PE-1,PE-3
```

---

## Notion 연동

| 파일 | Notion 페이지 |
|---|---|
| master_prompt_v3.md | [💼 PE-JV · Global JV Fund Prompt Library v3.0](https://www.notion.so/34f55ed436f081c08fececa8dd7577f9) |
| 전체 라이브러리 | [💼 PE-JV · Global Joint Venture Fund Prompt Library v3.0](https://www.notion.so/34f55ed436f08150b07dc7f5f800311b) |

---

## CHANGELOG

| 버전 | 날짜 | 변경 내용 |
|---|---|---|
| v3.0 | 2026-04-27 | v2 완전 재구조화, 도메인 파생 3종 추가, PE-1/PE-3 검증 내장 |
| v2.0 | (원본) | 최초 작성 (단일 XML 블록) |
