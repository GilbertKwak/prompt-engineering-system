# B-Star eCO2 JV Strategy Prompt v1.0

> **Parent**: [master_prompt_v3.md](../master_prompt_v3.md)  
> **Domain**: sCO2 Based Energy Systems  
> **Date**: 2026-04-27 | **PE-3 목표**: 90/100  
> **연동**: [B-Star-eCO2-Strategy](https://github.com/GilbertKwak/B-Star-eCO2-Strategy)

---

## 목적

B★ eCO₂ 소형 분산형 발전·냉각 시스템의 JV 파트너십 및 펀드 구조를 분석하는 특화 프롬프트.  
sCO2 터빈 기술과 데이터센터 냉각 수요의 시너지를 투자 관점에서 정량화한다.

---

## [CONTEXT INJECTION]

```yaml
BASE_PROMPT: master_prompt_v3.md
DOMAIN: sCO2
SUBDOMAIN: "{subdomain}"    # Power-Generation | DC-Cooling | Combined
TARGET_MARKET: "{market}"  # Korea | Southeast-Asia | US | EU
APPLICATION: "{app}"       # Datacenters | Industrial | Military | Residential
```

---

## [TASK — sCO2 특화]

### Step 1 — sCO2 기술 시장 분석
```
- 글로벌 sCO2 발전 시장 TAM (2026-2030)
- 소형 분산 발전 SAM 산출
- 데이터센터 냉각 연계 수요 정량화
- 한국 정부 R&D 지원 프로그램 매핑 (출처 명시)
```

### Step 2 — sCO2 파트너 매핑
```
국내 파트너 후보:
- 터빈/압축기 제조: DOOSAN, 한화파워시스템 등
- 열교환기: 경동나비엔, 귀뚜라미 계열 등
- 데이터센터 운영: KT, SK브로드밴드 등

해외 파트너 후보:
- sCO2 기술 선도: Echogen Power, Toshiba ESS 등
- 냉각 솔루션: Vertiv, Schneider Electric 등
```

### Step 3 — 3-Tier JV 구조 설계
```
Tier 1 — Singapore HoldCo (펀드 집결지)
Tier 2 — Korea R&D OpCo (기술 개발)
Tier 3 — US/APAC Sales Co (시장 확장)
→ 각 티어별 지분 구조, 세제 혜택, IP 귀속 방식 설계
```

### Step 4 — 정부 보조금 연계 분석
```
- 한국 산자부 에너지 R&D 과제 연계 가능성
- NET/NEP 인증 취득 전략
- IRA (미국 인플레이션감축법) 활용 방안
- EU 그린딜 보조금 연계 (해외 확장 시)
```

---

## [OUTPUT]

```json
{
  "domain": "sCO2",
  "market_sizing": {
    "global_sCO2_power_TAM": {"value": "", "year": "2030", "source": ""},
    "dc_cooling_integration_SAM": {"value": "", "note": "est."},
    "korea_priority_SOM": {"value": "", "note": "est."}
  },
  "partner_map": {
    "korea": [],
    "global": []
  },
  "jv_structure_3tier": {
    "singapore_holdco": {"equity": "", "tax_benefit": "", "ip_role": ""},
    "korea_rnd_opco": {"equity": "", "subsidy_linked": "", "key_milestones": []},
    "us_apac_sales": {"equity": "", "ira_benefit": "", "target_markets": []}
  },
  "government_subsidy_map": [
    {"program": "", "amount": "", "eligibility": "", "deadline": ""}
  ],
  "counter_scenario": {
    "assumption": "sCO2 TRL이 상업화 수준에 도달 가정",
    "failure_case": "기술 성숙 지연 시 DC 냉각 시장 진입 창 소멸",
    "probability": "M"
  },
  "next_actions": []
}
```

---

*Last updated: 2026-04-27 | prompt-engineering-system/prompts/jv_fund/variants/bstar_eco2_prompt.md*
