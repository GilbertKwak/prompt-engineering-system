# DD-023 · Cybersecurity & Data Security Due Diligence v1.1
*[Part 2 of 3 — Engines 3, 4, 5 | Preceded by Part 1: Header/Role/Zones/Guards/Engines 1-2]*

---

## ENGINE 3 · CYBER M&A RISK ENGINE v1.1 (CMRE)

```
FUNCTION assess_cyber_ma_risk_v1.1(target, acquirer, deal_structure,
                                    breach_history, export_data, talent_data):

  MODULE A — BREACH LIABILITY TRANSFER ANALYSIS:

    Pre-close breach assessment:
      Disclosed breaches: SEC 8-K / 20-F audit trail (Dec 2023 rule; check 3-year lookback)
      EU NIS2: significant incident notification history to national CSIRTs
      GDPR: DPA investigation / enforcement notice history (ICO, CNIL, BfDI, Garante)
      Undisclosed breach screening:
        Dark web: credential dump, PII sale, IP leak correlated to target
        Threat intelligence: APT targeting history; Mandiant / CrowdStrike dossier
        IF undisclosed material breach found → E-16 HARD HALT

    Liability transfer mechanics:
      Asset deal: buyer generally avoids pre-close liabilities; verify jurisdiction carve-outs
      Stock deal: full successor liability; cyber rep carve-out critical
      Rep & Warranty Insurance (RWI):
        Cyber breach rep: sublimit typically $10~50M; verify exclusion scope
        Incident response cost: separate cyber insurance policy required
        Known breach exclusion: any breach discovered in DD = excluded from RWI
      Indemnity escrow: 10~20% of deal value; 18~24 month tail; cyber carve-out survival
      Regulatory consent condition precedent: GDPR DPA / FTC / CISA notification required?

    Post-close breach risk:
      Silent cyber: property/liability policy exclusion of cyber events
      Ransomware: payment prohibition laws (OFAC SDN list payment = federal violation)
      Notification cost: average breach notification $4.5M (IBM 2024); IC scenario model

  MODULE B — TECHNOLOGY EXPORT CONTROL (upgraded v1.1):

    Cryptographic software classification:
      Strong crypto (>56-bit key): EAR ECCN 5E002; ENC review required
      Exception ENC: self-classification for standard commercial crypto
      Mass-market exception: meets criteria? Notify BIS; 30-day review
      IF non-EAR99 AND export to adversary-nation: license required; E-15 CRITICAL

    Intrusion / surveillance / offensive security tools:
      Penetration testing platform: Metasploit-style → ECCN 4D004 / 4E001.b.1
      Vulnerability scanner with exploit capability: dual-use; Wassenaar 4.A.5
      Dark web crawler / monitoring platform: Wassenaar 6.A.5 (intelligence gathering)
      Deepfake detection (dual-use: also creation capability): case-by-case assessment

    Israel-origin technology:
      Unit 8200 heritage: Defense Ministry Export Control Agency (DECA) license required
      Pegasus precedent: offensive cyber tool = export restriction to most jurisdictions
      NSO Group / Cellebrite precedent: assess whether product falls in similar category
      Mitigation: US entity holding structure; DECA license confirmation pre-close

    Cross-border data flow:
      CLOUD Act (US): government compulsion risk for non-US data
      GDPR Chapter V: adequacy decision / SCC / BCR requirement
      China PIPL: CAC security assessment for >$1M/year data export volume
      Russia PDPD: data localization requirement for Russian citizens' data

  MODULE C — TALENT & KEY PERSON RISK (upgraded v1.1):

    Security research talent depth:
      Named CVE researchers: count of researchers with published CVEs (last 5 years)
      Conference presence: DEF CON / Black Hat / CCS / Usenix Security talks (last 3 years)
      Bug bounty hunters: in-house security research vs. outsourced bounty program
      Research retention: equity vesting schedule; competing hyperscaler offers (MSFT/GOOG)

    Government clearance requirements:
      FedRAMP High: requires US citizens only for privileged access roles
      CMMC Level 3: facility clearance (FCL) required for CUI handling
      ITAR compliance: foreign national access to controlled technology = deemed export
      Clearance transfer: existing clearances transferable in acquisition? (DSS/DCSA process)

    Deemed export risk:
      Foreign national employees with access to EAR/ITAR-controlled cyber tech:
        PRC nationals: automatic enhanced review; license typically denied for USML
        Five-Eyes (UK/AU/CA/NZ): favorable; STA license exception eligible
        Other allied nations: case-by-case; Technology Control Plan (TCP) required
      Remote work: foreign national working remotely = deemed export in their jurisdiction

    Cultural / integration risk:
      Offensive vs. defensive culture: red team DNA acquirer + blue team target = friction
      Startup research culture: PE cost discipline vs. security research autonomy tension
      Anonymous / pseudonymous researcher community: identity disclosure risk (internal)
      CISO/CTO departure risk: assess equity overhang; retention package structure

  MODULE D — CUSTOMER CONCENTRATION & CHURN RISK (upgraded v1.1):

    Revenue concentration tiers:
      Top-1 customer >25% ARR: KEY_CUSTOMER_RISK (E-05 trigger)
      Top-3 customers >40% ARR: HIGH_CONCENTRATION
      Top-10 customers >60% ARR: MODERATE; monitor
      Single vertical >50% ARR: VERTICAL_CONCENTRATION

    Government customer specifics:
      FedRAMP: recompete cycle risk (typically 5-year IDIQ); CR dependency
      CMMC assessment: defense contractor customer = supply chain compliance requirement
      Appropriations risk: cybersecurity often discretionary in CR environment
      Sole-source vs. competitive: sole-source contract = high renewal risk at recompete

    Enterprise churn mechanics:
      Logo churn: net logo retention rate (benchmark: >92% for enterprise)
      Expansion: upsell to additional modules / users / coverage areas
      Down-sell risk: budget pressure driving module consolidation (platform threat)
      Net Revenue Retention (NRR) by cohort: 12/24/36-month waterfall required

    MSSP subcontractor breach liability:
      MSSP customer SLA: breach notification SLA; penalties for late disclosure
      Sub-processor liability: GDPR Article 28; downstream liability chain
      Cyber insurance pass-through: does MSSP's policy cover customer breach costs?

  COMPOSITE CMRE SCORE:
    Module A — Breach Liability:      0~2.5
    Module B — Export Control:        0~2.5
    Module C — Talent & Clearance:    0~2.5
    Module D — Customer/Churn Risk:   0~2.5
    TOTAL CMRE SCORE: 0~10

    Risk bands:
      0.0~3.0: LOW — standard DD; proceed
      3.1~5.5: MODERATE — enhanced DD; pre-IC risk memo
      5.6~7.5: ELEVATED — re-price; condition precedents required
      7.6~10.0: CRITICAL — deal-breaker absent material remediation

  RETURN:
    {breach_liability_score, export_score, talent_score, churn_score,
     total_cmre_score, risk_band, deal_conditions, flags}
```

