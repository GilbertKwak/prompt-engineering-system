# P-OPT-FIN-MASTER v1.0
# Financial & Investment Analysis Hub — PE-FIN-HUB
# ================================================
# Code      : PE-FIN-MASTER
# Section   : C-31
# Version   : 1.0
# Author    : Gilbert Kwak
# Created   : 2026-04-30
# PE-3 Target: 96+
# Domain    : Financial & Investment Analysis
# Engine    : T-09 PE-1 / PE-2 / PE-3
# SSOT      : Notion PE-IP SECTION 2 + GitHub PE-FIN/
# ================================================

---

## 📋 메타데이터

| 항목 | 값 |
|------|----|
| 코드 | PE-FIN-MASTER |
| 섹션 | C-31 |
| 버전 | v1.0 |
| 작성일 | 2026-04-30 |
| PE-3 목표 | 96점+ |
| 도메인 | 재무·투자 분석 라이브러리 |
| Gilbert 컨텍스트 | 반도체·배터리·JV·M&A·신용·광물 재무 영향 |
| 연동 엔진 | T-09 PE-1(자동개선)·PE-2(자동증식)·PE-3(자동검증) |
| Notion 위치 | PE-IP SECTION 2 → PE-FIN 라이브러리 |
| GitHub 경로 | `PE-FIN/fin_master_v1.0.md` |

---

## 🔗 도메인 연계 맵

| 연계 도메인 | 코드 | 엣지 타입 | 방향 |
|------------|------|----------|------|
| PE-JV | C-10 | ALPHA_SIGNAL_INPUT | PE-JV → PE-FIN |
| PE-BOARD | C-11 | MA_VALUATION_FEED | PE-BOARD → PE-FIN |
| SEMI-OPT-GNN | C-31 연계 | RISK_PROB_TO_EBITDA | GNN → FIN-001 |
| PE-MIN | C-27 | MINERAL_SHOCK_QUANTIFY | PE-MIN → FIN-001/002 |
| PE-SEMI | C-29 | FAB_UTIL_TO_REVENUE | PE-SEMI → FIN-001 |
| PE-EQP | C-22 | EQP_STATE_TO_CAPEX | PE-EQP → FIN-002 |

---

## 🔀 Auto Mode Detection

```
MODE-A [EBITDA_SHOCK]   트리거: "EBITDA", "충격", "가동률 영향", "shock"
                        → FIN-001 실행

MODE-B [VALUATION]      트리거: "DCF", "밸류에이션", "기업가치", "valuation"
                        → FIN-002 실행

MODE-C [CREDIT_RISK]    트리거: "신용", "채권", "등급", "credit", "bond"
                        → FIN-003 실행

MODE-D [JV_FUND_SIM]    트리거: "JV", "펀드", "수익률", "IRR", "fund"
                        → FIN-004 실행

MODE-AUTO               컨텍스트 복합 시 → 최고 관련도 모드 자동 선택
```

---

## 🟦 하위 프롬프트 라이브러리

| ID | 파일 | PE-3 목표 | 기능 |
|----|------|----------|------|
| FIN-001 | `fin_001_ebitda_shock_v1.0.md` | 96 | EBITDA 충격 시뮬레이션 |
| FIN-002 | `fin_002_dcf_valuation_v1.0.md` | 95 | DCF 밸류에이션 + 시나리오 |
| FIN-003 | `fin_003_credit_risk_v1.0.md` | 94 | 채권/신용등급 리스크 모델 |
| FIN-004 | `fin_004_jv_fund_sim_v1.0.md` | 96 | JV 펀드 수익률 시뮬레이션 |

---

## 📊 PE-3 자가 검증 규칙

```
출력 전 PE-3 5차원 자가 점검:
① 명확성(Clarity)          >= 19/20
② 구체성(Specificity)       >= 20/20
③ 실행가능성(Actionability) >= 19/20
④ 완전성(Completeness)      >= 19/20
⑤ Gilbert 컨텍스트 정렬    >= 19/20
→ 총점 < 93이면 자동 재생성
→ 96점 이상 목표
```

---

## 📅 변경 이력

| 버전 | 날짜 | 내용 |
|------|------|------|
| **v1.0** | 2026-04-30 | CMD-FS-05 — PE-FIN C-31 도메인 신설. FIN-001~004 라이브러리 초기화. T-09 C-31 등록. knowledge_graph v4.4 연동. |

---

> ✅ **[v1.0 | 2026-04-30 17:40 KST]** PE-FIN-MASTER v1.0 최초 생성 완료
> — C-31 신설 · FIN-001~004 라이브러리 초기화 · PE-3 96점 목표
> — T-09 PE-1/PE-2/PE-3 3-Engine 완전 연동 · knowledge_graph v4.4 반영 🟢

**버전**: v1.0 | **최종갱신**: 2026-04-30 17:40 KST | **관리자**: Gilbert Kwak | **상위 허브**: PE-FIN → PE-IP → T-09
