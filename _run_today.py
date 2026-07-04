#!/usr/bin/env python3
"""Run daily recommendations for 2026-07-03.
Source HTML fallback: 2026-07-01.html (barchart job didn't generate today's).
"""
import re, json, sys, time, gzip
import urllib.request, urllib.error
from html import unescape as html_unescape
from datetime import datetime, timezone, timedelta
from pathlib import Path

DATE = "2026-07-03"
SOURCE_DATE = "2026-07-01"  # barchart job didn't generate today's HTML
HTML_PATH = f"/home/matt/.openclaw/workspace/stock-reports/{SOURCE_DATE}.html"
OUT_DIR = Path("/home/matt/.openclaw/workspace/stock-reports/recommendations")
OUT_DIR.mkdir(parents=True, exist_ok=True)
TPE_TZ = timezone(timedelta(hours=8))

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
}


def clean(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()


def parse_html(path):
    with open(path) as f:
        html = f.read()
    m = re.search(r'<h2>🎯 進場推薦總表</h2>\s*<table>(.*?)</table>', html, re.DOTALL)
    if not m:
        print('ERROR: cannot find 進場推薦總表 table', file=sys.stderr)
        sys.exit(1)
    table_html = m.group(1)
    rows = re.findall(r'<tr>(.*?)</tr>', table_html, re.DOTALL)
    print(f'found {len(rows)} rows')
    report = {}
    for row in rows:
        tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
        if len(tds) < 9:
            continue
        m2 = re.search(r'quotes/([A-Z\.\-]+)/overview', tds[0])
        if not m2:
            continue
        ticker = m2.group(1)
        report[ticker] = {
            'price': clean(tds[1]),
            'day_pct': clean(tds[2]),
            '52w_range': clean(tds[3]),
            'pe': clean(tds[5]),
            'score': clean(tds[6]),
            'why': clean(tds[7]),
            'outlook': clean(tds[8]),
        }

    # Analysis cards
    analysis_cards = re.findall(
        r'<div class="card analysis-card">\s*<h3>.*?/quotes/([A-Z\.\-]+)/overview.*?</h3>(.*?)\s*</div>\s*(?=<div class="card analysis-card">|<div class="radar-section"|<h2>|$)',
        html, re.DOTALL
    )
    print(f'found {len(analysis_cards)} analysis cards')
    for ticker, body in analysis_cards:
        if ticker not in report:
            continue
        why_match = re.search(r'<strong>為什麼入選：</strong>\s*(.*?)\s*</p>', body, re.DOTALL)
        supply_match = re.search(r'<strong>供需邏輯：</strong>\s*(.*?)\s*</p>', body, re.DOTALL)
        outlook_match = re.search(r'<strong>未來展望：</strong>\s*(.*?)\s*</p>', body, re.DOTALL)
        risk_match = re.search(r'<strong>風險因素：</strong>\s*(.*?)\s*</p>', body, re.DOTALL)
        if why_match:   report[ticker]['why_detail']    = clean(why_match.group(1))
        if supply_match: report[ticker]['supply_logic'] = clean(supply_match.group(1))
        if outlook_match: report[ticker]['outlook_detail'] = clean(outlook_match.group(1))
        if risk_match:   report[ticker]['risk']         = clean(risk_match.group(1))
    return report


def fetch_research_reports(sym):
    url = f'https://finance.yahoo.com/quote/{sym}'
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as r:
            raw = r.read()
            encoding = r.headers.get('Content-Encoding', '')
            page = gzip.decompress(raw).decode('utf-8', errors='ignore') if encoding == 'gzip' else raw.decode('utf-8', errors='ignore')
    except Exception as e:
        print(f'  [research] {sym}: {e}', file=sys.stderr)
        return []
    pattern = re.compile(
        r'\\"id\\":\s*\\"([^"\\]{1,200})\\"[\s\S]{0,5000}?\\"headHtml\\":\s*\\"([^"\\]{1,300})\\"[\s\S]{0,5000}?\\"provider\\":\s*\\"([^"\\]{1,80})\\"[\s\S]{0,5000}?\\"reportDate\\":\s*\\"([^"\\]{1,40})\\"'
    )
    matches = pattern.findall(page)
    seen, reports = set(), []
    for rid, head, prov, rdate in matches:
        if rid in seen:
            continue
        seen.add(rid)
        head_decoded = html_unescape(head).strip()
        prov_decoded = prov.strip()
        rdate_decoded = rdate.strip()
        if len(head_decoded) < 5:
            continue
        url_id = rid.replace(' ', '%20').replace('/', '%2F')
        reports.append({
            'id': rid,
            'title_en': head_decoded,
            'provider': prov_decoded,
            'date': rdate_decoded,
            'url': f'https://finance.yahoo.com/research/reports/{url_id}',
        })
        if len(reports) >= 3:
            break
    return reports


def main():
    print(f'== {DATE} daily recommendations ==')
    print(f'Source HTML: {HTML_PATH}')
    report = parse_html(HTML_PATH)
    print(f'parsed {len(report)} tickers: {sorted(report.keys())}')

    research = {}
    for sym in sorted(report.keys()):
        rep = fetch_research_reports(sym)
        research[sym] = rep
        print(f'  {sym}: {len(rep)} reports')
        time.sleep(0.4)

    with open(f'/home/matt/.openclaw/workspace/stock-reports/_research_{DATE}.json', 'w') as f:
        json.dump(research, f, ensure_ascii=False, indent=2)
    with open(f'/home/matt/.openclaw/workspace/stock-reports/_tickers_{DATE}.json', 'w') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f'\nresearch saved. {sum(len(r) for r in research.values())} total reports')


if __name__ == '__main__':
    main()
