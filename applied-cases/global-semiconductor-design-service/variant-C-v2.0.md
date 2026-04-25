# 변형 C v2.0 — 재무·투자 분석 집중형

## 메타데이터
- **버전**: 2.0.0
- **기반**: Master Prompt v2.0 OUTPUT FORMAT 확장 변형
- **목적**: D-3 투자·M&A 매력도 평가 심층화 + 비공개 데이터 신뢰도 관리
- **생성일**: 2026-04-25
- **변경 내역 (v1→v2)**: 비공개 데이터 신뢰도 등급 필드 추가, IPO/M&A 신호 탐지 로직 구체화

---

## ⚠️ v1.0 대비 핵심 변경사항

| 항목 | v1.0 문제 | v2.0 수정 |
|---|---|---|
| IPO 가능성 | 비공개 데이터, 기준 없음 | 신호 탐지 5개 지표 + confidence 등급 |
| M&A 타깃 | 판별 기준 없음 | eSilicon→Inphi→Marvell 패턴 적용 |
| 데이터 신뢰도 | 미표기 | ENUM(HIGH/MEDIUM/LOW) 강제 표기 |

---

## D-3 확장 필드

```yaml
d3_extended_schema:
  ipo_signal_detection:
    signals:
      - name: "Late_Stage_VC"
        description: "Series C 이상 펀딩 확인"
        source: "Crunchbase, PitchBook"
        weight: 2
      - name: "Revenue_Growth_CAGR"
        description: "3년 CAGR > 25%"
        weight: 2
      - name: "Tier1_Underwriter_Contact"
        description: "Goldman, Morgan Stanley, JPM 접촉 기록"
        source: "LinkedIn, news"
        weight: 3
      - name: "Governance_Upgrade"
        description: "CFO 영입, Big4 감사법인 선임"
        weight: 2
      - name: "Patent_Portfolio_Expansion"
        description: "최근 2년 특허 출원 50건 이상"
        source: "USPTO, KIPO, EPO"
        weight: 1
    ipo_score_threshold: 7  # 총점 10점 중 7점 이상 = IPO 후보
  ma_target_pattern:
    reference_cases:
      - acquiree: "eSilicon"
        acquirer: "Inphi (later Marvell)"
        year: 2019
        pattern: "Design House + CoWoS expertise → Strategic buy"
      - acquiree: "Inphi"
        acquirer: "Marvell"
        year: 2021
        pattern: "IP portfolio + HPC interconnect → Consolidation"
      - acquiree: "Arm"
        acquirer: "SoftBank"
        year: 2016
        pattern: "IP licensor market dominance → Premium acquisition"
    detection_criteria:
      - "unique_ip_moat: true"
      - "customer_concentration < 40%"  # 특정 고객 의존도 낮음
      - "strategic_fit_score >= 4"  # 대형 전략 바이어와 시너지
      - "revenue_range: $50M ~ $500M"  # M&A 적정 규모
  confidence_rules:
    HIGH:
      conditions:
        - "revenue confirmed from public filing"
        - "VC info confirmed from press release"
    MEDIUM:
      conditions:
        - "revenue estimated from industry reports"
        - "VC info from secondary sources"
    LOW:
      conditions:
        - "revenue estimated/inferred"
        - "no VC confirmation available"
      mandatory_note: "[ESTIMATED — confidence LOW] 표기 필수"
```

## D-4 갭 분석 확장

```yaml
d4_gap_matrix:
  dimensions:
    - axis: "지역 커버리지"
      current_state: "Taiwan + US 중심"
      target_state: "India + 중동 + EU 확장"
      gap_score: 3  # 1(낮음)~5(높음)
    - axis: "첨단 노드 대응"
      current_state: "N5/N7 일부"
      target_state: "N2/N3 대응 가능"
      gap_score: 4
    - axis: "AI ASIC 전문성"
      current_state: "일반 SoC 설계"
      target_state: "NPU/LLM ASIC 특화"
      gap_score: 4
    - axis: "CoWoS/SoIC 역량"
      current_state: "파트너 의존"
      target_state: "자체 패키징 설계 역량"
      gap_score: 5
    - axis: "소프트웨어 플랫폼"
      current_state: "전통 EDA 의존"
      target_state: "AI-driven EDA / Cloud EDA"
      gap_score: 3
  output_format: "Matrix 표 + 로드맵 제안"
```
