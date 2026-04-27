# Global JV Fund — 적용 사례 인덱스

> **생성일**: 2026-04-28  
> **원본 파일**: `Global_Joint_Venture_Fund_Master_Prompt_v2.txt`  
> **현재 버전**: `../../prompts/jv-fund/master_prompt_v3.md`

---

## 개요

글로벌 합작투자 펀드 분석을 위한 프롬프트 적용 사례를 관리하는 디렉터리입니다.  
Master Prompt v3와 3종의 Domain Variant 프롬프트를 기반으로 합니다.

---

## 프롬프트 구조

```
prompts/jv-fund/
├── master_prompt_v3.md              ← 핵심 마스터 프롬프트 (PE-1/PE-3 검증)
├── VALIDATION_CHECKLIST.md          ← 검증 체크리스트
└── variants/
    ├── fu_series_adapter.md         ← FU-Series 보고서 연동
    ├── bstar_eco2_prompt.md         ← B-Star eCO2 전용
    └── ai_infra_prompt.md           ← AI 인프라 데이터센터 전용
```

---

## 연동 레포지토리

| 레포 | 연동 프롬프트 | 용도 |
|---|---|---|
| [fu-semiconductor-thermal](https://github.com/GilbertKwak/fu-semiconductor-thermal) | fu_series_adapter.md | FU 보고서 JV 기회 분석 |
| [B-Star-eCO2-Strategy](https://github.com/GilbertKwak/B-Star-eCO2-Strategy) | bstar_eco2_prompt.md | sCO2 JV 전략 |
| [AstraChips-Strategy](https://github.com/GilbertKwak/AstraChips-Strategy) | ai_infra_prompt.md | AI DC 열관리 JV |
| [global-semiconductor-ai-research](https://github.com/GilbertKwak/global-semiconductor-ai-research) | master_prompt_v3.md | 전체 반도체 JV 분석 |

---

## 빠른 사용 명령어

```bash
# 1. 마스터 프롬프트 검증
python automation/jv_fund_notion_sync.py --mode validate-only

# 2. Notion 동기화
export NOTION_TOKEN='your-token'
python automation/jv_fund_notion_sync.py --mode upsert

# 3. 새 JV 분석 이슈 생성
gh issue create \
  --repo GilbertKwak/prompt-engineering-system \
  --title "[JV-Analysis] {분석 대상}" \
  --label "jv-analysis" \
  --template .github/ISSUE_TEMPLATE/jv_analysis.md

# 4. B-Star eCO2 JV 분석 실행
gh issue create \
  --repo GilbertKwak/B-Star-eCO2-Strategy \
  --title "[JV] sCO2 파트너십 분석 $(date +%Y-%m)" \
  --label "strategy,jv-analysis"

# 5. 월간 프롬프트 리뷰 이슈
gh issue create \
  --repo GilbertKwak/prompt-engineering-system \
  --title "[Monthly-Review] JV Fund Prompt $(date +%Y-%m)" \
  --label "monthly-review,prompt-review"
```

---

## Notion 연동 정보

- **Notion 페이지**: JV Fund Prompt Library (prompt-engineering-system 허브 하위)
- **동기화 방식**: `automation/jv_fund_notion_sync.py` 실행
- **업데이트 주기**: 프롬프트 변경 시 즉시 / 월 1회 정기 리뷰

---

## 변경 이력

| 날짜 | 버전 | 내용 |
|---|---|---|
| 2026-04-28 | v1.0 | 최초 생성 (원본 v2 → v3 마이그레이션) |

---

*관리자: Gilbert Kwak | 문의: GilbertKwak/prompt-engineering-system Issues*
