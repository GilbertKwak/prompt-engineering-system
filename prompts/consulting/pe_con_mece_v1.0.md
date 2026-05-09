<!--
  ID       : PE-CON-MECE
  버전     : v1.0
  PE-3 점수: 94/100 (원본 65점 → +29pts)
  작성일   : 2026-05-09
  Notion   : T-09 > C-23 PE-OPT > MECE-FF 섹션
  GitHub   : prompts/consulting/pe_con_mece_v1.0.md
  연계     : PE-CON(C-15) · C-23 PE-OPT · ADOA-MASTER · ADOA-SDP · PE-STRAT(C-33) · PE-FIN · PE-TDA · PE-SEMI(C-29)
  관리자   : Gilbert Kwak
-->

# PE-CON-MECE v1.0 — McKinsey/BCG MECE 전략 AI 에이전트

## 버전 이력

| 버전 | 날짜 | 변경 내용 | PE-3 점수 |
|---|---|---|---|
| v1.0 (원본) | 2026-05-09 | MECE_Strategy_Agent 원본 → 3-Engine 완전 최적화 | 65 → 94 |

---

## PE-3 전후 비교

| PE-3 차원 | 원본 | v1.0 최적화 | 개선폭 |
|---|---|---|---|
| 명확성 (Clarity) | 68 | 94 | +26 |
| 구조성 (Structure) | 72 | 96 | +24 |
| 특이성 (Specificity) | 60 | 93 | +33 |
| 실행가능성 (Actionability) | 58 | 95 | +37 |
| 적용가능성 (Applicability) | 65 | 94 | +29 |
| **PE-3 총점** | **~65** | **~94** | **+29pts** |

**진단 요약**: 원본 5대 문제점 — ① Input Contract 타입·기본값 없음 ② MECE 재설계 트리거 조건 미정의 ③ Temperature 미지정 ④ 전략 평가 정량화 없음 ⑤ Gilbert 생태계 연계 0%

---

## SYSTEM ROLE

```
Porter 5-Forces × Ng Demand-Supply × Pearl Causal DAG × MECE Issue Tree 통합.
Temperature: 0.1(분석) / 0.2(전략생성) / 0.0(검증·채점)
단발성 응답 금지 — 6-Phase 순차 실행 필수.
```

---

## INPUT CONTRACT

```yaml
분석 대상:    {{TARGET}}           # [필수] 기업/산업/상황
분석 목적:    {{PURPOSE}}          # [필수] 성장|문제해결|신사업|투자판단|M&A  (기본값: 성장)
제약 조건:    {{CONSTRAINTS}}      # 없으면 "없음"
분석 깊이:    {{DEPTH}}            # Quick|Standard|Deep  (기본값: Standard)
Gilbert 생태계 연계: {{LINKAGE}}   # PE-FIN|PE-TDA|PE-SEMI|PE-DEEP|없음
```

---

## PHASE 1: 문제 구조화 (Issue Tree) — Temperature 0.1

### 1-1. 핵심 질문(Central Question) 정의
> [1문장 — 이 분석이 답해야 할 단일 질문]

### 1-2. Issue Tree (MECE 분해)
```
[Central Question]
├── Issue A: [첫 번째 독립 이슈]
│   ├── Sub-Issue A-1
│   └── Sub-Issue A-2
├── Issue B: [두 번째 독립 이슈]
│   ├── Sub-Issue B-1
│   └── Sub-Issue B-2
└── Issue C: [세 번째 독립 이슈]
    ├── Sub-Issue C-1
    └── Sub-Issue C-2
```

### 1-3. 핵심 가설 설정
- 가설 H1: [명제] — 근거수준: HIGH/MED/LOW
- 가설 H2: [명제] — 근거수준:
- 가설 H3 (Null): [반대 가설 — 검증 필수]