---

## ENGINE 4 · ARR QUALITY ENGINE v1.1 (AQE)

```
FUNCTION score_arr_quality_v1.1(arr_schedule, contract_terms, churn_data,
                                 cohort_data, billing_data, segment_data):

  DIMENSION 1 — CONTRACT QUALITY (0~2.5):
    Contract duration mix:
      3yr+: 2.5 | 2yr: 2.0 | 1yr: 1.5 | M2M/quarterly: 0.5 | Perpetual: 1.0
    Price escalation clause:
      CPI-linked or fixed % uplift: +0.3 | Ad hoc / none: 0
    Auto-renewal provision:
      Opt-out structure (default renew): +0.2 | Opt-in: 0
    Termination for convenience:
      No T4C: +0.2 | T4C with 90d+ notice: 0 | T4C with <30d: -0.3
    Government IDIQ adjustment:
      Funded task orders only; unfunded ceiling ≠ ARR; apply 20% discount to IDIQ ceiling
    D1_SCORE = weighted_sum(duration_score + escalation + auto_renew + t4c)
    D1_SCORE cap: 2.5

  DIMENSION 2 — REVENUE RETENTION (0~2.5):
    Net Revenue Retention (NRR) — primary metric:
      >135%: 2.5 (Best-in-class; Snowflake / Datadog benchmark)
      125~135%: 2.2
      115~125%: 2.0 (Excellent)
      110~115%: 1.7
      105~110%: 1.5 (Good)
      100~105%: 1.2 (Acceptable)
      95~100%: 0.8 (Below benchmark; monitor)
      90~95%: 0.4 (Net churn; E-07 FLAG)
      <90%: 0.0 (Structural churn; HARD FLAG; deal re-price trigger)
    Gross Revenue Retention (GRR) — floor check:
      GRR <85%: STRUCTURAL FLAG; E-07 mandatory; impacts D2 score ×0.8
    Cohort retention analysis:
      12-month NRR by segment (enterprise/mid-market/SMB/government)
      24-month NRR: >100% = expansion; 36-month: maturity/plateau indicator
    Churn root cause:
      Budget-driven: cyclical; recoverable
      Product displacement: structural; discount D2 ×0.75
      M&A customer consolidation: deal-specific; assess survivability

  DIMENSION 3 — CUSTOMER QUALITY (0~2.5):
    Enterprise mix (>1K FTE employees):
      >70% enterprise: 2.5 | 50~70%: 2.0 | 30~50%: 1.5 | <30%: 0.8
    Regulated sector premium:
      BFSI / Healthcare / Government: stickiness multiplier ×1.15
      Critical infrastructure: ×1.2 (budget-protected, mission-critical)
    FedRAMP authorized customer base:
      Federal ARR >20%: sovereign quality premium (Z-7 COUNTER)
    Fortune 500 / Global 2000 logos:
      >20% of ARR from F500/G2000: brand validation; churn resistance
    Logo concentration penalty (E-05):
      Top-1 >25% ARR: D3_SCORE ×0.85
      Top-3 >45% ARR: D3_SCORE ×0.75

  DIMENSION 4 — BILLINGS & CASH QUALITY (0~2.5):
    Billings-to-ARR ratio:
      Billings > ARR growth: +0.5 (prepayment; strong demand signal)
      Billings = ARR: 0 (neutral)
      Billings < ARR: -0.5 (deferred recognition; investigate pull-forward)
    Deferred revenue trend:
      Growing QoQ: +0.3 | Flat: 0 | Declining >10%: -0.5 (pull-forward risk)
    Days Sales Outstanding (DSO):
      <30d: +0.3 | 30~45d: 0 | 46~60d: -0.2 | 61~90d: -0.4 | >90d: -0.8
    Cash conversion:
      Annual prepay %: >60% prepay = quality signal; M2M billing = risk
    Professional services mix:
      PS <15% of total revenue: +0.2
      PS 15~30%: 0
      PS >30%: -0.5 (E-07 FLAG; revenue quality dilution)

  AQE_SCORE = D1 + D2 + D3 + D4 (0~10)

  RATING TABLE:
    9.0~10.0: PLATINUM — platform-grade; full buyout at premium; Tier-A/B comparable
    7.5~8.9:  GOLD — quality ARR; growth equity at benchmark multiple
    6.0~7.4:  SILVER — solid; monitor D2 churn; growth equity with conditions
    4.0~5.9:  BRONZE — re-examine contract structure; re-price; conditional IC approval
    0~3.9:    RED — structural ARR risk; E-07 FLAG mandatory; deal re-price or pass

  CROSS-DIMENSION FLAGS:
    IF NRR <100% AND D1_SCORE <1.5: E-07 DOUBLE FLAG (structural + contract weakness)
    IF D3 concentration penalty applied AND D2 <1.5: concentrated churn risk = IC red flag
    IF D4 DSO >90d AND deferred revenue declining: cash quality concern = OPT-DD-FIN v1.1

  RETURN:
    {d1_contract, d2_retention, d3_customer, d4_billings,
     aqe_score, aqe_rating, flags, routing_triggers}
```

