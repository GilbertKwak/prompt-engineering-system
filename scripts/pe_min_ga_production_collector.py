#!/usr/bin/env python3
"""
PE-MIN Gallium Production Collector — v1.0
5개 기관: USGS, EU CRMA, JOGMEC, KCMA, NRCan
"""
import argparse, json, os
from datetime import datetime, timezone

AGENCY_SOURCES = {
    "USGS":    {"url": "https://www.usgs.gov/centers/national-minerals-information-center/gallium", "region": "Americas"},
    "EU_CRMA": {"url": "https://rmis.jrc.ec.europa.eu/", "region": "Europe"},
    "JOGMEC":  {"url": "https://mric.jogmec.go.jp/", "region": "Asia-Pacific"},
    "KCMA":    {"url": "https://www.kores.net/", "region": "Korea"},
    "NRCan":   {"url": "https://www.nrcan.gc.ca/mining-materials/minerals-metals/", "region": "Canada"},
}

def collect_agency_data(agency: str, month: str, api_key: str = "") -> dict:
    """개별 기관 생산량 수집 스캐폴드"""
    # Production: Implement per-agency scraping/API calls
    return {
        "agency": agency,
        "month": month,
        "tons": 0.0,       # Fill with actual data
        "source_url": AGENCY_SOURCES.get(agency, {}).get("url", ""),
        "collected_at": datetime.now(timezone.utc).isoformat()
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--agencies", default="USGS,EU_CRMA,JOGMEC,KCMA,NRCan")
    parser.add_argument("--month", default="")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    api_key = os.environ.get("USGS_API_KEY", "")
    agency_list = args.agencies.split(",")

    # Determine reference month
    if not args.month:
        now = datetime.now(timezone.utc)
        if now.month == 1:
            ref = f"{now.year-1}-12"
        else:
            ref = f"{now.year}-{now.month-1:02d}"
    else:
        ref = args.month

    results = {}
    for agency in agency_list:
        results[agency] = collect_agency_data(agency.strip(), ref, api_key)

    output = {
        "reference_month": ref,
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "agencies": results
    }

    os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else ".", exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"✅ Production data collected ({ref}) → {args.output}")


if __name__ == "__main__":
    main()
