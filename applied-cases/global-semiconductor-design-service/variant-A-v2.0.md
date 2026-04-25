# 변형 A v2.0 — 특정 지역 집중 탐색형 (동남아·인도·중동)

## 메타데이터
- **버전**: 2.0.0
- **기반**: Master Prompt v2.0 SEARCH SCOPE 필터 변형
- **목적**: 동남아시아, 인도, 중동 지역 반도체 설계 서비스 기업 집중 발굴
- **생성일**: 2026-04-25
- **변경 내역 (v1→v2)**: "교체" 방식에서 "필터 추가" 방식으로 수정 (Anchor Company 충돌 방지)

---

## ⚠️ v1.0 대비 핵심 변경사항

| 항목 | v1.0 문제 | v2.0 수정 |
|---|---|---|
| SEARCH SCOPE | 전체 교체 → Anchor Company 지역 상충 | 필터 레이어 추가 방식으로 전환 |
| 지역 코드 | 텍스트 서술 | ISO-3166 코드 명시 |
| 결과 통합 | 미정의 | Master D-1에 Region 태그 추가 후 병합 |

---

## SCOPE OVERRIDE (Master v2.0에 추가 적용)

```yaml
scope_filter:
  mode: "ADDITIVE"  # 교체 아님, 필터 추가
  focus_regions:
    - code: "IN"  # India
      priority: "PRIMARY"
      search_keywords:
        - "India ASIC design house"
        - "India fabless semiconductor startup"
        - "India chip design center"
        - "VLSI design service India"
      key_hubs: ["Bangalore", "Hyderabad", "Pune", "Chennai", "Noida"]
    - code: "SG"  # Singapore
      priority: "PRIMARY"
      search_keywords:
        - "Singapore semiconductor design"
        - "IMDA semiconductor company Singapore"
    - code: "MY"  # Malaysia
      priority: "SECONDARY"
      key_hubs: ["Penang", "Kuala Lumpur"]
    - code: "VN"  # Vietnam
      priority: "SECONDARY"
      key_hubs: ["Ho Chi Minh City", "Hanoi"]
    - code: "AE"  # UAE
      priority: "SECONDARY"
      key_hubs: ["Dubai Silicon Oasis", "Abu Dhabi"]
    - code: "IL"  # Israel
      priority: "PRIMARY"
      key_hubs: ["Tel Aviv", "Haifa", "Beer Sheva"]
      search_keywords:
        - "Israel fabless semiconductor"
        - "Israel ASIC design"
        - "Israel chip startup"
```

## 추가 포함 기준

```yaml
additional_criteria:
  - indian_origin_founders_accepted: true   # 창업자 인도계 해외법인 포함
  - government_backed_accepted: true        # IESA/SIA-India 정부 지원 기업 포함
  - minimum_team_size: 10                   # 팀 10인 이상
  - vc_regional_accepted:                   # 지역 VC도 포함 (Tier 1 불가 시)
      - "Nexus Venture Partners"
      - "Blume Ventures"
      - "Chiratae Ventures"
      - "Info Edge Ventures"
```

## 예상 발굴 기업 카테고리

- **인도**: Signoff Semiconductors, Tessolve, eInfochips (Arrow), HCL Semiconductors, Wipro VLSI
- **이스라엘**: Marvell Israel R&D, Tower Semiconductor Design, Kneron Israel
- **싱가포어**: MediaTek Singapore Design Center, Broadcom Singapore
- **중동**: G42 Semiconductor (UAE), Bayanat AI chip initiative

## 결과 통합 방법

1. 발굴 기업 → Master D-1 테이블에 `region_focus: "A-variant"` 태그 추가 병합
2. Type 분류는 Master v2.0 기준 동일 적용
3. D-3 투자 매력도 — 지역 특수 리스크 항목 추가: `regulatory_risk`, `talent_availability`
