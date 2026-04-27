# JV Fund Prompt Validation Checklist

<!-- Version: v2.0 | Date: 2026-04-28 -->

## PE-1 — 데이터 정확성 검증

```
[ ] 모든 시장 규모 수치에 출처 명시 (기관명 + 연도)
[ ] 추정값(est.)과 확정값 구분 표기
[ ] 최소 3개 이상의 독립적 출처 활용
[ ] 수치 상충 시 범위로 표기 (e.g., $X–$YB)
[ ] 연도 기재: 2023, 2024, 2025, 2026 명확히 구분
[ ] 1차 출처 vs 2차 출처 구분
```

## PE-3 — 시나리오 다양성 검증

```
[ ] 낙관 시나리오 (Bull Case) 포함
[ ] 기준 시나리오 (Base Case) 포함
[ ] 비관 시나리오 (Bear Case) 포함
[ ] 반대 의견/반론 최소 1개 포함
[ ] 불확실성 요인 명시 (최소 2개)
[ ] 시나리오별 확률 가중치 표기 (선택)
```

## PE-5 — 출력 완결성 검증

```
[ ] Task Chain 5단계 모두 포함
[ ] Executive Summary (500자 이내) 포함
[ ] JSON 출력 포맷 포함
[ ] Notion 호환 MD 테이블 포함
[ ] GitHub Issue 생성 명령어 포함
[ ] KR/EN 병기 (Bilingual 설정 시)
[ ] 파트너 매핑 테이블 (국내 + 해외 각 3개 이상)
[ ] 리스크 매트릭스 (4개 유형 이상)
[ ] 실행 로드맵 (90일/6개월/1년)
```

## 자동 검증 명령어

```bash
# 전체 검증 실행
python automation/auto_validate.py \
  --file applied-cases/jv-fund/master_prompt_v3.md \
  --rules PE-1,PE-3,PE-5 \
  --output validation_report.json

# 빠른 체크 (PE-1만)
python automation/auto_validate.py \
  --file applied-cases/jv-fund/master_prompt_v3.md \
  --rules PE-1

# 모든 JV 파일 일괄 검증
python automation/auto_validate.py \
  --dir applied-cases/jv-fund/ \
  --rules PE-1,PE-3,PE-5
```

## 검증 점수 기준

| 점수 | 기준 | 처리 |
|---|---|---|
| 90-100% | ✅ Pass | 즉시 사용 가능 |
| 70-89% | ⚠️ Review | 수정 후 사용 |
| 50-69% | 🔄 Rework | 주요 항목 재작성 |
| 0-49% | ❌ Fail | 전면 재작성 |