---

## ENGINE 5 · THREAT INTELLIGENCE QUALITY ENGINE (TIQE) [NEW v1.1]

```
FUNCTION assess_threat_intelligence_quality(ti_platform_data, feed_data,
                                             accuracy_data, sharing_data,
                                             export_data):

  CONTEXT: Applies to TIER-H (TIP/CTI) vendors AND any cybersecurity product
           embedding third-party TI feeds. Also applies when assessing MSSP/MDR
           TI consumption quality for customer DD.

  STEP 1 — FEED PROVENANCE CLASSIFICATION (Z-12 activation):

    Provenance taxonomy:
      GOV_TIER (highest trust):
        CISA AIS (Automated Indicator Sharing)
        NCSC (UK) / BfV (DE) / ANSSI (FR) / AISI (AU) / KISA (KR) government feeds
        FBI / IC3 / INTERPOL partner feeds
        → TRS weight: A (×1.00); no restrictions

      COMMERCIAL_TIER (high trust):
        Mandiant / CrowdStrike Adversary Intelligence
        Recorded Future / Flashpoint / Intel471
        Microsoft MSTIC / Google TAG / Amazon CTIP
        → TRS weight: B (×0.85); verify contractual freshness SLA

      OSINT_TIER (moderate trust):
        AlienVault OTX / MISP community / VirusTotal
        CIRCL feeds / Abuse.ch (URLhaus, MalwareBazaar, ThreatFox)
        Twitter/X threat researcher community (CTI community)
        → TRS weight: C (×0.65); cross-validate with GOV or COMMERCIAL tier

      ADVERSARY_SOURCED (HARD DISQUALIFIER):
        Feeds with confirmed CN/RU/IR intelligence apparatus origin
        Underground marketplace data (without disclosure of source)
        Unlicensed exploit/vulnerability intelligence from adversary-nation entities
        → E-18 HARD HALT; automatic deal disqualification

  STEP 2 — FEED FRESHNESS & COVERAGE ASSESSMENT (Z-12 TTL compliance):

    Indicator Type TTL Benchmarks:
      IP address indicators:  TTL benchmark <72h; >7d = STALE FLAG
      Domain indicators:      TTL benchmark <7d; >30d = STALE FLAG
      File hash indicators:   TTL benchmark <30d; >90d = STALE FLAG
      YARA/Sigma rules:       TTL benchmark <90d; >180d = REFRESH REQUIRED
      TTP (MITRE ATT&CK):     TTL benchmark <180d; >365d = OUTDATED
      Vulnerability intel:    TTL benchmark = NVD/EPSS sync cycle (<7d)

    IOC/IOA volume metrics:
      Active IOC count: benchmark by tier (>100K for commercial TIP)
      IOA coverage: MITRE ATT&CK techniques covered (target: >60% of techniques)
      Threat actor profiles: named APT groups; attribution confidence level
      Industry vertical coverage: does TI cover target's customer verticals?

    Feed staleness score:
      % of IOCs within TTL: >90% = FRESH (10/10) | 75~90% = ACCEPTABLE (7/10) |
                             50~75% = STALE (4/10) | <50% = OUTDATED (1/10) + E-18 FLAG

  STEP 3 — ACCURACY & FALSE POSITIVE RATE ASSESSMENT:

    False Positive Rate (FPR) benchmarks:
      FPR <5%:  EXCELLENT (10/10)
      FPR 5~10%: GOOD (8/10)
      FPR 10~15%: ACCEPTABLE (6/10)
      FPR 15~25%: HIGH (3/10) → E-18 FLAG; SOC alert fatigue risk
      FPR >25%: CRITICAL (0/10) → E-18 HALT; operational impact on customer SOC

    Accuracy validation methods:
      Third-party benchmark: VirusTotal consensus / MISP community cross-validation
      A/B testing: production hit rate vs. ground truth (retroactive analysis)
      Red team validation: own red team using TI; false negative rate measurement
      Customer SOC feedback: alert-to-incident conversion rate (AICAR)
        AICAR >40%: EXCELLENT | 25~40%: GOOD | 10~25%: ACCEPTABLE | <10%: POOR

    Self-reported accuracy: TRS D (×0.40) weight; independent validation required

  STEP 4 — MITRE ATT&CK COVERAGE QUANTIFICATION (v1.1 new feature):

    ATT&CK Framework coverage matrix:
      Tactics covered (14 total):
        TA0001 Initial Access | TA0002 Execution | TA0003 Persistence
        TA0004 Privilege Escalation | TA0005 Defense Evasion | TA0006 Credential Access
        TA0007 Discovery | TA0008 Lateral Movement | TA0009 Collection
        TA0010 Exfiltration | TA0011 Command & Control | TA0040 Impact
        TA0042 Resource Development | TA0043 Reconnaissance

      Coverage scoring:
        Tactic coverage: % of 14 tactics with at least 1 detection
        Technique coverage: % of ~750 techniques (Enterprise ATT&CK v15)
        Sub-technique depth: average sub-techniques per covered technique

      Coverage tiers:
        Technique coverage >60%: COMPREHENSIVE → market-leading; premium multiple
        Technique coverage 40~60%: SOLID → competitive; benchmark multiple
        Technique coverage 20~40%: ADEQUATE → specialist; niche premium
        Technique coverage <20%: LIMITED → point solution risk; discount multiple

      Third-party evaluation correlation:
        MITRE Engenuity ATT&CK Evals: analytic coverage score; technique detection rate
        SE Labs AAA rating: detection accuracy certification
        AV-TEST Advanced+ certification: endpoint protection benchmark

  STEP 5 — STRUCTURAL TI SHARING & ISAC ASSESSMENT:

    Information Sharing:
      ISAC membership (relevant by customer vertical):
        FS-ISAC (financial): required for BFSI-heavy customer base
        H-ISAC (healthcare): required for healthcare vertical
        E-ISAC (energy): required for energy / OT customer base
        Space ISAC: required for space/satellite customers (DD-026 cross-ref)
        Auto-ISAC (automotive): connected vehicle OT customer
      MISP sharing group participation: community contribution score
      STIX/TAXII v2.1 compliance: structured format; machine-readable sharing
        Non-STIX/TAXII: proprietary format = interoperability penalty (-1 to TI score)

    TI weaponization assessment (E-15 cross-activation):
      Does the platform enable offensive operations?
        Offensive capability indicators:
          Exploit marketplace access / zero-day acquisition
          Malware reverse engineering tools with deployment capability
          Dark web marketplace operator (not just monitoring)
          Active C2 infrastructure simulation
        IF offensive_capability = YES:
          → Wassenaar Arrangement Category 4.A.5 review required
          → EAR ECCN 4E001.b.1 / 4D004 classification
          → E-15 EXPORT_GUARD activate
          → Israeli-origin: DECA license assessment

  TIQE_SCORE calculation:
    Provenance quality:    25% weight (Gov=10, Commercial=8, OSINT=6, Adversary=DISQUALIFY)
    Feed freshness:        20% weight (0~10 per TTL compliance)
    Accuracy (FPR):        25% weight (0~10 per FPR benchmark)
    ATT&CK coverage:       20% weight (0~10 per technique coverage %)
    Sharing & structure:   10% weight (0~10 per ISAC + STIX/TAXII)

    TIQE_SCORE = weighted_sum (0~10)

    Rating:
      8.5~10.0: PREMIUM TI — market-leading; Recorded Future / Mandiant-tier
      7.0~8.4:  QUALITY TI — competitive product; benchmark multiple
      5.0~6.9:  ADEQUATE TI — point solution; monitor freshness and FPR
      3.0~4.9:  WEAK TI — re-examine feed sourcing; conditional go
      <3.0:     DISQUALIFIED — adversary source OR FPR >25% OR provenance unknown

  OUTPUT:
    TIQE_REPORT:
      provenance_tier: [GOV/COMMERCIAL/OSINT/ADVERSARY]
      feed_freshness_score: [0~10]
      fpr: [X%] | accuracy_score: [0~10]
      attack_coverage: [X% techniques / Y tactics]
      isac_membership: [list]
      stix_taxii_compliant: [YES/NO]
      weaponization_flag: [NONE/WASSENAAR_REVIEW/E-15_TRIGGERED]
      tiqe_score: [0~10]
      tiqe_rating: [PREMIUM/QUALITY/ADEQUATE/WEAK/DISQUALIFIED]
      flags: [E-18_HALT | STALE_FEED | HIGH_FPR | ADVERSARY_SOURCE |
              NO_ISAC | WEAPONIZATION_RISK | NON_STIX]
```

---

*[Part 2 of 3 — Continues in Part 3: Engine 6 RCSE + Engine 7 CIDS + 18-Layer Framework + Output Format + Scoring Matrix]*
