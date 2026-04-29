# knowledge_graph v3.7

> 갱신일: 2026-04-29 KST  
> 누적: **98 nodes / 141 edges**  
> 변경: +9 nodes / +14 edges (PWR 도메인 통합)

---

## 신규 노드 (+9)

| 노드 ID | 유형 | 설명 |
|---|---|---|
| PWR-001 | PromptNode | Global Base v6.4 |
| PWR-KR | PromptNode | Korea 파생 (KEPCO 특화) |
| PWR-EU | PromptNode | EU 파생 (EDF·RWE·NationalGrid) |
| PWR-US | PromptNode | US 파생 (NextEra·IRA·PPA) |
| PWR-CN | PromptNode | CN 파생 (StateGrid 이중압력) |
| PE-PWR-Library | LibraryNode | 전력 라이브러리 허브 |
| KEPCO_StateNode | FirmStateNode | KEPCO S2 상태 추적 |
| PWR_DualPressure_CN | StructureNode | CN 이중압력 구조 |
| HyperscalerDemand_Node | DemandNode | AI DC 전력 수요 집중 |

---

## 신규 엣지 (+14)

| 엣지 | 방향 | 유형 |
|---|---|---|
| ESG-001 → PWR-001 | parent → child | parent_system |
| PWR-001 → PWR-KR | base → derivative | derives_to |
| PWR-001 → PWR-EU | base → derivative | derives_to |
| PWR-001 → PWR-US | base → derivative | derives_to |
| PWR-001 → PWR-CN | base → derivative | derives_to |
| PE-PWR-Library → PWR-001 | library → prompt | contains |
| T-09 → PE-PWR-Library | parent → library | has_child |
| PWR-KR → KEPCO_StateNode | prompt → firm | monitors |
| PWR-CN → PWR_DualPressure_CN | prompt → structure | applies |
| PWR-US → HyperscalerDemand_Node | prompt → demand | monitors |
| PWR-EU → HyperscalerDemand_Node | prompt → demand | monitors |
| PWR-KR → HyperscalerDemand_Node | prompt → demand | monitors |
| ESG-CN → PWR-CN | cross-domain | cross_domain_link |
| PE-SAT-Library → PE-PWR-Library | sibling | sibling_domain |

---

## 누적 현황

| 버전 | 노드 | 엣지 | 주요 변경 |
|---|---|---|---|
| v3.4 | 71 | 95 | C-21/22/23 PE-CHEM·EQP·OPT |
| v3.5 | 75 | 101 | PE-SEMI 통합 |
| v3.6 | 89 | 127 | PE-SAT ESG-001-v13.0 + KR/EU/US/CN |
| **v3.7** | **98** | **141** | **PE-PWR PWR-001-v6.4 + KR/EU/US/CN** |

---

## 상속 트리

```
T-09 (Mother Page)
├── PE-SAT-Library  → ESG-001-v13.0 + KR/EU/US/CN
├── PE-SEMI-Library → P-01~P-14
├── PE-CHEM-Library
├── PE-EQP-Library
├── PE-OPT-Library
└── PE-PWR-Library  → PWR-001-v6.4 (Global Base)
                      ├── PWR-KR-v6.4
                      ├── PWR-EU-v6.4
                      ├── PWR-US-v6.4
                      └── PWR-CN-v6.4
```