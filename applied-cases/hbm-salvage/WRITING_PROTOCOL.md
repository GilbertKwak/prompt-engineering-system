# HBM Salvage Report — Writing Protocol (작성 규칙)

**수립일**: 2026-04-10  
**버전**: v1.0  
**적용 범위**: HBM Salvage Value Program 전체 보고서 (Chapter 1–10)

---

## ✅ Rule 0 — 사전 확인 (Pre-Check)

> **보고서 작성 전** 반드시 아래 두 곳을 조회하여 현재 진행 상황을 확인한다.

- **Notion 허브**: https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b
- **GitHub 리포지토리**: https://github.com/GilbertKwak/prompt-engineering-system/tree/main/applied-cases/hbm-salvage

**확인 항목**:
- [ ] 완료된 챕터 번호
- [ ] 미완료 챕터 목록
- [ ] 최신 버전 번호
- [ ] 이전 세션 미처리 항목

---

## ✅ Rule 1 — 병렬 작성 (Bilingual Parallel)

> 모든 챕터는 **KO·EN 병렬 구조**로 작성한다.

- 한국어(KO) 먼저 작성 → 영문(EN) 재표현
- PE-3 자동검증 체크리스트 필수 포함
- 핵심 수치·결론은 KO·EN 완전 일치 확인

---

## ✅ Rule 2 — 사후 업데이트 (Post-Update)

> 챕터 완료 후 **Notion + GitHub 동시 업데이트**.

**GitHub 커밋 규칙**:
```
feat(hbm-salvage): [Chapter X] [KO/EN/Both] [brief description] [vX.X]
예: feat(hbm-salvage): Add Chapter 2 KO+EN defect analysis v1.0
```

**Notion 업데이트 항목**:
- 허브 페이지 버전 이력 갱신
- 챕터 상태 🔄 → ✅ 변경
- 완료일 기입

---

## ✅ Rule 3 — 목록 출력 (Status Report)

> 매 세션 종료 시 **3개 표를 의무 출력**한다.

1. 전체 보고서 챕터 목록 (상태 포함)
2. 완료된 작업 목록 (날짜·결과물·검증 상태)
3. 다음 세션 실행 목록 (우선순위 포함)

---

## 🔄 세션 시작 체크리스트

```
□ Rule 0: Notion 허브 fetch 완료
□ Rule 0: GitHub 디렉토리 확인 완료
□ 미처리 Rule 2 항목 존재 여부 확인
□ 현재 작업 챕터 번호 확정
□ 작업 시작
```
