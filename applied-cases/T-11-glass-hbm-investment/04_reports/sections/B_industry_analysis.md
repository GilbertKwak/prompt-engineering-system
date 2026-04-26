# Section B — Industry Analysis
> **T-11 | Glass/HBM 투자전략 | v2.0 | 2026-04-26**

---

## B.1 시장 규모 및 성장 동인

### B.1.1 HBM 시장

| 지표 | 2024 | 2026E | 2028E | CAGR |
|------|------|-------|-------|------|
| HBM 시장 규모 | $14B | $28B | $55B | ~40% |
| HBM 비중 (전체 DRAM) | 8% | 18% | 32% | — |
| HBM4 비중 | 0% | 35% | 70% | — |
| SK hynix 점유율 | 53% | 50% | 48% | — |

**핵심 성장 동인:**
- AI 가속기(H100→B200→R100) 당 HBM 용량 2배씩 증가
- 데이터센터 AI CAPEX 2026E $350B → 2028E $500B+
- CoWoS/SoIC 패키징 병목으로 HBM 실질 가용량 < 수요

### B.1.2 Glass Substrate 시장

| 지표 | 2025 | 2027E | 2030E |
|------|------|-------|-------|
| Glass Substrate 시장 | $0.3B | $2.1B | $8.5B |
| ABF 대비 신호 손실 감소 | 기준 | -30% | -50% |
| 양산 준비 업체 | Samsung, Corning, AGC | +DNP, Ibiden | 5+ |

**구조적 우위:**
- 열팽창계수(CTE) 일치 → 패키지 신뢰성 30% 향상
- 배선 밀도 기존 ABF 대비 2x → 칩렛 통합 핵심
- Intel Glass Core 2026 양산 발표 → 업계 표준화 가속

---

## B.2 공급망 병목 분석 (Agent-2 VS 결과)

### B.2.1 TOP 3 병목 노드

| 순위 | 노드 | VS Score | 지리 집중 | 대체 가능성 |
|------|------|---------|----------|----------|
| 1 | **HBM 생산능력** | 3.33 🔴 | SK hynix 53%, Samsung 38% | 낮음 (2-3년) |
| 2 | **Glass Substrate** | 2.02 🔴 | Samsung/Corning/AGC 3사 | 중간 (1-2년) |
| 3 | **EUV 노광장비** | 1.99 🔴 | ASML 100% | 없음 |

> VS = BS × Geo_Risk × DSM

### B.2.2 DSM 매트릭스 핵심

```
HBM ──────→ Glass Substrate (DSM: 0.85)
HBM ──────→ CoWoS 패키징 (DSM: 0.90)
Glass ─────→ Chiplet 통합 (DSM: 0.75)
CoWoS ─────→ AI 가속기 출하 (DSM: 0.95)
```

**결론:** HBM·Glass·CoWoS는 **순차 의존 구조** → 하나의 병목이 전체 AI 가속기 공급을 차단

---

## B.3 경쟁 지형

### Type A (Glass 수직통합) 경쟁자
- **Intel:** Glass Core 자체 개발, 외부 판매 미정
- **Ibiden/DNP:** 일본 기업, 소형 배치 생산 단계
- **T-11 포지션:** Samsung+Corning+AGC 3사 JV → 규모 + 레시피 동시 확보

### Type B (패키징 레버리지) 경쟁자
- **TSMC:** CoWoS 내부화 가속, 외부 오프테이크 제한 중
- **ASE/Amkor:** 고급 패키징 CAPEX 투자 중이나 기술 격차 존재
- **T-11 포지션:** TSMC와 오프테이크 계약 → 희소 슬롯 선점

### Type C (US/EU 헤지) 경쟁자
- **Broadcom/Marvell:** 자체 패키징 추진
- **US CHIPS Act 수혜:** Micron(아이다호), GlobalFoundries(뉴욕)
- **T-11 포지션:** Amkor 지분 + Micron CB → 정책 보조금 업스트림 포착

---

## B.4 4-World 시나리오 프레임워크 (Agent-3)

| 시나리오 | AI 수요 | 지정학 | MOIC 영향 |
|---------|--------|--------|----------|
| W1: Tech Boom | 고성장 | 안정 | +30% |
| W2: Fragmented | 고성장 | 긴장 | -15% |
| W3: AI Winter | 저성장 | 안정 | -40% |
| W4: Crisis | 저성장 | 위기 | -65% |

**확률 가중 EV_MOIC = 6.149x** (W1: 40%, W2: 35%, W3: 20%, W4: 5%)

---
*→ 재무 모델 상세: Section C | 리스크 분석: Section D*
