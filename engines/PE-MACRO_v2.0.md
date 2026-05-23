# PE-MACRO v2.0 — 엔진 매크로 오케스트레이션 매니페스트

> **SSOT 기준 문서** | T-09 전체 엔진 시스템의 통합 실행 명세  
> 최종 업데이트: 2026-05-23 | 상태: ✅ 운영 중

---

## 1. 개요

이 문서는 `engines/` 디렉토리 하위 3개 핵심 엔진(PE-1, PE-2, PE-3)의
**통합 실행 순서, CMD 명령어, 의존성 그래프, Notion 연동 경로**를 단일 SSOT로 정의합니다.

```
engines/
├── PE-1_auto-refinement/      # 자동개선 엔진
├── PE-2_auto-proliferation/   # 자동증식 엔진
├── PE-3_auto-validation/      # 자동검증 엔진
├── PE-7_ai-automation-design/ # AI 자동화 설계 엔진
└── PE-MACRO_v2.0.md           # ← 현재 문서 (오케스트레이션 매니페스트)
```

---

## 2. 엔진 등록부

| 엔진 ID | 이름 | 디렉토리 경로 | 상태 | Notion 페이지 |
|---------|------|--------------|------|---------------|
| PE-1 | 자동개선 (Auto-Refinement) | `engines/PE-1_auto-refinement/` | ✅ 운영 중 | T-09 > PE-1 |
| PE-2 | 자동증식 (Auto-Proliferation) | `engines/PE-2_auto-proliferation/` | ✅ 운영 중 | T-09 > PE-2 |
| PE-3 | 자동검증 (Auto-Validation) | `engines/PE-3_auto-validation/` | ✅ 운영 중 | T-09 > PE-3 |
| PE-7 | AI 자동화 설계 | `engines/PE-7_ai-automation-design/` | 🔄 개발 중 | T-09 > PE-7 |

---

## 3. 실행 순서 (Execution Pipeline)

```
[TRIGGER]
    │
    ▼
┌─────────────────────────────┐
│  STEP 1: PE-1 자동개선      │  프롬프트 품질 향상 · 개선안 생성
│  pe-refine --target all     │
└────────────┬────────────────┘
             │  개선된 프롬프트 세트
             ▼
┌─────────────────────────────┐
│  STEP 2: PE-2 자동증식      │  변형 프롬프트 대량 생성
│  pe-proliferate --source    │
│  ./refined/ --count 10      │
└────────────┬────────────────┘
             │  증식된 프롬프트 풀
             ▼
┌─────────────────────────────┐
│  STEP 3: PE-3 자동검증      │  품질 스코어링 · 필터링
│  pe-validate-all            │
│  --threshold 80             │
└────────────┬────────────────┘
             │  검증 통과 프롬프트
             ▼
┌─────────────────────────────┐
│  OUTPUT: Notion 동기화      │  SSOT DB 업데이트
│  notion-sync --engine all   │
└─────────────────────────────┘
```

---

## 4. CMD 명령어 레퍼런스

### 4-1. PE-1 자동개선

```bash
# 단일 프롬프트 개선
pe-refine --input ./prompts/<target>.md --output ./refined/

# 전체 프롬프트 배치 개선
pe-refine --target all --output ./refined/ --log ./logs/pe1_$(date +%Y%m%d).log

# 개선 강도 조정 (1=최소 / 5=최대)
pe-refine --target all --intensity 3
```

### 4-2. PE-2 자동증식

```bash
# 개선된 프롬프트 기반 증식 (기본 10개 변형)
pe-proliferate --source ./refined/ --count 10

# 도메인 특화 증식
pe-proliferate --source ./refined/ --domain semiconductor --count 20

# 시드 고정 재현 가능 증식
pe-proliferate --source ./refined/ --seed 42 --count 15
```

### 4-3. PE-3 자동검증

```bash
# 전체 검증 실행 (기본 임계값 80)
pe-validate-all --threshold 80

# 특정 디렉토리 대상 검증
pe-validate-all --input ./proliferated/ --threshold 85

# 상세 리포트 포함 검증
pe-validate-all --threshold 80 --report ./reports/validation_$(date +%Y%m%d).json

# 실패 항목 자동 PE-1 재처리 루프
pe-validate-all --threshold 80 --on-fail re-refine
```

### 4-4. 매크로 전체 파이프라인 실행

