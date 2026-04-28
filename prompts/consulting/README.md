# 🏢 PE-CON 컨설팅 전략 프롬프트 라이브러리

> **GitHub SSOT 경로**: `prompts/consulting/`  
> **Notion 연계**: [PE Hub v2.0](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b) → Workspace SSOT T-04  
> **PE-3 목표 점수**: ≥ 90점 (v1.0 기준 평균 75점 → +15pts 달성 목표)  
> **최초 생성**: 2026-04-28 | **관리자**: Gilbert Kwak  

---

## 📁 디렉토리 구조

```
prompts/consulting/
├── README.md                          ← 본 문서 (표준화 명세 SSOT)
├── PROMPT_VERSION_HISTORY.md          ← 버전 이력 (C-시리즈 전체)
├── c001_china_market_risk_v2.0.md     ← C-001: 중국 시장 리스크 분석
├── c002_furiosaai_china_risk_v2.0.md  ← C-002: FuriosaAI 중국 리스크
├── c003_furiosaai_competitive_v2.0.md ← C-003: FuriosaAI 경쟁 분석
├── c004_furiosaai_us_entry_v2.0.md    ← C-004: FuriosaAI 미국 진출 전략
├── c005_generic_us_entry_v2.0.md      ← C-005: 범용 미국 시장 진출 전략
└── bain-system/                       ← Bain System 전략 컨설팅 마스터 프롬프트
    └── bain_system_prompt.md
```

---

## 📋 프롬프트 인덱스 (C-시리즈 + Bain System)

| ID | 파일명 | 제목 | 버전 | PE-3 점수 | 상태 |
|---|---|---|---|---|---|
| **C-001** | `c001_china_market_risk_v2.0.md` | 중국 시장 리스크 분석 | v2.0 | — | 🟢 Active |
| **C-002** | `c002_furiosaai_china_risk_v2.0.md` | FuriosaAI 중국 사업 리스크 | v2.0 | — | 🟢 Active |
| **C-003** | `c003_furiosaai_competitive_v2.0.md` | FuriosaAI 경쟁 구도 분석 | v2.0 | — | 🟢 Active |
| **C-004** | `c004_furiosaai_us_entry_v2.0.md` | FuriosaAI 미국 진출 전략 | v2.0 | — | 🟢 Active |
| **C-005** | `c005_generic_us_entry_v2.0.md` | 범용 미국 시장 진출 전략 | v2.0 | — | 🟢 Active |
| **C-BAIN** | `bain-system/bain_system_prompt.md` | Bain System 전략 마스터 | v1.0 | — | 🟢 Active |

> PE-3 점수는 3-Engine 검증 실행 후 갱신. 목표: 전 항목 ≥ 90점.

---

## 🏷️ 네이밍 컨벤션

### 파일명 규칙
```
{id}_{slug}_{version}.md

예시:
  c001_china_market_risk_v2.0.md
  c006_new_topic_v1.0.md
```

### 규칙 상세
| 항목 | 규칙 | 예시 |
|---|---|---|
| **ID** | 소문자 `c` + 3자리 숫자 | `c001`, `c006` |
| **Slug** | 소문자 영문, 언더스코어 구분 | `china_market_risk` |
| **버전** | `v{major}.{minor}` | `v2.0`, `v1.1` |
| **확장자** | `.md` (Markdown) | |
| **서브디렉토리** | 시스템 단위 분리 시만 허용 | `bain-system/` |

### 버전 업 기준
- `Major (+1.0)`: 프롬프트 구조 전면 개편, 역할 재정의
- `Minor (+0.1)`: 섹션 추가·수정, 체인 로직 변경
- `Patch (+0.0.1)`: 오타 수정, 표현 다듬기

---

## 🔗 PE-7 × PE-CON × PE-10 크로스 연계 구조

```
[PE-CON 프롬프트 라이브러리]
  prompts/consulting/ (C-001~C-005 + Bain)
         |
         ↓  PE-7 자동화 파이프라인 (pe_con_automation.py)
  ┌──────────────────────────────────────┐
  │  PE-1 자동개선  →  PE-2 자동증식     │
  │        →  PE-3 자동검증 (≥ 90점)    │
  └──────────────────────────────────────┘
         |
         ↓  검증 PASS 시
  [PE-10 컨설팅 프로젝트 추적 DB]
  (Notion 크로스 연계 자동 등록)
         |
         ↓  SHA 동기화
  [GitHub SSOT] ← 본 디렉토리
```

