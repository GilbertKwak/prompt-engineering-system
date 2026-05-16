---
id: PE-STRAT-ECOSYSTEM-SOP-v1
version: 1.0
created: 2026-05-16
domain: PE-STRAT
tags: [sop, ecosystem, apply, report, automation, notion, github]
---

# AI Ecosystem Intelligence 보고서 최적화 프롬프트 자동 적용 SOP v1.0

## 목적
Notion & GitHub에 구축된 모든 심층 보고서 항목에
PE-STRAT 최적화 프롬프트를 **자동으로 적용**하는 표준 운영 절차.

---

## 적용 대상 보고서 유형
| 보고서 유형 | 적용 프롬프트 | 자동화 수준 |
|-----------|------------|------------|
| AI Ecosystem Intelligence | PE-STRAT-MOAT-v2 | 자동 (주 1회 스케줄) |
| 반도체 경쟁우위 분석 | PE-STRAT-VC-S-v4 | 이벤트 드리븐 |
| B2B SaaS DD 보고서 | PE-STRAT-VC-SAAS-v5 | 수동 트리거 |
| JV Fund 포트폴리오 리뷰 | PE-STRAT-MOAT-v2 + PE-FIN | 자동 (월 1회) |
| GNN 리스크 감시 보고서 | PE-STRAT-VC-S-v4 | 이벤트 드리븐 |

---

## 실행 플로우

```
[이벤트/스케줄 트리거]
        ↓
 PE-00 Orchestrator
        ↓
   대상 프롬프트 선택
   (보고서 유형 기반)
        ↓
 Company Analyzer 실행
 (PE-STRAT-MOAT-v2 or VC-S-v4)
        ↓
 PE-11 Validation
        ↓
  pe-score ≥ 85?
  YES → Notion 자동 동기화
  NO  → 재정제 루프 (최대 3회)
        ↓
 GitHub 커밋 (docs/reports/)
        ↓
  Notion DB 업데이트
 (PE-STRAT 라이브러리 페이지)
```

---

## GitHub Actions 트리거 예시
```yaml
# .github/workflows/strat_moat_weekly.yml
name: STRAT Moat Analyzer Weekly
on:
  schedule:
    - cron: '0 9 * * 1'   # 매주 월요일 09:00 KST
  workflow_dispatch:

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Moat Analyzer
        run: |
          python automation/run_prompt.py \
            --prompt PE-STRAT-MOAT-v2 \
            --companies "$COMPANY_LIST" \
            --output docs/reports/moat_$(date +%Y%m%d).md
      - name: Validate
        run: python automation/auto_validate.py --input docs/reports/
      - name: Sync to Notion
        run: python automation/notion_sync.py --page PE-STRAT-라이브러리
```

---

## Notion 저장 위치
| 프롬프트 | 저장 위치 | 뷰 유형 |
|---------|---------|--------|
| PE-STRAT-VC-S-v4 | PE-STRAT 라이브러리 > 경쟁우위분석 섹션 | 테이블 뷰 |
| PE-STRAT-VC-SAAS-v5 | PE-STRAT 라이브러리 > SaaS경쟁우위 섹션 | 테이블 뷰 |
| PE-STRAT-MOAT-v2 | PE-STRAT 라이브러리 > Moat비교분석 섹션 | 보드 뷰 |
| ECOSYSTEM-SOP-v1 | SOP 마스터 페이지 > 자동화 SOP 섹션 | 리스트 뷰 |

---

## 연계 페이지
- [PE-STRAT-P1-OPT-v2.0](https://www.notion.so/35c55ed436f081049030e23691f7444f)
- [PE-STRAT-JV-P1-v1.0](https://www.notion.so/35c55ed436f081b18d61fabcd606c316)
- [C-33 PE-STRAT 국가전략 감시 라이브러리](https://www.notion.so/35255ed436f0810f830be1feb1512c28)
