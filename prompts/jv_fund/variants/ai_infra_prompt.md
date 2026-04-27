# AI 인프라·데이터센터 JV 분석 프롬프트 (Variant C)

> **버전**: v1.0 | **기준일**: 2026-04-27 | **기반**: master_prompt_v3.md  
> **PE-3 점수**: 90/100 | **연동 레포**: `global-semiconductor-ai-research`

---

## [목적]

AI 데이터센터 열관리 및 인프라 분야의 글로벌 JV 기회를 분석합니다.  
Hyperscaler(AWS/Azure/GCP/Meta)와의 JV 또는 OSAT/패키징 업체와의 기술 파트너십에 특화됩니다.

---

## [파라미터]

```yaml
TARGET_MARKET: "{target}"      # Hyperscaler | Edge-DC | Colocation | HPC
COOLING_TECH:  "{tech}"        # Liquid | Immersion | Air | Hybrid
CHIP_GEN:      "{chip_gen}"    # H100 | H200 | B200 | GB300 | Next-Gen
REGION:        "{region}"      # US | EU | KR | SEA | Global
PARTNER_TYPE:  "{partner_type}" # Hyperscaler | OSAT | IDM | Cooling-OEM
```

---

## [분석 프레임]

### AI DC 열관리 시장 분석
```
- AI 서버 전력밀도 추이 (kW/rack): 2023→2025→2027
- 데이터센터 냉각 시장 규모 (Global/KR)
- Blackwell/GB300 열관리 요구 사양 (TDP 기준)
- 액침냉각 vs 직접수냉(DLC) vs 공냉 비용 비교
```

### 파트너 후보 매핑
```
Tier 1 — Hyperscaler (수요처):
  AWS / Microsoft Azure / Google GCP / Meta
  → 열관리 솔루션 공급 JV 또는 공동 R&D

Tier 2 — 반도체/패키징 (기술 파트너):
  SK하이닉스 (HBM4), 삼성전자 MX, TSMC CoWoS
  → 패키지 수준 열관리 공동 개발

Tier 3 — 냉각 OEM (제조 파트너):
  Vertiv, Schneider Electric, Asetek
  → 냉각 장비 공동 생산 JV
```

### AI DC JV 구조 옵션
```
옵션 A: 기술 라이선스 + 공급 계약
  → 낮은 리스크, 빠른 수익화
  → 지분 없음, 장기 통제력 약

옵션 B: 합작법인 설립 (50:50)
  → 공동 R&D 투자, IP 공유
  → 의사결정 지연 리스크

옵션 C: 소수 지분 투자 + 기술 협약
  → 유연성 최대, 전략적 포지셔닝
  → 추천: Hyperscaler와의 초기 진입 시
```

---

## [출력 포맷]

```markdown
## AI Infra JV Analysis — {target_market} | {cooling_tech}

**칩 세대**: {chip_gen} | **지역**: {region}  
**PE-3 점수**: {pe3_score}/100 | **신뢰도**: {confidence_score}/100

### 시장 기회 요약
- 글로벌 AI DC 냉각 시장: {tam} ({year}, 출처: {source})
- 한국 시장 점유율 목표: {kor_target}%
- 핵심 드라이버: {drivers}

### 추천 JV 옵션 (1순위)
{recommended_jv_option}

### 파트너 Fit Score
| 파트너 | 유형 | Fit Score | 핵심 강점 | Red Flag |
|---|---|---|---|---|

### 기술 리스크 매트릭스
{tech_risk_matrix}

### 반대 시나리오 (PE-3)
{downside_scenario}

### 90일 실행 계획
{day90_plan}

### GitHub Issue 생성 항목
{github_issues}
```

---

## [검증 규칙]
- [ ] AI DC 전력밀도 수치 출처 명시 (PE-1)
- [ ] 칩 TDP 공식 사양 기반 (PE-1)
- [ ] Hyperscaler 발표 자료 인용 시 날짜 명시
- [ ] 반대 시나리오 (온디바이스 AI 성장 시 DC 수요 감소) 포함 (PE-3)
- [ ] confidence_score 출력 필수
