# AI Infrastructure JV Fund Prompt

> **Version:** v1.0  
> **Date:** 2026-04-28  
> **Domain:** AI Data Center Thermal Management  
> **Linked Repos:** fu-semiconductor-thermal · AstraChips-Strategy  

---

## [DOMAIN CONTEXT]

AI 가속기 및 대규모 데이터센터의 열관리 솔루션 분야 JV 파트너십 발굴 및 펀드 구조 설계 전용 프롬프트입니다.

**핵심 영역:** 액침냉각 · 직접액냉(DLC) · 냉각판(Cold Plate) · TIM · Vapor Chamber  
**타겟 고객:** 하이퍼스케일러 (AWS · Google · Microsoft · 네이버 · 카카오)  

---

## [CONTEXT PARAMETERS]

```yaml
DOMAIN: "AI-DC-Thermal"
COOLING_TECH: "{tech}"          # ImmersionCooling | DLC | ColdPlate | Hybrid
TARGET_CHIP: "{chip}"           # H100 | B200 | HBM3E | HBM4 | Custom-ASIC
DEPLOY_SCALE: "{scale}"         # 1MW | 10MW | 100MW | Hyperscale
GEO: "{geo}"                    # KR | US | APAC | Global
```

---

## [ANALYSIS CHAIN]

### Step 1: AI 열관리 시장 현황 (2025~2030)
- 글로벌 데이터센터 냉각 시장 규모 및 CAGR
- AI 가속기 발열 밀도 트렌드 (H100 → B200 → 차세대)
- 액침냉각 vs DLC 기술 전환 속도
- 국내 하이퍼스케일러 투자 계획 (2025~2027 (est.))

### Step 2: 파트너 역량 매핑
```
냉각 솔루션: Vertiv · Asetek · CoolIT · Submer · 국내 열관리 스타트업
HBM 연동: SK하이닉스 · 삼성전자 HBM 파트너 생태계
EPC/시공: 롯데건설 · 삼성물산 데이터센터 사업부
```

### Step 3: AstraChips 연계 JV 시나리오
```
[Option A] AstraChips + 글로벌 냉각사 기술 JV
  → HBM Salvage + Thermal 패키징 통합 솔루션

[Option B] AstraChips + 국내 데이터센터 운영사 JV
  → 열관리 서비스(ThermalaaS) 모델

[Option C] 단독 사업화 후 전략적 M&A 유도
  → 기술 자산 축적 후 Exit
```

### Step 4: 리스크 매트릭스
| 리스크 | 가능성 | 영향도 | 대응 |
|---|---|---|---|
| NVIDIA 공급망 수직통합 | High | High | 멀티벤더 전략 |
| 액침냉각 표준화 지연 | Medium | Medium | 하이브리드 설계 |
| 국내 규제 (데이터센터 에너지) | Medium | Low | 에너지효율 인증 선취 |

### Step 5: 반대 시나리오 (PE-3)
- **Downside:** AI 투자 버블 붕괴 → DC 신규 발주 급감
- **Mitigation:** 기존 데이터센터 레트로핏(Retrofit) 시장 집중

---

## [OUTPUT]

```json
{
  "domain": "AI-DC-Thermal",
  "market_size_2026": "... (est., Source: Gartner 2025)",
  "top_jv_scenarios": [],
  "astrachips_integration_options": [],
  "risk_matrix": [],
  "recommended_jv_structure": "...",
  "next_actions": []
}
```

---

## [VALIDATION]
- [ ] PE-1: AI DC 시장 수치 출처 명시
- [ ] PE-3: Downside 시나리오 포함
- [ ] AstraChips-Strategy 레포 최신 상태 반영

---

*Parent: prompts/jv_fund/master_prompt_v3.md*  
*Linked: GilbertKwak/fu-semiconductor-thermal | GilbertKwak/AstraChips-Strategy*
