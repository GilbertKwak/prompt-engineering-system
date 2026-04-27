# AI Infrastructure JV Prompt v1.0

> **Version**: v1.0  
> **Date**: 2026-04-27  
> **Parent**: `master_prompt_v3.md`  
> **Purpose**: AI 데이터센터 열관리 인프라 특화 JV 분석  

---

## [CONTEXT]

```yaml
domain: AI-DC
focus_areas:
  - GPU/HBM 발열 밀도 분석
  - 액침냉각(Immersion) / 직접액냉(DLC) JV 구조
  - 데이터센터 PUE 최적화 비즈니스 케이스
  - NVIDIA H100/B200 클러스터 열관리 요구사항
```

---

## [TASK]

```
1. AI 데이터센터 열관리 시장 분석
   - GPU 발열 밀도 트렌드 (W/cm² 기준)
   - 글로벌 데이터센터 냉각 시장 규모 및 CAGR
   - 액침냉각 vs 직접액냉 vs 공냉 비용 비교

2. 핵심 파트너 매핑
   - 냉각 솔루션: Vertiv, Asetek, Iceotope, CoolIT
   - 데이터센터 오퍼레이터: Equinix, Digital Realty, KT, LG CNS
   - HBM/반도체: SK Hynix, Samsung, Micron
   - AI 클라우드: Hyperscalers (AWS, Azure, Google, Naver)

3. JV 구조 설계
   - 냉각 기술 라이선스 JV
   - 데이터센터 공동 개발 JV
   - HBM 패키징 + 냉각 통합 JV

4. 재무 모델링
   - CAPEX/OPEX 비교 (공냉 대비 액침냉각)
   - PUE 개선에 따른 운영비 절감액
   - IRR/NPV 추정 (fund_size 기준)
```

---

## [CHAIN]

```
Step 1 → AI DC 열관리 시장 현황
  - GPU 발열 밀도: H100 → B200 → Rubin 트렌드
  - 냉각 방식별 시장 점유율 변화

Step 2 → 파트너 역량 매트릭스
  - 기술 × 시장 접근성 × 재무 안정성

Step 3 → JV 구조 3가지 옵션 비교

Step 4 → 재무 모델 (간이)
  - 투자 수익 시뮬레이션 (Base / Bull / Bear)

Step 5 → 실행 로드맵 + GitHub Issue 명령어
```

---

## [OUTPUT FORMAT]

```markdown
## AI Infrastructure JV 분석

### 시장 규모
| 세그먼트 | 2024 | 2028 | CAGR | 출처 |
|---|---|---|---|---|

### 파트너 매트릭스
| 파트너 | 역량 | 시장접근 | 재무 | JV 유형 |
|---|---|---|---|---|

### JV 구조 비교
| 옵션 | 구조 | 장점 | 단점 | 권장 |
|---|---|---|---|---|

### 재무 시뮬레이션
| 시나리오 | IRR | NPV | 회수기간 |
|---|---|---|---|
| Base Case | | | |
| Bull Case | | | |
| Bear Case | | | |
```

---

## [VALIDATION]

- [ ] PE-1: GPU 발열 수치 출처 명시 (NVIDIA 공식 자료)
- [ ] PE-1: 시장 규모 수치 출처 명시
- [ ] PE-3: Bear Case (AI 투자 버블 붕괴 시나리오) 포함
- [ ] 에너지 규제 리스크 (각국 데이터센터 PUE 규제) 플래그
