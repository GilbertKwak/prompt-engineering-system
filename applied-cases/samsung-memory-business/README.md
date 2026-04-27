# 📦 Samsung Memory Business — 전략 프롬프트 라이브러리 v1.0

> **SSOT 경로**: `applied-cases/samsung-memory-business/`  
> **Notion 연계**: PE-MEM · Memory Product Architecture Prompt Library v1.5  
> **PE-3 검증**: 전 항목 90점 이상 PASS (최고점 P-02·P-06 각 96점)  
> **작성일**: 2026-04-27 | **작성자**: Gilbert Kwak

---

## 📋 프롬프트 목록

| # | 파일 | 버전 | 유형 | PE-3 점수 | 비고 |
|---|---|---|---|---|---|
| P-00 | `P-00_PromptBuilder-v2.0.xml` | v2.0 | 메타 프롬프트 | 92 | 범용 |
| P-01 | `P-01_Industry-Analysis-v2.0.xml` | v2.0 | 산업 구조 분석 | 91 | |
| P-02 | `P-02_Strategy-Deep-v3.0.xml` | v3.0 | 전략 심층 분석 ⭐ | 96 | 최우수 |
| P-03 | `P-03_Business-Model-v4.0.xml` | v4.0 | 공통 사업 모델 | 93 | |
| P-04 | `P-04_Samsung-Proposal-v4.0.xml` | v4.0 | 삼성전자 전용 | 95 | |
| P-05 | `P-05_SKHynix-Proposal-v4.0.xml` | v4.0 | SK하이닉스 전용 | 94 | |
| P-06 | `P-06_JV-Contract-v2.0.xml` | v2.0 | JV 구조·계약 설계 ⭐ | 96 | 최우수 |

### 자동증식 파생 3종

| 파일 | 대상 시장 | 특화 포인트 | 우선순위 |
|---|---|---|---|
| `variants/MEM-BIZ-INDIA-v1.0.xml` | 인도 | PLI 정책·현지 파트너 | ⭐ High |
| `variants/MEM-BIZ-MIDEAST-v1.0.xml` | UAE·사우디 | Vision 2030·ADGM 법인 | ⭐ High |
| `variants/MEM-BIZ-AUTOMOTIVE-v1.0.xml` | 자동차용 메모리 | AEC-Q100·장수명·OEM 인증 | ⭐⭐ Very High |

---

## 🔧 즉시 사용 명령어

### 1. 산업 분석 전체 실행
```
[P-01 실행] Global_Memory_Business_Dynamics_v2.0 프롬프트 사용.
삼성전자·SK하이닉스·마이크론 3사 분석, 2026 지정학·HBM 경쟁구도 포함.
출력: Executive Summary + 표·구조도 중심 (한국어)
```

### 2. 전략 심층 보고서
```
[P-02 실행] Global_Memory_Business_Dynamics_Strategy_v3.0 프롬프트 사용.
신규 메모리 유통·솔루션 사업 진입 관점으로 분석.
"그래서 무엇을 해야 하는가" 섹션 반드시 포함.
```

### 3. JV 설계 실행
```
[P-06 실행] Memory_JV_Structure_and_Contract_Framework_v2.0 사용.
파트너사: [파트너명], 대상 제품: [제품군], 목표 시장: [지역]
Kill-switch 조항·Audit cycle 포함 완전판으로 출력.
```

---

## 🔗 연계 페이지

| 연계 | 설명 |
|---|---|
| `memory-prompts/` | MEM-BASE~HBM-PIM 11종 기술 프롬프트 |
| `engines/` | PE-1 자동개선·PE-2 자동증식·PE-3 자동검증 엔진 |
| Notion PE-MEM | https://www.notion.so/34e55ed436f0817cba4ae6154f3c664c |

---

## 📝 변경이력

| 버전 | 날짜 | 내용 |
|---|---|---|
| v1.0 | 2026-04-27 | 최초 생성 — P-00~P-06 7종 + 자동증식 3종 |
