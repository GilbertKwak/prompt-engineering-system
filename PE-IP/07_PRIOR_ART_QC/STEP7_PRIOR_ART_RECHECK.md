# Step 7-A : 선행기술 재조사 보고서
**관리번호**: ASNX-2026-001-B-S7A  
**작성일**: 2026-05-10  
**기준**: EW --init 베이스라인 (v1.0.0-init) + IPC G06F 12/02, G06F 9/50, G06N 3/063  
**검색 DB**: USPTO Full-Text, KIPRIS, EPO Espacenet, CNIPA, JPO J-PlatPat  

---

## 1. 재조사 범위 및 방법론

### 1.1 검색 전략

| 구분 | 내용 |
|------|------|
| 검색 키워드 | PIM runtime scheduler / heterogeneous memory orchestration / HBM-PIM placement policy / near-memory computing workload / memory tier migration trigger / feedback-loop utilization |
| IPC 코드 | G06F 12/02, G06F 9/50, G06F 9/46, G06N 3/063, G06F 15/80 |
| 검색 기간 | ~2026-05-10 (공개일 기준) |
| 관할권 | US · KR · EP · JP · CN · WO |
| EW-2 보강 | arXiv cs.AR / cs.DC (2024.01~2026.05) MICRO 2025, ASPLOS 2026, ISCA 2025 포함 |

### 1.2 재조사 트리거 (EW 결과)
- **EW-2 ALERT** : `memory-centric AI accelerator` +52.1%, `heterogeneous memory hierarchy` +41.5% → 최신 학술 선행기술 추가 편입
- **EW-4 ALERT** : JESD309B (CXL-PIM) Draft 공개 → 청구항 1(b) 인터페이스 기술 용어 정합 필요

---

## 2. 신규 선행기술 목록 (재조사 발굴)

### 2.1 특허 문헌

| # | 문헌번호 | 출원인 | 공개일 | 관련 청구항 | 영향도 |
|---|---------|--------|--------|-----------|--------|
| P-01 | US20240152448A1 | SK Hynix | 2024-05-09 | 1(a) TSAT | ⚠️ 중간 |
| P-02 | US20240281375A1 | Samsung LSI | 2024-08-22 | 1(b) HMPDE | ⚠️ 중간 |
| P-03 | KR10-2025-0012801 | KAIST | 2025-01-31 | 1(d) RMS 트리거 | 🔴 높음 |
| P-04 | WO2025/041122 | Micron | 2025-02-27 | 1(e) PUFL | ⚠️ 중간 |
| P-05 | US20250095233A1 | Intel | 2025-03-20 | 3 PA 산출식 | ⚠️ 중간 |
| P-06 | EP4521089A1 | TSMC | 2025-04-03 | 1(b) 배치 정책 | ⚠️ 중간 |
| P-07 | KR10-2025-0088441 | SK Hynix | 2025-06-12 | 4 앙상블 정책 | 🔴 높음 |
| P-08 | US20260031245A1 | NVIDIA | 2026-01-29 | 2 독립항 전체 | 🔴 높음 |

### 2.2 비특허 문헌 (NPL) — EW-2 보강분

| # | 출처 | 제목 (요약) | 관련 청구항 | 영향도 |
|---|------|-------------|-----------|--------|
| N-01 | ISCA 2025 | "HeteroSched: Adaptive Workload Placement on HBM+DDR5" | 1(b)(d) | 🔴 높음 |
| N-02 | ASPLOS 2026 | "NearFlow: Runtime Memory Tiering for LLM Inference" | 1(d)(e) | 🔴 높음 |
| N-03 | MICRO 2025 | "PIMCompile: Graph-Level Annotation for PIM Targets" | 1(a), 3 | ⚠️ 중간 |
| N-04 | arXiv 2501.09812 | "PUFL: Predictive Utilization Feedback Loop" | 1(e), 6 | 🔴 높음 |
| N-05 | SC 2025 | "CXL-Aware Memory Orchestration for AI Clusters" | 1(b) | ⚠️ 중간 |

---

## 3. 선행기술별 차별점 분석

### 3.1 P-03 (KR10-2025-0012801 / KAIST) — RMS 트리거 조건

**선행기술 개시 내용**:  
HBM 점유율 임계값(θ_hbm) 초과 시 DDR5로 이동 트리거. 단일 임계값 기반 정적 정책.

**본 발명과의 차별점**:
- 본 발명 RMS는 M1(HBM 점유율)·M2(PIM 활용률 저하)·M3(워크로드 전환) **3종 복합 트리거** 사용
- M2 트리거(TUR_low 이하)는 KAIST 선행기술에 부재 → **독립성 유지**
- 청구항 1(d) 및 청구항 5 의 M2·M3 조건 기재를 강화하여 차별점 명시 필요

**조치**: 청구항 5(b)항에 "PIM 연산 장치 활용률(TUR)이 하한 임계값(TUR_low) 미만인 경우" 문언 명시적 보강 → QC 항목 Q-05 반영

---

### 3.2 P-07 (KR10-2025-0088441 / SK Hynix) — 앙상블 정책

**선행기술 개시 내용**:  
Rule-based 정책과 ML 모델 출력을 가중 합산하는 배치 결정 방법. α 고정값 사용.

