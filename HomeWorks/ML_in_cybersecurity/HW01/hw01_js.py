#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HW01 — OpenPhish parser with JS-rendering fallback (hw01_js.py)
"""

import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Tuple, Dict, Any

import requests
from bs4 import BeautifulSoup
import pandas as pd

try:
    from requests_html import HTMLSession  # type: ignore
except Exception:
    HTMLSession = None


@dataclass
class PhishRow:
    url: str
    brand: str
    attack_time: str


def _parse_table(html_text: str) -> List[PhishRow]:
    soup = BeautifulSoup(html_text, "html.parser")
    table = soup.find("table") or soup.select_one("table.table, table.data-table, table#data, table#main-table")
    if table is None:
        return []
    rows: List[PhishRow] = []
    for tr in table.find_all("tr"):
        cells = tr.find_all(["td", "th"])
        if len(cells) < 3:
            continue
        url_cell = cells[0].get_text(strip=True)
        brand_cell = cells[1].get_text(strip=True)
        time_cell = cells[2].get_text(strip=True)
        if not url_cell or url_cell.lower() == "url":
            continue
        rows.append(PhishRow(url=url_cell, brand=brand_cell, attack_time=time_cell))
    return rows


def fetch_rows(session: requests.Session,
               use_js: bool = False,
               js_timeout: int = 20,
               js_sleep: float = 1.5,
               js_tries: int = 1) -> List[PhishRow]:
    url = "https://openphish.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = session.get(url, timeout=20, headers=headers)
        resp.raise_for_status()
        rows = _parse_table(resp.text)
        if rows or not use_js:
            return rows
    except Exception as e:
        print(f"[WARN] HTTP error: {e}", file=sys.stderr)
        if not use_js:
            return []

    if HTMLSession is None:
        print("[WARN] requests_html не установлен.", file=sys.stderr)
        return []

    try:
        html_sess = HTMLSession()
        r = html_sess.get(url, headers=headers, timeout=20)
        rows: List[PhishRow] = []
        for attempt in range(1, js_tries + 1):
            try:
                r.html.render(timeout=js_timeout, sleep=js_sleep)
                rows = _parse_table(r.html.html or "")
                if rows:
                    break
            except Exception as re:
                print(f"[WARN] render attempt {attempt}/{js_tries} failed: {re}", file=sys.stderr)
                time.sleep(1)
        return rows
    except Exception as e:
        print(f"[WARN] JS session error: {e}", file=sys.stderr)
        return []


def ensure_dataframe(path: str) -> pd.DataFrame:
    cols = ["url", "brand", "attack_time", "first_seen_at_utc"]
    try:
        df = pd.read_csv(path)
        for c in cols:
            if c not in df.columns:
                df[c] = None
        return df[cols]
    except FileNotFoundError:
        return pd.DataFrame(columns=cols)


def merge_dedup(existing: pd.DataFrame, new_rows: List[PhishRow], seen_ts_iso: str) -> Tuple[pd.DataFrame, int]:
    if not new_rows:
        return existing, 0
    new_df = pd.DataFrame([
        {"url": r.url, "brand": r.brand, "attack_time": r.attack_time, "first_seen_at_utc": seen_ts_iso}
        for r in new_rows
    ])
    for col in ["url", "brand", "attack_time"]:
        new_df[col] = new_df[col].astype(str).str.strip()
    combined = pd.concat([existing, new_df], ignore_index=True)
    combined = combined.drop_duplicates(subset=["url", "attack_time"], keep="first")
    added = len(combined) - len(existing)
    return combined, added


def summarize(df: pd.DataFrame, start_iso: str, end_iso: str) -> Dict[str, Any]:
    if df.empty:
        return {"start_time": start_iso, "end_time": end_iso, "unique_urls": 0, "top3_brands": []}
    df = df.copy()
    df["first_seen_at_utc"] = df["first_seen_at_utc"].astype(str)
    mask = (df["first_seen_at_utc"] >= start_iso) & (df["first_seen_at_utc"] <= end_iso)
    period = df.loc[mask]
    unique_urls = int(period["url"].nunique()) if not period.empty else 0
    if period.empty:
        top3 = []
    else:
        counts = (period.assign(brand=period["brand"].fillna("").astype(str).str.strip())
                        .groupby("brand", dropna=False)["url"]
                        .nunique()
                        .sort_values(ascending=False))
        top3 = [(b if b else "Unknown", int(c)) for b, c in counts.head(3).items()]
    return {"start_time": start_iso, "end_time": end_iso, "unique_urls": unique_urls, "top3_brands": top3}


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="OpenPhish parser with optional JS rendering")
    parser.add_argument("--interval", type=int, default=300)
    parser.add_argument("--duration", type=int, default=3600)
    parser.add_argument("--out", type=str, default="openphish_data.csv")
    parser.add_argument("--render-js", action="store_true")
    parser.add_argument("--js-timeout", type=int, default=20)
    parser.add_argument("--js-sleep", type=float, default=1.5)
    parser.add_argument("--js-tries", type=int, default=2)
    args = parser.parse_args()

    session: requests.Session = requests.Session()
    df: pd.DataFrame = ensure_dataframe(args.out)

    start_ts = datetime.now(timezone.utc)
    start_iso = start_ts.strftime("%Y-%m-%d %H:%M:%S")

    remaining = args.duration
    iteration = 0
    print(f"[INFO] Start: {start_iso} UTC | interval={args.interval}s duration={args.duration}s")
    print(f"[INFO] JS rendering: {'ON' if args.render_js else 'OFF'}")

    try:
        while remaining >= 0:
            iteration += 1
            poll_ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            rows = fetch_rows(session, use_js=args.render_js,
                              js_timeout=args.js_timeout, js_sleep=args.js_sleep, js_tries=args.js_tries)
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
