# 📚 Knowledge Management Agent Domain

> Notion ↔ GitHub SSOT 지식관리 동기화 도메인

## 역할

- Notion 페이지 ↔ GitHub MD 파일 양방향 동기화
- 세션 로그 자동 저장
- 버전 히스토리 관리
- PE-3 채점 결과 반영

## SSOT 구조

```
T-09 Mother Page (Notion)
  └─ 세션 로그
  └─ KG 버전 히스토리
  └─ EW 리포트
  └─ PE-3 채점 현황

GitHub: GilbertKwak/prompt-engineering-system
  └─ automation/
  └─ agents/
  └─ output/
  └─ logs/
```

## 트리거 조건 (T-AUTO)

| ID | 조건 | 액션 |
|---|---|---|
| T-AUTO-01 | 세션 종료 | Notion 세션 로그 자동 저장 |
| T-AUTO-02 | MI RESOLVED | Annex B 자동 업데이트 |
| T-AUTO-03 | 새 리스크 발견 | 리스크 레지스터 자동 추가 |
| T-AUTO-04 | PE-3 점수 반영 | 마스터 프롬프트 채점표 업데이트 |
| T-AUTO-05 | v1.x 업그레이드 | GitHub 커밋 자동 생성 |
