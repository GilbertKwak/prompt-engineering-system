# DD-023 · Cybersecurity & Data Security Due Diligence v1.1
*[Part 3 of 3 — Engines 6, 7 | 18-Layer Scoring Matrix | Output Templates | Delta Registry]*
*[Preceded by Part 2: Engines 3 (CMRE), 4 (AQE), 5 (TIQE)]*

---

## ENGINE 6 · REGULATORY & COMPLIANCE SCORING ENGINE v1.1 (RCSE)

```
FUNCTION score_regulatory_compliance_v1.1(target, jurisdictions, certifications,
                                           audit_data, incident_history,
                                           customer_segments):

  CONTEXT: Comprehensive compliance posture scoring across all applicable
           regulatory frameworks. Activates automatically for any target
           with >$10M ARR, government contracts, or cross-border data flows.

  MODULE A — FRAMEWORK COVERAGE MATRIX:

    Tier-1 Mandatory (deal-blocking if absent for qualified verticals):
      SOC 2 Type II:
        Present: BASE +2.0
        Absent (SaaS/cloud target): -3.0 (E-09 FLAG; deal condition precedent)
        Bridge letter required if last audit >12 months
      ISO 27001:2022 certification:
        Present: +1.5
        Absent (enterprise target): -1.0 | Absent (SMB): 0
        Surveillance audit current (within 12m): required for ongoing credit
      FedRAMP (US Federal target):
        High: +3.0 (scarce; premium multiple justification)
        Moderate: +2.0
        Low: +1.0
        In-Progress (P-ATO): +0.5 (risk: timeline slippage; >18m average)
        Not started: 0 (barrier to federal revenue; discount GovTech ARR ×0.6)
      CMMC Level 2 (DoD supply chain):
        Certified (C3PAO assessment): +2.0
        Self-attested Level 1: +0.5
        Not initiated: -1.0 if DoD customer concentration >15%
      PCI DSS v4.0 (payment card handling):
        Compliant (QSA-assessed): +1.5
        SAQ D self-assessed: +0.8
        Non-compliant with active card data: E-09 CRITICAL FLAG

    Tier-2 Regional/Sector (scored by applicability):
      GDPR (EU data subjects):
        DPA-confirmed compliant + DPO appointed: +1.5
        SCCs executed + transfer impact assessments: +0.5
        DPA investigation active / enforcement notice: -3.0 (E-09 FLAG)
        Article 83(5) violation history: -5.0 (HARD FLAG; deal re-examination)
      NIS2 Directive (EU critical infrastructure, Oct 2024 enforcement):
        Essential entity registered + incident reporting SOP: +1.5
        Important entity: +1.0
        In-scope but not registered: -2.0 (regulatory gap; E-09 FLAG)
      HIPAA (US healthcare PHI handling):
        BAA in place with all covered entities: required
        Last HIPAA risk assessment <12m: +1.0
        OCR investigation / settlement history: -3.0 (E-09 FLAG)
      UK Cyber Essentials Plus:
        Present: +0.5
        Required for UK government contracts (pre-condition for Annex 3 gov revenue)
      APRA CPS 234 (Australia financial services):
        Compliant: +1.0 | Non-compliant with APRA-regulated customers: -1.5
      Korea ISMS-P certification:
        Certified: +1.0 (required for KR financial / healthcare / >1M users)
        In-scope without certification: -1.5 (KISA enforcement risk)

    Tier-3 Emerging Frameworks (forward-looking risk):
      EU AI Act (2026 mandatory for GPAI / high-risk AI systems):
        Conformity assessment initiated: +0.5
        High-risk AI system without roadmap: -1.0 (regulatory gap; forward risk)
      SEC Cybersecurity Rule (effective Dec 2023, US public targets/acquirers):
        4-day material incident disclosure: policy/SOP confirmed: +0.5
        Annual 10-K disclosure (CISO background, governance): confirmed: +0.3
        Non-compliant US public target: -2.0 (E-09 FLAG)
      DORA (Digital Operational Resilience Act, EU financial sector Jan 2025):
        ICT risk management framework aligned: +1.0
        TLPT (Threat-Led Penetration Testing) scheduled: +0.5
        Financial entity without DORA roadmap: -2.0

  MODULE B — AUDIT TRAIL & EVIDENCE QUALITY:

    Audit recency scoring:
      All Tier-1 audits <12 months: FULL_CREDIT
      Any Tier-1 audit 12~24 months: PARTIAL_CREDIT (×0.75)
      Any Tier-1 audit >24 months: STALE (×0.5; E-09 FLAG)
      No external audit evidence: SELF_REPORTED (×0.40; E-09 MANDATORY)

    Auditor quality:
      Big-4 / Top-10 (Deloitte, KPMG, PwC, EY, BDO, GT): TIER_A (×1.0)
      Accredited specialist (Coalfire, Schellman, Tevora, Rapid7): TIER_B (×0.9)
      Regional CPA / unaccredited: TIER_C (×0.7; verify accreditation)
      Self-assessment only: TIER_D (×0.4; conditional; require bridge letter)

    Remediation tracking:
      Open critical findings from last audit:
        0 critical open: +0.5
        1~3 critical open: 0
        >3 critical open: -1.0 (E-09 FLAG; deal condition: remediation plan)
      Time-to-remediation (TTR) for past findings:
        <30d average: EXCELLENT | 30~90d: GOOD | >90d: SLOW (culture signal)

  MODULE C — INCIDENT & BREACH HISTORY SCORING:

    Breach frequency (last 5 years):
      0 confirmed breaches: +2.0
      1 minor breach (contained; <1K records): +0.5
      1 significant breach (>1K records; notified): -1.0 (E-16 activation)
      2+ breaches: -2.5 (E-16 MANDATORY; pattern risk)
      Ransomware payment confirmed: -3.0 + E-16 + legal hold assessment

    Regulatory enforcement history:
      No regulatory action: +1.0
      Warning / informal action: 0
      Formal enforcement / fine <$1M: -1.0
      Fine >$1M or class action settlement: -3.0 (E-16 CRITICAL FLAG)
      Criminal referral / DOJ investigation: HARD DISQUALIFIER (D-09)

    Voluntary disclosure quality:
      SEC 8-K cybersecurity disclosure (if applicable): timeliness + completeness score
      EU NIS2 72-hour notification: confirmed compliance
      GDPR 72-hour breach notification: confirmed compliance
      Failure to notify when required: -2.0 per instance (material integrity risk)

  RCSE_SCORE = MODULE_A (0~20) + MODULE_B (0~5) + MODULE_C (0~5)
  NORMALIZED_RCSE = RCSE_RAW / 30 × 10 (0~10 scale)

  Rating:
    9.0~10.0: GOLD_STANDARD — institutional-grade compliance posture
    7.5~8.9:  STRONG — minor gaps; manageable with condition precedents
    6.0~7.4:  ADEQUATE — framework gaps; pre-close remediation required
    4.0~5.9:  WEAK — material compliance risk; deal re-price or conditions
    <4.0:     CRITICAL — compliance breakdown; E-09 mandatory; consider pass

  RETURN:
    {framework_scores, tier1_gaps, tier2_gaps, audit_quality_score,
     incident_score, normalized_rcse, rating, e09_flags, deal_conditions}
```

