# FU-Series JV 연동 프롬프트 (Adapter)

> **버전**: v1.0 | **날짜**: 2026-04-28  
> **부모 프롬프트**: `../master_prompt_v3.md`  
> **대상 레포**: GilbertKwak/fu-semiconductor-thermal

---

## [PURPOSE]

FU-Series 보고서(FU-001~025+)의 기술 분석 데이터를  
JV 펀드 타당성 분석에 직접 연결하는 어댑터 프롬프트.

---

## [CONTEXT]

```yaml
FU_Number: {fu_number}       # e.g. FU-008, FU-015
FU_Topic: {fu_topic}         # e.g. HBM4 Thermal, Vapor Chamber
Section_Reference: {section} # e.g. "Market Analysis", "Technical Specs"
JV_Stage: {jv_stage}         # Screening | Due-Diligence
```

---

## [TASK]

1. FU-{fu_number} 보고서의 `{section}` 섹션 데이터를 기반으로
2. 해당 기술 영역에서의 JV 타당성을 Master Prompt v3 프레임워크로 재검증
3. 기존 FU 보고서에 "JV Opportunity" 섹션 추가 제안

---

## [INPUT FORMAT]

```
[FU 보고서 관련 섹션 내용을 여기에 붙여넣기]
```

---

## [OUTPUT]

1. **JV 타당성 요약** (300자 이내)
2. **파트너 후보 3개사** (FU 보고서 언급 기업 우선)
3. **Notion 페이지 업데이트 초안**
4. **GitHub PR 본문 초안**

```bash
# GitHub PR 생성 명령어
gh pr create \
  --title "[FU-{fu_number}] JV Opportunity Analysis" \
  --body "FU 보고서 기반 JV 기회 분석 추가\n\n관련 레포: fu-semiconductor-thermal" \
  --label "jv-analysis,fu-series"
```

---

*Parent: master_prompt_v3.md | Repo: prompt-engineering-system*
