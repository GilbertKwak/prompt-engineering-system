# knowledge_graph.json — v3.1-osat 패치 노트
> 생성일: 2026-04-29T10:50:00+09:00 | 적용 대상: knowledge_graph.json

## 📊 버전 요약
| 항목 | 이전 (v3.2) | 이후 (v3.1-osat 병합) |
|------|------------|----------------------|
| 노드 수 | 68 | **70** (+2) |
| 엣지 수 | 95 | **98** (+3) |
| scan_dirs | 8 | **9** (+osat-strategy) |

## 🆕 신규 노드 (2개)

### NODE-69: PE-SAT-02
```json
{
  "id": "prompts/osat-strategy/pe_sat_02_v1.0.md",
  "type": "prompt",
  "title": "PE-SAT-02 · 멀티국가 OSAT 비교 감시 — 국가별 전략 붕괴 매트릭스 v1.0",
  "status": "active",
  "version": "v1.0",
  "date": "2026-04-29",
  "tags": ["PE-SAT", "PE-13", "OSAT", "multi-country", "KR", "TW", "CN", "JP", "US", "v1.0"],
  "notion_url": "https://www.notion.so/35155ed436f0812295f2de6895e27c39",
  "pe3_score": 88,
  "domain": ["멀티국가OSAT비교", "전략붕괴매트릭스"],
  "workspace_ssot": "T-09-C19"
}
```

### NODE-70: PE-SAT-03
```json
{
  "id": "prompts/osat-strategy/pe_sat_03_v1.0.md",
  "type": "prompt",
  "title": "PE-SAT-03 · OSAT 파트너 선정 S0 스크리닝 — HBM Salvage 연동 v1.0",
  "status": "active",
  "version": "v1.0",
  "date": "2026-04-29",
  "tags": ["PE-SAT", "PE-13", "OSAT", "partner-screening", "HBM", "Salvage", "S0", "v1.0"],
  "notion_url": "https://www.notion.so/35155ed436f0812295f2de6895e27c39",
  "pe3_score": 90,
  "domain": ["OSAT파트너선정", "HBMSalvage연동", "S0스크리닝"],
  "workspace_ssot": "T-09-C19"
}
```

## 🔗 신규 엣지 (3개)

| # | source | target | relation | note |
|---|--------|--------|----------|------|
| E-96 | `pe_sat_01_v7.0.md` | `pe_sat_02_v1.0.md` | `pipeline_next` | 단일국가 State 출력 → 멀티국가 비교 입력 |
| E-97 | `pe_sat_02_v1.0.md` | `pe_sat_03_v1.0.md` | `pipeline_next` | 멀티국가 후보 풀 → 파트너 스크리닝 입력 |
| E-98 | `pe_sat_03_v1.0.md` | `applied-cases/jv-fund/master_v3.md` | `cross_domain` | 스코어카드 결과 → IRR/NPV 교차 검증 (PE-FIN 연동) |

## 🔄 메타 갱신
- `version`: `3.2` → `3.1-osat` (OSAT 전용 패치 태깅, pe-graph --rebuild 완료)
- `scan_dirs`: +`prompts/osat-strategy`
- `changelog`: v3.1-osat 항목 최상단 추가

## ✅ 검증
- PE-SAT-02 PE-3: 88점 (목표 90+ → 다음 PE-1 루프 대상)
- PE-SAT-03 PE-3: 90점 ✅ 기준 충족
- 다음 실행: `pe-validate-all` → PE-SAT-02 개선 루프 예정
