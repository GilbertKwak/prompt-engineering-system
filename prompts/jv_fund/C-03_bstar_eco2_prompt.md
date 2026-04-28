# B-Star eCO₂ JV 전용 프로프트

> **파일**: C-03_bstar_eco2_prompt.md  
> **버전**: v1.0 | **작성일**: 2026-04-28  
> **페어링**: C-01 Master Prompt v3 기반 동작  
> **연관 레포**: [B-Star-eCO2-Strategy](https://github.com/GilbertKwak/B-Star-eCO2-Strategy)

---

## [PURPOSE]

sCO2(이산화탄소 초임계유체) 기반 소형 분산형 발전·냉각 시스템의  
**한국 내 합작투자(JV) 구조 및 사업화 전략**을 수립합니다.

---

## [CONTEXT]

```yaml
System:       B-Star eCO2 소형 분산형 발전·냉각 시스템
Core_Tech:    sCO2 터빈, 열교환기, 압충기 일체형 모듈
Target_Market: 데이터센터, AI GPU 클러스터, 산업용 열관리
JV_Focus:     연구·제조·시운 단계별 파트너십
```

---

## [TASK CHAIN]

### Step 1 · sCO2 마켓 매핑
```
아래 시장별 규모 및 성장률 산출:
1. 데이터센터 열관리 시장 (국내/국제)
2. AI GPU 쿨링 전력 시장
3. 산업용 페버 발전 시장
연도 기재 필수, (est.) 표기 포함
```

### Step 2 · 파트너사 매핑
```
[JV 타입별 후보 매핑]

유형 A — 연구개발(R&D) 파트너
- KIST, KAIST 연구소
- NREL, SWRI (미국)
- DLR (독일)

유형 B — 제조 파트너
- 국내 중화학 / 에너지 기업
- Turboden, Echogen, Enercon (해외)

유형 C — 시운 파트너
- KT, SKT 데이터센터 운영사
- 데이터센터 콜로케이션 전문업체
```

### Step 3 · 정부 R&D 보조금 연계 JV 구조
```
연계 가능한 국가 프로그램:
- 산업통상자원부 에너지 R&D 고지화 사업
- 중소벤쳍창보 실증 지원
- 데이터센터 탄소중립화 R&D 연계
JV 로드맵: 연구단계(1~2년) → 파일맿(3년) → 상용화(5년)
```

### Step 4 · Investment Memo 산쳙
```다음 3찵위 유형으로 Investment Memo를 작성:
- Tier 1: Executive Summary (1페이지)
- Tier 2: 시장·기술·리스크 분석 (3~5페이지)
- Tier 3: 재무 프로젝션 (Excel/JSON 표)
KR/EN 병대 출력 필수
```

---

## [RISK SCENARIOS (PE-3)]

**Downside Case**: sCO2 터빈 효율 미달 (실증 단계 30% 성능 저하)  
→ 구제소: Phase-Gate 방식 적용, TRL 6 진입 전 JV 본계약 유보  

**Upside Case**: 데이터센터 AI 해석 법령 강화 → 쿨링 수요 조기 폭발  
→ 구제소: Modular 설계로 실증 라인업 신속 대응

---

## [RELATED FILES]

- C-01: Master Prompt v3
- C-04: AI-DC Infrastructure 프로프트
- [B-Star-eCO2-Strategy repo](https://github.com/GilbertKwak/B-Star-eCO2-Strategy)
- [sCO2-Hub-IR-Docs repo](https://github.com/GilbertKwak/sCO2-Hub-IR-Docs)