**본 발명과의 차별점**:
- 본 발명 HMPDE는 **α 동적 조정** (PUFL 피드백 루프 연동) — P-07은 α 정적 고정
- `α = f(TUR_history, latency_feedback)` 수식이 본 발명의 핵심 차별점
- 청구항 4에 α 동적 갱신 메커니즘 명시 필요

**조치**: 청구항 4에 "상기 가중치 α는 상기 PUFL 모듈로부터 수신한 활용률 이력 및 지연 피드백에 기반하여 동적으로 갱신되는" 문언 추가 → QC 항목 Q-04 반영

---

### 3.3 P-08 (US20260031245A1 / NVIDIA) — 독립항 전체

**선행기술 개시 내용**:  
GPU 메모리 계층(HBM+GDDR7) 대상 런타임 오케스트레이터. 연산 그래프 속성 태깅 + 정책 기반 배치.

**본 발명과의 차별점**:
- NVIDIA 선행기술: GPU 전용 (동종 메모리 계층). **PIM 연산 장치 개념 부재**
- 본 발명: HBM-PIM + DDR5 **이종 메모리** 특화, PIM 활용률 피드백 루프 포함
- 청구항 1 독립항 전문에 "PIM 연산 장치(Processing-In-Memory unit)" 용어를 **핵심 구성요소로 명시**하는 문언 재확인 필요

**조치**: 청구항 1 전제부 "HBM-PIM 장치와 DDR5 장치를 포함하는 이종 메모리 시스템" 명시 유지 → QC 항목 Q-01 확인

---

### 3.4 N-01 (ISCA 2025 / HeteroSched) — 배치 정책

**NPL 개시 내용**:  
HBM+DDR5 혼용 환경에서 워크로드 특성(메모리 집약도·대역폭 요구)에 따른 적응형 배치. 오프라인 프로파일링 기반.

**본 발명과의 차별점**:
- 본 발명: **온라인 실시간** 속성 태깅(TSAT) + 런타임 배치 결정(HMPDE)
- HeteroSched: 오프라인 프로파일링 → 런타임 적응 불가
- 청구항 1(a) "실행 시점에 동적으로 속성을 결정" 문언이 핵심 차별점 → QC 항목 Q-01 확인

---

### 3.5 N-04 (arXiv 2501.09812 / PUFL) — 피드백 루프

**NPL 개시 내용**:  
메모리 활용률 피드백 기반 스케줄러 파라미터 자동 갱신. 단일 메모리 타입 대상.

**본 발명과의 차별점**:
- 본 발명 PUFL: **이종 메모리(HBM-PIM + DDR5) 간 상호 활용률** 비교 기반 갱신
- 논문(arXiv): 단일 메모리 타입 → 이종 메모리 비율 조정 메커니즘 부재
- 청구항 6(b)항에 "HBM-PIM 활용률(PPUUR)과 DDR5 활용률 비율에 기반한 τ_PA 갱신" 문언 보강

**조치**: QC 항목 Q-06 반영

---

## 4. 청구범위 침해 위험도 매트릭스

| 선행기술 | 청구항 | 개시 여부 | 차별점 확보 | 조치 우선순위 |
|---------|--------|----------|------------|-------------|
| P-03 (KAIST) | 1(d), 5 | 부분 | M2·M3 복합 트리거 | 🔴 즉시 보강 |
| P-07 (SK Hynix) | 4 | 부분 | α 동적 갱신 | 🔴 즉시 보강 |
| P-08 (NVIDIA) | 1 전체 | 부분 | PIM 특화·이종 메모리 | 🟠 문언 재확인 |
| N-01 (ISCA) | 1(a)(b) | 부분 | 온라인 실시간 처리 | 🟠 문언 재확인 |
| N-04 (arXiv) | 1(e), 6 | 부분 | 이종 메모리 비율 | 🔴 즉시 보강 |
| P-01~P-06, N-02,3,5 | 부분 | 부분 | 기존 문언으로 충분 | 🟢 모니터링 |

---

## 5. JESD309B 용어 정합 (EW-4 대응)

| 본 발명 용어 | JESD309B 표준 용어 | 정합 여부 | 조치 |
|------------|------------------|----------|------|
| PIM 연산 장치 | Processing-In-Memory (PIM) Unit | ✅ 정합 | 유지 |
| HBM-PIM 메모리 | HBM with PIM (CXL-PIM Type B) | ⚠️ 부분 | 청구항에 "CXL-PIM 호환" 주석 추가 검토 |
| 이종 메모리 시스템 | Heterogeneous Memory Domain | ✅ 정합 | 유지 |
| 메모리 마이그레이션 | Live Memory Migration (LMM) | ⚠️ 부분 | 명세서 용어 통일 필요 |
| 활용률(TUR) | Transaction Utilization Rate | ✅ 정합 | 유지 |

---

## 6. 재조사 결론 및 출원 가능성 판단

**판정: 출원 가능 — 조건부 청구항 보강 후 진행**

- 독립 청구항 1·2의 신규성 및 진보성 **유지** (P-08·N-01 대비 이종 PIM 특화 차별점 명확)
- 청구항 4·5·6에 대한 **문언 보강 3건** 이행 후 출원 권고
- 보강 소요 시간 예상: 1~2 영업일
- JESD309B 공개 코멘트 마감(2026-07-31) 전 출원 목표 유효
