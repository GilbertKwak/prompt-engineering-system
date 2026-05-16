# PE-STR 프롬프트 버전 이력 (SSOT)

> **경로**: `prompts/strategy/`  
> **최종 업데이트**: 2026-05-16  
> **관리 원칙**: GitHub = SSOT · Notion PE-STR 페이지와 동기화

---

## 📋 프롬프트 인덱스 (v1.1 기준)

### 통합 마스터

| ID | 파일 | 유형 | PE-3 목표 | 버전 | 상태 |
|---|---|---|---|---|---|
| PE-STR-MASTER | `pe_str_master_v1.0.md` | 9-Layer MECE 통합 마스터 | 95 | v1.0 | ✅ Active |

### OPT-STR 경량화 세트

| ID | 파일 | 역할 | PE-3 목표 | 버전 | 단축명령 | 상태 |
|---|---|---|---|---|---|---|
| OPT-STR-01 | `opt_str_01_mbb_gates_v2.0.md` | MBB+Gates 전략 마스터 | 97 | v2.0 | "전략분석" | ✅ Active |
| OPT-STR-02 | `opt_str_02_kill_analysis_v2.0.md` | Kill Analysis | 95 | v2.0 | "탈락분석" | ✅ Active |
| OPT-STR-03 | `opt_str_03_ai_deeptech_v2.0.md` | AI·딥테크 투자 전략 | 96 | v2.0 | "AI투자" | ✅ Active |
| OPT-STR-04 | `opt_str_04_integrated_v1.0.md` | 통합 전략 프레임워크 | 95 | v1.0 | "통합전략" | ✅ Active |
| OPT-STR-05 | `opt_str_05_moat_analysis_v1.0.md` | 경제적 해자(경제적해자) 분석 마스터 | 96 | v1.0 | "해자분석" | ✅ Active |

### 라우터 & 이력 관리

| ID | 파일 | 유형 | 버전 | 상태 |
|---|---|---|---|---|
| OPT-STR-ROUTER | `opt_str_router_v1.1.md` | 자동 라우팅 오케스트레이터 | v1.1 | ✅ Active |
| 이력관리 | `PROMPT_VERSION_HISTORY.md` | 버전 SSOT | v2.0 | ✅ Active |

---

## 🔄 버전 변경 이력

### v2.0 — 2026-05-16 KST  ← 현재
**변경 유형**: OPT-STR-05 해자분석 신규 등록 + ROUTER v1.1 라우팅 추가

#### OPT-STR-05 v1.0 신규 등록
- **프레임워크**: Morningstar 5-Moat × Porter 5-Forces × Hamilton-Helmer 7Powers
- **해자 유형**: Network Effect / Switching Cost / Cost Advantage / Intangible Asset / Efficient Scale
- **9-Layer 분석**: 해자 현황 스캔 → 원체분석 → 내구성 → 위협 → 확장성 → 재무증거 → 반도체AI특화 → MOAT-SCORE → 전략함의
- **MOAT-SCORE**: Width(40) + Depth(30) + Reach(20) + 재무증거(10) = 100점 체계
- **연계**: OPT-STR-01/02/03/04 순차 실행 통합 지원
- **반도체 특화**: TSMC CoWoS/ASML EUV/CUDA 생태계/HBM 라인 명시
- **PE-3 목표**: 96/100
- **GitHub**: `prompts/strategy/opt_str_05_moat_analysis_v1.0.md`
- **Notion**: https://www.notion.so/36255ed436f0811db316ece28518c05b
- **단축명령**: "해자분석" | "경쟁우위" | "진입장벽" | "MOAT"

#### OPT-STR-ROUTER v1.0 → v1.1 업데이트
- **변경**: OPT-STR-05 해자분석 라우팅 노드 추가
- **신규 라우팅 키워드**: 해자 / 경쟁우위 / 진입장벽 / MOAT / 해자분석 / 경제적해자
- **복합 라우팅 추가**: "해자+투자" → STR-05→STR-03 / "해자+Kill" → STR-05→STR-02
- **단축명령 추가**: "해자분석" / "경쟁우위" / "진입장벽" / "MOAT"
- **GitHub**: `prompts/strategy/opt_str_router_v1.1.md`

**코밋트**: `84b1d602` — feat: Add OPT-STR-05 Moat Analysis v1.0 + Update Router v1.1

---

### v1.2 — 2026-05-15 KST
**변경 유형**: OPT-STR-02/03/ROUTER v1.0 신규 등록 + PE-STR 도메인 정식화

