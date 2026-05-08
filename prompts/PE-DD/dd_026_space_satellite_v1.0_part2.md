# DD-026 · Space & Satellite Due Diligence — Part 2: Engines 1–3

*[Part 2 of 3 — Preceded by Part 1: Header/Role/Zones/Guards]*

---

## ENGINE 1 · CONSTELLATION & ASSET INTEGRITY ANALYZER (CAIA)

```
FUNCTION analyze_constellation_integrity(fleet_data, tle_data, fcc_filings, insurance_data):

  STEP 1 — ORBITAL FLEET ASSESSMENT:
    On-Orbit Status:
      Active satellites: operational vs. in-orbit spare vs. anomaly/controlled
      TLE vintage: last update <72h = current; >7 days = stale for LEO
      Altitude band: LEO (<2,000km) / MEO (2,000-35,786km) / GEO (35,786km)
      Inclination: SSO / ISS-altitude / polar / equatorial / Molniya
      Delta-V budget: estimated remaining propellant life (maneuver margin)

    Fleet Health Metrics:
      Anomaly rate: unplanned anomalies per satellite-year (benchmark <0.15)
      Total loss rate: on-orbit total losses / fleet size (benchmark <2%)
      Mean time between failures (MTBF): subsystem-level (ADCS, power, comms)
      Software-defined reconfigurability: percentage of payload reprogrammable on-orbit

    Constellation Completeness:
      IOC (Initial Operating Capability): minimum viable constellation threshold
      FOC (Full Operating Capability): planned final orbit count vs. current
      Phase deployment timeline: launch cadence required to maintain IOC
      Orbital slot filing: ITU coordination status per orbital plane

  STEP 2 — LAUNCH MANIFEST VERIFICATION:
    Confirmed launches: signed launch service agreements (LSA) with deposits
    Unconfirmed launches: LOI/MOU only = speculative; flag as UNVERIFIED
    Launch vehicle dependency:
      Single provider: SpaceX / RocketLab / Arianespace / ISRO
      Backup provider: manifest position secured vs. theoretical
      Rideshare constraints: mass/volume/vibration compatibility verified
    Launch cost modeling:
      $/kg to target orbit: current market rate (SpaceX F9 rideshare benchmark)
      Dedicated vs. rideshare tradeoff: schedule certainty vs. cost
      Insurance: pre-launch + launch + LEOP (Launch and Early Operations) coverage

  STEP 3 — SPECTRUM & ITU FILING INTEGRITY:
    Spectrum portfolio:
      Frequency bands: Ka / Ku / X / V / Q / UHF / L / S band allocations
      ITU filing administration: country of record; fiduciary relationship
      Due Diligence Date (DDP): years remaining before ITU cancellation risk
      Coordination agreements: bilateral/multilateral with adjacent operators
      Coordination disputes: active ITU Article 44 complaints
    Orbital slot:
      GEO: assigned vs. unassigned; longitude position; arc proximity
      NGSO: coordination with Starlink/OneWeb/Kuiper per ITU AP30B
      Spectrum squatting risk: paper satellite filings without deployment intent

  STEP 4 — INSURANCE & LIABILITY ASSESSMENT:
    Pre-launch coverage: satellite + launch vehicle (% of replacement cost)
    In-orbit coverage: anomaly / partial loss / total loss policy terms
    Third-party liability: Liability Convention 1972 sovereign liability passthrough
    Self-insurance threshold: fleet size >200 sats = pooled risk; actuarial review
    Historical claims: anomaly payouts; insurer relationship stability

  OUTPUT:
    CAIA_SCORE: [0-100] (fleet health + spectrum + launch + insurance composite)
    FLAGS: [ANOMALY_RATE_HIGH | SPECTRUM_DDP_SHORT | LAUNCH_UNCONFIRMED |
            SINGLE_PROVIDER | ITU_DISPUTE | DEORBIT_NONCOMPLIANT]
    ESCALATE_TO: [DD-022 if DUAL_USE; DD-023 if CYBER_C2_RISK]
```

