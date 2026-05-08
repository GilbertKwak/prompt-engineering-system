# 🔧 PE-TECH · tech-chain 프롬프트 디렉토리

> **도메인**: C-35 PE-TECH · 기술해설-진단-설계 통합 라이브러리 v1.0  
> **생성일**: 2026-05-08 | **PE-3 목표 평균**: 93

## 📁 포함 프롬프트

| 파일 | ID | 버전 | 역할 | PE-3 목표 |
|------|----|------|------|----------|
| SP-TECH-EXPLAIN-001.md | SP-TECH-EXPLAIN-001 | 2.0 | 기술 개념 해설 | 94 |
| SP-TECH-DIAGNOSE-001.md | SP-TECH-DIAGNOSE-001 | 2.0 | 기술 문제 진단 | 93 |
| SP-TECH-SOLUTION-001.md | SP-TECH-SOLUTION-001 | 2.0 | 기술 솔루션 설계 | 93 |

## 🔗 연계 도메인

- **PE-ARCH (C-34)**: 아키텍처 심화 확장
- **PE-EDU (C-08)**: 교육 콘텐츠 변환
- **PE-11**: 멀티에이전트 오케스트레이션

## ⛓️ 실행 체인

```
[문제 발생]
    ↓
SP-TECH-EXPLAIN-001  ← 개념 이해 필요 시
    ↓
SP-TECH-DIAGNOSE-001 ← 원인 규명
    ↓
SP-TECH-SOLUTION-001 ← 솔루션 설계
    ↓
[PE-11 오케스트레이터] ← 구현 태스크 분배
```

## 🧠 knowledge_graph 업데이트 예약

```bash
# +3 nodes: PE-TECH / SP-TECH-EXPLAIN-001 / SP-TECH-DIAGNOSE-001 / SP-TECH-SOLUTION-001
# +7 edges: C-35→PE-ARCH / C-35→PE-EDU / C-35→PE-11 /
#           EXPLAIN→DIAGNOSE / DIAGNOSE→SOLUTION / C-35→C-34 / C-35→T-09
pe-graph --rebuild --domain PE-TECH --delta v4.19
```

---

*Maintained by: GilbertKwak | Repo: prompt-engineering-system*