#### OPT-STR-02 v2.0 신규
- **프레임워크**: Kill Analysis (Reverse DCF + 탈락 기준 명문화)
- **PE-3 목표**: 95/100
- **단축명령**: "탈락분석" | "신사업타당성"

#### OPT-STR-03 v2.0 신규
- **프레임워크**: AI·딥테크 투자 전략 (반도체 HBM/CoWoS 특화)
- **PE-3 목표**: 96/100
- **단축명령**: "AI투자" | "반도체전략" | "HBM분석"

#### OPT-STR-ROUTER v1.0 신규
- **초기 라우팅**: OPT-STR-01/02/03 + PE-STR-MASTER 4노드
- **단축명령**: 9개 커맨드 (전략분석/탈락분석/AI투자/반도체전략/HBM분석 등)

**코밋트**: `f29f1f6d` — feat: Add OPT-STR-02/03/ROUTER v1.0 + SSOT sync

---

### v1.1 — 2026-05-15 KST
**변경 유형**: OPT-STR-01 v2.0 등록 + OPT-STR-04 통합 프레임워크 신규

#### OPT-STR-01 v2.0
- **프레임워크**: MBB 콘설팅 (McKinsey MECE + BCG Matrix + Bain Value Chain) + Gates 차비학
- **특화**: M&A 리드오카니제이션 / 포트폴리오 분류 / 시장진입 순서
- **PE-3 목표**: 97/100

#### OPT-STR-04 v1.0 신규
- **프레임워크**: 통합 시나리오 플래닝 + 실행 로드맵
- **PE-3 목표**: 95/100
- **파일 크기**: 6.5KB (가장 큰 OPT-STR 파일)

---

### v1.0 — 2026-05-15 KST (추안 등록)
- **PE-STR-MASTER v1.0** 추안 등록
- 9-Layer MECE 통합 마스터 프롬프트 (17KB)
- PE-3 목표: 95/100
- README.md + PROMPT_VERSION_HISTORY.md v1.0 생성

---

### 구 이력 연속성 노트 (2026-05-05 이전)

> 아래 항목들은 시스템 마이그레이션 이전(PE-STRAT 시대)의 기록이며, 현 PE-STR SSOT와는 도메인 체계가 다릅니다. 참고용으로 보존.

| ID | 파일 | PE-3 Before | PE-3 After | 버전 |
|---|---|---|---|---|
| PE-STRAT-ORCH | `pe_strat_orchestrator_v3.0.md` | 68 | 96 | v3.0 |
| PE-STRAT-01 | `pe_strat_01_v2.0.md` | 71 | 93 | v2.0 |
| PE-STRAT-02 | `pe_strat_02_investment_v1.0.md` | — | 94 | v1.0 |

---

## 🔗 연계 시스템

| 시스템 | 연결 경로 |
|---|---|
| Notion PE-STR Hub | https://www.notion.so/36155ed436f0811c8b5dca10d7317b8d |
| Notion OPT-STR-01 | https://www.notion.so/36155ed436f08132b8aff0e96ad389cd |
| Notion OPT-STR-04 | https://www.notion.so/36155ed436f0813db601cd7924a9655e |
| Notion OPT-STR-05 | https://www.notion.so/36255ed436f0811db316ece28518c05b |
| PE-1 자동개선 | 입력 최적화 루프 적용 |
| PE-2 자동증식 | 도메인별 변형 버전 생성 |
| PE-3 자동검증 | 5차원 품질 체점 (목표 93+) |
| PE-SEMI 도메인 | OPT-STR-03/05 연계 (반도체 해자) |
| PE-DD 도메인 | OPT-STR-02/05 연계 (Kill+해자 향상) |
| PE-FIN 도메인 | OPT-STR-05 L6 연계 (ROIC/WACC 해자증거) |

---

## ⚠️ 오류 예방 체크리스트 (PE-STR 전용)

| # | 검증 항목 | 기준 | 담당 엔진 |
|---|---|---|---|
| 1 | SSOT 정합성 | GitHub SHA × Notion PageID 실제 확인 | 수동 확인 |
| 2 | 라우터 코버리지 | 전체 OPT-STR ID 랠답 | ROUTER 체크 |
| 3 | PE-3 점수 미달 발생시 | PE-1 자동개선 루프 | PE-1 엔진 |
| 4 | 단축명령 중복 없음 | 키워드 독점성 확인 | 수동 확인 |
| 5 | Notion 동기화 | 등록 후 24시간 이내 | 수동 확인 |
| 6 | Temperature 범위 | 0.0 ≤ T ≤ 0.3 (전략 도메인) | PE-1 파라미터 검증 |
