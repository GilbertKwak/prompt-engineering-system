# 🤖 AI Intel Agent Domain

> Perplexity sonar/sonar-pro 기반 AI 인텔리전스 수집 도메인

## 담당 스크립트

`automation/ai_intel_collector.py`

## 수집 도메인

| 도메인 ID | 설명 | 기본 모델 |
|---|---|---|
| `enterprise_deployment` | 엔터프라이즈 AI 도입 동향 | sonar |
| `model_architecture` | LLM 아키텍처·벤치마크 | sonar |
| `regulatory_policy` | AI 규제·정책 변화 | sonar |
| `investment_funding` | AI 투자·펀딩 동향 | sonar |

## 프롬프트 템플릿

각 도메인별 시스템 프롬프트는 `agent_config.yaml` 참조.