---

## ENGINE 2 · SPACE MARKET & REVENUE MODEL VALIDATOR (SMRV)

```
FUNCTION validate_space_revenue_model(revenue_data, market_data, customer_data, backlog):

  STEP 1 — REVENUE SEGMENT ANALYSIS:
    Segment classification:
      Government: cost-plus IDIQ (NRO, NGA, NASA, DoD, ESA, JAXA) → stable but capex-heavy
      Commercial satcom: enterprise (aviation, maritime, energy, telco backhaul) → ARPU-driven
      Commercial EO: data subscription / tasking / analytics API → SaaS-comparable metrics
      Dual-use: classified + commercial hybrid → revenue opacity risk; FOCI flag
      In-space services: on-orbit servicing / refueling / ADR → nascent; milestone-based

    Revenue quality scoring:
      Contracted revenue: signed backlog with deposit / milestone structure
      Recurring vs. non-recurring: NRE (Non-Recurring Engineering) vs. ARR
      Government IDIQ: ceiling value vs. obligated; CR (Continuing Resolution) risk
      Commercial SLA: contract duration; termination for convenience clause

  STEP 2 — SATCOM MARKET BENCHMARKING:
    GEO HTS operators:
      Capacity pricing: $/MHz/month; transponder lease vs. managed service
      Fill rate: % of capacity under contract (benchmark: >70% for mature operators)
      HTS beam utilization: spot beam vs. wide beam efficiency
    LEO broadband:
      ARPU: $/user/month (Starlink consumer ~$120; enterprise $300-500+)
      Churn: monthly churn rate <3% = healthy for consumer; <1% for enterprise
      Terminal economics: UT (user terminal) subsidy; BOM cost trajectory
      Latency: <50ms LEO vs. ~600ms GEO = differentiation driver
    IoT/M2M:
      Device connections: active devices vs. under management
      Message pricing: $/message or $/device/month; duty cycle economics
      Addressable verticals: agriculture, maritime AIS, asset tracking, utilities

  STEP 3 — EARTH OBSERVATION REVENUE VALIDATION:
    Data tiers:
      Raw data (L0/L1): government bulk purchase; $/km² or $/scene pricing
      Analysis-ready data (L2/L3): processed; GIS-ready; cloud-delivered
      Analytics/AI insights (L4): value-added; subscription API; per-query pricing
    Customer segments:
      Government: intelligence (NRO, allied agencies); civil (USGS, Copernicus)
      Commercial: insurance, agriculture, forestry, urban planning, energy
      Defense: change detection, battle damage assessment (BDA) → ITAR review
    Competitive moat:
      Revisit rate: satellite passes per day per target area
      Resolution: optical <0.5m (near-military); SAR: 1m standard / 0.35m ultra
      Archive depth: historical imagery library value (geospatial data moat)

  STEP 4 — BACKLOG & PIPELINE QUALITY:
    Hard backlog: contracted, deposit received, launch-contingent milestones
    Soft pipeline: LOI / MOU / proposal stage = weight at 20% for valuation
    Book-to-bill ratio: quarterly new contracts / quarterly revenue (>1.2x = healthy)
    Customer concentration:
      Top-1 customer >30% revenue: KEY CUSTOMER RISK (E-05 trigger)
      US government >50% revenue: appropriations / CR dependency flag
      International government: ITAR export license required per contract

  OUTPUT:
    SMRV_SCORE: [0-100] (revenue quality + market position + backlog + concentration)
    FLAGS: [GOV_CONCENTRATION | BACKLOG_SOFT | ARPU_DECLINING | FILL_RATE_LOW |
            NRE_HEAVY | IDIQ_UNOBLIGATED]
    REVENUE_QUALITY_TIER: [TIER-1 (>80%) | TIER-2 (60-80%) | TIER-3 (<60%)]
```

---

## ENGINE 3 · DUAL-USE & EXPORT CONTROL RISK SCREENER (DUEC)

