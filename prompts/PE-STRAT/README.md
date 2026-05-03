# PE-STRAT · Strategic Monitoring Optimization Suite

**Version**: v1.0.0 | **Created**: 2026-05-03 | **Author**: GilbertKwak  
**Notion**: `C-3x · PE-PROMPT-OPT Hub` (T-09 하위) | `C-33 · PE-STRAT` | `DIR-09`

---

## 개요

`StrategicMonitoringAgent_v5.2` 계열 프롬프트를 자동 검증·개선·증식·실행하기 위한
최적화 컨트롤러 묶음입니다.

Porter Five Forces × Farrell 병목 무기화 × Ben Thompson 스택 분해 관점을 동시 적용하는
국가별 반도체×AI 전략 감시 에이전트를 더 정밀하게, 더 빠르게 운용하기 위해 설계되었습니다.

---

## 파일 구조

```
prompts/PE-STRAT/
├── README.md                          ← 이 파일
├── PE-STRAT-OPT_v1.0.xml             ← 품질 검증·개선 컨트롤러
├── PE-STRAT-VARIANT-GEN_v1.0.xml     ← 국가·산업·World별 Variant 생성기
├── PE-STRAT-META-EXT_v1.0.xml        ← Meta Monitoring 확장 (Blind Spot 탐지)
└── PE-STRAT-SESSION-CMD_v1.0.xml     ← 세션 명령어 세트 (A/B/C 시나리오)
```

---

## 파일별 역할

| 파일 | 역할 | 우선 사용 시점 |
|---|---|---|
| `PE-STRAT-OPT_v1.0.xml` | 기존 v5.2 프롬프트 품질 검증·개선 | 에이전트 실행 전 항상 |
| `PE-STRAT-VARIANT-GEN_v1.0.xml` | 국가·산업·World 특화 Variant 자동 생성 | 새 분석 세션 시작 시 |
| `PE-STRAT-META-EXT_v1.0.xml` | 외생 변수·Blind Spot 자동 탐지 | 분석 결과 보완 시 |
| `PE-STRAT-SESSION-CMD_v1.0.xml` | 재사용 가능 세션·보고서·업데이트 명령어 | 일상 운용 전반 |

---

## 표준 사용 흐름

```
1. PE-STRAT-OPT_v1.0     → 기존 에이전트 프롬프트 품질 검증
2. PE-STRAT-VARIANT-GEN  → 국가·산업·World 특화 Variant 생성
3. Variant 실행          → 전략 분기 경보(Alert) 산출
4. PE-STRAT-META-EXT     → Blind Spot 탐지 및 신규 변수 제안
5. PE-STRAT-SESSION-CMD  → 보고서(DIR-09 RPT-09-00X) 생성 및 저장
```

---

## Notion 연계

| Notion 페이지 | 연결 목적 |
|---|---|
| `T-09 · 프롬프트 엔지니어링 시스템` | 최상위 프롬프트 허브 |
| `C-33 · PE-STRAT` | 전략 에이전트 실행 허브 |
| `C-3x · PE-PROMPT-OPT Hub` | 이 디렉토리의 Notion 미러 |
| `DIR-09 · 반도체×AI 전략 분석` | 분석 결과 저장 보고서 |
| `FU-008 · 보고서 생성 템플릿` | 보고서 섹션 구조 기준 |
| `FU-025 · 전략 분기 경보 템플릿` | Alert 출력 형식 기준 |

---

## 버전 이력

| 버전 | 날짜 | 주요 변경 |
|---|---|---|
| v1.0.0 | 2026-05-03 | 최초 생성: OPT / VARIANT-GEN / META-EXT / SESSION-CMD 4종 |

---

## 관련 링크

- **GitHub Repo**: [GilbertKwak/prompt-engineering-system](https://github.com/GilbertKwak/prompt-engineering-system)
- **Notion Hub**: T-09 → C-3x PE-PROMPT-OPT Hub
- **Base Agent**: `StrategicMonitoringAgent_v5.2` (4개 버전, prompts/strategy-collapse/ 참조)
