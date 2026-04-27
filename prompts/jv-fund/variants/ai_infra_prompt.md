# AI Infrastructure JV 전용 프롬프트

> **버전**: v1.0 | **날짜**: 2026-04-28  
> **부모 프롬프트**: `../master_prompt_v3.md`  
> **대상 레포**: GilbertKwak/global-semiconductor-ai-research

---

## [PURPOSE]

AI 데이터센터 열관리 인프라 분야의 글로벌 JV 기회를  
반도체 열관리 기술(AstraChips 포함) 관점에서 분석하는 전용 프롬프트.

---

## [CONTEXT]

```yaml
Domain: AI-Infrastructure-Thermal
Target_Segment: {segment}    # HPC | Cloud | Edge | Sovereign-AI
Thermal_Solution: {solution} # Liquid-Cooling | Immersion | sCO2 | Hybrid
Chip_Platform: {platform}    # H100 | GB200 | MI300 | Custom-ASIC
Region: {region}             # Korea | US | Middle-East | Southeast-Asia
```

---

## [SPECIALIZED TASK CHAIN]

### Step 1 ▸ AI DC 열관리 시장 규모
- 글로벌 AI DC 냉각 시장 (2024~2030 CAGR)
- 칩 TDP 상승 추세 (H100: 700W → GB200: 1200W+)
- 액침냉각/직접액냉(DLC) 채택률 전망

### Step 2 ▸ AstraChips 포지셔닝
- HBM Salvage 기반 열관리 솔루션 차별화
- 경쟁사 대비 TCO 절감 효과
- 싱가포르 HoldCo → 한국 R&D OpCo → 미국 Sales 구조 활용

### Step 3 ▸ 글로벌 파트너 매핑
- Tier-1 하이퍼스케일러 (AWS, Google, MS Azure, Naver Cloud)
- ODM/OEM 파트너 (Wiwynn, Inventec, Foxconn)
- 국내 SI/EPC (삼성SDS, SK C&C, LG CNS)

### Step 4 ▸ JV 수익 모델
- SaaS형 Thermal-as-a-Service
- 장기 유지보수 계약 (MRO)
- 기술 라이선스 + 로열티

---

## [OUTPUT]

- AI Infra JV Investment Thesis (KR/EN)
- AstraChips-Strategy 레포 연동 분석 초안
- 파트너십 제안서 목차

```bash
# AstraChips 레포에 JV 이슈 생성
gh issue create \
  --repo GilbertKwak/AstraChips-Strategy \
  --title "[JV] AI-DC 열관리 파트너십 분석" \
  --label "strategy,jv-analysis,ai-infra" \
  --body "Master Prompt v3 기반 AI Infra JV 분석"
```

---

*Parent: master_prompt_v3.md | Repo: prompt-engineering-system*
