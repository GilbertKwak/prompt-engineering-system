# 🔄 Notion Sync Agent Domain

> Notion C-31 페이지 자동 동기화 도메인

## 담당 스크립트

`automation/notion_c31_updater.py`

## 대상 페이지

- **C-31**: `34a55ed436f0814d9cffe6a2f0816e29` (T-09 Mother Page)

## 업데이트 방식

- Notion Blocks API **append** 방식 (기존 내용 보존)
- 50블록 배치 처리
- EW 심각도에 따른 callout 배경색 자동 변경

## Callout 색상

| EW 레벨 | 색상 |
|---|---|
| CRITICAL | 🔴 red |
| HIGH | 🟠 orange |
| MEDIUM | 🟡 yellow |
| LOW | 🔵 blue |
| NONE | 🟢 green |

## Secrets 필요

- `NOTION_API_KEY` — Notion Integration Token
- Notion 페이지에 Integration 연결 필수
