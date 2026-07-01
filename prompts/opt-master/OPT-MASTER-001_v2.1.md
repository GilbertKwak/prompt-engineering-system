# OPT-MASTER-001 · 통합 자동처리 마스터 프롬프트 v2.1

**Gilbert PE System · 3-Engine Auto-Process Master**

| 항목 | 내용 |
|------|------|
| **프롬프트 ID** | OPT-MASTER-001 |
| **버전** | v2.1 |
| **생성일** | 2026-07-01 |
| **도메인** | 반도체·AI·금융터미널·글로벌 인텔리전스 |
| **연계 엔진** | PE-1 자동개선 · PE-2 자동증식 · PE-3 자동검증 |
| **합격 기준** | 전 항목 ≥ 85점 / 총점 ≥ 440점 |
| **Temperature** | 검증·개선 0.0 / 증식 0.3 |
| **Notion SSOT** | https://app.notion.com/p/39055ed436f081b9a7a0ced964cb7b8a |
| **KG Node** | OPT-MASTER-001 · v2.1 · 2026-07-01 |

---

## 3-Engine 통합 워크플로우

```
[사용자 초안 프롬프트 투입]
         ↓
┌─────────────────────────────────────┐
│  ENGINE 1: 자동검증 (PE-3 기준)      │
│  5차원 채점 → 약점 목록 출력          │
│  합격(≥440) → ENGINE 3 직행          │
│  미달 → ENGINE 2 자동 진입            │
└──────────────┬──────────────────────┘
               ↓ (미달 시)
┌─────────────────────────────────────┐
│  ENGINE 2: 자동개선 (PE-1 기준)      │
│  약점 항목별 재작성 루프 max 3회      │
│  완료 → ENGINE 1 재채점              │
└──────────────┬──────────────────────┘
               ↓ (합격 후)
┌─────────────────────────────────────┐
│  ENGINE 3: 자동증식 (PE-2 기준)      │
│  5개 표준 변형 버전 자동 생성         │
│  V1 분석형 / V2 실행형               │
│  V3 모니터링형 / V4 보고서형          │
│  V5 연동형(Notion+GitHub)            │
└──────────────┬──────────────────────┘
               ↓
  [최종 검증 완료 프롬프트 라이브러리]
  GitHub 커밋 + Notion 저장 자동 실행
```

---

## 마스터 프롬프트 전문

```
═══════════════════════════════════════════════════════════
GILBERT PE SYSTEM · 3-ENGINE AUTO-PROCESS MASTER v2.1
═══════════════════════════════════════════════════════════

[ROLE]
당신은 Gilbert의 프롬프트 엔지니어링 시스템(PE v6.4)에
통합된 선임 프롬프트 최적화 에이전트입니다.
도메인: 반도체·AI·금융·글로벌 인텔리전스

[INPUT]
{{USER_PROMPT_DRAFT}}  ← 대상 프롬프트 초안 삽입

[ENGINE 1: 자동검증 — PE-3 기준]
다음 5차원으로 0-100 채점 후 약점 목록 출력:
① Clarity(명확성):      모호어·중의어 탐지
② Structure(구조성):    ROLE→CONTEXT→TASK→FORMAT 완결성
③ Specificity(특이성):  도메인·수치·기준 명시도
④ Actionability(실행가능성): 즉시 실행 가능한 출력 명세
⑤ Ecosystem-Fit(생태계 적합성): Notion·GitHub·KG 연동성

합격 기준: 전 항목 ≥ 85점 / 총점 ≥ 440점
미달 시 → ENGINE 2 자동 진입

[ENGINE 2: 자동개선 — PE-1 기준]
약점 항목별 재작성 루프 (max 3회):
- 모호어       → 구체 동사·수치로 교체
- 구조 누락    → [ROLE][CONTEXT][TASK][OUTPUT][CONSTRAINTS] 보완
- 특이성 부족  → Gilbert 도메인 컨텍스트 주입
  (반도체 공급망 / 글로벌 AI 생태계 / Financial Terminal KR)
- 생태계 부적합 → Notion DB 링크·GitHub 커밋 명령 추가

루프 종료 조건: 합격 기준 달성 OR 3회 도달
3회 후 미달 시: 미달 차원 명시 + 수동 검토 요청

[ENGINE 3: 자동증식 — PE-2 기준]
검증 완료 프롬프트를 다음 5개 변형으로 확장:
V1: 분석형    (심층 원인 추적 / Pearl DAG)
V2: 실행형    (즉시 액션 플랜 / OKR 매핑)
V3: 모니터링형 (주간 자동 점검 / KPI 알림)
V4: 보고서형  (Executive Summary / KR+EN 양언어)
V5: 연동형    (Notion API + GitHub CI 자동화)

[OUTPUT FORMAT]
## 검증 점수표
| 차원 | Before | After | 개선폭 |
|------|--------|-------|--------|
| Clarity          | _ | _ | _ |
| Structure        | _ | _ | _ |
| Specificity      | _ | _ | _ |
| Actionability    | _ | _ | _ |
| Ecosystem-Fit    | _ | _ | _ |
| **총점**         | _ | _ | _ |

## 최적화 프롬프트 (V1~V5)
각 변형 버전 전문 출력

## GitHub 저장 명령어
git add prompts/[도메인]/[ID]_v[버전].md
git commit -m "feat(prompt): [ID] auto-optimized via 3-Engine v2.1"
git push origin main

## Notion 저장 위치
[추천 페이지 링크 + DB 속성값]

[CONSTRAINTS]
- Temperature: 검증·개선 0.0 / 증식 0.3
- 한글 우선, 기술 용어 EN 병기
- Gilbert KG (Knowledge Graph) v6.3 메타데이터 준수
- 매 루프 종료 후 PE-3 재채점 필수
- 기존 프롬프트 ID 체계 완전 계승 (OPT-/PE-/PROMPT_ 접두사)
═══════════════════════════════════════════════════════════
```

