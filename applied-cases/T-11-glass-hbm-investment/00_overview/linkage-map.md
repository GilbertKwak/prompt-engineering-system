# T-11 — 연결 맵 (Linkage Map)

## 상위 연결
```
Workspace SSOT (Notion)
└── T-11 Glass/HBM 투자전략 허브 (이 레포)
    ├── T-10 AstraChips 통합 전략 허브
    │   └── PE-9 AstraChips LP Fund Prompts
    ├── PE-7 AI Automation Design & Implementation
    └── T-04 프롬프트 엔지니어링 시스템 허브 v2.0
```

## 프롬프트 연결 (PE 시스템)
| PE ID | 역할 | 연결 파일 |
|-------|------|----------|
| PE-3 | 검증 엔진 (품질 게이트) | 모든 보고서 섹션 적용 |
| PE-7 | AI 자동화 설계 | `02_financial_model/model_scaffold.py` |
| PE-9 | LP Fund 프롬프트 | `03_prompts/` ↔ `astrachips-lp-fund/prompts/` |

## 데이터 흐름
```
시장 데이터 입력
    ↓
02_financial_model/model_scaffold.py  (Python IRR/MOIC)
    ↓
outputs/ (CSV + PNG)
    ↓
04_reports/ → Notion T-11 허브 → LP One-pager (PE-9)
```

## 교차 참조
- HBM 기술 기반: T-05 HBM Salvage Value Program
- 반도체 공급망: T-02 글로벌 반도체 & AI 생태계 조사
- 재무모델 벤치마크: T-03 sCO₂ / B★ eCO₂ Financial Models Hub
