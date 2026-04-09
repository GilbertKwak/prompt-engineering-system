# 🤖 PE-3 — 자동검증 엔진 (Auto-Validation)

> **ID**: PE-3 | **상태**: ✅ 운영 | **파일**: `engines/PE-3_auto-validation/`

---

## 역할

5개 차원 품질 채점으로 프롬프트를 구조적으로 평가하고 합격/재처리 판정을 내리는 엔진입니다.

## 5차원 채점 표

| 차원 | 설명 | 가중치 |
|------|------|------|
| 명확성 | 목표/대상/제약 명시 여부 | 25% |
| 연관성 | 엔진 역할 일치 | 20% |
| 실행가능성 | 파싱 안정성 | 25% |
| 효율성 | 토큰 경제성 | 15% |
| 안전성 | 리스크 포함 여부 | 15% |

**통과 기준: 70점 이상**

## 관련 파일

- `engines/PE-3_auto-validation/scoring_rubric.md`
- `engines/PE-3_auto-validation/examples/`
- [docs/rca-capa/RCA-002.md](../rca-capa/RCA-002.md) — 검증 기준 RCA

---

> [Master Index](../index.md) | [engines/PE-3/](../../engines/PE-3_auto-validation/)
