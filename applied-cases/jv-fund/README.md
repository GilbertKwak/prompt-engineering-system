# PE-JV · Global Joint Venture Fund Prompt Library

> **Version**: v3.0 | **Updated**: 2026-04-28 | **Author**: Gilbert  
> **Notion Sync**: [PE-JV Notion Page](https://notion.so/34f55ed436f08150b07dc7f5f800311b)  
> **Status**: ✅ Active

---

## 📂 Directory Structure

```
applied-cases/jv-fund/
├── master_prompt_v3.md          ← 메인 마스터 프롬프트 (현행)
├── fu_series_adapter.md         ← FU-Series 보고서 연동 프롬프트
├── bstar_eco2_prompt.md         ← B-Star sCO2 전용 JV 프롬프트
├── ai_infra_prompt.md           ← AI 인프라 데이터센터 JV 프롬프트
├── validation_checklist.md      ← PE-1/PE-3/PE-5 체크리스트
├── CHANGELOG.md                 ← 버전 이력
├── archive/
│   └── v2/                      ← v2 원본 보관
└── variants/                    ← 추가 도메인 파생본 (확장용)
```

---

## 🚀 Quick Start

```bash
# 1. 검증 실행
python automation/auto_validate.py \
  --file applied-cases/jv-fund/master_prompt_v3.md \
  --rules PE-1,PE-3,PE-5

# 2. 전체 JV 파일 일괄 검증
python automation/auto_validate.py \
  --dir applied-cases/jv-fund/ \
  --rules PE-1,PE-3,PE-5 \
  --output validation_report.json

# 3. GitHub Issue 생성 (JV 분석 시작)
gh issue create \
  --title "[JV Analysis] {domain} - {stage}" \
  --label "jv-analysis,{domain}"
```

---

## 📋 Prompt Files

| 파일 | 버전 | 용도 | 검증 규칙 |
|---|---|---|---|
| `master_prompt_v3.md` | v3.0 | 범용 JV 분석 마스터 | PE-1, PE-3, PE-5 |
| `fu_series_adapter.md` | v2.0 | FU-Series 보고서 연동 | PE-1, PE-3 |
| `bstar_eco2_prompt.md` | v2.0 | sCO2 에너지 JV | PE-1, PE-3 |
| `ai_infra_prompt.md` | v2.0 | AI DC 열관리 JV | PE-1, PE-3 |

---

## 🔄 Workflow

```
프롬프트 수정
    ↓
git push → GitHub Actions 자동 실행
    ↓
PE-1/PE-3/PE-5 검증 (auto_validate.py)
    ↓
검증 통과 → Notion 자동 동기화
    ↓
validation_report.json 아티팩트 저장
```

---

## ⚙️ GitHub Secrets 설정 (Notion Sync 활성화)

```
Settings → Secrets → Actions 에서 추가:
  NOTION_TOKEN        ← Notion Integration Token
  NOTION_JV_PAGE_ID   ← 34f55ed436f08150b07dc7f5f800311b
```

---

## 📌 Related

- [PE-11 Master Multi-Agent Prompt](../PE-11-master-multi-agent/)
- [HBM Salvage Prompts](../hbm-salvage/)
- [B-Star eCO2 Strategy](../global-semi-ai-energy/)
