# 📦 Samsung Memory Business — 전략 프롬프트 라이브러리

> **버전**: v1.0 | **생성일**: 2026-04-27 | **작성자**: Gilbert Kwak  
> **SSOT 연계**: [Notion PE-MEM v1.5](https://www.notion.so/34e55ed436f0817cba4ae6154f3c664c)  
> **PE 엔진**: PE-1 자동개선 · PE-2 자동증식 · PE-3 자동검증 3-Engine 완전 적용

---

## 📂 디렉토리 구조

```
samsung-memory-business/
├── README.md                          ← 이 파일 (인덱스 + 사용법)
├── P-00_PromptBuilder-v2.0.xml        ← 메타 프롬프트 (범용)
├── P-01_Industry-Analysis-v2.0.xml    ← 글로벌 메모리 산업 구조 분석
├── P-02_Strategy-Deep-v3.0.xml        ← 전략 심층 분석 ★ 최우수(96점)
├── P-03_Business-Model-v4.0.xml       ← 공통 사업 모델 프레임
├── P-04_Samsung-Proposal-v4.0.xml     ← 삼성전자 전용 제안서
├── P-05_SKHynix-Proposal-v4.0.xml     ← SK하이닉스 전용 제안서
├── P-06_JV-Contract-v2.0.xml          ← JV 구조·계약 설계 ★ 최우수(96점)
└── variants/
    ├── MEM-BIZ-INDIA-v1.0.xml         ← 인도 시장 특화 (자동증식)
    ├── MEM-BIZ-MIDEAST-v1.0.xml       ← UAE·사우디 특화 (자동증식)
    └── MEM-BIZ-AUTOMOTIVE-v1.0.xml    ← 자동차용 메모리 특화 (자동증식)
```

---

## 📊 프롬프트 검증 결과 (PE-3 Before → After)

| # | 프롬프트 ID | Before | After | 개선폭 | 판정 |
|---|---|---|---|---|---|
| P-00 | PromptBuilder-v2.0 | 74 | 92 | +18 | 🟢 통과 |
| P-01 | Industry-Analysis-v2.0 | 83 | 91 | +8 | 🟢 통과 |
| P-02 | Strategy-Deep-v3.0 ★ | 88 | 96 | +8 | 🟢 최우수 |
| P-03 | Business-Model-v4.0 | 86 | 93 | +7 | 🟢 통과 |
| P-04 | Samsung-Proposal-v4.0 | 90 | 95 | +5 | 🟢 최우수 |
| P-05 | SKHynix-Proposal-v4.0 | 89 | 94 | +5 | 🟢 통과 |
| P-06 | JV-Contract-v2.0 ★ | 89 | 96 | +7 | 🟢 최우수 |

---

## ⚡ 즉시 실행 명령어

### 1. 산업 전체 분석
```
[P-01 실행] P-01_Industry-Analysis-v2.0.xml 프롬프트 사용.
삼성전자·SK하이닉스·마이크론 3사 분석, 2026 지정학·HBM 포함.
출력: Executive Summary + 표·구조도 중심 (한국어)
```

### 2. 전략 심층 보고서
```
[P-02 실행] P-02_Strategy-Deep-v3.0.xml 프롬프트 사용.
신규 메모리 유통·솔루션 사업 진입 관점으로 분석.
"그래서 무엇을 해야 하는가" 섹션 반드시 포함.
대상 사업 모델: [직거래/대리점/트레이딩/JV 중 선택]
```

### 3. JV 설계 즉시 실행
```
[P-06 실행] P-06_JV-Contract-v2.0.xml 사용.
파트너사: [파트너명], 대상 제품: [제품군], 목표 시장: [지역]
Kill-switch 조항·Audit cycle 포함 완전판으로 출력.
법무팀 검토 가능 수준으로 작성.
```

### 4. 지역 특화 변형 실행
```
[PE-2 증식] variants/ 폴더의 [INDIA/MIDEAST/AUTOMOTIVE] 선택.
P-02 Strategy v3.0을 베이스로 지역 특화 조항 적용.
특화 항목: [PLI정책/Vision2030/AEC-Q100] 반드시 포함.
```

---

## 🔗 연계 맵

| 연계 | 사용 프롬프트 | 시나리오 |
|---|---|---|
| PE-4 HBM 불량 재활용 | P-02 Strategy v3.0 | HBM 특수 재활용 사업 분석 |
| PE-7 AI 자동화 | P-01 Industry v2.0 | 경쟁사 메모리 시장 자동 모니터링 |
| PE-8 NOR Flash | P-03 Business Model v4.0 | 신사업 사업성 검토 프레임 재사용 |
| FU Series 보고서 | P-04 / P-05 | 삼성·SK하이닉스 제안서 메모리 섹션 |
| MEM-BIZ 파생 3종 | variants/ | 신규 시장 진출 검토 보고서 자동화 |

---

## 📝 변경 이력

| 버전 | 날짜 | 내용 |
|---|---|---|
| v1.0 | 2026-04-27 | 최초 생성 — P-00~P-06 7종 + variants 3종 + README |

---

> ✅ **[v1.0 \| 2026-04-27 16:57 KST]** SSOT 완성 · PE-3 전 항목 90점 이상 PASS 🟢
