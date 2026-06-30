import re, json, sys

DATE = "2026-06-28"
HTML_PATH = f"/home/matt/.openclaw/workspace/stock-reports/{DATE}.html"
OUT_PATH = f"/home/matt/.openclaw/workspace/stock-reports/_tickers_parsed.json"

with open(HTML_PATH) as f:
    html = f.read()

# Try signal-buy and signal-watch rows
all_rows = re.findall(r'<tr class="(signal-buy|signal-watch)">\s*(.*?)\s*</tr>', html, re.DOTALL)
print(f'found {len(all_rows)} rows total (signal-buy + signal-watch)')

report = {}
for cls, row in all_rows:
    tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
    if len(tds) < 13:
        continue
    m = re.search(r'quotes/([A-Z\.\-]+)/overview', tds[0])
    if not m:
        continue
    ticker = m.group(1)
    def clean(s):
        s = re.sub(r'<[^>]+>', '', s)
        s = re.sub(r'\s+', ' ', s)
        return s.strip()
    report[ticker] = {
        'class': cls,
        'why': clean(tds[11]),
        'outlook': clean(tds[12]),
    }

print(f'parsed {len(report)} tickers')
print('sample NVDA:', json.dumps(report.get('NVDA', {}), ensure_ascii=False, indent=2)[:500])
print('tickers:', sorted(report.keys()))

with open(OUT_PATH, 'w') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print(f'saved to {OUT_PATH}')
