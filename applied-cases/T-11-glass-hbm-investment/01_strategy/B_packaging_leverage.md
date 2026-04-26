# Type B — 패키징 레버리지 전략 (Satellite)

## 전략 개요
| 항목 | 내용 |
|------|------|
| **유형** | Satellite (HBM 사이클 레버리지) |
| **구조** | SK hynix/Micron HBM4 오프테이크 2M units/year + TSMC CoWoS 15K wafers/year |
| **투자금** | $400M USD (Balanced: $350M) |
| **목표 NPV** | $3,158M |
| **목표 MOIC** | 8.90x |
| **주요 리스크** | 대만 해협 지정학 20%, HBM 가격 사이클 |

## 전략 근거
- HBM4 수요: 2026 8GB → 2028 24GB/GPU, 연간 40% 성장
- CoWoS 용량 제약: TSMC 2025 80K → 2027 200K wpm 확대 중 — 조기 오프테이크 프리미엄 가치
- 오프테이크 구조로 CAPEX 없이 공급망 레버리지 확보

## 실행 계획
### Phase 1 (2026 Q2)
- [ ] SK hynix HBM4 오프테이크 LOI 체결 (2M units/year, 3년)
- [ ] TSMC CoWoS 용량 확보 협상 (15K wafers/month)

### Phase 2 (2026 Q4-2027 Q1)
- [ ] 오프테이크 계약 확정 + 보증금 집행 ($100M)
- [ ] HBM4 램프업 일정 모니터링 체계 구축

### Phase 3 (2027-2028)
- [ ] HBM5 오프테이크 옵션 행사 검토
- [ ] CoWoS 3D 패키징 추가 용량 협상

## 재무 파라미터
```yaml
investment_usd: 400_000_000  # Baseline (350M in Balanced)
offtake_hbm4_units_per_year: 2_000_000
cowos_wafers_per_month: 15_000
npv_usd: 3_158_000_000
moic: 8.90
irr_target_pct: 45
payback_years: 2.5
taiwan_strait_risk_pct: 20
```

## 프롬프트 참조
- v1 투자구조 정의: `../03_prompts/v1_core_satellite_hedge.md` § Type-B
- 재무모델: `../02_financial_model/model_scaffold.py` — class TypeB
