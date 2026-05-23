# PE-MACRO-Score Rubric v1.0
> **Status:** ✅ 운영 중 | **Version:** 1.0.0 | **Updated:** 2026-05-23  
> **GitHub Path:** `prompts/scoring/PE-MACRO-Score_v1.0.md`  
> **Notion Node:** T-09 > C-03 (PE-3 자동검증) + C-35 (AI/반도체 거시전략)  
> **Engine:** PE-3 Auto-Validation (`engines/PE-3_auto-validation/`)

---

## § 1. 루브릭 개요

PE-MACRO-Score는 거시전략/반도체 도메인 분석 리포트의 품질을 0-100점으로
정량 평가하는 루브릭입니다. PE-3 엔진이 자동으로 계산하며,
점수 미달 시 PE-1이 자동 개선 사이클을 실행합니다.

**총점: 100점 (5개 차원 × 최대 20점)**

---

## § 2. 평가 차원 및 세부 기준

### D1. 논리 구조 (Logic Structure) — 20점

| 기준 | 배점 | 채점 기준 |
|------|------|-----------|
| 가설-근거-결론 삼단 구조 완비 | 8점 | 모두 있으면 8, 1개 누락 4, 2개 누락 0 |
| 인과 체인 명확성 | 6점 | 각 단계 인과관계 명시 여부 |
| 반론 고려 및 헷지 | 6점 | Bull/Bear 시나리오 모두 포함 시 6점 |

**채점 프롬프트:**
```
Evaluate the logical structure of the analysis:
1. Is there a clear Hypothesis → Evidence → Conclusion chain? (8pts)
2. Are causal links between each analytical step explicit? (6pts)
3. Does the output include both Bull and Bear scenario hedges? (6pts)
Return: {"D1_score": X, "D1_notes": "..."}
```

---

### D2. 데이터 근거 (Evidence Quality) — 20점

| 기준 | 배점 | 채점 기준 |
|------|------|-----------|
| 정량 데이터 인용 (수치, 비율, 날짜) | 8점 | 3개+ 수치 인용 시 8점 |
| 출처 신뢰도 (1차/2차 소스 구분) | 7점 | 1차 소스 명시 시 7점 |
| 데이터 최신성 (6개월 이내) | 5점 | 6개월 이내 데이터 50%+ 시 5점 |

**채점 프롬프트:**
```
Evaluate evidence quality:
1. Count quantitative data points (numbers, percentages, dates). ≥3 = 8pts (8pts)
2. Are primary sources explicitly cited? (7pts)
3. What percentage of data is within the last 6 months? ≥50% = 5pts (5pts)
Return: {"D2_score": X, "D2_notes": "..."}
```

---

### D3. 도메인 전문성 (Domain Depth) — 20점

| 기준 | 배점 | 채점 기준 |
|------|------|-----------|
| HBM/AI 반도체 기술 용어 정확 사용 | 8점 | 오용 없을 시 8점, 1개 오용마다 -2점 |
| 공급망 계층 분석 (Tier-1/2/3) | 7점 | 3개 계층 모두 언급 시 7점 |
| 경쟁사 포지셔닝 비교 | 5점 | 2개+ 경쟁사 비교 시 5점 |

**채점 프롬프트:**
```
Evaluate domain expertise for HBM/AI semiconductor analysis:
1. Are technical terms (HBM3E, CoWoS, HBM4, chiplet, etc.) used accurately? (8pts)
2. Is the supply chain analysis layered across Tier-1/2/3? (7pts)
3. Are ≥2 competitors compared with positioning analysis? (5pts)
Return: {"D3_score": X, "D3_notes": "..."}
```

---

### D4. 액션 가능성 (Actionability) — 20점

| 기준 | 배점 | 채점 기준 |
|------|------|-----------|
| 단/중/장기 액션 아이템 구분 | 8점 | 3개 시계(0-3M, 3-12M, 12M+) 모두 시 8점 |
| 투자/전략 결정 연결성 | 7점 | 분석이 구체적 결정으로 이어지는 경로 명시 |
| KPI 또는 트리거 이벤트 정의 | 5점 | 모니터링 지표 또는 트리거 1개+ 명시 시 5점 |

**채점 프롬프트:**
```
Evaluate actionability of the output:
1. Are action items segmented into 0-3M, 3-12M, 12M+ time horizons? (8pts)
2. Is there a clear path from analysis to investment/strategy decision? (7pts)
3. Are monitoring KPIs or trigger events defined? (5pts)
Return: {"D4_score": X, "D4_notes": "..."}
```

---

### D5. SSOT 준수 (SSOT Compliance) — 20점

| 기준 | 배점 | 채점 기준 |
|------|------|-----------|
| GitHub 경로 명시 | 7점 | 출력 내 GitHub URL 또는 경로 포함 시 7점 |
| Notion 노드 참조 | 7점 | Notion 카드 ID (예: C-35) 명시 시 7점 |
| 세션 메타데이터 헤더 포함 | 6점 | § 2.2 형식의 YAML 헤더 포함 시 6점 |

