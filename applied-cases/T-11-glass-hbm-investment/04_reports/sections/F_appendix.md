# Section F — Appendix & Reference
> **T-11 | Glass/HBM 투자전략 | v2.0 | 2026-04-26**

---

## F.1 용어 정의

| 용어 | 정의 |
|------|------|
| **HBM (High Bandwidth Memory)** | 여러 DRAM 다이를 TSV로 수직 적층한 고대역폭 메모리. AI 가속기 핵심 부품 |
| **Glass Substrate** | PCB/ABF를 대체하는 유리 기반 인터포저. 열팽창 안정성·배선 밀도 우수 |
| **CoWoS (Chip on Wafer on Substrate)** | TSMC 고급 패키징 공정. HBM + GPU/CPU를 하나의 패키지로 통합 |
| **MOIC** | Multiple on Invested Capital. 총 회수금 / 투자금 |
| **IRR** | Internal Rate of Return. 투자 현금흐름의 수익률 |
| **VS Score** | Vulnerability Score = BS × Geo_Risk × DSM. T-11 공급망 병목 지수 |
| **DSM** | Design Structure Matrix. 공급망 노드 간 의존도 매트릭스 |
| **Outtake Contract** | 사전 약정 구매 계약. 공급자는 물량 보장, 구매자는 가격/물량 선점 |
| **CB (전환사채)** | 전환사채. 일정 조건 충족 시 주식으로 전환 가능한 채권 |
| **CHIPS Act** | 미국 반도체 제조 투자 지원법 (2022). 보조금 및 세액공제 제공 |
| **EU Chips Act** | EU 반도체 산업 육성법 (2023). €43B 공공·민간 투자 동원 목표 |

---

## F.2 데이터 소스 및 가정

### 시장 데이터 출처
- HBM 시장 규모: Yole Intelligence, IDC (2025-2026)
- Glass Substrate 시장: Prismark, IPC (2025)
- CoWoS 가용 용량: TSMC 공식 IR, Digitimes (2025)
- AI CAPEX 전망: Goldman Sachs, Morgan Stanley (2026)

### 핵심 가정
```yaml
# 재무 모델 핵심 가정
discount_rate: 0.12  # WACC 12%
tax_rate: 0.21       # 미국 법인세
currency: USD
base_year: 2026
forecast_horizon: 2030

# Type A 가정
jv_market_share_base: 0.25
glass_market_size_2030: 8.5  # $B
ebitda_margin: 0.35
exit_multiple_evEBITDA: 15

# Type B 가정
hbm4_units_per_year: 2000000
hbm4_margin_per_unit: 50  # USD
cowos_wafers_per_year: 15000
cowos_margin_per_wafer: 3000  # USD

# Type C 가정
amkor_equity_stake: 0.10
micron_cb_amount: 150  # $M
micron_conversion_price: 120  # USD
micron_target_price_2029: 250  # USD
coupon_rate: 0.03
```

---

## F.3 Agent 파이프라인 버전 이력

| Agent | 버전 | 커밋 | 날짜 | 주요 변경사항 |
|-------|------|------|------|-------------|
| Agent-1 | v1.0 | 91a995a | 2026-04-26 | 초기 scaffold |
| Agent-1 | v2.0 | 64fab7f | 2026-04-26 | G-01~G-10 해소, Sub-Agent 4종 |
| Agent-2 | v1.0 | 64fab7f | 2026-04-26 | 의존성·병목 프레임워크 |
| Agent-2 | v2.0 | a9e6933 | 2026-04-26 | DSM 매트릭스, E-04/E-07 해소 |
| Agent-3 | v1.0 | 1b678eb | 2026-04-26 | 4-World, Monte Carlo 500회 |
| **Report v2.0** | — | **현재** | **2026-04-26** | **섹션 A~F 병렬 구성** |

---

## F.4 관련 문서 인덱스

### GitHub 내부 링크
```
📁 T-11-glass-hbm-investment/
├── 01_strategy/
│   ├── A_glass_vertical_integration.md
│   ├── B_packaging_leverage.md
│   └── C_us_eu_hedge.md
├── 02_financial_model/
│   ├── model_scaffold.py
│   └── scenario_matrix.md
├── 03_prompts/
│   ├── PROMPT_VERSION_HISTORY.md
│   ├── agent_1_expanded_profile_v2.0.md
│   ├── agent_2_dependency_bottleneck_profile_v2.0.md
│   └── agent_3_scenario_planning_v1.0.md
├── 04_reports/
│   ├── REPORT_INDEX.md          ← 업데이트 필요
│   ├── T11_investment_report_v1.0.md
│   ├── T11_investment_report_v2.0.md  ← 통합본 (예정)
│   └── sections/
│       ├── A_executive_summary.md     ✅
│       ├── B_industry_analysis.md     ✅
│       ├── C_financial_model.md       ✅
│       ├── D_risk_analysis.md         ✅
│       ├── E_execution_roadmap.md     ✅
│       └── F_appendix.md             ✅
└── 05_logs/
    └── CHANGE_LOG.md
```

### 외부 참조
- [TSMC CoWoS 기술 브리프](https://investor.tsmc.com)
- [Intel Glass Core 발표](https://newsroom.intel.com)
- [US CHIPS Act 공식 사이트](https://www.nist.gov/chips)
- [EU Chips Act](https://ec.europa.eu/chips-act)

---

## F.5 변경 이력 (이 보고서)

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v2.0 | 2026-04-26 | 섹션 A~F 병렬 구성 완성, Agent-3 Monte Carlo 결과 반영 |
| v1.0 | 2026-03-01 | Core/Satellite/Hedge 전략 + Python 재무모델 초기 버전 |

---
*본 보고서는 T-11 프로젝트의 SSOT(Single Source of Truth)입니다.*  
*GitHub: [T-11-glass-hbm-investment](https://github.com/GilbertKwak/prompt-engineering-system/tree/main/applied-cases/T-11-glass-hbm-investment)*
