import urllib.request, gzip, re, time, json
from datetime import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'text/html',
    'Accept-Encoding': 'gzip',
    'Accept-Language': 'en-US,en;q=0.9',
}

def fetch_research_reports(sym):
    url = f'https://finance.yahoo.com/quote/{sym}'
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read()
            encoding = r.headers.get('Content-Encoding', '')
            if encoding == 'gzip':
                html = gzip.decompress(raw).decode('utf-8', errors='ignore')
            else:
                html = raw.decode('utf-8', errors='ignore')
    except Exception as e:
        print(f'  [research] {sym}: {e}')
        return []

    pattern = r'<a[^>]+href="(/research/reports/[^"]+)"[^>]+title="([^"]+)"'
    matches = re.findall(pattern, html)
    seen, reports = set(), []
    for href, title in matches:
        if href in seen: continue
        seen.add(href)
        reports.append({
            'title_en': title.strip(),
            'url': f'https://finance.yahoo.com{href}',
        })
    return reports[:3]

tickers = ["CRWD", "NEE", "PLTR", "SNOW"]
data = {}
for sym in tickers:
    data[sym] = fetch_research_reports(sym)
    time.sleep(0.5)

with open('/home/matt/.openclaw/workspace/stock-reports/_research_2026-07-08.json', 'w') as f:
    json.dump(data, f, indent=2)
print("Research reports fetched.")
