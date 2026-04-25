# 변형 v2.5 — M&A 타깃 특화 분석

> **Base:** Master Prompt v2.0 + 변형 C 확장 | **Version:** v2.5 | **Created:** 2026-04-25
> **생성 근거:** eSilicon→Inphi→Marvell 등 M&A 패턴 학습 기반

---

## [M&A TARGET FILTER]

```yaml
ma_target_signal:
  HIGH_signal_criteria:
    quantitative:
      - "EV/Revenue < 3x (저평가 신호)"
      - "최근 12개월 주가 -20% 이상 (상장사)"
      - "Revenue $50M~$500M 구간 (바이아웃 최적 규모)"
    qualitative:
      - "전략적 기술 보유 (독점적 IP, 희소 인력풀)"
      - "특정 고객사 집중도 > 50% (전략적 인수자 동기)"
      - "창업자 2세대 이후 경영 → Exit 가능성"
      - "PE/전략적 투자자 Board Seat 보유"
      - "최근 2년 내 M&A 루머 Bloomberg/Reuters 보도"

historical_ma_patterns:
  pattern_1:
    name: "EDA/IP → 반도체 대기업 흡수"
    examples:
      - acquirer: "Synopsys"
        target: "Ansys"
        year: 2024
        value: "$35B"
      - acquirer: "Cadence"
        target: "OpenEye Scientific"
        year: 2022
  pattern_2:
    name: "설계 서비스 → 팹리스 대기업 흡수"
    examples:
      - acquirer: "Marvell"
        target: "Inphi (eSilicon 흡수 후)"
        year: 2021
        value: "$10B"
      - acquirer: "Broadcom"
        target: "eASIC"
        year: 2018
  pattern_3:
    name: "IT서비스 → 반도체 설계 서비스 인수"
    examples:
      - acquirer: "Wipro"
        target: "Capco"
      - acquirer: "HCL"
        target: "Sankalp Semiconductor"

potential_acquirers:
  strategic:
    - "Marvell (설계 서비스 역량 강화 패턴)"
    - "Broadcom (특정 기술 IP 확보 패턴)"
    - "MediaTek (ASIC 서비스 내재화)"
    - "Qualcomm (Edge AI 설계 역량)"
    - "Samsung (TSMC 파트너 대안 확보)"
  financial:
    - "KKR"
    - "Silver Lake"
    - "Thoma Bravo"
    - "Francisco Partners"
```

## [산출물]
- D-4_MA: M&A 타깃 Top 15 상세 분석
- D-4_MA_Matrix: 타깃 × 잠재인수자 매핑 매트릭스
