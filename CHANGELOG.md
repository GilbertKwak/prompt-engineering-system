# CHANGELOG — 프롬프트 엔진니어링 시스템

## [v1.4] — 2026-04-10

### Added
- `engines/PE-1_auto-refinement/upgrade_v1.4.md` — 자동개선 엔진 v1.4 업그레이드 프롬프트
- `engines/PE-2_auto-proliferation/upgrade_v1.4.md` — 자동증식 엔진 v1.4 업그레이드 프롬프트
- `engines/PE-3_auto-validation/upgrade_v1.4.md` — 자동검증 엔진 v1.4 업그레이드 프롬프트
- `applied-cases/2026-04-10_3engine-upgrade-v1.4.md` — v1.4 적용 실행 기록

### Changed
- `README.md` — v1.4로 갱신, 업그레이드 내역 반영
- `CHANGELOG.md` — v1.4 항목 추가
- `dashboard/metrics.md` — KPI 지표 v1.4 기준 갱신

### Upgrade Summary
자동개선·자동증식·자동검증 3-Engine에 다음 방식 적용:
- **자동개선**: Chain-of-Thought 구조 강화, 약점 탐지 정밀도 향상
- **자동증식**: 도메인 크로스오버 변형 로직 추가 (5→8 변형 타입)
- **자동검증**: 5차원 스코어링 + 신뢰도 가중치 시스템 도입

---

## [v1.3] — 2026-04-09

### Added
- `docs/agent1/README.md` — PE-1 자동개선 엔진 설명
- `docs/agent2/README.md` — PE-2 자동증식 엔진 설명
- `docs/agent3/README.md` — PE-3 자동검증 엔진 설명
- `docs/agent4/README.md` — PE-4 실적용 케이스 매니저
- `docs/agent5/README.md` — PE-5 마스터 오케스트레이터
- `docs/support/README.md` — 공통 지원 모듈 인덱스
- `docs/new/README.md` — 신규 기능 파이프라인
- `dashboard/README.md` — 메트릭스 대시보드 안내
- `dashboard/metrics.md` — KPI 추적 시트 (전체 지표 현황)

### Changed
- `docs/index.md` — Master Index로 전면 개편 (agent1~5, support, new, rca-capa, dashboard 전체 커버)
- `README.md` — v1.3으로 갱신, 5엔진 테이블, 전체 디렉토리 트리 반영

### Structure
재현 가능한 연구 프로젝트 구조 지침 준수:
- `docs/` — 배포 전용 문서 루트 (agent, support, new, rca-capa)
- `dashboard/` — 메트릭스 / KPI 독립 분리
- `engines/` — 실제 프롬프트 템플릿 저장소
- `applied-cases/` — 실적용 케이스 로그
- `workflows/` — 파이프라인 실행 설계

---

## [v1.2] — 2026-04-09
### Added
- `docs/index.md` — 문서 허브
- `docs/rca-capa/README.md` + `RCA-001~004.md`
- Notion Mother/Child 양방향 링크

### Changed
- README.md v1.2, CHANGELOG.md Cross-links 표 추가

---

## [v1.1] — 2026-04-05
### Added
- `engines/` 디렉토리 구조 (PE-1, PE-2, PE-3)
- `applied-cases/`, `workflows/3engine_pipeline.md`

### Changed
- README.md 전면 개편

---

## [v1.0] — 2026-04-05
### Added
- 최초 저장소 생성, 3-Engine 프레임워크 정립
