# HBM Salvage Value Program — 보고서 작성 규칙 (Writing Rules)

> **제정일**: 2026-04-10  
> **적용 범위**: HBM Salvage Value Program 전 챕터 (Chapter 1~10 예정)
> **관리 저장소**: `applied-cases/PE-4-HBM-Salvage/`

---

## 🔒 필수 작성 규칙 5개

### R-1. Notion & GitHub 사전 확인 의무 (Pre-Check Rule)
```
보고서 작성 시작 전 반드시 실행:
① Notion 허브 (https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b) 현황 확인
② GitHub PE-4-HBM-Salvage 폴더 기존 파일 목록 확인
③ 진행 상태(완료/진행 중/미착수) 확인 후 작성 순서 결정
④ 기존 내용과 중복·모순 여부 사전 점검
```

### R-2. 한국어 先 → 영문 後 순서 (Language Sequence Rule)
```
KO 초안 작성 → PE-3 검증 통과 → KO 확정본 저장
→ EN 재표현 (직역 금지, 글로벌 독자 최적화)
→ KR↔EN 대조 검증 → EN 확정본 저장
```

### R-3. PE-3 자동검증 체크리스트 필수 포함 (Validation Rule)
```
매 챕터 말미에 아래 7개 항목 검증 테이블 첨부:
1. 시장 데이터 정합성
2. 수율 수치 일관성  
3. Salvage 가치 산정 공식 재현 가능성
4. 불량 유형 분류 완전성
5. 타이밍 논거 항목 수
6. 경쟁 구도 플레이어 포함 여부
7. 데이터 경고 사항 (CAVEAT)
```

### R-4. 작성 완료 후 Notion + GitHub 동기화 의무 (Sync Rule)
```
작성 완료 즉시 실행:
① GitHub: applied-cases/PE-4-HBM-Salvage/ 에 Chapter 파일 커밋
② GitHub: 2026-04-10_PE4-progress-tracker.md 진행 현황 업데이트
③ Notion: 허브 버전 이력 테이블 업데이트
④ 출력: 전체 목록 / 완료 목록 / 미착수 목록 표 출력
```

### R-5. 챕터 간 연속성 보장 (Continuity Rule)
```
① 매 챕터 말미 "다음 장 Bridge" 섹션 포함
② 현 챕터 첫 문단에서 전 챕터 핵심 결론 요약 연결
③ 핵심 수치(시장 규모, 수율, Salvage 가치 등) 챕터 전체 일관 유지
```

---

## 📋 챕터 구성 표준 템플릿

```markdown
# Chapter N — [제목 KO] | [제목 EN]

## N.0 전 챕터 핵심 결론 연결 (Bridge from Ch.N-1)
## N.1 Executive Summary (KO + EN)
## N.2 [섹션1] (KO + EN)
## N.3 [섹션2] (KO + EN)
## N.4 [섹션3] (KO + EN)
## N.5 PE-3 자동검증 체크리스트
## N.6 다음 장 Bridge
```

---

## 🗂️ 파일 네이밍 규칙

```
ChapterNN_KO-EN_vX.Y.md   → 본문 보고서
2026-MM-DD_PE4-progress-tracker.md  → 진행 현황 추적
WRITING-RULES.md          → 본 문서 (작성 규칙)
```

---

*제정: 2026-04-10 | 관리자: Gilbert Kwak | 저장소: GilbertKwak/prompt-engineering-system*
