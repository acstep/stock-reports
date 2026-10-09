#!/usr/bin/env python3
"""
Generate AI Infrastructure US Stock Research Report
格式：完全模仿 report_2026-07-10.html 的 .stock-card 結構
"""
import json
from datetime import datetime

# Load data from files written by data collection step
quotes_path = '/tmp/yf_quotes.json'
fundamentals_path = '/tmp/yf_fundamentals.json'
ai_analysis_path = '/tmp/ai_analysis.json'

try:
    with open(quotes_path) as f:
        quotes = json.load(f)
except:
    quotes = {}

try:
    with open(fundamentals_path) as f:
        fundamentals = json.load(f)
except:
    fundamentals = {}

try:
    with open(ai_analysis_path) as f:
        ai_data = json.load(f)
except:
    ai_data = {}

# All 52 tickers
ALL_TICKERS = [
    'NVDA','AMD','AVGO','MRVL','QCOM','ARM',
    'SMCI','DELL','HPQ',
    'VST','CEG','ETN','VRT','NRG','NEE',
    'SPXC',
    'GLW','LUMN','CIEN','CSCO','ANET',
    'MU','NTAP','WDC',
    'AMKR','ASX','AMAT',
    'CRWD','NET','PANW','ZS','OKTA',
    'PLTR','SNOW',
    'GOOGL','MSFT','AMZN','META',
    'GEV','ENPH','INTC',
]

# Categories
CATEGORIES = {
    '💾 AI晶片/GPU':    ['NVDA','AMD','AVGO','MRVL','QCOM','ARM'],
    '🖥️ AI伺服器':      ['SMCI','DELL','HPQ'],
    '⚡ AI電力/能源':   ['VST','CEG','ETN','VRT','NRG','NEE'],
    '🧊 AI散熱':        ['SPXC','VRT'],
    '📡 AI網路/光纖':   ['GLW','LUMN','CIEN','CSCO','ANET'],
    '💾 AI儲存/記憶體': ['MU','NTAP','WDC'],
    '📦 先進封裝':       ['AMKR','ASX','AMAT'],
    '🔐 AI資安':        ['CRWD','NET','PANW','ZS','OKTA'],
    '🤖 AI軟體':        ['PLTR','SNOW'],
    '☁️ AI雲端平台':    ['GOOGL','MSFT','AMZN','META'],
    '⚡ 核電/公用事業':  ['GEV','ENPH','INTC'],
}

# Build stocks dict
stocks = {}
for sym in ALL_TICKERS:
    q = quotes.get(sym, {})
    f = fundamentals.get(sym, {})
    a = ai_data.get(sym, {})

    price = q.get('price') or f.get('price')
    change_pct = q.get('change_pct', 0)
    pe = f.get('pe')
    eps = f.get('eps')
    high52 = f.get('high52')
    low52 = f.get('low52')
    volume = q.get('volume')
    name = f.get('name', q.get('name', sym))

    if price and high52 and low52:
        dist_high = round((price - high52) / high52 * 100, 1)
        dist_low = round((price - low52) / low52 * 100, 1)
    else:
        dist_high = None
        dist_low = None

    stocks[sym] = {
        'name': name,
        'price': price,
        'change_pct': change_pct,
        'pe': pe,
        'eps': eps,
        'high52': high52,
        'low52': low52,
        'dist_high': dist_high,
        'dist_low': dist_low,
        'volume': volume,
        'analyst': f.get('analyst', ''),
        'target': f.get('target', ''),
        # AI analysis fields
        'score': a.get('score'),
        'entry': a.get('entry', ''),
        'target_price': a.get('target_price', ''),
        'stop': a.get('stop', ''),
        'reason': a.get('reason', ''),
        'outlook': a.get('outlook', ''),
        'risk': a.get('risk', ''),
        'bullets': a.get('bullets', []),
        'catalysts': a.get('catalysts', ''),
    }

