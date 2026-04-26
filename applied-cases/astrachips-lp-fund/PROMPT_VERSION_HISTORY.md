# 📋 AstraChips AI Infrastructure Fund I — Prompt Version History

> **SSOT 위치**: `prompt-engineering-system/applied-cases/astrachips-lp-fund/`  
> **Notion 연계**: [🧠 프롬프트 엔지니어링 시스템 허브 v2.0](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b)  
> **최초 생성**: 2026-04-26  
> **관리자**: Gilbert Kwak  
> **적용 범위**: AstraChips LP Roadshow 자료 일체 (One-pager, Q&A Handbook, Roadshow Plan, VDR Guide)

---

## 📊 버전 요약표

| 버전 | 날짜 | 프롬프트 유형 | 핵심 산출물 | 상태 |
|------|------|--------------|------------|------|
| v1.0 | 2026-03-01 | 산출물 제안 | 4개 산출물 제안 (One-pager, Q&A, Roadshow Plan, VDR) | ✅ 완료 |
| v2.0 | 2026-03-01 | One-pager 정교화 | LP 배포 가능 수준 AstraChips One-pager (한국어) | ✅ 완료 |
| v3.0 | 2026-03-01 | LP 세그먼트 분화 | Tech/VC LP 테크니컬 버전 (한/영) | ✅ 완료 |
| v4.0 | 2026-03-01 | LP 전략 커스텀 | Hyperscaler/Corporate VC 전략 버전 (한/영) | ✅ 완료 |
| v5.0 | 2026-04-26 | 시스템 아카이브 | 전체 프롬프트 버전별 정리 + Notion/GitHub 업데이트 | ✅ 완료 |

---

## 🔖 v1.0 — 산출물 제안 프롬프트

```
날짜: 2026-03-01
유형: 산출물 정의 (Output Definition)
목적: LP Roadshow용 즉시 제작 가능한 4개 산출물 구조 정의
```

### 📥 프롬프트 원문
```
5️⃣ 지금 바로 만들 수 있는 추가 산출물 제안

LP One-pager 초안 (완전 문장 형태)
→ 위 구조 그대로 A4 1페이지 텍스트 버전 생성.

Q&A Handbook v0.1 (20문·Answer 포함)
→ 가장 까다로운 질문들에 대한 "스탠다드 답변 문안" 작성.

Roadshow 30-day Plan 문서
→ T-30~T+7까지 Action item과 Owner를 표 형식으로 정리.

VDR LP 안내문 (2/3 페이지)
→ "Data Room 구조, 접근 방법, 문의 창구"를 설명하는 PDF용 텍스트.
```

### 📤 핵심 산출물
- **LP One-pager**: Gilbert AI Infrastructure Fund I → 7개 섹션 구조 (Fund Overview, Market Opportunity, Strategy & Portfolio, Key Metrics, SMR Highlight, Risk & Mitigants, Call to Action)
- **Q&A Handbook v0.1**: 20개 질문 + 표준 답변 (IRR 가정, 지정학 리스크, Exit 전략, ESG 등)
- **Roadshow 30-day Plan**: T-30~T+7 타임라인, 구간별 목표, Action Item + Owner
- **VDR LP 안내문**: Data Room 구조 8개 폴더, 접근 절차, NDA 체계

### 🔧 적용 파라미터
```yaml
fund_name: "Gilbert AI Infrastructure Fund I"
target_size: "USD 1.0-1.1B"
portfolio_irr: 16.83%
moic: 1.86x
tvpi: 2.65x
net_irr: 11.4%
smr_equity_irr: 17.9%
first_close_target: "2026 Q3"
```

---

## 🔖 v2.0 — LP One-pager 정교화 프롬프트

```
날짜: 2026-03-01
유형: 문서 정교화 (Document Refinement)
목적: 브랜드 변경(Gilbert → AstraChips) + 실제 LP 배포 가능 수준 완성도 달성
```

### 📥 프롬프트 원문
```
<q>LP One-pager (A4 1페이지 텍스트 초안)
Gilbert AI Infrastructure Fund I – LP One-Pager</q>
1. Gilbert changes to AstraChips
2. "실제 LP 배포 가능한 수준"까지 문장 정교화·압축·톤 맞춤
```

### 📤 핵심 변경사항
- **브랜드 통일**: Gilbert AI Infrastructure Fund I → **AstraChips AI Infrastructure Fund I**
- **톤 교정**: 분석 리포트 톤 → LP 투자설명서(PPM) 수준 공식 문체
- **압축도 향상**: 각 섹션 3-4문장으로 밀도 증가, A4 1페이지 내 수용
- **CTA 구체화**: NDA 체결 → VDR 접근 → 상세 자료 제공 플로우 명시
- **연락처 추가**: ir@astrachips-fund.com

