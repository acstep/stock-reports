#!/usr/bin/env python3
"""
2026-07-10 daily recommendations builder.
Strategy:
  - Today's HTML report (stock-reports/2026-07-10.html) doesn't exist yet
  - Use the 40 tickers from stock-charts 2026-07-10.html gallery as our universe
  - For each ticker, find most recent "為什麼推薦" + "核心邏輯" from past reports
  - Fetch Yahoo Finance research reports (max 3 per ticker)
"""
import re
import json
import os
import gzip
import time
import urllib.request
import urllib.error
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

DATE = "2026-07-10"
STOCK_REPORTS_DIR = "/home/matt/.openclaw/workspace/stock-reports"
STOCK_CHARTS_DIR = "/home/matt/.openclaw/workspace/stock-charts"
OUTPUT_FILE = f"{STOCK_REPORTS_DIR}/recommendations/{DATE}.json"

# === Step 1: Get ticker list from stock-charts gallery ===
def get_ticker_list_from_gallery():
    """Extract tickers from stock-charts 2026-07-10.html gallery."""
    chart_html = f"{STOCK_CHARTS_DIR}/charts/{DATE}.html"
    if not os.path.exists(chart_html):
        # fallback to symbols.json
        with open(f"{STOCK_CHARTS_DIR}/symbols.json") as f:
            return json.load(f)
    with open(chart_html) as f:
        html = f.read()
    tickers = re.findall(r'card-ticker">([A-Z]+)<', html)
    return sorted(set(tickers))

# === Step 2: Parse fallback HTML reports for 為什麼推薦 / 核心邏輯 ===
def parse_report(path):
    """Parse 進場推薦總表 from a report HTML. Returns dict {ticker: {why, outlook, name}}."""
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        html = f.read()
    # Find the 進場推薦總表 section
    m = re.search(r'進場推薦總表(.*?)(?=<div class="section"|<!-- [A-Z]\.|\Z)', html, re.DOTALL)
    if not m:
        return {}
    section = m.group(1)
    # Find the table
    table_m = re.search(r'<table[^>]*>(.*?)</table>', section, re.DOTALL)
    if not table_m:
        return {}
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table_m.group(1), re.DOTALL)
    report = {}
    for row in rows[1:]:  # skip header
        tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
        if len(tds) < 2:
            continue
        # ticker is first td (sometimes wrapped in <a>)
        ticker_m = re.search(r'([A-Z]+(?:\.[A-Z])?)', re.sub(r'<[^>]+>', '', tds[0]).strip())
        if not ticker_m:
            continue
        ticker = ticker_m.group(1)
        def clean(s):
            return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()
        # Try to find "為什麼推薦" and "核心邏輯與展望" columns
        # Heuristic: usually the last 2-3 text-heavy columns
        text_cols = [clean(td) for td in tds if len(clean(td)) > 20]
        if len(text_cols) >= 2:
            why = text_cols[-2]
            outlook = text_cols[-1]
        elif len(text_cols) == 1:
            why = text_cols[0]
            outlook = ""
        else:
            continue
        name = clean(tds[1]) if len(tds) > 1 else ""
        report[ticker] = {
            'why': why,
            'outlook': outlook,
            'name': name,
        }
    return report

# === Step 3: Fetch Yahoo Finance research ===
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip',
    'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8',
    'Accept-Charset': 'utf-8',
}

