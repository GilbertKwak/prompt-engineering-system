# VI-BLOCK YAML Schema v1.0

> **Value Intelligence Block** — 프롬프트 & 보고서 범용 최적화 표준  
> VE(Value Engineering) v1.0 원칙 적용: **기능 유지·강화 + 비용 제거·축소**

---

## 📁 디렉토리 구조

```
config/vi-block-schema/
├── VI_BLOCK_SCHEMA_v1.0.yaml          # 마스터 스키마 정의
├── VI_BLOCK_EXAMPLE_PE-CON.yaml       # PE-CON 도메인 예시 인스턴스
├── VI_BLOCK_EXAMPLE_REPORT.yaml       # 전 도메인 보고서 공통 출력 표준 블록
├── README.md                          # 이 파일
└── instances/                         # 실제 배포 인스턴스 디렉토리
    ├── PE-CON/
    ├── PE-FIN/
    ├── PE-IP/
    ├── PE-SEMI/
    ├── FU-SERIES/
    └── GLOBAL/
```

---

## 🎯 VI-BLOCK이란?

**VI-BLOCK(Value Intelligence Block)**은 프롬프트와 보고서에 공통으로 적용 가능한  
**YAML 기반 최적화 단위 블록**입니다.

| 개념 | 설명 |
|---|---|
| **기능 분석** | FAST 다이어그램 연계 — WHY/WHAT/HOW/HOW-MUCH 계층 분류 |
| **가치 분류** | BASIC(필수) / SECONDARY(보조) / UNNECESSARY(제거) / ESTEEM(신뢰) |
| **낭비 제거** | 중복·과잉 품질·불필요 단계·인지 부하·컨텍스트 낭비 제거 |
| **적용 범위** | 프롬프트 / 보고서 / 템플릿 / 워크플로 / 자동화 연계 |

---

## 🔑 Block ID 명명 규칙

```
[도메인코드]-[주제코드]-B[번호]
예: PE-CON-B001  /  FU-HBM-B012  /  GLOBAL-STD-B001
```

| 도메인코드 | 설명 |
|---|---|
| `PE-CON` | PE-CON (M&A 실사·LP Relations·Exit 전략) |
| `PE-FIN` | PE-FIN (재무 분석·모델링) |
| `PE-IP` | PE-IP (IP 분석·특허) |
| `PE-SEMI` | PE-SEMI (반도체 분석) |
| `FU-SERIES` | FU 시리즈 보고서 |
| `GLOBAL-STD` | 전 도메인 공통 표준 |
| `ASTRA` | AstraChips / AstraNext 전략 |

---

## ⚡ 빠른 시작

### 1. 새 VI-BLOCK 인스턴스 생성

```yaml
# 최소 필수 필드
$schema: "vi-block-schema/v1.0"
block_id: "PE-CON-B002"
block_name: "LP 보고서 자동 생성 블록"
block_type: FUNCTION
domain:
  primary: PE-CON
  cross_domain: false
ve_analysis:
  fast_level: HOW
  primary_function: "분기별 LP 보고서를 표준 형식으로 자동 생성한다"
  function_class: BASIC
application_scope:
  target_types: [PROMPT, REPORT]
  applicable_domains: [PE-CON]
  priority: P1_HIGH
metadata:
  version: "1.0.0"
  status: DRAFT
  author: "Gilbert Kwak"
  created_at: "2026-05-17"
  updated_at: "2026-05-17"
```

### 2. 기존 프롬프트에 적용

```
1. 해당 도메인 인스턴스 파일 조회
2. prompt_spec.instruction_template 추출
3. {{PLACEHOLDER}} 값 입력
4. chain_position 확인 후 프롬프트 체인에 삽입
```

### 3. 보고서 적용

```
1. report_spec.section_mapping 확인
2. auto_apply: true 블록은 자동 적용
3. output_format.depth_level 조정 (1~5)
4. automation_integration.notion_sync 설정 후 동기화
```

---

## 📊 현재 등록 블록

| Block ID | 이름 | 도메인 | 우선순위 | 상태 |
|---|---|---|---|---|
| GLOBAL-STD-B001 | 전 도메인 보고서 공통 출력 표준 | ALL | P0_CRITICAL | ACTIVE |
| PE-CON-B001 | M&A 실사 대상 기업 재무 분석 | PE-CON | P1_HIGH | ACTIVE |

---

## 🔗 연관 저장소

- [`notion-github-ops`](https://github.com/GilbertKwak/notion-github-ops) — Notion↔GitHub 운영체계
- [`auto-continuation-system`](https://github.com/GilbertKwak/auto-continuation-system) — ACP 자동화 연계
- [`pe-prompts`](https://github.com/GilbertKwak/pe-prompts) — PE 도메인 프롬프트 라이브러리

---

## 📋 업데이트 로그

| 날짜 | 버전 | 변경 내용 |
|---|---|---|
| 2026-05-17 | v1.0.0 | VI-BLOCK YAML 스키마 최초 정의 및 예시 2개 추가 |
