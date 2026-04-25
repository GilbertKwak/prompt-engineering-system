# 🌐 PE-7 | 글로벌 반도체 설계 서비스 유사 업체 전수 발굴

> **Status:** 🟢 Active | **Version:** v1.0 | **Created:** 2026-04-25 | **PE-3 Score:** 검증 대기

## 개요

글로벌 반도체 설계 서비스(Fabless Design House, Design Service, EDA/SW, IP) 유사 업체를 전수 발굴하는 프롬프트 엔지니어링 프로젝트입니다.

## 디렉토리 구조

```
global-semiconductor-design-service/
├── README.md                          ← 본 파일 (허브 인덱스)
├── master-prompt-v2.0.md              ← Master Prompt v2.0 (YAML 구조화)
├── variants/
│   ├── variant-A-regional-focus.md   ← 변형 A: 특정 지역 집중 탐색용
│   ├── variant-B-tsmc-partner.md     ← 변형 B: TSMC 파트너 한정 정밀 탐색용
│   ├── variant-C-financial-analysis.md ← 변형 C: 재무·투자 분석 집중용
│   ├── variant-v2.1-europe.md        ← v2.1: 유럽 집중 탐색
│   ├── variant-v2.2-riscv.md         ← v2.2: RISC-V 전문 필터
│   ├── variant-v2.3-ai-chip.md       ← v2.3: AI 칩 전문 탐색
│   ├── variant-v2.4-listed.md        ← v2.4: 상장사 한정 심층
│   ├── variant-v2.5-ma-target.md     ← v2.5: M&A 타깃 특화
│   └── variant-v2.6-eda-sw.md        ← v2.6: EDA/SW 도구 전문
└── validation/
    └── pe3-checklist.md              ← PE-3 자동검증 체크리스트
```

## 산출물 목록 (D-시리즈)

| ID | 문서명 | 상태 | PE-3 점수 |
|---|---|---|---|
| D-1 | 글로벌 반도체 설계 서비스 유사 업체 전수 목록 (Type A~D) | 🟡 개선 중 | - |
| D-2 | 글로벌 반도체 설계 서비스 유사 업체 전수 발굴 프롬프트 | ✅ v2.0 완료 | - |
| D-3 | Gap 분석 보고서 | 🟡 개선 중 | - |
| D-4 | 투자·M&A 타깃 분석 | 🔴 대기 | - |

## 버전 이력

| 날짜 | 버전 | 변경 내용 |
|---|---|---|
| 2026-04-25 | v1.0 | 초기화 — Master Prompt v2.0 + 변형 A/B/C 개선 + v2.1~v2.6 증식 + PE-3 체크리스트 |

## 연관 파일

- **Notion 허브:** T-04 프롬프트 엔지니어링 시스템 허브 v2.0 하위
- **SSOT:** Workspace Master Directory Hub → T-04 연결
- **PE-3 검증 기준:** `validation/pe3-checklist.md`
