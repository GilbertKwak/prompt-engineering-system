# PE-AI · AI Platform Strategy Library

**Domain:** AI-Platform  
**Hub:** C-28 PE-AI Library  
**Version:** v1.0  
**Created:** 2026-04-29  
**Status:** 🟢 Active  
**Notion Hub:** https://app.notion.com/p/35155ed436f08102bafbe7acba401e02  

---

## 디렉토리 구조

```
prompts/PE-AI/
├── README.md                    ← 이 파일
├── ai_001_v6.8_opt.md          ← AI-001-OPT (Global Base, PE-3: 95)
├── ai_001_kr_v6.8_opt.md       ← AI-001-KR  (KR Variant, PE-3: 94)
└── ai_001_global_v6.8.md       ← AI-001-GLOBAL (Multi-Country, PE-3: 93)
```

---

## 프롬프트 목록

| ID | 파일 | 설명 | PE-3 | 대상 |
|----|------|------|------|------|
| AI-001-OPT | ai_001_v6.8_opt.md | Global Base — Porter×Farrell×Thompson×Wu | 95 | 글로벌 |
| AI-001-KR | ai_001_kr_v6.8_opt.md | KR Regulatory Stack Override | 94 | 한국 |
| AI-001-GLOBAL | ai_001_global_v6.8.md | Multi-Country Comparative (US/EU/CN/JP/KR) | 93 | 다국가 |

---

## 생태계 연계

| 연계 도메인 | 연결 유형 | 가중치 |
|------------|----------|--------|
| PE-PWR | ecosystem_link | 0.85 |
| PE-MIN | ecosystem_link | 0.90 |
| PE-SEMI | ecosystem_link | 0.88 |
| PE-JV | ecosystem_link | 0.75 |
| PE-EQP | ecosystem_link | 0.82 |
| PE-11-MASTER | parent_system | 1.00 |

---

## knowledge_graph 반영

- **version:** v4.0
- **nodes:** 115 (+4 from v3.9)
- **edges:** 169 (+6 from v3.9)
- **신규 노드:** PE-AI-HUB / AI-001-OPT / AI-001-KR / AI-001-GLOBAL
- **신규 엣지:** PE-AI → PWR/MIN/SEMI/JV/EQP/PE-11

---

## 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| v1.0 | 2026-04-29 | C-28 PE-AI 신설, AI-001 3종 등록, kg v4.0 rebuild |
