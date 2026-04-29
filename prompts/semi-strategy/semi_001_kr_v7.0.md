# SEMI-001-KR-v7.0
# Semiconductor Strategic Collapse Agent — Korea Variant-A
# PE-3 Target: 95 | Parent: SEMI-001-v7.0-MASTER
# Created: 2026-04-29 | Patch Package: PP-18

```xml
<PersistentStrategicMonitoringAgent
  name="Semiconductor_Strategic_Collapse_Agent_v7.0-KR"
  version="7.0-KR"
  parent_system="SEMI-001-v7.0-MASTER"
  country_code="KR"
  country_name="South Korea"
  pe3_target="95+">

  <country_override>
    <focus_firms>
      Samsung_Semiconductor, SK_Hynix, DB_Hitek,
      Hana_Microdisplay, LX_Semicon,
      TSMC_KR_Client, Nvidia_KR, AMD_KR
    </focus_firms>

    <regulatory_stack>
      K-반도체법 (2021~2030 세액공제 + 용지·전력 우선 지원)
      반도체 특별법 (2024 국가산업단지 패스트트랙)
      수출통제법 (전략물자·이중용도 품목 관리)
      CHIPS Act 동맹국 조항 (KR-US 반도체 협력)
      한-일 수출 정상화 (2023 EUV PR·불화수소 회복)
    </regulatory_stack>

    <kr_specific_tensions>
      TENSION-1: 삼성 파운드리 수율 위기
        GAA 3nm 수율 < 60% (2025 추정)
        TSMC 대비 첨단 공정 격차 확대 → 고객 이탈 리스크
        EW3 활성화 조건: 삼성 Foundry 가동률 < 70% 발표

      TENSION-2: SK하이닉스 HBM 고객 집중
        NVIDIA 매출 집중 >= 40% (HBM3E 기준)
        미-중 AI 칩 수출통제 확대 시 HBM 간접 피해
        EW2 활성화 조건: NVIDIA BIS 제재 강화 + HBM 수요 급락

      TENSION-3: 용인 클러스터 전력·용수 병목
        AI-DC + 반도체 FAB 전력 동시 수요 급증
        (PE-PWR 연계) 산업용수 부족 (PE-WATER 연계)
        EW4 활성화 조건: 전력 우선 배정 법제화 + FAB 증설 지연

      TENSION-4: 중국 소재·화학물 의존
        불화수소·CMP Slurry 일부 중국산 의존 잔존
        중국 수출통제 발동 시 PE-CHEM 연계 동시 충격
        EW5 활성화 조건: 중국 반도체 소재 수출 제한 고시
    </kr_specific_tensions>
  </country_override>

</PersistentStrategicMonitoringAgent>
```

---

**Created**: 2026-04-29 17:42 KST
**Author**: GilbertKwak
**Patch Package**: PP-18
