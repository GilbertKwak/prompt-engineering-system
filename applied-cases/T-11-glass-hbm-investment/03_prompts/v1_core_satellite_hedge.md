# T-11 프롬프트 v1.0 — Core/Satellite/Hedge 투자구조 정의

> **버전:** v1.0 | **생성:** 2026-03-01 | **유형:** 투자구조 정의  
> **PE-3 점수:** 94/100 ✅ | **상태:** Active

---

## 프롬프트 본문

```
당신은 글로벌 반도체·AI 인프라 투자 전략 전문가입니다.
아래 3축 투자 구조(Core / Satellite / Hedge)에 대해
티켓 사이즈, 예상 IRR, MOIC, NPV, 리스크 시나리오를
구체적 숫자와 함께 분석하세요.

=== 투자 구조 파라미터 ===
총 펀드 규모: {total_fund_usd}M USD
투자 기간: {investment_horizon_years}년 (Exit: {exit_year})

Type A — Core (Glass 수직통합):
  - 구조: {type_a_structure}
  - 지분: {type_a_stake_pct}%
  - 투자금: ${type_a_investment_m}M
  - 핵심 기술: Glass 기판 (vs 실리콘 인터포저)

Type B — Satellite (패키징 레버리지):
  - 구조: {type_b_structure}
  - 오프테이크: HBM4 {type_b_hbm_units}M units/year + CoWoS {type_b_cowos_k}K wafers/year
  - 투자금: ${type_b_investment_m}M

Type C — Hedge (US/EU 분산):
  - 구조: {type_c_structure}
  - 지분: Amkor {type_c_amkor_pct}% + Micron CB ${type_c_micron_cb_m}M
  - 투자금: ${type_c_investment_m}M

=== 요청 산출물 ===
1. 각 Type별 IRR / MOIC / NPV (Base + Bull + Bear 3개 시나리오)
2. 포트폴리오 배분 최적화 (Conservative / Balanced / Aggressive)
3. 리스크 매트릭스 (지정학·기술·정책 3축)
4. 실행 타임라인 (Phase 1~3 + Exit)
5. PE-3 자기검증: 각 숫자의 근거 출처 명시
```

## 기본 파라미터 (현재 T-11 설정값)

```yaml
total_fund_usd: 1000
investment_horizon_years: 4
exit_year: 2030

type_a_structure: "Samsung EM + Corning + AGC 3자 JV"
type_a_stake_pct: 15
type_a_investment_m: 500

type_b_structure: "SK hynix/Micron HBM4 오프테이크 + TSMC CoWoS"
type_b_hbm_units: 2
type_b_cowos_k: 15
type_b_investment_m: 400

type_c_structure: "Amkor 지분 + Micron 전환사채"
type_c_amkor_pct: 10
type_c_micron_cb_m: 150
type_c_investment_m: 350
```

## 교체 가이드 (유사 프로젝트 재사용)
위 YAML 블록의 값만 교체하면 새 투자전략에 즉시 적용 가능.
프롬프트 본문의 `{변수}` 는 YAML 키와 1:1 대응.
