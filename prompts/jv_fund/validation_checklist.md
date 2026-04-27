# ✅ JV Fund Prompt Validation Checklist

> **용도**: 프롬프트 제출 / 업데이트 전 필수 체크  
> **규칙**: PE-1 (사실 정확성) + PE-3 (시나리오 완성도)  
> **자동화**: `python automation/auto_validate.py --file <파일경로> --rules PE-1,PE-3`

---

## PE-1 체크리스트 (Factual Accuracy)

- [ ] **출처 명시**: 모든 수치 데이터에 출처 및 연도 기재 (최소 3개 이상)
- [ ] **연도 기재**: `$X억 (2025년 기준)` 형식으로 연도 병기
- [ ] **추정값 표기**: 추정/예측 수치에 `(est.)` 또는 `(추정)` 명시
- [ ] **반대 데이터**: 상반된 데이터 소스 또는 시각 최소 1개 병기
- [ ] **보장 수익률 금지**: "보장", "guaranteed", "확정 수익" 표현 사용 안함
- [ ] **가정사항 명시**: 모든 주요 가정(Assumption)을 명확히 기재

## PE-3 체크리스트 (Scenario Completeness)

- [ ] **Bearish Case**: 하락/부정 시나리오 최소 1개 포함
- [ ] **리스크 매트릭스**: 기술/상업/규제/지정학 리스크 작성
- [ ] **규제 리스크**: AIFMD, SEC, 금융위 등 관련 규제 명시
- [ ] **컨틴전시 플랜**: 리스크 대응 방안 기재
- [ ] **스트레스 테스트**: 최소 1개 시나리오 정량적 스트레스 테스트

## Output Quality 체크리스트

- [ ] **언어**: `[LANG]` 파라미터 준수 (KR/EN/Bilingual)
- [ ] **톤**: Institutional / Professional 유지
- [ ] **구조**: Executive Summary → 상세 분석 → 리스크 → 액션 플랜
- [ ] **Notion 호환**: MD 테이블 형식 확인
- [ ] **GitHub 링크**: SSOT 링크 기재
- [ ] **피듀셔리 플래그**: 수탁자 책임 리스크 명시적 표시

---

## 자동 검증 명령어

```bash
# 단일 파일 검증
python automation/auto_validate.py \
  --file prompts/jv_fund/master_v3.md \
  --rules PE-1,PE-3

# 전체 디렉터리 검증 + JSON 리포트 저장
python automation/auto_validate.py \
  --dir prompts/jv_fund \
  --rules PE-1,PE-3 \
  --output validation_report.json

# 조용히 실행 (CI/CD용)
python automation/auto_validate.py \
  --dir prompts \
  --rules PE-1,PE-3 \
  --quiet
```

---

## 관련 링크

- [Notion PE-JV 페이지](https://www.notion.so/34f55ed436f081c08fececa8dd7577f9)
- [Master Prompt v3.0](./master_v3.md)
- [auto_validate.py](../../automation/auto_validate.py)
- [GitHub Actions Workflow](../../.github/workflows/validate_prompts.yml)
