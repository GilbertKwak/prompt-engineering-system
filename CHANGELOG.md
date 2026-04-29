# CHANGELOG — 프롬프트 엔지니어링 시스템

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
