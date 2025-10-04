#!/usr/bin/env python3
"""
OpenPhish homepage parser
- Visits https://openphish.com/ at a fixed interval
- Parses the main table (URL, Brand, Attack time)
- De-duplicates by URL and Attack time
- Persists to CSV between runs
- Prints summary when finished

Usage examples:
  python openphish_parser.py --interval 300 --duration 3600 --out openphish_data.csv
  python openphish_parser.py --interval 10 --duration 60 --out test.csv  # quick test
"""

import argparse
import csv
import sys
import time
from dataclasses import dataclass
from typing import List, Tuple
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup
import pandas as pd


@dataclass
class PhishRow:
    url: str
    brand: str
    attack_time: str


def fetch_rows(session: requests.Session) -> List[PhishRow]:
    """Fetch and parse rows from the OpenPhish homepage table.
    Returns a list of PhishRow. If parsing fails, returns an empty list.
    """
    url = "https://openphish.com/"
    try:
        resp = session.get(url, timeout=20, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        resp.raise_for_status()
    except Exception as e:
        print(f"[WARN] HTTP error: {e}", file=sys.stderr)
        return []

    soup = BeautifulSoup(resp.text, "html.parser")

    # Try to find the main table. The page structure could change; we try a few heuristics.
    table = None
    # Heuristic 1: first <table> on page
    table = soup.find("table")
    if table is None:
        print("[WARN] No <table> found on the page. The site may have changed or requires JS.", file=sys.stderr)
        return []

    rows = []
    for tr in table.find_all("tr"):
        tds = tr.find_all(["td", "th"])
        if len(tds) < 3:
            continue

        # Extract fields; attempt to map by position
        url_cell = tds[0].get_text(strip=True)
        brand_cell = tds[1].get_text(strip=True)
        time_cell = tds[2].get_text(strip=True)

        # Basic sanity checks
        if not url_cell or url_cell.lower() == "url":
            continue

        rows.append(PhishRow(url=url_cell, brand=brand_cell, attack_time=time_cell))

    return rows


def ensure_dataframe(path: str) -> pd.DataFrame:
    """Load existing CSV or create an empty DataFrame with the expected columns."""
    cols = ["url", "brand", "attack_time", "first_seen_at_utc"]
    try:
        df = pd.read_csv(path)
        # Ensure expected columns exist
        for c in cols:
            if c not in df.columns:
                df[c] = None
        return df[cols]
    except FileNotFoundError:
        return pd.DataFrame(columns=cols)


def merge_dedup(existing: pd.DataFrame, new_rows: List[PhishRow], seen_ts_iso: str) -> Tuple[pd.DataFrame, int]:
    """Merge new rows into existing DataFrame with de-duplication.
    De-duplicate by (url, attack_time). Returns (df, added_count).
    """
    if not new_rows:
        return existing, 0

    new_df = pd.DataFrame([
        {"url": r.url, "brand": r.brand, "attack_time": r.attack_time, "first_seen_at_utc": seen_ts_iso}
        for r in new_rows
    ])

    # Normalize whitespace
    for col in ["url", "brand", "attack_time"]:
        new_df[col] = new_df[col].astype(str).str.strip()

    # Concatenate and drop duplicates by key
    combined = pd.concat([existing, new_df], ignore_index=True)
    before = len(combined)
    combined = combined.drop_duplicates(subset=["url", "attack_time"], keep="first")
    after = len(combined)
    added = after - len(existing)
    return combined, added


def summarize(df: pd.DataFrame, start_iso: str, end_iso: str) -> dict:
    """Compute the required summary statistics."""
    # Unique URLs in period: we consider the subset first_seen_at_utc in [start,end]
    if df.empty:
        unique_count = 0
        top3 = []
    else:
        period_mask = (df["first_seen_at_utc"] >= start_iso) & (df["first_seen_at_utc"] <= end_iso)
        period_df = df.loc[period_mask].copy()
        unique_count = period_df["url"].nunique()
        top3 = (period_df.assign(brand=period_df["brand"].fillna("").astype(str).str.strip())
                .groupby("brand", dropna=False)["url"]
                .nunique()
                .sort_values(ascending=False)
                .head(3)
                .reset_index()
                .values.tolist())

    return {
        "start_time": start_iso,
        "end_time": end_iso,
        "unique_urls": int(unique_count),
        "top3_brands": [(str(b if b else "Unknown"), int(c)) for b, c in top3],
    }


def main():
    parser = argparse.ArgumentParser(description="Parse OpenPhish homepage table periodically.")
    parser.add_argument("--interval", type=int, default=300, help="Polling interval in seconds (default: 300 = 5 minutes)")
    parser.add_argument("--duration", type=int, default=3600, help="Total run duration in seconds (default: 3600 = 1 hour)")
    parser.add_argument("--out", type=str, default="openphish_data.csv", help="Output CSV path")
    args = parser.parse_args()

    session = requests.Session()

    df = ensure_dataframe(args.out)

    start_ts = datetime.now(timezone.utc)
    start_iso = start_ts.strftime("%Y-%m-%d %H:%M:%S")

    remaining = args.duration
    iteration = 0

    print(f"[INFO] Start: {start_iso} UTC | interval={args.interval}s duration={args.duration}s -> {args.duration//args.interval} polls")

    try:
        while remaining >= 0:
            iteration += 1
            poll_ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            rows = fetch_rows(session)
            df, added = merge_dedup(df, rows, poll_ts)
            df.to_csv(args.out, index=False)

            print(f"[INFO] Poll #{iteration} at {poll_ts} UTC: fetched={len(rows)} added={added} total={len(df)}")
            if remaining == 0:
                break
            sleep_time = min(args.interval, remaining)
            time.sleep(sleep_time)
            remaining -= sleep_time
    except KeyboardInterrupt:
        print("[INFO] Interrupted by user. Finishing...")
    finally:
        end_ts = datetime.now(timezone.utc)
        end_iso = end_ts.strftime("%Y-%m-%d %H:%M:%S")
        summary = summarize(df, start_iso, end_iso)

        # Print summary in required format
        print("\n=== SUMMARY ===")
        print(f"Время начала парсинга: {summary['start_time']} UTC")
        print(f"Время окончания парсинга: {summary['end_time']} UTC")
        print(f"Количество уникальных URL сайтов за период: {summary['unique_urls']}")
        print("Топ 3 наиболее часто атакуемых брендов:")
        if summary['top3_brands']:
            for brand, count in summary['top3_brands']:
                print(f"- {brand} – {count}")
        else:
            print("- (нет данных за период)")
        print(f"CSV: {args.out}")


if __name__ == "__main__":
    main()