def fetch_research_reports(sym):
    url = f'https://finance.yahoo.com/quote/{sym}'
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as r:
            raw = r.read()
            encoding = r.headers.get('Content-Encoding', '')
            if encoding == 'gzip':
                html = gzip.decompress(raw).decode('utf-8', errors='ignore')
            else:
                html = raw.decode('utf-8', errors='ignore')
    except Exception as e:
        return []

    # Look for research report links
    # Pattern: <a href="/research/reports/..." title="...">
    pattern = r'<a[^>]+href="(/research/reports/[^"]+)"[^>]+title="([^"]+)"'
    matches = re.findall(pattern, html)

    # Also try variant patterns
    if not matches:
        # Try data-test attribute or different quote styles
        pattern2 = r'href="(/research/reports/[^"]+)"[^>]*title="([^"]+)"'
        matches = re.findall(pattern2, html)
    if not matches:
        pattern3 = r'<a[^>]+title="([^"]+)"[^>]+href="(/research/reports/[^"]+)"'
        m3 = re.findall(pattern3, html)
        matches = [(u, t) for t, u in m3]

    seen, reports = set(), []
    for href, title in matches:
        href = href.replace('&amp;', '&')
        if href in seen:
            continue
        seen.add(href)
        title = title.replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
        reports.append({
            'title_en': title.strip(),
            'url': f'https://finance.yahoo.com{href}',
        })
    return reports[:3]

def fetch_one(sym):
    return sym, fetch_research_reports(sym)

# === Main ===
def main():
    tickers = get_ticker_list_from_gallery()
    print(f"[1] Gallery tickers: {len(tickers)} — {tickers}")

    # Build fallback report: try most recent first
    fallback_files = [
        f"{STOCK_REPORTS_DIR}/2026-07-05.html",
        f"{STOCK_REPORTS_DIR}/2026-07-04.html",
        f"{STOCK_REPORTS_DIR}/2026-07-03.html",
        f"{STOCK_REPORTS_DIR}/2026-07-01.html",
        f"{STOCK_REPORTS_DIR}/report_2026-07-08.md",
    ]

    report = {}
    for f in fallback_files:
        parsed = parse_report(f)
        for t, info in parsed.items():
            if t not in report:
                report[t] = {**info, 'source': os.path.basename(f)}

    # Also include index.html data (3 tickers: NVDA, AMD, MU)
    idx_path = f"{STOCK_REPORTS_DIR}/index.html"
    if os.path.exists(idx_path):
        with open(idx_path) as f:
            html = f.read()
        # Find rows in 今日精選標的 table
        m = re.search(r'今日精選標的(.*?)</table>', html, re.DOTALL)
        if m:
            rows = re.findall(r'<tr>(.*?)</tr>', m.group(1), re.DOTALL)
            for row in rows:
                tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
                if len(tds) < 4:
                    continue
                tk_m = re.search(r'quotes/([A-Z]+)/overview', tds[0])
                if not tk_m:
                    continue
                tk = tk_m.group(1)
                reason = re.sub(r'<[^>]+>', '', tds[3]).strip()
                if tk not in report:
                    report[tk] = {
                        'why': reason,
                        'outlook': '',
                        'name': '',
                        'source': 'index.html',
                    }

    print(f"[2] Fallback report data: {len(report)} tickers")
    for t in tickers[:5]:
        if t in report:
            print(f"     {t}: why={report[t]['why'][:60]}...")

    # === Step 4: Fetch Yahoo Finance research in parallel ===
    print(f"[3] Fetching Yahoo Finance research for {len(tickers)} tickers...")
    news_by_ticker = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(fetch_one, sym): sym for sym in tickers}
        done = 0
        for fut in as_completed(futures):
            sym, reports = fut.result()
            news_by_ticker[sym] = reports
            done += 1
            if done % 10 == 0:
                print(f"     [{done}/{len(tickers)}] fetched {sym} → {len(reports)} reports")

    total_news = sum(len(v) for v in news_by_ticker.values())
    print(f"[4] Total research reports fetched: {total_news}")

    # Save intermediate data for LLM processing
    intermediate = {
        'date': DATE,
        'tickers': tickers,
        'report': report,
        'news_by_ticker': news_by_ticker,
    }
    with open(f"{STOCK_REPORTS_DIR}/_cron_intermediate.json", 'w') as f:
        json.dump(intermediate, f, ensure_ascii=False, indent=2)
    print(f"[5] Saved intermediate to _cron_intermediate.json")

if __name__ == '__main__':
    main()