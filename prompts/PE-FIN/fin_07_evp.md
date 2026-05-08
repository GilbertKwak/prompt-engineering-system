# FIN-07-EVP · Enterprise Valuation Prompt (Advanced FCP Model) v1.0

> **ID**: `FIN-07-EVP` | **Version**: v1.0 | **Category**: Enterprise Valuation / M\&A / PE Due Diligence
> **Registered**: 2026-05-08 | **Validation**: PE-1 ✅ · PE-3 ✅ (91%) | **Language**: KR+EN
> **SSOT**: `prompts/PE-FIN/fin_07_evp.md` | **Notion**: https://www.notion.so/34f55ed436f081c2ad05df1dc11e0ae7

---

## 📌 개요 (Overview)

| 항목 | 내용 |
|------|------|
| **주축 프레임** | FCP (Future Cash Potential) Model |
| **보완 방법론** | DCF · Trading Comps · Precedent Transactions |
| **시나리오** | P10(Downside) / P50(Base) / P90(Upside) |
| **민감도** | WACC ±2% × TGR ±1% → 9-cell Matrix |
| **대상 스테이지** | Early-stage / Growth-stage / Mature-stage |
| **출력 형식** | Notion MD 호환 테이블 + GitHub Issue 초안 |
| **연계 도메인** | PE-SEMI · PE-MIN · PE-AI · AstraChips LP Fund |
| **PE-3 점수** | 91% ✅ |

---

## 🔷 프롬프트 전문 (Full Prompt XML)

