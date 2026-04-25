# 변형 B — TSMC 파트너 한정 정밀 탐색용 (v2.0 개선)

> **Base:** Master Prompt v2.0 | **Variant:** B | **Updated:** 2026-04-25
> **목적:** TSMC DCA/VCA 파트너 기업 정밀 탐색 및 파트너십 등급 분류

---

## [변경 사항 — v1.0 대비]

| 문제 | 원인 | 해결 |
|---|---|---|
| Type C 기업 대다수 탈락 | TSMC DCA 조건 적용 시 IT서비스 기업 탈락 | Type C 서브-변형 별도 정의 |
| VCA 기준 불명확 | VC 확인 수치 없음 | TSMC Value Chain Aggregator 정의 명시 |

---

## [TSMC PARTNER FILTER]

```yaml
tsmc_partner_criteria:
  DCA:  # Design Center Alliance
    definition: "TSMC가 공식 인증한 설계 파트너 (Design Center Alliance)"
    source: "https://www.tsmc.com/english/partnersupport/designCenter"
    types: ["TypeA", "TypeB"]  # TypeA/B 주요 대상
    verification: "TSMC 공식 파트너 페이지에서 확인 가능한 기업만"
  
  VCA:  # Value Chain Aggregator
    definition: "TSMC IP/EDA 파트너 + 설계 서비스를 통합 제공하는 기업"
    criteria:
      - "TSMC IP Alliance 또는 OIP(Open Innovation Platform) 참여"
      - "TSMC와 공동 PDK(Process Design Kit) 개발 이력"
    types: ["TypeA", "TypeB", "TypeD"]
  
  TypeC_subvariant:
    note: "Type C (IT서비스 기반) 기업은 TSMC 직접 파트너가 아닌 경우 많음"
    alternative_criteria:
      - "Arm DesignStart 참여"
      - "RISC-V Foundation 멤버"
      - "Synopsys/Cadence/Mentor 공식 서비스 파트너"
    output: "D-1B_TypeC 별도 섹션으로 분리"

other_foundry_partners:
  GlobalFoundries:
    program: "GF Certified Design Partner"
    types: ["TypeA", "TypeB"]
  Samsung_Foundry:
    program: "Samsung Foundry Design Solution Partner (DSP)"
    types: ["TypeA", "TypeB"]
  UMC:
    program: "UMC Design Alliance"
    types: ["TypeA"]
```

## [변형 B 전용 산출물]

- D-1B: TSMC DCA/VCA 파트너 기업 목록 (파트너십 등급 포함)
- D-1B_TypeC: TypeC 기업 전용 섹션 (Arm/RISC-V/EDA 파트너 기준)
- D-2B: 파트너십 등급별 상세 분석
