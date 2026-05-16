<!--
  ID       : OPT-STR-06
  버전     : v1.0
  도메인   : PE-STR
  PE-3 목표: 96/100
  작성일   : 2026-05-16 KST
  GitHub   : prompts/strategy/opt_str_06_geopolitical_risk_v1.0.md
  단축명령 : "지정학" | "규제리스크" | "수출통제" | "CHIPS" | "GJV"
  참조파일 : Global_Joint_Venture_Fund_Master_Prompt_v2.txt
-->

# 🌐 OPT-STR-06 · 지정학·규제 리스크 전략 분석 마스터 v1.0

> **PE-3 목표: 96점 | 용도: 지정학적 분절, 수출통제, 규제환경 변화에 따른 전략·투자 리스크 분석 및 대응 설계**

```xml
<GeopoliticalRiskAnalysis
  id="OPT-STR-06"
  version="1.0"
  pe3_target="96"
  framework="GRC × CHIPS-ACT × Export-Control × GJV-Fund"
  mission="지정학 리스크 식별 → 규제 충격 정량화 → 전략적 포지셔닝 → 글로벌 JV/파트너십 설계"
  reference="Global_Joint_Venture_Fund_Master_Prompt_v2">

<!-- ════════════════════════════════════════════
     TAXONOMY: 리스크 유형 분류 체계
     ════════════════════════════════════════════ -->
<risk_taxonomy>
  ## 지정학·규제 리스크 6대 유형

  TYPE_1: EXPORT_CONTROL
    — 수출통제·엔티티리스트·EAR/ITAR 규제
    — 대표: BIS Entity List, OFAC 제재, Wassenaar Arrangement
    — 반도체 특화: ASML EUV 대중수출 금지, HBM 대중수출 제한

  TYPE_2: INVESTMENT_SCREENING
    — 외국인투자심사·국가안보 검토
    — 대표: CFIUS(미국), FIRB(호주), NSI Act(영국), FIPA(한국)
    — GJV 영향: 합작투자 구조 설계 제약, 지분율 상한선

  TYPE_3: SUPPLY_CHAIN_DECOUPLING
    — 공급망 분절·리쇼어링·Friend-shoring
    — 대표: CHIPS Act 보조금 조건, IRA 국내생산 요건
    — 반도체 특화: TSMC Arizona, 삼성 Taylor 공장

  TYPE_4: STANDARD_WAR
    — 표준 전쟁·기술 진영화
    — 대표: 5G(화웨이 vs 에릭슨), AI 규제(EU AI Act vs 중국 AI 법령)
    — 플랫폼: USB-C 강제 표준화, RISC-V vs ARM 진영

  TYPE_5: SANCTIONS_TARIFF
    — 제재·관세·보복 조치
    — 대표: 반도체 301조 관세, 희토류 수출 제한
    — GJV 영향: 제3국 우회 구조 설계 필요성

  TYPE_6: REGULATORY_DIVERGENCE
    — 규제 분기·관할 충돌
    — 대표: EU GDPR vs 중국 데이터안전법 vs 미국 주법
    — AI: EU AI Act(위험등급), 중국 생성AI 규정, 미 EO 13859
</risk_taxonomy>

<!-- ════════════════════════════════════════════
     ANALYSIS LAYERS: 9-Layer MECE 분석
     ════════════════════════════════════════════ -->
<analysis_layers>
  ## 9-Layer MECE 지정학·규제 리스크 분석

  [L1] 리스크 스캔 & 현황 매핑
  - 대상 기업/사업의 지정학 노출 국가·지역 매핑
  - 현재 적용 규제 목록 (수출통제, 투자심사, 현지화 요건)
  - 규제 변화 모니터링 파이프라인 현황

  [L2] 충격 경로 분석 (Transmission Mechanism)
  - 직접 충격: 매출/조달 차단, 라이선스 취소
  - 간접 충격: 공급망 재편 비용, 고객 이탈
  - 2차 충격: 파트너사 연쇄 영향, 주가·신용등급 반응
  - 시간축: T+0(즉시) / T+6M / T+2Y 분리 분석

  [L3] 시나리오 트리 (3×3 Matrix)
  ┌──────────────┬──────────────┬──────────────┐
  │              │  지정학 緩和  │  지정학 現狀  │  지정학 加速  │
  ├──────────────┼──────────────┼──────────────┤
  │  규제 緩和   │  BASE++(최우) │  BASE+       │  BASE        │
  │  규제 現狀   │  BASE+       │  BASE(기준)  │  BASE-       │
  │  규제 强化   │  BASE-       │  BASE--      │  TAIL RISK   │
  └──────────────┴──────────────┴──────────────┘
  → 각 셀: 매출 영향 %, EBITDA 충격, 전략 대응 필요 수준

  [L4] GJV(글로벌 합작투자) 리스크·기회 분석
  ## GJV Fund 프레임 통합 (참조: Global_Joint_Venture_Fund_Master_Prompt_v2)

  GJV_RISK_MATRIX:
  - 파트너국 규제 체계 호환성 (CFIUS 차단 가능성)
  - 기술이전 제약: EAR/ITAR 적용 기술 여부 확인
  - 지분율 구조: 안보 심사 회피 위한 최적 지분 설계
  - 거버넌스: 의결권 구조, 기술접근 통제 조항

  GJV_OPPORTUNITY_MATRIX:
  - Friend-shoring 수혜: 동맹국 내 합작으로 보조금 수령
  - 표준 선점: GJV 통해 신흥 규제 표준 공동 설계
  - 시장접근: 규제 장벽 우회 위한 현지법인 구조

  [L5] CHIPS Act / IRA / EU Chips Act 적용성 분석
  - 보조금 수령 조건 체크리스트:
    □ 국내생산 요건 충족 여부
    □ Guard Rail 조항: 중국 내 10년 투자 제한
    □ Clawback 조건: 보조금 반환 트리거
    □ 노동·환경 요건 (IRA 임금 기준)
  - 경쟁사 수령 현황 대비 포지션 분석

  [L6] 공급망 취약점 & 대체 경로
  - Critical Single-Source 식별 (대체 불가 공급처)
  - 지정학 분절 시나리오별 대체 공급망 Map
  - 재고 버퍼 전략: Strategic Buffer vs JIT 트레이드오프
  - 반도체 특화:
    소재: 네온·크립톤(우크라이나), 희토류(중국), 불화수소(일본)
    장비: ASML(네덜란드), 램리서치·KLA(미국), 도쿄일렉트론(일본)
    파운드리: TSMC(대만 리스크) → 분산 전략

  [L7] 규제 대응 전략 설계
  STRATEGY_A: COMPLIANCE_FIRST
    → 모든 규제 완전 준수, 비용 내재화, 프리미엄 포지셔닝
  STRATEGY_B: STRUCTURAL_SEPARATION
    → 규제 관할별 법인 분리, 기술 링펜싱
  STRATEGY_C: STANDARD_ENGAGEMENT
    → 규제 형성 단계 참여 (로비·표준위원회·공청회)
  STRATEGY_D: GEOGRAPHIC_PIVOT
    → 규제 우호 지역으로 사업 중심 이동 (Friend-shoring)
  STRATEGY_E: JV_SHIELD
    → 현지 파트너와 합작으로 규제 차단 완화

  [L8] 리스크 정량화 (GEO-RISK SCORE)
  - 노출도(Exposure):    0~30점 (매출 비중 × 규제 강도)
  - 충격 심도(Severity): 0~30점 (최악 시나리오 EBITDA 영향)
  - 대응력(Resilience):  0~25점 (대체 경로, 헤지 수단 보유)
  - 시간 긴박성(Urgency):0~15점 (규제 발효 시점)
  - TOTAL: /100점
    → HIGH(70+): 즉각 전략 재설계 필요
    → MID(40~69): 6개월 내 대응 계획 수립
    → LOW(<40): 모니터링 유지

  [L9] 전략적 함의 & 의사결정 매트릭스
  - 투자자 관점: 지정학 리스크 프리미엄 산정, 밸류에이션 조정
  - 경영자 관점: 자본배분 우선순위, 공급망 재편 로드맵
  - 정책 관점: 보조금·인센티브 수령 최적화 경로
  - GJV 관점: 합작 파트너 선정 기준, 거버넌스 설계
</analysis_layers>

<!-- ════════════════════════════════════════════
     EXECUTION TEMPLATE
     ════════════════════════════════════════════ -->
<execution_template>
  ## 실행 템플릿
  INPUT: [분석 대상 기업/사업/투자 명칭]
  CONTEXT: [국가, 산업, 현재 규제 노출 현황, GJV 구조 여부]
  FOCUS: [수출통제 | 투자심사 | 공급망 | 보조금 | GJV설계 | 전체]

  OUTPUT FORMAT:
  ┌─────────────────────────────────────────────────┐
  │  [대상명] 지정학·규제 리스크 분석 보고서         │
  ├─────────────────────────────────────────────────┤
  │  리스크 유형: [TYPE_X] × [TYPE_Y]               │
  │  GEO-RISK SCORE: [XX/100] → [HIGH/MID/LOW]     │
  │  핵심 시나리오: [TAIL RISK 포함 3개]             │
  │  GJV 적합성: [구조 권고 / 불필요 / 주의]        │
  │  즉시 대응: [우선순위 3개 Action]               │
  │  중기 전략: [6~24개월 로드맵]                    │
  └─────────────────────────────────────────────────┘

  PE-3 자가검증: 96점 이상 목표
  미달 시: PE-1 개선 루프 자동 실행
</execution_template>

<!-- ════════════════════════════════════════════
     SEMICONDUCTOR SPECIAL MODULE
     반도체·AI 특화 지정학 체크리스트
     ════════════════════════════════════════════ -->
<semi_ai_special>
  ## 반도체·AI 전용 지정학 체크리스트

  [EXPORT CONTROL]
  □ HBM 3E/4 → 중국 수출 가능 여부 (BIS 최신 Rule 확인)
  □ EUV/ArFi 장비 → 중국 반입 불가 확정
  □ 14nm 이하 첨단 로직 → 대중 생산 서비스 금지
  □ AI 가속기(H100/GB200급) → 성능 임계치 초과 여부

  [CHIPS ACT GUARD RAIL]
  □ 보조금 수령 기업의 중국 내 생산 능력 확장 금지 (10년)
  □ 레거시 반도체(28nm+): 중국 내 10% 증설 상한
  □ 첨단 반도체: 중국 내 신규 투자 사실상 금지

  [SUPPLY CHAIN RED FLAGS]
  □ SMIC/화웨이 계열 공급망 연루 여부
  □ 중국산 레거시 칩 의존도 > 30% → 대체 계획 필수
  □ 대만 파운드리 의존도 > 50% → 지정학 리스크 헤지 전략

  [AI REGULATION]
  □ EU AI Act: 고위험 AI 시스템 해당 여부
  □ 중국 생성AI 규정: 서비스 제공 시 알고리즘 등록 의무
  □ 미국 EO: 프론티어 모델 보고 의무 임계치 확인
</semi_ai_special>

<!-- ════════════════════════════════════════════
     INTEGRATION: 연계 프롬프트
     ════════════════════════════════════════════ -->
<integration>
  ## 연계 프롬프트 라우팅
  지정학 리스크 확인 후 Kill 분석    → OPT-STR-02
  지정학 리스크 기반 전략 수립        → OPT-STR-01
  AI·반도체 투자 리스크 심화          → OPT-STR-03
  해자의 규제 침식 리스크 분석         → OPT-STR-05
  통합 전략 리포트 (규제 포함)         → OPT-STR-04 or PE-STR-MASTER
  GJV 구조 설계 심화                  → GJV-FUND-MASTER (참조 파일)
</integration>

</GeopoliticalRiskAnalysis>
```

