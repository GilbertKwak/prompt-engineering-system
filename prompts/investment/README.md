# 📊 Investment Prompts — FIN-MSIA System

> Gilbert Kwak Domain — AstraChips · HBM · B-Star eCO₂  
> Last Updated: 2026-05-19

---

## 파일 구조

```
prompts/investment/
├── fin_msia_master_v2.0.xml           ← ★ 통합 Multi-Agent 투자심사 (현행)
├── STRATEGIC_INVESTMENT_REVIEW_v1.md  ← 구버전 (참조용 보존)
├── templates/
│   └── investment_input_template.json ← 투자안 표준 입력 스키마
└── README.md
```

---

## 버전 이력

| 버전 | 파일 | 날짜 | 변경 내용 |
|------|------|------|-----------|
| v1.0 | STRATEGIC_INVESTMENT_REVIEW_v1.md | 2026-04 | 4개 독립 프롬프트 |
| v2.0 | fin_msia_master_v2.0.xml | 2026-05-19 | 통합 Multi-Agent 시스템 |

---

## v2.0 핵심 개선사항

| 항목 | v1.x | v2.0 |
|------|------|------|
| 구조 | 4개 독립 파일 | 1개 통합 오케스트레이터 |
| 의사결정 | 분석 중심 | Go/CG/NG 판단 직결 |
| 산업 특화 | 파일별 분리 | industry_selector 내장 |
| Multi-Agent | ❌ | ✅ 7개 Agent |
| 복수 투자안 비교 | ❌ | ✅ PortfolioAgent |
| 가중치 조정 | 고정 | 산업별 자동 조정 |

---

## 적용 Tier

| Tier | 대상 | 적용 범위 |
|------|------|-----------|
| **1** | 투자심의위원회 보고서 / M&A / 전략 포트폴리오 | Full 7 Agents |
| **2** | AI Intel Weekly / 반도체 심층 보고서 / ESG 리포트 | 모듈별 부분 적용 |
| **3** | Session Log / Raw 수집 / 단순 시황 | 미적용 |

---

## Notion 연계

- **PE-FIN 라이브러리**: https://www.notion.so/34f55ed436f081c2ad05df1dc11e0ae7
- **FIN-MSIA-SEMI v1.1**: https://www.notion.so/35a55ed436f08115aecae85ce645b76b
- **FIN-MSIA-ESG v1.1**: https://www.notion.so/35a55ed436f081a7b6d2ef1fcb1eacfd
- **FIN-MSIA-JV v1.1**: https://www.notion.so/35a55ed436f0815a8383ea119352243b
- **T-09 Mother Page v6.1**: https://www.notion.so/34a55ed436f0814d9cffe6a2f0816e29

---

## 사용법

```bash
# 1. 투자안 정보 입력
cp prompts/investment/templates/investment_input_template.json my_investment.json
# my_investment.json 편집

# 2. GPT-5.2 / Claude / Perplexity에 아래 순서로 입력
# [1] fin_msia_master_v2.0.xml 전체
# [2] my_investment.json
# [3] "위 투자안에 대해 FIN-MSIA-MASTER v2.0 기준으로 전체 투자심사를 진행해줘"
```
