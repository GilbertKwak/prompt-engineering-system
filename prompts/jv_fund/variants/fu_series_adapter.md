# FU-Series 연동 JV 분석 프롬프트 (Variant A)

> **버전**: v1.0 | **기준일**: 2026-04-27 | **기반**: master_prompt_v3.md  
> **PE-3 점수**: 88/100 | **연동 레포**: `fu-semiconductor-thermal`

---

## [목적]

FU-Series 보고서(FU-001~FU-025+)의 시장 분석 및 기술 데이터를 기반으로  
합작투자(JV) 타당성을 재검증하고 투자 메모(Investment Memo)를 자동 생성합니다.

---

## [파라미터]

```yaml
FU_NUMBER:  "{fu_number}"    # e.g. FU-008 (HBM4-GPU Thermal)
FU_SECTION: "{section}"     # Market Analysis | Technical Specs | Financial Model
JV_STAGE:   "{jv_stage}"    # Screening | DD | Structuring
OUTPUT_TARGET: "{target}"   # Notion-Page | GitHub-PR | Word-Doc
```

---

## [실행 체인]

```
Step 1: FU_{fu_number} 보고서에서 '{section}' 섹션 추출
Step 2: 추출 데이터 기반 JV 파트너 요건 도출
  → 기술 역량 요건 (FU 보고서 기술 스펙 기반)
  → 재무 규모 요건 (FU 보고서 시장 규모 기반)
Step 3: 글로벌 파트너 후보 3개사 매핑
  → 각 후보사별 Fit Score (0~100) 산출
Step 4: JV 타당성 결론 (GO / CONDITIONAL / NO-GO)
Step 5: 후속 액션 자동 생성
  → GitHub Issue 초안
  → Notion 업데이트 항목
```

---

## [출력 포맷]

```markdown
## FU-{fu_number} JV Feasibility Memo

**결론**: GO / CONDITIONAL / NO-GO  
**신뢰도**: {confidence_score}/100  
**PE-3 점수**: {pe3_score}/100

### 핵심 근거
- 시장 규모: {tam} (출처: FU-{fu_number} {section})
- 기술 성숙도: TRL {trl_level}
- 파트너 Fit Score 1위: {partner_name} ({fit_score}/100)

### 리스크 (H×H 항목)
{risk_list}

### 반대 시나리오 (PE-3 필수)
{downside_scenario}

### 다음 액션
- [ ] GitHub Issue: {issue_title}
- [ ] Notion 업데이트: {notion_page}
```

---

## [검증 규칙]
- [ ] FU 보고서 섹션 출처 명시 (PE-1)
- [ ] GO/CONDITIONAL/NO-GO 근거 3가지 이상
- [ ] 반대 시나리오 포함 (PE-3)
- [ ] confidence_score 수치 출력

---

## [연동 FU 보고서 목록]

| FU 번호 | 주제 | JV 관련성 |
|---|---|---|
| FU-008 | HBM4-GPU Thermal Architecture | 🔴 High |
| FU-009~FU-012 | 첨단 패키징 열관리 | 🔴 High |
| FU-013~FU-016 | AI 가속기 냉각 시스템 | 🟡 Medium |
| FU-017~FU-020 | CPO 광학 열관리 | 🟡 Medium |
| FU-021~FU-025 | 사업화 전략 | 🔴 High |
