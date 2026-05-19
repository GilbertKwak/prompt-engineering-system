# agents/kg_builder — KG Builder Agent

## 개요

Knowledge Graph 증분 빌더 에이전트의 프롬프트 및 설정 디렉토리입니다.
`ai_intel_collector`와 `ew_detector`의 출력을 입력으로 받아
`knowledge_graph_v{version}_delta.json`을 생성합니다.

## 노드 타입

`COMPANY` | `TECHNOLOGY` | `PERSON` | `EVENT` | `METRIC` | `REGULATION`

## 엣지 타입

`DEVELOPS` | `ACQUIRES` | `COMPETES_WITH` | `PARTNERS_WITH` | `REGULATES` | `INVESTS_IN` | `EW_SIGNAL`

## 버전 규칙

- **Major** (v4.x → v5.0): EW CRITICAL, 패러다임 전환
- **Minor** (v4.25 → v4.26): 신규 노드 5개+, EW HIGH
- **Patch** (v4.25 → v4.25.1): 속성 업데이트만
