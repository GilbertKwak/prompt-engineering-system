# 🌡️ PE-THERM · 반도체 열관리 분석 프롬프트 라이브러리 v1.0

> **T-09 C-20** | Notion SSOT: https://www.notion.so/35155ed436f081ca93bcddb49af69c7d
> **PE-3 평균 점수**: 93/100 | **등록일**: 2026-04-29 | **관리자**: Gilbert Kwak

## 📋 라이브러리 개요

HBM·2.5D/3D IC 패키징 반도체 열관리 분야 전용 최적화 프롬프트 라이브러리.
T-09 3-Engine 시스템(PE-1 자동개선 / PE-2 자동증식 / PE-3 자동검증) 완전 연동.

## 📂 프롬프트 인덱스

| 파일 | 주제 | 핵심 물리 모델 | PE-3 | 버전 |
|---|---|---|---|---|
| [THERM-01_v3.0.md](THERM-01_v3.0.md) | TIM 열저항 지배 메커니즘 | Series R-network · Kapitza · Scaling Law | **95** | v3.0 |
| [THERM-02_v2.0.md](THERM-02_v2.0.md) | Underfill 열차단 TC-NCF vs MR-MUF | κ 비교 · Percolation · TBR | **93** | v2.0 |
| [THERM-03_v2.0.md](THERM-03_v2.0.md) | Micro-Bump 열저항 정량 분석 | Fourier · R_th × N_interfaces | **91** | v2.0 |
| [THERM-04_v2.0.md](THERM-04_v2.0.md) | High I/O Activity 발열 분석 | P_dynamic ∝ f·C·V² · PHY 전력 모델 | **90** | v2.0 |
| [THERM-05_v2.0.md](THERM-05_v2.0.md) | Interposer/Substrate 열저항 | R_th Breakdown · Organic vs Si | **92** | v2.0 |
| [THERM-06_v3.0.md](THERM-06_v3.0.md) | TSV 열전달 PDE + Scaling Law | ∇·(k∇T) · Spreading R · Saturation | **97** | v3.0 |

**PE-3 평균: 93점** | **최고점: THERM-06 (97점)**

## 🔗 연계 도메인

| 코드 | 연계 포인트 |
|---|---|
| [PE-MEM](../prompts/bio/) | HBM 열설계 ↔ 메모리 아키텍처 통합 분석 |
| [PE-JV](../applied-cases/jv-fund/) | sCO2 냉각 시스템 투자 ROI 분석 |
| [PE-ICD](../prompts/) | 열해석 + 회로 설계 통합 |
| [PE-MFG](../applied-cases/) | 열관리 공정 최적화 |

## ⚡ 활용 명령어

```bash
# 단일 실행
PE-THERM-01을 실행해줘   → TIM 열저항 완전 분석
PE-THERM-06을 실행해줘   → TSV PDE 완전 분석

# 전체 체인 실행
PE-THERM 전체를 체인으로 실행해줘
→ THERM-01→02→03→04→05→06 순서
→ 최종 통합 Thermal Budget 리포트 생성

# PE-11 멀티에이전트 연동
PE-11 Master Multi-Agent System으로 HBM 열관리 종합 전략을 수행해줘

# PE-1 자동개선
PE-THERM-04를 PE-1로 분석해서 PE-3 점수 95+ 버전으로 업그레이드해줘

# PE-2 자동증식
PE-THERM-01에서 Variant A(HBM5), B(Chiplet), C(sCO2 냉각) 3종을 증식해줘

# PE-3 검증
pe-validate-all --domain PE-THERM
pe-metrics --domain PE-THERM
```

## 📊 PE-3 검증 이력

| 프롬프트 | 원본 점수 | 최적화 후 | 개선폭 | 검증일 |
|---|---|---|---|---|
| PE-THERM-01 | 67 | **95** | +28 | 2026-04-29 |
| PE-THERM-02 | 85 | **93** | +8 | 2026-04-29 |
| PE-THERM-03 | 81 | **91** | +10 | 2026-04-29 |
| PE-THERM-04 | 79 | **90** | +11 | 2026-04-29 |
| PE-THERM-05 | — | **92** | 신규 | 2026-04-29 |
| PE-THERM-06 | 92 | **97** | +5 | 2026-04-29 |
| **평균** | **80.8** | **93.0** | **+12.2** | — |

## 🗺️ 향후 로드맵

| 우선순위 | 과제 | 예상 추가 프롬프트 | 목표 PE-3 |
|---|---|---|---|
| ★★★★★ | HBM5 TSV 10k/mm² Variant 증식 | PE-THERM-06-A | 95+ |
| ★★★★☆ | CTE Mismatch 신뢰성 분석 신설 | PE-THERM-07 | 92+ |
| ★★★★☆ | Liquid Cooling ROI 분석 신설 | PE-THERM-08 | 90+ |
| ★★★☆☆ | sCO2 냉각 특화 프롬프트 신설 | PE-THERM-09 | 93+ |

---
**최초 작성**: 2026-04-29 10:42 KST | **버전**: v1.0 | **T-09 위치**: C-20
