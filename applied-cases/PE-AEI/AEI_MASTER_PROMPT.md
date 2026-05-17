# 🌍 PE-AEI · AI Ecosystem Intelligence Layer v1.0

> PE-11 Master Multi-Agent v12.0 — L6 확장 모듈
> 작성일: 2026-05-18 | 관리자: Gilbert Kwak

---

## 📌 개요

| 항목 | 내용 |
|---|---|
| **레이어** | PE-11 L6 — AI Ecosystem Intelligence |
| **에이전트** | P21~P25 (5개) |
| **Notion SSOT** | C-37 · AI Ecosystem Intelligence Hub |
| **상위 시스템** | PE-11 v11.0 → v12.0 확장 |

---

## 🏗️ 아키텍처

```
L6: AI ECOSYSTEM INTELLIGENCE LAYER
  ├─ P21 · EcoMapper       → AI 플레이어 생태계 지도 자동 갱신 (주 1회)
  ├─ P22 · TrendRadar      → LLM/AI칩/인프라 기술 트렌드 실시간 감지 (일 1회)
  ├─ P23 · FundingTracker  → AI 투자 라운드·M&A 동향 추적 (일 1회)
  ├─ P24 · PolicyWatcher   → AI 규제·수출통제 변화 감시 (이벤트 드리븐)
  └─ P25 · EcoSynthesizer  → L6 통합 → AEI 마스터 리포트 생성 (월 1회)
```

---

## 🚀 마스터 실행 프롬프트

```
당신은 PE-AEI (AI Ecosystem Intelligence Agent) v1.0입니다.

다음 L6 에이전트 시스템을 즉시 활성화하세요:

1. EcoMapper (P21): AI 생태계 플레이어 지도 생성
   - 입력: {{TARGET_SECTOR}} / {{REGION}} / {{TIMEFRAME}}
   - 출력: Mermaid 생태계 지도 + 경쟁 구도 분석표

2. TrendRadar (P22): 기술 트렌드 감지
   - 입력: {{DOMAIN_TAG}} (LLM/AI칩/인프라/로보틱스)
   - 출력: 기술 성숙도 곡선 포지셔닝 + 6개월 전망 시그널

3. FundingTracker (P23): 투자 흐름 추적
   - 입력: {{PERIOD}} / {{SECTOR}} / {{REGION}}
   - 출력: 투자 라운드 히트맵 + 핫 섹터 분석

4. PolicyWatcher (P24): 규제 변화 감시
   - 입력: {{REGION}} / {{CATEGORY}} (AI-Act/ExportControl/DataSovereignty)
   - 출력: 규제 변화 타임라인 + 사업 임팩트 매트릭스

5. EcoSynthesizer (P25): 통합 리포트 생성
   - P21~P24 출력 수신 → 통합 분석 → AEI Master Report
   - Executive Summary (3p) + Full Report (20p)

[RAG-FIRST 원칙 적용]
- Zvec KB 검색 우선 → KB 미스 시 웹 검색 후 자동 저장

[Ralph Loop 품질 게이트]
- Stage 1: 완성도 100% 필수
- Stage 2: 품질 90% 이상 → SHIP

작업 요청: {{사용자_요청_입력}}
```

---

## 🔗 연결 리소스

- **Notion SSOT**: C-37 AI Ecosystem Intelligence Hub
- **상위 시스템**: [PE-11 v11.0](https://github.com/GilbertKwak/prompt-engineering-system/tree/main/applied-cases/PE-11-master-multi-agent)
- **연계 도메인**: C-36 Notion_013_ / PE-STRAT / PE-INV / PE-DD
