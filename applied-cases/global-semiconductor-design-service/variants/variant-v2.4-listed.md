# 변형 v2.4 — 상장사 한정 심층 분석

> **Base:** Master Prompt v2.0 + 변형 C | **Version:** v2.4 | **Created:** 2026-04-25
> **생성 근거:** Alchip(TWSE), GUC(TWSE), Faraday(TWSE) 등 공시 데이터 활용 정밀분석

---

## [LISTED COMPANY FILTER]

```yaml
listed_only: true
target_exchanges:
  primary:
    - exchange: "TWSE"
      country: "TW"
      note: "대만 상장사 집중 — Alchip, GUC, Faraday, eMemory, M31"
    - exchange: "NASDAQ"
      country: "US"
    - exchange: "NYSE"
      country: "US"
  secondary:
    - exchange: "KRX"
      country: "KR"
    - exchange: "BSE/NSE"
      country: "IN"
      note: "Tata Elxsi, L&T Technology Services"
    - exchange: "LSE"
      country: "GB"
    - exchange: "HKEX"
      country: "HK"

required_financial_data:
  - "Revenue (FY2024 또는 최신 결산)"
  - "Gross Margin (%)"
  - "Operating Margin (%)"
  - "Market Cap (USD 환산)"
  - "EV/Revenue multiple (동종업계 비교)"
  - "YoY Revenue Growth (%)"
  - "R&D Expense / Revenue ratio"

twse_known_companies:
  design_service:
    - ticker: "2399"
      name: "Alchip Technologies"
    - ticker: "3443"
      name: "Global Unichip Corp (GUC)"
    - ticker: "3526"
      name: "Faraday Technology"
  ip_core:
    - ticker: "3529"
      name: "eMemory Technology"
    - ticker: "6643"
      name: "M31 Technology"
```

## [산출물]
- D-1_Listed: 상장사 목록 (거래소별 분류)
- D-2_Listed: 재무지표 비교표 (Revenue, Margin, EV/Revenue)
- D-4_Listed: 상장사 중 M&A 타깃 분석