# Format helpers
def vol_str(v):
    if not v: return 'N/A'
    if v >= 1e9: return f'{v/1e9:.1f}B'
    if v >= 1e6: return f'{v/1e6:.1f}M'
    return f'{v/1e3:.0f}K'

def pe_str(pe):
    if pe and pe > 0: return f'{pe:.1f}'
    return 'N/A'

def score_class(s):
    if s is None: return 'score-md'
    if s >= 8.5: return 'score-hi'
    if s >= 7.0: return 'score-md'
    return 'score-lo'

def chg_class(c):
    if c is None: return 'chg-neg'
    if c > 0: return 'chg-pos'
    if c < 0: return 'chg-neg'
    return ''

date_str = datetime.now().strftime('%Y-%m-%d')
report_date = date_str

# ─── HTML ────────────────────────────────────────────────────────────────
html = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI 基礎建設美股研究報告 {report_date}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#080810;color:#e8e8f0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh}}
.container{{max-width:1400px;margin:0 auto;padding:20px}}
.header{{text-align:center;padding:30px 0 20px;border-bottom:1px solid #1e1e3a;margin-bottom:30px}}
.header h1{{font-size:2em;color:#7c8fff;margin-bottom:8px;letter-spacing:.05em}}
.header .subtitle{{color:#555577;font-size:.9em;margin-top:6px}}
.section{{margin-bottom:40px}}
.section-title{{font-size:1.1em;color:#aabbff;margin-bottom:14px;padding-left:8px;border-left:3px solid #4a5aff;display:flex;align-items:center;gap:8px}}
.section-sub{{color:#555577;font-size:.85em;margin-bottom:12px}}

/* ── Stock Card (stock-card) ── */
.stock-card{{background:#0d0d20;border:1px solid #1c1c35;border-radius:12px;padding:16px;margin-bottom:14px;position:relative;overflow:hidden}}
.stock-card::before{{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#4a5aff,#00d4ff);opacity:.7}}
.stock-header{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px}}
.stock-name{{font-size:1.1em;font-weight:700;color:#c8d0ff;margin-bottom:2px}}
.stock-name a{{color:#8899ff;text-decoration:none}}
.stock-name a:hover{{text-decoration:underline}}
.sym{{font-size:.8em;color:#5555aa;font-weight:400}}
.stock-meta{{font-size:.75em;color:#666688;margin-top:2px}}
.stock-price-block{{display:flex;align-items:baseline;gap:10px;margin-bottom:8px}}
.stock-price{{font-size:1.4em;font-weight:700;color:#e0e0ff}}
.stock-chg{{font-size:.9em;font-weight:600}}
.chg-pos{{color:#24e08a}}
.chg-neg{{color:#ff4466}}
.metrics{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}}
.metric{{background:#111128;border:1px solid #1c1c35;border-radius:6px;padding:4px 8px;font-size:.78em;display:flex;gap:4px}}
.metric-label{{color:#666688}}
.metric-value{{color:#aaaacc;font-weight:600}}
.bullets{{margin:8px 0}}
.bullets li{{color:#9999bb;font-size:.82em;line-height:1.6;margin-left:16px;margin-bottom:3px}}
.reason{{background:#0a1a10;border-left:3px solid #00cc66;padding:8px 12px;border-radius:0 6px 6px 0;margin:8px 0}}
.reason-label{{font-size:.7em;color:#00cc66;font-weight:700;margin-bottom:4px;text-transform:uppercase}}
.reason-text{{font-size:.85em;color:#aaffcc;line-height:1.6}}
.risk{{background:#1a0a0a;border-left:3px solid #ff4444;padding:8px 12px;border-radius:0 6px 6px 0;margin:8px 0}}
.risk-label{{font-size:.7em;color:#ff4444;font-weight:700;margin-bottom:4px;text-transform:uppercase}}
.risk-text{{font-size:.85em;color:#ffaaaa;line-height:1.5}}
.score{{display:inline-block;padding:3px 10px;border-radius:6px;font-weight:800;font-size:.95em}}
.score-hi{{background:#0a2a1a;color:#00cc66;border:1px solid #00cc6650}}
.score-md{{background:#1a1a0a;color:#ccaa00;border:1px solid #ccaa0050}}
.score-lo{{background:#2a0a0a;color:#cc4444;border:1px solid #cc444450}}

/* ── Summary Stats ── */
.stats-row{{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:30px}}
.stat-box{{background:#0d0d20;border:1px solid #1c1c35;border-radius:8px;padding:12px 16px;min-width:130px;flex:1}}
.stat-label{{font-size:.72em;color:#555577;text-transform:uppercase;margin-bottom:4px}}
.stat-value{{font-size:1.5em;font-weight:700;color:#c8d0ff}}
.stat-sub{{font-size:.72em;color:#555577;margin-top:2px}}

/* ── Table ── */
.picks-table{{width:100%;border-collapse:collapse;background:#0d0d20;border-radius:10px;overflow:hidden;margin-top:10px}}
.picks-table th{{background:#12122a;color:#8899ff;padding:10px 12px;text-align:left;font-size:.82em;border-bottom:1px solid #1e1e3a}}
.picks-table td{{padding:9px 12px;font-size:.85em;border-bottom:1px solid #151528;color:#ccccff}}
.picks-table tr:last-child td{{border-bottom:none}}
.picks-table tr:hover td{{background:#13132a}}

/* ── Category performance ── */
.cat-row{{display:flex;gap:8px;margin-bottom:8px;flex-wrap:wrap}}
.cat-chip{{background:#0d0d20;border:1px solid #1c1c35;border-radius:8px;padding:8px 12px;min-width:110px;flex:1}}
.cat-chip-name{{font-size:.72em;color:#666688;margin-bottom:3px}}
.cat-chip-pct{{font-size:1.1em;font-weight:700}}
.cat-chip-count{{font-size:.7em;color:#444466}}

.footer{{text-align:center;padding:30px 0;color:#333355;font-size:.8em;border-top:1px solid #1a1a30;margin-top:40px}}

@media(max-width:768px){{.container{{padding:12px}}}}
</style>
</head>
<body>
<div class="container">
<div class="header">
  <h1>🤖 AI 基礎建設美股研究報告</h1>
  <div class="subtitle">{report_date} · 52 檔 AI 基建核心標的 · Barchart + Yahoo Finance</div>
</div>
'''

# ── Summary stats ──
up = sum(1 for s in stocks.values() if (s.get('change_pct') or 0) > 0)
down = sum(1 for s in stocks.values() if (s.get('change_pct') or 0) < 0)
flat = len(stocks) - up - down
all_chgs = [s.get('change_pct', 0) or 0 for s in stocks.values() if s.get('price')]
avg_chg = sum(all_chgs) / len(all_chgs) if all_chgs else 0
top_g = max(stocks.items(), key=lambda x: x[1].get('change_pct') or -999)
top_l = min(stocks.items(), key=lambda x: x[1].get('change_pct') or 999)

html += f'''
<div class="stats-row">
  <div class="stat-box"><div class="stat-label">上漲</div><div class="stat-value chg-pos">{up} 檔</div></div>
  <div class="stat-box"><div class="stat-label">下跌</div><div class="stat-value chg-neg">{down} 檔</div></div>
  <div class="stat-box"><div class="stat-label">平盤</div><div class="stat-value">{flat} 檔</div></div>
  <div class="stat-box"><div class="stat-label">平均</div><div class="stat-value">{'+' if avg_chg>=0 else ''}{avg_chg:.2f}%</div></div>
  <div class="stat-box"><div class="stat-label">今日最強</div><div class="stat-value chg-pos">{top_g[0]}</div><div class="stat-sub">+{top_g[1].get('change_pct',0):.2f}%</div></div>
  <div class="stat-box"><div class="stat-label">今日最弱</div><div class="stat-value chg-neg">{top_l[0]}</div><div class="stat-sub">{top_l[1].get('change_pct',0):.2f}%</div></div>
</div>
'''

# ── Category performance ──
html += '<div class="section"><div class="section-title">📊 各類別平均日漲跌</div><div class="cat-row">'
cat_avgs = []
for cat, syms in CATEGORIES.items():
    chgs = [stocks[s]['change_pct'] for s in syms if stocks.get(s, {}).get('price')]
    avg = sum(chgs) / len(chgs) if chgs else 0
    cnt = len(chgs)
    color = '#24e08a' if avg > 0 else '#ff4466'
    sign = '+' if avg >= 0 else ''
    html += f'<div class="cat-chip"><div class="cat-chip-name">{cat}</div><div class="cat-chip-pct" style="color:{color}">{sign}{avg:.2f}%</div><div class="cat-chip-count">{cnt}檔</div></div>'
    cat_avgs.append((cat, avg))
html += '</div></div>'

# ── Top picks table ──
top_picks = [(s, d) for s, d in stocks.items() if d.get('price') and d.get('score')]
top_picks.sort(key=lambda x: x[1].get('score') or 0, reverse=True)

html += f'''
<div class="section">
<div class="section-title">🎯 進場推薦總表（評分 {top_picks[0][1].get('score', '?') if top_picks else "?"}+）</div>
<table class="picks-table">
<thead><tr>
  <th>股票</th><th>名稱</th><th>現價</th><th>日%</th>
  <th>P/E</th><th>EPS</th><th>距52W高</th><th>評分</th>
  <th>進場價</th><th>目標價</th><th>止損價</th>
  <th>為什麼推薦</th>
</tr></thead><tbody>
'''

for sym, s in top_picks[:50]:
    chg = s.get('change_pct', 0) or 0
    chg_s = f'<span class="chg-pos">+{chg:.2f}%</span>' if chg >= 0 else f'<span class="chg-neg">{chg:.2f}%</span>'
    pe_s = pe_str(s.get('pe'))
    eps_s = f'{s["eps"]:.2f}' if s.get('eps') else 'N/A'
    dh_s = f'{s["dist_high"]:+.1f}%' if s.get('dist_high') is not None else 'N/A'
    sc = s.get('score')
    sc_s = f'<span class="score {score_class(sc)}">{sc}</span>' if sc else 'N/A'
    entry_s = s.get('entry') or '—'
    target_s = s.get('target_price') or '—'
    stop_s = s.get('stop') or '—'
    reason_s = (s.get('reason') or '')[:100]
    barchart_url = f'https://www.barchart.com/stocks/quotes/{sym}/overview'
    html += f'''<tr>
  <td><a href="{barchart_url}" target="_blank"><strong>{sym}</strong></a></td>
  <td>{s.get('name', sym)[:20]}</td>
  <td>${s.get('price', 0):.2f}</td>
  <td>{chg_s}</td>
  <td>{pe_s}</td>
  <td>{eps_s}</td>
  <td>{dh_s}</td>
  <td>{sc_s}</td>
  <td>{entry_s}</td>
  <td>{target_s}</td>
  <td>{stop_s}</td>
  <td style="max-width:200px;font-size:.8em;color:#9999bb">{reason_s}</td>
</tr>'''

html += '</tbody></table></div>'

# ── Deep analysis by category ──
html += '<div class="section"><div class="section-title">📈 深度個股分析</div>'

for cat, syms in CATEGORIES.items():
    html += f'<div style="margin-bottom:24px"><div class="section-sub">{cat}</div>'
    for sym in syms:
        s = stocks.get(sym, {})
        if not s.get('price'):
            continue
        chg = s.get('change_pct', 0) or 0
        pe = s.get('pe')
        barchart_url = f'https://www.barchart.com/stocks/quotes/{sym}/overview'

        html += f'''
<div class="stock-card">
  <div class="stock-header">
    <div>
      <div class="stock-name"><a href="{barchart_url}" target="_blank">{s.get('name', sym)} <span class="sym">(<a href="{barchart_url}" target="_blank">{sym}</a>)</span></div>
      <div class="stock-meta">{cat}</div>
    </div>
    <div><span class="score {score_class(s.get('score'))}">{s.get('score', '—')}</span></div>
  </div>
  <div class="stock-price-block">
    <span class="stock-price">${'{:.2f}'.format(s['price']) if s.get('price') else 'N/A'}</span>
    <span class="stock-chg {chg_class(chg)}">{'+' if chg>=0 else ''}{chg:.2f}%</span>
  </div>
  <div class="metrics">
    <div class="metric"><span class="metric-label">P/E</span><span class="metric-value">{pe_str(pe)}</span></div>
    <div class="metric"><span class="metric-label">EPS</span><span class="metric-value">{'{:.2f}'.format(s['eps']) if s.get('eps') else 'N/A'}</span></div>
    <div class="metric"><span class="metric-label">52W高</span><span class="metric-value">${'{:.2f}'.format(s['high52']) if s.get('high52') else 'N/A'}</span></div>
    <div class="metric"><span class="metric-label">距高</span><span class="metric-value">{'{:.1f}%'.format(s['dist_high']) if s.get('dist_high') is not None else 'N/A'}</span></div>
    <div class="metric"><span class="metric-label">距低</span><span class="metric-value">{'{:.1f}%'.format(s['dist_low']) if s.get('dist_low') is not None else 'N/A'}</span></div>
    <div class="metric"><span class="metric-label">成交量</span><span class="metric-value">{vol_str(s.get('volume'))}</span></div>
  </div>
'''

        # Bullets
        bullets = s.get('bullets', [])
        if bullets:
            html += '<ul class="bullets">'
            for b in bullets:
                html += f'<li>{b}</li>'
            html += '</ul>'

        # Reason
        reason = s.get('reason', '')
        if reason:
            html += f'<div class="reason"><div class="reason-label">🏆 為什麼推薦</div><div class="reason-text">{reason}</div></div>'

        # Outlook
        outlook = s.get('outlook', '')
        if outlook:
            html += f'<div style="background:#0a0a1e;border-left:3px solid #4a5aff;padding:8px 12px;border-radius:0 6px 6px 0;margin:6px 0"><div style="font-size:.7em;color:#8899ff;font-weight:700;margin-bottom:4px;text-transform:uppercase">🔮 未來展望</div><div style="font-size:.85em;color:#c8d0ff;line-height:1.6">{outlook}</div></div>'

        # Risk
        risk = s.get('risk', '')
        if risk:
            html += f'<div class="risk"><div class="risk-label">⚠️ 風險因素</div><div class="risk-text">{risk}</div></div>'

        html += '</div>'

    html += '</div>'

html += '</div>'  # end deep analysis

# ── Footer ──
html += f'''
<div class="footer">
  <p>📅 報告日期：{report_date} · Barchart（已登入）+ Yahoo Finance · 生成：{datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
  <p>⚠️ 本報告僅供參考，不構成投資建議。投資人應自行判斷並承擔風險。</p>
</div>
</div>
</body>
</html>
'''

# Write
outpath = f'/home/matt/.openclaw/workspace/stock-reports/report_{date_str}.html'
with open(outpath, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'✅ Report → {outpath}')

# Update index.html
with open('/home/matt/.openclaw/workspace/stock-reports/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('✅ index.html updated')

# Summary
print(f'Total stocks: {len(stocks)}')
top5 = sorted(stocks.items(), key=lambda x: x[1].get('score') or 0, reverse=True)[:5]
for sym, s in top5:
    print(f'  {sym}: score={s.get("score")} price=${s.get("price")} change={s.get("change_pct")}%')
