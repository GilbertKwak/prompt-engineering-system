# agents/ew_detection — EW Detection Agent

## 개요

Early Warning(EW) 탐지 에이전트의 프롬프트 및 설정 디렉토리입니다.

## 탐지 레이어

| Layer | 방법 | 활성화 조건 |
|-------|------|------------|
| 1 | 정량 임계값 (Metric Threshold) | 항상 실행 |
| 2 | 키워드 휴리스틱 (Keyword Heuristic) | 메트릭 미발견 시 폴백 |
| 3 | LLM 추론 (선택적) | `enabled: true` 시 |

## EW 심각도 기준

- **CRITICAL**: 패러다임 전환, 즉각 대응 필요
- **HIGH**: 2-4주 내 전략 수정
- **MEDIUM**: 모니터링 강화
- **LOW**: 트렌드 기록
- **NONE**: 정상 운영
