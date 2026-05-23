# CHANGELOG — 프롬프트 엔지니어링 시스템

## v6.4 (2026-05-23) — C-38 CRP 도메인 초기화 · 최적화 프롬프트 3종 · 하이브리드 전략 공식 적용

### 핵심 변경사항
- **CRP-THEORY-001** 신규 생성 — 학술 논문 수준 CRP 이론 정식화 프롬프트 (PE-3 목표 95+)
- **CRP-STRATEGY-001** 신규 생성 — CRP → OpenAI 급 플랫폼 전환 7단계 전략 프롬프트 (PE-3 목표 95+)
- **CRP-AGENT-FRAMEWORK-001** 신규 생성 — LangGraph/AutoGen/CrewAI 초월 CRP-Native Agent 프레임워크 설계 프롬프트 (PE-3 목표 95+)
- **하이브리드 전략 v1.0 공식 적용** — 커밋 메시지·파일명·JSON key: 영어 / 문서 본문: 한국어
- **Notion & GitHub 생태계 연계 분석** 완료 — CRP 3종 ↔ T-09 허브 통합 포인트 7개 명시
- **CHANGELOG 하이브리드 전략 소급 적용** — v6.3 커밋 메시지 기준 확립 (commit: `9cb314f6`)
- **CRP 3종 GitHub 저장 확인** — `prompts/PE-IP/CRP/` 디렉토리 (commit: `cb1c72c6`)
- **KG v6.4** 업데이트 예정 — CRP 클러스터 +4n/+6e (C-39 세션)

### CRP 도메인 프롬프트 3종 상세

| 파일명 | 버전 | PE-3 목표 | 핵심 기능 |
|--------|------|-----------|-----------| 
| `CRP-THEORY-001.md` | v1.0 | 95+ | 수학적 정의 · Ω 공간 · Reconfiguration Operator R |
| `CRP-STRATEGY-001.md` | v1.0 | 95+ | 7단계 전략 · KPI 연도별 · 경쟁사 대응 포함 |
| `CRP-AGENT-FRAMEWORK-001.md` | v1.0 | 95+ | TypeScript 스키마 · T-09 통합 7포인트 |

### 기존 프롬프트 대비 개선사항

| 항목 | 기존 | v6.4 개선 |
|------|------|-----------| 
| 수식 정밀도 | 서술형 | Ω 공간 + R 연산자 수학적 정의 |
| 실행 커맨드 | 없음 | PE-3 실행 커맨드 내장 |
| 생태계 연결 | 암묵적 | T-09 통합 포인트 7개 명시 |
| 경쟁사 대응 | 일반적 | Workday/SAP/LangGraph 구체 대응 |
| 언어 전략 | 혼재 | 하이브리드 전략 v1.0 일관 적용 |

### 생태계 연계 맵

| CRP 프롬프트 | 연계 기존 도메인 |
|-------------|----------------|
| CRP-THEORY-001 | PE-ARCH-001 · C-31 PE-AI · PE-3 파이프라인 |
| CRP-STRATEGY-001 | INV-STRAT-MASTER v1.0 · PE-CON-STRAT |
| CRP-AGENT-FRAMEWORK-001 | PE-7 · KM-PIPE-MASTER v3.0 · PE-3 |

### Notion 저장 권장 위치
- `CRP-THEORY-001` → C-31 PE-AI 하단 신규 섹션
- `CRP-STRATEGY-001` → C-36 INV-STRAT 하단
- `CRP-AGENT-FRAMEWORK-001` → PE-7 AI 자동화 하단

### C-39 다음 우선 과제
1. **KG v6.4** — CRP 클러스터 +4n/+6e 등록
2. **CRP-AGENT-FRAMEWORK → PE-7 통합** — T-09 전체 자동화 품질 시스템 레벨 향상
3. **RPT-AI-ECO-001** — CRP Cognitive Kernel 적용 1호 보고서 실행

### 파일 목록
- `prompts/PE-IP/CRP/CRP-THEORY-001.md` (신규, commit: `cb1c72c6`)
- `prompts/PE-IP/CRP/CRP-STRATEGY-001.md` (신규, commit: `cb1c72c6`)
- `prompts/PE-IP/CRP/CRP-AGENT-FRAMEWORK-001.md` (신규, commit: `cb1c72c6`)
- `CHANGELOG.md` (업데이트, commit: `9cb314f6` → 본 커밋)

---