---

## ENGINE 7 · CYBER INVESTMENT DECISION SYNTHESIZER v1.1 (CIDS)

```
FUNCTION synthesize_cyber_investment_decision_v1.1(
    cva_score,        # Engine 1 output
    sra_score,        # Engine 2 output
    cmre_score,       # Engine 3 output
    aqe_score,        # Engine 4 output
    tiqe_score,       # Engine 5 output
    rcse_score,       # Engine 6 output
    deal_params,      # valuation, entry multiple, hold period, exit strategy
    market_data,      # sector growth, M&A comps, public comps
    active_flags):

  ─────────────────────────────────────────────────────────────
  PHASE 1 — HARD DISQUALIFIER GATE (pre-scoring)
  ─────────────────────────────────────────────────────────────

    D-SERIES HARD DISQUALIFIERS (immediate deal rejection):

      D-01 SUPPLY_CHAIN_BACKDOOR:
        Condition: Confirmed adversary-nation supply chain implant in product
        Evidence: NSA/CISA advisory OR independent forensic confirmation
        Action: IMMEDIATE_REJECT; notify fund compliance officer; preserve evidence

      D-02 CRITICAL_INFRASTRUCTURE_SYSTEMIC:
        Condition: Single point of failure for >1 critical infrastructure sector
        Evidence: CISA SRMA assessment OR equivalent government advisory
        Action: REJECT unless government acquirer; national security review required

      D-03 REGULATORY_CRIMINAL:
        Condition: Active DOJ / FBI / SEC criminal investigation of target entity
        Evidence: Grand jury subpoena, DOJ press release, or CID receipt
        Action: IMMEDIATE_REJECT; do not consummate; preserve privilege

      D-04 ADVERSARY_TI_SOURCE:
        Condition: Core TI product fed by confirmed adversary-nation intelligence apparatus
        Evidence: TIQE Step 1 E-18 trigger OR CISA/FBI advisory
        Action: IMMEDIATE_REJECT; E-15 export concerns simultaneous

      D-05 UNDISCLOSED_MATERIAL_BREACH:
        Condition: Material breach identified in DD not disclosed to investors or regulators
        Evidence: Dark web intelligence + forensic corroboration; CMRE Module A
        Action: REJECT; legal hold; consider whistleblower obligation

      D-06 OFAC_SDN_NEXUS:
        Condition: Target, key personnel, or material customer on OFAC SDN list
        Evidence: OFAC SDN search + beneficial ownership verification
        Action: IMMEDIATE_REJECT; OFAC counsel notification required

      D-07 ITAR_UNLICENSED_EXPORT:
        Condition: Confirmed ITAR-controlled technology exported without license
        Evidence: Export records + DDTC/BIS investigation or voluntary disclosure
        Action: REJECT; voluntary disclosure assessment with ITAR counsel

      D-08 FINANCIAL_FRAUD:
        Condition: ARR fabrication or fraudulent contract evidence
        Evidence: Billing system discrepancy >15% vs. stated ARR; bank confirmation
        Action: REJECT; preserve evidence; legal referral

      D-09 CATASTROPHIC_COMPLIANCE_FAILURE:
        Condition: Multi-jurisdiction regulatory enforcement + criminal referral combination
        Evidence: RCSE Module C criminal referral flag
        Action: REJECT; reputational and legal exposure intolerable

  ─────────────────────────────────────────────────────────────
  PHASE 2 — COMPOSITE SCORING & WEIGHTING
  ─────────────────────────────────────────────────────────────

    WEIGHT TABLE by investment thesis:

      Thesis A — Platform Consolidator (acquire & integrate):
        CVA_SCORE:   20% (architecture must support integration)
        SRA_SCORE:   25% (must resolve, not inherit, risk)
        CMRE_SCORE:  20% (liability transfer critical)
        AQE_SCORE:   20% (ARR portability post-integration)
        TIQE_SCORE:  5%  (TI quality matters for product roadmap)
        RCSE_SCORE:  10% (compliance must transfer cleanly)

      Thesis B — Organic Growth / ARR Expansion:
        CVA_SCORE:   15%
        SRA_SCORE:   15%
        CMRE_SCORE:  10%
        AQE_SCORE:   35% (ARR engine is the core value driver)
        TIQE_SCORE:  10%
        RCSE_SCORE:  15% (regulatory moats drive NRR)

      Thesis C — Government / Defense Specialist:
        CVA_SCORE:   10%
        SRA_SCORE:   20%
        CMRE_SCORE:  20% (clearance/export critical)
        AQE_SCORE:   15%
        TIQE_SCORE:  10%
        RCSE_SCORE:  25% (FedRAMP/CMMC = moat; compliance is the product)

      Thesis D — Distressed / Special Situations:
        CVA_SCORE:   25% (tech asset quality assessment)
        SRA_SCORE:   30% (risk quantification for pricing)
        CMRE_SCORE:  25% (liability isolation strategy)
        AQE_SCORE:   10%
        TIQE_SCORE:  5%
        RCSE_SCORE:  5%  (assume remediation cost in model)

    COMPOSITE_SCORE = Σ(engine_score × weight) [0~10]

    COMPOSITE_BANDS:
      8.5~10.0: STRONG_BUY — proceed at target valuation; IC recommendation
      7.0~8.4:  CONDITIONAL_BUY — proceed with deal conditions; flag items to IC
      5.5~6.9:  HOLD_NEGOTIATE — re-price; re-examine; additional DD required
      4.0~5.4:  CONDITIONAL_PASS — material issues; pass unless seller concessions
      <4.0:     PASS — risk/return unfavorable; recommend decline

  ─────────────────────────────────────────────────────────────
  PHASE 3 — ROSI & VALUATION IMPACT ANALYSIS
  ─────────────────────────────────────────────────────────────

    ROSI (Return on Security Investment) Framework:

      ROSI = (Risk_Reduction_Value × Probability_of_Breach) - Cost_of_Control

      Risk Reduction Value inputs:
        Annual breach cost baseline: IBM Cost of Data Breach 2024 ($4.88M global avg)
        Industry premium: Healthcare ×3.2 | Financial ×2.7 | Tech ×1.8 | Retail ×1.4
        Breach probability: FAIR model; threat frequency × vulnerability magnitude
        Control effectiveness: % risk reduction per control category

      Security investment sizing benchmark:
        Cybersecurity spend as % revenue:
          Best-in-class (FedRAMP High / BFSI): 8~15% of revenue
          Industry average (enterprise SaaS): 5~8% of revenue
          Below-average (legacy/SMB): <5% (underinvestment signal)
          Over-invested (no ROI evidence): >20% (operational efficiency concern)

      Valuation impact calculation:
        Cyber risk discount to EV:
          HIGH_RISK target: apply 15~30% haircut to entry multiple
          ELEVATED_RISK: apply 8~15% haircut
          MODERATE_RISK: apply 3~8% haircut
          LOW_RISK: premium justification (+5~10% to benchmark multiple)

        Remediation cost modeling:
          Immediate remediation capex: point-in-time estimate from SRA Engine 2
          Ongoing security opex uplift: annualized run-rate cost
          NPV of remediation over hold period: discount at WACC
          Adjust entry EV: EV_adjusted = EV_stated - NPV_remediation

  ─────────────────────────────────────────────────────────────
  PHASE 4 — 4-SCENARIO STRESS TEST
  ─────────────────────────────────────────────────────────────

    Scenario S1 — BASE CASE:
      Assumptions: No material breach; 85% of flagged issues remediated within 18m;
                   NRR holds; regulatory compliance achieved on schedule
      IRR projection: based on entry multiple + organic growth + exit multiple
      Cyber risk impact: E[loss] = annual breach probability × average loss magnitude

    Scenario S2 — CYBER STRESS (material breach at T+18m):
      Assumptions: Tier-2 breach (100K~1M records); 3-day operational outage;
                   class action filed; GDPR/CCPA fine assessed
      Estimated breach cost: $15~50M total (notification + legal + regulatory + reputational)
      Revenue impact: NRR decline -15 to -25 pts for 2 quarters post-breach
      Exit multiple compression: -1.0 to -2.0x from S1 baseline
      IRR delta vs. S1: calculate; if delta >15% IRR points → deal-breaker signal

    Scenario S3 — REGULATORY ESCALATION (major compliance failure):
      Assumptions: GDPR Article 83(5) maximum fine (4% global revenue) levied;
                   SEC enforcement action for disclosure failure;
                   FedRAMP authorization suspended
      Fine estimate: 4% global annual revenue (capped at €20M or 4% if higher)
      Revenue impact: Federal ARR at risk if FedRAMP suspended; 60% loss estimate
      Customer churn: enterprise logo churn +20% from regulatory headline risk
      IRR delta vs. S1: calculate; recovery timeline >36m = PASS signal

    Scenario S4 — GEOPOLITICAL / EXPORT ESCALATION:
      Assumptions: BIS Entity List addition of key technology partner;
                   CFIUS retroactive investigation triggered by post-close foreign investor
      Revenue impact: ECCN-controlled products: suspension of export licenses;
                      EU revenue at risk if US extraterritorial application
      Operational impact: foreign national talent departure (deemed export resolution)
      IRR delta vs. S1: calculate; if irrecoverable within hold period → PASS

    Stress test composite:
      Weighted average IRR = 0.50×S1 + 0.25×S2 + 0.15×S3 + 0.10×S4
      Hurdle rate: fund-specific (typical PE: 20~25% net IRR)
      IF weighted_avg_IRR < hurdle_rate → PASS recommendation to IC
      IF S2 or S3 IRR_delta >20% from S1 AND probability >15% → ELEVATED_CONCERN flag

  ─────────────────────────────────────────────────────────────
  PHASE 5 — CVE/CVSS v3.1 AUTOMATED SCORING ENGINE
  ─────────────────────────────────────────────────────────────

    CONTEXT: Automated vulnerability triage for product security assessment.
             Ingests NVD feed, vendor advisory data, and EPSS scores.

    CVE Triage Protocol:

      Data sources (in priority order):
        1. NVD (nvd.nist.gov) API v2.0: official CVE/CVSS database
        2. EPSS (Exploit Prediction Scoring System) v3: exploitation probability
        3. CISA KEV (Known Exploited Vulnerabilities catalog): active exploitation
        4. Vendor advisory / VDP: vendor patch status
        5. Threat intelligence overlay: TIQE feed correlation

      Severity classification (CVSS v3.1 base score):
        Critical (9.0~10.0):
          Remediation SLA: 24h (internet-facing) / 72h (internal)
          DD escalation: immediate E-11 flag; IC notification required
          Unpatched critical at close: deal condition (patch pre-close or escrow)
        High (7.0~8.9):
          Remediation SLA: 7d (internet-facing) / 30d (internal)
          DD escalation: E-11 flag; remediation plan required pre-IC
        Medium (4.0~6.9):
          Remediation SLA: 30d (internet-facing) / 90d (internal)
          DD escalation: tracked; include in remediation roadmap
        Low (0.1~3.9):
          Remediation SLA: 180d
          DD escalation: logged; monitoring only
        Informational (0.0):
          No SLA; best-effort

      EPSS overlay (exploitation probability adjustment):
        EPSS >70%: regardless of CVSS base score → escalate to CRITICAL tier
        EPSS 30~70% + CVSS ≥7.0: priority remediation; SLA ÷ 2
        EPSS <10% + CVSS <7.0: standard SLA; monitoring

      CISA KEV mandatory:
        Any CVE on CISA KEV: automatic CRITICAL escalation
        Unpatched KEV at close: HARD deal condition; cannot proceed without patch

      Vulnerability density metrics:
        Critical CVE density: count per 1,000 lines of code (benchmark: <0.1)
        MTTR (Mean Time to Remediate): critical/high/medium by tier
          Critical MTTR benchmark: <7d | High: <30d | Medium: <90d
        Patch cadence: % of critical CVEs patched within SLA (target: >95%)
        Vulnerability backlog age: median age of open vulnerabilities

      Automated scoring output:
        total_cves_scanned: count
        critical_unpatched: count + list
        high_unpatched: count
        kev_unpatched: count (ZERO TOLERANCE at close)
        epss_escalated: count
        mttr_score: 0~10 (10 = best; benchmark vs. industry)
        vuln_density_score: 0~10
        cvss_composite: weighted_avg_severity
        patch_compliance_rate: %
        flags: [KEV_UNPATCHED | CRITICAL_BACKLOG | MTTR_EXCEEDED |
                EPSS_OVERRIDE | LEGACY_UNSUPPORTED]

  CIDS_FINAL_RECOMMENDATION:
    {
      hard_disqualifier_triggered: [D-01~D-09 | NONE],
      composite_score: [0~10],
      composite_band: [STRONG_BUY | CONDITIONAL_BUY | HOLD_NEGOTIATE |
                       CONDITIONAL_PASS | PASS],
      investment_thesis: [A | B | C | D],
      rosi_summary: {breach_probability, annual_expected_loss,
                     security_investment_adequacy, ev_adjustment},
      stress_test: {s1_irr, s2_irr, s3_irr, s4_irr, weighted_avg_irr,
                    hurdle_cleared: [YES/NO], stress_delta_flag: [YES/NO]},
      cve_summary: {critical_unpatched, kev_unpatched, mttr_score,
                    patch_compliance, kev_cleared: [YES/NO]},
      deal_conditions: [list_of_required_conditions],
      ic_narrative: [3-sentence IC recommendation],
      escalation_triggers: [list]
    }
```

