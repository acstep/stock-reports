import urllib.request, gzip, re, time, json, sys

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
}

def fetch_research_reports(sym):
    url = f'https://finance.yahoo.com/quote/{sym}'
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as r:
            raw = r.read()
            encoding = r.headers.get('Content-Encoding', '')
            if encoding == 'gzip':
                html = gzip.decompress(raw).decode('utf-8', errors='ignore')
            else:
                html = raw.decode('utf-8', errors='ignore')
    except Exception as e:
        print(f'  [research] {sym}: {e}', file=sys.stderr)
        return []

    # Multiple patterns because Yahoo changes HTML structure
    patterns = [
        r'<a[^>]+href="(/research/reports/[^"]+)"[^>]+title="([^"]+)"',
        r'<a[^>]+title="([^"]+)"[^>]+href="(/research/reports/[^"]+)"',
        r'href="(/research/reports/[^"]+)"[^>]*>([^<]{15,200})</a>',
    ]
    matches = []
    for p in patterns:
        m = re.findall(p, html)
        if m:
            matches = m
            break

    seen, reports = set(), []
    for match in matches:
        if len(match) == 2:
            if match[0].startswith('/research/'):
                href, title = match[0], match[1]
            else:
                title, href = match[0], match[1]
        else:
            continue
        if href in seen:
            continue
        seen.add(href)
        # Skip non-English / decoded junk
        title = title.strip()
        if len(title) < 10 or len(title) > 300:
            continue
        reports.append({
            'title_en': title,
            'url': f'https://finance.yahoo.com{href}',
        })
        if len(reports) >= 3:
            break
    return reports

# Load tickers
with open('/home/matt/.openclaw/workspace/stock-reports/_tickers_parsed.json') as f:
    parsed = json.load(f)

tickers = sorted(parsed.keys())
print(f'fetching research for {len(tickers)} tickers...')

news_by_ticker = {}
total_reports = 0
for i, sym in enumerate(tickers):
    reports = fetch_research_reports(sym)
    news_by_ticker[sym] = reports
    total_reports += len(reports)
    print(f'  [{i+1:2d}/{len(tickers)}] {sym:6s} -> {len(reports)} report(s)')
    sys.stdout.flush()
    time.sleep(0.3)

print(f'\nTOTAL: {total_reports} reports across {len(tickers)} tickers')
print(f'tickers with reports: {sum(1 for v in news_by_ticker.values() if v)}')
print(f'tickers with 0 reports: {sum(1 for v in news_by_ticker.values() if not v)}')

with open('/home/matt/.openclaw/workspace/stock-reports/_research_raw.json', 'w') as f:
    json.dump(news_by_ticker, f, ensure_ascii=False, indent=2)
print('saved to _research_raw.json')

# Print samples
for sym in tickers[:5]:
    if news_by_ticker[sym]:
        print(f'\n--- {sym} sample ---')
        print(json.dumps(news_by_ticker[sym][0], ensure_ascii=False))
