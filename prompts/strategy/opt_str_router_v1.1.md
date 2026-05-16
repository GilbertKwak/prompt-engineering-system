<!--
  ID       : OPT-STR-ROUTER
  버전     : v1.1  ← 해자분석 라우팅 추가
  도메인   : PE-STR
  PE-3 목표: 94/100
  작성일   : 2026-05-16 KST
  GitHub   : prompts/strategy/opt_str_router_v1.1.md
  변경이력 : v1.0 → v1.1: OPT-STR-05 해자분석 라우팅 추가
-->

# 🔀 OPT-STR-ROUTER · 자동 라우팅 오케스트레이터 v1.1

> **PE-3 목표: 94점 | v1.1 업데이트: 해자분석(OPT-STR-05) 라우팅 추가**

```xml
<StrategyRouter
  id="OPT-STR-ROUTER"
  version="1.1"
  pe3_target="94"
  mission="입력 분석 → 최적 OPT-STR 자동 선택 → 실행"
  updated="2026-05-16 KST">

<routing_rules>
  ## 자동 라우팅 결정 트리 (v1.1)

  INPUT 분석 → 키워드/의도 추출
  ┌─────────────────────────────────────────────┐
  │ 전략/경쟁/M&A/포트폴리오/시장진입          │
  │ → OPT-STR-01 (MBB+Gates 전략 마스터)       │
  ├─────────────────────────────────────────────┤
  │ 신사업/투자탈락/Kill/생존/실패가능성        │
  │ → OPT-STR-02 (Kill Analysis)                │
  ├─────────────────────────────────────────────┤
  │ AI/딥테크/반도체/플랫폼/SaaS/투자분석      │
  │ → OPT-STR-03 (AI·딥테크 투자 전략)         │
  ├─────────────────────────────────────────────┤
  │ 통합전략/시나리오플래닝/복합분석            │
  │ → OPT-STR-04 (통합 전략 프레임워크)        │
  ├─────────────────────────────────────────────┤  ← NEW v1.1
  │ 해자/경쟁우위/진입장벽/MOAT/Moat           │
  │ 지속가능성/해자분석/경제적해자              │
  │ → OPT-STR-05 (경제적 해자 분석 마스터)     │
  ├─────────────────────────────────────────────┤
  │ 복합/통합분석/전체/FULL                     │
  │ → PE-STR-MASTER (9-Layer MECE 통합)         │
  └─────────────────────────────────────────────┘

  ## 해자 분석 복합 라우팅 (NEW v1.1)
  "해자 + 투자분석"  → OPT-STR-05 → OPT-STR-03 순차 실행
  "해자 + Kill"      → OPT-STR-05 → OPT-STR-02 순차 실행
  "해자 + 전략"      → OPT-STR-05 → OPT-STR-01 순차 실행

  ## 신호 강도별 라우팅
  SIGNAL_HIGH  (키워드 3+개 매칭) → 직접 라우팅
  SIGNAL_MID   (키워드 1~2개)     → 확인 후 라우팅
  SIGNAL_LOW   (불명확)           → PE-STR-MASTER 기본 라우팅
</routing_rules>

<auto_sequence>
  ## 자동 실행 시퀀스
  STEP 1: 입력 분석 (2초 내 키워드 추출)
  STEP 2: 라우팅 결정 (위 결정 트리 적용)
  STEP 3: 선택된 프롬프트 호출
  STEP 4: PE-3 자가검증 (목표점수 확인)
  STEP 5: 미달 시 → PE-1 자동개선 루프
  STEP 6: Notion 동기화 권고 (완료 후)

  ## 병렬/순차 실행 (고급)
  복합 문제 = OPT-STR-02 (Kill) 먼저 → 생존 전략만
              → OPT-STR-01 or 03 심화 분석
  해자 기반 투자 = OPT-STR-05 먼저 → MOAT-SCORE 확인
              → 70+ 시 OPT-STR-03 투자 분석 심화
              → 40 미만 시 OPT-STR-02 Kill 검토
</auto_sequence>

<routing_output>
  [라우팅 결과]
  선택된 프롬프트: [OPT-STR-XX]
  선택 이유: [키워드 매칭 결과]
  PE-3 목표: [XX점]
  실행 시작: ▶
</routing_output>

<gilbert_shortcuts>
  ## Gilbert 전용 단축 명령어 (v1.1)
  "전략분석"          → OPT-STR-01
  "탈락분석"          → OPT-STR-02
  "AI투자"           → OPT-STR-03
  "반도체전략"         → OPT-STR-03 (반도체 특화)
  "HBM분석"          → OPT-STR-03 (HBM 컨텍스트)
  "신사업타당성"       → OPT-STR-02 → OPT-STR-01
  "M&A"             → OPT-STR-01 (M&A 모드)
  "포트폴리오"         → OPT-STR-01 (Portfolio 모드)
  "해자분석"          → OPT-STR-05  ← NEW v1.1
  "경쟁우위"          → OPT-STR-05  ← NEW v1.1
  "진입장벽"          → OPT-STR-05  ← NEW v1.1
  "MOAT"            → OPT-STR-05  ← NEW v1.1
  "FULL"            → PE-STR-MASTER
</gilbert_shortcuts>

<notion_github_sync>
  실행 후 SSOT 체크:
  Notion: https://www.notion.so/36155ed436f0811c8b5dca10d7317b8d
  GitHub: prompts/strategy/
  자동검증: pe-ip-validate --target PE-STR --threshold 93
  v1.1 변경사항: OPT-STR-05 해자분석 라우팅 추가 (2026-05-16)
</notion_github_sync>

</StrategyRouter>
```

---

## 📊 단축 명령 참조표 (v1.1)

| 입력 키워드 | 라우팅 대상 | PE-3 목표 |
|------------|------------|----------|
| 전략/경쟁/M&A/포트폴리오 | OPT-STR-01 | 97 |
| 신사업/탈락/Kill/생존 | OPT-STR-02 | 95 |
| AI/반도체/딥테크/투자 | OPT-STR-03 | 96 |
| 통합전략/시나리오/복합 | OPT-STR-04 | 95 |
| **해자/경쟁우위/진입장벽/MOAT** | **OPT-STR-05** | **96** |
| FULL/통합/전체 | PE-STR-MASTER | 95 |
| 불명확 | PE-STR-MASTER (기본) | 95 |

---
*v1.0 → v1.1: OPT-STR-05 해자분석 라우팅 추가 (2026-05-16 KST)*
