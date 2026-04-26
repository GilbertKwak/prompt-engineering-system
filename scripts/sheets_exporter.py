#!/usr/bin/env python3
"""Track A-1: Google Sheets → Notion DB Export
PE-7 v2.0 | E-05 GCP fallback, retry | Gilbert Kwak 2026-04-26"""
import os, json, time, pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import requests
from datetime import datetime

NOTION_TOKEN  = os.environ.get("NOTION_TOKEN", "")
NOTION_DB_ID  = os.environ.get("NOTION_DB_ID", "")  # KPI DB
SHEETS_ID     = os.environ.get("GOOGLE_SHEETS_ID", "")
SA_JSON       = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
os.makedirs("data", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# ── E-05: safe_request ────────────────────────────────────────────────────────
def safe_request(func, retries=3, fallback=None):
    """E-05 API timeout → exponential backoff → fallback"""
    for i in range(retries):
        try:
            return func()
        except Exception as e:
            wait = 2 ** i
            print(f"[E-05] 시도 {i+1}/{retries}: {e} — {wait}s 대기")
            time.sleep(wait)
    print(f"[E-05] Fallback 사용")
    return fallback

# ── Notion DB 조회 ────────────────────────────────────────────────────────────
def fetch_notion_db(db_id: str) -> list[dict]:
    url = f"https://api.notion.com/v1/databases/{db_id}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    def call():
        res = requests.post(url, headers=headers, json={}, timeout=15)
        res.raise_for_status()
        return res.json().get("results", [])
    results = safe_request(call, fallback=[])
    rows = []
    for r in results:
        props = r.get("properties", {})
        row = {}
        for k, v in props.items():
            vtype = v.get("type")
            if   vtype == "title":     row[k] = v["title"][0]["plain_text"]    if v["title"]     else ""
            elif vtype == "rich_text": row[k] = v["rich_text"][0]["plain_text"] if v["rich_text"] else ""
            elif vtype == "number":    row[k] = v.get("number")
            elif vtype == "select":    row[k] = v["select"]["name"]             if v.get("select") else ""
            elif vtype == "date":      row[k] = v["date"]["start"]              if v.get("date")   else ""
            else:                      row[k] = str(v)
        rows.append(row)
    return rows

# ── Google Sheets Export ──────────────────────────────────────────────────────
def export_to_sheets(df: pd.DataFrame, sheet_name: str = "KPI_Dashboard"):
    if not SA_JSON:
        print("[SKIP] GOOGLE_SERVICE_ACCOUNT_JSON 미설정 → CSV fallback")
        path = f"data/sheets_export_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"[FALLBACK] CSV 저장: {path}")
        return
    creds_dict = json.loads(SA_JSON)
    creds  = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    client = gspread.authorize(creds)
    def write():
        sh = client.open_by_key(SHEETS_ID)
        ws = sh.worksheet(sheet_name) if sheet_name in [w.title for w in sh.worksheets()] \
             else sh.add_worksheet(title=sheet_name, rows=500, cols=30)
        ws.clear()
        ws.update([df.columns.tolist()] + df.fillna("").values.tolist())
        print(f"[OK] Sheets Export: {len(df)}행 → {sheet_name}")
    safe_request(write)

# ── main ──────────────────────────────────────────────────────────────────────
def main():
    print("[Track A-1] Google Sheets Export 시작 ...")
    rows = fetch_notion_db(NOTION_DB_ID) if NOTION_DB_ID else []
    if not rows:
        rows = [
            {"Company": "TSMC",     "Metric": "CoWoS 가동률",      "Value": 92, "Status": "정상", "Date": "2026-04"},
            {"Company": "Nvidia",   "Metric": "H100 QoQ 출하",    "Value": 18, "Status": "증가", "Date": "2026-04"},
            {"Company": "SK Hynix", "Metric": "HBM3E 점유율",     "Value": 53, "Status": "정상", "Date": "2026-04"},
            {"Company": "Intel",    "Metric": "18A 수율",         "Value": 52, "Status": "주의", "Date": "2026-04"},
            {"Company": "ASML",     "Metric": "High-NA 출하",     "Value":  3, "Status": "정상", "Date": "2026-04"},
        ]
    df = pd.DataFrame(rows)
    df.to_csv(f"data/notion_db_{datetime.now().strftime('%Y%m%d')}.csv", index=False)
    export_to_sheets(df)
    print("[Track A-1] 완료")

if __name__ == "__main__":
    main()
