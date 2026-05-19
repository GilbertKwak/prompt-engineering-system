# 🕸️ KG Builder Agent Domain

> Knowledge Graph Delta 자동 생성 도메인

## 담당 스크립트

`automation/kg_delta_generator.py`

## 노드 타입

`COMPANY` | `TECHNOLOGY` | `PERSON` | `EVENT` | `METRIC` | `REGULATION`

## 엣지 타입

`DEVELOPS` | `ACQUIRES` | `COMPETES_WITH` | `PARTNERS_WITH` | `REGULATES` | `INVESTS_IN` | `EW_SIGNAL`

## 버전 트리거

| 타입 | 조건 |
|---|---|
| Major (x.0) | EW CRITICAL 또는 paradigm shift |
| Minor (x.x) | 신규 노드 5개 이상 |
| Patch (x.x.x) | 속성 업데이트만 |

## 현재 KG 버전

`v4.26` (2026-05-20 기준)
