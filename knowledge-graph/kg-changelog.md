# Knowledge Graph Changelog

> 파일 경로: `knowledge-graph/kg-changelog.md`  
> 최종 업데이트: 2026-05-22 16:25 KST

---

## v6.3 — 2026-05-22

### Build Info
```
pe-graph --rebuild --version 6.3 --add-domain PE-AI-ECO-001-C
Timestamp : 2026-05-22T16:25:00+09:00
Source    : PE-AI-ECO-001 Variant C (Startup / Edge AI · Phase 4)
Commit    : d43e9f01 (notion-ref: 36455ed4-36f0-816e-9b1e-c012fad7f2d6)
```

### ✅ Integrity Check
```
pe-graph --integrity-check --version 6.3

[CHECK] node_id_uniqueness        : PASS
[CHECK] edge_reference_validity   : PASS
[CHECK] domain_schema_compliance  : PASS
[CHECK] orphan_nodes              : 0    PASS
[CHECK] circular_dependency       : NONE PASS
[CHECK] dangling_edges            : 0    PASS
[CHECK] cross_domain_links_valid  : PASS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OVERALL STATUS : ✅ PASS
WARNINGS       : 0
ERRORS         : 0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 🆕 신규 도메인 — PE-AI-ECO-001-C
**Variant C: Startup / Edge AI · 5-Agent Pipeline · PE-3 Score 95/100**

- **AGENT-1** Edge AI Startup Landscape Mapping — 4-Layer 스타트업 50개 히트맵
- **AGENT-2** White Space & Disruption Scan — 4차원 공백 점수 + Top-5 디스럽션 신호
- **AGENT-3** Startup Traction & PMF Scoring — 5차원 PMF + Bayesian Beta(3,7)
- **AGENT-4** AstraChips Strategic Fit — 5차원 Fit 점수 (STRATEGIC PRIORITY / WATCH & BUILD / REFERENCE ONLY)
- **AGENT-5** KG Integration & NBD Memo — 본 delta JSON 생성 + C-30 라우팅

**Top-5 디스럽션 신호**: RISC-V 엣지 AI 칩 / On-Device Transformer 경량화 / 생체인식+엣지AI / 이상감지 B2B SaaS / In-sensor AI

**신규 EW 트리거**:
- `EW-AI-ECO-C-01` — AI 인프라 HBM 할당량 변동 ±15% → 즉시 재스캔 + C-29 업데이트
- `EW-AI-ECO-C-02` — 신규 LLM Tier1 진입/M&A → 경쟁 구도 재매핑 + C-33 갱신

### 📊 그래프 통계
| 항목 | v6.2 | v6.3 | Δ |
|------|------|------|---|
| 총 노드 수 | 294 | 312 | +18 |
| 총 엣지 수 | 465 | 489 | +24 |
| 도메인 수 | 13 | 14 | +1 |
| 수정된 노드 | — | 7 | +7 |
| 수정된 엣지 | — | 5 | +5 |
| EW 트리거 누적 | 12 | 14 | +2 |

### 🔗 Cross-Domain Links (신규)
| 소스 | 타겟 | 관계 |
|------|------|------|
| PE-AI-ECO-001-C | PE-SEMI-HBM | FEEDS_DATA |
| PE-AI-ECO-001-C | PE-GEO-RISK | MODULATES |
| PE-AI-ECO-001-C | C-33 | INFORMS |
| PE-AI-ECO-001-C | C-35 (PE-INV) | ROUTES_TO |
| PE-AI-ECO-001-C | C-30 (PE-NBD) | ROUTES_TO |
| PE-AI-ECO-001-C | PE-AI-ECO-001-A | CROSS_REFS |
| PE-AI-ECO-001-C | PE-AI-ECO-001-B | CROSS_REFS |

### 🔧 스키마 변경
- `early_warning` 노드 타입에 `trigger_id` + `severity` 필드 추가 (하위 호환)

---

## v6.2 — 2026-05-21

- MA-MoE-8AGENT GLOBAL 변형 추가 반영
- 5개국 공급망 연쇄충격 시뮬레이션 노드 추가
- EW-GLOBAL-01~03, EW-GEO-01/02 등록
- README 업데이트 (OPT/KR/GLOBAL 3-variant 인덱스)

---

## v6.1 — 2026-05-18

- PE-AI-ECO-001 Variant A (반도체 에코시스템) — KG v6.1 트리거
- PE-AI-ECO-001 Variant B (PE 투자 포커스) — KG v6.2 트리거
- C-36 MultiAgent Strategic Intelligence System v2.0-OPT 반영
- PE-SEMI-HBM 도메인 노드 확장
- 루프 기반 점수 노드(ΔScore) 타입 추가

---

## v6.0 — 2026-05-15

- Knowledge Graph v6 메이저 리빌드
- 도메인 구조 재편: PE-CON / PE-FIN / PE-IP → 통합 레이어
- 기존 v4.x delta 파일군 아카이브 처리
- `knowledge-graph/` 디렉토리 신설 (기존 루트 분산 파일 정리)

---

## v4.x Archive

> v4.12 ~ v4.25 delta 파일은 레포 루트에 보존 (하위 호환 참조용)

| 버전 | 주요 변경 |
|------|----------|
| v4.25 | PE-IP 도메인 노드 확장 |
| v4.24 | 투자 포트폴리오 연계 노드 추가 |
| v4.23 | 반도체 지정학 리스크 노드 추가 |
| v4.22 | M&A 시나리오 엣지 추가 |
| v4.21 | FU Series 연구 허브 연동 |
| v4.12~v4.20 | 초기 도메인 구조 정립 |