### 연계 파일 매핑
| 연계 대상 | 경로 / URL | 역할 |
|---|---|---|
| PE-7 자동화 스크립트 | `automation/pe_con_automation.py` | 3-Engine 실행 진입점 |
| PE-3 검증 룰셋 | `validation/pe3_rules.yaml` | 5차원 채점 기준 |
| PE-10 Notion DB | [PE Hub v2.0](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b) | 결과물 추적 |
| SSOT 버전 이력 | `prompts/consulting/PROMPT_VERSION_HISTORY.md` | 이 디렉토리 변경 이력 |

---

## ✅ PE-3 검증 기준 (5차원)

| 차원 | 기준 | 가중치 | 합격 기준 |
|---|---|---|---|
| **1. 명확성** | 역할·목표·출력 형식 완전 명시 | 25% | ≥ 22점 / 25점 |
| **2. 구체성** | 추상 표현 없음, 실행 가능 수준 | 25% | ≥ 22점 / 25점 |
| **3. 근거 추적** | 수치 출처 최소 3개 명시 | 20% | ≥ 18점 / 20점 |
| **4. 반대 시나리오** | 반대 케이스 1개 이상 포함 | 15% | ≥ 13점 / 15점 |
| **5. 출력 구조** | JSON / 테이블 / 트리 등 구조화 | 15% | ≥ 13점 / 15점 |
| **합계** | | **100%** | **≥ 90점 (PASS)** |

> 미달 시 PE-1 자동개선 루프 재실행 (max 3회)

---

## 🚨 E-0N 연계 규칙

| 코드 | 감지 조건 | 자동 처리 |
|---|---|---|
| **E-07** | KPI 섹션 또는 리스크 섹션 누락 | 템플릿 자동 삽입 |
| **E-09** | PE-CON 파일 누락 (인덱스 ≠ 실제 파일) | 경고 로그 + GitHub Issue 생성 |
| **E-04** | Notion ↔ GitHub 구조 불일치 | 구조 diff 리포트 생성 |
| **E-01** | SHA 불일치 | SHA 자동 갱신 |

---

## 🔄 GitHub SSOT ↔ Notion 동기화 정책

| 항목 | 정책 |
|---|---|
| **Primary SSOT** | GitHub (`prompts/consulting/`) |
| **Notion 역할** | 열람·참조용 미러 (편집은 GitHub에서) |
| **동기화 주기** | GitHub Actions `pe7_daily_pipeline.yml` — KST 08:00 자동 실행 |
| **수동 동기화** | `python automation/notion_sync.py --dir prompts/consulting` |
| **충돌 해결** | GitHub 버전 우선 (Notion 덮어쓰기) |
| **버전 이력 관리** | `PROMPT_VERSION_HISTORY.md` 단일 파일에 전체 이력 기록 |

---

## 📝 새 프롬프트 추가 가이드

1. **파일 생성**: 네이밍 컨벤션 준수 (`c{NNN}_{slug}_v1.0.md`)
2. **필수 헤더** 포함:
   ```markdown
   ---
   id: C-NNN
   title: 프롬프트 제목
   version: v1.0
   created: YYYY-MM-DD
   pe3_score: null  # 검증 전
   status: Draft
   ---
   ```
3. **PE-3 검증 실행**: `python automation/pe_con_automation.py --id C-NNN`
4. **인덱스 업데이트**: 본 README의 프롬프트 인덱스 테이블 갱신
5. **PROMPT_VERSION_HISTORY.md** 에 신규 항목 추가
6. **커밋 메시지 규칙**: `feat(consulting): [C-NNN] 프롬프트명 v1.0 신규 등록 | PE-3 PASS`

---

## 📊 버전 이력

| 버전 | 날짜 | 내용 |
|---|---|---|
| **v1.0** | 2026-04-28 | 최초 생성 — 디렉토리 표준화 명세, 네이밍 컨벤션, PE-3 기준, E-0N 연계 규칙, SSOT 동기화 정책, 기여 가이드 확립 (Phase D) |

---

> **관련 문서**  
> - [PE Hub v2.0 (Notion)](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b)  
> - [PE-7 AI 자동화 설계 v2.0 (Notion)](https://www.notion.so/34955ed436f081149dd6de25dba027d7)  
> - [PROMPT_VERSION_HISTORY.md](./PROMPT_VERSION_HISTORY.md)