```bash
# 전체 파이프라인 원샷 실행
pe-macro run --all --threshold 80 --log ./logs/macro_$(date +%Y%m%d).log

# 드라이런 (실제 실행 없이 계획 출력)
pe-macro run --all --dry-run

# 특정 엔진만 선택 실행
pe-macro run --engines PE-1,PE-3 --threshold 80
```

---

## 5. 의존성 & 환경 설정

```yaml
# pe-macro.config.yaml
version: "2.0"
engines:
  pe1:
    path: engines/PE-1_auto-refinement/
    enabled: true
    intensity: 3
  pe2:
    path: engines/PE-2_auto-proliferation/
    enabled: true
    default_count: 10
  pe3:
    path: engines/PE-3_auto-validation/
    enabled: true
    threshold: 80
    on_fail: re-refine

pipeline:
  order: [pe1, pe2, pe3]
  stop_on_error: false
  notify_on_complete: true

notion:
  sync_enabled: true
  database_id: "${NOTION_T09_DB_ID}"
  status_property: "Status"
  active_value: "✅ 운영 중"

logging:
  dir: ./logs/
  level: INFO
  retention_days: 30
```

---

## 6. Notion ↔ GitHub SSOT 연동 매핑

| Notion 필드 | GitHub 경로 | 동기화 방향 |
|-------------|-------------|-------------|
| `Status` = ✅ 운영 중 | 각 엔진 `README.md` 상태 뱃지 | Notion → GitHub |
| `CMD` 코드블록 | 본 문서 §4 CMD 레퍼런스 | GitHub → Notion |
| `GitHub URL` | `engines/<ENGINE_DIR>/` | GitHub → Notion |
| `PE-Score` | `reports/validation_*.json` | GitHub → Notion |
| `Last Updated` | 최신 커밋 타임스탬프 | GitHub → Notion |

### Notion Child Page 직접 링크

- **PE-1 페이지**: Notion T-09 > PE-1(자동개선)
  - GitHub 연동: [`engines/PE-1_auto-refinement/`](https://github.com/GilbertKwak/prompt-engineering-system/tree/main/engines/PE-1_auto-refinement)
- **PE-2 페이지**: Notion T-09 > PE-2(자동증식)
  - GitHub 연동: [`engines/PE-2_auto-proliferation/`](https://github.com/GilbertKwak/prompt-engineering-system/tree/main/engines/PE-2_auto-proliferation)
- **PE-3 페이지**: Notion T-09 > PE-3(자동검증)
  - GitHub 연동: [`engines/PE-3_auto-validation/`](https://github.com/GilbertKwak/prompt-engineering-system/tree/main/engines/PE-3_auto-validation)

---

## 7. 품질 기준 (Quality Gates)

| 게이트 | 기준값 | 담당 엔진 | 실패 시 처리 |
|--------|--------|----------|-------------|
| 개선율 | ≥ 15% 향상 | PE-1 | 강도(intensity) +1 재실행 |
| 증식 다양성 | 유사도 < 0.85 | PE-2 | 시드 변경 재실행 |
| 검증 통과율 | PE-Score ≥ 80 | PE-3 | PE-1 재처리 루프 |
| 전체 파이프라인 | 통과율 ≥ 90% | 매크로 | Slack/Notion 알림 |

---

## 8. 변경 이력

| 버전 | 날짜 | 변경 내용 | 작성자 |
|------|------|----------|--------|
| v2.0 | 2026-05-23 | 초기 SSOT 매니페스트 생성 · T-09 SSOT 완성 | GilbertKwak |

---

## 9. 관련 문서

- [`engines/PE-1_auto-refinement/`](https://github.com/GilbertKwak/prompt-engineering-system/tree/main/engines/PE-1_auto-refinement) — PE-1 엔진 상세
- [`engines/PE-2_auto-proliferation/`](https://github.com/GilbertKwak/prompt-engineering-system/tree/main/engines/PE-2_auto-proliferation) — PE-2 엔진 상세
- [`engines/PE-3_auto-validation/`](https://github.com/GilbertKwak/prompt-engineering-system/tree/main/engines/PE-3_auto-validation) — PE-3 엔진 상세
- [`engines/PE-7_ai-automation-design/`](https://github.com/GilbertKwak/prompt-engineering-system/tree/main/engines/PE-7_ai-automation-design) — PE-7 엔진 상세

---

> 📌 **SSOT 원칙**: 이 파일이 엔진 실행 명세의 단일 진실 공급원입니다.  
> Notion Child Page의 CMD·GitHub URL·Status는 반드시 이 문서를 기준으로 동기화하십시오.
