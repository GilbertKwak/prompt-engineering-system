# PROMPT_VERSION_HISTORY.md
# Marketing Strategies — 프롬프트 버전 이력 완전판

> **SSOT**: `prompt-engineering-system/applied-cases/marketing-strategies/`  
> **Notion 허브**: [PE-MKT v2.0 — MKT-00~08](https://www.notion.so/34f55ed436f081b1bb25ed8c47bcb595)  
> **최종 업데이트**: 2026-04-27  
> **관리자**: Gilbert Kwak

---

## 📋 디렉터리 인덱스

| ID | 파일 | 카테고리 | 복잡도 | 버전 | 등록일 |
|---|---|---|---|---|---|
| **MKT-00** | `MKT-00.md` | 마케팅 유형 분류 + ROI/CAC/LTV | ⭐⭐⭐ | v1.0 | 2026-04-27 |
| **MKT-01** | `MKT-01.md` | STP 기본 컨설팅 보고서 | ⭐⭐⭐ | v1.0 | 2026-04-27 |
| **MKT-02** | `MKT-02.md` | STP + Execution Bridge + Competitive | ⭐⭐⭐⭐ | v1.0 | 2026-04-27 |
| **MKT-03** | `MKT-03.md` | Industry-Specific IF-분기 로직 | ⭐⭐⭐⭐ | v1.0 | 2026-04-27 |
| **MKT-04** | `MKT-04.md` | STP + Financial Model + IR Deck | ⭐⭐⭐⭐⭐ | v1.0 | 2026-04-27 |
| **MKT-05** | `MKT-05.md` | Growth Hacking + Experimentation Framework | ⭐⭐⭐⭐ | v1.0 | 2026-04-27 |
| **MKT-06** | `MKT-06.md` | Brand Positioning + Auto-Report | ⭐⭐⭐⭐ | v1.0 | 2026-04-27 |
| **MKT-07** | `MKT-07.md` | 통합 심층 프롬프트 — v1.0→v4.0 진화 계보 | ⭐⭐⭐⭐⭐ | v1.0 | 2026-04-27 |
| **MKT-08** | `MKT-08.md` | 시장조사 & 진입 전략 — v2.0→McKinsey 5종 | ⭐⭐⭐~⭐⭐⭐⭐⭐ | v1.0 | 2026-04-27 |

---

## 🔄 MKT-07 진화 계보 상세

### v1.0 — 기본 마케팅 전략 5단계

| 항목 | 내용 |
|---|---|
| **XML 태그** | `IntegratedMarketingStrategy` |
| **핵심 구조** | 환경분석 → 목표 → STP → 마케팅믹스 → PLC |
| **자동 계산** | 시장 성장률(CAGR), 경쟁 강도 지수, 기회 점수, 필요 리드 수, CAC 허용치 |
| **출력** | 전략 보고서 + 표/매트릭스 + 자동 계산 KPI |
| **적용 대상** | 마케팅 기본 전략 보고서 작성 |

### v2.0 — 고도화 전략 (시나리오 시뮬레이션)

| 항목 | 내용 |
|---|---|
| **XML 태그** | `AIIntegratedMarketingStrategy_v2` |
| **핵심 추가** | 경쟁사 가격 인하 / 신규 진입자 시나리오 시뮬레이션 |
| **KPI** | North Star Metric, 채널별 CAC 비교, LTV = 평균구매금액 × 구매빈도 × 유지기간 |
| **퍼널** | Awareness → Interest → Consideration → Conversion → Retention → Loyalty |
| **적용 대상** | 경쟁 대응 전략 수립, ROI 극대화 |

### v3.0 — 멀티 에이전트 마케팅 시스템

| 항목 | 내용 |
|---|---|
| **XML 태그** | `Marketing_Agent_System_v3` |
| **에이전트 구성** | ResearchAgent / StrategyAgent / ExecutionAgent / OptimizationAgent / Orchestrator |
| **자동화 루프** | 성과 기준 미달 시 자동 재실행, KPI 달성 시 확장 전략 수행 |
| **연계** | PE-10 (멀티에이전트 패턴) |
| **적용 대상** | 마케팅 자동화 파이프라인 |

### v4.0 — 완전 자율형 AI 기업 시스템

| 항목 | 내용 |
|---|---|
| **XML 태그** | `Autonomous_AI_Company_v4` |
| **에이전트 구성** | CEO / Strategy / Marketing / Sales / Product / Finance / Operations / HR (8 Agent) |
| **핵심 메커니즘** | Infinite Optimization Loop — 시장 변화 감지 → 전략 자동 수정 → 실행 |
| **KPI** | Revenue / Profit Margin / CAC / LTV / Burn Rate / Runway |
| **연계** | PE-11 (마스터 멀티에이전트) |
| **적용 대상** | AI 스타트업/기업 운영 전략 |

---

## 🌍 MKT-08 진화 계보 상세

### v1 — 고급 전략형 (AdvancedMarketResearchStrategyPrompt v2.0)

| 항목 | 내용 |
|---|---|
| **XML 태그** | `AdvancedMarketResearchStrategyPrompt` |
| **핵심 구조** | 시장발굴(3관점) → 시장조사(7항목) → 시장분석(TAM/SAM/SOM) → GTM 전략 |
| **실행 방식** | 수동 입력 (산업/제품, 목표시장, 분석 목적) |
| **GPT 최적화** | GPT-5.2 명시 |
| **적용 대상** | 전략기획 담당자, 실무 정밀 분석 |

### v2 — 자동 추론형 (HyperCustomMarketStrategyPrompt v3.0)

| 항목 | 내용 |
|---|---|
| **XML 태그** | `HyperCustomMarketStrategyPrompt` |
| **핵심 추가** | 입력 없어도 자동 시나리오 2~3개 생성, 산업별 KSF 자동 적용 |
| **자동화** | 유망 산업·국가 자동 추론 → 최적 조합 선택 → 비교 분석 |
| **GPT 최적화** | GPT-5.2 명시 |
| **적용 대상** | 신규 사업 탐색, 빠른 시장 후보 비교 |

### v3 — 질문형 에이전트 (InteractiveMarketResearchAgent v1.0)

| 항목 | 내용 |
|---|---|
| **XML 태그** | `InteractiveMarketResearchAgent` |
| **핵심 구조** | Stage 0~4 순차 진행 (질문 → 응답 → 분석 → 다음 질문) |
| **인터랙션** | 절대 한 번에 모든 분석 수행 안 함, 단계별 사용자 확인 |
| **적용 대상** | 신입/중급 분석가, 팀원과 협업 분석 |

### v4 — 풀오토 보고서 생성 (FullAutoMarketResearchReportAgent)

| 항목 | 내용 |
|---|---|
| **XML 태그** | `FullAutoMarketResearchReportAgent` |
| **핵심 구조** | 완전 자동 — Executive Summary ~ 결론 8섹션 자동 생성 |
| **자동화** | 질문 없이 전체 보고서 생성, 데이터 부족 시 합리적 가정 명시 |
| **적용 대상** | 자동화 파이프라인, 빠른 보고서 생성 |

### v5 — McKinsey 슬라이드 덱 (McKinseyStyleStrategyDeckGenerator)

| 항목 | 내용 |
|---|---|
| **XML 태그** | `McKinseyStyleStrategyDeckGenerator` |
| **핵심 구조** | Pyramid Principle + MECE + Slide 1~11 CEO 보고용 덱 |
| **원칙** | Slide Title = 한 문장 핵심 메시지, 모든 슬라이드 "의사결정" 도움 |
| **적용 대상** | CMO, 경영진 보고 담당자, 이사회 보고 |

---

## 📊 디렉터리 버전 이력

| 버전 | 날짜 | 변경 내용 |
|---|---|---|
| **v2.1** | **2026-04-27** | MKT-08 등록 (시장조사·진입전략 5종), MKT-08 진화 계보 상세 추가, Notion + GitHub SSOT 동기화 완료 |
| v2.0 | 2026-04-27 | MKT-07 심층 프롬프트 등록 (v1→v4 진화 계보), PROMPT_VERSION_HISTORY.md 신규 작성, Notion PE-MKT v2.0 업그레이드, PE-10/PE-11 크로스 연계 추가 |
| v1.2 | 2026-04-27 | README.md v1.3 — MKT-07 인덱스 추가, 진화 계보 섹션 신설, PE-10/11 연계 행 추가 |
| v1.1 | 2026-04-27 | MKT-05 (그로스 해킹), MKT-06 (브랜드 포지셔닝) 신규 등록, README.md v1.2 업데이트 |
| v1.0 | 2026-04-27 | 최초 생성 — MKT-00~04 5종 등록, PE-FIN/PE-EDU 크로스 참조 체계 구축 |

---

## 🔗 크로스 도메인 연계

| 연계 시스템 | 연계 ID | 활용 시나리오 |
|---|---|---|
| **PE-FIN** | MKT-03/04 ↔ FIN-01·FIN-03·FIN-05 | 투자 유치 전략 설계 |
| **PE-EDU** | MKT-00 ↔ EDU-06/07 | 마케팅 교육 콘텐츠 생성 |
| **PE-7** | MKT 전체 ↔ PE-7 자동화 아키텍처 | 마케팅 자동화 설계 |
| **PE-10** | MKT-07 v3.0 ↔ PE-10 멀티에이전트 패턴 | 에이전트 파이프라인 구현 |
| **PE-11** | MKT-07 v4.0 ↔ PE-11 마스터 멀티에이전트 | AI 기업 운영 전략 실행 |
| **MKT-08** | MKT-08-v3/v4 ↔ FIN-01~03 | 해외시장 진출 + 투자 수익성 분석 |
| **PE Hub v2.0** | T-09 Mother Page | SSOT 유지, 전체 허브 색인 반영 |

---

## 📁 관련 파일

- [`README.md`](./README.md) — 디렉터리 인덱스 + 운영 가이드 (v1.4)
- [`MKT-07.md`](./MKT-07.md) — 마케팅 전략 진화 계보 통합 심층 프롬프트
- [`MKT-08.md`](./MKT-08.md) — 시장조사·진입 전략 진화 계보 5종
- **Notion SSOT**: [PE-MKT v2.0](https://www.notion.so/34f55ed436f081b1bb25ed8c47bcb595)
