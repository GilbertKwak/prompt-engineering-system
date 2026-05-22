# Knowledge Graph Changelog

> 파일 경로: `knowledge-graph/kg-changelog.md`  
> 최종 업데이트: 2026-05-22

---

## v6.3 — 2026-05-22

### 🆕 신규 도메인 추가
- **PE-AI-ECO-001-C** `AI Ecosystem Intelligence — Competitive Layer C`
  - LLM 공급자 Tier1 클러스터 (OpenAI / Anthropic / Google DeepMind / Meta AI)
  - AI 인프라 레이어 클러스터 (AWS / Azure / GCP / CoreWeave / Lambda Labs)
  - 수직통합 플레이어 클러스터 (Apple / Samsung / SK Hynix / TSMC / Intel)
  - Early Warning 트리거 2종: EW-AI-ECO-C-01, EW-AI-ECO-C-02
  - Cross-domain links: PE-SEMI-HBM, PE-GEO-RISK, C-33

### 📊 그래프 통계
| 항목 | v6.2 | v6.3 | Delta |
|------|------|------|-------|
| 총 노드 수 | 294 | 312 | +18 |
| 총 엣지 수 | 465 | 489 | +24 |
| 도메인 수 | 13 | 14 | +1 |
| 수정된 노드 | — | 7 | +7 |
| 수정된 엣지 | — | 5 | +5 |

### ✅ Integrity Check 결과
```
pe-graph --integrity-check --version 6.3

[CHECK] node_id_uniqueness       : PASS
[CHECK] edge_reference_validity  : PASS
[CHECK] domain_schema_compliance : PASS
[CHECK] orphan_nodes             : 0    PASS
[CHECK] circular_dependency      : NONE PASS
[CHECK] dangling_edges           : 0    PASS
[CHECK] cross_domain_links_valid : PASS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OVERALL STATUS : ✅ PASS
WARNINGS       : 0
ERRORS         : 0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 🔗 스키마 변경
- `early_warning` 노드 타입에 `trigger_id` 필드 추가 (하위 호환)

---

## v6.2 — 2026-05-21

- MA-MoE-8AGENT GLOBAL 변형 추가 반영
- 5개국 공급망 연쇄충격 시뮬레이션 노드 추가
- EW-GLOBAL-01~03, EW-GEO-01/02 등록
- README 업데이트 (OPT/KR/GLOBAL 3-variant 인덱스)

---

## v6.1 — 2026-05-18

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
