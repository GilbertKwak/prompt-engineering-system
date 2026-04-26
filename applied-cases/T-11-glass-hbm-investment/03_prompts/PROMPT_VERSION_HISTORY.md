# T-11 — 프롬프트 버전 이력 마스터 인덱스

> **SSOT:** 이 파일이 T-11 모든 프롬프트의 단일 진실 원본  
> **연결:** PE-9 `astrachips-lp-fund/PROMPT_VERSION_HISTORY.md` (LP Fund 산출물)  
> **마지막 갱신:** 2026-04-26

## 버전 인덱스

| 버전 | 날짜 | 유형 | 핵심 내용 | 산출물 | 상태 |
|------|------|------|----------|--------|------|
| v1.0 | 2026-03-01 | 투자구조 정의 | Core/Satellite/Hedge 3축 구조 + 티켓 사이즈 정의 | 투자구조 정의서 3종 | ✅ |
| v2.0 | 2026-03-01 | 재무모델 실행 | IRR/MOIC/NPV Python 모델 + 4개 시나리오 | portfolio_summary.csv, 차트 3종 | ✅ |
| v3.0 | 2026-04-26 | SSOT 아카이브 | Notion+GitHub 구조화, PE-9 연결, 재사용 가이드 | 이 레포 전체 | ✅ |

## 개별 프롬프트 파일
- [v1_core_satellite_hedge.md](./v1_core_satellite_hedge.md) — 투자구조 정의 프롬프트
- [v2_financial_model.md](./v2_financial_model.md) — 재무모델 실행 프롬프트

## 재사용 가이드
1. **유사 투자펀드 적용 시:** `v1_core_satellite_hedge.md` 의 YAML 파라미터 블록에서 `투자금·지분율·오프테이크` 값만 교체
2. **재무모델 확장 시:** `v2_financial_model.md` 에서 시나리오 비중 조정 후 `model_scaffold.py` 재실행
3. **LP 배포 자료 연계 시:** PE-9 레포 `v1_output_definition.md` 참조 (One-pager 구조 사전 정의)

## PE 시스템 연결
| PE ID | 역할 | 적용 범위 |
|-------|------|----------|
| PE-3 | 품질 검증 엔진 | 모든 v1~v3 산출물 검증 기준 |
| PE-7 | AI 자동화 설계 | model_scaffold.py 자동 실행 파이프라인 |
| PE-9 | LP Fund 프롬프트 | AstraChips One-pager / Q&A Handbook 연계 |
