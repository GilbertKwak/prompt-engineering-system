# agents/notion_sync — Notion Sync Agent

## 개요

Notion C-31 페이지 동기화 에이전트의 프롬프트 및 설정 디렉토리입니다.

## 핵심 설계 원칙

- **Append 전용**: 기존 Notion 콘텐츠는 절대 삭제하지 않음
- **50블록 배치**: API 레이트 리밋 준수
- **EW 색상 매핑**: 심각도별 callout 배경색 자동 설정

## EW 색상 규칙

| Severity | 배경색 | 아이콘 |
|----------|--------|--------|
| NONE | 🟢 green | ✅ |
| LOW | 🔵 blue | 🔵 |
| MEDIUM | 🟡 yellow | 🟡 |
| HIGH | 🟠 orange | 🟠 |
| CRITICAL | 🔴 red | ⚠️ |

## C-31 페이지 ID

`34a55ed436f0814d9cffe6a2f0816e29`
