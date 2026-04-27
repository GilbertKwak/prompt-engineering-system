# 🔷 AI Infrastructure JV Prompt v1.0

> **파일**: `prompts/jv_fund/ai_infra_v1.md`  
> **버전**: v1.0 | **날짜**: 2026-04-27  
> **도메인**: AI Data Center Thermal Management JV  
> **검증룰**: PE-1 + PE-3

---

## [PURPOSE]

AI 데이터센터 열관리 솔루션 관련 JV 기회를 스크리닝하고, HBM/반도체 공급망과 연계한 투자 분석 수행.

---

## [PARAMETERS]

```
- [COOLING_TYPE]  : Liquid | Immersion | sCO2-Hybrid | Air+Liquid  (필수)
- [HBM_GEN]       : HBM2e | HBM3 | HBM3e | HBM4  (필수)
- [DC_SCALE]      : Hyperscale | Enterprise | Edge  (기본값: Hyperscale)
- [STAGE]         : Screening | Due Diligence | Structuring  (필수)
- [LANG]          : KR | EN | Bilingual  (기본값: Bilingual)
```

---

## [TASK CHAIN]

### Step 1 | AI DC 냉각 시장 분석
- 글로벌 AI DC 냉각 시장 규모 (TAM, 연도 명시)
- HBM {HBM_GEN} 기준 열밀도 요건 (W/mm²)
- {COOLING_TYPE} 솔루션 시장 점유율

### Step 2 | 한국 하이퍼스케일러 투자 현황
- 삼성/SK/KT/네이버 데이터센터 투자 계획
- HBM 공급망 연계 냉각 솔루션 수요
- 정부 AI 인프라 지원 정책

### Step 3 | JV 파트너 매핑

| 역할 | 국내 후보 | 해외 후보 | 시너지 |
|---|---|---|---|
| 냉각 기술 보유사 | | | |
| HBM 패키징 연계 | | | |
| DC 운영사 | | | |
| 열관리 소재 | | | |

### Step 4 | JV 구조 옵션

**Option A**: 기술 JV (공동 R&D + IP 공유)  
**Option B**: 상업 JV (공동 영업 + 수익 분배)  
**Option C**: 합작법인 (50:50 지분 + 공동 운영)

### Step 5 | 리스크 매트릭스 (PE-3 필수)

| 리스크 | 발생가능성 | 영향도 | Bear Scenario | 대응 |
|---|---|---|---|---|
| HBM 수요 둔화 | | | | |
| 냉각 기술 대체 | | | | |
| 규제 변화 | | | | |
| 파트너 이탈 | | | | |

---

## [OUTPUT — Investment Screening Report]

```markdown
## AI Infra JV Screening: {COOLING_TYPE} × {HBM_GEN}

### Executive Summary
(300자 이내)

### 시장 기회
- TAM: ... ({연도}년 기준)
- 성장률: ...% CAGR (est.)
- 핵심 드라이버: ...

### 추천 JV 구조
- 파트너: ...
- 지분: ...
- IP 조건: ...

### 리스크 요약
- Bull: ...
- Base: ...
- Bear: ...

### 다음 액션
1. ...
2. ...
3. ...
```

---

## [VALIDATION]

- [ ] PE-1: TAM 수치 출처 및 연도 기재
- [ ] PE-3: Bear Scenario 포함
- [ ] HBM 세대별 열밀도 수치 명시
- [ ] 삼성/SK하이닉스 공급망 연계 검토
- [ ] KR/EN 병기 확인
- [ ] GitHub SSOT 링크 기재
