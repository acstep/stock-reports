import urllib.request, gzip, re, time, json, sys
from html import unescape as html_unescape

DATE = "2026-07-01"
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
                page = gzip.decompress(raw).decode('utf-8', errors='ignore')
            else:
                page = raw.decode('utf-8', errors='ignore')
    except Exception as e:
        print(f'  [research] {sym}: {e}', file=sys.stderr)
        return []

    # The page contains multiple reports as escaped JSON objects.
    # Each: {\"id\":\"...\",\"headHtml\":\"...\",\"provider\":\"...\",\"reportDate\":\"...\", ...}
    # Use a non-overlapping pattern that captures each object's id+headHtml+provider+reportDate.
    report_pattern = re.compile(
        r'\\"id\\":\s*\\"([^"\\]{1,200})\\"[\s\S]{0,5000}?\\"headHtml\\":\s*\\"([^"\\]{1,300})\\"[\s\S]{0,5000}?\\"provider\\":\s*\\"([^"\\]{1,80})\\"[\s\S]{0,5000}?\\"reportDate\\":\s*\\"([^"\\]{1,40})\\"'
    )
    matches = report_pattern.findall(page)

    seen, reports = set(), []
    for rid, head, prov, rdate in matches:
        if rid in seen:
            continue
        seen.add(rid)
        # Decode escaped HTML
        head = html_unescape(head).strip()
        prov = prov.strip()
        rdate = rdate.strip()
        if len(head) < 5:
            continue
        url_id = rid.replace(' ', '%20').replace('/', '%2F')
        reports.append({
            'title_en': head,
            'provider': prov,
            'date': rdate,
            'url': f'https://finance.yahoo.com/research/reports/{url_id}',
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
    time.sleep(0.4)

print(f'\nTOTAL: {total_reports} reports across {len(tickers)} tickers')
print(f'tickers with reports: {sum(1 for v in news_by_ticker.values() if v)}')
print(f'tickers with 0 reports: {sum(1 for v in news_by_ticker.values() if not v)}')

with open('/home/matt/.openclaw/workspace/stock-reports/_research_raw.json', 'w') as f:
    json.dump(news_by_ticker, f, ensure_ascii=False, indent=2)
print('saved to _research_raw.json')

# Print samples
for sym in tickers:
    if news_by_ticker[sym]:
        print(f'\n--- {sym} sample ---')
        for r in news_by_ticker[sym]:
            print(f"  {r['title_en'][:120]} ({r['provider']})")
