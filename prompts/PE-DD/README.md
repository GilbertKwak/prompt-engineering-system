# PE-DD · Enterprise Due Diligence Prompt Library

> **Domain**: PE-DD | **Status**: ✅ Active | **Created**: 2026-05-08  
> **Notion**: [PE-DD Library v1.0](https://www.notion.so/35955ed436f081028fbbe44e65f63d84)  
> **Parent System**: T-09 Prompt Engineering Ecosystem

---

## 📂 Library Index

| ID | 파일명 | 버전 | PE-3 | 상태 | 특징 |
|---|---|---|---|---|---|
| **P-OPT-DD-MASTER** | `dd_master_v2.0.md` | v2.0 | **97/100** | ✅ Active | 범용 Enterprise DD 최상위 마스터 |
| DD-009-A | `dd_009a_semi_v1.0.md` | v1.0 | TBD | 🔵 예정 | 반도체·AI 특화 (PRESET-SEMI 파생) |
| DD-009-B | `dd_009b_board_v1.0.md` | v1.0 | TBD | 🔵 예정 | 이사회용 Board Pack (BOARD_PACK 파생) |
| DD-010 | `dd_010_osat_v1.0.md` | v1.0 | TBD | 🔵 예정 | OSAT M&A 전용 |
| DD-011 | `dd_011_ai_infra_v1.0.md` | v1.0 | TBD | 🔵 예정 | AI Infra 전용 |

---

## 🗺️ PRESET 도메인 분기

```
P-OPT-DD-MASTER v2.0
    ├── PRESET=SEMI  → HBM·OSAT·EAR §742.4·CHIPS §50004·B-Star 4
    ├── PRESET=AI    → GPU·LLM·데이터센터·클라우드·AI거버넌스
    ├── PRESET=MFG   → 공장·CapEx·ESG·노동·sCO₂
    └── PRESET=BIO   → 임상·FDA·특허절벽·바이오시밀러·CMC
```

---

## 🔗 Cross-Domain Links

- **PE-SEMI**: 반도체 전략 분석 생태계
- **PE-FIN**: 재무 모델링·가치평가
- **PE-CON**: 계약·법무 검토
- **PE-OPT**: 자기진화 최적화 시스템 (EVO-001 등록)
- **T-09**: Mother Page — 전체 PE 생태계 허브

---

## 📋 Usage

```xml
<!-- 기본 실행 (STD 깊이, 범용) -->
COMPANY_NAME  = "[대상 기업]"
DD_TYPE       = "FULL"
DEAL_CONTEXT  = "M&A"
PRESET        = "NONE"
DEPTH         = "STD"
OUTPUT_LANG   = "KR"

<!-- 반도체 M&A 특화 실행 -->
COMPANY_NAME  = "[반도체 기업]"
DD_TYPE       = "FULL"
DEAL_CONTEXT  = "M&A"
PRESET        = "SEMI"
DEPTH         = "DEEP"
OUTPUT_LANG   = "KR"

<!-- 이사회 제출용 (EXEC 깊이) -->
COMPANY_NAME  = "[대상 기업]"
DD_TYPE       = "COMMERCIAL"
DEAL_CONTEXT  = "INVESTMENT"
PRESET        = "AI"
DEPTH         = "EXEC"
OUTPUT_LANG   = "Bilingual"
```
