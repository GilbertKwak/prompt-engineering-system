# 📋 Global AI·Semi·Energy 프로젝트 — 프롬프트 버전 이력

> **프로젝트**: 글로벌 반도체·AI·에너지 산업 통합 시나리오 분석 보고서  
> **기간**: 2026년 2월 ~ 2026년 3월  
> **관리**: GitHub (SSOT) ↔ Notion (미러)  
> **연관 Notion 허브**: [🧠 프롬프트 엔지니어링 시스템 v2.0](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b)  
> **최종 업데이트**: 2026-04-26  

---

## 🗂️ 버전 인덱스

| 버전 | 명칭 | 날짜 | 핵심 목적 | 상태 |
|------|------|------|-----------|------|
| v1 | Agent 3 시나리오 프레임워크 v4 개발 | 2026-02-10 | 4-World 시나리오 구조 수립 | ✅ 완료 |
| v2 | 추가 모듈 추천 | 2026-03-02 | 5개 전략·재무 모듈 설계 | ✅ 완료 |
| v3 | 워드파일 캔버스 + 차트 생성 | 2026-03-02 | 5개 docx + 20개 PNG 생성 | ✅ 완료 |
| v4 | 국가·레이어 딥다이브 캔버스팩 | 2026-03-02 | 미국/중국/대만 완성본 생성 | ✅ 완료 |
| v5 | Agent 1/2 수치 추출 및 인덱스 | 2026-03-02 | WSPM·투자액·비중 정량 정리 | ✅ 완료 |
| v6 | SMR·에너지 연계 | 미진행 | 반도체 시나리오 + SMR IRR 연결 | 🔵 대기 |

---

## 📌 v1 — Agent 3 시나리오 프레임워크 v4 개발

**날짜**: 2026-02-10  
**목적**: Agent 2 분석 결과를 기반으로 4-World 확률 시나리오 프레임워크를 v3 대비 7가지 개선 포함 v4로 업그레이드

### 프롬프트 본문

```
Agent 2 분석을 기반으로 Agent 3 Scenario Framework v4를 개발하겠습니다.
v3 대비 7가지 핵심 개선 사항을 포함합니다.

[개선 사항]
1. 확률 모델: 단순 점 추정 → 베이지안 업데이트 + 조건부 확률 트리
2. 시나리오 전환: 선형적 경로 → 분기점(Bifurcation) 타임라인 + 복합 시나리오
3. 정량 지표: 점 추정값 → 신뢰구간 (P10/P50/P90)
4. 조기경보: 정적 지표 40개 → 동적 대시보드 + 월간 업데이트 프로토콜
5. 전략 매트릭스: 국가별 영향 분석 → 결정 트리 + 최적 대응 경로
6. 역사적 검증: 부재 → 유사 사례 매핑 (5개 역사적 전환점)
7. 복합 시나리오: 단일 World 분석 → 하이브리드 시나리오 (A+D, B+C 등)
```

### 출력 결과

- PHASE 3.1~3.7 상세 구조
- 4-World 확률 업데이트 (World A 5%, B 45%, C 35%, D 15%)
- 분기점 5개 정의
- 복합 시나리오 (A+D, B+C)
- 대시보드 SOP + 조기경보 40개 지표

---

## 📌 v2 — 추가 모듈 추천

**날짜**: 2026-03-02  
**목적**: Agent 3 프레임워크 완성 후 실용성 확장을 위한 5개 추가 모듈 식별 및 우선순위화

### 프롬프트 본문

```
추가 진행 추천

→ 목표 5개 축:
1. "Scenario → 전략/액션" 연결 모듈
2. 재무·밸류에이션 모듈 (CFO View)
3. AI-Driven 시나리오 엔진 / Implementation Guide
4. "전략 실험실 (Strategy Lab)" 모듈
5. 조기경보 지표 메타-검증 + 리스크 인덱스
```

### 출력 결과

- 5개 모듈 상세 설명 + 우선순위
- 추천 순서: 숫자 인덱스 → Fact Sheet v2 → SMR-Fab-DC 연결

---

## 📌 v3 — 워드파일 캔버스 + 차트 생성

**날짜**: 2026-03-02  
**목적**: 5개 모듈을 docx 캔버스 형태로 작성하고, 필요 차트 전체 생성

### 프롬프트 본문

