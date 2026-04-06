# 🚀 AI 신사업 발굴 멀티에이전트 프롬프트 시스템 v3.0

> **적용 사례 코드**: `CASE-ABD-001`  
> **버전**: v3.0 (COT + RAG + 자동검증 통합)  
> **최종 업데이트**: 2026-04-06  
> **작성자**: Gilbert Kwak  

---

## 📌 개요

이 디렉토리는 **AI 응용 생태계 신사업 발굴**을 위한 멀티에이전트 프롬프트 시스템의
전체 설계, 개선 이력, 실행 가능한 프롬프트를 저장합니다.

### 핵심 기능
- **자동검증 (Auto-Validation)**: 주장·숫자·가정에 대한 내부 타당성 체크
- **자동검색 (Auto-Search)**: 시장/경쟁/규제 데이터 자동 조회
- **자동추가 (Auto-Augment)**: 누락 항목 자동 보완
- **COT (Chain-of-Thought)**: 단계별 논리적 사고 프로세스 내장
- **RAG (Retrieval-Augmented Generation)**: 과거 패턴·사례·규제 정보 검색 활용

---

## 📂 파일 구조

```
ai-business-discovery/
├── README.md                          ← 이 파일 (개요·구조·사용법)
├── PROMPT_MASTER.md                   ← 단일 실행 가능 통합 프롬프트
├── IMPROVEMENT_LOG.md                 ← 문제 근본 원인 분석 및 개선 이력
├── agents/
│   ├── AGENT1_SCOUT.md                ← 기회 탐지 에이전트 상세 설계
│   ├── AGENT2_ARCHITECT.md            ← 비즈니스 설계 에이전트
│   ├── AGENT3_VALIDATOR.md            ← 실행 검증 에이전트
│   ├── AGENT4_RISK.md                 ← 리스크 평가 에이전트
│   └── ORCHESTRATOR.md               ← 전체 흐름 통제 에이전트
├── templates/
│   ├── OPPORTUNITY_CARD.md            ← 표준 기회 카드 템플릿
│   ├── RISK_HEATMAP.md                ← 리스크 히트맵 + 철수 조건
│   ├── VALIDATION_CHECKLIST.md        ← 실행 검증 체크리스트
│   └── FOUNDER_ACTION_LIST.md         ← Founder 관점 액션 리스트
└── examples/
    └── HEALTHCARE_KOREA_SAMPLE.md     ← 한국 헬스케어 AI 적용 예시
```

---

## ⚡ 빠른 시작

1. `PROMPT_MASTER.md`를 열어 전체 프롬프트를 복사
2. AI 모델(Claude, GPT-4o 등)에 붙여넣기
3. 마지막 줄에 사용자 요청 추가:
   ```
   [요청]: 한국 Healthcare AI 붕괴 패턴에서 신사업 2~3개 도출, Top 1 설계+검증 요약
   ```
4. 실행 후 ORCHESTRATOR 보고서 수신

---

## 🔗 연관 저장소

- [multi-agent-system-v3-hybrid](https://github.com/GilbertKwak/multi-agent-system-v3-hybrid): 기반 멀티에이전트 아키텍처
- [global-semiconductor-ai-research](https://github.com/GilbertKwak/global-semiconductor-ai-research): 적용 사례 참조
- [notion-github-ops](https://github.com/GilbertKwak/notion-github-ops): Notion 연동 운영 체계
