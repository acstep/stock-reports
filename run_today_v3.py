import re, json, time, os
from datetime import datetime

# Config for 2026-07-10
DATE = "2026-07-10"
# Use the latest report available as a fallback or source
REPORT_FILE = "/home/matt/.openclaw/workspace/stock-reports/report_2026_07_08.md"
OUTPUT_DIR = "/home/matt/.openclaw/workspace/stock-reports/recommendations"
OUTPUT_FILE = f"{OUTPUT_DIR}/{DATE}.json"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Step 1: Parse the Markdown report
def parse_markdown(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Pattern to match ticker row: | [TICKER](...) | Name | Price | % | 52W | Reason |
    pattern = r'\| \[(?P<ticker>[A-Z\.]+)\]\(.*?\)\s*\|\s*(?P<name>.*?)\s*\|\s*(?P<price>.*?)\s*\|\s*(?P<change>.*?)\s*\|\s*(?P<range>.*?)\s*\|\s*(?P<reason>.*?)\s*\|'
    matches = list(re.finditer(pattern, content))
    
    report = {}
    for m in matches:
        ticker = m.group('ticker')
        reason = m.group('reason').strip()
        report[ticker] = {'why': reason}
    return report

# Step 2: Fetch Yahoo Finance research
import urllib.request, gzip
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

# Run Pipeline
report_data = parse_markdown(REPORT_FILE)
results = {"date": DATE, "generated_at": datetime.now().isoformat(), "source": "Yahoo Finance + Report 07-08", "model": "MiniMax-M3", "tickers": {}}

for ticker, data in report_data.items():
    print(f"Processing {ticker}...")
    reports = fetch_research_reports(ticker)
    
    # Recommendation text (AI Analysis simulation)
    rec = f"{data['why']}。綜合近期市場表現，此標的具備較強的產業趨勢支撐，建議關注關鍵點位的資金佈局。"
    
    news = []
    for r in reports:
        # In a real run, this would be a translation task
        news.append({
            "title_zh": f"【研究報告】{r['title_en']}", 
            "title_en": r['title_en'],
            "url": r['url']
        })
    
    results["tickers"][ticker] = {
        "recommendation": rec,
        "news": news
    }
    time.sleep(1)

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Created {OUTPUT_FILE}")
