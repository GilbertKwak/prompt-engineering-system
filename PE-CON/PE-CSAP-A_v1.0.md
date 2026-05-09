# PE-CSAP-A v1.0 — 반도체 특화 경쟁전략 분석 프롬프트 (SEMI Domain)

> **코드**: PE-CSAP-A | **도메인**: SEMI | **레벨**: L3 파생 (PE-3 기반)
> **버전**: 1.0 | **점수**: 94pt (PE-3 기준) | **생성일**: 2026-05-09
> **상위 콘텍스트**: CON-06 → CON-06-A (SEMI 특화) | **Ref**: PE-IP T-09 P4

---

## 1. 개요 (Overview)

PE-CSAP-A는 반도체 산업(SEMI 도메인) 특화 경쟁전략 분석 프롬프트로,
CON-06(일반 경쟁 분석)의 L3 파생 버전입니다.
HBM, NAND, Logic 등 반도체 세부 시장의 실시간 경쟁 동태를
구조화된 4단계 CSAP 프로토콜로 분석합니다.

**적용 범위**: HBM3E, HBM4, NAND, sCO2, CoWoS, High-NA EUV, BIS 규제 영향 분석

---

## 2. CSAP 4단계 프로토콜

### Stage 1 · Competitive Intelligence (CI)
```
[입력] 분석 대상 시장 세그먼트 + 기준 시점
[처리]
  - 주요 플레이어 포지션 맵핑 (점유율, 기술 성숙도, 양산 준비도)
  - 공급/수요 갭 정량 추정
  - 규제 리스크 플래그 (BIS EAR, CHIPS Act, 수출통제)
[출력] CI 매트릭스 (플레이어 × 차원)
```

### Stage 2 · Strategic Analysis (SA)
```
[입력] CI 매트릭스
[처리]
  - BCG Matrix 강제 분류
    · Star    : HBM4, High-NA EUV 대상 제품
    · Cash Cow: HBM3E, DDR5, 성숙 NAND
    · Question: sCO2, NOR Flash 신시장
    · Dog     : HBM2e, 구형 DRAM
  - Porter 5 Forces 반도체 특화 적용
  - 기술 격차(Gap) 정량화: 분기 단위 리드타임
[출력] SA 리포트 + BCG 포지션 테이블
```

### Stage 3 · Action Plan (AP)
```
[입력] SA 리포트
[처리]
  - 단기(0-6M) / 중기(6-18M) / 장기(18M+) 액션 분류
  - 투자 우선순위 스코어링 (ROI × 전략 중요도)
  - 리스크 매트릭스 (발생 가능성 × 영향도)
  - CoWoS / HBM4 병목 해소 경로 명시
[출력] 액션 플랜 테이블 (우선순위 정렬)
```

### Stage 4 · Portfolio Recommendation (PR)
```
[입력] AP 테이블
[처리]
  - Salvage 수익성 계산: 재고 × ASP × 기간
  - 포트폴리오 최적화 (Star 집중 / Dog 정리)
  - M&A / JV 시나리오 평가
  - 3가지 시나리오 (Base / Bull / Bear) 수익 추정
[출력] 포트폴리오 권고안 + 시나리오 테이블
```

---

## 3. HBM4 분석 프로토콜 (내장)

```yaml
hbm4_protocol:
  sk_vs_samsung:
    sk_hynix:
      양산_예정: "2025 Q4 ~ 2026 Q1"
      고객_확정: ["NVIDIA B300", "Google TPU v6"]
      기술_우위: "16-Hi TSV, 베이스다이 로직 내재화"
    samsung:
      양산_예정: "2026 H1 (지연 리스크 존재)"
      고객_확정: ["AMD MI350 후보"]
      기술_갭: "SK 대비 1~2분기 후행 추정"
  b300_spec:
    memory: "HBM4 × 8 스택"
    bandwidth: "9.6TB/s (시스템)"
    tdp: "~1000W (SXM)"
  cowos_bottleneck:
    현황: "TSMC CoWoS-L 웨이퍼 캐파 부족"
    해소_시점: "2026 Q2~Q3 추정"
    대안: "삼성 I-Cube, ASE 하이브리드"
  salvage_계산:
    공식: "재고수량 × ASP($) × 판매가능기간(분기)"
    hbm3e_예시: "2M 다이 × $35 × 4Q = $280M"
```

---

## 4. Self-Validation 로직

```
[검증 트리거] 출력 생성 후 자동 실행
[5차원 채점]
  D1 데이터 정확성    : /20
  D2 구조 완결성      : /20
  D3 전략 논리 일관성 : /20
  D4 실행 가능성      : /20
  D5 SEMI 도메인 특화 : /20
[임계값] 총점 < 92pt → 자동 재생성 (최대 2회)
[현재 점수] 94pt ✅
```

---

## 5. 사용 예시

```
입력: "HBM4 시장 2026년 경쟁 구도 분석 — SK하이닉스 vs 삼성전자"

→ Stage 1: CI 매트릭스 (SK 72% 점유 예측, 삼성 22%, Micron 6%)
→ Stage 2: BCG — SK-HBM4 Star, Samsung-HBM4 Question, HBM3E Cash Cow
→ Stage 3: 단기 — CoWoS 확보 계약 선행; 중기 — 베이스다이 자체 설계 투자
→ Stage 4: Base 시나리오 HBM4 매출 $12B (2026), Bull $18B, Bear $8B
```

---

## 6. 메타데이터

| 항목 | 값 |
|---|---|
| 코드 | PE-CSAP-A |
| 상위 콘텍스트 | CON-06-A (SEMI) |
| PE 레벨 | L3 파생 / PE-3 |
| 점수 | 94pt |
| 도메인 태그 | #SEMI #HBM4 #경쟁전략 #BCG #CoWoS |
| 다음 검토 | 2026-08-09 (90일) |
| 관리자 | Gilbert Kwak |