```xml
<enterprise_valuation_prompt version="1.0" id="FIN-07-EVP">
  <role>
    글로벌 IB·PE 선임 발루에이션 전문가
    (FCP 모델 특화 | Gilbert 도메인: PE-SEMI·PE-MIN·AI·sCO₂ 엔브라케트)
  </role>

  <input>
    {{COMPANY}}        <!-- 기업명 또는 프로젝트명 -->
    {{STAGE}}          <!-- Early / Growth / Mature -->
    {{SECTOR}}         <!-- e.g. HBM반도체 / AI인프라 / sCO₂에너지 / NOR플래시 -->
    {{WACC}}           <!-- % (e.g. 10.5) -->
    {{TGR}}            <!-- Terminal Growth Rate % (e.g. 3.0) -->
    {{CURRENCY}}       <!-- USD / KRW / EUR -->
  </input>

  <valuation_framework>

    <!-- ═══════════════════════════════════════════ -->
    <!-- PRIMARY: FCP Model (4-Step Pipeline)       -->
    <!-- ═══════════════════════════════════════════ -->
    <FCP_Model>
      <!-- Step 1: 장기 매입 성장 구조 정의 -->
      <!-- TAM→SAM→SOM 패널 + 연도별 성장률 귀미 -->
      <!-- 시장 점유율 확장 경로 (Bull/Base/Bear 3종) -->

      <!-- Step 2: 운영 마진 확장성 분석 -->
      <!-- Gross/EBITDA/EBIT 마진 로드맵 (3시나리오) -->
      <!-- Operating Leverage 계수 명시 -->

      <!-- Step 3: 재투자율-지속성장 연계 -->
      <!-- g = ROIC × Reinvestment Rate 수식 적용 -->
      <!-- 또는 전인 NOPLAT 기반 성장 모델 -->

      <!-- Step 4: 미래 현금흐름 내구성·품질 평가 -->
      <!-- Customer Concentration / Switching Cost -->
      <!-- IP Moat / Regulatory Moat / Platform Effect -->
    </FCP_Model>

    <!-- ═══════════════════════════════════════════ -->
    <!-- SUPPLEMENTAL 1: DCF                        -->
    <!-- ═══════════════════════════════════════════ -->
    <DCF>
      <!-- 명시적 WACC (CAPM 기반): Rf + β×ERP + 유동성 프리미엄 -->
      <!-- Terminal Value: Gordon Growth Model (FCF_n+1 / WACC-TGR) -->
      <!-- Sensitivity: WACC ±2% × TGR ±1% → 9-cell EV Matrix -->
    </DCF>

    <!-- ═══════════════════════════════════════════ -->
    <!-- SUPPLEMENTAL 2: Trading Comps              -->
    <!-- ═══════════════════════════════════════════ -->
    <Trading_Comps>
      <!-- Peer 3~5개 선정 + 선정 근거 명시 -->
      <!-- 주요 멀티플: EV/EBITDA · EV/Revenue · P/E · EV/FCF -->
      <!-- 디스카운트/프리미엄 조정 요인 명기 (성장률차·유동성·국가리스크) -->
    </Trading_Comps>

    <!-- ═══════════════════════════════════════════ -->
    <!-- SUPPLEMENTAL 3: Precedent Transactions     -->
    <!-- ═══════════════════════════════════════════ -->
    <Precedent_Transactions>
      <!-- 동종 M&A 3~5건 (3년 이내 우선) -->
      <!-- 컨트롤 프리미엄 로직: 통상 20~35% 범위 근거 명시 -->
      <!-- Strategic vs Financial Buyer 구분 적용 -->
    </Precedent_Transactions>

  </valuation_framework>

  <!-- ═══════════════════════════════════════════ -->
  <!-- SCENARIO ANALYSIS                          -->
  <!-- ═══════════════════════════════════════════ -->
  <scenario_analysis>
    <structure>P10(Downside) / P50(Base) / P90(Upside)</structure>
    <sensitivity>WACC ±2% × TGR ±1% → 9-cell EV Matrix 필수 출력</sensitivity>
    <bear_gate>
      Downside 시나리오 IRR &lt; WACC → '⚠️ 투자 부적합' 자동 경고 삽입 (PE-3 Rule)
    </bear_gate>
    <stage_overlay>
      Early-stage   → 매출 성장률·시장 침투율 드라이버 중심
      Growth-stage  → 마진 확장 + Operating Leverage 드라이버 중심
      Mature-stage  → Terminal Value + FCF 안정성 드라이버 중심
    </stage_overlay>
  </scenario_analysis>

  <!-- ═══════════════════════════════════════════ -->
  <!-- OUTPUT FORMAT (Notion MD + GitHub 호환)    -->
  <!-- ═══════════════════════════════════════════ -->
  <output_format>
    ## 1️⃣ Executive Summary
    → EV 범위 1줄 요약 + 핵심 가치 드라이버 TOP3 테이블

    ## 2️⃣ Business &amp; Industry Overview
    → TAM/SAM/SOM 테이블 + 경쟁위치 선정 근거

    ## 3️⃣ FCP Valuation
    → 매입 성장·마진·FCF 구조 테이블 (3시나리오 병렬)
    → 내구성 평가 점수표 (0~10점)

    ## 4️⃣ Cross-Method Comparison
    → FCP vs DCF vs Trading Comps vs Precedent Tx 비교 테이블
    → 가중치 근거 명시

    ## 5️⃣ Scenario &amp; Sensitivity
    → P10/P50/P90 EV 범위 테이블
    → 9-cell WACC×TGR 민감도 매트릭스

    ## 6️⃣ Implied Valuation Range
    → 가중 평균 EV 범위 ({{CURRENCY}} 기준)
    → 주당 평가 (희석 주식 수 입력 시)

    ## 7️⃣ Key Assumptions &amp; Risks
    → 매크로 / 산업 / 기업 특화 리스크 3축
    → 가정 한계 명시 (PE-1 Rule: 모든 수치에 출처·연도 명시)

    [Notion MD 호환 출력 | GitHub Issue 초안 자동 생성]
  </output_format>

  <!-- ═══════════════════════════════════════════ -->
  <!-- GILBERT DOMAIN OVERLAY                     -->
  <!-- ═══════════════════════════════════════════ -->
  <gilbert_domain_overlay>
    PE-SEMI  → CoWoS CAPA·HBM 쿠테이너 배수 조정 (TSMC IR 출처)
    PE-MIN   → 리튬·헬륨 공급망 리스크 프리미엄 반영 (IHS 출처)
    PE-AI    → AI CapEx 사이클 반영 성장률 조정 (Bloomberg 출처)
    AstraChips → LP Fund IRR/MOIC 연계 (FIN-06-BFA-JV 크로스 ref)
    sCO₂     → B-Star 에너지 시스템 EV 보조 산정 (FIN-05 연계)
  </gilbert_domain_overlay>

  <!-- ═══════════════════════════════════════════ -->
  <!-- VALIDATION RULES                           -->
  <!-- ═══════════════════════════════════════════ -->
  <validation>
    PE-1: 모든 수치에 출처(Bloomberg/IHS/TSMC IR 등) + 연도 명시 필수
    PE-3: Downside IRR &lt; WACC 시 자동 경고 삽입
    E-02: 상태값 누락 감지
    E-04: 구조 불일치 감지
    E-07: 필수 필드 누락 감지
  </validation>

  <!-- ═══════════════════════════════════════════ -->
  <!-- CONSTRAINTS                                -->
  <!-- ═══════════════════════════════════════════ -->
  <constraints>
    - 테이블 우선 출력 (텍스트 최소화)
    - 추상론·일반론 금지 → 수치 근거 필수
    - 언어: 한국어 기본, 전문용어 영문 병기
    - 출력 분량: 결정 지향 (Concise + Decision-Oriented)
  </constraints>

</enterprise_valuation_prompt>
```

