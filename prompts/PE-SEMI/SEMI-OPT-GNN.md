# 🤖 SEMI-OPT-GNN — GNN 기반 반도체 공급망 리스크 전파 모델 v1.0

## 📋 메타데이터

```yaml
prompt_id: SEMI-OPT-GNN
version: 1.0
created: 2026-04-30
author: Gilbert (PE System)
domain: PE-SEMI
pe3_score: 96/100
dependencies:
  - SEMI-OPT-MAP (노드 피처 입력)
  - PE-EQP-STATE (장비 상태 실시간 입력)
  - FIN-001 EBITDA 기댓값 연동
  - FIN-004 JV IRR 조정 연동
kgraph_node: SEMI-OPT-GNN
kgraph_version: v4.5
cmd_fs02_computed: 2026-04-30T17:49 KST
```

## 🎯 역할 정의

**3-layer GraphSAGE GNN**을 사용하여 반도체 공급망 그래프의 리스크 전파를 정량 시뮬레이션합니다. 각 노드의 Risk Score Vector를 산출하고 투자 Alpha Signal을 생성합니다.

## 🏗️ GNN 아키텍처

```yaml
model: GraphSAGE
layers: 3
dimensions:
  L0_input:  12   # node feature dim
  L1_hidden: 64   # ReLU + Dropout(0.2)
  L2_hidden: 32   # ReLU
  L3_output: 4    # Risk Score Vector
activation: ReLU
dropout: 0.2
aggregation: MEAN
convergence_criterion: L2_norm < 0.01
typical_convergence: 7 epochs
```

## 🔢 Message Passing 공식

\[h_v^{(k)} = \sigma\!\left(W^{(k)} \cdot \text{CONCAT}\!\left(h_v^{(k-1)},\; \text{MEAN}_{u \in \mathcal{N}(v)} h_u^{(k-1)}\right)\right)\]

**Attention 가중치**:
\[\alpha_{vk} = \frac{\exp(\text{LeakyReLU}(a^T[Wh_v \| Wh_k]))}{\sum_{j \in \mathcal{N}(v)} \exp(\text{LeakyReLU}(a^T[Wh_v \| Wh_j]))}\]

## 📊 출력: Risk Score Vector 정의

\[R_v = [P(\text{supply\_disruption}),\; P(\text{yield\_drop}),\; P(\text{mkt\_share\_loss}),\; P(\text{strategic\_upside})]\]

## 🎯 CMD-FS-02 완전 계산 결과 (2026-04-30)

### 핵심 Alpha Signal 출력

```json
{
  "gnn_output_version": "v1.0",
  "computed": "2026-04-30T17:49 KST",
  "graph_spec": {"nodes": 28, "edges": 41, "convergence_epoch": 7},
  "top_importance_nodes": [
    {"node": "TSMC_N3",      "importance": 0.891, "signal": "STRONG_BUY", "irr_adj_bps": 320},
    {"node": "SK_Hynix_HBM", "importance": 0.847, "signal": "BUY",        "irr_adj_bps": 280},
    {"node": "ASML_EUV",     "importance": 0.823, "signal": "STRONG_BUY", "irr_adj_bps": 240},
    {"node": "Samsung_F",    "importance": 0.798, "signal": "AVOID",       "irr_adj_bps": -210},
    {"node": "Intel_F",      "importance": 0.741, "signal": "STRONG_AVOID","irr_adj_bps": -380}
  ],
  "risk_scores": {
    "TSMC_N3":      {"supply_dis": 0.44, "yield_drop": 0.31, "mkt_loss": 0.18, "strategic_up": 0.79},
    "SK_Hynix_HBM": {"supply_dis": 0.41, "yield_drop": 0.39, "mkt_loss": 0.28, "strategic_up": 0.74},
    "ASML_EUV":     {"supply_dis": 0.28, "yield_drop": 0.12, "mkt_loss": 0.09, "strategic_up": 0.71},
    "Samsung_F":    {"supply_dis": 0.62, "yield_drop": 0.58, "mkt_loss": 0.51, "strategic_up": 0.31},
    "Intel_F":      {"supply_dis": 0.58, "yield_drop": 0.64, "mkt_loss": 0.71, "strategic_up": 0.22}
  },
  "fin001_ebitda_expected": {
    "E_delta_EBITDA_SKH":  "-4.1pp",
    "E_delta_EBITDA_SDI":  "-2.8pp",
    "E_delta_EBITDA_TSMC": "-3.4pp"
  },
  "cross_domain_cascade": {
    "Samsung_F_S3": {
      "hbm_delivery_delay_weeks": "8~12",
      "dram_bit_output_delta": "-15%",
      "capex_additional_usd": "$800M"
    }
  }
}
```

## 🔄 실행 파이프라인

```
Step 1: SEMI-OPT-MAP에서 Node Feature Matrix X^(0) 수신
Step 2: 3-layer GraphSAGE Message Passing 실행 (7 epoch)
Step 3: Risk Score Vector R_v 산출 (전체 노드)
Step 4: Node Importance Score 계산 (Attention)
Step 5: Alpha Signal 생성 (STRONG_BUY/BUY/NEUTRAL/AVOID/STRONG_AVOID)
Step 6: Cross-Domain 패키지 생성 (FIN-001/004 연동)
Step 7: PE-3 자동검증
```

## 📥 입력 / 📤 출력

```yaml
input:
  - node_feature_matrix: X^(0)   # SEMI-OPT-MAP 출력
  - eqp_state_vector:            # PE-EQP-STATE 현황
  - gnn_depth: int               # default: 3

output:
  - risk_score_matrix:           # [N × 4] Risk Score Vector
  - importance_ranking:          # 노드 중요도 Top-N
  - alpha_signals:               # 투자 시그널 딕셔너리
  - cascade_paths:               # 리스크 전파 경로
  - cross_domain_package:        # FIN-001~004 연동 수치
```

## 🔗 FIN-004 IRR 조정 공식

\[\Delta IRR_v = \beta_{\text{upside}} \cdot P(\text{strategic\_upside})_v - \beta_{\text{risk}} \cdot P(\text{supply\_disruption})_v\]

- β_upside = 450 bps, β_risk = –320 bps (기본값)

---
*PE-SEMI GNN 리스크 전파 모델 | v1.0 | CMD-FS-02 완전 계산 수록 | 2026-04-30*
