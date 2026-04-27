# 🌐 PE-NBD · GBR (Global Business Research) v2.0

> PE-NBD 프롬프트 라이브러리의 **글로벌 비즈니스 리서치 특화 모듈**

---

## 📌 개요

| 항목 | 내용 |
|---|---|
| **ID** | PE-NBD-GBR-v2.0 |
| **포지션** | PE-NBD chain-04 글로벌 경쟁분석 심화 확장판 |
| **특화** | 5개 언어권 (한/영/일/중/유럽) 동시 분석 |
| **PE-3 점수** | Before 55점 → After **92점** |
| **언어 버전** | KR + EN |
| **Notion 페이지** | [🌐 GBR v2.0](https://www.notion.so/34f55ed436f0815abe52d1e70d0ffd6b) |

---

## 🔗 Chain 연결도

```
PE-NBD-01 (IR 보고서)
    ↓
PE-NBD-02 (핵심가치 추출)
    ↓
PE-NBD-03 (누락요소 진단)
    ↓
PE-NBD-04 (글로벌 경쟁분석 일반)
    ↓ [심화 분기]
[GBR v2.0] ← 이 디렉토리 (5개 언어권 특화)
    ↓
PE-NBD-05 (3-Expert 리스크)
    ↓
PE-NBD-06 (실행 로드맵)
```

---

## 📁 파일 구성

| 파일 | 내용 |
|---|---|
| `GBR-v2.0-KR.md` | 한국어 최적화 프롬프트 전문 (v2.0) |
| `GBR-v2.0-EN.md` | 영어 최적화 프롬프트 전문 (v2.0) |
| `README.md` | 사용 가이드 + Chain 연결도 (이 파일) |

---

## 🚀 빠른 시작

### 1. 단독 실행 (기본)
```
GBR v2.0 실행:
business_summary = [신사업 개요 3~5문장]
industry_sector  = [산업 분류]
target_geography = [목표 시장]
```

### 2. NBD 체인 연동 (심화)
```
PE-NBD chain-04 심화 (GBR v2.0):
chain_input      = {{PE-NBD-03.output}}
business_summary = [내용]
→ QualityGate 3단계 통과 → chain-05 pass
```

### 3. JV 특화 실행
```
GBR v2.2-JV 실행:
모드 = 합작투자 파트너 탐색
business_summary = [JV 대상 사업 내용]
```

---

## ✅ QualityGate 3단계

| Gate | 기준 | 미달 시 |
|---|---|---|
| Gate 1 | 경쟁사 9개 이상 식별 | 보완 후 재실행 |
| Gate 2 | 5개 언어권 각 1개 이상 포함 | 해당 언어권 재조사 |
| Gate 3 | ScoreCard 합계 ≥ 8점 | Depth 섹션 보완 |

---

## 📊 ScoreCard 기준

| 항목 | 배점 | 기준 |
|---|---|---|
| Coverage | 2점 | 5개 언어권 모두 포함 여부 |
| Depth | 3점 | 경쟁사당 6개 항목 완비 여부 |
| Action | 5점 | 시사점이 구체적 액션과 연결 여부 |
| **합계** | **/10** | **8점 미만 시 재분석 권고** |

---

## 🗂️ 관련 링크

| 링크 | 내용 |
|---|---|
| [Notion GBR v2.0](https://www.notion.so/34f55ed436f0815abe52d1e70d0ffd6b) | Notion SSOT 페이지 |
| [PE-NBD 라이브러리](https://www.notion.so/34f55ed436f08162b162e53607cf8bc0) | 부모 페이지 |
| [T-09 Mother Page](https://www.notion.so/34a55ed436f0814d9cffe6a2f0816e29) | 프롬프트 엔지니어링 시스템 |
| [prompt-engineering-system](https://github.com/GilbertKwak/prompt-engineering-system) | GitHub 레포 |

---

*최초 작성: 2026-04-27 | 버전: v2.0 | 관리자: Gilbert Kwak*
