# P7 — Word 보고서 자동 생성 운영 문서

> **PE-7 프로젝트 | P 시리즈 단계 7**  
> ExaFLOPS TCO 분석 결과를 Word(.docx) 보고서로 자동 생성하는 파이프라인

---

## 1. 개요

| 항목 | 내용 |
|------|------|
| 목적 | P6 ExaFLOPS TCO 데이터 + P5 차트 5개 → DOCX 자동 빌드 |
| 입력 | `output/p6_exaflops_tco.json`, `output/p6_charts/*.png` |
| 출력 | `output/reports/PE7_ExaFLOPS_TCO_Report_YYYYMMDD.docx` |
| 언어 | 한국어(기본) / 영문(`--lang en`) |
| 섹션 | 커버 · 목차 · Executive Summary · TCO 결과 · 차트 · 결론 · 부록 |

---

## 2. 파일 구조

```
plugins/finance/
├── docx_report_builder.py    # 메인 빌더 (≈550 LOC)
├── p7_report_config.yaml     # 섹션·스타일·차트 설정
└── templates/
    └── (옵션) 커스텀 DOCX 템플릿

docs/
└── P7_Word_Report_Builder.md  # 본 운영 문서

.github/workflows/
└── pe7_p7_report.yml          # GitHub Actions 자동 빌드 워크플로

output/
├── p6_exaflops_tco.json       # P6 TCO 데이터 (입력)
├── p6_charts/                 # P5/P6 차트 PNG (입력)
│   ├── tco_heatmap.png
│   ├── moic_grouped_bar.png
│   ├── moic_delta_bar.png
│   ├── moic_waterfall.png
│   └── irr_moic_bubble.png
└── reports/                   # 출력
    ├── PE7_ExaFLOPS_TCO_Report_YYYYMMDD.docx
    ├── PE7_ExaFLOPS_TCO_Report_YYYYMMDD_EN.docx
    └── build_manifest.json
```

---

## 3. 설치

```bash
# 의존성 설치
pip install python-docx>=0.8.11 pyyaml>=6.0 openpyxl>=3.1.0

# 또는 프로젝트 루트에서
pip install -r requirements.txt
```

---

## 4. 실행 명령어

### 기본 실행 (한국어 보고서)
```bash
cd plugins/finance
python docx_report_builder.py
```

### 영문 보고서
```bash
python docx_report_builder.py --lang en
```

### 특정 시스템만 포함
```bash
python docx_report_builder.py --system SYS_C
```

### 특정 시나리오만
```bash
python docx_report_builder.py --scenario smr_full
```

### Dry-run (검증만, 파일 미생성)
```bash
python docx_report_builder.py --dry-run
```

### 커스텀 출력 경로
```bash
python docx_report_builder.py --output /path/to/my_report.docx
```

### 전체 빌드 (KR + EN 동시)
```bash
python docx_report_builder.py --lang ko && python docx_report_builder.py --lang en
```

---

## 5. 보고서 섹션 구성

| 섹션 | 내용 | 자동화 수준 |
|------|------|-------------|
| 커버 | 제목·날짜·메타 테이블 | 완전 자동 |
| 목차 | 8개 섹션 + 부록 | 완전 자동 |
| Executive Summary | KPI 3종 요약 테이블 | JSON 데이터 기반 |
| 방법론 (§2) | 4-레이어 모델 설명 | 설정 기반 |
| 시스템 정의 (§3) | SYS_A/B/C 사양 | YAML 기반 |
| TCO 결과 (§4) | 시스템별 × 시나리오 테이블 | JSON 데이터 기반 |
| 민감도 (§5) | CAPEX ±20% 충격 분석 | JSON 데이터 기반 |
| 포트폴리오 (§6) | MOIC/IRR 요약 | JSON 데이터 기반 |
| 차트 (§7) | PNG 5개 자동 삽입 + 캡션 | 파일 감지 자동 |
| 결론 (§8) | 3개 권고사항 | 설정 기반 |
| 부록 | 파라미터 13종 테이블 | YAML 기반 |

---

## 6. GitHub Actions 자동 빌드

워크플로: `.github/workflows/pe7_p7_report.yml`

### 트리거
- **자동**: P6 모델 실행 완료 후 (`pe7_smr_pipeline.yml` 완료 시)
- **수동**: `workflow_dispatch` (GitHub UI 또는 CLI)

### 수동 트리거
```bash
# 한국어 보고서
gh workflow run pe7_p7_report.yml -f lang=ko

# 영문 보고서
gh workflow run pe7_p7_report.yml -f lang=en

# 양쪽 모두
gh workflow run pe7_p7_report.yml -f lang=both
```

### 아티팩트
- 빌드 완료 후 `.docx` 파일이 GitHub Actions 아티팩트로 7일간 보관
- Notion 업로드: `notion_chart_uploader.py` 연동 시 자동 업로드

---

## 7. 커스터마이징

### 섹션 ON/OFF
`p7_report_config.yaml`에서 `enabled: false` 설정:
```yaml
sections:
  - id: methodology
    enabled: false  # 해당 섹션 제외
```

### 스타일 변경
```yaml
style:
  brand_blue: "2C5F8A"   # 헤더·강조 색상
  chart_width_inches: 5.8  # 차트 너비 조정
```

### 차트 추가
```yaml
charts:
  - key: new_chart
    filename: new_chart.png
    figure_no: "7-6"
    caption_ko: "새 차트 설명"
    width_inches: 5.8
```

---

## 8. 의존성

| 패키지 | 버전 | 용도 |
|--------|------|------|
| python-docx | ≥0.8.11 | DOCX 생성 |
| pyyaml | ≥6.0 | 설정 로드 |
| openpyxl | ≥3.1.0 | Excel 데이터 읽기 |

---

## 9. 변경 이력

| 버전 | 날짜 | 내용 |
|------|------|------|
| v1.0 | 2026-04-26 | 최초 생성 — 4-레이어 TCO + 차트 5개 자동 삽입 |

---

## 10. P 시리즈 연계

```
P3 smr_power_model.py
        │
        ▼
P6 exaflops_resource_model.py  →  output/p6_exaflops_tco.json
P5 exaflops_viz.py             →  output/p6_charts/*.png
        │
        ▼
P7 docx_report_builder.py      →  output/reports/PE7_*.docx
        │
        ▼
P4 GitHub Actions              →  자동 빌드 + 아티팩트 업로드
```
