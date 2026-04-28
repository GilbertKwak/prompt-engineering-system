# FU-Series 연동 JV 분석 프로프트

> **파일**: C-02_fu_series_adapter.md  
> **버전**: v1.0 | **작성일**: 2026-04-28  
> **페어링**: C-01 Master Prompt v3 기반 동작  
> **연관 레포**: [fu-semiconductor-thermal](https://github.com/GilbertKwak/fu-semiconductor-thermal)

---

## [PURPOSE]

FU-Series 보고서(FU-001~FU-025+)의 특정 섹션을 입력으로 받아,  
성능 데이터 기반의 **JV 타당성 검증 및 파트너 후보 매칭**을 자동화합니다.

---

## [INPUT SCHEMA]

```yaml
FU_Number:    {FU_NUMBER}       # e.g. FU-008, FU-015
Section:      {SECTION}         # Market-Analysis | Technical-Specs | Cost-Model
Target_JV:    {JV_TARGET}       # e.g. 다이렉트 리퀴드 쿨링 JV
Depth:        {depth}           # Quick | Standard | Deep
```

---

## [TASK CHAIN]

### Step 1 · FU 데이터 추용
```
FU-{FU_NUMBER}의 {SECTION} 데이터를 추출하라:
- 핵심 기술 수치 (성능 / 비용 / 효율)
- 마켓 사이즈 (서울반도체 시장 기준)
- 기술 성숭도 (TRL 1~9)
```

### Step 2 · JV 타당성 스코어링
```
아래 기준으로 1~5점 스코어링:
- 기술 성숙도 (TRL 기반)
- 시장 진입 시점 (3년 이내 가능 여부)
- 파트너십 신선요인 (특정 국내사와의 신뢰 관계)
- 수익성 (IRR / NPV 개추)
```

### Step 3 · 파트너 후보 매칭
```
FU 기술 데이터를 기반으로 아래를 수행:
1. 해당 기술 종속성이 높은 국내 OEM/OSAT 3개 선정
2. 해외 연구소/기업 3개 선정
3. 각사의 JV 가치제안 포인트 정리
```

### Step 4 · Notion/GitHub 출력
```
산출물:
- Notion 페이지 업데이트용 MD 블록
- GitHub Issue 생성 명령어 (gh issue create)
- FU 보고서 PR 직접 연동 코멘트
```

---

## [EXAMPLE USAGE]

```
다음 조건으로 FU-Series 연동 JV 분석을 수행하라:
- FU_Number: FU-008
- Section: Technical-Specs
- Target_JV: 다이렉트 리퀴드 쿨링 + 다이아리코드 TIM JV
- Depth: Standard
```

---

## [VALIDATION]

- [ ] PE-1: FU 보고서 단락 번호 출처 명시
- [ ] PE-3: 해당 기술의 대체 솔루션 시나리오 포함
- [ ] FU 모듈 연결 정합성 확인

---

## [RELATED FILES]

- C-01: Master Prompt v3 (JV 공통 프레임워크)
- C-03: B-Star eCO2 전용 프로프트
- [fu-semiconductor-thermal repo](https://github.com/GilbertKwak/fu-semiconductor-thermal)
