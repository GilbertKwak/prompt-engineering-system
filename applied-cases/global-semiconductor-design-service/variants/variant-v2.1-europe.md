# 변형 v2.1 — 유럽 집중 탐색

> **Base:** Master Prompt v2.0 + 변형 A | **Version:** v2.1 | **Created:** 2026-04-25
> **생성 근거:** D-1 데이터에서 SiPearl(EU HPC SoC 설계) 발굴 → EU 클러스터 존재 확인

---

## [REGIONAL OVERRIDE]

```yaml
region: EU
target_countries: ["DE", "FR", "GB", "NL", "SE", "FI", "IL", "CH", "BE", "AT"]
min_results_per_country:
  DE: 3
  FR: 3
  GB: 5
  NL: 2
  IL: 4
  SE: 2

key_eu_clusters:
  - name: "Sophia Antipolis (FR)"
    focus: "SoC, RF, Automotive chip design"
  - name: "Munich / Bavaria (DE)"
    focus: "Automotive, Industrial IoT ASIC"
  - name: "Cambridge (GB)"
    focus: "Arm 생태계, AI chip, CPU IP"
  - name: "Israel Tech Corridor"
    focus: "AI chip, Cyber security ASIC, Networking"
    known_companies: ["Mobileye", "Hailo", "Mellanox(NVIDIA)", "Annapurna Labs(Amazon)"]

specific_search_queries:
  - "semiconductor design service Germany"
  - "ASIC design house UK Cambridge"
  - "fabless chip design France"
  - "SoC design service Netherlands"
  - "chip design startup Israel Tel Aviv"
  - "European semiconductor IP company"
```

## [산출물]
- D-1_EU: 유럽 반도체 설계 서비스 기업 목록
- D-3_EU: 유럽 지역 Gap 분석
