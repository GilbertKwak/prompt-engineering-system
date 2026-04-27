# 🏭 PE-MFG · AI Manufacturing Plant Prompt Library v1.0

> **Status**: ✅ Active | **Created**: 2026-04-27 | **Manager**: GilbertKwak
> **Notion SSOT**: [PE-MFG Notion Page](https://www.notion.so/34f55ed436f081498e16f75110c5d675)
> **Parent**: T-09 프롬프트 엔지니어링 시스템 Mother Page (C-10)

---

## 개요

AI 스마트 제조 공장 구축 전용 프롬프트 라이브러리입니다.
초기 기획·설계·시뮬레이션·AI 통합·생산 최적화·확장까지 **6단계 전주기**를 커버합니다.

## 파일 구조

```
PE-MFG/
├── README.md                                          # 이 파일
├── system_prompt.xml                                  # 원본 System Prompt (XML)
├── deployment_steps.md                                # 6단계 실행 프레임워크
└── integration_map.md                                 # PE-7 / PE-11 / T-09 연동 구조
```

## 6단계 프레임워크 요약

| Phase | 한글명 | 핵심 기술 | KPI |
|-------|--------|-----------|-----|
| 1 | 기획 및 전략 수립 | Data Analytics, AI Strategy | ROI 정확도 >85% |
| 2 | 공정 분석 및 데이터 인프라 | IoT, Data Lake, Cloud | 데이터 정확도 >99% |
| 3 | AI 모델 설계 및 시뮬레이션 | ML, DL, Digital Twin | 예측 정확도 >90% |
| 4 | AI 통합 및 자동화 | RPA, Edge AI, API | 자동화율 >70% |
| 5 | 운영 최적화 및 지속 개선 | MLOps, BI Tools | OEE >85% |
| 6 | 확장 및 고도화 | Federated Learning, AutoML | 글로벌 생산성 >20% |

## 연동 구조

- **PE-7 AI 자동화**: `pe7_daily_pipeline.yml` 내 PE-MFG 프롬프트 자동 선택
- **PE-11 멀티에이전트**: manufacturing 도메인 요청 시 Agent Router → PE-MFG 라우팅
- **T-09 Mother Page**: 도메인별 라이브러리 인덱스 C-10 등록

## E-0N 상태

```
E-01 SHA 불일치: ✅ CLEAR
E-02 상태값 누락: ✅ CLEAR  
E-03 버전 역행:   ✅ CLEAR
E-04 구조 불일치: ✅ CLEAR
E-07 필수 필드:   ✅ CLEAR
```

---
*Last updated: 2026-04-27 | Version: v1.0*