---

## 18-LAYER SCORING MATRIX — MASTER FRAMEWORK v1.1

```
LAYER  ENGINE   SUBSYSTEM                        WEIGHT  MAX_SCORE  NOTES
──────────────────────────────────────────────────────────────────────────────
L-01   E1-CVA   Architecture Depth               8%      10         SDLC, DevSecOps, ZTA
L-02   E1-CVA   Technology Stack Quality         6%      10         Dependency risk, EOL
L-03   E1-CVA   Cloud Security Posture           6%      10         CSPM, IaC, multi-cloud
L-04   E2-SRA   Attack Surface Quantification    8%      10         EASM, Crown Jewel
L-05   E2-SRA   Control Effectiveness            7%      10         MITRE D3FEND mapping
L-06   E2-SRA   IR & Resilience Capability       5%      10         RTO/RPO, playbooks
L-07   E3-CMRE  Breach Liability Transfer        5%      10         RWI, escrow
L-08   E3-CMRE  Export Control Compliance        5%      10         EAR/ITAR/Wassenaar
L-09   E3-CMRE  Talent & Clearance Risk          3%      10         ITAR deemed export
L-10   E4-AQE   ARR Contract Quality             5%      10         Duration, T4C, escalation
L-11   E4-AQE   Net Revenue Retention            7%      10         NRR/GRR cohort analysis
L-12   E4-AQE   Customer Quality & Churn         5%      10         Enterprise mix, verticals
L-13   E5-TIQE  Threat Intelligence Quality      4%      10         Provenance, freshness, FPR
L-14   E5-TIQE  ATT&CK Coverage                  3%      10         Technique coverage %
L-15   E6-RCSE  Regulatory Framework Coverage    6%      10         SOC2, FedRAMP, ISO 27001
L-16   E6-RCSE  Audit Quality & Recency          3%      10         Auditor tier, TTR
L-17   E7-CIDS  ROSI & Valuation Discipline      5%      10         EV adjustment, NPV
L-18   E7-CIDS  Stress Test IRR Quality          4%      10         4-scenario weighted avg
──────────────────────────────────────────────────────────────────────────────
TOTAL                                            100%    10

FINAL_SCORE = Σ(L-01 through L-18 weighted scores)

RANK TABLE:
  9.0~10.0: TIER-A  — Best-in-class cybersecurity platform; premium multiple justified
  8.0~8.9:  TIER-B  — High-quality; market-leading; growth equity at benchmark
  7.0~7.9:  TIER-C  — Solid; manageable issues; conditional approval
  6.0~6.9:  TIER-D  — Adequate; notable gaps; re-price or conditions required
  5.0~5.9:  TIER-E  — Below benchmark; elevated risk; conditional pass
  <5.0:     TIER-F  — Material risk; recommend pass (absent special situations thesis)

E-SERIES FLAG TALLY:
  0 flags:     Clean DD; proceed
  1~2 flags:   Standard risk; address in deal conditions
  3~5 flags:   Elevated; pre-IC risk memo required
  6~9 flags:   High; partner-level escalation required
  ≥10 flags:   CRITICAL accumulation; strong pass signal regardless of total score
```

