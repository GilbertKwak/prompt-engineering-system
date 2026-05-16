---
suite: Porter ValueChain Competitive Advantage Suite
domain: PE-STRAT
version: "1.0"
created: 2026-05-16
---

# Porter ValueChain Suite — Index

| ID | 파일 | 버전 | 용도 | pe3_score |
|---|---|---|---|---|
| PE-STRAT-VC-P1 | PE-STRAT-VC-P1-v3.0.md | 3.0 | 일반 기업 Value Chain 지속 가능성 | 96 |
| PE-STRAT-VC-P2 | PE-STRAT-VC-P2-v4.0.md | 4.0 | B2B SaaS / Platform Moat 분석 | 97 |
| PE-STRAT-MAS | PE-STRAT-MAS-v1.0.md | 1.0 | 다기업 비교 Multi-Agent System | 98 |

## 적용 순서
```
단일 기업 (일반) → PE-STRAT-VC-P1-v3.0
단일 기업 (SaaS) → PE-STRAT-VC-P2-v4.0
다기업 비교      → PE-STRAT-MAS-v1.0
보고서 생성      → PE-06 --template porter_vc / saas_moat / saas_moat_mas
```

## Notion 연계 위치
- `C-33 PE-STRAT` 하위 > `Porter ValueChain Suite` 페이지
- PE-IP (통합 라이브러리) 인덱스 자동 등록 대상

## Report Integration Hook
모든 AI Ecosystem Intelligence 심층 보고서에 적용 가능:
```bash
# PE-06 보고서 생성 시 템플릿 지정
python automation/pe06_report.py \
  --template saas_moat_mas \
  --prompt PE-STRAT-MAS-v1.0 \
  --companies "[기업 리스트]"
```