```
각각에 대해 워드파일 캔버스 형태로 docx 파일 작성
(이미지, 표, 차트 등을 삽입)

→ 작성된 자료를 검토해서 각 파일에 필요한 이미지, 차트 등을 모두 생성
→ 계속작성

[5개 캔버스 대상]
1. Strategy_Action_Canvas
2. Financial_Valuation_Module
3. AI_Engine_Implementation_Guide
4. Strategy_Lab_Module
5. EWS_Meta_Risk_Index

각각: 표 3개(개요, KPI, 타임라인) + 차트 삽입 위치 포함
차트 20개 생성 (2x2 맵, Heatmap, Radar, Fan Chart, Waterfall 등)
```

### 출력 결과

| 산출물 유형 | 수량 | 내용 |
|-------------|------|------|
| docx 캔버스 | 5개 | Strategy/Financial/AI/Lab/EWS |
| PNG 차트 | 20개 | 4-World 포지셔닝, HBM 매출 범위, Bayesian 네트워크, Taiwan Risk Index 등 |

---

## 📌 v4 — 국가·레이어 딥다이브 캔버스팩

**날짜**: 2026-03-02  
**목적**: 12개국 × 10개 레이어 분석 결과를 국가별 전용 캔버스팩 + 레이어별 딥다이브로 시각화

### 프롬프트 본문

```
[요청 1] 국가·기업별 전용 캔버스팩 + 레이어별 딥다이브 캔버스
→ 추천 내용에 대한 심층 보고서 실제 작성
→ Agent 1/2 수치 삽입 완성형
→ 미국/중국/대만 상세 보고서

[국가 캔버스팩 구성] (한국/미국/중국/대만/일본)
- 1장 요약 캔버스
  - 국가 프로파일, 레이어 점수, 병목·레버리지, 3대 전략 질문, 핵심 수치
- 4-World 전개
  - 포지션 매트릭스, 손익 스냅샷, 시퀀스 타임라인
- 액션 리스트 (No-regret + World별 옵션)

[레이어 딥다이브 대상] L1/L5/L6/L7/L8
- 병목 구조 도식
- World별 리스크 곡선
- 완화 옵션 매트릭스

[Agent 1/2 핵심 수치 삽입 기준]
- TSMC 2nm 100K WSPM
- 한국 HBM 82% (SK hynix 54% + 삼성 28%)
- 희토류: 중국 67% 생산 / 85% 정제
- 미국 희토류 11.6%
- Fab 투자: TSMC Arizona $165B
- 일본 EUV 포토레지스트 90%
```

### 출력 결과

- `Agent3_Deep_Report_Canvas.docx` (구조 캔버스)
- `Agent3_US_China_Taiwan_Integrated_Report.docx` (미국/중국/대만 완성본)

---

## 📌 v5 — Agent 1/2 수치 추출 및 인덱스

**날짜**: 2026-03-02  
**목적**: Agent 1/2 첨부파일에서 WSPM·투자액·점유율·비중 정량 수치 전체 추출 및 레이어별 정리

### 프롬프트 본문

```
Agent 1/2 테이블에 있는 구체 수치 (WSPM, 투자액, 비중 등)에 대해 출력

[첨부 파일]
- Agent-1-Phase-2-bogoseo_12gaegug-x-10gae-reieo.md
- Agent-2-Multi-Layer-Structural-Analyst.md
- 01_06_12_Global_AI_Semi_Energy_Integrated_Report.md

[추출 대상]
- L1: 희토류 생산량·점유율 (국가별)
- L2: 소재 시장 규모·점유율 (일본 중심)
- L3: Fab 투자액·전력 수요 (국가별)
- L4: 용수 소비량·재이용률
- L5: HBM 시장 점유율·성장률
- L6: WSPM (Wafers per Month) 국가·기업별
- L8: 데이터센터·AI 인프라 투자액
```

### 핵심 추출 수치 요약

