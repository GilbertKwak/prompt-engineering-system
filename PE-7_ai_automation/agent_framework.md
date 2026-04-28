# PE-7 AI Automation Agent Framework v1.0
> SSOT Reference: Workspace Master Directory Hub  
> Linked: PE-3 Hub | Deep Prompt v2.0 | Prompt Engineering Hub v2.0  
> Version: 1.0.0 | Created: 2026-04-28  

---

## 에이전트 계층 구조 (3-Layer Architecture)

### Layer 0: Orchestrator Agent
- **역할**: 전체 작업 분배 및 병렬 실행 조율
- **입력**: Master Prompt → Task Decomposition
- **출력**: Section별 Sub-Agent 할당
- **오류 처리**: PE-7 사전 예측 → 대안 경로 자동 전환

### Layer 1: Analysis Agents (병렬 실행)

| Agent ID | Domain | Input Source | Output Target | Priority |
|----------|--------|--------------|---------------|----------|
| A-01 | HBM/반도체 | FU-Series Reports | Notion DB | 🔴 P1 |
| A-02 | Thermal | CFD/FEA Data | GitHub + Notion | 🔴 P1 |
| A-03 | sCO2/Energy | B-Star Strategy | JV Fund Analysis | 🔴 P1 |
| A-04 | AI Infra | Market Intelligence | Executive Reports | 🟡 P2 |
| A-05 | JV Fund | Global JV Master Prompt | Investment Memo | 🟡 P2 |

### Layer 2: Validation Agents

| Agent ID | Function | Rules Applied | Trigger |
|----------|----------|---------------|---------|
| V-01 | PE-1 Validator | 출처/수치 검증 | 항상 실행 |
| V-02 | PE-3 Checker | 반대 시나리오 | 항상 실행 |
| V-03 | PE-7 Error Predictor | 오류 사전 예측 | 실행 전 |
| V-04 | Auto-Corrector | 오류 수정 실행 | 검증 실패 시 |

### Layer 3: Output Agents

| Agent ID | Function | Destination | Format |
|----------|----------|-------------|--------|
| O-01 | Notion Sync | 지정 Notion 페이지 | MD |
| O-02 | GitHub Commit | 자동 커밋/PR 생성 | MD/PY/YML |
| O-03 | Report Generator | DOCX/MD 출력 | DOCX+MD |
| O-04 | Alert System | 오류 알림 + 대안 제시 | GitHub Issue |

---

## 실행 흐름 (Execution Flow)

```
Input
  └─► Orchestrator (Layer 0)
        ├─► A-01 (HBM)     ─┐
        ├─► A-02 (Thermal)  ├─► 병렬 실행
        ├─► A-03 (sCO2)    ─┘
        │
        ├─► V-01 (PE-1 검증) ─┐
        ├─► V-02 (PE-3 검증)  ├─► 검증 레이어
        ├─► V-03 (오류 예측)  |
        └─► V-04 (자동 수정) ─┘
              │
              ├─► O-01 (Notion)
              ├─► O-02 (GitHub)
              └─► O-03 (Report)
```

---

## 에러 처리 원칙 (PE-7 Error Handling Protocol)

### Phase 1: 사전 예측 (Pre-Execution)
- 입력 파라미터 완전성 검사
- 도메인 컨텍스트 매칭 확인
- 리스크 스코어 계산 (0.0~1.0)
- 스코어 ≥ 0.7 → 대안 경로 자동 준비

### Phase 2: 사전 검증 (Pre-Validation)
- Dry-run 실행 → 예상 출력 검토
- PE-1/PE-3 체크리스트 사전 확인
- 대안 에이전트 대기 상태 설정

### Phase 3: 실시간 수정 (Auto-Correction)
- 오류 발생 시 `correction_prompt` 자동 생성
- 최대 3회 재시도 (max_retry: 3)
- 3회 실패 시 → GitHub Issue 자동 생성 + 알림

### Phase 4: 병렬 백업 (Parallel Fallback)
- 주 경로 실패 시 백업 에이전트 즉시 전환
- 데이터 손실 없이 재개 (checkpoint 저장)

---

## 도메인별 에이전트 설정

### HBM/반도체 (A-01)
```yaml
agent_id: A-01
domain: HBM
sources:
  - FU-Series Reports (FU-001 ~ FU-025+)
  - HBM-Salvage-Value-Program
  - SK Hynix / Micron / Samsung 공식 자료
validation: PE-1 (출처 필수) + PE-3 (시나리오 2개 이상)
output_format: Notion MD + GitHub MD
```

### sCO2/에너지 (A-03)
```yaml
agent_id: A-03
domain: sCO2
sources:
  - B-Star-eCO2-Strategy
  - sCO2-Hub-IR-Docs
  - 국내외 sCO2 터빈 연구 논문
validation: PE-1 + JV 구조 검증
output_format: Investment Memo MD
```

### JV Fund (A-05)
```yaml
agent_id: A-05
domain: JV
sources:
  - Global JV Fund Master Prompt v3
  - 반도체/에너지 M&A 시장 데이터
validation: PE-1 + PE-3 + 법적 구조 검토
output_format: 3-tier Investment Memo (KR+EN)
```

---

## 연동 시스템

| 시스템 | 연결 방식 | 동기화 주기 |
|--------|----------|------------|
| Notion | API (notion_sync.py) | Push 시 자동 |
| GitHub Actions | pe7_parallel.yml | Push + Cron |
| PE-3 Hub | Import 참조 | 실시간 |
| Deep Prompt v2.0 | 직접 호출 | 실행 시 |

---

## 버전 히스토리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v1.0.0 | 2026-04-28 | 최초 생성 — 3-Layer 아키텍처 설계 |

---
*Linked Repository: [prompt-engineering-system](https://github.com/GilbertKwak/prompt-engineering-system)*  
*SSOT Hub: Workspace Master Directory Hub (Notion)*