## v6.3 (2026-05-23) — C-37 KM-PIPE 도메인 편입 · Notion↔GitHub 양방향 동기화 파이프라인 오케스트레이터

### 핵심 변경사항
- **KM-PIPE-MASTER v3.0** 신규 생성 — Notion↔GitHub 양방향 동기화 오케스트레이터 (C-37)
- **KM-PIPE-A v1.0** 신규 생성 — Notion→GitHub 단방향 동기화 파이프라인
- **KM-PIPE-B v1.0** 신규 생성 — GitHub→Notion 역방향 동기화 + 세션로그 자동화 파이프라인
- **KG v6.3** rebuild 완료 — 66 nodes / 80 edges (+3n / +5e from v6.2)
- **하이브리드 언어 전략** 적용 — 커밋 메시지·파일명·JSON key: 영어 / 문서 본문: 한국어

### KG 변경
| 구분 | v6.2 | v6.3 | 증가 |
|---|---|---|---|
| Nodes | 63 | **66** | +3 |
| Edges | 75 | **80** | +5 |
| KM-PIPE 클러스터 | 0 | 3 | +3 |

### 신규 노드 3종
| Node ID | 타입 | 설명 |
|---------|------|------|
| KM-PIPE-MASTER-HUB | domain_hub | C-37 오케스트레이터 허브 |
| KM-PIPE-A | prompt | Notion→GitHub 단방향 파이프라인 |
| KM-PIPE-B | prompt | GitHub→Notion 역방향 + 세션로그 |

### 신규 엣지 5종
| From | To | Relation |
|------|----|----------|
| KM-PIPE-MASTER-HUB | T-09-MOTHER | child_of |
| KM-PIPE-MASTER-HUB | PE-IP-HUB | child_of |
| KM-PIPE-MASTER-HUB | KM-PIPE-A | orchestrates |
| KM-PIPE-MASTER-HUB | KM-PIPE-B | orchestrates |
| KM-PIPE-MASTER-HUB | README.md | cross_domain_link |

### 파일 목록
- `PE-IP/KM-PIPE/KM-PIPE-MASTER-v3.0.md` (신규)
- `PE-IP/KM-PIPE/KM-PIPE-A-v1.0.md` (신규)
- `PE-IP/KM-PIPE/KM-PIPE-B-v1.0.md` (신규)
- `knowledge_graph.json` → v6.3 (업데이트, commit: `b5a42adb`)

---

## v6.2 (2026-05-20) — C-36 INV-STRAT 도메인 편입 · 개인투자 전략 마스터 프레임워크

### 핵심 변경사항
- **INV-STRAT-MASTER v1.0** 신규 생성 — NerdWallet 기반 → 기관급 의사결정 변환 프레임워크 (C-36)
- **7대 투자 전략 최적화 모델** 수록 — 성장/가치/배당/모멘텀/퀀트/글로벌/대안
- **생애주기 전략 전환 맵** 수록 — 축적기/전환기/인출기 3단계
- **한국 시장 현지화 맵** 수록 — ISA/IRP/세제/규제 특화
- **PE-3 스코어 92점** 달성 (목표: v1.1에서 97점)
- **KG v6.2** rebuild 완료 — 63 nodes / 75 edges (+5n / +7e from v6.1)

### KG 변경
| 구분 | v6.1 | v6.2 | 증가 |
|---|---|---|---|
| Nodes | 58 | **63** | +5 |
| Edges | 68 | **75** | +7 |
| INV-STRAT 클러스터 | 0 | 5 | +5 |

### 신규 노드 5종
| Node ID | 타입 | 설명 |
|---------|------|------|
| INV-STRAT-HUB | domain_hub | C-36 투자전략 허브 |
| INV-STRAT-MASTER-v1.0 | prompt | 마스터 프레임워크 프롬프트 |
| INV-STRATEGY-7 | component | 7대 투자전략 모델 |
| INV-LIFECYCLE | component | 생애주기 전환 맵 |
| INV-KR-MAP | component | 한국 시장 현지화 맵 |

### 파일 목록
- `prompts/INV-STRAT/inv_strat_master_v1.0.md` (신규)
- `knowledge_graph.json` → v6.2 (업데이트, commit: `ad4c26d4`)

---

## v6.1 (2026-05-19) — C-35 PE-OPTICAL 도메인 편입 · 광학모듈 투자분석 라이브러리

