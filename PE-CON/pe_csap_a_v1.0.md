# PE-CSAP-A v1.0 — Semiconductor-Specialized Competitive Strategy Analysis Prompt

> **코드**: PE-CSAP-A  
> **도메인**: SEMI (반도체 특화)  
> **상위 허브**: CON-06-A (L3 파생)  
> **PE Score**: 94pt (목표 92pt 초과)  
> **생성일**: 2026-05-09  
> **작성자**: Gilbert Kwak  
> **버전**: v1.0  

---

## 📌 Overview

PE-CSAP-A는 CON-06 시리즈의 반도체 전략 특화 파생 프롬프트다. HBM, CoWoS, EUV 등 첨단 반도체 공정 및 공급망 경쟁 환경에서의 전략 분석을 자동화한다. BCG Matrix 강제 배치, 공급망 위험 자동 계산, PE-3 수준 Self-validation을 포함한다.

---

## 🧬 CSAP 4단계 프레임워크

### Stage 1 · Competitive Intel
```yaml
inputs:
  - company: [SK하이닉스 | 삼성전자 | 마이크론]
  - product: [HBM4 | HBM3E | CoWoS | High-NA EUV]
  - horizon: [Q1~Q4 | YoY]
outputs:
  - market_share_delta
  - capex_trajectory
  - yield_estimate
```

### Stage 2 · Strategic Analysis
- BCG Matrix 강제 배치 (Star/Cash Cow/Question Mark/Dog)
- Porter 5 Forces 자동 스코어링
- Geopolitical Risk Index (BIS 규제 연동)

### Stage 3 · Action Plan
```yaml
format:
  - immediate: [0-3개월 액션]
  - mid_term: [3-12개월 로드맵]
  - long_term: [1-3년 전략 포지셔닝]
output_style: MECE | 80/20
```

### Stage 4 · Portfolio Optimization
- Salvage 수익성 자동 계산 (HBM2e/HBM3E 재고)
- HBM4 투자 타이밍 최적화 모델
- CapEx ROI 시뮬레이션

---

## 🔧 HBM4 전용 프로토콜

```yaml
hbm4_protocol:
  competitive_timing:
    sk_hynix: "2026-Q3 양산 기준"
    samsung: "2026-Q4 추격 예상"
    micron: "2027-Q1 후발"
  b300_spec_check:
    hbm_stacks: 8
    bandwidth: "1.2TB/s"
    cowos_bottleneck: "TSMC CoWoS-L 캐파 제약"
  salvage_calc:
    hbm3e_margin: 35%
    hbm2e_margin: 12%
    transition_risk: HIGH
```

---

## ✅ Self-Validation (PE-3 기준)

```yaml
validation:
  dimensions:
    - clarity: 19/20
    - structure: 20/20
    - domain_accuracy: 19/20
    - actionability: 18/20
    - completeness: 18/20
  total: 94/100
  threshold: 92
  auto_retry:
    max_attempts: 2
    trigger: "score < threshold"
```

---

## 📊 BCG Matrix 자동 배치 규칙

| 제품 | 분류 | 기준 |
|------|------|------|
| HBM4 | ⭐ Star | 고성장 + 점유율 확대 |
| HBM3E | 🐄 Cash Cow | 성숙 시장 + 마진 방어 |
| HBM2e | 🐕 Dog | 저성장 + 전환 급속 |
| HBM4 Sampling | ❓ Question Mark | 초기 시장 진입 |

---

## 🔗 연관 코드

- **상위**: CON-06 (전략 분석 허브)
- **형제**: PE-CSAP-B (FIN 특화), PE-CSAP-C (GEO 특화)
- **참조 KG**: graphs/knowledge_graph_v2.1_hbm4_delta.json
- **MCP 연결**: Perplexity MCP A2 (실시간 쿼리)

---

## 📝 Changelog

| 버전 | 날짜 | 변경 사항 |
|------|------|-----------|
| v1.0 | 2026-05-09 | 최초 생성 (CON-06-A 파생, HBM4 프로토콜 포함) |
