# v3.0 — Tech/VC LP 테크니컬 버전 프롬프트

> **작성일**: 2026-03-01  
> **프롬프트 유형**: LP 세그먼트 분화  
> **적용 프로젝트**: AstraChips AI Infrastructure Fund I

## 📥 프롬프트 원문

```
<q>"Tech/VC LP용 더 테크니컬 버전</q>
작성한 내용을 한글과 영어로 별개로 작성
```

## 🎯 핵심 지시사항
1. 기술 이해도 높은 LP(VC, CVC, 엔지니어링 배경 투자자) 대상
2. ExaFLOPS → 하드웨어 스택(HBM, CoWoS, Glass) 연결 설명
3. 반도체 기술 용어(TSV, RDL, Line/Space µm) 적극 사용
4. **한국어·영어 각각 별도 완전 문서로 작성** (번역본 아님)

## 🔧 기술 파라미터
```yaml
hbm_transition: "HBM3E → HBM4/4E"
packaging: "CoWoS 2.5D + Glass Substrate"
line_space: "2/2 µm target (vs ABF 5/5 µm)"
base_die_node: TSV pitch 최적화
smr_load_profile: High load factor, Low curtailment
power_cost_metric: "$/GPU-hour, $/token (not just $/MWh)"
cluster_scale: "100-300 MW per AI campus"
```

## 📐 섹션 구조
```
1. Fund Overview → AI compute stack physical layer 투자
2. Market & Technical Thesis → ExaFLOPS → HW bottleneck 분석
3. Strategy & Portfolio Architecture → HW 스택 기반 배분
4. Technical Edge & Partner Ecosystem → Corning, OSAT, GPU vendors
5. Return Profile & Risk Envelope → Sharpe 1.4+, stress scenarios
6. Why It's Relevant for Tech/VC LPs → VC 포트폴리오 보완성
```
