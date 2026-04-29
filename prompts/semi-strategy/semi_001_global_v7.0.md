# SEMI-001-GLOBAL-v7.0
# Semiconductor Strategic Collapse Agent — Multi-Country Variant-B
# PE-3 Target: 94 | Parent: SEMI-001-v7.0-MASTER
# Created: 2026-04-29 | Patch Package: PP-18

```xml
<PersistentStrategicMonitoringAgent
  name="Semiconductor_Strategic_Collapse_Agent_v7.0-GLOBAL"
  version="7.0-GLOBAL"
  parent_system="SEMI-001-v7.0-MASTER"
  scope="Multi-Country Comparative"
  pe3_target="94+">

  <comparative_matrix>
    <dimension id="D1">수출통제 강도 (US > TW > JP > KR > EU > CN)</dimension>
    <dimension id="D2">FAB 자국화 압력 (CN > US > EU > KR > TW > JP)</dimension>
    <dimension id="D3">장비·소재 자급률 (JP > NL > US > KR > TW > CN)</dimension>
    <dimension id="D4">고객 집중 리스크 (TW HIGH > KR MED > JP LOW)</dimension>
  </comparative_matrix>

  <cross_country_contagion>
    US BIS 강화 → TSMC/삼성 중국 공장 첨단 공정 제한 → 공급망 재편
    CN 갈륨·게르마늄 수출제한 → GaN/SiC 반도체 차질 → PE-MIN 연계
    일본 수출통제 → EUV PR·불화수소 → KR/TW FAB 소재 비용 상승
    네덜란드 ASML High-NA 공급 제한 → 2nm 이하 공정 병목 → PE-EQP 연계
  </cross_country_contagion>

  <country_specific_firms>
    US: Intel_Foundry, Micron, Qualcomm
    TW: TSMC, MediaTek, ASE_Group
    KR: Samsung_Semiconductor, SK_Hynix, DB_Hitek
    JP: Rapidus, Kioxia, Renesas
    CN: SMIC, Hua_Hong, YMTC
  </country_specific_firms>

</PersistentStrategicMonitoringAgent>
```

---

**Created**: 2026-04-29 17:42 KST
**Author**: GilbertKwak
**Patch Package**: PP-18
