# CHANGELOG — 프롬프트 엔지니어링 시스템

## [v1.2] — 2026-04-09

### Added
- `docs/index.md` — 전체 러스트 문서 허브
- `docs/rca-capa/README.md` — RCA/CAPA 인덱스 (표준 효과 지표 포함)
- `docs/rca-capa/RCA-001.md` — 프롬프트 구조 복잡도 (XML→Markdown 전환)
- `docs/rca-capa/RCA-002.md` — 검증 기준 모호성 (정량 스코어 전환)
- `docs/rca-capa/RCA-003.md` — 필수 고려사항 누락 (RISK 에이전트 개선)
- `docs/rca-capa/RCA-004.md` — 중복 출력 과다 (Orchestrator scope 명확화)
- Notion Mother Page: [🔧 RCA/CAPA 관리 시스템](https://www.notion.so/33d55ed436f081bfa2aeccc26f344de5)
- Notion Child Pages: RCA-001~004 (각 5-Why + CAPA + 검증 결과)

### Changed
- `README.md` — v1.2로 갱신, docs/ 구조 표시, RCA/CAPA 섹션 추가
- `README.md` — Notion Mother/Child 양방향 링크 표 전면 갱신

### Cross-links

| 방향 | 충료 |
|------|------|
| Notion Mother → GitHub | docs/index.md, docs/rca-capa/ 링크 포함 |
| GitHub README → Notion | 6개 Notion 페이지 링크 표 |
| GitHub RCA-00x → Notion | 각 RCA 파일 상단에 Notion URL 포함 |
| Notion Child → GitHub | 각 Child 페이지 하단에 GitHub URL 연동 |

---

## [v1.1] — 2026-04-05
### Added
- `engines/` 디렉토리 구조 전체 수립 (PE-1, PE-2, PE-3)
- `applied-cases/` 디렉토리 신설 — 실행 기록 관리
- `workflows/3engine_pipeline.md` — 통합 파이프라인 문서
- `applied-cases/2026-04-05_upgrade-execution.md` — 업그레이드 실행 기록
- 각 엔진별 `prompt_template.md` 및 `examples/` 폴더 추가
- PE-3 전용 `scoring_rubric.md` (5차원 채점 기준표)

### Changed
- README.md 전면 개편 — 저장소 전체 구조 명시

---

## [v1.0] — 2026-04-05
### Added
- 최초 저장소 생성
- 3-Engine 프레임워크(PE-1/PE-2/PE-3) 개념 정립
- Notion Hub 연동 구조 수립
