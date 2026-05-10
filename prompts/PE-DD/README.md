# PE-DD · Enterprise Due Diligence Prompt Library

> **Domain**: PE-DD | **Status**: ✅ Active | **Updated**: 2026-05-10 (Session C36)  
> **Notion**: [PE-DD Library v1.0](https://www.notion.so/35955ed436f081028fbbe44e65f63d84)  
> **Parent System**: T-09 Prompt Engineering Ecosystem

---

## 📂 Library Index (DD-MASTER + 18 Domains)

### 🔵 DD-MASTER

| ID | 파일명 | 버전 | PE-3 | 상태 |
|---|---|---|---|---|
| **P-OPT-DD-MASTER** | `dd_master_v2.1.md` | v2.1 | **97/100** | ✅ Active |

### 🟣 OPT Layer (4종)

| ID | 파일명 | 버전 | PE-3 | 상태 |
|---|---|---|---|---|
| OPT-DD | `opt_dd_v1.0.md` | v1.0 | 93 | ✅ Active |
| OPT-DD-FIN | `opt_dd_fin_v1.1.md` | v1.1 | **95** | ✅ Active |
| OPT-DD-POLICY | `opt_dd_policy_v1.1.md` | v1.1 | **95** | ✅ Active |
| OPT-DD-SEMI | `opt_dd_semi_v1.1.md` | v1.1 | **94** | ✅ Active |

### 🟢 DD Domain Series (18종 — DD-009 ~ DD-026)

| ID | 파일명 | 도메인 | PE-3 | 상태 |
|---|---|---|---|---|
| DD-009-A | `dd_009_a_semi_v1.0.md` | 반도체 (Fab/Foundry/Fabless) | 94 | ✅ Active |
| DD-009-B | `dd_009_b_board_pack_v1.0.md` | Board Pack / Executive Summary | 93 | ✅ Active |
| DD-009 | `dd_009_enterprise_research_master_v1.0.md` | Enterprise Research Master | 93 | ✅ Active |
| DD-010 | `dd_010_osat_v1.0.md` | OSAT / 패키징 / 테스트 | 93 | ✅ Active |
| DD-011 | `dd_011_ai_infra_v1.0.md` | AI 인프라 / GPU / 데이터센터 | 93 | ✅ Active |
| DD-012 | `dd_012_bio_pharma_v1.0.md` | 바이오 / 제약 | 93 | ✅ Active |
| DD-013 | `dd_013_mfg_esg_v1.0.md` | 제조 / ESG | 93 | ✅ Active |
| DD-014 | `dd_014_realestate_infra_v1.0.md` | 부동산 / 인프라 | 93 | ✅ Active |
| DD-015 | `dd_015_energy_transition_v1.0.md` | 에너지 전환 / 재생에너지 | 93 | ✅ Active |
| DD-016 | `dd_016_tmt_media_v1.0.md` | TMT / 미디어 / SaaS | 93 | ✅ Active |
| DD-017 | `dd_017_consumer_retail_v1.0.md` | 소비재 / 리테일 | 93 | ✅ Active |
| DD-018 | `dd_018_fintech_fs_v1.0.md` | FinTech / 금융서비스 | 93 | ✅ Active |
| DD-019 | `dd_019_healthcare_medtech_v1.0.md` | 헬스케어 / MedTech | 93 | ✅ Active |
| DD-020 | `dd_020_repe_v1.0.md` | 부동산 PE / 대안투자 | 93 | ✅ Active |
| DD-021 | `dd_021_infra_pf_v1.0.md` | 인프라 & 프로젝트 파이낸스 | 93 | ✅ Active |
| DD-022 | `dd_022_defense_aerospace_v1.0.md` | 방산 / 항공우주 | 93 | ✅ Active |
| DD-023 | `dd_023_cybersecurity_v1.0.md` | 사이버보안 / 정보보안 | 93 | ✅ Active |
| DD-024 | `dd_024_private_credit_v1.0.md` | 프라이빗 크레딧 / 직접대출 | 93 | ✅ Active |
| **DD-025** | **`dd_025_logistics_sc_v1.0.md`** | **물류 / 공급망 관리** | **93** | ✅ **NEW** |
| **DD-026** | **`dd_026_space_satellite_v1.0_part1~3.md`** | **우주 / 위성** | **93** | ✅ **NEW** |

---

## 🗺️ DD-MASTER v2.1 Zone 구조

```
P-OPT-DD-MASTER v2.1 (PE-3: 97)
    ├── Z-1  Executive Summary
    ├── Z-2  Commercial & Market DD
    ├── Z-3  Financial DD
    ├── Z-4  Legal & Regulatory DD
    ├── Z-5  Technology & Engineering DD
    ├── Z-6  People & ESG DD
    ├── Z-7~9  Domain-Specific Zones (파생별 오버라이드)
    └── Z-10 Geopolitical & Supply Chain Risk [v2.1 NEW]
         └── E-14 GeopoliticalGuard (GEO_RISK: LOW→CRITICAL)
```

---

## 🔗 Cross-Domain Links

- **PE-SEMI**: 반도체 전략 분석 생태계
- **PE-FIN**: 재무 모델링·가치평가
- **PE-CON**: 계약·법무 검토
- **PE-OPT**: 자기진화 최적화 시스템 (EVO-001 등록)
- **T-09**: Mother Page — 전체 PE 생태계 허브

---

## 📋 Usage

```xml
<!-- 기본 실행 (STD 깊이, 범용) -->
COMPANY_NAME  = "[대상 기업]"
DD_TYPE       = "FULL"
DEAL_CONTEXT  = "M&A"
DEPTH         = "STD"
OUTPUT_LANG   = "KR"

<!-- 물류/공급망 M&A 특화 실행 -->
COMPANY_NAME  = "[물류 기업]"
DD_TYPE       = "FULL"
DEAL_CONTEXT  = "M&A"
DEPTH         = "DEEP"
GEO_RISK      = "HIGH"
OUTPUT_LANG   = "KR"

<!-- 우주/위성 투자 실사 -->
COMPANY_NAME  = "[우주기업]"
DD_TYPE       = "TECH"
DEAL_CONTEXT  = "INVESTMENT"
DEPTH         = "DEEP"
GEO_RISK      = "CRITICAL"
OUTPUT_LANG   = "Bilingual"
```
