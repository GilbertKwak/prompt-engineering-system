# 📁 prompts/strategy/

> **PE-STR 도메인** — 전략·신사업 통합 리서치 & 의사결정 프롬프트 라이브러리
> **인덱스 버전**: v2.0 | **마지막 동기화**: 2026-05-16 08:04 KST

---

## 파일 목록 (전체)

| 파일명 | 코드 | 버전 | PE-3 목표 | 상태 | 설명 |
|--------|------|------|-----------|------|------|
| `pe_str_master_v1.0.md` | PE-STR-MASTER | v1.0 | 95 | 🟢 Active | 9-Layer MECE 전략·신사업 통합 마스터 |
| `opt_str_01_mbb_gates_v2.0.md` | OPT-STR-01 | v2.0 | 97 | 🟢 Active | MBB+Gates 전략 마스터 |
| `opt_str_02_kill_analysis_v2.0.md` | OPT-STR-02 | v2.0 | 95 | 🟢 Active | Kill Analysis 탈락 검증 |
| `opt_str_03_ai_deeptech_v2.0.md` | OPT-STR-03 | v2.0 | 96 | 🟢 Active | AI·딥테크 투자 전략 |
| `opt_str_04_integrated_v1.0.md` | OPT-STR-04 | v1.0 | 96 | 🟢 Active | **통합 전략 분석 & 실행 로드맵 마스터** |
| `opt_str_router_v1.0.md` | OPT-STR-ROUTER | v1.0 | 94 | 🟢 Active | 자동 라우터 |
| `PROMPT_VERSION_HISTORY.md` | — | — | — | 📋 참조 | 버전 이력 |

---

## OPT-STR 시리즈 실행 가이드

```
입력 키워드          → 실행 프롬프트
─────────────────────────────────────────
"전략분석"           → OPT-STR-01  [PE-3: 97]
"탈락분석"           → OPT-STR-02  [PE-3: 95]
"AI투자"             → OPT-STR-03  [PE-3: 96]
"통합전략"            → OPT-STR-04  [PE-3: 96]  ← NEW
"반도체전략"          → OPT-STR-03 (HBM/OSAT 특화)
"신사업타당성"        → OPT-STR-02 → OPT-STR-01
"전략분석FULL"        → OPT-STR-ROUTER 경유
"FULL"               → PE-STR-MASTER (9-Layer)
```

---

## PE-STR-MASTER 구조

```
PE-STR-MASTER v1.0
├── PHASE 0: Auto-Mode Detection (9-Mode)
├── PHASE 1: Essence Gate (Steve Jobs)
├── PHASE 2: First Principles (Elon Musk)
├── PHASE 3: 9-Layer MECE Analysis
│   ├── Layer A [INSIGHT]
│   ├── Layer B [DECISION]
│   ├── Layer C [MARKET]    → Router: PE-CON-008
│   ├── Layer D [TECH-IP]
│   ├── Layer E [BIZ-GTM]   → Router: PE-PROD
│   ├── Layer F [ECOSYSTEM] → Router: PE-CON-007
│   ├── Layer G [NEWBIZ]    → Router: PE-NBD
│   ├── Layer H [PORTFOLIO]
│   └── Layer I [RISK]
├── PHASE 4: Strategic Options (Playing to Win)
├── PHASE 5: Compounding Gate (Bezos)
├── PHASE 6: False Positive Filter
└── PHASE 7: Output Format (5 Sections)
```

---

## OPT-STR-04 프레임워크 인과 흐름

```
PEST (매크로 환경)
  └─► SWOT (전략 포지션 합성)
        └─► Porter VC (가치 차별화 맵)
              └─► BCG (포트폴리오 분류)
                    └─► McKinsey 7-S (조직 정합성 진단)
                          └─► 3 Horizons (혁신 포트폴리오 배분)
```

---

## SSOT 연계

- **Notion PE-STR 라이브러리**: [바로가기](https://www.notion.so/36155ed436f0811c8b5dca10d7317b8d)
- **Notion OPT-STR-04**: [바로가기](https://www.notion.so/36155ed436f0813db601cd7924a9655e)
- **상위 계층**: T-09 > PE-IP > PE-STR
- **마지막 동기화**: 2026-05-16 08:04 KST

---

## PE-3 검증 명령어

```bash
# 전체 PE-STR 검증
pe-ip-validate --target PE-STR --threshold 93

# OPT-STR-04 단독 검증
pe-ip-validate --target OPT-STR-04 --threshold 93

# 신규 프롬프트 추가
pe-ip-add --code OPT-STR-05 --domain PE-STR
```