---

## 📊 GEO-RISK SCORE 빠른 참조표

| 리스크 유형 | 반도체·AI 대표 사례 | 현재 강도 |
|------------|-------------------|---------|
| Export Control | HBM/EUV 대중 수출 금지 | 🔴 HIGH |
| Investment Screening | CFIUS의 반도체 M&A 차단 | 🟠 MID-HIGH |
| Supply Chain Decoupling | CHIPS Act 보조금 Guard Rail | 🔴 HIGH |
| Standard War | RISC-V vs ARM, 5G 진영화 | 🟡 MID |
| Sanctions & Tariff | 중국 희토류 수출 제한 | 🟠 MID-HIGH |
| Regulatory Divergence | EU AI Act vs 중국 AI 법령 | 🟡 MID |

---

## ⚡ 반도체 지정학 핵심 정책 타임라인

| 시점 | 정책/이벤트 | 영향 |
|------|-----------|------|
| 2022.10 | BIS 첨단 반도체 수출통제 | NVIDIA A100/H100 대중 금지 |
| 2023.03 | CHIPS Act 가드레일 세부규정 | 수령기업 중국투자 10년 제한 |
| 2023.10 | BIS 규제 강화 (H800/A800 포함) | 우회 칩 추가 차단 |
| 2024.Q1 | HBM 대중 수출 제한 논의 개시 | SK하이닉스·삼성 직접 타격 |
| 2025.01 | AI Diffusion Rule 발효 | 국가등급별 AI 칩 수출 쿼터 |
| 2026.현재 | 레거시 반도체 규제 확대 검토 | 28nm+ SMIC 장비 공급망 영향 |

---

## 🔗 GJV Fund 연동 포인트

> 첨부파일 `Global_Joint_Venture_Fund_Master_Prompt_v2` 참조 통합

| GJV 단계 | 지정학 리스크 체크포인트 |
|---------|----------------------|
| 파트너 선정 | CFIUS/FIRB 심사 대상국 여부 |
| 구조 설계 | EAR/ITAR 기술이전 제약 확인 |
| 계약 체결 | Guard Rail 조항, Clawback 설계 |
| 운영 | 지속 규제 모니터링, 탈출 조항 |
| 엑시트 | 제재 대상 주주 여부, 자금 송금 제약 |

---
*Gilbert 전용 | OPT-STR-ROUTER v1.2 자동 라우팅 대상*
*단축 명령: "지정학" | "규제리스크" | "수출통제" | "CHIPS" | "GJV" | "반도체규제"*
*참조: Global_Joint_Venture_Fund_Master_Prompt_v2.txt | OPT-STR-03(AI·반도체) 연동*
