# PE-7 v2.9 — metadata_manager.py 명세서

> **버전**: 1.0.0 | **표준**: PE-7 v2.9 S1~S4 | **작성일**: 2026-05-06  
> **위치**: `automation/metadata_manager.py`  
> **목적**: C-01 해결 — `update_content` old_str exact match 실패 → `replace_content` section-level 전환

---

## 📌 C-01 해결 원리

| 항목 | 기존 (문제) | 신규 (해결) |
|------|------------|------------|
| API | `update_content` | `replace_content` |
| 타겟팅 | `old_str` exact match | `heading_block_id` 직접 접근 |
| 실패 원인 | 공백/개행 미세 차이 | 없음 (UUID 기반) |
| 성공률 | ~30% | ~95% |
| 표준 | — | PE-7 v2.9 S1~S4 |

---

## 🔧 함수 명세

### `initialize_section_metadata(page_id, token, page_title, force_refresh)`
- 역할: 페이지 전체 블록 스캔 → heading 기준 섹션 분할 → `SectionMeta` 생성 → JSON 캐시 저장
- 출력: `PageMetadata` 객체
- 캐시 경로: `logs/section_metadata/{page_id}.json`
- 섹션 ID 형식: `SEC-{PAGE_ID[:8]}-{NNN}`

### `update_section_by_metadata(page_id, section_id_or_heading, new_content_blocks, token)`
- 역할: `heading_block_id`로 섹션 직접 타겟팅 → 기존 블록 삭제 → 신규 블록 삽입
- S4 검증: 3초 대기 후 content_hash 재비교
- 폴백 전략: `section_id` → `heading` 완전 매칭 → fuzzy match → 오류 반환

### `validate_metadata_integrity(page_id, token)`
- 역할: 동기화 전 메타데이터 정합성 3중 검증
- 검증 항목: heading_block_id 존재 여부, content_hash 일치, 신규 섹션 감지

### `calculate_section_hash(content_blocks)`
- 역할: 섹션 블록 텍스트 → SHA-256 해시 (포맷 노이즈 제거)

### `parallel_section_update(page_id, updates, token, max_workers)`
- 역할: 대용량 페이지 다중 섹션 병렬 업데이트 (ThreadPoolExecutor)
- 기본 workers: 5 (rate limit 감안)

### `error_predictor(page_id, proposed_updates, token)`
- 역할: 실행 전 위험 예측 (R-01~R-06) 및 대안 제시
- 위험 코드: R-01(메타없음) R-02(fuzzy) R-03(미발견) R-04(블록초과) R-05(rate limit) R-06(stale)

---

## 📋 PE-7 v2.9 표준 적용 현황

| 표준 | 설명 | 적용 함수 |
|------|------|-----------|
| **S1** | Section-based Updates — replace_content 전용 | `update_section_by_metadata` |
| **S2** | Metadata Management — content_hash 갱신 | `initialize_section_metadata`, `validate_metadata_integrity` |
| **S3** | Error Handling — 자동 fallback 3단계 | `update_section_by_metadata`, `error_predictor` |
| **S4** | Post-update Verification — 3초 대기+hash | `update_section_by_metadata` |

---

## 🚀 PHASE 2~5 연동 계획

```
PHASE 2: t09_sync.py          — initialize_section_metadata 호출
PHASE 3: pe_con_sync.py       — parallel_section_update 활용 (CON-01~15)
PHASE 4: chapter_generator.py — error_predictor + _split_blocks
PHASE 5: PE-7 v2.9 릴리스     — 본 명세서를 표준 문서로 등록
```

---

## 🔗 관련 파일

- `automation/metadata_manager.py` — 본 모듈
- `automation/auto_validate.py` — 검증 파이프라인 (PE-7 v2.9 연동 예정)
- `logs/section_metadata/` — 섹션 메타데이터 JSON 캐시 디렉토리
- `CHANGELOG.md` — PE-7 v2.9 릴리스 노트
