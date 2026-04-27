# CHANGELOG — JV Fund Prompts

> Repository: `GilbertKwak/prompt-engineering-system`  
> Path: `prompts/jv_fund/`  

---

## [v3.0.0] — 2026-04-28

### 🆕 신규 추가
- `master_v3.md` — 파라미터화된 JV 펀드 마스터 프롬프트 v3
- `fu_series_adapter.md` — FU-Series 보고서 연동 어댑터
- `bstar_eco2_prompt.md` — B-Star eCO2 전용 JV 전략 프롬프트
- `ai_infra_prompt.md` — AI 인프라/데이터센터 열관리 JV 프롬프트
- `CHANGELOG.md` — 버전 이력 관리 파일

### ✅ 검증 기준 적용
- PE-1 (데이터 품질): 모든 프롬프트에 출처 명기 규칙 적용
- PE-3 (시나리오 균형): master_v3, bstar_eco2, ai_infra에 반대 시나리오 필드 추가

### 🔧 구조 개선 (vs v2)
| 항목 | v2 (원본) | v3 (개선) |
|------|-----------|----------|
| 프롬프트 구조 | 단일 블록 텍스트 | ROLE/PARAMS/CHAIN/OUTPUT 분리 |
| 버전 관리 | 없음 | CHANGELOG + 버전 헤더 |
| 언어 | 영문 단일 | KR+EN 병기 |
| 검증 기준 | 없음 | PE-1 / PE-3 체크리스트 |
| 출력 포맷 | 미지정 | JSON 스키마 명시 |
| 파라미터화 | 없음 | YAML 파라미터 블록 |
| 도메인 분리 | 통합 단일 | 4개 도메인 전용 파일 |
| 프롬프트 연동 | 없음 | 교차 참조(CROSS-REFERENCE) 명시 |

---

## [v2.0.0] — 2026-04-27 (원본 보관)

### 원본 파일
- `Global_Joint_Venture_Fund_Master_Prompt_v2.txt`
- 위치: 첨부 파일 (Perplexity 분석 세션)

### 주요 내용
- 글로벌 JV 펀드 분석을 위한 초기 마스터 프롬프트
- 단일 블록 구조, 영문 작성

---

## [향후 계획]

### v3.1.0 (예정: 2026-05)
- [ ] `auto_validate.py` PE-1/PE-3 자동 검증 연동
- [ ] GitHub Actions 워크플로우 추가 (push → validate)
- [ ] Notion 동기화 스크립트 연동

### v4.0.0 (예정: 2026-07)
- [ ] LLM API 직접 호출 지원 (OpenAI / Claude / Perplexity)
- [ ] 분석 결과 자동 Notion DB 저장
- [ ] 월간 시장 데이터 자동 업데이트

---

## [기여 가이드]

```bash
# 신규 프롬프트 추가 시
git checkout -b feat/prompts-jv-{domain}
# 작성 후
git commit -m "feat(prompts/jv_fund): Add {domain} variant prompt v{X.Y.Z}"
git push origin feat/prompts-jv-{domain}
gh pr create --title "JV Prompt: {domain} variant"
```
