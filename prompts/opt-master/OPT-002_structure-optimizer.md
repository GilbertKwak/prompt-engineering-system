---
id: OPT-002
title: 구조화 최적화 프롬프트
version: 1.0
category: opt-master
pe3_score: 91
notion_sync: T-09 > OPT-MASTER-001
github_path: prompts/opt-master/OPT-002_structure-optimizer.md
created: 2026-07-02
---

# OPT-002 · 구조화 최적화 프롬프트 v1.0

## 🎯 목적
비정형 입력을 논리적 계층 구조로 변환하여 AI의 처리 효율을 높인다.

## 📐 프롬프트 구조

```
[STRUCTURE OPTIMIZER v1.0]

당신은 정보 구조화 전문가입니다.
입력된 내용을 아래 프레임워크로 재구성하십시오.

### FRAME A — 피라미드 구조
핵심 주장 (1문장)
  └─ 근거 1
      └─ 세부 증거 1-1
      └─ 세부 증거 1-2
  └─ 근거 2
      └─ 세부 증거 2-1

### FRAME B — MECE 검증
- 상호 배타적 (Mutually Exclusive): 항목 간 중복 확인
- 전체 포괄적 (Collectively Exhaustive): 누락 항목 확인
- MECE 점수: [X/10]

### FRAME C — 출력 형식 최적화
- 대상 독자 수준에 맞게 언어 조정
- 핵심→세부 순서 유지
- 시각적 계층(##, ###, -) 적용

입력: {{RAW_INPUT}}
대상 독자: {{AUDIENCE_LEVEL}} (초급/중급/전문가)
```

## 🔧 활용 파라미터
| 파라미터 | 기본값 | 설명 |
|---------|--------|------|
| `{{RAW_INPUT}}` | — | 구조화할 원본 텍스트 |
| `{{AUDIENCE_LEVEL}}` | 중급 | 독자 수준 |

## 📊 성능 지표
- PE-3 Score: 91
- 구조 명확도 향상: +41%
- MECE 달성률: 87%

## 🔗 연관 프롬프트
- OPT-001 (컨텍스트), OPT-003 (체인)