---

## OUTPUT TEMPLATES

### TEMPLATE-A · EXECUTIVE SUMMARY (IC-Grade)

```
═══════════════════════════════════════════════════════════════
  DD-023 CYBERSECURITY DUE DILIGENCE — EXECUTIVE SUMMARY
  Target: [COMPANY_NAME] | Deal Code: [DEAL_CODE]
  Assessment Date: [DATE] | Lead Analyst: [ANALYST]
  Classification: CONFIDENTIAL — IC USE ONLY
═══════════════════════════════════════════════════════════════

1. INVESTMENT RECOMMENDATION
   ┌────────────────────────────────────────────┐
   │  DECISION: [STRONG_BUY / COND_BUY /        │
   │            HOLD / COND_PASS / PASS]         │
   │  COMPOSITE SCORE: [X.X / 10.0]             │
   │  TIER: [A / B / C / D / E / F]             │
   │  HARD DISQUALIFIER: [NONE / D-XX triggered] │
   └────────────────────────────────────────────┘

2. SNAPSHOT SCORECARD
   Engine          Score   Rating        Key Finding
   ─────────────────────────────────────────────────────
   E1 CVA          [X.X]   [TIER]        [1-line summary]
   E2 SRA          [X.X]   [TIER]        [1-line summary]
   E3 CMRE         [X.X]   [BAND]        [1-line summary]
   E4 AQE          [X.X]   [RATING]      [1-line summary]
   E5 TIQE         [X.X]   [RATING]      [1-line summary]
   E6 RCSE         [X.X]   [RATING]      [1-line summary]
   E7 CIDS         [X.X]   [BAND]        [1-line summary]
   ─────────────────────────────────────────────────────
   COMPOSITE        [X.X]   [TIER]        [overall verdict]

3. FLAGS SUMMARY
   E-Series Flags Triggered: [count]
   Critical (E-01~E-06):  [count] — [flag codes]
   Operational (E-07~E-12): [count] — [flag codes]
   Regulatory (E-09, E-15, E-16): [count] — [flag codes]
   Hard Disqualifiers: [count] — [D-codes if any]

4. TOP 3 VALUE DRIVERS
   ① [Driver 1: e.g., FedRAMP High moat; ~$35M protected ARR]
   ② [Driver 2: e.g., NRR 127%; best-in-class retention]
   ③ [Driver 3: e.g., ATT&CK 68% coverage; market-leading TI]

5. TOP 3 RISK FACTORS
   ① [Risk 1: e.g., 3 unpatched Critical CVEs on CISA KEV — deal condition]
   ② [Risk 2: e.g., GDPR DPA inquiry active — €8M max exposure]
   ③ [Risk 3: e.g., Key CISO departure risk — 80% equity vested]

6. DEAL CONDITIONS (pre-IC approval)
   □ [Condition 1: e.g., Patch all CISA KEV CVEs pre-close]
   □ [Condition 2: e.g., SOC 2 Type II bridge letter (current <12m)]
   □ [Condition 3: e.g., RWI cyber rep sub-limit $25M minimum]
   □ [Condition 4: e.g., CISO retention package — 4yr vesting cliff]

7. VALUATION IMPACT
   Entry EV (stated):         $[X]M at [Y]x ARR
   Cyber risk discount:       -[Z]% ([risk_band] band adjustment)
   Remediation NPV:           -$[W]M (over [hold_period]yr hold)
   ADJUSTED ENTRY EV:         $[X-adj]M at [Y-adj]x ARR

8. STRESS TEST SUMMARY
   Scenario      IRR Estimate    Probability   Key Assumption
   ──────────────────────────────────────────────────────────
   S1 Base       [XX%]           50%           Clean ops
   S2 Breach     [XX%]           25%           T+18m breach
   S3 Regulatory [XX%]           15%           GDPR fine
   S4 Geo/Export [XX%]           10%           BIS escalation
   ──────────────────────────────────────────────────────────
   WEIGHTED IRR   [XX%]    Hurdle [XX%]   [CLEARED / NOT CLEARED]

═══════════════════════════════════════════════════════════════
```

