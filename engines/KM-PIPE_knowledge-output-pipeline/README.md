# 🔄 KM-PIPE · Knowledge-to-Output Pipeline

**Version:** 3.0  
**Engine ID:** KM-PIPE  
**Status:** ✅ 운영 중  
**Notion Ref:** T-09 > PE-IP > KM-PIPE-MASTER-v3.0  
**KG Node:** KM-PIPE-001  

---

## Overview

KM-PIPE는 Gilbert의 프롬프트 엔지니어링 생태계에서  
**Raw Input → 구조화 지식 → Notion + Word + Chart 자동 출력**을 담당하는  
8-Agent 순차·병렬 파이프라인입니다.

```
Raw Input
  └─ A1 IngestAgent      → 데이터 정규화 + PARA 분류
      └─ A2 MemoryAgent  → KG 기존 노드 검색 + 중복 판단
          └─ A3 AnalysisAgent → 3줄 요약 + 핵심개념 + 인사이트
              └─ A4 KGAgent  → KG 노드 생성 + backlinks
                  ├─ A5 NotionAgent    ─┐
                  ├─ A6 DocumentAgent  ─┼─ 병렬 실행
                  ├─ A7 VizAgent       ─┘
                  └─ A8 ValidationAgent → PE-3 품질 검증
```

---

## Scripts

| 파일 | 에이전트 | 기능 |
|------|----------|------|
| `generate_word.py` | A6 DocumentAgent | Word .docx 자동 생성 (python-docx) |
| `generate_charts.py` | A7 VisualizationAgent | Tufte-styled 차트 생성 (matplotlib, 300dpi) |

---

## Installation

```bash
pip install python-docx matplotlib numpy networkx
```

---

## Quick Start

### Word 문서 생성

```bash
# Simple mode
python generate_word.py \
  --title "HBM Market Intelligence W21/2026" \
  --content "HBM3E 공급 타이트..." \
  --domain semiconductor \
  --output reports/hbm-w21.docx

# Full pipeline mode (KM-PIPE JSON)
python generate_word.py \
  --input pipeline_output.json \
  --output reports/weekly-intel.docx
```

### 차트 생성

```bash
# Quick mode (bar chart)
python generate_charts.py \
  --data '{"labels":["SK Hynix","Samsung","Micron"],"values":[42,35,23]}' \
  --type hbar \
  --title "HBM Market Share 2026" \
  --domain semiconductor \
  --output hbm_share.png

# Full pipeline mode
python generate_charts.py \
  --input pipeline_output.json \
  --output-dir charts/
```

---

## C-38 Weekly Intel Integration (권장 워크플로우)

```bash
# STEP 1 — PE-1 개선 실행
python ../PE-1_auto-refinement/pe1_refiner.py \
  --input ../../reports/c38-weekly.md --max-loops 2

# STEP 2 — Word + Chart 동시 생성
python generate_word.py --input pipeline_output.json --output reports/W21.docx
python generate_charts.py --input pipeline_output.json --output-dir charts/

# STEP 3 — Notion 동기화 + KG 업데이트
python ../../automation/notion_sync.py --page C-38 --append
python ../../automation/kg_updater.py --add-node KM-W21-2026 --version 6.3

# STEP 4 — Git commit
git add -A && git commit -m "feat: KM-PIPE W21/2026 — C-38 Intel 자동화 보고서"
```

---

## Linked Engines

| 엔진 | 연동 방식 |
|------|-----------|
| PE-1 자동개선 | 입력 텍스트 품질 개선 → KM-PIPE 입력 |
| PE-2 자동증식 | `pe2_proliferation_seeds` 필드 수신 |
| PE-3 자동검증 | A8 ValidationAgent에 PE-3 체크리스트 적용 |
| PE-7 AI 자동화 | 전체 파이프라인 오케스트레이션 |
| PE-11 Multi-Agent | 상위 호환 — KM-PIPE를 서브에이전트로 호출 |

---

## Output Formats

- **Word (.docx)**: Tufte-inspired clean layout, 300dpi image 삽입 지원  
- **Chart PNG**: 300dpi, A4 인쇄 적합  
- **Chart SVG**: 벡터 포맷, 슬라이드/웹 삽입용  
- **Notion JSON**: API 업로드 가능 포맷  

---

## PE-Score Baseline

| 항목 | 기준 점수 |
|------|-----------|
| 구조 완전성 | 25점 |
| 코드 실행 가능성 | 25점 |
| Tufte 원칙 준수 | 25점 |
| PE 생태계 연동 | 25점 |
| **Total baseline** | **100점** |

---

*Last updated: 2026-05-23 · KM-PIPE v3.0 · GilbertKwak*
