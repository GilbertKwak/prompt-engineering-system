# knowledge_graph v4.7 Changelog

**갱신일**: 2026-05-02 KST  
**이전 버전**: v4.6 (140 nodes / 213 edges)  
**현재 버전**: v4.7 (143 nodes / 223 edges)

---

## 신규 노드 (+3)

| Node ID | 유형 | 설명 |
|---|---|---|
| STRAT-007-MASTER | Prompt | SEMI-STRAT-007 Master (PE-3: 96.2) |
| STRAT-007-KR | Prompt Variant | SEMI-STRAT-007 한국 단일국가형 (PE-3: 95) |
| STRAT-007-GLOBAL | Prompt Variant | SEMI-STRAT-007 6개국 병렬형 (PE-3: 94) |

## 신규 엣지 (+10)

| Source | Target | 관계 유형 | 비고 |
|---|---|---|---|
| STRAT-007-MASTER | PE-SEMI-HUB | belongs_to | Fab State Machine 공유 |
| STRAT-007-MASTER | PE-AI-HUB | belongs_to | Firm State Machine 공유 |
| STRAT-007-MASTER | COLLAPSE-TYPOLOGY | references | CT-1/CT-2/CT-3 유형 |
| STRAT-007-MASTER | WORLD-A | covers | Hard Decoupling |
| STRAT-007-MASTER | WORLD-B | covers | Managed De-risking |
| STRAT-007-MASTER | WORLD-C | covers | Partial Re-coupling |
| STRAT-007-MASTER | WORLD-D | covers | Alliance Fragmentation |
| STRAT-007-KR | STRAT-007-MASTER | variant_of | Variant-A |
| STRAT-007-GLOBAL | STRAT-007-MASTER | variant_of | Variant-B |
| STRAT-007-MASTER | PE-EQP-HUB | cross_link | EW-S3 장비 수출통제 연계 |

---

## 누적 현황

| 항목 | v4.6 | v4.7 | Δ |
|---|---|---|---|
| Nodes | 140 | 143 | +3 |
| Edges | 213 | 223 | +10 |
| PE-STRAT 노드 수 | 7 | 10 | +3 |
| World 커버리지 | A/B/C (부분) | A/B/C/D (완전) | +WorldD |

---

## pe-sync-up 실행 내역

```
[2026-05-02 14:54 KST] pe-graph --rebuild --tag v4.7
[2026-05-02 14:55 KST] PUSH: prompts/strategy-collapse/SEMI-STRAT-007/ (3 files)
[2026-05-02 14:55 KST] PUSH: knowledge_graph/graph_v4.7_changelog.md
[2026-05-02 14:55 KST] Notion ↔ GitHub sync: pe-sync-up ✅
[2026-05-02 14:55 KST] Status: 143 nodes / 223 edges | COMPLETED
```
