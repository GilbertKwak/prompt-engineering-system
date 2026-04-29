# PE-MIN-001-v6.3-OPT
## 핵심광물 공급망 리스크 분석 프롬프트

---

### 메타데이터
```yaml
id:           PE-MIN-001
version:      6.3-OPT
pe3_score:    96/100
status:       ACTIVE — EW3 CRITICAL
last_updated: 2026-04-29
cmd_history:  [CMD-NEXT-03, CMD-MIN-01, CMD-MIN-01-REVALIDATE]
linked_nodes: [PE-PWR, PE-JV, PE-CHEM, PE-SEMI, PE-FIN, PE-SAT]
kg_version:   v4.0  # 114 nodes / 167 edges
```

---

### 파라미터
```javascript
COUNTRY_CODE:   CN | KR | AU | CA | DE | JP
mineral_focus:  Gallium | Germanium  // + 7종 크로스체크 (Li, Ni, Co, RE, Gr, Ga, Ge)
stage:          Alert
alert_period:   Weekly
output_lang:    KOR
model:          PE-MIN Firm State Machine × Bayesian SCP × Weaponized Interdependence
```

---

### Firm State Machine 정의
| State | 레이블 | 진입 조건 |
|-------|--------|----------|
| S1 | Normal | HHI < 2500, 가격 외교 비연동 |
| S2 | Tension | HHI 2500~5000 or EW1 발동 |
| S3 | Strategically_Instrumentalized | HHI > 5000 + EW2+EW3 발동 |
| **S4** | **Broken** | 비중국 대체공급 시장가동 불가 + EW3 CRITICAL |

현재 상태:
- **M06 Gallium: S3 → S4 경보** (EW3 CRITICAL 충족)
- **M07 Germanium: S3** (EW1+EW3 활성)

---

### EW 신호 정의
| ID | 신호 | 임계 |
|----|------|------|
| EW1 | 가격이 외교 이벤트에 반응 | 수출허가 발표 후 14일 내 ±15% |
| EW2 | 정부 오프테이크 +30%p (12개월) | MOFCOM 허가 건수 YoY |
| EW3 | 설비투자 ROI→지정학 전환 | 비중국 채산성 불가 + 보조금 의존 |
| EW4 | 배터리 Top-5 대체 공급망 발표 | IR 공시 키워드 탐지 |
| EW5 | IR 공시 "국가 안보" 언급 +200% | Earnings Call NLP |

---

### MIN-SIM-D 5년 시뮬레이션 결과 (2026–2030)

#### 갈륨 가격 궤적
| 연도 | 기본 ($/kg) | +ESG ($) | PE-MIN State |
|------|------------|---------|-------------|
| 2026 | 1,250 | 1,475 | S3 |
| **2027** | **1,580 피크** | **1,864** | S3→S4 경보 |
| 2028 | 1,420 | 1,676 | S3 |
| 2029 | 1,190 | 1,404 | S2→S3 완화 |
| 2030 | 980 | 1,156 | S2 (조건부) |

#### 게르마늄 가격 궤적
| 연도 | 기본 ($/kg) | +ESG ($) |
|------|------------|----------|
| 2026 | 6,200 | 7,564 |
| **2027** | **8,100 피크** | **9,882** |
| 2028 | 7,400 | 9,028 |
| 2029 | 6,800 | 8,296 |
| 2030 | 5,900 | 7,198 |

#### Bayesian SCP — 비가역 고착 확률
- 3종 광물 동시 충격 시나리오: **84%** (95% CI: [74%, 92%])

---

### PE-3 자동검증 스코어
```
총점: 120/125  →  96/100  ✅ PASS
이전: 92/100 (CMD-NEXT-03) → 현재 +4 개선
```

---

### 연계 에지 (knowledge_graph v4.0)
```
PE-MIN-001 ──EW3_CRITICAL──→  PE-PWR (AI-DC SiC/GaN 붕괴 연쇄, 84%)
PE-MIN-001 ──JV_ROI_SHIFT──→  PE-JV  (채산성→보조금 전환 감시)
PE-MIN-001 ──GE_LENS───────→  PE-CHEM (ASML EUV Ge 렌즈 수급)
PE-MIN-001 ──GAN_HEMT──────→  PE-SEMI (GaN HEMT·SiC MOSFET)
PE-MIN-001 ──EBITDA_IMPACT─→  PE-FIN  (배터리 3사 -11~-18pp)
PE-MIN-001 ──ESG_PREMIUM───→  PE-SAT  (CBAM Ga/Ge 프리미엄 +18~22%)
```

---

*PE-MIN 라이브러리 v1.0 | GilbertKwak/prompt-engineering-system*
