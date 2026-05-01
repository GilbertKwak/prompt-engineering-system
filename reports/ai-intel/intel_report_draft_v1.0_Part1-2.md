# 글로벌 AI 기술 인텔리전스 보고서
**분류**: C-31 PE-AI Intelligence Library  
**버전**: v1.0 Draft  
**생성**: 2026-05-01 | **프롬프트**: notion_005_v1.0  
**KG 참조**: v4.6 corp-nodes  

---

## PART 1. 글로벌 AI 가속기 시장 구조 분석

### 1.1 시장 개요 및 경쟁 지형

2026년 글로벌 AI 가속기 시장은 NVIDIA의 압도적 점유율(H100/H200/B200 라인)을 중심으로,
AMD MI300X 시리즈, Google TPU v5, Intel Gaudi 3, 그리고 중국의 Huawei Ascend 910C 간의
다층적 경쟁 구도로 재편되고 있다.

**핵심 시장 지표 (2026Q1 추정)**

| 지표 | 값 | YoY 변화 |
|------|-----|------|
| 글로벌 AI 가속기 시장 규모 | $87.4B | +62% |
| NVIDIA 점유율 (수익 기준) | ~72% | -4pp |
| AMD 점유율 | ~12% | +5pp |
| 기타 | ~16% | -1pp |
| HBM 탑재율 (고성능 GPU) | 98% | +8pp |

### 1.2 HBM 공급망 구조

HBM(High Bandwidth Memory)은 AI 가속기 성능의 핵심 병목이며,
Samsung(CORP-011)과 SK Hynix(CORP-012)가 전 세계 HBM 생산의 약 95%를 점유한다.

**HBM 세대별 대역폭 비교**

| 세대 | 대역폭 | 용량 | 채택 칩 |
|------|--------|------|---------|
| HBM2e | 461 GB/s | 16-32GB | A100 |
| HBM3  | 819 GB/s | 24-48GB | H100 |
| HBM3E | 1.2 TB/s | 36-96GB | H200, MI300X |
| HBM4  | 2.0 TB/s+ | 64-128GB | B300(예정) |

### 1.3 미중 기술 규제 환경

미국 BIS 수출 통제로 Huawei Ascend 910C는 TSMC 접근이 차단되어 있으며,
중국 자체 파운드리(SMIC 7nm급)로 대체 생산을 시도 중이나 성능 격차는 2~3세대 수준이다.

---

## PART 2. 주요 AI 파운데이션 모델 기업 분석

### 2.1 OpenAI — 시장 지위 및 전략

OpenAI(CORP-006)는 GPT-4o / o3 시리즈를 기반으로 API 마켓 및 ChatGPT Enterprise를 통해
B2B·B2C 시장을 동시 공략하고 있다. Microsoft Azure(CORP-008)와의 Azure OpenAI Service
파트너십이 인프라 비용을 크게 절감하는 구조다.

| 항목 | 값 |
|------|-----|
| ARR | ~$10B |
| MAU | ~600M |
| 모델 패밀리 | GPT-4o, o3, o3-mini |
| 배포 파트너 | Azure, AWS Marketplace |

### 2.2 Anthropic — 안전성 중심 차별화

Anthropic(CORP-007)은 Constitutional AI(CAI) 방법론 기반 Claude 3.x 시리즈를 개발하며,
AWS Bedrock(CORP-009)을 통한 엔터프라이즈 배포를 주력으로 한다.

| 구분 | Anthropic | OpenAI |
|------|-----------|--------|
| 주력 모델 | Claude 3.7 Sonnet | GPT-4o / o3 |
| 차별화 축 | 안전성·긴 컨텍스트 | 멀티모달·에이전트 |
| 주 파트너 | AWS Bedrock | Azure OpenAI |
| 컨텍스트 | 200K tokens | 128K tokens |
| 기업 가치 (추정) | ~$61.5B | ~$157B |

### 2.3 Meta AI — 오픈소스 전략

Meta AI(CORP-010)의 Llama 3.x 오픈소스 전략은 클로즈드 모델 기업들에게 가격 압박을 형성한다.
2026년 AI/Infra CAPEX 가이던스 $60~65B, H100/H200 누적 보유 ~350,000대(추정).

### 2.4 신흥 플레이어

| 기업 | 모델 | 차별화 |
|------|------|--------|
| xAI (CORP-016) | Grok 3 | 실시간 X 데이터 |
| Mistral AI (CORP-017) | Mistral Large 2 | 유럽 오픈소스 |
| Groq (CORP-018) | LPU 추론 칩 | 500 tok/s+ |

---

*본 보고서는 notion_005_v1.0 프롬프트 및 KG v4.6 corp-nodes 기반 생성*  
*데이터 기준일: 2026-05-01 | 다음 업데이트: 자동 (intel-report-update.yml)*