### 📐 최종 구조 (7섹션)
```
1. Fund Overview    → 펀드 정의 + 목표 규모 + 전략 포지셔닝
2. Market Opportunity → 60 ExaFLOPS 성장 + $240B CAPEX 병목 분석
3. Strategy & Portfolio → 3축 (제조 55% / SMR 35% / 유동성 10%)
4. Key Fund Metrics  → TVPI 2.65x / Net IRR 11.4% / Year-7 Payback
5. SMR Anchor Asset  → UAE 300MW / Equity IRR 17.9% / NPV $4.94억
6. Risk & Mitigants  → 6개 시나리오 / 지정학 / 기술 / 금리 대응
7. Contact & Next Steps → Q3 2026 First Close / NDA → VDR
```

---

## 🔖 v3.0 — Tech/VC LP 테크니컬 버전 프롬프트

```
날짜: 2026-03-01
유형: LP 세그먼트 분화 (LP Segmentation)
목적: 기술 이해도가 높은 Tech/VC LP용 기술 중심 버전 한/영 병행 작성
```

### 📥 프롬프트 원문
```
<q>"Tech/VC LP용 더 테크니컬 버전</q>
작성한 내용을 한글과 영어로 별개로 작성
```

### 📤 핵심 차별점 (vs v2.0 Baseline)

| 항목 | Baseline v2.0 | Tech/VC v3.0 |
|------|-------------|-------------|
| 기술 깊이 | 시장 성장 수치 중심 | ExaFLOPS → 하드웨어 스택 연결 |
| 용어 수준 | 일반 투자자 언어 | TSV pitch, RDL, Line/Space µm |
| 포트폴리오 설명 | 3축 자산 배분 | Memory/Packaging Layer 분리 기술 |
| SMR 설명 | PPA + IRR | GPU-hour 당 전력비용 관점 |
| Call to Action | IR 문의 | 기술 로드맵 정렬 제안 |

### 🔧 추가된 기술 파라미터
```yaml
hbm_transition: "HBM3E → HBM4/4E"
packaging: "CoWoS 2.5D + Glass Substrate"
line_space_target: "2/2 µm (vs ABF 5/5 µm)"
smr_load_profile: "High load factor, Low curtailment"
power_target: "150 $/MWh fixed PPA, 300MW"
cluster_scale: "100-300 MW per AI campus"
```

### 📐 섹션 구조 (6섹션, EN/KR 병행)
```
1. Fund Overview      → AI compute stack physical layer
2. Market & Technical Thesis → ExaFLOPS → HW bottleneck analysis
3. Strategy & Portfolio Architecture → HW stack-based allocation
4. Technical Edge & Partner Ecosystem → Corning, OSAT, GPU vendors
5. Return Profile & Risk Envelope → Sharpe 1.4+, stress scenarios
6. Why It's Relevant for Tech/VC LPs → Complement to VC allocation
```

---

## 🔖 v4.0 — Hyperscaler / Corporate VC 전략 커스텀 프롬프트

```
날짜: 2026-03-01
유형: 전략적 LP 타겟 커스텀 (Strategic LP Customization)
목적: 하이퍼스케일러 및 기업 CVC 대상 Co-investment / 용량 확보 프레임 설계
```

### 📥 프롬프트 원문
```
특정 LP(예: hyperscaler CVC, corporate VC 등)를 겨냥한 커스텀 버전으로도 재구성
```

### 📤 핵심 전략 프레임 (Hyperscaler용)

**3가지 협업 모드 (Co-Design & Co-Investment Model)**
```
1. Forward Capacity Alignment
   → 3~5년 GPU/가속기 로드맵 사전 정렬
   → Volume commitments / ROFO / Priority allocation 구조화

2. Strategic Co-Investment
   → 핵심 딜(Korea Glass+HBM JV, Taiwan CoWoS, UAE SMR)에
     전략적 LP로 직접 공동 투자 참여 (개선된 fee/carry 조건)

3. Structured Options for Future Control
   → Call option / Step-in right / Buy-up mechanism
   → 자산 검증 후 완전 내재화(Insourcing)까지 이어지는 경로 설계
```

### 📐 섹션 구조 (6섹션, EN/KR 병행)
```
1. Strategic Fit for Hyperscalers/CVCs → 외부 확장 팔 포지셔닝
2. Why This Matters to You → Capacity bottleneck Pain Point
3. Co-Design / Co-Investment Model → 3개 협업 모드
4. Technical Focus Areas → HBM·Packaging + Power·Thermal
5. Governance & Information Rights → Technical steering committee
6. Financial Profile + Strategic Optionality → Off-balance sheet + 업사이드
```

### 🔧 Hyperscaler-Specific 파라미터
```yaml
collaboration_modes:
  - Forward Capacity Alignment (ROFO, Volume Commitment)
  - Strategic Co-Investment (Improved fee/carry terms)
  - Structured Control Options (Call option, Step-in right)
custom_reporting:
  - Capacity ramp status + Yield trends
  - Technical Steering Committee participation
  - Confidentiality + Conflict management framework
key_differentiator: "Off-balance sheet infra with practical capacity access"
contact: "partners@astrachips-fund.com"
```

---

## 🔖 v5.0 — 시스템 아카이브 및 관리 체계화 프롬프트

