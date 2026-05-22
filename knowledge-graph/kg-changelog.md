# Knowledge Graph Changelog

> **시스템**: T-09 프롬프트 엔지니어링 시스템  
> **저장소**: `GilbertKwak/prompt-engineering-system`  
> **경로**: `knowledge-graph/kg-changelog.md`

---

## [v6.3] — 2026-05-22

### Trigger
- **Source**: PE-AI-ECO-001 Variant C — Startup/Edge AI
- **Commit**: `d43e9f01`
- **Command**: `pe-graph --rebuild --version 6.3 --add-domain PE-AI-ECO-001-C`
- **Time**: 21:13 KST

### Stats

| Metric | v6.2 | v6.3 | Delta |
|--------|:----:|:----:|:-----:|
| Nodes | 191 | **195** | +4 |
| Edges | 326 | **335** | +9 |
| Prompts | 115 | **116** | +1 |
| Active Domains | 13/13 | 13/13 | — |
| Graph Density | 1.71 | **1.72** | +0.01 |

### New Nodes (4)

| Node ID | Label | Layer | Domains | AstraChips Role |
|---------|-------|:-----:|---------|:---------------:|
| `edge-device` | Edge Device Intelligence Hub | L2 | PE-AI-ECO / semi-silicon | STRATEGIC |
| `edge-infra` | Edge Infrastructure Mapping | L2 | PE-AI-ECO / semi-infra | MONITOR |
| `edge-startup` | Edge AI Startup Ecosystem | L3 | PE-AI-ECO / PE-NBD / PE-INV | PARTNERSHIP |
| `edge-exit` | Edge AI Exit & M&A Pathway | L3 | PE-AI-ECO / inv-exit | STRATEGIC |

### New Edges (9)

| Source | Target | Type | Weight | 근거 |
|--------|--------|------|:------:|------|
| PE-AI-ECO-001-C | edge-device | domain_link | 1.00 | Variant C 직접 연결 |
| PE-AI-ECO-001-C | edge-infra | domain_link | 1.00 | Variant C 직접 연결 |
| PE-AI-ECO-001-C | edge-startup | domain_link | 1.00 | Variant C 직접 연결 |
| PE-AI-ECO-001-C | edge-exit | domain_link | 1.00 | Variant C 직접 연결 |
| `edge-device` | semi-silicon | cross_domain | 0.90 | 엣지칩 ↔ 반도체 실리콘 교차 |
| `edge-startup` | PE-NBD | nbd_link | 0.92 | AstraChips NBD 파이프라인 |
| `edge-startup` | PE-INV | investment_signal | 0.88 | PMF-CONFIRMED 라우팅 |
| `edge-infra` | semi-infra | cross_domain | 0.85 | 엣지 인프라 ↔ 반도체 인프라 |
| `edge-exit` | inv-exit | exit_link | 0.93 | Exit 시나리오 S1/S2/S3 연동 |

### Integrity Check

| 검증 항목 | 판정 | 비고 |
|-----------|:----:|------|
| `edge-exit` ↔ `inv-exit` 중복 여부 | ✅ PASS | inv-exit는 v6.2 기존 node — edge만 신규 추가 |
| `edge-device` ↔ v6.4 `ci-moat` 충돌 | ✅ PASS | v6.4에서 재사용 예정 — v6.3에서 선생성 필수 |
| `edge-infra` → `semi-infra` 존재 확인 | ⚠️ ASSUMED PASS | rebuild 전 semi-infra node 존재 여부 검증 권장 |
| MECE 위반 (edge-startup 이중 연결) | ✅ PASS | type 상이(nbd_link vs investment_signal)로 허용 |

### Cross-Domain Map

```
PE-AI-ECO-001-C
    ├── edge-device  ──→ semi-silicon   (cross_domain 0.90)
    ├── edge-infra   ──→ semi-infra     (cross_domain 0.85)
    ├── edge-startup ──→ PE-NBD         (nbd_link 0.92)
    │                ──→ PE-INV         (investment_signal 0.88)
    └── edge-exit    ──→ inv-exit       (exit_link 0.93)
                          └── (v6.2 기존) inv-exit → PE-INV
```

### Next: v6.4 Bridge

- **트리거**: PE-AI-ECO-002 (AI Competitive Intelligence Deep Scan)
- **상태**: 🟢 READY
- **예상**: 199 nodes / 343 edges
- **신규 노드**: `ci-radar` (L1), `ci-dna` (L2), `ci-moat` (L2), `ci-threat` (L3)

---

## [v6.2] — 2026-05-18

- Base: 191 nodes / 326 edges / 115 prompts
- Trigger: PE-AI-ECO Phase 4 (A/B/C) 완료
- Active Domains: 13/13
- Graph Density: 1.71

---

*Knowledge Graph Changelog · T-09 PE 시스템 · GilbertKwak/prompt-engineering-system*
