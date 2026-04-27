# 💼 JV Fund Prompt Library v3.0

> **목적**: 글로벌 합작투자(JV) 펀드 분석을 위한 최적화 프롬프트 라이브러리  
> **버전**: v3.0 | **생성일**: 2026-04-27  
> **Notion SSOT**: [PE-JV · Global JV Fund Prompt Library](https://www.notion.so/34f55ed436f081c08fececa8dd7577f9)

---

## 📁 파일 구조

```
prompts/jv_fund/
├── README.md              ← 이 파일 (인덱스 + 사용 가이드)
├── master_v3.md           ← 🔷 Master Prompt (핵심)
├── fu_adapter_v1.md       ← 🔷 FU-Series 연동 어댑터
├── bstar_eco2_v1.md       ← 🔷 B-Star sCO2 전용
└── ai_infra_v1.md         ← 🔷 AI 인프라 전용
```

---

## 📋 Quick Reference

| 파일 | 버전 | 도메인 | 검증룰 | 상태 |
|---|---|---|---|---|
| `master_v3.md` | v3.0 | All | PE-1+PE-3 | ✅ Active |
| `fu_adapter_v1.md` | v1.0 | HBM/Thermal | PE-1 | ✅ Active |
| `bstar_eco2_v1.md` | v1.0 | sCO2 Energy | PE-1 | ✅ Active |
| `ai_infra_v1.md` | v1.0 | AI DC | PE-1+PE-3 | ✅ Active |

---

## 🚀 사용법

### 1. 기본 실행 (Master Prompt)
```bash
# 파라미터 지정 후 AI 도구에 master_v3.md 내용 + 파라미터 입력
DOMAIN=HBM STAGE=Screening LANG=KR DEPTH=Executive
```

### 2. 검증 실행
```bash
python automation/auto_validate.py \
  --file prompts/jv_fund/master_v3.md \
  --rules PE-1,PE-3
```

### 3. Notion 동기화
```bash
python automation/notion_sync.py \
  --page-id 34f55ed436f081c08fececa8dd7577f9 \
  --file prompts/jv_fund/master_v3.md
```

---

## 📅 CHANGELOG

| 버전 | 날짜 | 내용 |
|---|---|---|
| v3.0 | 2026-04-27 | 최초 생성 — PE-1/PE-3 통합, 4개 도메인 프롬프트 구축 |
| v2.0 | (origin) | `Global_Joint_Venture_Fund_Master_Prompt_v2.txt` 원본 |

---

## 🔗 관련 링크

- [Notion PE Hub](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b)
- [PE-JV Notion Page](https://www.notion.so/34f55ed436f081c08fececa8dd7577f9)
- [FU-Series Reports](https://github.com/GilbertKwak/prompt-engineering-system/tree/main/applied-cases)
