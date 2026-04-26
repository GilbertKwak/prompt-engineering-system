# T-11 — 시나리오 매트릭스

## 포트폴리오 배분 시나리오 (총 $1,000M)

| 시나리오 | Type A (Glass Core) | Type B (패키징) | Type C (US/EU) | Portfolio MOIC | Risk Score |
|----------|---------------------|-----------------|----------------|----------------|------------|
| **Conservative** | 50% ($500M) | 30% ($300M) | 20% ($200M) | 5.52x | 0.155 |
| **Balanced** ⭐ | 40% ($400M) | 35% ($350M) | 25% ($250M) | 6.43x | 0.155 |
| **Aggressive** | 20% ($200M) | 50% ($500M) | 30% ($300M) | 7.08x | 0.170 |
| **Geo-Hedge** | 30% ($300M) | 30% ($300M) | 40% ($400M) | 7.60x | 0.145 |

⭐ **권장: Balanced** — 리스크-수익 균형 최적, 2030 MOIC 6.43x

## 개별 투자유형 재무 성과

| Type | 투자금 | NPV | MOIC | IRR | Payback | 주요 리스크 |
|------|--------|-----|------|-----|---------|------------|
| A — Glass Core | $500M | $52.7M | 1.11x | 12% | 6년 | 지정학 15% |
| B — 패키징 Sat. | $400M | $3,158M | 8.90x | 45% | 2.5년 | 대만 20% |
| C — US/EU Hedge | $350M | $3,676M | 11.50x | 55% | 2.0년 | 정책 10% |

## 실행 타임라인

| Phase | 기간 | Type A | Type B | Type C |
|-------|------|--------|--------|--------|
| Phase 1 | 2026 Q2-Q3 | JV 협상 착수 | — | Amkor 지분 + Micron CB |
| Phase 2 | 2026 Q4-2027 Q1 | JV 설립 | HBM4 오프테이크 확정 | EU Chips Act 신청 |
| Phase 3 | 2027-2028 | Glass 2세대 | HBM5 옵션 | Micron CB 전환 검토 |
| Exit | 2029-2030 | IPO/Secondary | 오프테이크 만기 | 부분 매각 |

## Python 모델 실행
```bash
cd 02_financial_model
python model_scaffold.py
# → outputs/portfolio_summary.csv 자동 생성
```
