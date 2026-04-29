# CHANGELOG — 프롬프트 엔진니어링 시스템

## [PE-THERM v1.0 · knowledge_graph v3.2] — 2026-04-29 10:48 KST

> 커밋 기준: `feat(PE-THERM): Add PE-THERM 반도체 열관리 라이브러리 v1.0` · 담당자: GilbertKwak

### Added — PE-THERM 반도체 열관리 분석 라이브러리 (신규)

| 파일 | 역할 | 버전 | PE-3 점수 |
|---|---|---|---|
| `prompts/thermal/README.md` | PE-THERM 라이브러리 허브 (T-09 C-20) | v1.0 | avg 93 |
| `prompts/thermal/THERM-01_v3.0.md` | TIM 열저항 지배 메커니즘 — Kapitza·Series R·Scaling Law | v3.0 | 95 |
| `prompts/thermal/THERM-02_v2.0.md` | Underfill 열차단 분석 — TC-NCF vs MR-MUF | v2.0 | 93 |
| `prompts/thermal/THERM-03_v2.0.md` | Micro-Bump 열저항 정량 분석 — Fourier·R_th×N | v2.0 | 91 |
| `prompts/thermal/THERM-04_v2.0.md` | High I/O Activity 발열 분석 — P_dynamic·PHY 전력 | v2.0 | 90 |
| `prompts/thermal/THERM-05_v2.0.md` | Interposer/Substrate 열저항 — Organic vs Si | v2.0 | 92 |
| `prompts/thermal/THERM-06_v3.0.md` | TSV 열전달 PDE + Scaling Law — Spreading R·Saturation | v3.0 | **97** |

### Changed — knowledge_graph v3.0 → v3.2 업그레이드

| 항목 | v3.0 | v3.2 | 변화 |
|---|---|---|---|
| total_nodes | 62 | **68** | **+6** |
| total_edges | 87 | **95** | **+8** |
| scan_dirs | 7개 | **8개** | `prompts/thermal` 추가 |
| version | 3.0 | **3.2** | — |
| generated_at | 2026-04-29T09:06 | **2026-04-29T10:48** | — |

### 신규 엣지 목록 (+8)

| # | source | target | relation | 비고 |
|---|---|---|---|---|
| 1 | `prompts/thermal/README.md` | `engines/PE-3_auto-validation/README.md` | `validated_by` | PE-3 avg 93점 |
| 2 | `prompts/thermal/README.md` | `prompts/pe_ip/README.md` | `indexed_by` | THERM 시리즈 PE-IP 등록 |
| 3 | `prompts/thermal/README.md` | `README.md` | `registered_in` | T-09-C20 SSOT |
| 4 | `prompts/thermal/README.md` | `prompts/bio/README.md` | `cross_domain` | PE-MEM HBM 교차 연동 |
| 5 | `prompts/thermal/README.md` | `engines/PE-1_auto-refinement/README.md` | `pipeline_entry` | PE-1→PE-3 파이프라인 |
| 6 | `prompts/thermal/THERM-01_v3.0.md` | `prompts/thermal/README.md` | `sub_module_of` | TIM PE-3 95점 |
| 7 | `prompts/thermal/THERM-02_v2.0.md` | `prompts/thermal/README.md` | `sub_module_of` | Underfill PE-3 93점 |
| 8 | `prompts/thermal/THERM-06_v3.0.md` | `prompts/thermal/README.md` | `sub_module_of` | TSV PE-3 97점 |

### Linked

- Notion SSOT: [T-09 C-20 PE-THERM](https://www.notion.so/35155ed436f081ca93bcddb49af69c7d)
- T-09 Mother Page: [v3.2 갱신](https://www.notion.so/34a55ed436f0814d9cffe6a2f0816e29)
- 연계 도메인: PE-MEM · PE-JV · PE-ICD · PE-MFG

---

## [JV Fund Prompt v3.0] — 2026-04-27

> 커밋 기준: `prompts/jv_fund/ 신규 생성` · 담당자: GilbertKwak

### Added — JV Fund Prompt Suite (신규)

| 파일 | 역할 | PE-3 목표 |
|---|---| ---|
| `prompts/jv_fund/master_prompt_v3.md` | 글로벌 JV 펀드 마스터 프롬프트 v3 | 90/100 |
| `prompts/jv_fund/variants/fu_series_adapter.md` | FU-Series 연동 파생 | 90/100 |
| `prompts/jv_fund/variants/bstar_eco2_prompt.md` | B-Star eCO2 전용 파생 | 90/100 |
| `prompts/jv_fund/variants/ai_infra_prompt.md` | AI 인프라 DC 전용 파생 | 90/100 |
| `prompts/jv_fund/VALIDATION_CHECKLIST.md` | PE-1/PE-3 검증 체크리스트 | — |

### Changed — v2 → v3 주요 개선 사항

- **구조화**: 단일 블록 텍스트 → ROLE / CONTEXT / TASK CHAIN / OUTPUT / VALIDATION 5구조 분리
- **파라미터화**: DOMAIN · STAGE · DEPTH · LANG 입력 파라미터 표준화
- **출력 포맷**: JSON + MD 병기 출력 구조 신설
- **PE-1 통합**: 출처 명시 · 추정값 표기 · 최신성 요건 내장
- **PE-3 통합**: counter_scenario 필드 · confidence 수치 · pe3_score 목표 내장
- **도메인 변형**: FU-Series / B-Star eCO2 / AI Infra 3종 파생 프롬프트 생성
- **언어**: KR+EN 병기 구조 표준화

---

## [PE-10 v2.0 Batch Upgrade] — 2026-04-27

> 커밋 기준: `ea99c34` · 담당자: GilbertKwak

### Changed — P-02 ~ P-09 일괄 v1.0 → v2.0 업그레이드

| 프롬프트 | 역할 | PE-3 v1.0 | PE-3 v2.0 | 핵심 추가 필드 |
|---|---|---|---|---|
| P-02 | Recovery Inject | 76 | **91** | `SOURCE_ERROR_TYPE` · `EVIDENCE` |
| P-03 | 요구사항 정제 | 78 | **92** | `ambiguities` 서브필드 |
| P-04 | 실행 계획 생성 | 75 | **90** | `risk_flags` · `confidence_score` |
| P-05 | Ralph Stage 1 Spec | 81 | **93** | `checks.evidence` 서브필드 |
| P-06 | Ralph Stage 2 Quality | 82 | **94** | `iteration_count` · `dimension.evidence` |
| P-07 | Recursive 분해 | 77 | **91** | `DECOMP_REASON` 필드 |
| P-08 | Leaf 실행 | 76 | **91** | `leaf_id` · `LEAF_TRACE` |
| P-09 | 결과 통합 | 79 | **93** | `LEAF_TRACE` · `synthesis_confidence` |

---

## [PE-8 v2.3 Patch 12] — 2026-04-25

### Added
- `applied-cases/PE-8-NOR-Flash/Ch07_ProjectSummary_v1.0.md`

---

## [v1.6] — 2026-04-18

### Added
- `docs/report/2026-04-10_3engine-upgrade-report-v1.6.md`
- `applied-cases/2026-04-10_3engine-upgrade-v1.6.md`

### Changed
- `README.md` — v1.6으로 갱신

---

## [v1.0~v1.5] — 2026-04-05~10
- 최초 저장소 생성, 3-Engine 프레임워크 정립
