# MFA-AGENT-01 Changelog

## v2.0 — 2026-04-28

### 🚀 주요 변경사항
- **PE-3 점수:** 62점 → **94점** (Pass ≥92 달성)
- **Validator Agent (Agent 4) 신규 추가:** PE-1 / PE-3 / SSOT 3중 자동 검증
- **JSON Schema 완비:** 각 에이전트 output_schema 구조화
- **context_bus 추가:** 에이전트 간 데이터 전달 파이프라인 명시
- **routing_logic 추가:** stage 파라미터 기반 에이전트 활성화 로직
- **orchestration_config 추가:** 4-Phase 파이프라인 설정 (YAML 구조)
- **input_schema 추가:** domain / stage / depth / lang / proposal 파라미터 정의
- **PE-1 강제 규칙:** 수치 출처·연도 필수, DATA_GAP 태그 의무화
- **PE-3 베어리시 시나리오:** pe3_bearish_requirement 블록 추가
- **SSOT 메타데이터:** GitHub 경로 + Notion 페이지 ID 명시
- **모호성 처리 태그:** [[ASSUMPTION]], [[CONFLICT]], [[DATA_GAP]] 공식화

### 🔗 연동 체인
- 상위: MFA-ENG-01
- 하위: PE-NBD-04
- 부모 프레임워크: JV-04 (Notion: 35055ed436f081c2ade8d3fe8c4f580e)

### 📊 PE-3 상세 점수
| 기준 | v1.0 | v2.0 | 비고 |
|-----|:----:|:----:|----|
| 역할 명확성 | 12 | 20 | Orchestrator 라우팅 로직 추가 |
| 지시 구조 | 13 | 20 | context_bus + phase 설계 |
| 출력 형식 | 12 | 18 | JSON Schema 완비 |
| 모호성 처리 | 12 | 18 | 3종 태그 체계 |
| 재현성 | 13 | 18 | input_schema + SSOT 메타데이터 |
| **총점** | **62** | **94** | **Pass** |

---

## v1.0 — 2026-04-28 (원본)
- 최초 생성: sCO2_Market_Feasibility_Agent 기본 구조
- 원본 파일: `MFA-AGENT-01-v1.0.xml`
- PE-3 점수: 62/100
