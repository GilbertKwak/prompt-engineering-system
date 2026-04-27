# B-Star eCO2 JV 전용 프롬프트

> **버전**: v1.0 | **날짜**: 2026-04-28  
> **부모 프롬프트**: `../master_prompt_v3.md`  
> **대상 레포**: GilbertKwak/B-Star-eCO2-Strategy

---

## [PURPOSE]

sCO2(초임계 CO2) 기반 소형 분산 발전·냉각 시스템의  
한국 사업화를 위한 JV 파트너십 전략 전용 프롬프트.

---

## [CONTEXT]

```yaml
Domain: sCO2-Energy-System
Application: {application}    # DataCenter-Cooling | District-Heating | Industrial
Target_Region: {region}       # Korea | Southeast-Asia | Middle-East
JV_Type: {jv_type}            # Technology-License | Manufacturing | Full-JV
Government_Grant: {grant}     # MOTIE | KETEP | NRF | None
```

---

## [SPECIALIZED TASK CHAIN]

### Step 1 ▸ sCO2 기술 파트너 매핑
- 한국 내 sCO2 터빈/열교환기 기술 보유 기업 (KEPCO, 두산에너빌리티 등)
- 해외 파트너: Echogen (미국), Siemens (독일), Toshiba (일본)
- 국내 정부출연연: KAERI, KIER, KIST

### Step 2 ▸ 데이터센터 냉각 수요 연계 분석
- 국내 하이퍼스케일 DC 열 배출량 현황
- sCO2 폐열 회수 시너지 정량화 (kWh/year)
- B-Star 솔루션의 경쟁 우위 포인트

### Step 3 ▸ 정부 R&D 보조금 연계 JV 구조
- MOTIE 탄소중립 기술개발 프로그램 연계
- 한-EU 녹색기술협력 프레임워크 활용
- 보조금 수령 주체 및 JV 법인 구조 최적화

### Step 4 ▸ 투자 조건 설계
- 초기 투자 규모 및 단계별 증자 계획
- Break-Even Point 분석
- Exit 전략 (IPO / M&A / Strategic Buy-Out)

---

## [OUTPUT]

- 3-Tier Investment Memo (Executive / Technical / Financial)
- KR/EN 병기 버전
- B-Star-eCO2-Strategy 레포지토리 Issue 생성 초안

```bash
# B-Star 레포에 JV 분석 이슈 생성
gh issue create \
  --repo GilbertKwak/B-Star-eCO2-Strategy \
  --title "[JV] sCO2 파트너십 전략 분석" \
  --label "strategy,jv-analysis" \
  --body "Master Prompt v3 기반 sCO2 JV 분석 결과"
```

---

*Parent: master_prompt_v3.md | Repo: prompt-engineering-system*
