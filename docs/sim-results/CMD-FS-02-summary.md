# CMD-FS-02 · SEMI-OPT-GNN 가상 수치 완전 계산

> **실행일**: 2026-04-30 18:03 KST  
> **빌드**: knowledge_graph v4.3 공식 빌드  
> **모델**: GraphSAGE-3L | 28 nodes × 12 features | 41 edges | 7 epochs | 5,888 params

---

## 🏆 Top-10 노드 위험도 + Alpha Signal

| Rank | Node | Importance | supply_dis | yield_drop | mkt_loss | strategic_up | IRR_adj (bps) | Signal |
|------|------|-----------|-----------|-----------|---------|-------------|--------------|--------|
| 1 | Samsung_F | 1.0000 | 0.5800 | 0.5397 | 0.4958 | 0.3885 | −10.8 | NEUTRAL |
| 2 | TSMC_N3 | 0.9402 | 0.4769 | 0.3915 | 0.3181 | 0.6418 | **+136.2** | ✅ BUY |
| 3 | Intel_F | 0.8115 | 0.5552 | 0.5780 | 0.5933 | 0.3429 | −23.4 | NEUTRAL |
| 4 | Samsung_DRAM | 0.7508 | 0.4812 | 0.4514 | 0.3845 | 0.5944 | **+113.5** | ✅ BUY |
| 5 | SK_Hynix_HBM | 0.7446 | 0.4667 | 0.4326 | 0.3683 | 0.6234 | **+131.2** | ✅ BUY |
| 6 | SMIC | 0.7442 | 0.6757 | 0.6184 | 0.5879 | 0.3151 | −74.4 | 🔴 AVOID |
| 7 | GlobalFoundry | 0.7335 | 0.4849 | 0.4417 | 0.3905 | 0.5197 | +78.7 | NEUTRAL |
| 8 | AMAT | 0.7062 | 0.3864 | 0.3663 | 0.3192 | 0.5749 | **+135.1** | ✅ BUY |
| 9 | LAM_Research | 0.7036 | 0.4395 | 0.3851 | 0.3519 | 0.5582 | **+110.6** | ✅ BUY |
| 10 | Entegris | 0.6902 | 0.4510 | 0.3801 | 0.3280 | 0.5922 | **+122.2** | ✅ BUY |

---

## 💰 FIN-001 EBITDA 기댓값

| 기업 | E[ΔEBITDA] (pp) |
|------|---------------|
| SK Hynix HBM | **−10.46** |
| Samsung Foundry | −10.20 |
| TSMC N3 | −6.73 (최소 충격) |
| Samsung DRAM | −9.42 |
| Intel Foundry | **−12.40** (최대 충격) |

---

## ⚡ PE-EQP × PE-SEMI 카스케이드 확률

| 이벤트 | 확률 | 레벨 |
|-------|------|------|
| LAM S2→S3 | 0.4431 | 🟠 MED |
| Samsung_F S3→S4 | 0.5690 | 🟠 MED |
| Intel_F S3 유지 | 0.6670 | 🔴 HIGH |
| SMIC S4 진입 | **0.7554** | 🔴 HIGH |

---

## 🎯 JV Alpha Top-3

1. **TSMC_N3** +136.2 bps — EUV 공급 확보, geo-risk SEMI-OPT-MAP 헤지  
2. **ASML_EUV** +131.4 bps — Sole-source 해자 × strategic_up 0.74  
3. **SK_Hynix_HBM** +131.2 bps — HBM4 램프 × SEMI-OPT-YIELD 수렴

---

*Source: `docs/sim-results/CMD-FS-02-gnn-result.json` → knowledge_graph v4.3 SEMI-OPT-GNN 노드*
