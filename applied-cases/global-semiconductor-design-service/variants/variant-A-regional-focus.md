# 변형 A — 특정 지역 집중 탐색용 (v2.0 개선)

> **Base:** Master Prompt v2.0 | **Variant:** A | **Updated:** 2026-04-25
> **목적:** 동남아·인도·중동 지역 기업 집중 발굴 (Master Prompt v1.0의 지역 누락 보완)

---

## [변경 사항 — v1.0 대비]

| 섹션 | v1.0 문제 | v2.0 개선 |
|---|---|---|
| SEARCH SCOPE | 지역 조건 텍스트 서술식 → 파싱 오류 위험 | ISO-3166 코드 기준 명시 |
| INCLUSION CRITERIA | 지역 필터 없음 → 대만/미국 편중 | 지역 가중치 조건 추가 |
| OUTPUT FORMAT | 국가 필드 비표준 | ISO-3166 alpha-2 강제 |

---

## [REGIONAL OVERRIDE]

```yaml
regional_focus:
  mode: "FILTER_ADD"  # v1.0의 교체(REPLACE) 방식 수정 → 필터 추가 방식으로 변경
  target_regions:
    Southeast_Asia:
      countries: ["SG", "MY", "VN", "TH", "PH", "ID"]
      min_results: 5
      search_boost: HIGH
    India:
      countries: ["IN"]
      min_results: 8
      search_boost: HIGH
      focus_types: ["TypeC"]  # IT서비스 기반 설계 서비스 집중
      key_companies: ["Tata Elxsi", "HCL Technologies", "Wipro", "Sasken", "KPIT"]
    Middle_East:
      countries: ["AE", "IL"]
      min_results: 3
      search_boost: MEDIUM
  
  # Anchor Company 유지 (교체 아님)
  anchor_companies_preserved: true
```

## [추가 검색 키워드]

```yaml
regional_keywords:
  India: ["VLSI design India", "semiconductor design services Bangalore", "chip design outsourcing India"]
  SEA: ["semiconductor design Singapore", "chip design Malaysia Penang", "fabless design Vietnam"]
  Middle_East: ["semiconductor design Israel", "fabless Israel", "chip design UAE"]
```

## [변형 A 전용 산출물]

- D-1A: 동남아·인도·중동 지역 기업 목록 (표 1 필터링 버전)
- D-3A: 지역별 Gap 분석 (미발굴 국가 및 추가 탐색 권장 키워드)

---

*변형 A는 Master Prompt v2.0의 SEARCH SCOPE를 **교체하지 않고** 필터 조건만 추가합니다.*
*Master Prompt의 Anchor Company 및 Validation Rules는 그대로 유지됩니다.*
