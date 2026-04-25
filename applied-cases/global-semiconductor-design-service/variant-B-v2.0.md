# 변형 B v2.0 — TSMC DCA/VCA 파트너 한정 정밀 탐색형

## 메타데이터
- **버전**: 2.0.0
- **기반**: Master Prompt v2.0 INCLUSION CRITERIA 확장 변형
- **목적**: TSMC Design Center Alliance(DCA) 또는 Value Chain Aggregator(VCA) 등록 기업 정밀 탐색
- **생성일**: 2026-04-25
- **변경 내역 (v1→v2)**: Type C 기업 대다수 탈락 문제 → Type C 서브-변형 조건 분리

---

## ⚠️ v1.0 대비 핵심 변경사항

| 항목 | v1.0 문제 | v2.0 수정 |
|---|---|---|
| Type C 기업 탈락 | TSMC 파트너 조건 미충족 기업 전부 탈락 | Type C는 별도 서브-변형 B-C로 분리 |
| TSMC 파트너 확인 | 방법 미정의 | 공식 Alliance 리스트 URL 명시 |
| CoWoS/SoIC 조건 | 미포함 | 첨단 패키징 파트너 조건 추가 |

---

## CRITERIA EXTENSION (Master v2.0에 추가 적용)

```yaml
criteria_extension:
  tsmc_partner_filter:
    mode: "ADDITIVE_STRICT"  # 이 조건을 만족하는 기업만 B-variant 포함
    programs:
      - name: "TSMC Design Center Alliance (DCA)"
        url: "https://www.tsmc.com/english/dedicatedFoundry/services/DCA.htm"
        member_types: ["Gold", "Silver", "Member"]
      - name: "TSMC Value Chain Aggregator (VCA)"
        url: "https://www.tsmc.com/english/dedicatedFoundry/services/VCA.htm"
      - name: "TSMC Open Innovation Platform (OIP)"
        url: "https://www.tsmc.com/english/dedicatedFoundry/services/OIP.htm"
      - name: "TSMC Advanced Packaging Partner"
        programs: ["CoWoS", "SoIC", "InFO", "COWOS-S", "COWOS-L"]
```

## Type C 서브-변형 B-C (별도 실행)

```yaml
subvariant_B_C:
  description: "TSMC 파트너이지만 IT서비스 중심인 Type C 기업 전용"
  criteria:
    - tsmc_partner: true
    - primary_business: "EDA_service OR PDK_service OR DFM_service"
    - not_turnkey_asic: true  # Turnkey ASIC 직접 수행 안 함
  examples:
    - "Ansys (TSMC certified signoff)"
    - "Mentor (Siemens EDA) — TSMC DRC kit 보유"
    - "Synopsys — PDK 공급자이자 DCA 멤버"
```

## 심층 분석 필드 추가 (D-1 확장)

```yaml
additional_fields_for_B_variant:
  - name: "TSMC_Node"
    type: "STRING"
    description: "지원 가능 TSMC 공정 노드"
    example: "N3E, N4P, N5, N7, N12FFC"
  - name: "TSMC_Partner_Level"
    type: "ENUM(DCA_Gold, DCA_Silver, DCA_Member, VCA, OIP, AP)"
    required: true
  - name: "CoWoS_Capable"
    type: "BOOLEAN"
  - name: "Tape_Out_Count_Annual"
    type: "INTEGER"
    description: "연간 테이프아웃 건수 (추정)"
```

## 예상 발굴 기업 (TSMC DCA 멤버 확인)

| 기업 | 국가 | Type | TSMC 관계 |
|---|---|---|---|
| Alchip Technologies | TW | A | DCA Gold |
| GUC (Global Unichip) | TW | A | TSMC 자회사 |
| Faraday Technology | TW | A | DCA Gold |
| Dolphin Design | FR | B | OIP 멤버 |
| Arteris IP | US | B | OIP 멤버 |
| Synopsys | US | B | DCA + OIP |
| Cadence | US | B | DCA + OIP |
| Ansys | US | C | TSMC Certified |
| eSilicon (now Inphi) | US | A | DCA (구) |
