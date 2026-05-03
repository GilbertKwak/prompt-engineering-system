# CHANGELOG — 프롬프트 엔지니어링 시스템

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
- **ESG-UNIFIED-01 Section D** 중국 지역 통합:
  - Geopolitical Lock Index CN: **88**
  - Average SCP CN: **0.71**
  - 전염 행렬 (CN→KR: 0.81, CN→TW: 0.89, CN→EU: 0.74, CN→US: 0.62)

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