### TEMPLATE-B · TECHNICAL DD REPORT (Full)

```
SECTIONS:
  1. Engagement Scope & Methodology
     1.1 Assessment period; documents reviewed; interviews conducted
     1.2 Tools used: EASM platform, SAST/DAST results, pentest reports
     1.3 Limitations and reliance statements

  2. Architecture Assessment (Engine 1 — CVA)
     2.1 Architecture diagram and security zone mapping
     2.2 SDLC maturity assessment
     2.3 Crown Jewel inventory and protection controls
     2.4 CVA score breakdown by dimension

  3. Attack Surface & Risk Quantification (Engine 2 — SRA)
     3.1 External attack surface inventory
     3.2 Internal segmentation analysis
     3.3 Quantified risk by asset class (FAIR model)
     3.4 Control gap prioritization matrix

  4. M&A-Specific Risk (Engine 3 — CMRE)
     4.1 Breach liability analysis and escrow recommendation
     4.2 Export control classification table
     4.3 Talent/clearance risk register
     4.4 Customer concentration analysis

  5. ARR Quality Analysis (Engine 4 — AQE)
     5.1 Contract terms analysis
     5.2 NRR/GRR cohort waterfall
     5.3 Customer quality segmentation
     5.4 Billings and cash quality assessment

  6. Threat Intelligence Quality (Engine 5 — TIQE)
     6.1 Feed provenance and trust tier analysis
     6.2 Freshness and TTL compliance by IOC type
     6.3 ATT&CK coverage heatmap
     6.4 ISAC participation and STIX/TAXII compliance

  7. Regulatory Compliance Assessment (Engine 6 — RCSE)
     7.1 Framework coverage matrix with scores
     7.2 Audit trail and evidence quality
     7.3 Incident/breach history register
     7.4 Forward-looking regulatory risk (AI Act, DORA)

  8. CVE/Vulnerability Analysis
     8.1 Vulnerability inventory by severity
     8.2 CISA KEV status table
     8.3 EPSS-adjusted priority list
     8.4 MTTR analysis and patch cadence scoring

  9. Investment Decision (Engine 7 — CIDS)
     9.1 Composite scoring and weighting rationale
     9.2 ROSI analysis and EV adjustment
     9.3 4-scenario stress test detail
     9.4 Deal conditions and IC recommendation

  10. Appendices
      A. Flag register (all E-series and D-series flags)
      B. Document request list and response status
      C. Interview log
      D. Tool output excerpts (redacted)
      E. Expert consultant findings (ITAR/export, forensics)
```

