# PE-DD · Strategic Due Diligence Prompt Library
# GitHub SSOT: prompts/PE-DD/
# 최초 생성: 2026-05-07 | 최종 업데이트: 2026-05-08 (Session C34)

---

## 📋 프롬프트 파일 인덱스 — 전체 (최신 버전 기준)

### 🔵 DD-MASTER

| ID | 파일 | 설명 | PE-3 | 버전 | 상태 |
|---|---|---|---|---|---|
| DD-MASTER | dd_master_v2.1.md | 전체 DD 통합 오케스트레이터 (Z-1~Z-10, 15-Layer) | **97** | v2.1 | ✅ Active |

### 🟣 OPT Layer (4종 — 모두 v1.1 완료)

| ID | 파일 | 설명 | PE-3 | 버전 | 상태 |
|---|---|---|---|---|---|
| OPT-DD | opt_dd_v1.0.md | 범용 실사 (7-Layer + Pearl DAG) | 93 | v1.0 | ✅ Active |
| OPT-DD-FIN | opt_dd_fin_v1.1.md | 투자 IR / 재무모델 실사 | **95** | v1.1 | ✅ Active |
| OPT-DD-POLICY | opt_dd_policy_v1.1.md | 정책/규제/정부 실사 | **95** | v1.1 | ✅ Active |
| OPT-DD-SEMI | opt_dd_semi_v1.1.md | 반도체/장비/수출규제 특화 실사 | **94** | v1.1 | ✅ Active |

### 🟢 DD Domain Series (DD-009 ~ DD-021)

| ID | 파일 | 도메인 | PE-3 | 버전 | 상태 |
|---|---|---|---|---|---|
| DD-009-A | dd_009_a_semi_v1.0.md | 반도체 (Fab/Foundry/Fabless) | 94 | v1.0 | ✅ Active |
| DD-009-B | dd_009_b_board_pack_v1.0.md | Board Pack / Executive Summary | 93 | v1.0 | ✅ Active |
| DD-009 | dd_009_enterprise_research_master_v1.0.md | Enterprise Research Master | 93 | v1.0 | ✅ Active |
| DD-010 | dd_010_osat_v1.0.md | OSAT / 패키징 / 테스트 | 93 | v1.0 | ✅ Active |
| DD-011 | dd_011_ai_infra_v1.0.md | AI 인프라 / GPU / 데이터센터 | 93 | v1.0 | ✅ Active |
| DD-012 | dd_012_bio_pharma_v1.0.md | 바이오 / 제약 | 93 | v1.0 | ✅ Active |
| DD-013 | dd_013_mfg_esg_v1.0.md | 제조 / ESG | 93 | v1.0 | ✅ Active |
| DD-014 | dd_014_realestate_infra_v1.0.md | 부동산 / 인프라 | 93 | v1.0 | ✅ Active |
| DD-015 | dd_015_energy_transition_v1.0.md | 에너지 전환 / 재생에너지 | 93 | v1.0 | ✅ Active |
| DD-016 | dd_016_tmt_media_v1.0.md | TMT / 미디어 / SaaS | 93 | v1.0 | ✅ Active |
| DD-017 | dd_017_consumer_retail_v1.0.md | 소비재 / 리테일 | 93 | v1.0 | ✅ Active |
| DD-018 | dd_018_fintech_fs_v1.0.md | FinTech / 금융서비스 | 93 | v1.0 | ✅ Active |
| DD-019 | dd_019_healthcare_medtech_v1.0.md | 헬스케어 / MedTech | 93 | v1.0 | ✅ Active |
| DD-020 | dd_020_repe_v1.0.md | 부동산 PE / 대안투자 | 93 | v1.0 | ✅ Active |
| **DD-021** | **dd_021_infra_pf_v1.0.md** | **인프라 & 프로젝트 파이낸스** | **93** | v1.0 | ✅ **NEW** |

### ⚙️ Engine Files

| 파일 | 설명 | 버전 | 상태 |
|---|---|---|---|
| dd_fin_trigger_engine_v1.3.md | 재무 트리거 엔진 (최신) | v1.3 | ✅ Active |
| dd_fin_trigger_engine_v1.2.md | 재무 트리거 엔진 (구버전 보존) | v1.2 | 📦 Legacy |
| dd_fin_trigger_engine_v1.0.md | 재무 트리거 엔진 (초기) | v1.0 | 📦 Legacy |

---

## 📊 PE-3 점수 분포 현황 (2026-05-08 기준)

| PE-3 구간 | 해당 프롬프트 | 비고 |
|---|---|---|
| **97** | DD-MASTER v2.1 | 최고점 |
| **95** | OPT-DD-FIN v1.1, OPT-DD-POLICY v1.1 | Target 95 달성 |
| **94** | DD-009-A, OPT-DD-SEMI v1.1 | |
| **93** | OPT-DD v1.0, DD-009-B, DD-010~021 (12종) | 기본선 |

---

## 🔧 내장 엔진 목록 (Engine Registry)