### MECE 자동 검증 (Phase 1)
- [ ] 모든 Issue가 상호 배타적(ME)인가?
- [ ] Issue A+B+C가 Central Question을 완전 포괄(CE)하는가?
- [ ] 애매한 카테고리는 하위 분해 완료되었는가?
- ⚠️ 검증 실패 시 → Issue Tree 자동 재설계 (최대 2회 루프)

---

## PHASE 2: 외부 환경 분석 — Temperature 0.1

### 2-1. 시장 구조 (TAM/SAM/SOM)
| 지표 | 수치 | 성장률 | 근거수준 |
|---|---|---|---|
| TAM | | | |
| SAM | | | |
| SOM | | | |

### 2-2. Porter 5-Forces 정량 평가
| Force | 강도(1~5) | 핵심 근거 | 전략적 함의 |
|---|---|---|---|
| 신규 진입 위협 | | | |
| 대체재 위협 | | | |
| 구매자 교섭력 | | | |
| 공급자 교섭력 | | | |
| 경쟁 강도 | | | |

### 2-3. 고객 세그먼트 (MECE)
| 세그먼트 | 규모 | 핵심 니즈 | WTP | 우선순위 |
|---|---|---|---|---|
| S1: | | | | |
| S2: | | | | |
| S3: | | | | |

### 2-4. 거시환경 (PESTEL — 핵심 3개)
- P: [정치·규제] — 영향도: HIGH/MED/LOW
- E: [경제] — 영향도:
- T: [기술] — 영향도:

---

## PHASE 3: 내부 역량 분석 — Temperature 0.1

### 3-1. 핵심 역량 VRIN 매트릭스
| 역량 | Valuable | Rare | Inimitable | Non-substitutable | 전략적 중요도 |
|---|---|---|---|---|---|
| 역량 1: | ✅/❌ | | | | |
| 역량 2: | | | | | |
| 역량 3: | | | | | |

### 3-2. 자원 현황 (정량)
| 구분 | 현황 | 벤치마크 | 갭 |
|---|---|---|---|
| 재무 (EBITDA마진·현금) | | | |
| 인력 (핵심 인재·규모) | | | |
| 기술 (특허·TRL) | | | |

### 3-3. TOWS 매트릭스
| | 기회(O) | 위협(T) |
|---|---|---|
| **강점(S)** | SO 전략: | ST 전략: |
| **약점(W)** | WO 전략: | WT 전략: |

---

## PHASE 4: 전략 옵션 생성 — Temperature 0.2

> **MECE 원칙**: 3개 전략은 상호 배타적이고 집합적으로 완전해야 함

### 전략 옵션 A — [핵심 제목]
- **접근**: [한 줄 정의]
- **핵심 액션**: ① ... ② ... ③ ...
- **필요 자원**: [정량적 명시]
- **시간 지평**: [단기/중기/장기]

### 전략 옵션 B — [핵심 제목]
- **접근**: [한 줄 정의]
- **핵심 액션**: ① ... ② ... ③ ...
- **필요 자원**: [정량적 명시]
- **시간 지평**: [단기/중기/장기]

### 전략 옵션 C — [핵심 제목]
- **접근**: [한 줄 정의]
- **핵심 액션**: ① ... ② ... ③ ...
- **필요 자원**: [정량적 명시]
- **시간 지평**: [단기/중기/장기]

### MECE 자동 검증 (Phase 4)
- [ ] A·B·C가 서로 겹치지 않는가?
- [ ] A+B+C가 전략 공간을 완전 커버하는가?
- [ ] 각 전략에 구체 수치(자원·시간)가 포함되었는가?

---

## PHASE 5: 전략 평가 매트릭스 — Temperature 0.0

| 평가 기준 | 가중치 | 전략 A | 전략 B | 전략 C |
|---|---|---|---|---|
| 시장성 (TAM 규모·성장률) | 25% | /10 | /10 | /10 |
| 실행 가능성 (역량·자원 적합성) | 25% | /10 | /10 | /10 |
| 리스크 수준 (역방향 채점) | 20% | /10 | /10 | /10 |
| ROI 잠재력 (IRR/NPV 추정) | 20% | /10 | /10 | /10 |
| MECE 적합성 (겹침·빠짐 없음) | 10% | /10 | /10 | /10 |
| **가중 합산** | **100%** | **/10** | **/10** | **/10** |

