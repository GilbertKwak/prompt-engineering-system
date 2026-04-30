# 🗺️ SEMI-OPT-MAP — 반도체 공급망 리스크 매핑 + HHI 분석 v1.0

## 📋 메타데이터

```yaml
prompt_id: SEMI-OPT-MAP
version: 1.0
created: 2026-04-30
author: Gilbert (PE System)
domain: PE-SEMI
pe3_score: 96/100
dependencies:
  - PE-MIN-HHI (광물 집중도 연동)
  - SEMI-OPT-GNN (노드 피처 공급)
kgraph_node: SEMI-OPT-MAP
kgraph_version: v4.5
```

## 🎯 역할 정의

반도체 공급망의 **노드-엣지 구조를 매핑**하고, HHI(허핀달-허쉬만 지수) 기반 시장집중도 분석 및 지리적·규제적 리스크를 정량화합니다.

## 🏗️ 공급망 그래프 정의

```yaml
graph_spec:
  total_nodes: 28
  total_edges: 41
  node_categories:
    Equipment: 9    # ASML, LAM, KLA, TEL, AMAT 등
    Foundry:   5    # TSMC, Samsung F., Intel F., SMIC, GlobalF.
    Memory:    7    # SK Hynix, Samsung DRAM, Micron 등
    Chemical:  4    # JSR, Shin-Etsu, Sumco, Entegris
    Logistics: 3    # 물류·패키징 노드
  edge_types:
    SUPPLY:          18  # 공급 관계
    PROCESS_DEP:     12  # 공정 의존성
    RISK_PROPAGATION: 11  # 리스크 전파
```

## 📊 노드 피처 벡터 정의 (dim=12)

```yaml
node_features:
  - fab_util       # 가동률 [0,1]
  - eqp_state      # S1=1.0, S2=2.0, S3=3.0, S4=4.0
  - hhi_score      # HHI [0, 10000]
  - geo_risk       # 지리 리스크 [0,1]
  - lead_time      # 리드타임 (월)
  - yield_rate     # 수율 [0,1]
  - inv_buffer     # 재고 버퍼 [0,1]
  - esg_score      # ESG 점수 [0,100]
  - capex_ratio    # CAPEX/Revenue
  - rev_growth     # 매출 성장률 YoY
  - chem_dep       # 화학물질 의존도 [0,1]
  - alt_src        # 대체 소싱 가능성 [0,1]
```

## 🔴 HHI 분석 — 핵심 병목 노드

| 공급망 레이어 | 핵심 기업 | HHI | 리스크 등급 | PE-MIN-HHI 연동 |
|---|---|---|---|---|
| EUV 리소그래피 | ASML | **9,200** | 🔴 CRITICAL | 사실상 독점 |
| 포토레지스트 | JSR | **8,700** | 🔴 CRITICAL | 일본 수출규제 취약 |
| 파운드리 선단공정 | TSMC | **7,800** | 🔴 HIGH | 대만 지정학 리스크 |
| 실리콘 웨이퍼 | Shin-Etsu | **7,200** | 🟠 HIGH | 일본 집중 |
| KrF 포토레지스트 | 복수 | 4,200 | 🟡 MEDIUM | 대체재 존재 |
| DRAM | 삼성/SK H/Micron | **5,400** | 🟠 HIGH | 3사 과점 |

## 🌏 지리적 리스크 레이어

```yaml
geo_risk_matrix:
  Taiwan (TSMC):     geo_risk=0.71  # 양안 리스크
  Japan (JSR/Shnetsu): geo_risk=0.58  # 수출규제 이력
  Korea (Samsung/SKH): geo_risk=0.46  # THAAD 선례
  USA (Intel/Applied): geo_risk=0.35  # 정책 불확실성
  Netherlands (ASML):  geo_risk=0.62  # EUV 수출통제
```

## 🔗 엣지 가중치 계산 공식

\[w_{uv} = \alpha \cdot \text{supply\_share}_{uv} + \beta \cdot \text{HHI}_{v}/10000 + \gamma \cdot (1 - \text{alt\_src}_u)\]

- α=0.4, β=0.35, γ=0.25 (Gilbert 시스템 기본값)

## 📥 입력 / 📤 출력

```yaml
input:
  - query_node: str        # 분석 대상 노드
  - depth: int             # 탐색 깊이 (default: 2)
  - risk_threshold: float  # 필터링 임계값 (default: 0.5)

output:
  - node_feature_matrix    # SEMI-OPT-GNN 입력용
  - hhi_ranking            # 병목 노드 순위
  - geo_risk_heatmap       # 지리 리스크 레이어
  - critical_paths         # 최고위험 공급 경로 Top-5
  - alt_sourcing_options   # 대체 소싱 가능 노드
```

---
*PE-SEMI 공급망 매핑 모듈 | v1.0 | 2026-04-30*
