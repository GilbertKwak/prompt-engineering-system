# B-Star eCO₂ JV Fund Prompt

> **Version:** v1.0  
> **Date:** 2026-04-28  
> **Domain:** sCO2 Based Energy Systems  
> **Linked Repo:** GilbertKwak/B-Star-eCO2-Strategy  

---

## [DOMAIN CONTEXT]

B★ eCO₂ 소형 분산형 발전·냉각 시스템의 글로벌 JV 파트너십 발굴 및 펀드 구조 설계에 특화된 프롬프트입니다.

**핵심 기술:** sCO₂ Brayton Cycle · 소형 터빈 (1~10 MW) · 데이터센터 폐열 회수  
**타겟 시장:** 한국 데이터센터 · 산업 플랜트 · 해양 플랫폼  

---

## [CONTEXT PARAMETERS]

```yaml
DOMAIN: "sCO2-Energy"
APPLICATION: "{application}"    # DC-Cooling | Industrial | Marine | Grid
PARTNER_TYPE: "{type}"          # Technology | EPC | Finance | Government
FUNDING_STAGE: "{stage}"        # Seed | Series-A | Series-B | Grant
GEO_FOCUS: "{geo}"              # KR | US | EU | Global
```

---

## [ANALYSIS CHAIN]

### Step 1: sCO₂ 시장 현황
- 글로벌 sCO₂ 터빈 시장 규모 (2024~2030)
- 주요 기술 플레이어 (Echogen · Toshiba · GE Research · 한국 KIER)
- 데이터센터 폐열 회수 수요 (AI 가속으로 인한 성장률)
- 정부 R&D 지원 프로그램 (한국 에너지기술평가원 · 미국 DOE)

### Step 2: JV 파트너 매핑 (3-Tier)
```
Tier 1 — 핵심 기술 파트너 (sCO₂ 터빈/열교환기)
Tier 2 — 시장 채널 파트너 (데이터센터 운영사/EPC)
Tier 3 — 재무 파트너 (VC/PE/정책금융)
```

### Step 3: JV 구조 설계
- **Singapore HoldCo** → 글로벌 IP 보유
- **Korea R&D OpCo** → 기술 개발 (정부 보조금 수혜)
- **US/EU Sales LLC** → 해외 시장 진입

### Step 4: 재무 모델 (간이)
```
CapEx: {capex_estimate} (est.)
OpEx/year: {opex_estimate} (est.)
Payback Period: {payback} years (est.)
IRR Target: {irr}%
Grant Coverage: {grant}%
```

### Step 5: 반대 시나리오 (PE-3)
- **Downside:** sCO₂ 효율 상용화 지연 → 파트너 철수 리스크
- **Mitigation:** 모듈식 설계 + 단계적 스케일업 전략

---

## [OUTPUT]

```json
{
  "domain": "sCO2-Energy",
  "jv_structure_recommendation": "Singapore HoldCo Model",
  "tier1_partners": [],
  "tier2_partners": [],
  "tier3_partners": [],
  "financial_model_summary": {},
  "government_grants_applicable": [],
  "next_actions": []
}
```

---

## [VALIDATION]
- [ ] PE-1: 시장 수치 출처 (IEA · KIER · DOE) 명시
- [ ] PE-3: Downside 시나리오 포함
- [ ] B-Star-eCO2-Strategy 레포 최신 이슈 반영

---

*Parent: prompts/jv_fund/master_prompt_v3.md*  
*Linked: GilbertKwak/B-Star-eCO2-Strategy*
