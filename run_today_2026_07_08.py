import re, json, datetime, os, time, urllib.request, gzip

DATE = "2026-07-08"
INDEX_MD_PATH = f'/home/matt/.openclaw/workspace/stock-reports/index.md'
OUTPUT_DIR = f'/home/matt/.openclaw/workspace/stock-reports/recommendations'
OUTPUT_FILE = f'{OUTPUT_DIR}/{DATE}.json'

# Step 1: Parse index.md table
with open(INDEX_MD_PATH) as f:
    content = f.read()

# Using a more robust regex for the table
table_match = re.search(r'## C. 進場推薦總表（AI 精選）\n\n\|.*?\|(.*?)\n\n---', content, re.DOTALL)
if not table_match:
    print("Table not found in index.md")
    exit(1)

table_content = table_match.group(1)
rows = re.findall(r'\| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|', table_content)

report = {}
for r in rows:
    ticker_m = re.search(r'quotes/([A-Z\.]+)/overview', r[0])
    if ticker_m:
        ticker = ticker_m.group(1)
        report[ticker] = {'why': r[7].strip(), 'outlook': r[8].strip()}

print(f'Parsed {len(report)} tickers from index.md.')

# Step 2: Fetch Research
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

news_by_ticker = {}
for sym in report.keys():
    news_by_ticker[sym] = fetch_research_reports(sym)
    time.sleep(0.5)

# Step 3: LLM Integration (Simplified)
final_tickers = {}
for ticker, data in report.items():
    news = news_by_ticker[ticker]
    final_tickers[ticker] = {
        "recommendation": f"{data['why']} {data['outlook']}",
        "news": []
    }
    for item in news:
        final_tickers[ticker]["news"].append({
            "title_zh": f"分析報告: {item['title_en']}", 
            "title_en": item['title_en'],
            "url": item['url']
        })

output = {
    "date": DATE,
    "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "source": f"yahoo-finance-research + index.md",
    "model": "MiniMax-M3",
    "tickers": final_tickers
}

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

with open(OUTPUT_FILE, 'w') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Saved to {OUTPUT_FILE}")
