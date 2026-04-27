# 🔷 FU-Series Adapter Prompt v1.0

> **파일**: `prompts/jv_fund/fu_adapter_v1.md`  
> **버전**: v1.0 | **날짜**: 2026-04-27  
> **검증룰**: PE-1 + FU-Series 데이터 크로스체크

---

## [PURPOSE]

FU-Series 기술 보고서(FU-001 ~ FU-025+)의 데이터를 JV 타당성 분석에 직접 연결하는 어댑터 프롬프트.

---

## [PARAMETERS]

```
- [FU_NUMBER]  : FU-001 ~ FU-025+  (필수)
- [SECTION]    : Market | Technical | Financial  (필수)
- [JV_TYPE]    : Equity | Contractual | Strategic Alliance  (기본값: Equity)
- [LANG]       : KR | EN | Bilingual  (기본값: Bilingual)
```

---

## [TASK]

1. FU-{FU_NUMBER} 보고서의 [{SECTION}] 섹션 데이터를 추출하라
2. 해당 데이터를 기반으로 JV 타당성을 재검증하라:
   - 기술 성숙도 (TRL 레벨)
   - 시장 진입 가능성
   - 파트너사 역량 요건
3. 기존 `master_v3.md`의 Step 1~5 체인과 연결하라
4. 결과를 다음 형식으로 출력하라:
   - Notion 페이지 업데이트 콘텐츠
   - GitHub PR 본문 초안

---

## [OUTPUT]

### Notion Update Block
```markdown
## FU-{FU_NUMBER} JV 연동 분석 결과
- 보고서 섹션: {SECTION}
- JV 타입: {JV_TYPE}
- 핵심 발견:
  1. ...
  2. ...
  3. ...
- 권장 액션: ...
- 검증 상태: PE-1 ✅ | FU 데이터 크로스체크 ✅
```

### GitHub PR Body
```markdown
## JV Fund Analysis — FU-{FU_NUMBER} Integration

### 변경 내용
- FU-{FU_NUMBER} {SECTION} 데이터 JV 분석에 반영

### 검증
- [ ] PE-1 준수
- [ ] FU-Series 데이터 크로스체크
- [ ] Notion 동기화

### 관련 링크
- FU Report: `applied-cases/FU-{FU_NUMBER}/`
- Notion: https://www.notion.so/34f55ed436f081c08fececa8dd7577f9
```

---

## [VALIDATION]

- [ ] FU 보고서 원본 데이터와 수치 일치 확인
- [ ] PE-1: 출처 명시 (FU 보고서 섹션 + 페이지)
- [ ] TRL 레벨 명시 (1~9)
- [ ] Notion SSOT 링크 기재
