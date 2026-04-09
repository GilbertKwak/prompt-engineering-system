# 🤖 PE-1 — 자동개선 엔진 (Auto-Refinement)

> **ID**: PE-1 | **상태**: ✅ 운영 | **파일**: `engines/PE-1_auto-refinement/`

---

## 역할

프롬프트의 약점을 자동 탐지하고 개선된 버전으로 재작성하는 루프 엔진입니다. 최대 3회 반복하며 품질 기준 이상일 때 종료합니다.

## 입력 / 출력

| 구분 | 형식 | 설명 |
|------|------|------|
| INPUT | Markdown | 사용자 초안 프롬프트 |
| OUTPUT | Markdown | 개선된 프롬프트 + 변경 사항 |

## 핵심 로직

```
[초안 프롬플트 입력]
    ↓
[약점 탐지: 모호성 / 구조 불일치 / 누락]
    ↓
[재작성 실행]
    ↓
[PE-3 검증 통과? → Yes: 완료 / No: 루프 (max 3회)]
```

## 관련 파일

- `engines/PE-1_auto-refinement/prompt_template.md`
- `engines/PE-1_auto-refinement/examples/`
- [docs/rca-capa/RCA-001.md](../rca-capa/RCA-001.md) — 구조 복잡도 RCA

---

> [Master Index](../index.md) | [engines/PE-1/](../../engines/PE-1_auto-refinement/)