### TEMPLATE-C · RED FLAG ESCALATION NOTICE

```
╔════════════════════════════════════════════════════════════╗
║  ⚠  RED FLAG ESCALATION — DD-023 CYBERSECURITY            ║
║  CLASSIFICATION: CONFIDENTIAL — RESTRICTED DISTRIBUTION   ║
╠════════════════════════════════════════════════════════════╣
║  Target:          [COMPANY_NAME]                          ║
║  Deal Code:        [DEAL_CODE]                            ║
║  Escalation Time:  [ISO_TIMESTAMP]                        ║
║  Triggered By:     [ANALYST] / [ENGINE_ID]                ║
╠════════════════════════════════════════════════════════════╣
║  FLAG TYPE:  [E-XX / D-XX]                                ║
║  SEVERITY:   [CRITICAL / HIGH / MEDIUM]                   ║
║  STATUS:     [ACTIVE / UNDER_REVIEW / RESOLVED]           ║
╠════════════════════════════════════════════════════════════╣
║  FINDING SUMMARY:                                         ║
║  [2~3 sentence description of the specific finding,       ║
║   evidence source, and immediate risk implication]        ║
╠════════════════════════════════════════════════════════════╣
║  EVIDENCE BASE:                                           ║
║  • [Document/source 1 with date]                         ║
║  • [Document/source 2 with date]                         ║
║  • [Third-party confirmation if available]               ║
╠════════════════════════════════════════════════════════════╣
║  REQUIRED ACTIONS:                                        ║
║  □ [Action 1: owner / deadline]                          ║
║  □ [Action 2: owner / deadline]                          ║
║  □ [Action 3: legal/compliance notification if needed]   ║
╠════════════════════════════════════════════════════════════╣
║  IC IMPACT ASSESSMENT:                                    ║
║  Composite score delta:  [±X.X points]                   ║
║  EV impact estimate:     [-$XM to -$YM range]            ║
║  Deal recommendation:    [PROCEED / CONDITION / PAUSE /  ║
║                           REJECT]                         ║
╚════════════════════════════════════════════════════════════╝

Distribution: Deal Lead | General Counsel | Risk Committee | Fund CISO
```

