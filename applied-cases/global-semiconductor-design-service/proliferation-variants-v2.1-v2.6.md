# 자동증식 변형 v2.1~v2.6 — 글로벌 반도체 설계 서비스 프로젝트

## 메타데이터
- **버전**: 2.0.0
- **엔진 유형**: Auto-Proliferate (3-Engine 중 3번)
- **기반**: Master Prompt v2.0 + 변형 A/B/C v2.0
- **생성일**: 2026-04-25
- **총 변형 수**: 6종 (v2.1~v2.6)

---

## 변형 v2.1 — 유럽 집중 탐색

```yaml
variant_2_1:
  name: "EU 반도체 설계 서비스 집중 탐색"
  base: "variant-A-v2.0 지역 변경"
  focus_regions:
    - code: "DE"  # Germany
      key_hubs: ["Munich", "Dresden", "Stuttgart"]
    - code: "FR"  # France  
      key_hubs: ["Grenoble", "Paris", "Sophia Antipolis"]
    - code: "GB"  # United Kingdom
      key_hubs: ["Cambridge", "Bristol", "Edinburgh"]
    - code: "NL"  # Netherlands
      key_hubs: ["Eindhoven", "Delft"]
    - code: "SE"  # Sweden
      key_hubs: ["Stockholm", "Lund"]
  rationale: "SiPearl(EU HPC) 발굴, EU Chips Act 수혜 기업 집중 탐색"
  additional_keywords:
    - "EU Chips Act beneficiary"
    - "European fabless semiconductor"
    - "IMEC spinoff"
    - "Fraunhofer semiconductor"
  expected_targets:
    - "SiPearl (FR) — EU HPC processor"
    - "Codasip (CZ) — RISC-V IP"
    - "Dolphin Design (FR) — IP licensor"
    - "Moortec Semiconductor (GB) — Process monitoring IP"
    - "Sondrel (GB) — ASIC design house"
```

---

## 변형 v2.2 — RISC-V 전문 필터

```yaml
variant_2_2:
  name: "RISC-V 아키텍처 전문 설계 서비스 탐색"
  base: "variant-B-v2.0 키워드 확장"
  additional_criteria:
    keyword_required: "RISC-V"
    ip_type: ["RISC-V core IP", "RISC-V SoC", "RISC-V toolchain"]
  target_organizations:
    - "RISC-V International 멤버 중 설계 서비스 기업"
  expected_targets:
    - "Codasip (CZ) — Commercial RISC-V IP"
    - "Andes Technology (TW) — RISC-V IP"
    - "OpenFive (US, acquired by SiFive) — RISC-V ASIC"
    - "SiFive (US) — RISC-V CPU IP + Design service"
    - "Nuclei System Technology (CN) — RISC-V IP"
    - "Imperas Software (GB) — RISC-V simulation"
    - "CHIPS Alliance members"
  special_note: "오픈소스 RISC-V 기반이더라도 상업 서비스 제공 시 포함"
```

---

## 변형 v2.3 — AI 칩 전문 탐색

```yaml
variant_2_3:
  name: "AI ASIC / NPU 전문 설계 서비스 탐색"
  base: "Master v2.0 SEARCH SCOPE AI 키워드 추가"
  additional_search_keywords:
    - "AI ASIC design service"
    - "NPU chip design"
    - "LLM accelerator design"
    - "inference chip startup"
    - "AI chip design house"
  inclusion_extension:
    ai_focus_required: true
    minimum_ai_revenue_share: 0.30  # AI 관련 매출 30% 이상
  expected_targets:
    - "Axelera AI (NL) — AI inference ASIC"
    - "Blaize (US) — Edge AI processor"
    - "Alif Semiconductor (US) — AI MCU"
    - "Untether AI (CA) — AI accelerator"
    - "Tenstorrent (CA) — AI chip + RISC-V"
    - "Hailo (IL) — Edge AI processor"
    - "Kneron (TW/US) — Edge AI SoC"
```

---

## 변형 v2.4 — 상장사 한정 심층 분석

```yaml
variant_2_4:
  name: "상장 반도체 설계 서비스 기업 심층 분석"
  base: "variant-C-v2.0 상장 조건 추가"
  filter:
    listed: true
    exchanges: ["TWSE", "NASDAQ", "NYSE", "KOSDAQ", "KOSPI", "SGX", "HKEX"]
  additional_fields:
    - name: "Market_Cap_USD"
      type: "STRING"
      example: "$2.3B"
    - name: "PE_Ratio"
      type: "FLOAT"
    - name: "Revenue_CAGR_3Y"
      type: "FLOAT"
      description: "3년 CAGR (%)"
    - name: "Major_Shareholders"
      type: "STRING"
  expected_targets:
    - "Alchip Technologies (TW, TWSE: 3661)"
    - "GUC / Global Unichip (TW, TWSE: 3443)"
    - "Faraday Technology (TW, TWSE: 3035)"
    - "Arm Holdings (US, NASDAQ: ARM)"
    - "Synopsys (US, NASDAQ: SNPS)"
    - "Cadence Design Systems (US, NASDAQ: CDNS)"
    - "CEVA Inc (US, NASDAQ: CEVA)"
```

---

## 변형 v2.5 — M&A 타깃 특화

```yaml
variant_2_5:
  name: "M&A 타깃 가능성 높은 설계 서비스 기업 탐색"
  base: "variant-C-v2.0 M&A 패턴 확장"
  ma_signal_criteria:
    revenue_range: "$50M ~ $500M"  # 적정 M&A 규모
    unique_ip_moat: true
    customer_concentration_max: 0.40
    strategic_fit_acquirers:
      - "Marvell Technology"
      - "Broadcom"
      - "Qualcomm"
      - "MediaTek"
      - "Samsung LSI"
      - "Intel Foundry Services"
  historical_pattern_reference:
    - "eSilicon → Inphi → Marvell (2019→2021)"
    - "Cavium → Marvell (2018)"
    - "Globalfoundries acquires OnRamp (2021)"
  scoring:
    ma_score_threshold: 15  # 20점 만점
    fields:
      - "IP uniqueness: 1-5"
      - "Revenue stability: 1-5"
      - "Strategic fit: 1-5"
      - "Integration ease: 1-5"
```

---

## 변형 v2.6 — EDA/SW 플랫폼 전문

```yaml
variant_2_6:
  name: "EDA 소프트웨어 및 설계 플랫폼 전문 탐색"
  base: "Master v2.0 SEARCH SCOPE Section 3 독립 실행"
  type_focus: ["C", "D"]  # Type C와 D 전용
  additional_search_keywords:
    - "EDA software startup"
    - "chip design SaaS"
    - "semiconductor cloud platform"
    - "PCB design collaboration tool"
    - "hardware version control"
    - "silicon photonics EDA"
    - "AI-driven EDA"
  expected_targets:
    - "Flexcompute (US) — Cloud EDA/CFD SaaS"
    - "AllSpice (US) — Hardware design collaboration"
    - "ChipAgents (US) — AI chip design assistant"
    - "Silvaco (US) — TCAD + EDA"
    - "Ansys (US) — Simulation + semiconductor"
    - "Zuken (JP) — PCB/EDA"
    - "Celus (DE) — AI electronics design"
    - "Flux (US) — AI PCB design"
  special_criteria:
    saas_model_preferred: true
    ai_integration_bonus: true
    open_source_core_accepted: true
```