```
FUNCTION screen_dual_use_export_risk(technology_data, customer_list, supply_chain, team_data):

  STEP 1 — ITAR/EAR CLASSIFICATION MATRIX:
    USML Category XV (Spacecraft and Related Articles):
      XV(a): spacecraft (including satellites) → ITAR controlled
      XV(b): ground control systems with uplink capability → ITAR controlled
      XV(c): GPS/GNSS receivers with military capability → ITAR controlled
      XV(d): classified satellite components → TS/SCI access required
      XV(e): launch vehicles with MTCR Category I parameters → ITAR + State Dept.
    EAR CCL 9A/9E Series:
      9A515: civil remote sensing satellites → EAR license for non-AT countries
      9A004: launch vehicles, rocket propulsion → strict end-user cert.
      9E515: technology for civil EO satellites → deemed export risk
    Transition assessment: USML → CCL (2014 reform): verify current classification

  STEP 2 — MTCR THRESHOLD SCREENING:
    Category I trigger: payload mass >500kg AND range >300km
      → Presumption of denial for export to non-MTCR partners
      → US: State Dept. Space Policy review required
      → Launch services to non-allied nations: case-by-case
    Category II: sub-threshold components; missile-related equipment
      → License required; enhanced end-user certificate
    Sub-threshold commercial launch: SmallSat rideshare <500kg
      → Standard EAR treatment; less restrictive but still requires classification

  STEP 3 — SUPPLY CHAIN ADVERSARY SCREENING:
    Component-level review:
      Chinese-sourced components: COTS satellite parts → US nexus rule trigger
      Russian-sourced: RD-180 / RD-181 successor dependency (phased out post-2022)
      Iranian / NK involvement: automatic OFAC SDN → hard disqualifier
    Semiconductor content: ITAR-controlled rad-hard components (TID-rated)
      → US domestic sourcing preferred; non-US rad-hard: classification review
    Ground modem chipset: Qualcomm / MediaTek foreign fab: EAR 3A001 check
    Encryption hardware: NSA Type 1 / FIPS 140-3 compliance for gov contracts

  STEP 4 — DEEMED EXPORT & FOREIGN NATIONAL RISK:
    Team composition:
      Foreign nationals with access to ITAR tech: deemed export license required
      PRC nationals: automatic enhanced review; typically license denial for USML
      Five-Eyes nationals (UK/CA/AU/NZ): favorable treatment; license exception STA
    Technology transfer controls:
      Visitor access log: ITAR-controlled facilities; foreign visit request (FVR)
      IP assignment: foreign co-inventor → foreign filing license required (37 CFR 5.11)
      University collaboration: fundamental research exclusion applicability

  STEP 5 — CFIUS / FOCI ASSESSMENT:
    CFIUS trigger criteria for space:
      Foreign investment in US satellite operators: TID business (critical technology)
      Ground station with government SLA: critical infrastructure
      EO satellite with sub-0.5m resolution: national security nexus
      Launch facility on US soil: critical infrastructure; CFIUS jurisdiction
    FOCI mitigation for classified programs:
      NRO/NGA/NSA contracts: DSS (DCSA) facility clearance required
      Foreign ownership: SSA / SCA / Proxy Board / Voting Trust options
      Mitigation instrument lead time: 12-24 months; deal timing risk

  OUTPUT:
    DUEC_SCORE: [0-100] (lower score = higher risk)
    FLAGS: [ITAR_USML_XV | MTCR_CAT_I | PRC_SUPPLY_CHAIN | DEEMED_EXPORT |
            CFIUS_TRIGGER | FOCI_REQUIRED | ADVERSARY_NATION]
    EXPORT_RISK_TIER: [GREEN (low) | AMBER (manageable) | RED (deal-breaker risk)]
    ESCALATE_TO: [DD-022 Defense if CLASSIFIED_PROGRAM; DD-MASTER if HARD_DISQUALIFIER]
```

---

*[Part 2 of 3 — Continues in Part 3: Engines 4–5, Output Format, Scoring Matrix]*