---

## ESCALATION TRIGGER TREE v1.1

```
ROOT TRIGGER CHECK (run at DD initiation and daily during active DD)
│
├─ ANY D-series flag triggered?
│    YES → IMMEDIATE_REJECT → Notify: GP + GC + Compliance Officer
│    NO  → Continue to E-series gate
│
├─ Critical E-series flags (E-01 to E-06): count ≥ 1?
│    YES → PARTNER_ESCALATION within 4h
│          → Pre-IC risk memo required (T-3 days before IC)
│          → Expert consultant engagement (ITAR/forensics/export)
│    NO  → Continue
│
├─ Operational E-series flags (E-07 to E-12): count ≥ 3?
│    YES → DEAL_LEAD_ESCALATION within 24h
│          → Seller notification for remediation plan
│          → Deal condition term sheet draft
│    NO  → Continue
│
├─ Regulatory flags (E-09, E-15, E-16) triggered?
│    YES → LEGAL_COUNSEL_NOTIFICATION (same day)
│          → Jurisdiction-specific specialist engagement
│          → Government notification assessment (mandatory reporting?)
│    NO  → Continue
│
├─ Composite score < 5.0?
│    YES → GP-LEVEL_DECISION (deal team cannot proceed without GP approval)
│    NO  → Continue
│
├─ Stress test: any scenario IRR < hurdle AND probability > 20%?
│    YES → QUANTITATIVE_RE-EXAMINATION; re-run with updated assumptions
│    NO  → Continue
│
└─ ALL GATES CLEAR → Standard IC process; include flag summary in IC deck

RESPONSE TIME SLA:
  D-series:               IMMEDIATE (within 1h of discovery)
  Critical E-series:      4 hours
  Operational E-series:   24 hours
  Regulatory flags:       Same business day
  Composite score <5.0:   48 hours (GP schedule)
  Standard flag:          Next deal team update cycle
```

---

## v1.0 → v1.1 DELTA REGISTRY

