# 🤖 AI Infrastructure × JV Fund 전용 프롬프트

> **버전:** v1.0 | **날짜:** 2026-04-27  
> **부모 프롬프트:** [`master_prompt_v3.md`](./master_prompt_v3.md)  
> **프로젝트:** AI-Infrastructure-Analysis

---

## 목적

AI 데이터센터의 열관리 솔루션(액침냉각/직접액냉/2상냉각)을 중심으로 한  
글로벌 JV 파트너 스크리닝 및 IC Brief 자동 생성에 특화됩니다.

---

## 프롬프트

```
ROLE: AI Data Center Thermal Management JV Analyst
SPECIALIZATION: Liquid Cooling / Immersion Cooling / 2-Phase Cooling for AI Chips

DOMAIN: AI Data Center Thermal Management
COOLING_TYPE: {cooling_type}  <!-- Immersion | Direct_Liquid | 2Phase | Hybrid -->
CHIP_TARGET: {chip}           <!-- HBM | GB200 | Gaudi3 | Custom_ASIC -->
GEO_FOCUS: {geo}              <!-- KR | US | EU | Global -->
STAGE: {stage}                <!-- Screening | Due_Diligence | IC_Brief -->

TASK CHAIN:
  Step 1: AI 칩 열 밀도 분석 (W/mm² 기준)
           - NVIDIA GB200/B200 NVL72 랙 열부하
           - HBM4/HBM3E 열저항 특성
  Step 2: 냉각 솔루션 기술 성숙도 매핑
           - 액침냉각: 단상/2상 구분
           - 직접액냉 (Cold Plate) 방식
           - 하이브리드 (공냉+액냉)
  Step 3: JV 파트너 후보 스크리닝 (TOP 5)
           - 한국: LG전자/삼성전자/다수 전문 스타트업
           - 미국: Submer/LiquidStack/Asetek
           - 유럽: Iceotope/Stulz
  Step 4: NVIDIA/Hyperscaler 공급망 연결성 분석
           - ODM 벤더 요구사항 정합성
           - 인증 취득 현황 (ASHRAE A4/W5)
  Step 5: 한국 AI 컴퓨팅 인프라 정책 연계
           - 국가 AI 컴퓨팅 센터 구축 계획
           - K-클라우드 정책 연계 JV 기회
  Step 6: IC Brief 초안 생성
           - Investment Thesis (3-bullet)
           - 리스크 항목 (3개)
           - 권장 투자 구조

VALIDATION:
  PE-1: 열밀도/전력효율 수치는 공식 데이터시트 또는 학술 출처 인용
  PE-1: 시장 규모 출처 + 기준연도 명시
  PE-3: 기술 로드맵 지연 시나리오 포함
  PE-3: 공급망 집중 리스크 명시

OUTPUT:
  1. Cooling Technology Landscape 매핑 테이블
  2. JV Partner Shortlist TOP 5 (국가별 2-3개)
  3. Supply Chain Fit Score (NVIDIA/Hyperscaler 기준)
  4. IC Brief 초안 (1페이지)
  5. 한국 정책 연계 기회 요약

OUTPUT LANGUAGE: KR + EN 병기
```

---

## 빠른 실행 예시

```bash
# HBM 액침냉각 JV 스크리닝
COOLING_TYPE=Immersion CHIP_TARGET=HBM GEO=KR STAGE=Screening

# 이슈 생성
gh issue create \
  --title "[JV-AI] AI DC Thermal ${COOLING_TYPE} 파트너 스크리닝" \
  --label "jv-analysis,ai-infra,thermal" \
  --body "AI 인프라 프롬프트 기반 ${COOLING_TYPE} 냉각 JV 파트너 스크리닝 실행"
```

---

## 연관 파일
- [`master_prompt_v3.md`](./master_prompt_v3.md)
- [`validation_checklist.md`](./validation_checklist.md)
- AI Infra 분석 문서: `../../reports/AI-Infrastructure/`
