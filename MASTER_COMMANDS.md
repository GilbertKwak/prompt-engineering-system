# 🧠 MASTER COMMANDS v1.1 — Gilbert Prompt Engineering System

> **Version**: 1.1 | **Updated**: 2026-04-28 | **Author**: Gilbert Kwak  
> **Scope**: T-09 전 도메인 통합 명령어 허브 (PE-11, PE-MEM, PE-EDU, PE-ICD, PE-NBD, PE-MFG, PE-JV, PE-FIN, PE-MKT, PE-7, **PE-IP**)

---

## 📌 사용 원칙

- **GitHub** = 프롬프트 XML 원본 · 스크립트 · 자동화 (Single Source of Truth)
- **Notion** = 검색 · 참조 · 인덱스 · 업무 메모
- **업데이트 흐름**: GitHub PR → PE-3 자동검증(85+) → knowledge_graph 재생성 → Notion 동기화

---

## 🔴 CMD-01 · 신규 프롬프트 등록

```
PE-[코드] [도메인명] 프롬프트를 신규 등록해줘.
PE-3 자동검증 후 GitHub prompts/<도메인>/<코드>.md 에 저장하고,
T-09 Child Page 신규 생성, knowledge_graph.json 노드 추가까지 완료해줘.
버전 태그는 v1.0으로 시작하고 Notion Mother Page 인덱스 테이블에 행 추가해줘.
```

**적용 도메인**: 전체  
**출력 기대값**: GitHub 커밋 링크 + Notion Child Page URL + knowledge_graph 노드 수 갱신 확인

---

## 🟡 CMD-02 · 기존 프롬프트 최적화 (버전업)

```
[프롬프트명] v[현재버전]을 PE-1 자동개선 엔진으로 분석해서
PE-3 점수 90+ 달성 버전으로 업그레이드해줘.
GitHub prompts/<도메인>/<코드>.md 에 커밋하고
Notion 해당 Child Page 버전 태그와 최종갱신 날짜 갱신해줘.
```

**사전 조건**: 현재 PE-3 점수 확인 필요  
**출력 기대값**: Before/After PE-3 점수 비교표 + 개선 포인트 요약

---

## 🟢 CMD-03 · 도메인 라이브러리 조회 & 추천

```
T-09 하위 [도메인코드] 라이브러리에서
[업무키워드] 관련 프롬프트 3개 추천해줘.
각 프롬프트의 PE-3 점수, GitHub 경로, Notion 페이지 링크 포함해서.
```

