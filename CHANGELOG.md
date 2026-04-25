# CHANGELOG — 프롬프트 엔진니어링 시스템

## [PE-8 v2.3 Patch 11] — 2026-04-25

### Added
- `applied-cases/PE-8-NOR-Flash/Ch09_FinancialModel_v1.0.md` — Ch.9 5개년 재무모델 (Base/Bull/Bear 3시나리오, PE-3 92/100 ✅)

### Changed
- PE-8 마스터 프롬프트 Ch.9 상태: 🔴 Draft → 🟢 Done
- Notion PE-8 Ch.9 페이지 생성 완료 (https://www.notion.so/34d55ed436f081f59dccc2e6b03b442b)

### PE-8 재무 패키지 완성 현황 (2026-04-25)
| 챕터 | 제목 | 상태 | PE-3 |
|---|---|---|---|
| Ch.9 | 5개년 재무모델 (P&L 3시나리오) | ✅ Done | 92/100 |
| Ch.9.5 | 현금흐름표 (IAS 7 직접법+간접법) | ✅ Done | 96/100 |
| Ch.16 | ROI·ROE·BEP·Payback | ✅ Done | 96/100 |

### Financial Model Key Figures (Base Scenario)
- Y5(2030) Revenue: $11.2M | GM: 46% | EBITDA: -$2.85M
- 5Y Cumulative Revenue: $16.8M | Capex: $23.0M
- BEP: 2031 Q1

---

## [v1.6] — 2026-04-18

### Added
- `docs/report/2026-04-10_3engine-upgrade-report-v1.6.md` — 3-Engine 업그레이드 통합 실행 보고서 (한글)
- `applied-cases/2026-04-10_3engine-upgrade-v1.6.md` — v1.6 실행 기록 및 정량 지표

### Changed
- `README.md` — v1.6으로 갱신
  - 버전 배지 v1.5 → v1.6
  - 디렉토리 트리에 `knowledge_graph.json` 및 `scripts/build_knowledge_graph.py` 항목 추가
  - 🔧 KG 빌드 & 검증 실행 섹션 신설 (방법 B 커맨드, 옵션 표, SKIP 조건 명시)
  - 버전 이력에 v1.6 항목 추가
  - 다음 리뷰 v1.6 → v1.7로 갱신
- `CHANGELOG.md` — v1.6 항목 날짜 및 scripts 변경사항 보완
- `scripts/build_knowledge_graph.py` — CLI 방법 B 공식화
- Notion 허브 페이지 v1.6으로 동기화 완료

### Upgrade Summary — v1.6
**실행일**: 2026-04-10 | **관리자**: Gilbert Kwak

#### 핵심 정량 지표 (v1.5 → v1.6)
| 지표 | v1.5 기준 | v1.6 달성 | 개선율 |
|------|-----------|-----------|--------|
| 프롬프트 품질 점수 (5차원 평균) | 72/100 | 88/100 | +22.2% |
| 자동개선 루프 평균 반복 횟수 | 2.8회 | 1.9회 | -32.1% |
| 자동증식 변형 버전 생성 수 | 5종 | 8종 | +60.0% |
| 자동검증 합격률 (1차 통과) | 61% | 84% | +37.7% |
| Notion↔GitHub 동기화 소요시간 | 45분 | 12분 | -73.3% |

---

## [v1.5] — 2026-04-10

### Added
- `applied-cases/2026-04-10_3engine-upgrade-v1.5.md`
- `engines/PE-1_auto-refinement/prompt_template_v1.5.md`
- `engines/PE-2_auto-proliferation/prompt_template_v1.5.md`
- `engines/PE-3_auto-validation/prompt_template_v1.5.md`

### Changed
- `README.md` — v1.5로 갱신
- `CHANGELOG.md` — v1.5 항목 추가

---

## [v1.4] — 2026-04-10

### Added
- `engines/PE-1_auto-refinement/upgrade_v1.4.md`
- `engines/PE-2_auto-proliferation/upgrade_v1.4.md`
- `engines/PE-3_auto-validation/upgrade_v1.4.md`
- `applied-cases/2026-04-10_3engine-upgrade-v1.4.md`

### Changed
- `README.md` — v1.4로 갱신
- `CHANGELOG.md` — v1.4 항목 추가
- `dashboard/metrics.md` — KPI 지표 v1.4 기준 갱신

---

## [v1.3] — 2026-04-09

### Added
- `docs/agent1/README.md` ~ `docs/agent5/README.md`
- `docs/support/README.md`, `docs/new/README.md`
- `dashboard/README.md`, `dashboard/metrics.md`

### Changed
- `docs/index.md` — Master Index 전면 개편
- `README.md` — v1.3으로 갱신

---

## [v1.2] — 2026-04-09
### Added
- `docs/index.md`, `docs/rca-capa/README.md` + `RCA-001~004.md`

### Changed
- README.md v1.2, CHANGELOG.md Cross-links 표 추가

---

## [v1.1] — 2026-04-05
### Added
- `engines/` 디렉토리 구조 (PE-1, PE-2, PE-3)
- `applied-cases/`, `workflows/3engine_pipeline.md`

### Changed
- README.md 전면 개편

---

## [v1.0] — 2026-04-05
### Added
- 최초 저장소 생성, 3-Engine 프레임워크 정립
