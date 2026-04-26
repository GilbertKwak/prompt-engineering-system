# T-11 — Glass 수직통합 & HBM 투자전략 허브
> **SSOT:** GitHub `prompt-engineering-system/applied-cases/T-11-glass-hbm-investment/`  
> **Notion 허브:** https://www.notion.so/ (T-11 Mother Hub — 생성 완료)  
> **상태:** 🟢 Active | **v1.0** | 2026-04-26 초기화  
> **연결:** T-10 AstraChips | PE-9 LP Fund Prompts | PE-7 AI Automation | Workspace SSOT

---

## 프로젝트 헌장

| 항목 | 내용 |
|------|------|
| **목적** | Glass 수직통합(Core) / 패키징 레버리지(Satellite) / US·EU 분산(Hedge) 3축 투자전략 구조화 |
| **총 투자 규모** | $1,000M USD |
| **목표 MOIC** | 6.43x (Balanced 시나리오) |
| **실행 기간** | 2026 Q2 → 2030 |
| **최초 생성** | 2026-03-01 (전략 수립) → 2026-04-26 (SSOT 아카이브) |
| **PE 연결** | PE-7 (AI 자동화), PE-9 (AstraChips LP Fund) |

---

## 디렉토리 구조

```
T-11-glass-hbm-investment/
├── README.md                          ← 이 파일 (프로젝트 헌장 + 네비게이션)
├── 00_overview/
│   ├── project-scope.md               ← 범위·목적·SSOT 정의
│   └── linkage-map.md                 ← PE-7/PE-9/T-10 연결 맵
├── 01_strategy/
│   ├── A_glass_vertical_integration.md   ← Core: Glass 수직통합 전략
│   ├── B_packaging_leverage.md           ← Satellite: 패키징 레버리지
│   └── C_us_eu_hedge.md                  ← Hedge: US/EU 지정학 분산
├── 02_financial_model/
│   ├── model_scaffold.py              ← IRR/MOIC/NPV Python 모델
│   ├── scenario_matrix.md             ← Conservative/Balanced/Aggressive
│   └── outputs/                       ← 차트·CSV 산출물
├── 03_prompts/
│   ├── PROMPT_VERSION_HISTORY.md      ← 프롬프트 버전 마스터 인덱스
│   ├── v1_core_satellite_hedge.md     ← v1.0 투자구조 정의 프롬프트
│   └── v2_financial_model.md          ← v2.0 재무모델 실행 프롬프트
├── 04_reports/
│   └── REPORT_INDEX.md                ← 보고서 인덱스
├── 05_logs/
│   └── CHANGE_LOG.md                  ← 변경 이력
└── 99_archive/
    └── .gitkeep
```

---

## 빠른 참조 (Quick Links)

| 문서 | 경로 | 용도 |
|------|------|------|
| 전략 A (Glass Core) | `01_strategy/A_glass_vertical_integration.md` | Samsung+Corning+AGC JV 15% 지분 전략 |
| 전략 B (패키징) | `01_strategy/B_packaging_leverage.md` | HBM4 오프테이크 + CoWoS 구조 |
| 전략 C (US/EU) | `01_strategy/C_us_eu_hedge.md` | Amkor 지분 + Micron CB |
| 재무모델 | `02_financial_model/model_scaffold.py` | IRR/MOIC/NPV 시뮬레이션 |
| 시나리오 | `02_financial_model/scenario_matrix.md` | 3개 시나리오 비교 |
| 프롬프트 v1 | `03_prompts/v1_core_satellite_hedge.md` | 투자구조 정의 프롬프트 |
| 변경이력 | `05_logs/CHANGE_LOG.md` | 전체 패치 이력 |

---

## 재사용 가이드 (유사 투자전략 프로젝트 적용)

1. `01_strategy/` 3개 파일의 파라미터(투자금액·지분율·오프테이크 조건)만 교체
2. `02_financial_model/model_scaffold.py` 실행 → `outputs/` 자동 생성
3. `03_prompts/v1_core_satellite_hedge.md` 프롬프트로 보고서 섹션 재생성
4. `04_reports/REPORT_INDEX.md` 에 신규 보고서 행 추가
5. 본 README 상단 상태값·버전 업데이트
