# P25 · EcoSynthesizer — Ecosystem Intelligence Synthesizer v1.0

> PE-AEI L6 | 작성일: 2026-05-18 | 관리자: Gilbert Kwak

---

## 📌 에이전트 명세

| 항목 | 내용 |
|---|---|
| **에이전트 ID** | P25 / EcoSynthesizer |
| **레이어** | L6 — AI Ecosystem Intelligence |
| **역할** | P21~P24 출력 통합 → AEI 마스터 리포트 자동 생성 |
| **연계 에이전트** | P13 ReportPlanner → P14 SectionWriter → P15 VisualGenerator |
| **갱신 주기** | 월 1회 Full Report + 주 1회 요약 리포트 |
| **출력 저장** | Notion C-37 AEI Report DB + GitHub outputs/aei-reports/ |

---

## 🎯 역할

P21(생태계 지도) + P22(기술 트렌드) + P23(투자 흐름) + P24(규제 변화)
4개 에이전트 출력을 통합하여 경영진용 AI Ecosystem Intelligence Report를
자동으로 생성하고 Notion + GitHub에 동시 저장한다.

---

## 📤 출력 포맷

### Executive Summary (3페이지)
```
1. AI 생태계 핵심 변화 (이번 달 Top 5)
2. 투자 흐름 하이라이트
3. 규제 리스크 Alert
4. 전략적 권고사항 (3가지)
```

### Full Report (20페이지)
```
Section 1: AI 생태계 플레이어 지도 (EcoMapper P21)
Section 2: 기술 트렌드 레이더 (TrendRadar P22)
Section 3: 투자 흐름 분석 (FundingTracker P23)
Section 4: 규제 환경 변화 (PolicyWatcher P24)
Section 5: 통합 전략 시사점
Section 6: 다음 달 모니터링 항목
```

---

## 🔄 실행 프롬프트

```
[EcoSynthesizer P25 활성화]

역할: 당신은 AI 생태계 인텔리전스 통합 에이전트입니다.

입력 데이터:
- P21 EcoMapper 출력: {{ECO_MAP_DATA}}
- P22 TrendRadar 출력: {{TREND_DATA}}
- P23 FundingTracker 출력: {{FUNDING_DATA}}
- P24 PolicyWatcher 출력: {{POLICY_DATA}}

실행 단계:
1. 4개 에이전트 출력 수신 및 교차 분석
2. Conflict Resolver (P12): 에이전트 간 데이터 충돌 해결
3. P13 ReportPlanner: Executive Summary + Full Report 목차 설계
4. P14 SectionWriter×5: 섹션별 병렬 작성
5. P15 VisualGenerator: Mermaid 시각화 통합
6. Ralph Loop Stage 1+2: 완성도·품질 게이트
7. 최종 출력:
   - Executive Summary (3p) → Notion C-37 저장
   - Full Report (20p) → Notion C-37 + GitHub 저장
   - P19 Notifier: 완료 알림 발송
```

---

## 📊 월간 리포트 자동화 스케줄

```yaml
# 매월 마지막 영업일 오후 6시 KST
schedule:
  full_report: "monthly-last-business-day 18:00 KST"
  weekly_summary: "every-friday 09:00 KST"
  policy_alert: "event-driven"  # 규제 변화 감지 즉시
```
