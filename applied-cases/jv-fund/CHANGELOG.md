# 📋 JV Fund Prompt — 변경 이력

> **관리:** GitHub SSOT | **Notion 연동:** [PE-JV · Global JV Fund Prompt Library v3.1](https://www.notion.so/34f55ed436f08150b07dc7f5f800311b)

---

## [v3.1] — 2026-04-27

### 🔧 개선
- `master_prompt_v3.md`: v3.0 → v3.1 업그레이드
  - `<parameters>` 블록에 `DATE: {date}` 파라미터 추가
  - 태그명 `v3` → `v3_1` 갱신
  - v2 vs v3 vs v3.1 **3열 전후 비교 테이블** 추가
  - **저장소 이원화 전략 테이블** 추가 (Notion Hub / GitHub Engine 원칙)
  - **alias 4종** 추가 (`jv-validate`, `jv-sync`, `jv-new`, `jv-review`)
  - Notion 링크 v3.1 반영

### 📚 CHANGELOG.md 업데이트
- v3.1 항목 추가
- 향후 로드맵 v3.1 예정 날짜 갱신 (실제 완료 상태로 변경)

### 🔗 트리거
- 원본 체크리스트: `Global_Joint_Venture_Fund_Master_Prompt_v2.txt` 자동검증·자동개선·자동증식 사이클 적용 완료
- Notion [PE-JV 페이지](https://www.notion.so/34f55ed436f08150b07dc7f5f800311b) v3.1 동기화 완료

---

## [v3.0] — 2026-04-27

### 🆕 신규 추가
- `master_prompt_v3.md`: 원본 v2 완전 개선판 생성
  - Role/Parameters/TaskChain/Validation 구조 분리
  - {domain}/{stage}/{depth}/{lang} 파라미터 주입 지원
  - PE-1 (6개) / PE-3 (5개) 검증 룰 명시
  - KR + EN 병기 출력 포맷 추가
  - Notion DB Entry / GitHub Issue 출력 형식 추가
- `fu_series_adapter.md`: FU-Series 보고서 연동 파생 프롬프트 신규
- `bstar_eco2_prompt.md`: B-Star sCO2 JV 전략 특화 프롬프트 신규
- `ai_infra_prompt.md`: AI 데이터센터 열관리 JV 분석 프롬프트 신규
- `validation_checklist.md`: PE-1/PE-3/SQ 통합 검증 체크리스트 신규
- `CHANGELOG.md`: 이 파일

### 🔧 개선
- v2 단일 XML → v3 모듈화 구조로 전환
- 영문 단일 → KR+EN 병기 출력 지원
- 고정 콘텐츠 → 파라미터화 (재사용성 향상)

### 📁 파일 구조
```
applied-cases/jv-fund/
├── master_prompt_v3.md       # 핵심 마스터 프롬프트 (v3.1)
├── fu_series_adapter.md      # FU-Series 연동 어댑터
├── bstar_eco2_prompt.md      # B-Star eCO2 전용
├── ai_infra_prompt.md        # AI 인프라 전용
├── validation_checklist.md   # PE-1/PE-3 검증 체크리스트
├── CHANGELOG.md              # 이 파일
└── archive/                   # 구버전 보관
└── variants/                  # 도메인 파생본
```

---

## [v2.0] — 2026-04 이전 (원본 보관)

### 원본 특성
- 단일 XML 블록 구조
- 8개 core_modules (GP/LP/Structuring/Sizing/IC/Value/Exit/Risk)
- 영문 단일 출력
- 검증 기준 없음
- 파라미터화 없음

### 원본 파일
- `Global_Joint_Venture_Fund_Master_Prompt_v2.txt` (보관용)

---

## 향후 로드맵

| 버전 | 예정 날짜 | 내용 |
|---|---|---|
| v3.1 | 2026-04-27 ✅ **완료** | 자동검증 사이클, alias, 이원화 전략 |
| v3.2 | 2026-05 | `auto_validate.py` JV 전용 룰셋 추가 |
| v3.3 | 2026-06 | GitHub Actions 워크플로우 고도화 |
| v4.0 | 2026-Q3 | Multi-Agent 연동 (PE-11 시스템 통합) |
