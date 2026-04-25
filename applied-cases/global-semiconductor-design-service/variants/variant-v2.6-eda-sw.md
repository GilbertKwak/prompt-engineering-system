# 변형 v2.6 — EDA·SW 도구 전문 탐색

> **Base:** Master Prompt v2.0 (TypeD 독립 실행) | **Version:** v2.6 | **Created:** 2026-04-25
> **생성 근거:** Master Prompt SEARCH SCOPE 3번 섹션(TypeD: EDA/SW)을 독립 실행

---

## [EDA/SW DESIGN SERVICE FILTER]

```yaml
eda_sw_focus:
  target_description: "EDA 툴 또는 설계 자동화 솔루션 기반으로 설계 서비스를 겸업하는 기업"
  
  categories:
    EDA_tools:
      - "Synopsys, Cadence, Siemens EDA(Mentor)는 제외 (Big 3 — Pure EDA 대기업)"
      - "대상: 신흥 EDA, 클라우드 기반 EDA, AI-powered EDA 스타트업"
      companies:
        - name: "Flexcompute"
          country: "US"
          focus: "클라우드 기반 전자기 시뮬레이션 + 설계 서비스"
        - name: "Silvaco"
          country: "US"
          focus: "EDA + TCAD + 설계 서비스"
        - name: "Ansys (EDA 부문)"
          country: "US"
          focus: "전자기/열 시뮬레이션 기반 설계 서비스"
    
    design_collaboration_platforms:
      - name: "AllSpice"
        country: "US"
        focus: "하드웨어 설계 협업 플랫폼 (GitHub for Hardware)"
      - name: "Flux.ai"
        country: "US"
        focus: "AI 기반 PCB/회로 설계 플랫폼"
      - name: "ChipAgents"
        country: "US"
        focus: "AI 에이전트 기반 칩 설계 자동화"
    
    ai_eda_startups:
      search_queries:
        - "AI EDA startup chip design automation"
        - "LLM chip design automation"
        - "generative AI semiconductor design"
        - "cloud EDA design service"
      known_players:
        - "Copilot for EDA (다수 스타트업)"
        - "ZeroASIC"
        - "Efabless"
        - "Tiny Tapeout (교육 → 상업화)"
    
    hardware_description_language:
      search_queries:
        - "HLS high-level synthesis design service"
        - "SystemVerilog design service"
        - "Chisel RISC-V design service"

validation_note: |
  TypeD 기업은 순수 EDA 대기업(Synopsys/Cadence/Siemens)과 혼동 주의.
  '설계 서비스를 제공하는가'가 핵심 판단 기준.
  EDA 툴만 판매하고 서비스가 없는 경우 제외.
```

## [산출물]
- D-1_EDA: EDA·SW 기반 설계 서비스 기업 목록 (TypeD 전용)
- D-2_EDA: EDA/SW 기업 상세 분석 (AI EDA 스타트업 포함)
