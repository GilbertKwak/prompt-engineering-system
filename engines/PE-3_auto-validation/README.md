# ✅ PE-3: 자동검증 엔진 (Auto-Validation Engine)

> **Parent**: [prompt-engineering-system](https://github.com/GilbertKwak/prompt-engineering-system)  
> **버전**: v1.1 | **최종 수정**: 2026-04-05

---

## 개요

프롬프트 및 AI 출력물을 **5개 차원**으로 품질 채점하고,  
**합격(Pass) / 조건부 합격 / 재처리(Fail)** 판정을 자동으로 내립니다.

---

## 5차원 채점 기준

| 차원 | 코드 | 만점 | 측정 기준 |
|------|------|------|-----------|
| 정확성 (Accuracy) | A | 25 | 사실 오류, 수치 검증 |
| 완결성 (Completeness) | C | 20 | 요청 항목 누락 여부 |
| 구조성 (Structure) | S | 20 | 포맷·순서·가독성 |
| 실행가능성 (Actionability) | X | 20 | 즉시 활용 가능 수준 |
| 일관성 (Consistency) | I | 15 | 내부 논리 모순 |
| **합계** | | **100** | |

**판정 기준**:
- ✅ **Pass**: 85점 이상
- ⚠️ **Conditional Pass**: 70~84점 (명시된 약점 보완 후 사용)
- ❌ **Fail / Reprocess**: 69점 이하 (PE-1 재처리)

---

## 파일 구조

```
PE-3_auto-validation/
├── README.md              ← 본 파일
├── prompt_template.md     ← 자동검증 실행 프롬프트 템플릿
├── scoring_rubric.md      ← 5차원 상세 채점 기준표
└── examples/
```

---

> [Notion 대응 페이지](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b)
