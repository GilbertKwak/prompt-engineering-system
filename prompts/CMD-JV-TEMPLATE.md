# CMD-JV · JV 재무 구조 조정 커맨드 템플릿
<!-- version: 2.1 | updated: 2026-05-17 | SK On 시나리오 슬롯 확장 -->

## 메타데이터

```yaml
cmd_id:        "CMD-JV-{NN}"           # 예: CMD-JV-01
domain:        "PE-FIN / PE-JV"        # 연관 도메인
target_entity: ""                      # 예: SK_On / Samsung_SDI
base_year:     2024                    # 기준 회계연도
forecast_end:  2029                    # 예측 종료 연도
graph_version: "v4.3"
run_date:      "YYYY-MM-DD"
author:        "GilbertKwak"
```

---

## 1. 커맨드 목적

> 한 줄 요약: 어떤 기업의 재무 구조 조정 시나리오를 분석하는가?

| 항목 | 내용 |
|------|------|
| 분석 유형 | JV 파트너 / 분사·IPO / 무재조정 시나리오 비교 |
| 핵심 지표 | 매출 / EBITDA / 순부채 / CAPEX / IRR 조정 |
| GNN 연동 | PE-MIN HHI S3 카스케이드 충격 반영 여부 |

---

## 2. 파라미터 슬롯

```yaml
params:
  entity:            ""         # 분석 대상 기업 (예: SK_On)
  scenarios:                    # 활성화할 시나리오 목록
    - Base
    - JV_Partner              # A: JV 파트너 유치
    - Spinoff_IPO             # B: 분사·상장
    - No_Restructuring        # C: 무재조정 + 충격 누적
  shock_overlay:     true       # PE-MIN HHI 광물 충격 오버레이 적용
  gnn_impact_pp:     -18.3      # GNN 누적 충격 (pp, knowledge-graph 기준)
  irr_threshold_bps: 100        # IRR 조정 임계치 (bps)
  output_format:     "table+chart"  # table / chart / table+chart
```

### 시나리오 세부 파라미터

```yaml
scenario_params:
  JV_Partner:
    partner_capex_share: 0.35   # CAPEX 분담 비율
    ebitda_turn_year: 2027      # 흑자전환 목표 연도
    net_debt_2029F_tril: 6.5    # 순부채 목표 (KRW 조원)
  Spinoff_IPO:
    net_debt_2029F_tril: 4.5
    revenue_growth_cap: 0.04    # 연평균 매출성장 상한
  No_Restructuring:
    mineral_shock_start: 2025   # 광물 충격 시작 연도
    hhi_cascade_prob: 0.569     # Samsung_F S3→S4 전이 확률
    net_debt_breach_tril: 22.0  # 리파이낸싱 위험 임계치
```

---

## 3. 실행 체크리스트

- [ ] `entity` 및 `base_year` 재무 데이터 최신 여부 확인
- [ ] `shock_overlay: true` 시 `gnn_impact_pp` 값을 knowledge-graph 최신 버전과 동기화
- [ ] 시나리오별 CAPEX 분담 / 순부채 목표 합리성 검증
- [ ] IRR 조정 bps 기준: `irr_threshold_bps >= 100` 이면 JV 우선 권고
- [ ] 차트 저장: `docs/charts/CMD-JV-{NN}_{date}.png`
- [ ] 메타 JSON 저장: `docs/charts/CMD-JV-{NN}_{date}.png.meta.json`
- [ ] Notion `PE-FIN` 페이지 재무 테이블 동기화

---

## 4. 출력 구조

### 4-1. 시나리오 비교 테이블 (KRW 조원)

```
| 연도 | 지표    | Base  | JV_Partner | Spinoff_IPO | No_Restructuring |
|------|---------|-------|------------|-------------|------------------|
| 2027 | 매출    |  ...  |     ...    |     ...     |       ...        |
| 2027 | EBITDA  |  ...  |     ...    |     ...     |       ...        |
| 2029 | 순부채  |  ...  |     ...    |     ...     |       ...        |
| 2029 | CAPEX   |  ...  |     ...    |     ...     |       ...        |
```

### 4-2. 출력 차트 형식

```
멀티 라인 차트 (연도 x축 / KRW 조원 y축):
  - Base:              회색 실선
  - JV_Partner:        청록 실선 (Primary)
  - Spinoff_IPO:       파랑 점선
  - No_Restructuring:  빨강 파선 (위험 강조)
  리파이낸싱 임계선: 수평 점선 (22조 기준)
```

### 4-3. 의사결정 요약 JSON

```json
{
  "cmd_id": "CMD-JV-{NN}",
  "entity": "",
  "run_date": "YYYY-MM-DD",
  "recommended_scenario": "",
  "recommendation_condition": "",
  "scenarios": [
    {
      "id": "JV_Partner",
      "revenue_2029F": 0,
      "ebitda_2029F": 0,
      "net_debt_2029F": 0,
      "capex_2029F": 0,
      "irr_adj_bps": 0,
      "risk_flag": false
    }
  ],
  "shock_applied": true,
  "gnn_impact_pp": -18.3
}
```

---

## 5. 의사결정 규칙

```
IF irr_adj_bps >= 100  → JV_Partner 권고 (CAPEX 분담 + 흑자전환 가속)
ELSE IF 단기 안정 우선 → Spinoff_IPO 권고 (순부채 최소화)
IF shock_overlay AND hhi_cascade_prob >= 0.50 → No_Restructuring 위험 플래그 ON
  → 회사채 리파이낸싱 임계치(net_debt_breach_tril) 도달 경고 발생
```

---

## 6. YAML-safe 실행 가이드

> **YAML 문법 충돌 방지 원칙** (pe7_product_mece_loop.yml L82 교훈)

```bash
# ✅ 올바른 방법
python automation/pe7_summary.py --cmd CMD-JV-{NN} --output $GITHUB_STEP_SUMMARY

# ❌ 금지: run: | 블록 내 인라인 python3 -c "..." + 딕셔너리 키 이스케이프 혼용
```

---

## 7. 연관 커맨드

| CMD ID | 설명 |
|--------|------|
| **CMD-JV-01** | **SK On 재무 구조 조정 시나리오** ← 현재 |
| CMD-JV-02 | Samsung SDI JV 파트너십 IRR 시뮬레이션 |
| CMD-JV-03 | 배터리 소재 JV 공급망 리스크 통합 분석 |
| CMD-FS-04 | 경로 충격 전파 분석 (PE-MIN HHI 연동) |

---

## 8. 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v1.0 | 2026-04-30 | 최초 생성 |
| v2.0 | 2026-05-16 | pe7_summary.py 연동, YAML-safe 섹션 추가 |
| **v2.1** | **2026-05-17** | 시나리오 세부 파라미터 슬롯 확장, 의사결정 규칙 명문화, 연관 CMD 테이블 추가, No_Restructuring 리파이낸싱 임계치 파라미터 추가 |
