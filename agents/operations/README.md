# ⚙️ Operations Agent Domain

> 시스템 운영·모니터링·헬스체크 도메인

## 역할

- 파이프라인 헬스 모니터링
- 실패 알림 및 재시도 관리
- 로그 로테이션
- GitHub Actions 워크플로우 상태 추적

## 모니터링 대상

- `automation/` 스크립트 실행 상태
- Notion API 응답 시간
- Perplexity API 레이트 리밋
- GitHub Actions 잡 성공률

## 알림 설정

현재: 로그 파일 기반 (`logs/operations/`)

향후 계획:
- Slack Webhook 연동
- Email 알림
- Prometheus 메트릭 수집