### 핵심 변경사항
- **OPTICAL-MODULE-DEEP v2.1** 신규 생성 — 광학모듈 심층 투자분석 프롬프트 (C-35)
- **I/O Contract v2.0** 수록 — 입출력 계약 명세 (인터페이스 표준화)
- **Memory Handoff Engine v1.0** 수록 — 세션 간 메모리 핸드오프
- **Fallback 3조건 Engine v1.0** 수록 — 신뢰도 저하 대응 체계
- **Version A/B 분기** 수록 — 투자집중형 / 기술심층형 분석 모드
- **PE-3 스코어 95점** 달성
- **KG v6.1** rebuild 완료 — 58 nodes / 68 edges (+6n / +8e from v6.0)

### KG 변경
| 구분 | v6.0 | v6.1 | 증가 |
|---|---|---|---|
| Nodes | 52 | **58** | +6 |
| Edges | 60 | **68** | +8 |
| PE-OPTICAL 클러스터 | 0 | 6 | +6 |

### 신규 노드 6종
| Node ID | 타입 | 설명 |
|---------|------|------|
| PE-OPTICAL-HUB | domain_hub | C-35 광학모듈 허브 |
| OPTICAL-MODULE-DEEP-v2.1 | prompt | 심층 투자분석 프롬프트 |
| OPT-IO-CONTRACT | component | I/O 계약 명세 |
| OPT-MEMORY-HANDOFF | component | 메모리 핸드오프 엔진 |
| OPT-FALLBACK-ENGINE | component | Fallback 3조건 엔진 |
| OPT-VERSION-AB | component | 분석 모드 A/B 분기 |

### 파일 목록
- `prompts/PE-OPTICAL/pe_optical_01_deep_v2.1.md` (신규)
- `knowledge_graph.json` → v6.1 (업데이트)

---

## v4.15 (2026-05-07) — 세션 #1~#5 통합 동기화 · PE-INVEST/GTR-ISR/PE-CON/DD-FIN

