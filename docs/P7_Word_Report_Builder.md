# P7 — Word 보고서 자동 생성 운영 문서

> **PE-7 프로젝트 | P 시리즈 단계 7**  
> ExaFLOPS TCO 분석 결과를 Word(.docx) 보고서로 자동 생성하는 파이프라인

---

## 1. 개요

| 항목 | 내용 |
|------|------|
| 목적 | P6 ExaFLOPS TCO 데이터 → DOCX 빌드 |
| 생성 방식 | **AI 터미널(Perplexity) 직접 생성** 또는 로컈 `python docx_report_builder.py` |
| GitHub Actions | ❌ 사용 안 함 — 로컈/AI 단만 생성 |
| 천기 | 한국어(기본) / 영문(`--lang en`) |
| 섹션 | 커버 · 목차 · Exec Summary · TCO 결과 · 민감도 · 포트폴리오 · 결론 · 부록 |

---

## 2. 파일 구조

```
plugins/finance/
├── docx_report_builder.py    # 메인 빌더 (로컈 실행 전용)
└── p7_report_config.yaml     # 섹션·스타일 설정

docs/
└── P7_Word_Report_Builder.md  # 본 운영 문서

output/  (로컈 생성 시)
└── PE7_ExaFLOPS_TCO_Report_YYYYMMDD.docx
```

---

## 3. 설치

```bash
pip install python-docx pyyaml
```

---

## 4. 실행 명령어

### 한국어 보고서 (기본)
```bash
cd plugins/finance
python docx_report_builder.py
# → PE7_ExaFLOPS_TCO_Report_20260426.docx
```

### 영문 보고서
```bash
python docx_report_builder.py --lang en
# → PE7_ExaFLOPS_TCO_Report_20260426_EN.docx
```

### 경로 지정
```bash
python docx_report_builder.py --out ~/Desktop/PE7_Report.docx
```

### Dry-run (검증만)
```bash
python docx_report_builder.py --dry-run
```

### AI 터미널 직접 생성 (Perplexity 권장)
```
Perplexity에서 직접 질의:
"PE-7 ExaFLOPS TCO Word 보고서 DOCX 직접 생성"
→ python-docx로 생성 후 다운로드 제연
```

---

## 5. 보고서 섹션 구성

| 순서 | 섹션 | 자동화 수준 |
|------|------|-------------|
| 1 | 커버 | 완전 자동 |
| 2 | 목차 | 완전 자동 |
| 3 | Executive Summary + KPI 테이블 | JSON 데이터 기반 |
| 4 | 방법론 (4-레이어 설명) | 하드코드 |
| 5 | 시스템 정의 (SYS_A/B/C) | 하드코드 |
| 6 | TCO 결과 테이블 (시스템별) | JSON 데이터 기반 |
| 7 | 민감도 분석 | 하드코드 |
| 8 | 포트폴리오 MOIC/IRR | JSON 데이터 기반 |
| 9 | 결론 및 권고 | 하드코드 |
| 10 | 부록 (파라미터 13종) | 하드코드 |

---

## 6. 생성 방식 비교

| 방식 | 장점 | 단점 |
|------|------|------|
| AI 터미널 (권장) | 즉시 다운로드, 환경 설치 불필요 | 환경에 의존하지 않음 |
| 로컈 실행 | 완전한 커스터마이징 | python-docx 설치 필요 |
| ~~GitHub Actions~~ | ~~자동화~~ | ❌ 사용 안 함 |

---

## 7. P 시리즈 연계

```
P3 smr_power_model.py
    │
    ▼
P6 exaflops_resource_model.py  →  output/p6_exaflops_tco.json
P5 exaflops_viz.py             →  output/p6_charts/*.png
    │
    ▼
P7 docx_report_builder.py      →  PE7_*.docx  (로컈 또는 AI 직접 생성)
```

---

## 8. 변경 이력

| 버전 | 날짜 | 내용 |
|------|------|------|
| v1.0 | 2026-04-26 | 최초 생성 — 4-레이어 TCO 자동 로컈 빌드 |
| v1.1 | 2026-04-26 | GHA 워크플로 제거 — AI 터미널 직접 생성 방식으로 전환 |
