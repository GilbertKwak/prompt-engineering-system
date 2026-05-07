# PE-STRAT Prompt Library

## 디렉터리 구조

### 핵심 최적화 프롬프트 (OPT Series)
| File | Code | PE-3 | Description |
|------|------|------|-------------|
| OPT-AOCRS-v1.0.md | OPT-AOCRS v1.0 | ~95 | Advanced Ownership Control Risk Strategy |
| OPT-CSGS-v1.0.md | OPT-CSGS v1.0 | ~94 | Chaebol Succession & Global Control Simulation |
| OPT-GHCRA-v1.0.md | OPT-GHCRA v1.0 | ~94 | Global Hedge Fund & Regulatory Control Risk |
| opt_aif_v1.0.md | OPT-AIF v1.0 | ~94 | Advanced Insight Forecasting |
| opt_sfa_v1.0.md | OPT-SFA v1.0 | ~93 | Strategic Forecasting Agent |

### 기존 전략 프롬프트
| File | Description |
|------|-------------|
| pe_strat_01_v2.0.md | PE-STRAT 기존 전략 통합 v2.0 |
| SAuRP-v3.1-OPT.md | Strategy Unified Research Prompt |
| PHFA-v2.0-OPT.md | Predictive Horizon Forecasting Agent |
| GIPA-v2.0-OPT.md | Global Intelligence & Prediction Agent |
| AUTOPLUS-v1.0-OPT.md | Auto Plus Strategy |

### 메타/설정 파일
| File | Description |
|------|-------------|
| PE-STRAT-META-EXT_v1.0.xml | 메타 확장 설정 |
| PE-STRAT-OPT_v1.0.xml | 최적화 설정 |
| PE-STRAT-SESSION-CMD_v1.0.xml | 세션 명령어 |
| PE-STRAT-VARIANT-GEN_v1.0.xml | 변형 생성기 |
| PROMPT_VERSION_HISTORY.md | 버전 히스토리 |

### E2E 검증 케이스
| File | Description |
|------|-------------|
| e2e_tc02_steelcore_aif_sfa.md | TC-02 SteelCore 제조업 검증 |
| e2e_tc03_cloudflow_aif_sfa.md | TC-03 CloudFlow SaaS 검증 |
| e2e_validation_summary.md | E2E 검증 요약 |

## 전체 파이프라인
```
PE-DD → OPT-AIF → OPT-SFA → OPT-AOCRS → OPT-CSGS → OPT-GHCRA → PE-FIN
```

## 빠른 실행 명령어
```javascript
// 지배구조 통합 분석
/aocrs run TARGET="[기업]" MODE="Full" | /csgs run --from-aocrs | /ghcra run --from-csgs | /fin run FIN-07

// 전략 예측 통합
/aif run TARGET="[대상]" DEPTH="Full" | /sfa init --from-aif

// 전체 DD→분석→재무 파이프라인
/dd-fin run TARGET="[IR]" STAGE="[단계]" DOMAIN="[도메인]" TRIGGER_ENGINE=ON
```

*Last updated: 2026-05-07*
