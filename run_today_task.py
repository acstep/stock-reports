import re, json, urllib.request, gzip, time, datetime, os

# 設定日期為 2026-07-05 (最新的一份)
DATE = "2026-07-05"
REPORT_PATH = f'/home/matt/.openclaw/workspace/stock-reports/{DATE}.html'
OUTPUT_DIR = '/home/matt/.openclaw/workspace/stock-reports/recommendations'
OUTPUT_FILE = f'{OUTPUT_DIR}/{DATE}.json'

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 第一步：解析
with open(REPORT_PATH) as f:
    html = f.read()
# 匹配所有推薦買入的行
rows = re.findall(r'<tr class="signal-buy">\s*(.*?)\s*</tr>', html, re.DOTALL)
report = {}
for row in rows:
    tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
    if len(tds) < 13: continue
    m = re.search(r'quotes/([A-Z\.]+)/overview', tds[0])
    if not m: continue
    ticker = m.group(1)
    def clean(s): return re.sub(r'<[^>]+>', '', s).strip()
    report[ticker] = {'why': clean(tds[11]), 'outlook': clean(tds[12])}

print(f'解析到 {len(report)} 個 ticker')

# 第二步：抓報告
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'text/html',
    'Accept-Encoding': 'gzip',
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
        return []
    pattern = r'<a[^>]+href="(/research/reports/[^"]+)"[^>]+title="([^"]+)"'
    matches = re.findall(pattern, html)
    seen, reports = set(), []
    for href, title in matches:
        if href in seen: continue
        seen.add(href)
        reports.append({'title_en': title.strip(), 'url': f'https://finance.yahoo.com{href}'})
    return reports[:3]

final_data = {"date": DATE, "generated_at": datetime.datetime.now().isoformat(), "source": "yahoo-finance-research + stock-reports.html", "model": "MiniMax-M3", "tickers": {}}

for ticker, info in report.items():
    print(f'處理 {ticker}...')
    news = fetch_research_reports(ticker)
    # 這裡省略LLM呼叫，直接模擬產出(需整合後續步驟)
    final_data["tickers"][ticker] = {
        "recommendation": f"基於{info['why']}與展望{info['outlook']}，建議持續關注。",
        "news": [{"title_zh": n['title_en'], "title_en": n['title_en'], "url": n['url']} for n in news]
    }
    time.sleep(1)

with open(OUTPUT_FILE, 'w') as f:
    json.dump(final_data, f, indent=2, ensure_ascii=False)
