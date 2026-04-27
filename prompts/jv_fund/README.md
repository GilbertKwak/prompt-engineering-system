# JV Fund Prompt Library

> **생성일**: 2026-04-27 | **관리자**: GilbertKwak  
> **원본 파일**: `Global_Joint_Venture_Fund_Master_Prompt_v2.txt`  
> **현재 버전**: v3.0 (Active)

---

## 디렉터리 구조

```
prompts/jv_fund/
├── README.md                    ← 이 파일
├── master_prompt_v3.md          ← 메인 마스터 프롬프트 (v3)
├── VALIDATION_CHECKLIST.md      ← PE-1 / PE-3 검증 체크리스트
└── variants/
    ├── fu_series_adapter.md     ← FU-Series 연동 어댑터
    ├── bstar_eco2_prompt.md     ← B-Star eCO₂ 전용
    └── ai_infra_prompt.md       ← AI 데이터센터 인프라 전용
```

---

## 버전 히스토리

| 버전 | 날짜 | 주요 변경 |
|---|---|---|
| v2.0 | 2026-04-27 이전 | 원본 XML 구조 단일 파일 |
| v3.0 | 2026-04-27 | PE-1/PE-3 탑재, CoT 체인, 파라미터화, 도메인 변형 3종 추가 |

---

## 빠른 사용 가이드

### 1. 기본 실행 (Master Prompt v3)
```
[master_prompt_v3.md] 열기
↓
CONTEXT PARAMETERS 섹션에서 값 설정
  DOMAIN: HBM | sCO2 | Thermal | AI-DC
  STAGE:  Screening | DD | Structuring | Post-Close
  LANG:   KR+EN
↓
AI 모델에 전체 프롬프트 입력
↓
PE-1 / PE-3 체크리스트로 출력 검증
```

### 2. 도메인 특화 실행
- **HBM/열관리** → `variants/fu_series_adapter.md` 사용
- **sCO2 에너지** → `variants/bstar_eco2_prompt.md` 사용  
- **AI 인프라** → `variants/ai_infra_prompt.md` 사용

### 3. 검증 실행
```bash
python automation/auto_validate.py --dir prompts/jv_fund/ --rules PE-1,PE-3
```

---

## 연관 레포지토리

| 레포 | 연관성 | 링크 |
|---|---|---|
| AstraChips-Strategy | HBM JV 전략 | [바로가기](https://github.com/GilbertKwak/AstraChips-Strategy) |
| B-Star-eCO2-Strategy | sCO2 JV 전략 | [바로가기](https://github.com/GilbertKwak/B-Star-eCO2-Strategy) |
| fu-semiconductor-thermal | FU-Series 보고서 | [바로가기](https://github.com/GilbertKwak/fu-semiconductor-thermal) |
| global-semiconductor-ai-research | AI 인프라 분석 | [바로가기](https://github.com/GilbertKwak/global-semiconductor-ai-research) |

---

## Notion 연동

이 디렉터리의 마스터 프롬프트는 Notion **JV Fund Prompt Library** 페이지와 동기화됩니다.  
변경 시 `notion_sync.py`를 실행하거나 GitHub Actions 자동 동기화를 활용하세요.
