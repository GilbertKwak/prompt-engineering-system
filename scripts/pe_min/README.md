# PE-MIN Scripts — 핵심광물 자동화 파이프라인

## 개요
`PE-MIN-001-v6.3-OPT` 프롬프트 시스템의 실행 스크립트 모음입니다.

## 스크립트 목록

### MOFCOM EW3 모니터링 (Weekly)
| 파일 | 역할 |
|------|------|
| `fetch_mofcom_licenses.py` | 중국 상무부(MOFCOM) 수출허가 데이터 수집 |
| `parse_ew_signals.py` | EW1~EW5 신호 파싱 및 GitHub Output 변수 생성 |
| `ew3_trigger_check.py` | EW3 임계값 판정 (전주 대비 -20%) |
| `notion_sync_ew_table.py` | Notion PE-MIN EW 모니터 테이블 갱신 |
| `kg_node_update.py` | knowledge_graph v4.0 노드 타임스탬프 갱신 |
| `send_ew3_alert.py` | Slack Webhook EW3 CRITICAL 알림 발송 |

### Gallium S4 월간 리포트 (Monthly)
| 파일 | 역할 |
|------|------|
| `collect_ga_production.py` | 비중국 갈륨 생산량 집계 (USGS·EU CRMA·JOGMEC·KCMA·NRCan) |
| `aggregate_production.py` | YoY 성장률 계산 및 누적 집계 |
| `s4_threshold_check.py` | 50톤/년 임계 달성 여부 판정 |
| `generate_s4_monthly_report.py` | Markdown/JSON 월간 리포트 생성 |
| `notion_push_monthly_report.py` | Notion PE-MIN Monthly Reports DB 푸시 |
| `pe_jv_partner_sync.py` | PE-JV 파트너 평가 인풋 Notion 동기화 |
| `deactivate_s4_alert.py` | 50톤 달성 시 S4 경보 비활성화 처리 |

---

## Secrets 설정 (GitHub Repository Settings)

```
MOFCOM_API_KEY          # 중국 상무부 API 키
USGS_API_KEY            # USGS MCS API 키
DERA_API_KEY            # 독일 연방지질자원연구소 API
NOTION_API_KEY          # Notion Integration Token
NOTION_PE_MIN_DB_ID     # Notion PE-MIN EW Monitor 테이블 DB ID
NOTION_PE_MIN_RPT_DB    # Notion PE-MIN Monthly Reports DB ID
NOTION_KG_DB_ID         # Notion knowledge_graph v4.0 DB ID
NOTION_PE_JV_DB_ID      # Notion PE-JV Partner Evaluation DB ID
SLACK_WEBHOOK_URL       # EW3 CRITICAL 알림 Slack Webhook
```

---

## knowledge_graph v4.0 노드/에지 현황

```
총 노드: 114
총 에지: 167

신규 추가 (CMD-MIN-03):
  노드 +3:
    - MIN-SIM-D-2026-PEAK    (시뮬레이션: 2027 갈륨 피크 시나리오)
    - MIN-SIM-D-S4-THRESHOLD (시뮬레이션: S4 전이 조건 노드)
    - MIN-SIM-D-RECOVERY     (시뮬레이션: 2029-2030 구조 복원 경로)
  에지 +4:
    - PE-MIN-001 ──EW3_CRITICAL──→ PE-PWR   (Bayesian SCP 84%)
    - PE-MIN-001 ──JV_ROI_SHIFT──→ PE-JV
    - PE-MIN-001 ──GE_LENS───────→ PE-CHEM
    - PE-MIN-001 ──GAN_HEMT──────→ PE-SEMI
```

---

## 워크플로우 트리거 요약

| 워크플로우 | 트리거 | 주기 |
|-----------|--------|------|
| `pe-min-ew3-mofcom-monitor.yml` | cron + manual | 매주 월요일 09:00 KST |
| `pe-min-ga-s4-monthly-report.yml` | cron + manual | 매월 1일 09:00 KST |

---

*PE-MIN 라이브러리 v1.0 | 2026-04-29 | GilbertKwak/prompt-engineering-system*
