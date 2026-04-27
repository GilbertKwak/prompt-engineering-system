# JV Fund Prompt Library

> **Domain:** Global Joint Venture Fund Analysis  
> **Maintained by:** Gilbert Kwak  
> **Last Updated:** 2026-04-27

---

## Overview

This directory contains the master prompt system for Global Joint Venture (JV) Fund analysis across semiconductor, thermal management, AI infrastructure, and sCO₂ energy domains.

## File Structure

```
prompts/jv_fund/
├── README.md                    ← This file
├── master_v3.md                 ← ✅ Current master prompt (PE-1/PE-3 validated)
└── variants/
    ├── hbm_salvage_variant.md   ← HBM & Salvage Value JV analysis
    ├── bstar_eco2_variant.md    ← B-Star sCO₂ strategy JV analysis
    ├── ai_infra_variant.md      ← AI Data Center infrastructure JV analysis
    └── fu_series_adapter.md    ← FU-Series report integration adapter
```

## Quick Start

1. Open `master_v3.md`
2. Set the `[CONTEXT PARAMETERS]` for your analysis
3. Execute the 5-step `[TASK CHAIN]`
4. Validate output against `[VALIDATION RULES]` (PE-1 + PE-3)
5. Run `python automation/auto_validate.py --rules PE-1,PE-3` for automated check

## Version History

| Version | File | Status |
|---|---|---|
| v3.0 | `master_v3.md` | ✅ Active |
| v2.0 | `Global_Joint_Venture_Fund_Master_Prompt_v2.txt` | 🗄 Archived |

## Validation

All prompts in this directory must pass:
- **PE-1:** Source citation standard (numerical claims cited)
- **PE-3:** Counter-scenario requirement (bear case included)

Run validation:
```bash
python automation/auto_validate.py \
  --file prompts/jv_fund/master_v3.md \
  --rules PE-1,PE-3 \
  --output reports/validation_jv_fund_v3.json
```

## Related Resources

- **Notion:** JV Fund Prompt Library page (workspace link)
- **GitHub Actions:** `.github/workflows/prompt_validate.yml`
- **FU-Series Reports:** `applied-cases/` directory