| 레이어 | 국가/기업 | 지표 | 수치 |
|--------|-----------|------|------|
| L1 | 중국 | 희토류 생산 | 270,000톤/년 (67%) |
| L1 | 중국 | 희토류 정제 | 85~90% 글로벌 |
| L1 | 미국 | 희토류 생산 | 45,000톤/년 (11.6%) |
| L2 | 일본 | EUV 포토레지스트 점유율 | 90% |
| L2 | 일본 | EUV 포토레지스트 시장 | $176~296M (2024) |
| L3 | TSMC | Arizona 투자 | $165B (3개 Fab) |
| L3 | TSMC | Phoenix 전력 수요 | 1,500MW |
| L3 | Intel | Columbus 투자 | $100B (8개 Fab) |
| L3 | 중국 | ACP100 SMR 투자 | ~$1.5B |
| L4 | TSMC | 연간 용수 사용 | 1억 400만 m³ |
| L4 | TSMC | 용수 재이용률 | 86% (2024) → 90% (2030) |
| L4 | 싱가포르 | NEWater 비중 | 국가 용수 40% |
| L5 | 한국 | HBM 시장 점유율 | 82% (SK 54% + 삼성 28%) |
| L5 | 글로벌 | HBM 시장 (2026) | $54.6B (+58% YoY) |
| L6 | TSMC AZ | 2nm WSPM | 100,000 WSPM |
| L6 | 미국 전체 | 첨단공정 추가 WSPM | 115,000 WSPM |
| L8 | 사우디 | NEOM DataVolt | $5B (Phase 1) |
| L8 | 사우디 | 2030년 DC 용량 목표 | 1,300MW |

---

## 📌 v6 — SMR·에너지 연계 (대기)

**날짜**: 미진행  
**목적**: SMR IRR·민감도 분석 결과와 반도체/AI 공급망 시나리오를 연결하는 에너지 투자 의사결정 레이어 구축

### 프롬프트 설계 (초안)

```
[첨부 파일]
- 01_05_19_smr_equity_irr_matrix.csv
- 01_05_19_smr_sensitivity_analysis.csv
- 01_05_19_smr_project_irr_matrix.csv

[요청]
에너지 인프라 투자(원전/SMR)가 Fab·데이터센터 리스크를 어떻게 줄이는지
1~2페이지 정량/시나리오로 작성

[구성]
1. SMR IRR 시나리오 (Base / Bull / Bear)
2. Fab 전력 의존 리스크 수치화
3. SMR 투자 → Fab 가동률 안정 효과 (World A/B/C/D 별)
4. 포트폴리오 최적화: 반도체 + SMR 결합 투자 수익률
```

### 상태

- 🔵 **대기**: SMR CSV 파일 첨부 확인 완료, 상세 분석 미착수
- **추천 우선순위**: 3번째 (숫자 인덱스 → Fact Sheet v2 → SMR 연계)

---

## 🔗 연계 문서

### Notion 페이지

| 페이지명 | URL |
|----------|-----|
| 🧠 프롬프트 엔지니어링 허브 v2.0 | [링크](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b) |
| 🔵 Agent 1: 산업 생태계 매핑 | [링크](https://www.notion.so/30255ed436f081b89712eb9f1ca0b8d6) |
| 🟢 Agent 2: 구조 분석 | [링크](https://www.notion.so/30255ed436f0818881ffe771fc183d2e) |
| 🟠 Agent 3: 4-World 시나리오 | [링크](https://www.notion.so/30255ed436f08161bb3ee2cb66a109b1) |
| 📋 마스터 목록표 v3.0 | [링크](https://www.notion.so/33855ed436f081b3b6b0ce977665e295) |

### GitHub 저장소

| 저장소 | 목적 |
|--------|------|
| [prompt-engineering-system](https://github.com/GilbertKwak/prompt-engineering-system) | 프롬프트 SSOT |
| [global-semiconductor-ai-research](https://github.com/GilbertKwak/global-semiconductor-ai-research) | 반도체 AI 연구 |
| [multi-agent-system-v3-hybrid](https://github.com/GilbertKwak/multi-agent-system-v3-hybrid) | 분석 시스템 v3.0 |

---

## 📊 워크플로우 요약

```
[v1] Agent 3 v4 프레임워크 (4-World, Bayesian, 분기점 5개)
         ↓
[v2] 추가 모듈 추천 (5개 축: Strategy/Financial/AI/Lab/EWS)
         ↓
[v3] docx 캔버스 5개 + PNG 차트 20개 생성
         ↓
[v4] 국가별 캔버스팩 + 레이어 딥다이브 (미·중·대만)
         ↓
[v5] Agent 1/2 수치 인덱스 (L1~L8, 국가·기업별)
         ↓
[v6] SMR-Fab-데이터센터 에너지 연계 ← 🔵 대기
```

---

**문서 관리**: Gilbert Kwak  
**최초 생성**: 2026-04-26  
**다음 업데이트**: v6 SMR 연계 완료 시  
**SSOT**: GitHub (본 파일) → Notion 미러 업데이트  
