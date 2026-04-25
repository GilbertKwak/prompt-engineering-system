# 자동개선 엔진 설계 — 글로벌 반도체 설계 서비스 프로젝트

## 메타데이터
- **버전**: 2.0.0
- **엔진 유형**: Auto-Improve (3-Engine 중 1번)
- **적용 대상**: Master Prompt v1.0 → v2.0 변환
- **생성일**: 2026-04-25

---

## 진단: Master Prompt v1.0 취약점 분석

### 구조적 문제 5개

| ID | 문제 섹션 | 문제 내용 | 영향 | 심각도 |
|---|---|---|---|---|
| P-01 | SEARCH SCOPE | 지역 조건이 텍스트 서술식 → 파싱 오류 위험 | 인도/UAE 기업 누락 | HIGH |
| P-02 | INCLUSION CRITERIA | AND/OR 논리 구조 불명확 | IDM 혼입 가능성 (Semifive 계열) | CRITICAL |
| P-03 | OUTPUT FORMAT | Founded 필드 형식 미강제 | D-1 날짜 불일치 | MEDIUM |
| P-04 | VALIDATION RULES | Rule 3 VC 기준 수치 없음 | Tier 1 VC 판별 불가 | HIGH |
| P-05 | FINAL DELIVERABLE | D-3/D-4 생성 조건 미명시 | Gap 분석 반복 시 기준 흔들림 | HIGH |

---

## 개선 로직 (Diff: v1.0 → v2.0)

### P-01 수정

```diff
- SEARCH SCOPE: 전 세계 주요 반도체 클러스터 (대만, 미국, 중국, 한국, 인도, 이스라엘...)
+ search_scope:
+   geographic_coverage:
+     tier_1_must_include:
+       - code: "TW"  # Taiwan
+       - code: "US"  # United States  
+       - code: "CN"  # China
+       - code: "KR"  # South Korea
+     tier_2_include:
+       - code: "IN"  # India (명시적 포함)
+       - code: "AE"  # UAE (명시적 포함)
```

### P-02 수정

```diff
- 포함 기준:
-   - 반도체 설계 서비스 제공
-   - IDM 제외
-   - 어느 정도의 매출 또는 VC 투자
+ inclusion_criteria:
+   logic: |
+     INCLUDE IF:
+       (
+         type_match = TRUE
+         AND fab_status != "IDM"
+         AND (
+           revenue >= 1_000_000
+           OR vc_tier_1 = TRUE
+           OR listed = TRUE
+         )
+         AND activity_last_3y = TRUE
+       )
```

### P-03 수정

```diff
- Founded: 설립연도
+ - name: "Founded"
+   type: "INTEGER(YYYY)"
+   format: "4자리 연도만, 예: 1999"
```

### P-04 수정

```diff
- Tier 1 VC 투자 여부 확인
+ vc_tier_1_list:
+   - "Sequoia Capital"
+   - "Andreessen Horowitz (a16z)"
+   - "Bessemer Venture Partners"
+   - "Intel Capital"
+   - "Qualcomm Ventures"
+   [... 12개 명시]
```

### P-05 수정

```diff
- D-3, D-4 생성 (선택)
+ deliverable_3:
+   scoring_criteria: ["기술 차별성", "시장 성장성", "수익 안정성", "전략 시너지"]
+   confidence_field: "ENUM(HIGH,MEDIUM,LOW)"
+   note: "비공개 데이터 사용 시 confidence=LOW 필수 표기"
```

---

## 자동개선 실행 프로토콜

```yaml
auto_improve_protocol:
  trigger_conditions:
    - "PE-3 validation_failure >= 1 CRITICAL"
    - "PE-3 validation_failure >= 3 HIGH"
    - "Output quality score < 70/100"
  improvement_steps:
    step_1: "오류 분류 (CRITICAL/HIGH/MEDIUM/LOW)"
    step_2: "CRITICAL 오류 즉시 수정 (blocking)"
    step_3: "HIGH 오류 수정 후 재검증"
    step_4: "MEDIUM/LOW 오류 차기 버전에 반영"
    step_5: "버전 번호 업 (PATCH: x.x.1, MINOR: x.1.0, MAJOR: 1.0.0→2.0.0)"
  version_policy:
    PATCH: "오류 수정만"
    MINOR: "필드/규칙 추가"
    MAJOR: "구조 전면 개편 (v1→v2)"
```