```
날짜: 2026-04-26
유형: 시스템 관리 (System Archiving & SSOT 구축)
목적: 본 스페이스 전체 프롬프트 버전 정리 + Notion/GitHub SSOT 구축
```

### 📥 프롬프트 원문
```
본 스페이스에서 적용한 모든 프롬프트를 버전별로 정리 출력
```

```
프롬프트를 notion & github를 참조해서 가장 적합한 장소에 업데이트
(전체 시스템 및 보고서에 적합한 장소 검증 후,
향후 참조하기 용이하고 항상 활용할 수 있는 방안 구축)
```

### 📤 핵심 의사결정 (적합 위치 선정)

```
[GitHub — SSOT / 버전관리]
prompt-engineering-system/
└── applied-cases/
    └── astrachips-lp-fund/          ← 신규 생성
        ├── PROMPT_VERSION_HISTORY.md ← 본 파일 (버전별 프롬프트 전체)
        ├── prompts/
        │   ├── v1_output_definition.md
        │   ├── v2_one_pager_refinement.md
        │   ├── v3_tech_vc_lp.md
        │   ├── v4_hyperscaler_cvc.md
        │   └── v5_system_archive.md
        └── outputs/
            ├── one_pager_baseline_KR.md
            ├── one_pager_tech_vc_KR.md
            ├── one_pager_tech_vc_EN.md
            ├── one_pager_hyperscaler_KR.md
            ├── one_pager_hyperscaler_EN.md
            └── qa_handbook_v0.1.md

[Notion — 문서 허브 / 내부 참조]
🧠 프롬프트 엔지니어링 시스템 허브 v2.0
└── PE-9 AstraChips LP Fund 프롬프트 시스템
    ├── 버전별 프롬프트 인덱스
    ├── 산출물 링크 모음
    └── 재사용 가이드
```

---

## 🔄 재사용 가이드 (향후 유사 프로젝트 적용)

### ✅ 이 시스템을 새 펀드/보고서에 적용할 때

```
Step 1: v1.0 프롬프트로 산출물 4개 구조 정의
Step 2: v2.0 프롬프트로 Baseline One-pager 작성 (브랜드·톤·구조 확정)
Step 3: v3.0 프롬프트로 Tech/VC LP 버전 파생 (기술 파라미터 교체)
Step 4: v4.0 프롬프트로 Hyperscaler/CVC 버전 파생 (협업 모드 교체)
Step 5: 각 버전 산출물 → GitHub outputs/ 에 저장
Step 6: Notion PE 허브 해당 섹션에 링크 추가
```

### 🔧 교체해야 할 파라미터 (새 프로젝트 적용 시)
```yaml
# 반드시 교체
fund_name: "[새 펀드명]"
target_size: "[목표 규모]"
portfolio_irr: [신규 IRR]
moic: [신규 MOIC]
tvpi: [신규 TVPI]
net_irr: [신규 Net IRR]
smr_equity_irr: [해당시 교체]
first_close_target: "[클로징 목표일]"
contact_ir: "[IR 이메일]"
contact_strategic: "[전략 LP 이메일]"

# 기술 파라미터 (Tech/VC 버전)
hbm_transition: "[현재 로드맵]"
packaging: "[현재 패키징 기술]"
power_target: "[전력 단가 목표]"
```

---

## 📊 전체 산출물 인덱스

| 산출물 | 버전 | 언어 | 용도 |
|--------|------|------|------|
| LP One-pager Baseline | v2.0 | KR | 국내 기관 LP 초기 배포 |
| LP One-pager Tech/VC | v3.0 | KR+EN | Tech/VC LP, CVC 배포 |
| LP One-pager Hyperscaler | v4.0 | KR+EN | 하이퍼스케일러, 전략적 LP |
| Q&A Handbook v0.1 | v1.0 | KR | 내부 준비 + IR 팀 |
| Roadshow 30-day Plan | v1.0 | KR | 실행 일정 관리 |
| VDR LP 안내문 | v1.0 | KR | Data Room 접근 안내 |

---

## 📌 관련 링크

- **Notion 허브**: [🧠 프롬프트 엔지니어링 시스템 v2.0](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b)
- **GitHub SSOT**: [prompt-engineering-system](https://github.com/GilbertKwak/prompt-engineering-system)
- **기존 버전 이력**: [global-semi-ai-energy PROMPT_VERSION_HISTORY](https://github.com/GilbertKwak/prompt-engineering-system/blob/main/applied-cases/global-semi-ai-energy/PROMPT_VERSION_HISTORY.md)
- **AstraChips 전략 허브 (Notion)**: [🏢 AstraChips 통합 전략 허브 v1.0](https://www.notion.so/34855ed436f081219806e8ca4210eb26)

---

> **마지막 업데이트**: 2026-04-26  
> **다음 업데이트 예정**: v6.0 (Q3 2026 First Close 이후 — 실제 LP 미팅 피드백 반영)  
> **관리 원칙**: GitHub = SSOT (버전 관리), Notion = 허브 (내부 참조·링크)