**도메인코드 목록**:
| 코드 | 도메인 | Notion |
|------|--------|--------|
| PE-11 | 멀티에이전트 오케스트레이션 | [링크](https://www.notion.so/34e55ed436f081c5a148d8200bc2896b) |
| PE-MEM | 반도체 메모리 (HBM·LPDDR·NAND·PIM) | [링크](https://www.notion.so/34e55ed436f0817cba4ae6154f3c664c) |
| PE-EDU | 교육·개념설명·기억법 | [링크](https://www.notion.so/34e55ed436f08136a396f4a612f6daf1) |
| PE-ICD | IC설계·회로도 | [링크](https://www.notion.so/34f55ed436f081e3be64ff8dbad0e845) |
| PE-NBD | 신사업개발 7-Chain | [링크](https://www.notion.so/34f55ed436f08162b162e53607cf8bc0) |
| PE-MFG | AI 스마트제조 | [링크](https://www.notion.so/34f55ed436f081498e16f75110c5d675) |
| PE-JV | 글로벌 JV 펀드 분석 | [링크](https://www.notion.so/34f55ed436f08150b07dc7f5f800311b) |
| PE-FIN | 투자전략 | [링크](https://www.notion.so/34f55ed436f081c2ad05df1dc11e0ae7) |
| PE-MKT | 마케팅전략 | [링크](https://www.notion.so/34f55ed436f081b1bb25ed8c47bcb595) |
| PE-7 | AI 자동화 설계 | [링크](https://www.notion.so/34955ed436f081149dd6de25dba027d7) |
| **PE-IP** | **통합 마스터 프롬프트 라이브러리** | [링크](https://www.notion.so/35055ed436f08159aaa8d0817e76ba18) |

---

## 🔵 CMD-04 · 멀티에이전트 전체 실행 (PE-11)

```
PE-11 Master Multi-Agent System으로 [업무 목표]를 수행해줘.
Inception → Deep Research → Hypothesis Validation → Strategic Roadmap 순서로 실행하고,
각 단계 결과를 요약 후 다음 단계 입력으로 연결해줘.
최종 결과는 Notion T-09에 저장할 수 있는 형식으로 출력해줘.
```

**연결 스크립트**: `scripts/inception_module.py` → `scripts/brainstorming.py` → `scripts/ralph_loop_2stage.py` → `scripts/recursive_delegation.py`

---

## ⚫ CMD-05 · 시스템 상태 점검

```
현재 knowledge_graph.json 최신 상태 확인하고,
PE-3 점수 미달(85 미만) 프롬프트 목록 전체 뽑아줘.
우선순위 개선 스케줄(이번 주/다음 주/이번 달)로 나눠서 제안해줘.
마지막으로 Notion T-09 Mother Page와 GitHub README 동기화 상태도 확인해줘.
```

**참조 파일**: `dashboard/metrics.md`, `knowledge_graph.json`

---

## 🟣 CMD-06 · 신규 도메인 추가

```
PE-[신규코드] [새도메인명] 라이브러리를 신설해줘.
1. T-09 Mother Page 인덱스 테이블에 신규 행 추가
2. GitHub prompts/[새도메인]/ 폴더 생성 + README.md 작성
3. knowledge_graph.json 신규 노드 추가
4. MASTER_COMMANDS.md CMD-03 도메인코드 테이블에 행 추가
5. GitHub README.md 도메인 인덱스 갱신
위 5단계를 순서대로 완료해줘.
```

---

## 🟠 CMD-07 · Notion ↔ GitHub 동기화 실행

```bash
# notion_sync.py 수동 실행
python automation/notion_sync.py --target T-09 --direction github-to-notion

# 또는 역방향
python automation/notion_sync.py --target T-09 --direction notion-to-github

# GitHub Actions 수동 트리거
gh workflow run pe7_daily_pipeline.yml

# 실행 상태 확인
gh run list --workflow=pe7_daily_pipeline.yml --limit 5
```

---

## 🔶 CMD-08 · PE-3 일괄 검증

```bash
# 전체 prompts/ 디렉터리 일괄 PE-3 검증
for f in prompts/**/*.md; do
  python automation/auto_validate_jv.py --file "$f" --rules PE-1,PE-3 --verbose
done

# 결과를 dashboard/metrics.md에 반영
python dashboard/update_metrics.py --input results/ --output dashboard/metrics.md
```

---

## 🧬 CMD-09 · PE-IP 라이브러리 관리

> **대상**: PE-IP Integrated Prompt Library (통합 마스터 프롬프트 라이브러리)  
> **Notion**: https://www.notion.so/35055ed436f08159aaa8d0817e76ba18  
> **GitHub 경로**: `PE-IP/`

```
[pe-ip-index] PE-IP 라이브러리에 등록된 전체 프롬프트 목록을 조회해줘.
  — 코드 / 라이브러리명 / 도메인 / PE-3 점수 / GitHub 경로 / 상태 테이블 형식으로 출력.

[pe-ip-add] PE-IP 라이브러리에 [프롬프트명 or 코드] 를 신규 추가해줘.
  — PE-3 자동검증(88+) 완료 후 PE-IP 마스터 인덱스 테이블에 행 추가,
    GitHub PE-IP/ 폴더에 .md 파일 생성, knowledge_graph.json 노드/엣지 갱신까지 완료해줘.

[pe-ip-validate] PE-IP 라이브러리 전체를 PE-1(자동개선) + PE-3(자동검증) 기준으로 일괄 검증해줘.
  — 점수 미달(88 미만) 항목은 E-09 태깅 후 PE-1 자동개선 루프 즉시 트리거.
    결과를 Before/After 비교표와 E-0N 오류 코드 목록으로 출력해줘.
```

### Shell Alias — PE-IP 전용 3종

```bash
PE_HOME="~/workspace/prompt-engineering-system"

# pe-ip-index: PE-IP 전체 목록 조회
alias pe-ip-index='python $PE_HOME/automation/pe_ip_indexer.py --list-all'

# pe-ip-add: PE-IP 신규 항목 추가 (사용법: pe-ip-add --code PE-XX --name "라이브러리명")
alias pe-ip-add='python $PE_HOME/automation/pe_ip_indexer.py --add'

# pe-ip-validate: PE-IP 전체 PE-1 + PE-3 일괄 검증
alias pe-ip-validate='python $PE_HOME/automation/auto_validate.py --target PE-IP --rules PE-1,PE-3 --threshold 88 --e09-trigger'
```

### 실행 예시

```bash
# 1) 전체 목록 조회
pe-ip-index
# 출력: PE-IP 마스터 인덱스 테이블 (코드·도메인·PE-3 점수·상태)

# 2) 신규 항목 추가
pe-ip-add --code PE-RISK --name "Risk Management Prompt Library v1.0" \
          --domain "리스크관리" --path "PE-IP/pe_risk_v1.0.md"
# 출력: 추가 완료 + knowledge_graph 노드 수 갱신 확인

# 3) 전체 검증 실행
pe-ip-validate --verbose
# 출력: Before/After PE-3 점수 비교표 + E-09 트리거 목록

# 4) 검증 후 동기화
pe-ip-validate && pe-sync-up
```

### pe_ip_indexer.py 핵심 구조

```python
# automation/pe_ip_indexer.py
import json, argparse
from pathlib import Path

PE_IP_INDEX = Path("PE-IP/index.json")

def list_all():
    """PE-IP 전체 목록 조회"""
    index = json.loads(PE_IP_INDEX.read_text())
    print(f"{'코드':<10} {'라이브러리명':<40} {'PE-3':>6} {'상태':<10}")
    print("-" * 75)
    for item in index["libraries"]:
        print(f"{item['code']:<10} {item['name']:<40} {item['pe3_score']:>6} {item['status']:<10}")

def add_library(code: str, name: str, domain: str, path: str):
    """PE-IP 신규 항목 추가"""
    index = json.loads(PE_IP_INDEX.read_text())
    new_entry = {
        "code": code, "name": name, "domain": domain,
        "path": path, "pe3_score": None, "status": "Draft",
        "added": "2026-04-28"
    }
    index["libraries"].append(new_entry)
    PE_IP_INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2))
    print(f"[OK] {code} 추가 완료 — 총 {len(index['libraries'])}개")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--list-all", action="store_true")
    parser.add_argument("--add", action="store_true")
    parser.add_argument("--code"); parser.add_argument("--name")
    parser.add_argument("--domain"); parser.add_argument("--path")
    args = parser.parse_args()
    if args.list_all: list_all()
    elif args.add: add_library(args.code, args.name, args.domain, args.path)
```

---

## 🏃 Shell Alias 등록 (전체 시스템)

```bash
# ~/.bashrc 또는 ~/.zshrc에 추가 — Gilbert PE System 전체
PE_HOME="~/workspace/prompt-engineering-system"

# 검증
alias pe-validate='python $PE_HOME/automation/auto_validate_jv.py --rules PE-1,PE-3'
alias pe-validate-v='python $PE_HOME/automation/auto_validate_jv.py --rules PE-1,PE-3 --verbose'
alias pe-validate-all='for f in $PE_HOME/prompts/**/*.md; do pe-validate-v --file "$f"; done'

# 동기화
alias pe-sync-up='python $PE_HOME/automation/notion_sync.py --direction github-to-notion'
alias pe-sync-down='python $PE_HOME/automation/notion_sync.py --direction notion-to-github'

# 파이프라인
alias pe-pipeline='gh workflow run pe7_daily_pipeline.yml'
alias pe-status='gh run list --workflow=pe7_daily_pipeline.yml --limit 5'

# 그래프
alias pe-graph='python $PE_HOME/scripts/update_knowledge_graph.py'

# 메트릭스
alias pe-metrics='cat $PE_HOME/dashboard/metrics.md'
alias pe-metrics-update='python $PE_HOME/dashboard/update_metrics.py'

# ── PE-IP 전용 (v1.1 신규) ──────────────────────────────────────────────
alias pe-ip-index='python $PE_HOME/automation/pe_ip_indexer.py --list-all'
alias pe-ip-add='python $PE_HOME/automation/pe_ip_indexer.py --add'
alias pe-ip-validate='python $PE_HOME/automation/auto_validate.py --target PE-IP --rules PE-1,PE-3 --threshold 88 --e09-trigger'
# ────────────────────────────────────────────────────────────────────────

# 적용
source ~/.bashrc
```

---

## 📊 빠른 참조 테이블

| 명령 | 설명 | Alias |
|------|------|-------|
| 단일 프롬프트 검증 | PE-3 검증 실행 | `pe-validate --file <path>` |
| 전체 검증 | 모든 prompts/ 검증 | `pe-validate-all` |
| GitHub→Notion 동기화 | 최신 내용 Notion 반영 | `pe-sync-up` |
| Notion→GitHub 동기화 | Notion 내용 GitHub 반영 | `pe-sync-down` |
| 일일 파이프라인 | 전체 자동화 실행 | `pe-pipeline` |
| 파이프라인 상태 | 최근 5회 실행 결과 | `pe-status` |
| 지식 그래프 업데이트 | knowledge_graph 재생성 | `pe-graph` |
| 메트릭스 확인 | PE-3 점수 대시보드 | `pe-metrics` |
| **PE-IP 전체 목록** | 통합 라이브러리 인덱스 조회 | `pe-ip-index` |
| **PE-IP 항목 추가** | 신규 프롬프트 라이브러리 등록 | `pe-ip-add --code ... --name ...` |
| **PE-IP 일괄 검증** | PE-1+PE-3 기준 전체 검증 + E-09 자동 트리거 | `pe-ip-validate` |

---

## 🔗 핵심 링크 (SSOT)

| 구분 | URL |
|------|-----|
| **T-09 Mother Page** | https://www.notion.so/34a55ed436f0814d9cffe6a2f0816e29 |
| **Master Hub (PE Lab)** | https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b |
| **PE-IP 라이브러리** | https://www.notion.so/35055ed436f08159aaa8d0817e76ba18 |
| **GitHub 저장소** | https://github.com/GilbertKwak/prompt-engineering-system |
| **knowledge_graph.json** | https://github.com/GilbertKwak/prompt-engineering-system/blob/main/knowledge_graph.json |
| **PE-7 AI 자동화** | https://www.notion.so/34955ed436f081149dd6de25dba027d7 |

---

> ✅ **[v1.0 | 2026-04-28 10:46 KST]** MASTER_COMMANDS.md 전 도메인 통합 신규 생성 — CMD-01~08 + Alias 전체 + 도메인 인덱스 테이블 🟢  
> ✅ **[v1.1 | 2026-04-28 13:31 KST]** PE-IP 명령어 3종 추가 — CMD-09 신설(pe-ip-index · pe-ip-add · pe-ip-validate) + CMD-03 테이블 PE-IP 행 추가 + 빠른 참조 테이블 3행 추가 + SSOT 링크 PE-IP 등록 🟢  
> **다음 업데이트 기준**: 신규 도메인 추가 시 CMD-03 테이블에 행 추가 + 버전 태그 갱신
