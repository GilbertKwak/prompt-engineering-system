# Section D — Risk Analysis
> **T-11 | Glass/HBM 투자전략 | v2.0 | 2026-04-26**

---

## D.1 리스크 레지스터 (전체)

| ID | 리스크 | 타입 | 확률 | 영향 | Score | 대응 전략 |
|----|--------|------|------|------|-------|----------|
| R-01 | 대만해협 군사 긴장 | 지정학 | 20% | 높음 | 🔴 0.32 | Type C 비중 확대, CoWoS 대체처 계약 |
| R-02 | HBM 가격 -40% (AI Winter) | 시장 | 15% | 높음 | 🔴 0.24 | 오프테이크 minimum take-or-pay 조항 |
| R-03 | Glass Substrate 양산 지연 | 기술 | 25% | 중간 | 🟡 0.20 | JV 마일스톤 기반 단계적 납입 |
| R-04 | US CHIPS Act 정책 변화 | 규제 | 10% | 중간 | 🟡 0.10 | EU Chips Act 이중 포지셔닝 |
| R-05 | TSMC CoWoS 슬롯 취소 | 계약 | 15% | 높음 | 🟡 0.18 | ASE/Amkor 백업 계약 사전 체결 |
| R-06 | Micron CB 전환 미실현 | 재무 | 20% | 낮음 | 🟢 0.08 | 쿠폰 수익으로 하방 보호 |
| R-07 | 한국 지정학 리스크 | 지정학 | 15% | 중간 | 🟡 0.15 | 분산 투자 구조로 노출 제한 |

---

## D.2 스트레스 테스트 5종 (Agent-2 검증)

### ST-1: 대만해협 긴장 고조
```
트리거: 대만 해협 군사 충돌 발생
영향:
  - Type B MOIC: 8.90x → 3.5x (CoWoS 전면 중단)
  - Type A MOIC: 4.1x → 2.8x (부품 수입 차질)
  - Type C MOIC: 11.50x → 15.2x (미국 내재화 가속)
Portfolio MOIC: 6.43x → 5.2x (-19%)
대응: C 비중 즉시 +15% 리밸런싱
```

### ST-2: AI Winter (수요 급감)
```
트리거: 2027 H1 AI 모델 성능 정체 + 기업 AI 투자 동결
영향:
  - HBM 수요 -60% → Type B MOIC: 8.90x → 2.1x
  - Glass Substrate 수요 연기 → Type A MOIC: 1.11x
  - Micron 주가 -50% → Type C CB 전환 포기, 쿠폰만 수취
Portfolio MOIC: 6.43x → 2.8x (-56%)
대응: Type B 오프테이크 조기 청산 옵션 확보
```

### ST-3: HBM 공급과잉 (2027 Q2)
```
트리거: Samsung/Micron HBM4 증설 가속 → 가격 -35%
영향:
  - Type B 유통마진 압축 → MOIC: 8.90x → 5.8x
  - Type A 영향 제한적 (장기 계약)
Portfolio MOIC: 6.43x → 5.1x (-21%)
대응: 오프테이크 계약 가격 인덱싱 조항 삽입
```

### ST-4: US/EU 규제 강화
```
트리거: 반도체 수출통제 강화 + CHIPS Act 보조금 축소
영향:
  - Type C Amkor 지분가치 -20%
  - EU Chips Act 대체 수혜로 부분 상쇄
Portfolio MOIC: 6.43x → 5.9x (-8%)
대응: 이중 상장 + EU 거점 추가
```

### ST-5: Glass 기술 표준화 실패
```
트리거: Intel Glass Core 실패 → 업계 ABF 회귀
영향:
  - Type A JV 가치 급락 → MOIC: 1.11x → 0.6x (손실)
  - B/C는 영향 없음
Portfolio MOIC: 6.43x → 5.8x (-10%)
대응: Type A 투자 단계적 실행, 기술 마일스톤 KPI 설정
```

---

## D.3 포트폴리오 통합 노출도

```
가중 병목 노출도 계산:
  Type A: VS(Glass) 2.02 × 40% = 0.808
  Type B: VS(HBM) 3.33 × 35% = 1.166 (일부)
         + VS(CoWoS) 1.85 × 35% = 0.648 (일부)
  Type C: VS(Amkor) 1.2 × 25% = 0.300

Portfolio 통합 노출도: 1.785 (MEDIUM)
임계값: >2.5 HIGH, 1.5~2.5 MEDIUM, <1.5 LOW
```

---

## D.4 동적 리밸런싱 트리거

| 트리거 | 임계값 | 액션 |
|--------|--------|------|
| HBM 가격 하락 | -25% QoQ | Type B → C 15% 이동 |
| 대만 해협 긴장 지수 | >70 (Economist) | Type C +10% 즉시 |
| Glass 양산 지연 | 2분기 이상 | Type A 추가 납입 동결 |
| Portfolio MOIC (추적) | <4.0x P50 | 전체 포지션 재검토 |
| IRR 실적 | <20% at 2yr | Exit 옵션 조기 행사 |

---
*→ 실행 로드맵: Section E | 부록: Section F*
