# PROMPT VERSION HISTORY — PE-STRAT

## E2E 검증 케이스 이력

| TC | 대상 | 파이프라인 | INSIGHT_ID | 날짜 | 결과 |
|----|------|-----------|------------|------|------|
| TC-01 | (내부 검증) | AIF v1.0 단독 | — | 2026-04-01 | ✅ PASS |
| TC-02 | SteelCore-K | AIF v1.0 → SFA v1.0 | SCK-IND-260430 | 2026-04-30 | ✅ PASS |
| TC-03 | CloudFlow SaaS | AIF v1.0 → SFA v1.0 | CLF-SAAS-240507 | 2026-05-07 | ✅ PASS (PE-3 94/93) |
| **TC-04** | **HoldCo-K** | **AOCRS→CSGS→GHCRA→AIF→SFA→PE-FIN** | **HCK-HOLD-260507** | **2026-05-07** | **✅ 전 구간 PASS · CONDITIONAL_PROCEED** |

---

## v1.2-candidate — 발견사항 (TC-04 기반)

> TC-04 E2E 전 파이프라인 실행 중 발견된 개선 후보 — 다음 마이너 릴리즈 반영 예정

### FINDING-01 · PE-FIN 수신 로직 (FIN-07/08)
- RED 에스컬레이션 수신 시 상태를 `PENDING_DD_RESOLUTION`으로 명시하는 수신부 표준화 필요
- PE-FIN FIN-07: Option C(분리 바이아웃) 처리 경로 추가
- 대상 파일: PE-FIN FIN-07/08 프롬프트 수신부

### FINDING-02 · GHCRA→AIF 전환 시 sub_target 필드
- HoldCo → 자회사 분리 투자 구조에서 `company_name`이 전환되는 시점 명시 부재
- HANDOFF_03에 `sub_target` 필드 추가 권고
- 대상 파일: `OPT-GHCRA-v1.2.md` HANDOFF_PACKET 스키마

### FINDING-03 · CSGS→GHCRA 자동 매핑 테이블
- CSGS Scenario B/C 판정 결과가 GHCRA PE 구조 권고(PE-A/B/C)에 자동 매핑되는 로직 미존재
- CSGS Scenario → GHCRA PE 구조 매핑 테이블 추가 권고
- 대상 파일: `OPT-CSGS-v1.2.md` 출력 섹션 + `OPT-GHCRA-v1.2.md` 입력 수신부

---

## v1.1 — 2026-05-07

### OPT-AOCRS v1.1
- **F1**: HANDOFF_PACKET YAML 표준 구조 신설 (→ CSGS 자동 전달)
- **F2**: AUTO_SCORE 5항목 체크리스트 + SCORE_GATE_90 내장
- **F3**: Worked Example (HoldCo-K) — Layer 1/2 지분 테이블 + Stress Matrix

### OPT-CSGS v1.1
- **F1**: AOCRS→CSGS HANDOFF relay 자동전파 수신부 신설
- **F2**: Output Contract AUTO_SCORE + /rerun --loop1 트리거
- **F3**: Worked Example (HoldCo-K) — 상속세 실계산 (세액 1.86조, 강제매각 후 25.6%)

### OPT-GHCRA v1.1
- **F1**: CSGS→GHCRA HANDOFF relay, PE-FIN FIN-07 라우팅 패킷
- **F2**: 5차원 스코어카드 AUTO_SCORE 검증
- **F3**: Worked Example (HoldCo-K) — 국가별 스코어카드 (US 8.2/HIGH, EU 7.2/HIGH)

### OPT-AIF v1.1
- **F1**: AIF HANDOFF_PACKET 표준 YAML 신설 (→ SFA 자동 전달); AOCRS 패킷 자동 수신부
- **F2**: AUTO_SCORE 5항목 체크리스트 + SCORE_GATE_90 내장
- **F3**: Worked Example (SteelCore-K) — Ecosystem 6.40, Moat Tier-2, Base IRR 31%

### OPT-SFA v1.1
- **F1**: AIF→SFA HANDOFF relay 자동수신 + SFA→PE-FIN HANDOFF_PACKET 출력
- **F2**: AUTO_SCORE 5항목 체크리스트 + SCORE_GATE_90 내장
- **F3**: Worked Example (SteelCore-K) — Platform C 구조, Base IRR 34%, VERDICT: PROCEED

### E2E TC-03 · CloudFlow SaaS (AIF v1.0 → SFA v1.0)
- OPT-AIF PE-3 실측 **94** / OPT-SFA PE-3 실측 **93** (목표 일치)
- bear_case AUTO-SET 구조 SFA 확률 자동 반영 검증
- INSIGHT_ID: CLF-SAAS-240507

### **E2E TC-04 · HoldCo-K 풀 파이프라인 [신규 — 2026-05-07]**
- **최초 6단계 풀 파이프라인 E2E 검증** (AOCRS→CSGS→GHCRA→AIF→SFA→PE-FIN)
- F1 체인 무결성: HANDOFF_01~05 전 구간 자동 전파, 재입력 **0회**
- F2 AUTO_SCORE: 전 구간 5/5, SCORE_GATE_90 위반 **0건**
- F3 Worked Example: 상속세 5,528억 → CFIUS HIGH → Moat 7.49 → IRR 34% 인과관계 체인 완전 추적
- VERDICT: CONDITIONAL_PROCEED (KAI Systems 분리 바이아웃 Option C)
- INSIGHT_ID: HCK-HOLD-260507
- 파일: `e2e_tc04_holdco_k_full_pipeline.md`

---

## v1.0 — 2026-04-01 (Initial Release)

### OPT-AOCRS v1.0
- Initial PE-3 optimized prompt for Ownership & Control Risk Structure

### OPT-CSGS v1.0
- Initial PE-3 optimized prompt for Corporate Succession & Governance Strategy

### OPT-GHCRA v1.0
- Initial PE-3 optimized prompt for Global Holding Company Regulatory Assessment

### OPT-AIF v1.0
- Initial PE-3 optimized prompt for AI Industry Framework

### OPT-SFA v1.0
- Initial PE-3 optimized prompt for Strategic Fit Assessment

---

## Roadmap

| Priority | Item | Target Version | Status |
|----------|------|---------------|--------|
| ~~HIGH~~ | ~~D) HoldCo-K E2E TC-04 검증 케이스~~ | ~~v1.2~~ | ✅ **완료 (2026-05-07)** |
| HIGH | FINDING-01: PE-FIN FIN-07/08 수신 로직 PENDING 표준화 | v1.2 | 🔲 대기 |
| HIGH | FINDING-02: GHCRA HANDOFF_03 sub_target 필드 추가 | v1.2 | 🔲 대기 |
| HIGH | FINDING-03: CSGS Scenario→GHCRA PE 구조 매핑 테이블 | v1.2 | 🔲 대기 |
| HIGH | C) PE-FIN FIN-07/08 수신 로직 업데이트 | v1.1-FIN | 🔲 대기 |
| MED | A) Notion PE-STRAT 페이지 동기화 | v1.1 | 🔲 대기 |
| MED | E2E SteelCore-K TC-05 (AIF→SFA→FIN) | v1.2 | 🔲 대기 |
| MED | E2E TC-05 HoldCo-K v1.2-candidate 검증 (FINDING 3건 반영 후) | v1.2 | 🔲 대기 |
