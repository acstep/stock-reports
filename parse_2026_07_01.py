import re, json

DATE = "2026-07-01"
HTML_PATH = f"/home/matt/.openclaw/workspace/stock-reports/{DATE}.html"
OUT_PATH = f"/home/matt/.openclaw/workspace/stock-reports/_tickers_parsed.json"

with open(HTML_PATH) as f:
    html = f.read()

def clean(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

# Parse "進場推薦總表" table - simple structure (no signal-buy class)
# Find the table after the 進場推薦總表 heading
m = re.search(r'<h2>🎯 進場推薦總表</h2>\s*<table>(.*?)</table>', html, re.DOTALL)
if not m:
    print('ERROR: cannot find 進場推薦總表 table')
    raise SystemExit(1)
table_html = m.group(1)

# Extract rows
rows = re.findall(r'<tr>(.*?)</tr>', table_html, re.DOTALL)
print(f'found {len(rows)} rows in 進場推薦總表 table')

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
        'class': 'signal-buy',  # default for this report
        'price': clean(tds[1]),
        'day_pct': clean(tds[2]),
        '52w_range': clean(tds[3]),
        'pct_from_low': clean(tds[4]),
        'pe': clean(tds[5]),
        'score': clean(tds[6]),
        'why': clean(tds[7]),
        'outlook': clean(tds[8]),
    }

print(f'parsed {len(report)} tickers from table')
print('tickers:', sorted(report.keys()))

# Also parse analysis cards for richer "core logic" text
# Each <div class="card analysis-card"> contains: 為什麼入選 / 供需邏輯 / 未來展望 / 風險因素
analysis_cards = re.findall(
    r'<div class="card analysis-card">\s*<h3>.*?/quotes/([A-Z\.\-]+)/overview.*?</h3>(.*?)\s*</div>\s*(?=<div class="card analysis-card">|<div class="radar-section"|<h2>|$)',
    html, re.DOTALL
)
print(f'\nfound {len(analysis_cards)} analysis cards')

for ticker, body in analysis_cards:
    if ticker not in report:
        continue
    why_match = re.search(r'<strong>為什麼入選：</strong>\s*(.*?)\s*</p>', body, re.DOTALL)
    supply_match = re.search(r'<strong>供需邏輯：</strong>\s*(.*?)\s*</p>', body, re.DOTALL)
    outlook_match = re.search(r'<strong>未來展望：</strong>\s*(.*?)\s*</p>', body, re.DOTALL)
    risk_match = re.search(r'<strong>風險因素：</strong>\s*(.*?)\s*</p>', body, re.DOTALL)
    if why_match:
        report[ticker]['why_detail'] = clean(why_match.group(1))
    if supply_match:
        report[ticker]['supply_logic'] = clean(supply_match.group(1))
    if outlook_match:
        report[ticker]['outlook_detail'] = clean(outlook_match.group(1))
    if risk_match:
        report[ticker]['risk'] = clean(risk_match.group(1))

# Combine for LLM input: "why" (推薦理由) + "outlook" (核心邏輯) = main story
# Use the longer analysis card text if available
for tkr, info in report.items():
    if 'supply_logic' in info and 'outlook_detail' in info:
        info['full_story'] = f"{info['why']} | {info['outlook']} | 供需邏輯: {info['supply_logic']} | 未來展望: {info['outlook_detail']} | 風險: {info.get('risk','')}"
    else:
        info['full_story'] = f"{info['why']} | {info['outlook']}"

# Sample
sample = report.get('NVDA', report.get('AMAT', {}))
print(f'\nsample AMAT:')
print(json.dumps(report.get('AMAT', {}), ensure_ascii=False, indent=2)[:800])

with open(OUT_PATH, 'w') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print(f'\nsaved to {OUT_PATH}')
