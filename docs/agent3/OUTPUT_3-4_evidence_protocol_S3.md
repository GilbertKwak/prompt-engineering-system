# §3 Evidence 수집 프로토콜 — OUTPUT 3-4 베이지안 방법론

**작성일**: 2026-05-02 | **버전**: 1.0 | **작성자**: Gilbert

---

## 3.1 증거 유형 분류 체계

| 코드 | 카테고리 | 빈도 | 주요 소스 | World 민감도 |
|------|----------|------|-----------|-------------|
| E-POL | 정책·규제 | 비정기 | BIS, USTR, MOFCOM | A↑, C↓ |
| E-MKT | 시장·실적 | 분기 | IR, SEMI, IDC | C↑, A↓ |
| E-GEO | 지정학 | 주간 | CSIS, 대만 국방부 | A↑ |
| E-SUP | 공급망 | 월간 | USGS, ASML, 세관 | A↑, C↓ |
| E-FIN | 금융 | 일간 | Bloomberg, Reuters | 전 World |

## 3.2 우도비(Likelihood Ratio) 산정 방법론

### 단계 1: 전문가 델파이 (n≥5명)
- 라운드 1: 각 World별 "이 증거가 해당 World에서 발생할 확률" 익명 추정
- 라운드 2: 중간값 공유 후 재추정 (표준편차 <15% 수렴 목표)
- 라운드 3: 합의 LR 확정

### 단계 2: 역사적 유추 보정

| 참조 사건 | 연도 | 유추 적용 |
|----------|------|----------|
| 일본 반도체 수출 규제 | 2019 | LR 보정 기준 E-POL |
| 우크라이나 전쟁 에너지 쇼크 | 2022 | E-SUP 상한 설정 |
| CHIPS Act 통과 | 2022 | E-POL World B 가중 |
| 화웨이 Mate 60 Pro | 2023 | E-MKT World A 상향 기준 |

### 단계 3: 신뢰도 가중치

```
confidence = (source_quality × 0.4) + (recency × 0.3) + (consensus × 0.3)

source_quality: 공식 정부=1.0, IR=0.95, 분석기관=0.80, 미디어=0.60
recency:        <1주=1.0, 1~4주=0.90, 1~3개월=0.75, >3개월=0.60
consensus:      복수 소스 일치=1.0, 단일=0.80
```

## 3.3 업데이트 트리거 규칙

### 정기 업데이트 (분기)
- 시점: 분기 실적 시즌 종료 후 2주 이내
- 필수 증거: E-MKT (SK하이닉스, TSMC, Nvidia 실적)

### 비정기 업데이트 (중대 이벤트, 48시간 내)
1. 대만 ADIZ 침범 월 20회 초과 (3개월 연속)
2. 중국 희토류 수출 월 전년비 -50% 초과
3. 미국 수출통제 신규 품목 15개/분기 초과
4. 주요국 관세율 ±10%p 이상 변동
5. EW-01~EW-15 중 CRITICAL 3개 이상 동시 발생

## 3.4 검증 코드

```python
assert abs(sum(posterior.values()) - 1.0) < 1e-6
assert all(0.0 <= p <= 1.0 for p in posterior.values())
assert max(posterior.values()) <= 0.95  # 단일 World 독점 경계
```

## 3.5 관련 파일

- `code/agent3/bayesian_update.py` — Bayesian Engine + Evidence 번들
- `code/agent3/monte_carlo_sim.py` — N=10,000 MC 시뮬레이션
- `output/bayesian_history.csv` — 업데이트 이력
- `output/bayesian_posterior.json` — 최신 사후확률
