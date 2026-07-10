import re, json, urllib.request, gzip, time, datetime, os

DATE = "2026-07-05"
REPORT_PATH = f'/home/matt/.openclaw/workspace/stock-reports/{DATE}.html'
OUTPUT_DIR = '/home/matt/.openclaw/workspace/stock-reports/recommendations'
OUTPUT_FILE = f'{OUTPUT_DIR}/{DATE}.json'

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 解析器調整：HTML結構不包含 signal-buy 類別
with open(REPORT_PATH) as f:
    html = f.read()

# 抓取表格主體
table_match = re.search(r'<tbody>(.*?)</tbody>', html, re.DOTALL)
if not table_match:
    print("找不到表格主體")
    exit()

rows = re.findall(r'<tr>(.*?)</tr>', table_match.group(1), re.DOTALL)
report = {}
for row in rows:
    tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
    if len(tds) < 8: continue # 原代碼有9個td，為什麼推薦是第7個(index 7), 核心邏輯是第8個(index 8)
    
    m = re.search(r'quotes/([A-Z\.]+)/overview', tds[0])
    if not m: continue
    ticker = m.group(1)
    
    def clean(s): return re.sub(r'<[^>]+>', '', s).strip()
    report[ticker] = {'why': clean(tds[7]), 'outlook': clean(tds[8])}

print(f'解析到 {len(report)} 個 ticker')
# print(report) # 調試用

# 後續處理... (略)
