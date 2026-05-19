# 투자검토 입력 양식 (Investment Input Template)

> `InvestmentReviewMaster v1.0` 및 `InvestmentPortfolioAgent v1.0` 입력용

---

## 단일 투자안 입력 양식

```yaml
investment:
  name: "[투자명]"
  industry: "[Manufacturing|Semiconductor/Display|Bio/Healthcare|Platform/IT/AI|Energy/ESG|Consumer/Retail]"
  type: "[Build|Buy/M&A|Partner|유가증권|CAPEX]"
  amount_krw: "[금액 (단위: 억원)]"
  currency: KRW
  strategic_purpose: "[전략 목적 2~3줄]"
  expected_irr: "[%]"
  target_market: "[주요 시장]"
  competitive_landscape: "[경쟁 상황 요약]"
  expected_synergy: "[예상 시너지]"
  key_risks: "[주요 리스크 Top 3]"
  investment_timeline: "[투자 일정]"
  exit_strategy: "[Exit 전략]"
  additional_materials: "[추가 자료 또는 없음]"
```

## 포트폴리오 비교용 (복수 투자안)

```yaml
portfolio_review:
  total_budget_krw: "[총 예산]"
  investments:
    - name: "투자안 A"
      # ... 위 필드 반복
    - name: "투자안 B"
      # ...
    - name: "투자안 C"
      # ...
```

---
*Template v1.0 | PE-FIN | 2026-05-19*
