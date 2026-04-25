# 변형 C — 재무·투자 분석 집중용 (v2.0 개선)

> **Base:** Master Prompt v2.0 | **Variant:** C | **Updated:** 2026-04-25
> **목적:** D-4 투자·M&A 타깃 분석에 필요한 재무 데이터 및 신호 수집

---

## [변경 사항 — v1.0 대비]

| 문제 | 해결 |
|---|---|
| IPO/M&A 타깃은 비공개 데이터 → 신뢰도 불명확 | 신뢰도 등급 필드 추가 (A/B/C) |
| VC 확인 기준 수치 없음 | Tier 1 VC 명단 명시 |
| M&A 가능성 판단 기준 없음 | MA_signal 판단 기준 5개 추가 |

---

## [FINANCIAL FILTER]

```yaml
financial_criteria:
  listed_companies:
    condition: "listed = true"
    exchanges: ["TWSE", "NASDAQ", "NYSE", "KRX", "BSE", "NSE", "LSE", "HKEX"]
    required_data:
      - "Market Cap (USD)"
      - "Revenue (USD, latest FY)"
      - "EV/Revenue multiple"
      - "YoY Growth Rate"
  
  private_companies:
    vc_tier1_list:
      - "Sequoia Capital"
      - "Andreessen Horowitz (a16z)"
      - "Bessemer Venture Partners"
      - "New Enterprise Associates (NEA)"
      - "Khosla Ventures"
      - "GV (Google Ventures)"
      - "SoftBank Vision Fund"
      - "Tiger Global Management"
      - "Intel Capital"
      - "Qualcomm Ventures"
      - "Samsung Ventures"
    data_fields:
      - "Total Funding (USD)"
      - "Latest Round (Series, 금액, 연도)"
      - "Valuation (추정, 신뢰도 등급 C)"

ma_signal_criteria:
  HIGH:
    conditions:
      - "최근 2년 내 M&A 루머 보도 (Bloomberg/Reuters)"
      - "주요 고객사가 잠재 인수자와 동일 생태계"
      - "창업자 Exit 의향 공개 발언"
      - "PE/전략적 투자자 Board Seat 보유"
      - "EV/Revenue < 3x (저평가 신호)"
  MEDIUM:
    conditions:
      - "IPO 준비 중 보도"
      - "전략적 파트너십 확대"
  LOW:
    conditions:
      - "신규 대규모 VC 투자 유치 (독립 성장 선호)"

additional_output_fields:
  - name: "IPO 가능성"
    type: ENUM
    values: ["High (2년 내)", "Medium (3~5년)", "Low", "N/A"]
    trust_level: "C (추정)" # 비공개 데이터
  - name: "잠재 인수자"
    type: STRING
    format: "기업명 (전략적/재무적)"
  - name: "EV/Revenue 추정"
    type: STRING
    note: "상장사: 실제값, 비상장: 동종업계 배수 적용 추정"
  - name: "신뢰도 등급"
    type: ENUM
    values: ["A (공시/IR)", "B (Crunchbase/PitchBook)", "C (추정)"]
    required: true
```

## [변형 C 전용 산출물]

- D-4C: M&A 타깃 Top 10 상세 분석 (잠재 인수자 매핑 포함)
- D-4C_IPO: IPO 준비 기업 목록 (신뢰도 등급 표시)
