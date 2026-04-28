---
id: VARIANT_FU_SERIES
title: FU-Series 연동 JV 분석 Variant
version: "1.0"
domain: FU-Thermal
tags: [fu-series, thermal, hbm, semiconductor, jv]
description: FU-Series 보고서 데이터 기반 JV 타당성 재검증 Variant
created_at: 2026-04-28
status: active
---

# FU-Series 연동 JV 분석 Variant v1.0

> [출처: GilbertKwak/fu-semiconductor-thermal, 2026년 기준]

## CONTEXT

이 Variant는 `fu-semiconductor-thermal` 레포지토리의 FU-Series 보고서 데이터를
글로벌 JV 펀드 분석에 직접 연결합니다.

## INPUT

```
FU 보고서 번호: {FU_NUMBER}        # 예: FU-008
연동 섹션: {SECTION}               # Market Analysis | Technical Specs | Cost Model
분석 목적: {PURPOSE}               # JV 타당성 검증 | 파트너 역량 매핑 | IP 가치 산정
```

## TASK

1. 지정 FU 보고서 섹션에서 핵심 기술·시장 데이터 추출
2. 추출 데이터를 JV Master Prompt Step 1~3에 자동 매핑
3. 기술 성숙도(TRL) 기반 JV 리스크 재산정
4. FU 보고서와 외부 시장 데이터 간 격차(Gap) 분석 [출처 명시 필수]

## OUTPUT

- FU-Series 기반 JV Feasibility Score (0~100)
- 연동 데이터 매핑 테이블 (Notion MD 포맷)
- GitHub PR 본문 초안 (`fu-semiconductor-thermal` → `prompt-engineering-system` 참조)

## 리스크 / 반대 시나리오 (PE-3)

- **단점**: FU 보고서 데이터는 2026년(est.) 기준으로 시장 변동성 미반영 가능
- **반대 시나리오**: FU 기술이 상용화 전이라면 JV 대신 전략적 투자(minority stake)가 유효
- **대안**: FU 보고서 데이터 부족 시 IDC 2025 Semiconductor Outlook 보고서 병행 활용 [출처: IDC, 2025]
