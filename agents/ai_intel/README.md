# agents/ai_intel — AI Intel Collector Prompts

## 개요

`ai_intel_collector.py`가 사용하는 도메인별 프롬프트 정의 디렉토리입니다.
각 YAML 파일은 하나의 도메인을 담당하며, 수집 쿼리, 출력 스키마, 검증 규칙을 포함합니다.

## 도메인 구조

```
agents/ai_intel/
├── README.md
└── prompts/
    ├── enterprise_deployment.yaml   # 기업 AI 도입 동향
    ├── model_architecture.yaml      # LLM 아키텍처 혁신
    ├── regulatory_policy.yaml       # AI/반도체 규제 정책
    └── investment_funding.yaml      # VC/M&A/PE 투자 동향
```

## 프롬프트 YAML 구조

```yaml
domain:
  id: string              # 도메인 고유 ID
  name: string            # 표시 이름
  description: string     # 설명
  priority: HIGH|MEDIUM   # 수집 우선순위
  ew_sensitivity: level   # EW 탐지 민감도

model:
  standard: sonar         # 기본 수집 모델
  deep: sonar-pro         # 심층 분석 모델
  emergency: sonar-pro    # EW 발동 시 모델

system_prompt: |          # LLM 시스템 프롬프트
queries:
  primary: []             # 주요 수집 쿼리
  secondary: []           # 보조 쿼리
  ew_triggers: []         # EW 탐지 쿼리

output_schema:            # 출력 JSON 스키마 정의
validation:               # 품질 검증 규칙
```

## 새 도메인 추가 방법

1. `prompts/` 디렉토리에 `{domain_id}.yaml` 파일 생성
2. 위 구조에 맞게 작성
3. `agent_index.yaml`의 `ai_intel_collector.domains`에 domain_id 추가
4. `automation/ai_intel_collector.py`의 `DOMAIN_CONFIGS`에 등록