### 핵심 변경사항
- **PE-INVEST-MASTER v5.0.6** 릴리즈 — Palantir AI Pure-Play (9th Sector) 검증 · A024~A026 알고리즘 · 9-sector 평균 4.2 달성
- **PE-2 역대 최고 점수 4.3** 기록 (세션 #1)
- **OPT-DD-FIN ↔ PE-FIN Trigger Engine v1.0 → v1.2** 업그레이드 — 라우팅 매트릭스 전체 검증 (4/4 E2E 패스)
- **GTR-ISR v1.0** 신규 생성 — PE-3 3-Engine 최적화 · Notion 생태계 연계 방안 수립 (세션 #3)
- **PE-CON CON-06~09 연계** + **CON-10~12 섹터 특화 확장** + **INDEX.md v3.0 완성** (총 24종) (세션 #4)
- **GitHub 커밋 동기화** + **T-09 작업일지 SSOT 업데이트** (세션 #5)

### 세션 이력
| 세션 | 주요 완료 항목 | 커밋/링크 |
|------|--------------|---------| 
| 세션 #1 | PE-INVEST-MASTER v5.0.6 · A024~A026 · PE-2: 4.3 | 5c5649f |
| 세션 #2 | OPT-DD-FIN ↔ PE-FIN Trigger Engine v1.2 · E2E 4/4 | — |
| 세션 #3 | GTR-ISR v1.0 · PE-3 최적화 · Notion 연계 방안 | — |
| 세션 #4 | PE-CON 24종 완성 · CON-10~12 섹터 특화 · INDEX.md v3.0 | — |
| 세션 #5 | GitHub SSOT 동기화 · T-09 작업일지 업데이트 | 본 커밋 |

### SSOT Sync 현황
- ✅ CHANGELOG v4.15 커밋 (본 커밋)
- ✅ T-09 작업일지 세션 #5 인덱스 등록
- ✅ 누적 통계 업데이트 (KG v4.14 · C-34 반영)

### 파일 목록
- `CHANGELOG.md` (업데이트)

---

## v4.14 (2026-05-03) — PIPE-2026-0503-KR · KG Delta Sync · PE-7 STEP 5

### 핵심 변경사항
- **KG v4.13 → v4.14** 델타 업데이트 (PIPE-2026-0503-KR 분석 결과 반영)
- **SKH-S1** 노드 신규 등록 — SK Hynix HBM Salvage Strategy (HBM3E/HBM4 로드맵)
- **SEC-S1** 노드 신규 등록 — Samsung Electronics Memory/HBM Strategy (SEMI-STRAT-001 v6.2 기반)
- **E-KG-001~006** 엣지 6종 신규 (COMPETES_WITH · ANALYZED_BY · STORED_IN · SUPPLY_CHAIN_OVERLAP)
- **Notion Master Directory Hub** KG 버전 필드 v4.13 → v4.14 업데이트 완료
- **knowledge_graph_v4.14_delta.json** 커밋 (SHA: c7b3612)

### 그래프 변경
| 구분 | v4.13 | v4.14 | 증가 |
|---|---|---|---|
| Nodes | 127 | **129** | +2 |
| Edges | 191 | **197** | +6 |
| 신규 클러스터 | — | SKH-S1 / SEC-S1 | +2 |

### 신규 노드 2종
| Node ID | Label | 도메인 | 소스 |
|---------|-------|--------|------|
| SKH-S1 | SK Hynix — HBM Salvage Strategy | Semiconductor · HBM | HBM_Salvage Ch.2/3/6 |
| SEC-S1 | Samsung Electronics — Memory/HBM Strategy | Semiconductor · Memory | SEMI-STRAT-001 v6.2 |

### 신규 엣지 6종
| Edge ID | From | To | Type |
|---------|------|----|------|
| E-KG-001 | SKH-S1 | SEC-S1 | COMPETES_WITH (w=0.92) |
| E-KG-002 | SKH-S1 | PE-7 | ANALYZED_BY (w=0.88) |
| E-KG-003 | SEC-S1 | PE-7 | ANALYZED_BY (w=0.85) |
| E-KG-004 | SKH-S1 | DIR-09 | STORED_IN (w=1.00) |
| E-KG-005 | SEC-S1 | DIR-09 | STORED_IN (w=1.00) |
| E-KG-006 | SKH-S1 | SEC-S1 | SUPPLY_CHAIN_OVERLAP (w=0.76) |

### SSOT Sync 현황
- ✅ Notion Master Directory Hub — KG v4.14 업데이트
- ✅ GitHub `knowledge_graph_v4.14_delta.json` 커밋 (c7b3612)
- ✅ CHANGELOG PE-7 STEP 5 Sync Push (본 커밋)
- ⬜ T-09 변경 로그 — 수동 paste 권고 (Notion API exact-match 제한)

### 파일 목록
- `knowledge_graph_v4.14_delta.json` (신규 · 루트)
- `CHANGELOG.md` (업데이트)

---

## v4.5 (2026-05-01) — knowledge_graph v4.5 · C-31 PE-AI Intel 등록

### 핵심 변경사항
- knowledge_graph v4.5 생성 · C-31 PE-AI Intel 신규 노드 반영
- notion_005 최적화 프롬프트 수록 (AI 플랫폼 전략 / 글로벌 AI 기술 트렌드)
- 생태계 연계: PE-AI(C-28) · PE-DC(C-30) · PE-SEMI · PE-JV

---

## v4.4 (2026-04-30) — CMD-FS-05 · PE-FIN C-31 재무·투자 분석 라이브러리 신설

### 핵심 변경사항
- **PE-FIN/ 디렉토리 신설** (C-31) — T-09 직계 하위 허브
- **fin_master_v1.0.md**: PE-FIN-HUB MASTER · Auto Mode 4종 · PE-3 96점 목표
- **FIN-001** EBITDA 충격 시뮬레이션 — SEMI-OPT-GNN·PE-MIN·PE-SEMI 3-도메인 입력 통합
- **FIN-002** DCF 밸류에이션 + 시나리오 분석 — Damodaran 방법론 · 지정학 리스크 WACC 반영
- **FIN-003** 채권/신용등급 리스크 모델 — Moody's/S&P 방법론 · IG/HY 경계 특화
- **FIN-004** JV 펀드 수익률 시뮬레이션 — SEMI-OPT-GNN Alpha Signal IRR 통합
- **knowledge_graph_v4.4.json**: 134 nodes / 201 edges (+5n/+8e from v4.3)

### 그래프 변경
| 구분 | v4.3 | v4.4 | 증가 |
|---|---|---|---|
| Nodes | 129 | **134** | +5 |
| Edges | 193 | **201** | +8 |
| PE-FIN 클러스터 | 0 | 5 | +5 |

### 신규 엣지 8종
| From | To | Type |
|------|-----|------|
| T-09 | PE-FIN-HUB | child_of |
| PE-FIN-HUB | FIN-001 | contains |
| PE-FIN-HUB | FIN-002 | contains |
| PE-FIN-HUB | FIN-003 | contains |
| PE-FIN-HUB | FIN-004 | contains |
| SEMI-OPT-GNN | FIN-001 | RISK_INPUT |
| PE-MIN-MASTER | FIN-001 | MINERAL_SHOCK_QUANTIFY |
| PE-JV-MASTER | FIN-004 | ALPHA_SIGNAL_INPUT |

### 파일 목록
- `PE-FIN/fin_master_v1.0.md` (신규)
- `PE-FIN/fin_001_ebitda_shock_v1.0.md` (신규)
- `PE-FIN/fin_002_dcf_valuation_v1.0.md` (신규)
- `PE-FIN/fin_003_credit_risk_v1.0.md` (신규)
- `PE-FIN/fin_004_jv_fund_sim_v1.0.md` (신규)
- `knowledge_graph_v4.4.json` (신규)

---

## v4.3 (2026-04-30) — CMD-FS-03 · knowledge_graph v4.3 빌드

### 핵심 변경사항
- SEMI-OPT 클러스터 신설 (MASTER/MAP/GNN/YIELD)
- PE-EQP-v2.0 업그레이드 + PE-EQP-RISK 서브노드
- PE-MIN 도메인 신설 (MASTER/MIN-SIM-D/PE-MIN-KR/PE-MIN-HHI)
- PE-FIN-HUB 플레이스홀더 등록 (FS-05 완료 시 활성화 → 본 v4.4에서 완성)
- knowledge_graph v4.3: 129 nodes / 193 edges

---

## v3.8 (2026-04-29) — PE-SAT ESG+반도체 통합 에이전트 + CN 클러스터 신설

### 핵심 변경사항
- **PR#4 squash merge** (SHA: `8b3f8f3`) — `feature/PE-SAT-ESG-001-v13` → `main`
- **ESG-001-v13.0** MASTER 등록: 8인 역할 통일 · Bayesian 전 도메인 공통화 · A~G 출력 표준화
- **ESG-KR/EU/US-v13.0** 3종 국가 파생 동시 등록
- **ESG-CN-v8.0** 중국 특화 파생 신설
  - `Party_Directive_Override` State 추가 (CN 전용 5번째 상태)
  - `dual_pressure_flag=true` / `political_risk_flag=VERY_HIGH`
  - CN 7개 기업 리스크 노드 (CATL·BYD·LONGi·Huawei·SMIC·China Mobile·PetroChina)
  - CN 규제 스택 6종 (CSRC·PBOC·CGB·CSDDD·MOFCOM·BIS)
- **knowledge_graph v3.8** 생성: +16 nodes / +22 edges → 누적 **108 nodes / 159 edges**

### 그래프 변경
| 구분 | v3.5 | v3.8 | 증가 |
|---|---|---|---|
| Nodes | 96 | 108 | +12 |
| Edges | 138 | 159 | +21 |
| CN 클러스터 | 0 | 11 | +11 |

### 파일 목록
- `knowledge_graph_v3.8.json` (신규)
- `prompts/PE-SAT/ESG-001-v13.0.xml` (PR#4)
- `prompts/PE-SAT/ESG-CN-v8.0.xml` (PR#4)
- `prompts/PE-SAT/ESG-KR-v13.0.xml` (PR#4)
- `prompts/PE-SAT/ESG-EU-v13.0.xml` (PR#4)
- `prompts/PE-SAT/ESG-US-v13.0.xml` (PR#4)

---

## v3.5 (2026-04-29) — C-24 PE-SEMI 생태계 통합 파이프라인
- P-12 Bayesian-GNN (ASML/LAM/KLA/TEL/AMAT) 허브 노드 등록
- PE-13 OSAT 스크리닝 + PE-THERM 인풋 패키지 + PE-CHEM 교차 검증
- +14 nodes / +18 edges

## v3.4 (2026-04-29) — PE-CHEM-SEMI-01 + APIS v11.1
- 반도체 공정 조사 PE-CHEM-SEMI-01 v2.0 + VAR 5종
- PE-OPT 도메인 최초 생성 (APIS v11.1 PE-3: 97점)
- +7 nodes / +15 edges

## v3.3 (2026-04-29) — C-21 PE-CHEM + C-22 PE-EQP
- PE-CHEM 반도체 공정 화학물 라이브러리 (+6 nodes)
- PE-EQP 첨단 장비 전략 붕괴 감시 라이브러리 (+7 nodes)
- +13 nodes / +18 edges
