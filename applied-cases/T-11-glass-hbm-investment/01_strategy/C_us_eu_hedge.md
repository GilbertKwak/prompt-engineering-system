# Type C — US/EU 지정학 헤지 전략 (Hedge)

## 전략 개요
| 항목 | 내용 |
|------|------|
| **유형** | Hedge (지정학 분산 + 정책 인센티브) |
| **구조** | Amkor Technology 지분 10% + Micron Technology 전환사채 $150M |
| **투자금** | $350M USD (Balanced: $250M) |
| **목표 NPV** | $3,676M |
| **목표 MOIC** | 11.50x |
| **주요 리스크** | 정책 변화 10%, CHIPS Act 집행 불확실성 |

## 전략 근거
- CHIPS Act $52B + EU Chips Act €43B — 정부 보조금 수혜 구조 선점
- Amkor Arizona 신공장(2025 가동): 미국 내 선단 패키징 거점 확보
- Micron CB: HBM4E 양산 시점(2027) 전환 시 업사이드 극대화

## 실행 계획
### Phase 1 (2026 Q2-Q3)
- [ ] Amkor 지분 10% 취득 (공개시장 또는 블록딜)
- [ ] Micron 전환사채 $150M 발행 협상 (전환가 $120, 3년 만기)

### Phase 2 (2026 Q4)
- [ ] EU Chips Act 보조금 신청 파트너십 (ESMC/Intel Fab 연계)
- [ ] US CHIPS 펀드 LP 참여 검토

### Phase 3 (2027-2028)
- [ ] Micron CB 전환 시점 판단 (HBM4E 양산 모니터링)
- [ ] Amkor 지분 추가 취득 또는 부분 매각 검토

## 재무 파라미터
```yaml
investment_usd: 350_000_000  # Baseline (250M in Balanced)
amkor_stake_pct: 10
micron_cb_usd: 150_000_000
micron_cb_conversion_price: 120
npv_usd: 3_676_000_000
moic: 11.50
irr_target_pct: 55
payback_years: 2.0
policy_risk_pct: 10
```

## 프롬프트 참조
- v1 투자구조 정의: `../03_prompts/v1_core_satellite_hedge.md` § Type-C
- 재무모델: `../02_financial_model/model_scaffold.py` — class TypeC