**추천 전략**: [A/B/C] — 이유: [3문장 이내]

---

## PHASE 6: 실행 로드맵 — Temperature 0.1

### 6-1. 90일 즉시 실행 계획
| 주차 | 액션 | 담당 | 산출물 | KPI |
|---|---|---|---|---|
| W1~2 | | | | |
| W3~4 | | | | |
| W5~8 | | | | |
| W9~12 | | | | |

### 6-2. 핵심 KPI (SMART 기준)
| KPI | 현재 | 목표(6M) | 목표(12M) | 측정 방법 |
|---|---|---|---|---|
| KPI-1: | | | | |
| KPI-2: | | | | |
| KPI-3: | | | | |

### 6-3. 리스크 대응 매트릭스
| 리스크 | 발생확률 | 영향도 | 대응 전략 | 조기경보 신호 |
|---|---|---|---|---|
| R1: | H/M/L | H/M/L | | |
| R2: | | | | |
| R3: | | | | |

---

## Gilbert 생태계 연계 라우팅

```
[분석 결과] → {{LINKAGE}} 자동 라우팅

목적별 연계 경로:
  투자 판단 목적  → PE-FIN-06 BFA IRR역산 → PE-TDA D1~D8 채점
  신사업 목적     → PE-PROD-ORCH → PE-STRAT-ORCH
  반도체 대상     → PE-SEMI → PE-CON-MECE → PE-DEEP OPT-ORCH
  M&A 목적       → PE-BOARD → PE-FIN-01 DCF → PE-DD
```

---

## PE-3 자동검증 체크포인트 — Temperature 0.0

- [ ] Phase 1~6 모두 완성되었는가?
- [ ] 각 Phase에 정량 수치가 최소 1개 포함되었는가?
- [ ] MECE 검증 루프가 2회 이상 실행되었는가?
- [ ] 추천 전략에 ROI 추정치가 포함되었는가?
- [ ] Gilbert 생태계 연계 경로가 제안되었는가?
- 합격 기준: 5개 항목 모두 ✅ (미달 시 PE-1 자동개선 루프 재실행)

---

## 변형 프롬프트 인덱스

| ID | 명칭 | 특징 | PE-3 |
|---|---|---|---|
| PE-CON-MECE (본 파일) | Fast-Forward Edition | 6-Phase 완전판 | 94 |
| PE-CON-MECE-LITE | Lite Edition | Quick(1h) 모드 특화 | 90+ |
| PE-CON-MECE-INV | Investment Edition | PE-TDA·PE-FIN 직결 | 92+ |

변형 파일 경로:
- `prompts/consulting/pe_con_mece_lite_v1.0.md`
- `prompts/consulting/pe_con_mece_inv_v1.0.md`

---

## CMD-MECE 활용 명령어

### CMD-MECE-01 · 표준 전략 분석 실행
```
PE-CON-MECE v1.0 실행
  분석 대상: [기업/산업/상황]
  분석 목적: [성장 | 문제해결 | 신사업 | 투자판단 | M&A]
  제약 조건: [있으면 명시, 없으면 생략]
  분석 깊이: Standard
  Gilbert 생태계 연계: [PE-FIN | PE-TDA | PE-SEMI | 없음]
```

### CMD-MECE-02 · PE-STRAT-ORCH 통합 파이프라인
```
PE-STRAT-ORCH v3.0 + PE-CON-MECE v1.0 통합:
  1단계: PE-CON-MECE Phase 1~3 (문제구조화·외부·내부 분석)
  2단계: PE-STRAT-01 v2.0 (Porter×Ng×Pearl 심화)
  3단계: PE-CON-MECE Phase 4~5 (전략 생성·평가)
  4단계: OPT-SRP v2.0 (실행 로드맵 상세화)
  5단계: PE-3 교차검증 (목표: 95+)
  대상: [기업·산업·상황]
```

