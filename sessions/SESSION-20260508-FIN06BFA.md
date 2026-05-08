# SESSION-20260508-FIN06BFA
**날짜**: 2026-05-08 (금) 10:14 ~ 10:51 KST
**주제**: FIN-06-BFA Entry EV 협상 시뮬레이션 + IRR 모델 v2 (PIK 복리 + Ratchet 통합 재실행)
**PE 프레임**: PE-FIN / FIN-06
**SSOT**: `prompts/PE-FIN/pe_fin_06_pe_investment_v2.0.md`
**PE-3 스코어**: 92% ✅

---

## 세션 흐름

### PHASE 1 — FIN-06-BFA v1.0: Entry EV 협상 시뮬레이션 (10:14 KST)

**수행 내용**
- Entry EV 700M ~ 1,080M 전 범위 IRR/MOIC 매트릭스
- v1 Base 구조 (CB 쿠폰 3.5%, 전환가 $7.15) 기준 역산
- Fund 목표 IRR 20% 달성 조건 역산
- **Bear Gate 확인**: Entry EV 900M + 단순 CB → P50 IRR 10.1% (❌ BEAR)

**핵심 발견**
```
v1 Base P50 IRR 10.1% → Fund 목표 20% 미달 (-9.9pp)
구조 개선 Option 3+4 복합 권고:
  Option 3: 쿠폰 현금 3% + PIK 5%
  Option 4: Ratchet 강화
```

**출력 파일**: `reports/evp/astrachips_fin06_bfa_20260508.md` (커밋 `6dac43a9`)

---

### PHASE 2 — Notion + GitHub 저장 (10:34 KST)

- **Notion**: https://www.notion.so/35a55ed436f081169ddcc0eb0951acbc
- **GitHub**: `reports/evp/astrachips_fin06_bfa_20260508.md`

**추가 진행 권고 5선:**
1. IRR 모델 v2 PIK 복리 + Ratchet 통합 재실행 → 다음 세션 진행
2. Term Sheet v2.1 법무 초안 (2026-05-12)
3. Entry EV 카운터오퍼 준비 820M 제시 / 850M 수용 상한 (2026-05-13)
4. Tranche B KPI 설계 (2026-05-15)
5. PIK 세금 처리 검토 (2026-05-20)

---

### PHASE 3 — IRR 모델 v2.0 재실행 (10:41 KST)

**모델 v2 Full 사양**

| 파라미터 | v1 Base | v2 Full |
|---------|---------|--------|
| 현금 쿠폰 | 3.5% | 3.0% |
| PIK 쿠폰 | 0% | 5.0% 복리 |
| 총 쿠폰 | 3.5% | 8.0% |
| Ratchet | 없음 | IRR<15% 시 -10% |
| MOIC Floor | 없음 | 1.5× 보장 Put |

**6섹션 실행 결과 요약**

| 섹션 | 핵심 결과 |
|------|----------|
| A: 구조별 비교 | v2 Full P50 17.1% (+7.0pp vs v1) |
| B: Entry EV 매트릭스 | 850M P50 16.0% 🟡 / 700M P50 20.1% ✅ |
| C: PIK 분해 | 지분율 8.1% → 11.5% (+3.4pp) |
| D-1: PIK 쿠폰 조정 | PIK 11% 시 P50 21% ✅ |
| D-2: Ratchet 할인 조정 | -20% 시 P50 19.8% (근접) |
| E/F: 최적 3안 + 9-cell | v2_Aggressive P50 21% ✅ |

**저장 완료**: `reports/evp/astrachips_fin06_bfa_irr_v2_20260508.md` (커밋 `389d51e6`)

---

## 핵심 의사결정

### Bear Gate 입욥 확정
```
[문제] v1 Base P50 IRR 10.1% → Fund 목표 20% 심각하게 미달
[해결] v2 Full P50 IRR 17.1% (+7.0pp) | P10 11.0% (WACC 도달)
[잔여 갭] -2.9pp → PIK 인상 또는 Ratchet 강화로 커버 가능
```

### 최적 협상 패키지
```
Entry EV:    USD 850M (타겟) / 900M (수용 상한)
쿠폰:        현금 3.0% + PIK 8.0% = 실효 11.0%
Ratchet:    IRR < 15% 시 전환가 추가 -20%
MOIC Floor: 1.5× 보장 Put (만기 5년)
예상 P50 IRR: ~19% (20% 근접)
```

---

## 산출물 (Artifacts)

| 타입 | 파일 | 내용 |
|------|------|------|
| Notion | [FIN-06-BFA 협상 v1.0](https://www.notion.so/35a55ed436f081169ddcc0eb0951acbc) | v1 IRR 역산 전체 |
| GitHub | `astrachips_fin06_bfa_20260508.md` | v1.0 보고서 |
| GitHub | `astrachips_fin06_bfa_irr_v2_20260508.md` | v2.0 PIK+Ratchet 완성본 |
| Chart | `irr_structure_comparison.png` | 구조별 P50 IRR 바차트 |
| Chart | `irr_heatmap_v2.png` | 9-cell IRR 히트맵 |

---

## 미결 항목 (Open Items)

| # | 항목 | 유형 | 기한 |
|---|------|------|------|
| 1 | Term Sheet v2.1 법무 초안 (PIK 8~11% 반영) | 🔴 Critical | 2026-05-12 |
| 2 | Entry EV 820M 카운터오퍼 준비 | 🔴 Critical | 2026-05-13 |
| 3 | Tranche B 65M 마일스톤 KPI 설계 | 🟠 High | 2026-05-15 |
| 4 | PIK 세금 처리 검토 | 🟠 High | 2026-05-20 |
| 5 | IC 보고용 1-pager (PIK 11% + Ratchet -20%) | 🟡 Medium | 2026-05-20 |

---

## 다음 세션 쿼리 추천

```
[P1] Term Sheet v2.1 법무 초안
     → "Term Sheet v2.1 PIK 8% + Ratchet -20% + MOIC Floor 1.5× 반영 초안"

[P2] IC 보고용 Executive Summary
     → "FIN-06-BFA IC 제출용 1-pager (v2_Full 구조 기준)"

[P3] Tranche B KPI
     → "Tranche B 65M 마일스톤 KPI: 2027E 매출 273M+ 조건 설계"
```

---

## 연계 페이지

- **Notion 세션**: https://www.notion.so/35a55ed436f081169ddcc0eb0951acbc
- **전일 세션**: sessions/SESSION-20260507-OPT-DD-FIN.md
- **CB Term Sheet v2.0**: reports/evp/astrachips_term_sheet_2026.md
- **CB/Ratchet 보완**: reports/evp/astrachips_ratchet_v1.md
- **EVP v1.0**: reports/evp/astrachips_evp_v1.md

---
*세션 종료: 2026-05-08 10:51 KST | 다음 세션: Term Sheet v2.1 법무 초안*
