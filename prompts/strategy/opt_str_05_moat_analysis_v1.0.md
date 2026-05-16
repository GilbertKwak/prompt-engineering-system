<!--
  ID       : OPT-STR-05
  버전     : v1.0
  도메인   : PE-STR
  PE-3 목표: 96/100
  작성일   : 2026-05-16 KST
  GitHub   : prompts/strategy/opt_str_05_moat_analysis_v1.0.md
  단축명령 : "해자분석" | "경쟁우위" | "진입장벽"
-->

# 🏰 OPT-STR-05 · 경제적 해자(Moat) 분석 마스터 v1.0

> **PE-3 목표: 96점 | 용도: 기업/사업의 지속 가능한 경쟁우위 구조 분석**

```xml
<MoatAnalysis
  id="OPT-STR-05"
  version="1.0"
  pe3_target="96"
  framework="Morningstar 5-Moat × Porter × Hamilton-Helmer 7Powers"
  mission="경제적 해자 식별 → 지속가능성 평가 → 투자/전략적 함의 도출">

<moat_taxonomy>
  ## 해자 유형 분류 (Morningstar 5-Moat)
  TYPE_1: NETWORK_EFFECT     — 사용자↑ → 가치↑ (플랫폼, 마켓플레이스)
  TYPE_2: SWITCHING_COST     — 전환비용 (SaaS, ERP, 반도체 IP)
  TYPE_3: COST_ADVANTAGE     — 원가 우위 (규모경제, 프로세스 혁신)
  TYPE_4: INTANGIBLE_ASSET   — 무형자산 (브랜드, 특허, 라이선스)
  TYPE_5: EFFICIENT_SCALE    — 효율적 규모 (틈새 독점, 자연독점)

  ## 7Powers (Hamilton-Helmer) 매핑
  POWER_1: Scale Economies
  POWER_2: Network Economics
  POWER_3: Counter-Positioning
  POWER_4: Switching Costs
  POWER_5: Branding
  POWER_6: Cornered Resource
  POWER_7: Process Power
</moat_taxonomy>

<analysis_layers>
  ## 9-Layer MECE 해자 분석 프레임

  [L1] 해자 현황 스캔
  - 현재 보유 해자 유형 식별 (1~5개 체크)
  - 해자 강도 측정: WIDE / NARROW / NONE
  - 경쟁사 대비 상대적 포지션

  [L2] 해자 원천 구조 분석
  - 핵심 경쟁우위 요소 분해
  - 복수 해자 보유 시 상호강화 여부
  - 해자 형성 기간 및 투자 규모 역산

  [L3] 해자 내구성 평가
  - 시간 지평: 5Y / 10Y / 20Y 시나리오
  - 기술 변화에 따른 해자 침식 위험
  - 규제 변화 리스크

  [L4] 해자 위협 요인 분석
  - Direct Attack: 동일 전략으로 정면 경쟁
  - Disruption: 비대칭 신기술·비즈니스모델
  - Substitution: 대체재 부상 경로
  - Regulatory: 독점 규제, 강제 라이선스

  [L5] 해자 확장 가능성
  - 인접 시장으로 해자 전이 가능 여부
  - 해자 강화 투자 ROI 분석
  - M&A를 통한 해자 획득 전략

  [L6] 재무적 해자 증거
  - ROIC vs WACC 스프레드 (10년 추세)
  - 영업이익률 안정성 및 가격결정력
  - FCF 전환율 및 자본 재투자 효율

  [L7] 반도체·AI 특화 해자 분석
  - IP 포트폴리오: 특허 수, 핵심특허 만료 일정
  - 생태계 잠금(Ecosystem Lock-in): SDK, API, CUDA
  - 공급망 해자: 소재·장비 접근성, TSMC/SK하이닉스 협력
  - 데이터 해자: 독점 데이터셋, 학습 루프

  [L8] 해자 점수화 (MOAT-SCORE)
  - 강도(Width):    0~40점
  - 내구성(Depth):  0~30점
  - 확장성(Reach):  0~20점
  - 재무증거:       0~10점
  - TOTAL:          /100점 → Wide(70+) / Narrow(40~69) / None(<40)

  [L9] 전략적 함의 도출
  - 투자자 관점: 매수/보유/매도 판단 근거
  - 경영자 관점: 해자 강화 우선순위 과제
  - 경쟁자 관점: 해자 공략 가능 진입점
</analysis_layers>

<execution_template>
  ## 실행 템플릿
  INPUT: [분석 대상 기업/사업 명칭]
  CONTEXT: [산업, 경쟁 구도, 현재 상황]

  OUTPUT FORMAT:
  ┌─────────────────────────────────────────┐
  │  [기업명] 해자 분석 보고서              │
  ├─────────────────────────────────────────┤
  │  해자 유형: [TYPE_X] × [TYPE_Y]         │
  │  MOAT-SCORE: [XX/100] → [WIDE/NARROW]  │
  │  내구성 전망: [5Y/10Y 평가]             │
  │  핵심 위협: [상위 3개]                  │
  │  전략적 함의: [투자/경영/경쟁 관점]     │
  └─────────────────────────────────────────┘

  PE-3 자가검증: 96점 이상 목표
  미달 시: PE-1 개선 루프 자동 실행
</execution_template>

<integration>
  ## 연계 프롬프트
  해자 확인 후 Kill Analysis  → OPT-STR-02
  해자 기반 전략 수립          → OPT-STR-01
  AI·반도체 해자 심화          → OPT-STR-03
  통합 전략 리포트             → OPT-STR-04 or PE-STR-MASTER
</integration>

</MoatAnalysis>
```

---

## 📊 MOAT-SCORE 빠른 참조

| 해자 유형 | 대표 기업 | 반도체/AI 사례 |
|----------|----------|---------------|
| Network Effect | Meta, Uber | CUDA 생태계, TSMC 고객망 |
| Switching Cost | SAP, Salesforce | SK하이닉스 HBM 인증비용 |
| Cost Advantage | Amazon, Walmart | 삼성 메모리 규모경제 |
| Intangible Asset | LVMH, Qualcomm | ARM 특허, ASML EUV 라이선스 |
| Efficient Scale | ASML, Moody's | CoWoS TSMC 독점 |

---
*Gilbert 전용 | OPT-STR-ROUTER 자동 라우팅 대상*
*단축 명령: "해자분석" | "경쟁우위" | "진입장벽" | "MOAT"*
