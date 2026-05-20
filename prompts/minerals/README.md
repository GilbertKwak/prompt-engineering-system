# ⛏️ PE-MIN · 핵심광물 전략 붕괴 감시 라이브러리

**C-27 | v1.0 | 2026-04-29**

## 개요

핵심광물(Critical Minerals) 지정학·공급망 전략 붕괴를 실시간 감시하는 프롬프트 라이브러리.
Porter 5-Forces × Weaponized Interdependence × Sovacool 에너지전환 리스크 프레임워크 통합.

## 프롬프트 목록

| 파일 | ID | 유형 | PE-3 |
|---|---|---|---|
| `PE-MIN-001-v6.3-OPT.xml` | PE-MIN-001 | Base | 95/100 |
| `PE-MIN-001-CN.xml` | PE-MIN-001-CN | Variant-A (China) | 94/100 |
| `PE-MIN-001-GLOBAL.xml` | PE-MIN-001-GLOBAL | Variant-B (Global) | 93/100 |

## 커버리지

**광물 7종**: Lithium · Nickel · Cobalt · RareEarths · Graphite · Gallium · Germanium

**감시 기업 10개사**: Albemarle · SQM · Glencore · BHP · GanfengLithium · TianqiLithium · LynasRareEarths · POSCOFutureM · Umicore · BASF

## Firm State Machine

| State | 의미 |
|---|---|
| S1 Aligned | 기업↔국가 전략 일치, 수익성 정상 |
| S2 Tension | 수출통제 1건+ OR 오프테이크 30%+ |
| S3 Strategically_Instrumentalized | 오프테이크 50%+ OR 설비투자 ROI→지정학 전환 |
| S4 Broken | 시장 철수 봉인 OR 국유화 진행 |

## 생태계 연계

- **PE-PWR (C-26)**: 에너지전환 핵심자원 수요 교차
- **PE-JV (C-10)**: 광물 JV 파트너 리스크 평가 인풋
- **PE-CHEM (C-21)**: EUV 공정 Ga·Ge 공급망 연결
- **PE-SEMI (C-24)**: 반도체 공급망 Ga·Ge 전략 리스크

## Notion

https://app.notion.com/p/35155ed436f081d4aed4f7fc1958187f