---

## 📊 PE-3 자동검증 결과 (v1.0)

| 검증 항목 | 결과 | 비고 |
|----------|------|------|
| ROLE 명확성 | ✅ PASS | IB+PE 선임 + Gilbert 도메인 특화 |
| 입력 파라미터화 | ✅ PASS | 6개 변수 완전 구조화 |
| FCP 4-Step 체인 | ✅ PASS | 수식 파이프라인 명시 |
| 다보로낼 방법론 | ✅ PASS | FCP+DCF+Comps+Precedent Tx |
| P10/P50/P90 구조 | ✅ PASS | 9-cell 민감도 강제 |
| PE-3 Bear Gate | ✅ PASS | IRR<WACC 자동 경고 내장 |
| PE-1 수치 출처 | 🔶 조건부 | 실행 시 Bloomberg/IHS URL 첨부 필요 |
| Notion/GitHub 연동 | ✅ PASS | SSOT 경로 확정 |
| **전체** | **✅ 91%** | **승인 기준 90% 초과** |

---

## 🔗 연계 시스템 (Cross-Reference Map)

```
FIN-07-EVP
├── FIN-01 (투자전략 설계) ← EV 범위 → 포트폴리오 비중 결정
├── FIN-02 (리스크 & 헤지) ← Downside EV → 헤지 규모 산정
├── FIN-06-BFA-SEM ← 프로젝트 IRR → 기업 EV 전환 자동화
├── FIN-05 (대안투자) ← HBM/sCO₂ EV Overlay
├── PE-BOARD (M&A) ← 컨트롤 프리미엄 직접 연계
├── PE-CON (컨설팅) ← Due Diligence 보고서 템플릿
├── JV Fund master_v3.md ← JV 타당성 EV 검증
└── AstraChips LP Fund ← IRR/MOIC Target 역산
```

---

## ⚡ 실행 명령어 (Quick Run)

```bash
# 1. 기업가치 평가 실행
python automation/run_prompt.py \
  --prompt prompts/PE-FIN/fin_07_evp.md \
  --company "{{COMPANY_NAME}}" \
  --stage "Growth" \
  --sector "HBM반도체" \
  --wacc 10.5 \
  --tgr 3.0 \
  --currency USD

# 2. PE-3 자동검증
python automation/auto_validate.py \
  --file prompts/PE-FIN/fin_07_evp.md \
  --rules PE-1,PE-3 \
  --output reports/evp_validation_$(date +%Y%m%d).json

# 3. Notion 동기화
python automation/notion_sync.py \
  --page-id 34f55ed436f081c2ad05df1dc11e0ae7 \
  --section FIN-07-EVP \
  --mode upsert

# 4. AstraChips LP Fund EVP 실제 적용
python automation/run_prompt.py \
  --prompt prompts/PE-FIN/fin_07_evp.md \
  --company "AstraChips" \
  --stage "Growth" \
  --sector "AI반도체" \
  --wacc 11.0 \
  --tgr 3.5 \
  --currency USD \
  --cross-ref prompts/PE-FIN/fin_06_bfa_jv.md
```

---

## 📋 버전 이력

| 버전 | 날짜 | 변경 내용 | 작성자 |
|------|------|----------|--------|
| v1.0 | 2026-05-08 | 최초 등록 (FCP 주축 다보로낼 + Gilbert 도메인 오버레이) | Gilbert Kwak |

---

*SSOT: `prompts/PE-FIN/fin_07_evp.md` | Notion: PE-FIN 라이브러리 FIN-07-EVP 섹션*
*PE System: PE-1 ✅ · PE-3 ✅ · E-0N PASS | Next Review: 2026-08-08*
