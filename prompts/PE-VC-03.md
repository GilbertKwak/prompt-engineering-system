# PE-VC-03 · Layer 3 — 심층 분석 엔진 (선택 3종 특화 적용)

## 메타데이터

| 항목 | 값 |
|------|----|
| Prompt ID | PE-VC-03 |
| Layer | 3 — Deep Analysis Engine |
| **적용 도메인** | **AI Ecosystem Intelligence (PE-AI-ECO) / PE-SEMI / PE-DD — 3종 한정** |
| 실행 시점 | PE-VC-02 라우팅 패킷의 `layer3_escalate: true` 시 / 또는 직접 호출 |
| 버전 | v1.0 |
| 작성일 | 2026-05-17 |

---

## 역할 정의

PE-VC-03은 고복잡도·고불확실성 분석을 위한 **심층 추론 레이어**입니다.  
3종 도메인에만 선택 적용하여 **토큰 비용 vs 분석 깊이**의 최적 균형을 유지합니다.

---

## 도메인별 심층 모듈

---

### MODULE A — PE-AI-ECO (AI Ecosystem Intelligence)

#### A-1. 생태계 구조 매핑
```
[INPUT: AI 생태계 쿼리]
↓
계층 분해:
  L1 인프라: 칩(NVIDIA/AMD/자체개발) → 클라우드(AWS/Azure/GCP) → 네트워킹
  L2 플랫폼: 파운데이션 모델 → MLOps → 데이터 파이프라인
  L3 응용: 버티컬 AI → 에이전트 → AI 네이티브 SaaS
↓
경쟁구도 매핑: 수직통합도 × 시장점유율 × 해자강도
```

#### A-2. 기술 가속도 분석
```
[TECH_VELOCITY]
- 모델 성능 개선 곡선 (Scaling Law 적합도)
- 추론 비용 하락률 ($/token YoY)
- 오픈소스 vs 클로즈드 역학
- 정책/규제 리스크 벡터 (EU AI Act / EO 14110)
```

#### A-3. 투자 시그널 추출
```
[SIGNAL_EXTRACTION]
알파 신호 3종:
  SIG-A1: 밸류체인 병목 재편 (누가 가장 이득을 보는가)
  SIG-A2: 플랫폼 전환 비용 임계치 (락인 강도)
  SIG-A3: 차세대 아키텍처 전환 타임라인 (Transformer→Mamba/SSM 등)
```

---

### MODULE B — PE-SEMI (반도체 공급망 GNN)

#### B-1. GraphSAGE-3L 노드 상태 갱신
```
[GNN_UPDATE]
노드 피처 갱신:
  - importance: PageRank × 수요 탄력성
  - alpha_signal: 모멘텀 × 밸류에이션 Z-score
  - shock_propagation: 직접 1홉 + 간접 2홉 가중 평균

엣지 가중치 재계산:
  SUPPLY: 납기 리스크 × 점유율 집중도
  PROCESS: 공정 전환 비용 × 수율 민감도
  RISK: 지정학 지수 × 재고 버퍼 역수
```

#### B-2. 충격 시뮬레이션
```
[SHOCK_SIM] — 3시나리오
S1 (기준): 현 공급망 유지
S2 (충격): SMIC 수출규제 강화 → 삼성-TSMC 주문 재배분
S3 (극단): CoWoS 병목 + HBM 공급 부족 동시 발생

출력 지표:
  - HHI 변화량 ΔHerfindahl
  - 노드별 리스크 스코어 변화 (S1→S2→S3)
  - 포트폴리오 헤지 권고 (알파 상위 3종)
```

#### B-3. 선단 공정 로드맵 갱신
```
[ROADMAP_UPDATE]
- TSMC N2/A16 양산 일정 신뢰도
- Samsung SF2 수율 회복 가능성
- Intel 18A EUV 전환 타임라인
- ASML High-NA EUV 공급 제약
```

---

### MODULE C — PE-DD (Due Diligence 심층)

#### C-1. 재무 건전성 다층 진단
```
[FIN_DIAG]
Layer A (표면): PL / BS / CF 3종 표준 분석
Layer B (구조): 운전자본 효율 × ROIC 분해 × 레버리지 구조
Layer C (심층): 현금창출 지속성 × 수익 품질 × 숨겨진 부채

리스크 스코어링:
  RS = Σ(weight_i × normalized_metric_i)
  임계치: RS > 7.0 → HIGH RISK 플래그
  임계치: RS > 5.0 → MODERATE RISK
```

#### C-2. 밸류에이션 크로스체크
```
[VALUATION_MATRIX]
DCF (기본) vs EV/EBITDA (피어비교) vs 청산가치 (하방)
→ 3종 가중 평균: DCF 40% + EV/EBITDA 40% + 청산 20%
→ 괴리율 > 30% 시 재검토 플래그
```

#### C-3. 경영진 / 거버넌스 리스크
```
[GOVERNANCE_CHECK]
- 창업자-경영자 일치 여부
- 지분 구조 투명성
- 과거 재무보고 오류 이력
- ESG 리스크 (산업별 materiality 가중)
```

#### C-4. 출구 전략 매핑
```
[EXIT_MAPPING]
- IPO 가능성 (시장 사이클 × 섹터 멀티플 현황)
- 전략적 인수자 후보 3종 + 프리미엄 추정
- 2차 거래 유동성 (LP 포지션 규모 기준)
```

---

## 통합 출력 포맷

```yaml
# PE-VC-03 심층 분석 패킷
layer3_output:
  domain: "[PE-AI-ECO | PE-SEMI | PE-DD]"
  module_executed: ["A-1", "A-2", "A-3"]  # 실행된 서브모듈 목록
  key_findings:
    - finding: "[핵심 발견 1]"
      confidence: 0.XX
      action_signal: "[BUY|HOLD|AVOID|MONITOR]"
  risk_flags: []
  recommended_followup: "[후속 CMD 제안]"
  token_used: XXXX
```

---

## 에스컬레이션 기준 (PE-VC-02 → PE-VC-03)

| 조건 | 트리거 |
|------|--------|
| PE-AI-ECO 쿼리에 밸류체인 전방위 포함 | 자동 에스컬레이션 |
| PE-SEMI 공급망 충격 시뮬레이션 요청 | 자동 에스컬레이션 |
| PE-DD 리스크 스코어 > 7.0 | 자동 에스컬레이션 |
| 사용자 명시적 `[DEEP]` 플래그 | 수동 에스컬레이션 |

---

## 품질 기준 (QA Gate)

- [ ] 모듈별 실행 완료 확인 (서브모듈 누락 없음)
- [ ] 신뢰도 confidence ≥ 0.75
- [ ] 액션 시그널 명시 (BUY/HOLD/AVOID/MONITOR 중 1종)
- [ ] 후속 CMD 제안 포함
- [ ] 토큰 사용 4,000 이하 (초과 시 모듈 우선순위화)
