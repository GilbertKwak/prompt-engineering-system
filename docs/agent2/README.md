# 🤖 PE-2 — 자동증식 엔진 (Auto-Proliferation)

> **ID**: PE-2 | **상태**: ✅ 운영 | **파일**: `engines/PE-2_auto-proliferation/`

---

## 역할

단일 프롬프트를 다양한 목적과 도메인에 맞는 여러 버전으로 자동 맞춤 확장하는 엔진입니다.

## 입력 / 출력

| 구분 | 형식 | 설명 |
|------|------|------|
| INPUT | Markdown | PE-1 통과 프롬프트 |
| OUTPUT | Markdown 배열 | 도메인·난이도·포맷 변형 버전 |

## 변형 축 (3가지)

| 축 | 예시 |
|----|------|
| 도메인 | 반도체, 제약, 헬스케어, 금융 |
| 난이도 | 실험적 / 표준 / 부스터 |
| 포맷 | JSON 구조화 / 서술형 / 출력 템플릿화 |

## 관련 파일

- `engines/PE-2_auto-proliferation/prompt_template.md`
- `engines/PE-2_auto-proliferation/examples/`

---

> [Master Index](../index.md) | [engines/PE-2/](../../engines/PE-2_auto-proliferation/)