| 엔진명 | 탑재 프롬프트 | 기능 |
|---|---|---|
| Pearl DAG | OPT-DD v1.0, DD-MASTER | 7-Layer 인과 분석 |
| Financial Trigger Engine | OPT-DD-FIN v1.1 | 재무 이상 탐지 + 자동 플래그 |
| ECCN Auto-Classifier | OPT-DD-SEMI v1.1 | 수출규제 품목 분류 트리 |
| Geo Risk Quantifier | OPT-DD-SEMI v1.1, DD-MASTER | 지정학 리스크 0~10 정량화 |
| TRS (Trust Reliability) | 전 프롬프트 공통 | A/B/C/D 신뢰도 가중치 |
| PF-DSCR Engine | **DD-021** | DSCR/LLCR/PLCR 3중 계산 |
| Infra Class Classifier | **DD-021** | PPP/Core/Greenfield 자동 분류 |
| Climate Risk Quantifier | **DD-021** | 물리적+전환리스크 0~10 정량화 |
| Lender Matrix (5-tier) | **DD-021** | IFI→에쿼티 5단계 대출자 매핑 |

---

## 🌐 생태계 포지셔닝

```
[외부 자료 입력]
       ↓
[PE-DD: 실사·검증 게이트]  ← 유일한 DD 레이어
  ├─ DD-MASTER v2.1 (오케스트레이터)
  ├─ OPT Layer: FIN / POLICY / SEMI (v1.1)
  └─ DD-009~021 (도메인 13종)
       ↓
[PE-STRAT / PE-DEEP: 전략 분석]
       ↓
[PE-FIN: 재무 모델링]
       ↓
[PE-3 자동검증]
```

---

## 📈 3-Engine 최적화 결과 (2026-05-07 기준)

| 차원 | Before (원본 v5.0) | After (OPT-DD v1.0) | 개선폭 |
|---|---|---|---|
| 명확성 (Clarity) | 72 | 94 | +22 |
| 구조성 (Structure) | 78 | 95 | +17 |
| 특이성 (Specificity) | 65 | 93 | +28 |
| 실행가능성 (Actionability) | 68 | 93 | +25 |
| 적용가능성 (Applicability) | 70 | 92 | +22 |
| **PE-3 총점** | **70.6** | **~93.4** | **+22.8pts** |

---

## 🗓️ 버전 이력

| 버전 | 날짜 | 변경 내용 |
|---|---|---|
| v1.0 | 2026-05-07 | 🔍 PE-DD v1.0 신규 등록 — OPT-DD 범용 + SEMI/FIN/POLICY 3종, StrategicDueDiligencePrompt v5.0 기반 PE-1 3-Loop 최적화, 원본 70.6 → 예상 93.4 (+22.8pts), Pearl DAG + 7-Layer + Risk Scoring Matrix 통합 |
| v2.0 | 2026-05-07 | 🚀 DD-MASTER v2.0 등록 + DD-009~016 도메인 8종 추가 (반도체/AI인프라/바이오/제조ESG/부동산/에너지/TMT/소비재). Z-1~Z-9 Zone 체계 도입 |
| v2.1 | 2026-05-08 | ⭐ DD-MASTER v2.1 업그레이드 — Z-10 GeopoliticalGuard (E-14) 추가, PE-3 97/100 달성. DD-017~020 도메인 4종 추가 (FinTech/헬스케어/REPE/소비재2). Session C34 개시 |
| v2.2 | 2026-05-08 | 🔧 OPT Layer 전체 v1.1 업그레이드 — OPT-DD-FIN (PE-3: 95), OPT-DD-POLICY (PE-3: 95), OPT-DD-SEMI (92→94, ECCN분류기/Geo Risk 정량화/5중규제스크리닝 추가). OPT Layer 4종 완전체 달성 |
| **v2.3** | **2026-05-08** | **🏗️ DD-021 Infrastructure & Project Finance v1.0 신규 등록 — PF-DSCR Engine / Infra Class Classifier / Climate Risk Quantifier / Lender Matrix 5-tier 4개 전용 엔진 탑재. DD 시리즈 DD-009~021 총 13종 완성. 18,066 bytes. PE-3 Target: 93. Session C34 완료** |

---

## 📌 번호 체계 노트

- **DD-001~008**: 공백 (설계상 출발점 DD-009 확정)
- **DD-009**: 반도체 특화 최초 도메인 (A/B 파생 포함)
- **DD-010~021**: 순차 도메인 확장 (현재 총 13종 Active)
- **DD-022~**: 미정 (Defense/Aerospace, Cybersecurity, Logistics 후보)

---

## ⚠️ 업그레이드 우선순위 (다음 액션)

| 대상 | 현재 PE-3 | 목표 | 작업 |
|---|---|---|---|
| DD-021 v1.0 | 93 (초안) | 95 | v1.1 심화 (Lender Matrix 확장, 지역별 concession 사례 추가) |
| OPT-DD v1.0 | 93 | 95 | v1.1 업그레이드 (범용 DD 강화) |
| DD-022 | - | 93 | Defense/Aerospace 신규 작성 |