---

## 전체 활용 명령어

### 신규 프롬프트 투입 (원스텝)
```
[OPT-MASTER-001 v2.1 실행]
대상 프롬프트: {{여기에 초안 붙여넣기}}
→ ENGINE 1 자동검증 → ENGINE 2 자동개선 → ENGINE 3 자동증식
→ V1~V5 변형 출력 + GitHub 커밋 명령 + Notion 저장 위치 출력
```

### 기존 프롬프트 재검증
```
[PE-3 재채점 요청]
대상: [프롬프트 ID]
기준: OPT-MASTER-001 v2.1 5차원
출력: 점수표 + 개선 권고사항
```

### 주간 생태계 동기화
```bash
bash ~/prompt-engineering-system/automation/weekly_sync.sh
# → Notion 신규 페이지 감지 → GitHub 자동 커밋 → KG 업데이트
```

### GitHub 업데이트 (버전 업 시)
```bash
# STEP 1 — 파일 수정
vi ~/prompt-engineering-system/prompts/opt-master/OPT-MASTER-001_v2.1.md

# STEP 2 — KG 업데이트
python automation/kg_updater.py \
  --add-node OPT-MASTER-001 \
  --version 2.2 \
  --domain "opt-master"

# STEP 3 — 커밋 & 푸시
git -C ~/prompt-engineering-system add prompts/opt-master/
git -C ~/prompt-engineering-system commit \
  -m "feat(prompt): OPT-MASTER-001 v2.2 — [변경 요약]"
git -C ~/prompt-engineering-system push origin main
```

---

## 기존 vs 최적화 성능 비교

| 비교 항목 | 기존 PE-1~3 분리 실행 | OPT-MASTER-001 통합 | 우위 |
|-----------|----------------------|---------------------|------|
| 자동화 수준 | 3-Engine 수동 순차 호출 | 단일 명령 통합 실행 | ✅ 최적화 |
| 도메인 특화 | 반도체·AI 중심 | 금융터미널·KR 투자자 추가 | ✅ 최적화 |
| 생태계 연동 | GitHub 링크 수동 삽입 | 커밋 명령 자동 생성 | ✅ 최적화 |
| 증식 다양성 | 3~4종 변형 | 5종 표준 변형 | ✅ 최적화 |
| 합격 기준 | 미명시 | ≥85점 / 총점≥440 명시 | ✅ 최적화 |
| KG 연동 | 별도 실행 | 프롬프트 내 자동 삽입 | ✅ 최적화 |
| 성숙도 | 실검증 데이터 축적 | 신규, 실사용 검증 필요 | ✅ 기존 |
| 특화 깊이 | 도메인별 세밀 커스터마이징 | 공통화로 일부 희생 | ✅ 기존 |

### PE-DEEP 실적 기반 기대 성과

| 차원 | Before 평균 | OPT After 예상 | 개선폭 |
|------|-------------|----------------|--------|
| Clarity | 73 | 94 | +21 |
| Structure | 75 | 95 | +20 |
| Specificity | 68 | 93 | +25 |
| Actionability | 65 | 92 | +27 |
| Ecosystem-Fit | 60 | 91 | +31 |
| **총점** | **341** | **465** | **+124** |

---

## 연계 문서

| 구분 | 링크 |
|------|------|
| Notion 저장 위치 | https://app.notion.com/p/39055ed436f081b9a7a0ced964cb7b8a |
| PE System Mother Page v6.4 | https://app.notion.com/p/34a55ed436f0814d9cffe6a2f0816e29 |
| 자동개선·자동증식·자동검증 허브 v2.0 | https://app.notion.com/p/33955ed436f081cc9f0bd014d631aa7b |
| C-38 PE-INTEL Market Intelligence | https://app.notion.com/p/36855ed436f08192a4d0ce8054028be9 |
| Financial Terminal 최적화 프롬프트 허브 | https://app.notion.com/p/36f55ed436f081f5b875c0320816901c |
| GitHub SSOT | https://github.com/GilbertKwak/prompt-engineering-system |

---

## 변경 이력

| 버전 | 날짜 | 변경 내용 | 작성자 |
|------|------|-----------|--------|
| v2.1 | 2026-07-01 | 최초 통합 마스터 생성 / Financial Terminal 도메인 추가 / 합격 기준 명시 / 5종 증식 표준화 | Gilbert PE System |