### Version Control Header
```
Prompt ID:     DD-023
Domain:        Cybersecurity & Data Security Due Diligence
Version:       v1.1
Release Date:  2026-05-09
Prior Version: v1.0 (2025; single-file, 29,942 bytes)
Authored by:   PE System — GilbertKwak / Perplexity AI
File structure: 3-part split (Part1: ~23KB | Part2: ~18KB | Part3: ~[this file])
PE-3 Target Score: 95+
Change scope:  MAJOR UPGRADE (architecture, engines, scoring, output)
```

### DELTA CATALOG

| Delta ID | Category | Change Description | v1.0 State | v1.1 State | Impact |
|---|---|---|---|---|---|
| Δ-001 | Structure | File split into 3 parts | Single 30KB file | 3-part modular (Part1/2/3) | Load efficiency; modularity |
| Δ-002 | Engine | Engine 3 CMRE Export Control Module | Basic export flag | Full EAR/ITAR/Wassenaar/DECA coverage | E-15 precision ↑ |
| Δ-003 | Engine | Engine 3 CMRE Talent Module | Headcount/attrition | Clearance/deemed export/TCP | Gov deal applicability ↑ |
| Δ-004 | Engine | Engine 4 AQE — new (v1.0 absent) | Not present | Full 4-dimension ARR quality | ARR rigor ↑ |
| Δ-005 | Engine | Engine 5 TIQE — new (v1.0 absent) | Not present | Feed provenance + ATT&CK coverage | TI vendor DD ↑ |
| Δ-006 | Engine | Engine 6 RCSE — new (v1.0 absent) | Basic compliance list | 3-module 30-point framework | Regulatory depth ↑ |
| Δ-007 | Engine | Engine 7 CIDS — new (v1.0 absent) | Not present | D-series + 4-scenario stress test | Investment decision rigor ↑ |
| Δ-008 | CVE | CVE/CVSS v3.1 auto-scoring module | Manual flag only | EPSS v3 + CISA KEV + NVD API v2 | Vulnerability triage precision ↑ |
| Δ-009 | Scoring | 18-Layer scoring matrix | 8-layer (estimated) | Full 18-layer weighted framework | Score consistency ↑ |
| Δ-010 | Scoring | Hard Disqualifier registry | 3 disqualifiers (E-series) | 9 D-series (D-01~D-09) | Deal protection ↑ |
| Δ-011 | Output | Executive Summary template | Narrative only | Structured TEMPLATE-A scorecard | IC readiness ↑ |
| Δ-012 | Output | Technical DD Report template | Ad hoc | 10-section TEMPLATE-B | Standardization ↑ |
| Δ-013 | Output | Red Flag Escalation Notice | Email prose | TEMPLATE-C structured form | Response time ↓ |
| Δ-014 | Escalation | Escalation trigger tree | Manual judgment | Automated 6-gate trigger tree with SLAs | Consistency ↑ |
| Δ-015 | Regulation | NIS2 Directive coverage | Mentioned briefly | Module A Tier-2 full scoring | EU coverage ↑ |
| Δ-016 | Regulation | DORA coverage | Not present | Module A Tier-3 scoring | EU financial sector ↑ |
| Δ-017 | Regulation | EU AI Act coverage | Not present | Module A Tier-3 forward risk | AI product DD ↑ |
| Δ-018 | Regulation | SEC Cybersecurity Rule (Dec 2023) | Not present | Module A Tier-3 scoring | US public target ↑ |
| Δ-019 | ROSI | Return on Security Investment framework | Not present | Full ROSI formula + EV adjustment | Valuation discipline ↑ |
| Δ-020 | Market | MITRE Engenuity ATT&CK Evals integration | Not referenced | TIQE Step 4 third-party correlation | TI benchmark ↑ |

### Backward Compatibility Notes
```
- DD-023 v1.1 is NOT backward compatible with v1.0 scoring outputs
- All v1.0 scores must be re-run using v1.1 engines before IC presentation
- Engine 4 (AQE) and Engine 6 (RCSE) are net-new; v1.0 deals lack these scores
- TEMPLATE-A/B/C replace all v1.0 ad hoc output formats
- D-series disqualifiers supersede E-series escalation for listed conditions
```

### Known Limitations & Future Development (v1.2 Roadmap)
```
L-01: OT/ICS Security Engine (PE-SEMI integration) — targeted for v1.2
L-02: AI/ML Security Assessment Module (adversarial ML, model poisoning) — v1.2
L-03: Quantum Computing Cryptography Risk Module (post-quantum readiness) — v1.3
L-04: Automated NVD API v2.0 live pull integration — v1.2 pipeline automation
L-05: CVSS v4.0 adoption (released Oct 2023; full integration) — v1.2
L-06: BFSI-specific DORA ICT sub-contractor chain scoring — v1.2
```

---

*[Part 3 of 3 — DD-023 v1.1 COMPLETE]*
*[Part 1: Header / Role Definition / 7 Security Zones / 16 Guard Rails / Engines 1~2 (CVA, SRA)]*
*[Part 2: Engines 3~5 (CMRE, AQE, TIQE)]*
*[Part 3: Engines 6~7 (RCSE, CIDS) / 18-Layer Matrix / Output Templates / Escalation Tree / Delta Registry]*
