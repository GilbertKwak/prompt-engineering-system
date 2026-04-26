# P6: ExaFLOPS 통합 자원모델 — HBM·Glass·전력·패키징 단일 TCO

> **버전**: 1.0.0 | **생성일**: 2026-04-26 | **파이프라인**: PE-7

---

## 1. 개요

P6는 ExaFLOPS 단위의 AI/HPC 시스템에 대해 **4개 자원 레이어를 단일 TCO 엔진으로 통합**한 모델이다.

| 자원 레이어 | 핵심 변수 | 출력 KPI |
|------------|----------|----------|
| HBM (메모리) | Gen/Stack수/Yield/Salvage | 레이어별 순원가 ($M) |
| Glass Substrate | 채택률/프리미엄/Yield 개선 | 기판+패키징 비용 ($M) |
| 전력 (SMR) | SMR 비율/LCOE/CAPEX | 10Y NPV 전력 TCO ($M) |
| 패키징 (OSAT) | CoWoS 면적/Yield/리드타임 | 패키징 비용 + 용량 제약 |

---

## 2. 타겟 시스템

| ID | 이름 | ExaFLOPS | GPU 수 | GPU 모델 | HBM | 지역 |
|----|------|----------|--------|----------|-----|------|
| SYS_A | HPC Cluster | 1.0 EF | 8,192 | H100 SXM5 | HBM3E | US |
| SYS_B | AI Training DC | 5.0 EF | 40,960 | H100 SXM5 | HBM3E | US |
| SYS_C | Sovereign AI DC | 10.0 EF | 81,920 | B200 | HBM4 | KR |

---

## 3. 핵심 수식

### 3.1 HBM 레이어

```
Gross Cost = stacks_total × unit_cost(t)
Yield-Adj Cost = Gross Cost / yield_rate
Salvage Value = salvageable_stacks × unit_cost × salvage_value_pct
              − salvageable_stacks × reconditioning_cost
Net HBM Cost = Yield-Adj Cost − Salvage Value
```

단가 연도 보정: `unit_cost(t) = unit_cost_0 × (1 − annual_decline)^t`

### 3.2 Glass Substrate 레이어

```
n_glass = n_gpu × adoption_rate
n_abf   = n_gpu − n_glass
Total Substrate Cost = n_glass × glass_unit + n_abf × abf_unit
Premium vs All-ABF   = Total − n_gpu × abf_unit
```

### 3.3 전력(SMR) 레이어

```
Total Power (MW) = n_gpu × GPU_TDP × overhead_mult × PUE / 1e6
Annual Energy (GWh) = Total Power × 8,760 / 1,000

Annual Grid Cost = GWh × (1−smr_pct) × grid_price / 1000  [$M]
Annual SMR Cost  = GWh × smr_pct    × smr_lcoe  / 1000  [$M]

NPV 10Y = Σ_{t=0}^{T-1} Annual × (1+esc)^t / (1+dr)^(t+1)
Blended LCOE = (1−smr_pct) × grid_price + smr_pct × smr_lcoe
Saving vs Grid = NPV(all-grid) − NPV(blended) − SMR CAPEX
```

### 3.4 패키징(OSAT) 레이어

```
CoWoS Area = n_gpu × CoWoS_size_mm² / 1e6  [M mm²]
Gross Pkg Cost = n_gpu × pkg_unit_cost
Yield Loss = Gross × (1 − yield) / yield
Total Pkg Cost = Gross + Yield Loss

용량 제약 = (required_wafer_starts > pe7_allocation × total_capacity)
```

### 3.5 통합 TCO

```
Total CAPEX = HBM_net + Glass/Pkg + Power_Infra(+SMR_CAPEX) + GPU/Other + Facility + Network
Total OPEX  = NPV(Power_OPEX) + NPV(Maintenance) + NPV(Staffing) + NPV(SW+Cooling)
Total TCO   = Total CAPEX + Total OPEX
TCO/EF      = Total TCO / ExaFLOPS
TCO/EF/Yr   = TCO/EF / Lifetime
```

---

## 4. 파일 구조

```
plugins/finance/
├── exaflops_config.yaml          # 전체 파라미터 설정
├── exaflops_resource_model.py    # TCO 계산 엔진 (CLI 지원)
├── exaflops_viz.py               # 5개 차트 생성
docs/
└── P6_ExaFLOPS_TCO.md            # 이 문서
.github/workflows/
└── pe7_smr_pipeline.yml          # P4 파이프라인 (P6 연동 가능)
```

---

## 5. 실행 가이드

### 5.1 전체 실행 (모든 시스템 × 시나리오)

```bash
cd plugins/finance
python exaflops_resource_model.py
# → P6_ExaFLOPS_TCO_Model.xlsx + p6_exaflops_tco.json 생성

python exaflops_viz.py
# → output/p6_charts/ 에 5개 PNG 생성
```

### 5.2 단일 시스템 + 시나리오 선택 실행

```bash
python exaflops_resource_model.py --system SYS_C --scenario smr_full --glass aggressive
```

### 5.3 Dry Run (파일 미저장)

```bash
python exaflops_resource_model.py --dry-run
```

### 5.4 GitHub Actions 수동 트리거

```bash
gh workflow run pe7_smr_pipeline.yml \
  -f smr_scenario=smr_full \
  -f dry_run=false
```

---

## 6. 차트 목록 (exaflops_viz.py 출력)

| 파일명 | 내용 |
|--------|------|
| `p6_tco_stacked.png` | 시스템 × 시나리오 TCO 스택 바 (7개 레이어) |
| `p6_cost_per_exaflops.png` | ExaFLOPS당 단위 TCO 비교 (그룹 바) |
| `p6_layer_breakdown.png` | 자원 레이어 비중 파이 차트 (3개 시스템) |
| `p6_smr_saving_scatter.png` | SMR 절감액 vs 총 TCO 산점도 |
| `p6_glass_adoption.png` | Glass 채택률별 기판 비용 추이 |

---

## 7. P 시리즈 완료 현황

| 단계 | 내용 | 상태 |
|------|------|------|
| P2-1~P2-4 | Excel 7시트 + Notion 자동화 | ✅ |
| P3 | SMR 전력비 모델 (Sheet 8~9) | ✅ |
| P5 | MOIC/TCO 차트 5개 | ✅ |
| P4 | GitHub Actions 4-Job 파이프라인 | ✅ |
| **P6** | **ExaFLOPS 통합 자원모델** | ✅ |
| P7 | Word 보고서 자동 생성 DOCX | 🔜 |