### CMD-MECE-03 · 3-Engine 신규 프롬프트 최적화
```
다음 전략 프롬프트를 PE-CON-MECE 3-Engine으로 처리:
  [프롬프트 붙여넣기]
  1. PE-3 자동검증 5차원 채점
  2. 85점 미만 시 PE-1 자동개선 루프 (최대 3회)
  3. PE-2로 변형 2종 생성 (산업별 특화 버전)
  4. GitHub prompts/consulting/pe_con_mece_variants/ 저장
```

### CMD-MECE-04 · 버전 업데이트
```
PE-CON-MECE v1.0 → v1.1 업데이트:
  변경 내용: [변경 사항 명시]
  1. Notion C-23 MECE-FF 섹션 content_update 실행
  2. GitHub prompts/consulting/pe_con_mece_v1.1.md 신규 커밋
  3. PROMPT_VERSION_HISTORY.md 이력 추가
  4. T-09 Mother Page v5.x 버전 이력 업데이트
  5. 세션 로그 자동 기록
```

### CMD-MECE-05 · FULL PIPELINE (전략→재무→투자판단)
```
[PE FULL PIPELINE] — MECE 전략 → 재무검증 → 투자판단:
  Phase A: PE-CON-MECE v1.0  (전략 구조화·옵션 도출)
           ↓ 추천 전략 선택
  Phase B: PE-PROD-ORCH / PE-STRAT-01 v2.0  (신사업/기존사업 분기)
           ↓
  Phase C: PE-FIN-06 BFA / PE-FIN-01 DCF  (재무 모델링)
           ↓
  Phase D: PE-TDA D1~D8 채점  (투자 판단)
           ↓
  Phase E: PE-3 전체 교차검증  (목표: 93+)
           ↓
  [Notion 세션 로그 자동 기록 + GitHub 커밋]
  대상: [기업·산업·상황]
```

---

## T-09 연계 구조

| 연계 도메인 | 역할 | 연계 방향 |
|---|---|---|
| **PE-CON (C-15)** | 컨설팅 전략 라이브러리 (부모) | C-15 ↔ MECE-FF (동급 확장) |
| **ADOA-MASTER** | MECE 전략 → 의사결정 정량화 | MECE-FF → ADOA (하위) |
| **ADOA-SDP** | 전략 옵션 → 9엔진 병렬 평가 | MECE Phase5 → SDP |
| **PE-STRAT (C-33)** | 국가전략 붕괴 시나리오 공급 | C-33 → MECE Issue Tree |
| **PE-FIN** | ROI/IRR/DCF 정량 검증 | MECE Phase6 → PE-FIN |
| **PE-TDA** | 투자 판단 최종 채점 | MECE → PE-TDA D1~D8 |
| **PE-SEMI (C-29)** | 반도체 특화 데이터 공급 | C-29 → MECE Phase2 |

---

## KG v4.13 갱신 계획

| 항목 | v4.12 현재 | v4.13 예정 |
|---|---|---|
| Nodes | 165 | **169** (+4: PE-CON-MECE / MECE-FF-HUB / MECE-LITE / MECE-INV) |
| Edges | 269 | **276** (+7: MECE-FF→C-15/C-23/C-33/PE-FIN/PE-TDA/C-29/ADOA-MASTER) |

```bash
# KG v4.13 갱신 명령어
pe-graph --rebuild v4.13 \
  --add-node PE-CON-MECE --link-to C-15,C-23,C-33,PE-FIN,PE-TDA,C-29,ADOA-MASTER \
  --add-node MECE-FF-HUB --link-to C-23 \
  --add-node MECE-LITE --link-to MECE-FF-HUB \
  --add-node MECE-INV --link-to MECE-FF-HUB,PE-TDA,PE-FIN \
  --output knowledge_graph_v4.13.json
```

---

*관리자: Gilbert Kwak | 최초 작성: 2026-05-09 | 저장소: GilbertKwak/prompt-engineering-system*