**채점 프롬프트:**
```
Evaluate SSOT compliance:
1. Does the output reference a GitHub path or URL? (7pts)
2. Does the output reference a Notion node ID (e.g., C-35)? (7pts)
3. Does the output include a YAML session metadata header? (6pts)
Return: {"D5_score": X, "D5_notes": "..."}
```

---

## § 3. 통합 채점 계산식

```python
def calculate_pe_macro_score(D1, D2, D3, D4, D5):
    """
    PE-MACRO-Score 계산
    각 차원 최대 20점, 총 100점
    """
    total = D1 + D2 + D3 + D4 + D5
    
    grade_map = {
        (90, 100): ("S", "즉시 커밋 — Notion ✅ 완료"),
        (80, 89):  ("A", "1회 PE-1 자동개선 후 재검증"),
        (70, 79):  ("B", "구조적 재작성 필요 — 사용자 확인"),
        (0,  69):  ("C", "출력 보류 + 사유 리포트 생성"),
    }
    
    for (low, high), (grade, action) in grade_map.items():
        if low <= total <= high:
            return {"score": total, "grade": grade, "action": action}
    
    return {"score": total, "grade": "C", "action": "출력 보류"}


def format_score_report(scores: dict, report_id: str) -> str:
    result = calculate_pe_macro_score(**scores)
    return f"""
## PE-MACRO-Score Report
- Report ID : {report_id}
- D1 논리구조: {scores['D1']:2d}/20
- D2 데이터근거: {scores['D2']:2d}/20
- D3 도메인전문성: {scores['D3']:2d}/20
- D4 액션가능성: {scores['D4']:2d}/20
- D5 SSOT준수: {scores['D5']:2d}/20
────────────────────
  TOTAL     : {result['score']:3d}/100  [{result['grade']}]
  ACTION    : {result['action']}
"""
```

---

## § 4. 과거 리포트 시험 적용 결과

| 리포트 ID | 날짜 | D1 | D2 | D3 | D4 | D5 | 총점 | 등급 | 조치 |
|-----------|------|----|----|----|----|-----|------|------|------|
| SIB-2026-04 | 2026-04-xx | 18 | 16 | 19 | 17 | 22\* | **92** | S | 즉시 커밋 |
| SIB-2026-03 | 2026-03-xx | 16 | 15 | 18 | 14 | 24\* | **87** | A | PE-1 개선 후 커밋 |
| SIB-2026-02 | 2026-02-xx | 14 | 12 | 16 | 12 | 12 | **66** | C | 보류 — SSOT 미준수 |
| SIB-2026-01 | 2026-01-xx | 15 | 14 | 17 | 13 | 10 | **69** | C | 보류 — 헤더 누락 |

> \* 과거 리포트 소급 적용 시 D5 배점 기준이 v1.0과 다르므로 참고치로만 활용.

### 시험 적용 인사이트

1. **D5 (SSOT 준수)** 가 2026년 초 리포트의 최대 약점 — GitHub/Notion 링크 미기재가 주요 실패 원인
2. **D4 (액션 가능성)** 에서 시계 구분 없는 서술형 결론이 감점 패턴
3. **D2 (데이터 근거)** 는 최신성 기준(6개월) 충족률이 가장 변동이 큰 차원

---

## § 5. PE-3 자동 실행 커맨드

```bash
# 단일 리포트 채점
python engines/PE-3_auto-validation/score.py \
  --rubric prompts/scoring/PE-MACRO-Score_v1.0.md \
  --input output/SIB-latest.md \
  --notion-node C-35 \
  --auto-improve  # 80점 미만 시 PE-1 자동 호출

# 과거 리포트 배치 채점
python engines/PE-3_auto-validation/batch_score.py \
  --rubric prompts/scoring/PE-MACRO-Score_v1.0.md \
  --input-dir reports/ \
  --pattern "SIB-*.md" \
  --output-csv output/score_history.csv

# 점수 히스토리 Notion 동기화
python scripts/sync_scores_to_notion.py \
  --csv output/score_history.csv \
  --notion-db C-35
```

---

## § 6. 관련 파일 인덱스

```
GitHub: GilbertKwak/prompt-engineering-system
├── prompts/scoring/PE-MACRO-Score_v1.0.md    ← 이 파일
├── prompts/master/MASTER_PROMPT_v2.0.md
├── prompts/sub/PE-MACRO_AI_Semi_Strategy_v2.0.md
├── engines/PE-3_auto-validation/
│   ├── score.py
│   ├── batch_score.py
│   └── validate.py
└── output/score_history.csv

Notion:
T-09 > C-03 (PE-3 자동검증) — 루브릭 링크
T-09 > C-35 (AI/반도체 거시전략) — 채점 이력
```
