# CHANGELOG — JV Fund Prompts

> 모든 버전 변경 이력을 기록합니다.

---

## [v6.0.0] — 2026-04-28

### 🚀 Major Release
- **완전 재설계**: Role/Context/Chain/Output/Validation 5-Layer 구조 도입
- **PE-1/PE-3 내장**: 외부 검증 의존 제거, 프롬프트 자체 검증 룰 포함
- **완전 파라미터화**: `{DOMAIN}`, `{STAGE}`, `{LANG}`, `{DEPTH}` 등 7개 파라미터
- **이중 출력 포맷**: JSON + Notion-MD 동시 지원
- **3-Engine 연동**: Auto-Refinement / Auto-Proliferation / Auto-Validation 명시적 연동
- **도메인 어댑터 통합**: HBM/sCO2/Thermal/AI-DC 4개 도메인 분기 내장
- **KR/EN 병기**: 모든 출력 한국어+영어 동시 지원
- **원본 v2 아카이빙**: `archive/Global_Joint_Venture_Fund_Master_Prompt_v2.txt`
- **GitHub Issue 명령어**: 분석 결과에서 바로 Issue 생성 가능

### 📁 파일 변경
- 추가: `master_prompt_v6.md`
- 추가: `archive/Global_Joint_Venture_Fund_Master_Prompt_v2.txt`
- 업데이트: `CHANGELOG.md`

### 🔗 트리거
- 입력: `Global_Joint_Venture_Fund_Master_Prompt_v2.txt` 분석 요청
- 실행: Perplexity AI × prompt-engineering-system 3-Engine
- 검증: PE-1(사실정확성) + PE-3(균형분석) 통과

---

## [v5.0.0] — 이전 버전

- `master_prompt_v5.md` 참조

## [v4.0.0] — 이전 버전

- `master_prompt_v4.md` 참조

## [v3.0.0] — 이전 버전

- `master_prompt_v3.md` 참조

## [v2.0.0] — ARCHIVED

- 원본: `archive/Global_Joint_Venture_Fund_Master_Prompt_v2.txt`
- 아카이브 사유: v6.0.0 출시에 따른 보관

---

*Maintained by GilbertKwak/prompt-engineering-system*
