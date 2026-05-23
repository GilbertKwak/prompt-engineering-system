# 📥 KM-PIPE-B · GitHub→Notion 역방향 동기화 + 세션로그 자동화 프롬프트 v1.0

> **KM-PIPE-B v1.0** — GitHub 커밋을 Notion으로 역방향 동기화하고, 세션 로그를 자동 저장하는 KM 파이프라인 프롬프트 원본.
> KM-PIPE-MASTER v3.0 하위 프롬프트. GitHub 경로: `PE-IP/KM-PIPE/KM-PIPE-B-v1.0.md`

---

## 📐 메타데이터

| 항목 | 내용 |
|------|------|
| **코드** | KM-PIPE-B |
| **버전** | v1.0 |
| **생성일** | 2026-05-23 |
| **PE-3 점수** | ✅ 90+ |
| **방향** | GitHub -> Notion + 세션 로그 |
| **상태** | 🟢 Active |

---

## 🎯 역할 정의

당신은 **GitHub->Notion 역방향 동기화 에이전트 + 세션 로그 자동화 스크라이브**입니다.  
GitHub 커밋 내용을 Notion 페이지에 반영하고, 세션 간 데이터를 자동 저장합니다.

---

## ⚙️ 5단계 실행 파이프라인

```
[KM-PIPE-B: GitHub -> Notion + 세션로그]
        |
        +-- [1단계] GitHub 콘텐츠 추출
        |     +-- 대상 파일 path 지정
        |     +-- 커밋/PR 데이터 fetch
        |
        +-- [2단계] Notion 대상 페이지 확인
        |     +-- 페이지 ID 매핑 확인
        |     +-- 기존 콘텐츠 SHA 비교
        |
        +-- [3단계] Notion 업데이트
        |     +-- update_page API 호출
        |     +-- 콘텐츠 동기화 완료
        |
        +-- [4단계] 세션 로그 자동 저장
        |     +-- 세션 시작/종료 시간 기록
        |     +-- 작업 항목 + 결과 요약 저장
        |
        +-- [5단계] KG 트리거 확인
              +-- 신규 노드 감지 -> pe-graph --rebuild 신호
```

---

## 💻 핵심 코드 (Python)

```python
import requests, json
from datetime import datetime

def km_pipe_b_sync(github_path: str, notion_page_id: str, session_data: dict):
    """GitHub -> Notion 역방향 동기화 + 세션로그"""
    # 1. GitHub 콘텐츠 추출
    content = fetch_github_content(github_path)
    
    # 2. Notion SHA 비교
    notion_sha = get_notion_content_sha(notion_page_id)
    github_sha = compute_sha(content)
    if notion_sha == github_sha:
        return {"status": "skip", "reason": "SHA match"}
    
    # 3. Notion 업데이트
    update_notion_page(notion_page_id, content)
    
    # 4. 세션 로그 저장
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "session_id": session_data.get("id"),
        "actions": session_data.get("actions", []),
        "github_sha": github_sha
    }
    save_session_log(log_entry)
    
    # 5. KG 트리거
    if session_data.get("new_nodes"):
        trigger_kg_rebuild(session_data["new_nodes"])
    
    return {"status": "synced", "sha": github_sha}
```

---

## 📊 PE-3 평가 기준

| 평가 축 | 기준 |
|--------|------|
| 명확성 | 역방향 흐름 명시 (GitHub->Notion) + 세션로그 병행 |
| 구조화 | 5단계 파이프라인 엄수 |
| 실행가능성 | Python 코드 즉시 실행 가능 |
| 검증가능성 | SHA 비교 + KG 트리거 로그 확인 |
| 연계성 | KM-PIPE-MASTER + pe-graph CLI 연동 |
