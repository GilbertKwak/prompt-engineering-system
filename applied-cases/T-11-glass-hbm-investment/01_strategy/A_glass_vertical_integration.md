# Type A — Glass 수직통합 전략 (Core)

## 전략 개요
| 항목 | 내용 |
|------|------|
| **유형** | Core (포트폴리오 기반·안정) |
| **구조** | Samsung Electro-Mechanics + Corning + AGC 3자 JV, 15% 지분 |
| **투자금** | $500M USD (Balanced: $400M) |
| **목표 NPV** | $52.7M |
| **목표 MOIC** | 1.11x |
| **주요 리스크** | 한반도 지정학 15%, 기술 실현 지연 |

## 전략 근거
- Glass 기판은 실리콘 인터포저 대비 신호 손실 30% 개선, 원가 20% 절감 예상
- Samsung EM의 ABF 기판 → Glass 전환 로드맵(2026~2028) 조기 참여
- Corning(광학 유리), AGC(전기 유리) 이중 공급망으로 기술 헷지

## 실행 계획
### Phase 1 (2026 Q2-Q3)
- [ ] Samsung EM–Corning–AGC JV 참여 협상 착수
- [ ] 기술 실사 (Glass 기판 수율 데이터 확보)
- [ ] 지분 구조 확정 (15% 목표, 최소 10%)

### Phase 2 (2026 Q4-2027 Q1)
- [ ] JV 설립 법인 등기 (한국 또는 싱가포르)
- [ ] 1세대 Glass 기판 파일럿 라인 CAPEX 집행

### Phase 3 (2027-2028)
- [ ] HBM5 패키지 기판 공급 계약 체결
- [ ] 2세대 Glass 로드맵 반영 추가 투자 검토

## 재무 파라미터
```yaml
investment_usd: 500_000_000  # Baseline (400M in Balanced)
jv_stake_pct: 15
npv_usd: 52_700_000
moic: 1.11
irr_target_pct: 12
payback_years: 6
geopolitical_risk_pct: 15
```

## 프롬프트 참조
- v1 투자구조 정의: `../03_prompts/v1_core_satellite_hedge.md` § Type-A
- 재무모델: `../02_financial_model/model_scaffold.py` — class TypeA
