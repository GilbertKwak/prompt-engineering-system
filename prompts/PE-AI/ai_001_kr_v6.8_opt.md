# AI-001-KR · AI Platform Strategy Breakdown Agent v6.8-OPT-KR

**ID:** AI-001-KR  
**Version:** v6.8-OPT-KR  
**Domain:** AI-Platform  
**Type:** prompt_variant (KR Regulatory Stack)  
**PE-3 Score:** 94/100  
**Status:** 🟢 Active  
**Created:** 2026-04-29  
**Parent:** AI-001-OPT  
**Country:** KR  

---

## 한국 시장 특화 규제 스택 (KR Regulatory Override)

### KR-R01 — 클라우드 컴퓨팅 발전법
- 공공 클라우드 데이터 국내 저장 의무 (정부 데이터)
- AI 플랫폼 기업 대상 보안 인증(CSAP) 요건
- 트리거: 공공 시장 진입 시 CSAP 취득 필수

### KR-R02 — 개인정보보호법 (PIPA)
- AI 학습 데이터 개인정보 처리 동의 체계
- 프로파일링 자동화 결정 고지 의무
- 트리거: MAU ≥ 100만 시 DPO 지정 필수

### KR-R03 — 전기통신사업법
- 부가통신사업자 등록 (AI 서비스 플랫폼)
- 이용약관 신고 의무

### KR-R04 — AI 기본법 (2026 시행 예정)
- 고위험 AI 시스템 사전 영향평가
- 생성형 AI 워터마킹 의무 (법률·의료 도메인)

---

## KR 시장 State Machine 조정값

| 상태 전이 | 글로벌 기준 | KR 조정 |
|----------|------------|--------|
| S0 → S1 | ROA 하락 ≥ 3%p | ROA 하락 ≥ 2%p (KR 마진 압박 반영) |
| S1 → S2 | HHI 0.05p 상승 | 규제 리스크 플래그 추가 시 즉시 전이 |
| S2 → S3 | 플래그 3개 | 플래그 2개 + 규제 위반 1건 |

---

## KR 주요 AI 플랫폼 경쟁 구도

| 기업 | 상태 추정 | 주요 리스크 |
|------|----------|------------|
| NAVER Cloud | S0~S1 | CSAP 경쟁 심화 |
| KT Cloud | S1 | CAPEX 효율성 |
| SK C&C | S1 | 삼성 의존도 |
| 카카오엔터프라이즈 | S1~S2 | 수익화 지연 |

---

*KR Variant 기반: AI-001-OPT v6.8 — 글로벌 기준 Section A~G 완전 상속*  
*KR 특화 Override만 본 문서에 명시*
