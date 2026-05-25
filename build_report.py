import json

with open('/tmp/stock_report_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

prices = data['prices']
signals = data['signals']
categories = data['categories']
analysis = data['analysis']
selected = data['selected']

# Sort selected by category
def cat_sort_key(sym):
    cat = categories.get(sym, ('Other', '#888'))[0]
    order = ['AI 晶片', 'AI 伺服器', 'AI 電力', 'AI 散熱', 'AI 光纖', 'AI 網路', 'AI 記憶體', 'AI 儲存', '先進封裝', '半導體設備', 'AI 資安', 'AI 軟體', 'AI 雲端', 'AI 資料中心']
    for i, o in enumerate(order):
        if o in cat:
            return i
    return 99

sorted_syms = sorted(selected, key=cat_sort_key)

# Group by category
from collections import defaultdict
groups = defaultdict(list)
for sym in sorted_syms:
    cat = categories.get(sym, ('Other', '#888'))[0]
    groups[cat].append(sym)

today = '2026年05月25日'

html = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI 基礎建設研究報告 | {today}</title>
<style>
:root {{
  --bg: #080810; --bg2: #0c0c1a; --bg3: #10101f; --bg-card: #0e0e20;
  --border: rgba(255,255,255,0.07); --border-accent: rgba(91,127,255,0.3);
  --text: #e0e4f0; --text-dim: #7880a0; --text-muted: #444660;
  --accent: #5b7fff; --accent-glow: rgba(91,127,255,0.25);
  --green: #24e08a; --green-bg: rgba(36,224,138,0.1);
  --red: #f04040; --red-bg: rgba(240,64,64,0.1);
  --purple: #a855f7; --cyan: #06b6d4; --orange: #f97316; --gold: #ffd700;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
a {{ color: var(--accent); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--text); line-height: 1.7; font-size: 15px; }}
.wrap {{ max-width: 1140px; margin: 0 auto; padding: 28px 24px; }}

.site-header {{ display: flex; justify-content: space-between; align-items: center; padding: 18px 24px; border-bottom: 1px solid var(--border); background: var(--bg2); position: sticky; top: 0; z-index: 100; }}
.site-header .logo {{ font-size: 18px; font-weight: 700; }}
.site-header .logo span {{ color: var(--accent); }}
.site-header .nav-links {{ display: flex; gap: 24px; }}
.site-header .nav-links a {{ color: var(--text-dim); font-size: 13px; font-weight: 500; transition: color 0.2s; }}
.site-header .nav-links a:hover {{ color: var(--accent); text-decoration: none; }}
.update-badge {{ font-size: 11px; color: var(--text-dim); background: var(--bg3); border: 1px solid var(--border); padding: 5px 12px; border-radius: 20px; font-family: monospace; }}

.hero {{ background: linear-gradient(135deg, var(--bg2) 0%, var(--bg3) 60%, #0d0a28 100%); border: 1px solid rgba(91,127,255,0.18); border-radius: 24px; padding: 48px 52px; margin-bottom: 32px; text-align: center; position: relative; overflow: hidden; }}
.hero::before {{ content: ''; position: absolute; top: -50%; left: 50%; transform: translateX(-50%); width: 600px; height: 400px; background: radial-gradient(ellipse, rgba(91,127,255,0.09) 0%, transparent 70%); pointer-events: none; }}
.hero .hero-tag {{ display: inline-block; background: rgba(91,127,255,0.12); border: 1px solid rgba(91,127,255,0.3); color: var(--accent); font-size: 11px; font-weight: 600; padding: 5px 14px; border-radius: 20px; margin-bottom: 16px; letter-spacing: 1px; }}
.hero h1 {{ font-size: 32px; font-weight: 800; margin-bottom: 8px; letter-spacing: -0.5px; position: relative; }}
.hero .subtitle {{ color: var(--text-dim); font-size: 15px; margin-bottom: 28px; }}
.hero .stats-row {{ display: flex; justify-content: center; gap: 48px; flex-wrap: wrap; }}
.hero .stat {{ text-align: center; }}
.hero .stat .val {{ font-size: 22px; font-weight: 700; color: var(--green); }}
.hero .stat .label {{ font-size: 12px; color: var(--text-muted); margin-top: 2px; }}

.section {{ margin-bottom: 32px; }}
.section-header {{ display: flex; align-items: center; gap: 12px; margin-bottom: 18px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }}
.section-header h2 {{ font-size: 17px; font-weight: 700; }}
.section-header .badge {{ font-size: 10px; padding: 3px 9px; border-radius: 10px; background: rgba(91,127,255,0.12); color: var(--accent); font-weight: 600; letter-spacing: 0.5px; }}

.card {{ background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 22px 24px; margin-bottom: 16px; transition: border-color 0.3s, box-shadow 0.3s; }}
.card:hover {{ border-color: var(--border-accent); box-shadow: 0 4px 24px rgba(0,0,0,0.3); }}
.card-row {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }}
.card-row .card {{ margin-bottom: 0; }}

.stock-table {{ width: 100%; border-collapse: collapse; font-size: 13.5px; }}
.stock-table th {{ text-align: left; padding: 10px 14px; color: var(--text-muted); font-weight: 600; font-size: 11px; letter-spacing: 0.5px; border-bottom: 1px solid var(--border); background: var(--bg3); }}
.stock-table th:first-child {{ border-radius: 10px 0 0 0; }}
.stock-table th:last-child {{ border-radius: 0 10px 0 0; }}
.stock-table td {{ padding: 13px 14px; border-bottom: 1px solid rgba(255,255,255,0.04); vertical-align: middle; }}
.stock-table tr:last-child td {{ border-bottom: none; }}
.stock-table tr:hover td {{ background: rgba(255,255,255,0.02); }}
.sym {{ font-weight: 700; font-size: 14px; color: var(--accent); letter-spacing: 0.3px; }}
.sym-name {{ font-size: 11px; color: var(--text-dim); margin-top: 2px; }}
.price {{ font-weight: 700; font-size: 15px; }}
.chg-up {{ color: var(--green); font-weight: 600; font-size: 13px; }}
.chg-dn {{ color: var(--red); font-weight: 600; font-size: 13px; }}
.pill {{ display: inline-block; font-size: 11px; padding: 3px 9px; border-radius: 8px; font-weight: 600; }}
.pill-green {{ background: var(--green-bg); color: var(--green); }}
.pill-red {{ background: var(--red-bg); color: var(--red); }}
.pill-blue {{ background: rgba(91,127,255,0.12); color: var(--accent); }}
.pill-orange {{ background: rgba(249,115,22,0.12); color: var(--orange); }}
.score-bar {{ display: flex; gap: 2px; align-items: center; }}
.score-dot {{ width: 7px; height: 7px; border-radius: 2px; background: var(--text-muted); }}
.score-dot.filled {{ background: var(--green); }}
.tag {{ display: inline-block; font-size: 10px; padding: 2px 7px; border-radius: 6px; background: rgba(168,85,247,0.1); color: var(--purple); font-weight: 500; margin-right: 4px; }}
.tag-electric {{ background: rgba(6,182,212,0.1); color: var(--cyan); }}
.tag-chip {{ background: rgba(249,115,22,0.1); color: var(--orange); }}
.tag-security {{ background: rgba(36,224,138,0.1); color: var(--green); }}

.grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
.grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }}

.deep-card {{ background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 24px; margin-bottom: 20px; }}
.deep-card .stock-header {{ display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 16px; }}
.deep-card .stock-title {{ display: flex; align-items: center; gap: 12px; }}
.deep-card .stock-title h3 {{ font-size: 18px; font-weight: 700; color: var(--accent); }}
.deep-card .stock-title span {{ font-size: 13px; color: var(--text-dim); }}
.deep-card .verdict {{ font-size: 12px; font-weight: 700; padding: 5px 12px; border-radius: 10px; }}
.deep-card .verdict.strong-buy {{ background: var(--green-bg); color: var(--green); }}
.deep-card .verdict.buy {{ background: rgba(91,127,255,0.12); color: var(--accent); }}
.deep-card .verdict.spec-buy {{ background: rgba(249,115,22,0.12); color: var(--orange); }}
.deep-card .verdict.partial {{ background: rgba(168,85,247,0.12); color: var(--purple); }}
.deep-card .metrics {{ display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 16px; }}
.deep-card .metric {{ text-align: center; }}
.deep-card .metric .mval {{ font-size: 18px; font-weight: 700; }}
.deep-card .metric .mlabel {{ font-size: 10px; color: var(--text-muted); margin-top: 2px; }}
.deep-card .signal-badge {{ display: inline-block; font-size: 11px; padding: 4px 10px; border-radius: 8px; background: rgba(6,182,212,0.1); color: var(--cyan); font-weight: 600; margin-bottom: 12px; }}
.deep-card .analysis-block {{ background: var(--bg3); border-radius: 12px; padding: 16px; margin-bottom: 12px; }}
.deep-card .analysis-block h4 {{ font-size: 12px; color: var(--text-dim); font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 8px; }}
.deep-card .analysis-block p {{ font-size: 13.5px; line-height: 1.7; color: var(--text); }}
.deep-card .strategy-row {{ display: flex; gap: 20px; flex-wrap: wrap; }}
.deep-card .strategy-item {{ background: var(--bg3); border-radius: 10px; padding: 10px 14px; text-align: center; min-width: 100px; }}
.deep-card .strategy-item .slabel {{ font-size: 10px; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
.deep-card .strategy-item .sval {{ font-size: 15px; font-weight: 700; margin-top: 4px; }}
.deep-card .strategy-item .sval.green {{ color: var(--green); }}
.deep-card .strategy-item .sval.red {{ color: var(--red); }}

.theme-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 16px; }}
.theme-card {{ background: var(--bg-card); border: 1px solid var(--border); border-radius: 14px; padding: 18px; }}
.theme-card .theme-name {{ font-size: 13px; font-weight: 600; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; }}
.theme-card .theme-stocks {{ display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 10px; }}
.theme-card .mini-chip {{ font-size: 10px; padding: 2px 7px; border-radius: 6px; font-weight: 600; }}
.theme-card .theme-bar {{ height: 4px; border-radius: 2px; background: var(--bg3); margin-top: 10px; }}
.theme-card .theme-bar-fill {{ height: 4px; border-radius: 2px; }}

.supply-block {{ background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 28px; margin-bottom: 20px; }}
.supply-block h3 {{ font-size: 16px; font-weight: 700; margin-bottom: 16px; }}
.supply-block .供需-row {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 14px; }}
.supply-block .供需-card {{ background: var(--bg3); border-radius: 12px; padding: 16px; }}
.supply-block .供需-card h4 {{ font-size: 12px; font-weight: 600; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }}
.supply-block .供需-card p {{ font-size: 13px; color: var(--text); line-height: 1.6; }}

.footer {{ text-align: center; padding: 32px 0; color: var(--text-muted); font-size: 12px; border-top: 1px solid var(--border); margin-top: 40px; }}

@media (max-width: 768px) {{ .grid-2, .grid-3 {{ grid-template-columns: 1fr; }} .hero {{ padding: 32px 24px; }} .hero h1 {{ font-size: 24px; }} .hero .stats-row {{ gap: 24px; }} .site-header .nav-links {{ display: none; }} }}
</style>
</head>
<body>
<div class="site-header">
  <div class="logo">AI 基建 <span>研究報告</span></div>
  <div class="nav-links">
    <a href="#market-radar">市場雷達</a>
    <a href="#recommendations">推薦總表</a>
    <a href="#deep-dive">深度分析</a>
    <a href="#themes">主題板塊</a>
    <a href="#supply">供需分析</a>
  </div>
  <div class="update-badge">{today} 更新</div>
</div>

<div class="wrap">
'''

# Hero stats
gainers = [s for s in selected if prices.get(s, {}).get('chg', 0) > 0]
losers = [s for s in selected if prices.get(s, {}).get('chg', 0) < 0]
top_gainer = max(selected, key=lambda s: prices.get(s, {}).get('chg', -999))
top_gainer_chg = prices[top_gainer]['chg']

html += f'''
<!-- HERO -->
<div class="hero">
  <div class="hero-tag">AI 基礎建設美股研究報告</div>
  <h1>人工智慧基建超級周期</h1>
  <div class="subtitle">{today} | 精選 {len(selected)} 檔 AI 基建核心標的</div>
  <div class="stats-row">
    <div class="stat"><div class="val">{len(selected)}</div><div class="label">精選股票</div></div>
    <div class="stat"><div class="val">{len(gainers)}</div><div class="label">上漲</div></div>
    <div class="stat"><div class="val">{len(losers)}</div><div class="label">下跌/整理</div></div>
    <div class="stat"><div class="val">+{top_gainer} {top_gainer_chg:+.1f}%</div><div class="label">今日最強</div></div>
    <div class="stat"><div class="val">ARM +46.5%</div><div class="label">最大漲幅</div></div>
  </div>
</div>
'''

# MARKET RADAR
html += '''
<!-- MARKET RADAR -->
<div class="section" id="market-radar">
  <div class="section-header">
    <h2>A. 市場情緒雷達</h2>
    <span class="badge">實時監控</span>
  </div>
  <div class="card-row">
'''

radar_items = [
    ('AI 晶片/GPU', ['NVDA', 'AMD', 'AVGO', 'QCOM', 'MRVL', 'INTC', 'ARM', 'TSM'], '💾', '#f97316'),
    ('AI 伺服器/雲端', ['SMCI', 'DELL', 'HPQ', 'ANET'], '🖥️', '#06b6d4'),
    ('AI 電力/能源', ['VST', 'CEG', 'NRG', 'NEE', 'AES', 'PNRG', 'BE'], '⚡', '#24e08a'),
    ('AI 散熱/液冷', ['VRT', 'SPXC'], '🧊', '#06b6d4'),
    ('AI 網路/光纖', ['GLW', 'LUMN', 'CIEN', 'CSCO', 'LSCC'], '📡', '#a855f7'),
    ('AI 儲存/記憶體', ['MU', 'NTAP', 'PSTG', 'WDC', 'ON'], '💾', '#6366f1'),
    ('先進封裝/設備', ['AMKR', 'ASX', 'AMAT', 'LRCX'], '📦', '#6366f1'),
    ('AI 資安/雲端', ['CRWD', 'NET', 'PANW', 'ZS', 'OKta'], '🔐', '#24e08a'),
    ('AI 軟體/資料', ['PLTR', 'SNOW', 'DDOG'], '🤖', '#f97316'),
    ('AI 雲端平台', ['GOOGL', 'MSFT', 'AMZN', 'META'], '☁️', '#5b7fff'),
    ('AI 資料中心REIT', ['DLR', 'EQIX', 'AMT', 'PLD'], '🏢', '#5b7fff'),
]

for cat_name, syms, emoji, color in radar_items:
    gains = [s for s in syms if s in prices and prices[s]['chg'] > 0]
    loss = [s for s in syms if s in prices and prices[s]['chg'] < 0]
    max_chg_sym = max(syms, key=lambda s: prices.get(s, {}).get('chg', -999)) if syms else None
    max_chg = prices[max_chg_sym]['chg'] if max_chg_sym and max_chg_sym in prices else 0
    if max_chg > 0:
        indicator = f'<span style="color:{color}">🟢強勢</span>'
    elif max_chg < -5:
        indicator = f'<span style="color:#f04040">🔴回調</span>'
    else:
        indicator = f'<span style="color:#f97316">🟡震盪</span>'
    syms_html = ' '.join([f'<span class="mini-chip" style="background:{color}20;color:{color}">{s}</span>' for s in syms if s in prices])
    html += f'''
    <div class="card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
        <span style="font-size:20px">{emoji}</span>
        <span style="font-weight:700;font-size:13px">{cat_name}</span>
      </div>
      <div style="margin-bottom:8px">{indicator}</div>
      <div style="display:flex;gap:5px;flex-wrap:wrap;margin-bottom:8px">{syms_html}</div>
      <div style="font-size:11px;color:var(--text-dim)">漲 {len(gains)} / 跌 {len(loss)}</div>
    </div>
'''

html += '''
  </div>
</div>
'''

# RECOMMENDATIONS TABLE
html += '''
<!-- RECOMMENDATIONS TABLE -->
<div class="section" id="recommendations">
  <div class="section-header">
    <h2>B. 進場推薦總表</h2>
    <span class="badge">''' + f'{len(selected)} 檔精選' + '''</span>
  </div>
  <div class="card">
    <table class="stock-table">
      <thead>
        <tr>
          <th>代號</th>
          <th>價格</th>
          <th>漲跌</th>
          <th>52W區間</th>
          <th>距低/高</th>
          <th>評等</th>
          <th>Barchart</th>
        </tr>
      </thead>
      <tbody>
'''

for sym in sorted_syms:
    p = prices.get(sym, {})
    a = analysis.get(sym, {})
    cat, color = categories.get(sym, ('Other', '#888'))
    price = p.get('price', 'N/A')
    chg = p.get('chg', 0)
    high52 = p.get('high52')
    low52 = p.get('low52')
    from_low = p.get('from_low_pct')
    chg_class = 'chg-up' if chg >= 0 else 'chg-dn'
    chg_str = f'+{chg:.2f}%' if chg >= 0 else f'{chg:.2f}%'
    
    # BC signal
    bc = signals.get(sym, {})
    bc_opinion = bc.get('opinion', '-')
    
    verdict = a.get('verdict', '-')
    if verdict == 'STRONG BUY':
        v_class = 'pill-green'
    elif verdict == 'BUY':
        v_class = 'pill-blue'
    elif verdict == 'SPECULATIVE BUY':
        v_class = 'pill-orange'
    elif 'PARTIAL' in verdict:
        v_class = ''
    else:
        v_class = ''
    
    if high52 and low52:
        range_str = f'$...'
    else:
        range_str = '-'
    
    entry = a.get('entry', '-')
    stop = a.get('stop', '-')
    cat_tag = f'<span style="font-size:10px;padding:2px 7px;border-radius:6px;background:{color}15;color:{color};font-weight:500">{cat}</span>'
    
    html += f'''
        <tr>
          <td>
            <div class="sym">{sym}</div>
            <div class="sym-name">{p.get('name', '')}</div>
            {cat_tag}
          </td>
          <td><div class="price">${price}</div></td>
          <td><span class="{chg_class}">{chg_str}</span></td>
          <td style="font-size:12px;color:var(--text-dim)">{'${:.2f}'.format(low52) if low52 else '-'} – ${'{:.2f}'.format(high52) if high52 else '-'}</td>
          <td style="font-size:12px">{'+{:.1f}% from低'.format(from_low) if from_low else '-'}</td>
          <td><span class="pill {v_class}">{verdict}</span></td>
          <td><span style="font-size:12px;color:var(--text-dim)">{bc_opinion}</span></td>
        </tr>
'''

html += '''
      </tbody>
    </table>
  </div>
</div>
'''

# DEEP DIVE
html += '''
<!-- DEEP DIVE -->
<div class="section" id="deep-dive">
  <div class="section-header">
    <h2>C. 深度個股分析</h2>
    <span class="badge">''' + f'{len(selected)} 檔' + '''</span>
  </div>
'''

for sym in sorted_syms:
    p = prices.get(sym, {})
    a = analysis.get(sym, {})
    cat, color = categories.get(sym, ('Other', '#888'))
    price = p.get('price', 'N/A')
    chg = p.get('chg', 0)
    high52 = p.get('high52')
    low52 = p.get('low52')
    from_low = p.get('from_low_pct')
    volume = p.get('volume')
    entry = a.get('entry', '-')
    stop = a.get('stop', '-')
    core = a.get('core', '')
    outlook = a.get('outlook', '')
    signal = a.get('signal', '')
    verdict = a.get('verdict', '-')
    
    if verdict == 'STRONG BUY':
        v_class = 'strong-buy'
    elif verdict == 'BUY':
        v_class = 'buy'
    elif verdict == 'SPECULATIVE BUY':
        v_class = 'spec-buy'
    elif 'PARTIAL' in verdict:
        v_class = 'partial'
    else:
        v_class = ''
    
    chg_class = 'chg-up' if chg >= 0 else 'chg-dn'
    chg_str = f'+{chg:.2f}%' if chg >= 0 else f'{chg:.2f}%'
    
    vol_str = f'{volume/1e6:.1f}M' if volume else '-'
    
    html += f'''
  <div class="deep-card">
    <div class="stock-header">
      <div class="stock-title">
        <h3>{sym}</h3>
        <span>{p.get('name', '')}</span>
        <span style="font-size:12px;padding:2px 8px;border-radius:8px;font-weight:600;background:{color}15;color:{color}">{cat}</span>
      </div>
      <div style="display:flex;align-items:center;gap:10px">
        <span class="verdict {v_class}">{verdict}</span>
        <span class="{chg_class}" style="font-size:16px;font-weight:700">${price} {chg_str}</span>
      </div>
    </div>
    <div class="signal-badge">{signal}</div>
    <div class="metrics">
      <div class="metric"><div class="mval" style="color:var(--green)">${'{:.2f}'.format(price)}</div><div class="mlabel">現價</div></div>
      <div class="metric"><div class="mval">${'{:.2f}'.format(low52) if low52 else '-'}</div><div class="mlabel">52W 低</div></div>
      <div class="metric"><div class="mval">${'{:.2f}'.format(high52) if high52 else '-'}</div><div class="mlabel">52W 高</div></div>
      <div class="metric"><div class="mval">+{from_low if from_low else 0:.1f}%</div><div class="mlabel">from 52W低</div></div>
      <div class="metric"><div class="mval">{vol_str}</div><div class="mlabel">成交量</div></div>
    </div>
    <div class="analysis-block">
      <h4>AI 原生推薦邏輯</h4>
      <p>{core}</p>
    </div>
    <div class="analysis-block">
      <h4>核心邏輯與展望</h4>
      <p>{outlook}</p>
    </div>
    <div class="strategy-row">
      <div class="strategy-item">
        <div class="slabel">進場策略</div>
        <div class="sval green">{entry}</div>
      </div>
      <div class="strategy-item">
        <div class="slabel">止損位</div>
        <div class="sval red">{stop}</div>
      </div>
    </div>
  </div>
'''

html += '''
</div>
'''

# THEMES
html += '''
<!-- THEMES -->
<div class="section" id="themes">
  <div class="section-header">
    <h2>D. 主題板塊評估</h2>
    <span class="badge">6 大 AI 基建主題</span>
  </div>
  <div class="supply-block">
    <h3>AI 基礎建設六大赛道深度評估</h3>
    <div class="供需-row">
'''

theme_blocks = [
    ('💾 AI 晶片/GPU', '#f97316', '⭐⭐⭐⭐⭐', '極短線供需緊張，Blackwell GB200 產能嚴重不足，CoWoS 封裝是核心瓶頸。NVDA 定價權無可撼動，AMD MI300X 性價比殺傷力開始顯現。ARM 架構在雲端資料中心份額快速爬升，2025-2027 是結構性替代x86的起點。Custom ASIC 趨勢讓 Marvell、博通獲得新增長曲線。', ['NVDA', 'AMD', 'AVGO', 'QCOM', 'MRVL', 'INTC', 'ARM', 'TSM', 'LSCC', 'ON']),
    ('⚡ AI 電力/能源', '#24e08a', '⭐⭐⭐⭐⭐', '最被低估的 AI 基建板塊。AI 資料中心用電量2030年將較2023年增加200%+，電力基礎設施嚴重滞後。核電是唯一可以提供24/7無碳穩定電力的能源，Constellation重啟三里島象徵核電AI時代來臨。VST、CEG、NRG 估值仍處歷史低位，距離52W低點提供罕見安全邊際。', ['VST', 'CEG', 'NRG', 'NEE', 'AES', 'PNRG', 'BE', 'ETN']),
    ('🖥️ AI 伺服器/雲端', '#06b6d4', '⭐⭐⭐⭐', 'CSP 資本支出2025年同比增30%+，Dell 今日暴漲22%象徵AI伺服器超級周期已來臨。HP PC復甦+AI PC換機潮提供額外彈性。Supermicro 審計問題掩蓋了真實AI需求，恢復後有修復空間。Arista 在AI網路交換器市場領導地位稳固。', ['SMCI', 'DELL', 'HPQ', 'ANET']),
    ('🔐 AI 資安/雲端安全', '#24e08a', '⭐⭐⭐⭐', 'AI攻擊增加（deepfake欺詐+AI-driven malware）創造結構性剛需。CrowdStrike Charlotte AI平台鞏固領導地位，Zscaler SASE市場領導但估值偏貴建議獲利了結。Okta 零信任身份管理是AI時代最底層的防線。Cloudflare Workers AI將AI推向edge，IoT安全是新成長曲線。', ['CRWD', 'NET', 'PANW', 'ZS', 'OKta']),
    ('📡 AI 光纖/網路', '#a855f7', '⭐⭐⭐⭐', 'AI資料中心互聯(DCI)需求爆發，800G光纖傳輸設備供不應求。Ciena即將創新高，WaveLogic 8平台全球領先。Marvell光纖收發器業務协同效應明顯，Corning特殊光纖供應緊俏。Lumen轉型CSP光纖骨幹網絡的故事誘人但執行風險高。', ['CIEN', 'GLW', 'LUMN', 'CSCO', 'MRVL']),
    ('💾 AI 記憶體/HBM', '#6366f1', '⭐⭐⭐⭐', 'HBM3e是AI GPU標配，美光已通過NVIDIA認證，三大CSP持續擴大訂單。AI伺服器memory含量是傳統伺服器4-5倍，HBM供需持續緊張至2025年底。三星落後給美光創造結構性份額提升。NAND景氣觸底反彈，WDC和鎧俠合併進程將改善供給側結構。', ['MU', 'WDC', 'NTAP', 'PSTG']),
]

for name, color, stars, desc, syms in theme_blocks:
    syms_html = ' '.join([f'<span style="font-size:10px;padding:2px 7px;border-radius:6px;font-weight:600;background:{color}15;color:{color}">{s}</span>' for s in syms if s in prices])
    html += f'''
      <div class="供需-card">
        <h4 style="color:{color}">{name} {stars}</h4>
        <p>{desc}</p>
        <div style="margin-top:10px;display:flex;flex-wrap:wrap;gap:5px">{syms_html}</div>
      </div>
'''

html += '''
    </div>
  </div>
</div>
'''

# SUPPLY/DEMAND
html += '''
<!-- SUPPLY/DEMAND -->
<div class="section" id="supply">
  <div class="section-header">
    <h2>E. AI 供需失衡深度分析</h2>
    <span class="badge">供給瓶頸 vs 需求爆發</span>
  </div>
  <div class="supply-block">
    <h3>關鍵供給瓶頸識別</h3>
    <div class="供需-row">
'''

bottlenecks = [
    ('CoWoS 先進封裝', '#6366f1', '台積電CoWoS產能是NVDA Blackwell出貨的唯一瓶頸。2025年CoWoS產能擴張進度將直接決定GB200交付節奏。這也是為什麼ASE和Amkor的替代封裝方案如此重要的原因。'),
    ('HBM 記憶體', '#f97316', 'HBM3e認證僅限美光和SK海力士，產能嚴重不足。三星 ainda落後，導致美光獲得不對稱份額提升。AI GPU標配HBM，需求量是傳統伺服器的4-5倍。'),
    ('電力容量', '#24e08a', '美國資料中心電力需求2030年將增加200%+，但電網基礎設施現代化嚴重滞後。核電、天然氣電廠審批新建需要5-10年。AI公司開始直接投資發電廠（微軟與Constellation合作為標誌）。'),
    ('光纖骨幹網', '#a855f7', 'AI資料中心互聯需要800G光纖傳輸，但Ciena、Marvell的800G產品交付落後需求1-2個季度。光纖基礎設施升級是長期結構性主題。'),
    ('液冷系統', '#06b6d4', 'AI伺服器熱密度傳統風冷已無法處理，液冷/浸沒式冷却是剛需。Vertiv今天暴跌-11.7%象徵散熱板塊短期超買，但長期需求真實存在。SPXC冷水機組估值仍合理。'),
    ('ARM 架構替代', '#f97316', 'x86在雲端資料中心的份額正在被ARM吃掉。AWS Graviton3、Microsoft Cobalt、Meta Scalable Solutions均基於Arm Neoverse，這是10年的結構性替代趨勢。Intel/AMD專利壁壘使替代不會瞬間發生，但份額流失不可逆。'),
]

for name, color, desc in bottlenecks:
    html += f'''
      <div class="供需-card">
        <h4 style="color:{color}">瓶頸：{name}</h4>
        <p>{desc}</p>
      </div>
'''

html += '''
    </div>
  </div>
  <div class="supply-block">
    <h3>需求爆發驅動力</h3>
    <div class="供需-row">
'''

demands = [
    ('CSP 資本支出', '#5b7fff', 'Microsoft、Google、Amazon、Meta 2025年資本支出總額將超過 $3000億，其中AI基礎設施佔比超過70%。這是史無前例的超級周期。'),
    ('推理需求爆發', '#f97316', 'ChatGPT以降，AI應用爆發。現在重心從訓練轉向推理，意味著需要更多GPU實例持續運行。推理的邊際成本結構使CSP有強烈動機優化性價比，利好AMD、Marvell等替代方案。'),
    ('企業 AI 採用', '#24e08a', 'Microsoft Copilot、Google Gemini、AWS Bedrock正在將AI普惠化。企業AI訂閱覆蓋率從不到5%快速爬升，帶動Azure、AWS、GCP整體成長加速。'),
    ('AI Edge 設備', '#06b6d4', 'Snapdragon X Elite、AI PC、智慧手機AI晶片將創造數十億規模的Edge AI設備換機潮。高通、蘋果、聯發科是核心受益者。Qualcomm今日暴漲+18.2%象徵市場開始認知這個趨勢。'),
    ('AI 軍事/國防', '#a855f7', '烏克蘭、以巴戰爭展示AI精確制導、無人機、AI情報分析的價值。美國、中國、歐洲各國開始大規模投資AI軍事應用。Palantir、Aurora、Anduril等是純粹AI軍工受益者。'),
]

for name, color, desc in demands:
    html += f'''
      <div class="供需-card">
        <h4 style="color:{color}">驅動：{name}</h4>
        <p>{desc}</p>
      </div>
'''

html += '''
    </div>
  </div>
</div>
'''

# TOMORROW
html += '''
<!-- TOMORROW -->
<div class="section">
  <div class="section-header">
    <h2>F. 明日觀察重點</h2>
    <span class="badge">2026-05-26</span>
  </div>
  <div class="card-row">
    <div class="card">
      <h3 style="margin-bottom:12px;font-size:14px">需密切關注的信號</h3>
      <ul style="font-size:13px;padding-left:18px;color:var(--text-dim);line-height:2">
        <li>NVDA 能否守住 $200 關口，若跌破可能測試 $185 支撐</li>
        <li>ARM 若能站穩 $300+，短線目標 $340，挑戰 $380</li>
        <li>DELL 逼近 $298 歷史高點，能否突破並創新高</li>
        <li>CIEN 若突破 $600 歷史高，開啟新一波漲勢</li>
        <li>VRT 今天暴跌 -11.7%，觀望是否止穩於 $310 支撐</li>
        <li>QCOM +18.2% 後，注意獲利了結賣壓</li>
      </ul>
    </div>
    <div class="card">
      <h3 style="margin-bottom:12px;font-size:14px">重要催化劑日曆</h3>
      <ul style="font-size:13px;padding-left:18px;color:var(--text-dim);line-height:2">
        <li>6月中旬：主要 CSP Q2 營收指引更新（GOOGL、MSFT、AMZN）</li>
        <li>6月下旬：美光 Q2 營收財報（記憶體景氣關鍵指標）</li>
        <li>NVIDIA GTC 大會（如有新品發布，持續催化股價）</li>
        <li>FED 利率決策（影響高P/E科技股估值）</li>
        <li>Arm Q2 營收（觀察資料中心滲透率是否加速）</li>
      </ul>
    </div>
    <div class="card">
      <h3 style="margin-bottom:12px;font-size:14px">主題機會追蹤</h3>
      <ul style="font-size:13px;padding-left:18px;color:var(--text-dim);line-height:2">
        <li>⚡ 電力短缺主題：VST、CEG、NRG 本週持續強勢，核電+天然氣多重能源組合更受青睐</li>
        <li>💾 HBM 記憶體：MU 本週仍有上漲空間，注意 $800 心理關口</li>
        <li>📡 光纖升級：CIEN 技術突破形態，等待 $600 確認</li>
        <li>🖥️ 伺服器超級周期：DELL、HPQ 短線動能最強，注意機構買盤持續性</li>
        <li>🤖 AI 軟體補漲：SNOW、PLTR 本週落後大盤，有補漲空間</li>
      </ul>
    </div>
  </div>
</div>
'''

html += f'''
<div class="footer">
  AI 基礎建設研究報告 | {today} | 精選 {len(selected)} 檔核心標的<br>
  本報告僅供參考，不構成投資建議。數據來源：Yahoo Finance、Barchart、信誼<br>
  <span style="color:var(--text-muted)">© 2026 AI Infrastructure Research. All rights reserved.</span>
</div>
</div>
</body>
</html>
'''

# Write HTML report
report_path = f'/home/matt/.openclaw/workspace/stock-reports/reports/{today.replace("年", "-").replace("月", "-").replace("日", "")}.html'
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Report saved to {report_path}")

# Now update index.html to point to this report
index_content = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI 基礎建設研究報告｜{today}</title>
<style>
:root {{ --bg: #080810; --bg2: #0c0c1a; --bg3: #10101f; --bg-card: #0e0e20; --border: rgba(255,255,255,0.07); --border-accent: rgba(91,127,255,0.3); --text: #e0e4f0; --text-dim: #7880a0; --text-muted: #444660; --accent: #5b7fff; --accent-glow: rgba(91,127,255,0.25); --green: #24e08a; --red: #f04040; --purple: #a855f7; --cyan: #06b6d4; --orange: #f97316; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
a {{ color: var(--accent); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--text); line-height: 1.7; font-size: 15px; }}
.wrap {{ max-width: 1140px; margin: 0 auto; padding: 28px 24px; }}
.site-header {{ display: flex; justify-content: space-between; align-items: center; padding: 18px 24px; border-bottom: 1px solid var(--border); background: var(--bg2); position: sticky; top: 0; z-index: 100; }}
.site-header .logo {{ font-size: 18px; font-weight: 700; }}
.site-header .logo span {{ color: var(--accent); }}
.site-header .nav-links {{ display: flex; gap: 24px; }}
.site-header .nav-links a {{ color: var(--text-dim); font-size: 13px; font-weight: 500; transition: color 0.2s; }}
.site-header .nav-links a:hover {{ color: var(--accent); text-decoration: none; }}
.update-badge {{ font-size: 11px; color: var(--text-dim); background: var(--bg3); border: 1px solid var(--border); padding: 5px 12px; border-radius: 20px; font-family: monospace; }}
.hero {{ background: linear-gradient(135deg, var(--bg2) 0%, var(--bg3) 60%, #0d0a28 100%); border: 1px solid rgba(91,127,255,0.18); border-radius: 24px; padding: 48px 52px; margin-bottom: 32px; text-align: center; position: relative; overflow: hidden; }}
.hero::before {{ content: ''; position: absolute; top: -50%; left: 50%; transform: translateX(-50%); width: 600px; height: 400px; background: radial-gradient(ellipse, rgba(91,127,255,0.09) 0%, transparent 70%); pointer-events: none; }}
.hero .hero-tag {{ display: inline-block; background: rgba(91,127,255,0.12); border: 1px solid rgba(91,127,255,0.3); color: var(--accent); font-size: 11px; font-weight: 600; padding: 5px 14px; border-radius: 20px; margin-bottom: 16px; letter-spacing: 1px; }}
.hero h1 {{ font-size: 32px; font-weight: 800; margin-bottom: 8px; letter-spacing: -0.5px; position: relative; }}
.hero .subtitle {{ color: var(--text-dim); font-size: 15px; margin-bottom: 28px; }}
.hero .stats-row {{ display: flex; justify-content: center; gap: 48px; flex-wrap: wrap; }}
.hero .stat {{ text-align: center; }}
.hero .stat .val {{ font-size: 22px; font-weight: 700; color: var(--green); }}
.hero .stat .label {{ font-size: 12px; color: var(--text-muted); margin-top: 2px; }}
.section {{ margin-bottom: 32px; }}
.section-header {{ display: flex; align-items: center; gap: 12px; margin-bottom: 18px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }}
.section-header h2 {{ font-size: 17px; font-weight: 700; }}
.section-header .badge {{ font-size: 10px; padding: 3px 9px; border-radius: 10px; background: rgba(91,127,255,0.12); color: var(--accent); font-weight: 600; letter-spacing: 0.5px; }}
.card {{ background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 22px 24px; margin-bottom: 16px; }}
.card:hover {{ border-color: var(--border-accent); box-shadow: 0 4px 24px rgba(0,0,0,0.3); }}
.report-card {{ display: block; background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 28px 32px; margin-bottom: 12px; transition: all 0.3s; text-decoration: none; }}
.report-card:hover {{ border-color: rgba(91,127,255,0.5); transform: translateY(-2px); box-shadow: 0 8px 32px rgba(91,127,255,0.15); }}
.report-card .report-date {{ font-size: 11px; color: var(--text-muted); font-weight: 600; letter-spacing: 0.5px; margin-bottom: 6px; text-transform: uppercase; }}
.report-card h3 {{ font-size: 18px; font-weight: 700; color: var(--text); margin-bottom: 6px; }}
.report-card .report-meta {{ display: flex; gap: 16px; font-size: 12px; color: var(--text-dim); margin-top: 10px; }}
.report-card .report-meta span {{ display: flex; align-items: center; gap: 4px; }}
.report-card .arrow {{ float: right; font-size: 20px; color: var(--accent); margin-top: -24px; }}
.grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
.grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }}
.theme-card {{ background: var(--bg-card); border: 1px solid var(--border); border-radius: 14px; padding: 18px; }}
.theme-card .theme-name {{ font-size: 13px; font-weight: 600; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; }}
.theme-card .theme-stocks {{ display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 10px; }}
.theme-card .mini-chip {{ font-size: 10px; padding: 2px 7px; border-radius: 6px; font-weight: 600; }}
.footer {{ text-align: center; padding: 32px 0; color: var(--text-muted); font-size: 12px; border-top: 1px solid var(--border); margin-top: 40px; }}
@media (max-width: 768px) {{ .grid-2, .grid-3 {{ grid-template-columns: 1fr; }} .hero {{ padding: 32px 24px; }} .hero h1 {{ font-size: 24px; }} .hero .stats-row {{ gap: 24px; }} .site-header .nav-links {{ display: none; }} }}
</style>
</head>
<body>
<div class="site-header">
  <div class="logo">AI 基建 <span>研究報告</span></div>
  <div class="nav-links">
    <a href="#latest-report">最新報告</a>
    <a href="#theme-watch">主題追蹤</a>
    <a href="#about">關於</a>
  </div>
  <div class="update-badge">{today} 更新</div>
</div>

<div class="wrap">
  <!-- HERO -->
  <div class="hero">
    <div class="hero-tag">AI 基礎建設美股研究報告</div>
    <h1>人工智慧基建超級周期</h1>
    <div class="subtitle">{today} | 每日自動更新</div>
    <div class="stats-row">
      <div class="stat"><div class="val">{len(selected)}</div><div class="label">精選股票</div></div>
      <div class="stat"><div class="val">12</div><div class="label">覆蓋板塊</div></div>
      <div class="stat"><div class="val">47</div><div class="label">Buy/Strong Buy</div></div>
      <div class="stat"><div class="val">ARM +46.5%</div><div class="label">今日最大漲幅</div></div>
      <div class="stat"><div class="val">⚡電力</div><div class="label">最大供需失衡</div></div>
    </div>
  </div>

  <!-- LATEST REPORT -->
  <div class="section" id="latest-report">
    <div class="section-header">
      <h2>最新研究報告</h2>
      <span class="badge">每日更新</span>
    </div>
    <a href="reports/{today.replace("年", "-").replace("月", "-").replace("日", "")}.html" class="report-card">
      <div class="report-date">{today}</div>
      <h3>AI 基礎建設美股研究報告｜{today}</h3>
      <div style="font-size:13px;color:var(--text-dim);margin-top:8px">
        涵蓋 {len(selected)} 檔 AI 基建核心標的｜市場雷達｜進場推薦｜深度分析｜供需失衡｜明日觀察
      </div>
      <div class="report-meta">
        <span>📊 {len(selected)} 檔精選</span>
        <span>💾 AI 晶片/GPU</span>
        <span>⚡ AI 電力/能源</span>
        <span>🔐 AI 資安/雲端</span>
        <span>☁️ AI 雲端平台</span>
      </div>
      <span class="arrow">→</span>
    </a>
  </div>

  <!-- THEME WATCH -->
  <div class="section" id="theme-watch">
    <div class="section-header">
      <h2>主題追蹤雷達</h2>
      <span class="badge">6 大賽道</span>
    </div>
    <div class="grid-3">
      <div class="theme-card">
        <div class="theme-name" style="color:#f97316">💾 AI 晶片/GPU ⭐⭐⭐⭐⭐</div>
        <div class="theme-stocks">
          <span class="mini-chip" style="background:rgba(249,115,22,0.15);color:#f97316">NVDA</span>
          <span class="mini-chip" style="background:rgba(249,115,22,0.15);color:#f97316">AMD</span>
          <span class="mini-chip" style="background:rgba(249,115,22,0.15);color:#f97316">ARM</span>
          <span class="mini-chip" style="background:rgba(249,115,22,0.15);color:#f97316">AVGO</span>
          <span class="mini-chip" style="background:rgba(249,115,22,0.15);color:#f97316">QCOM</span>
          <span class="mini-chip" style="background:rgba(249,115,22,0.15);color:#f97316">MRVL</span>
        </div>
        <p style="font-size:12px;color:var(--text-dim)">Blackwell瓶頸+CoWoS封裝+ARM替代x86</p>
      </div>
      <div class="theme-card">
        <div class="theme-name" style="color:#24e08a">⚡ AI 電力/能源 ⭐⭐⭐⭐⭐</div>
        <div class="theme-stocks">
          <span class="mini-chip" style="background:rgba(36,224,138,0.15);color:#24e08a">VST</span>
          <span class="mini-chip" style="background:rgba(36,224,138,0.15);color:#24e08a">CEG</span>
          <span class="mini-chip" style="background:rgba(36,224,138,0.15);color:#24e08a">NRG</span>
          <span class="mini-chip" style="background:rgba(36,224,138,0.15);color:#24e08a">NEE</span>
          <span class="mini-chip" style="background:rgba(36,224,138,0.15);color:#24e08a">BE</span>
          <span class="mini-chip" style="background:rgba(36,224,138,0.15);color:#24e08a">ETN</span>
        </div>
        <p style="font-size:12px;color:var(--text-dim)">核電+天然氣，距離52W低點黃金進場區</p>
      </div>
      <div class="theme-card">
        <div class="theme-name" style="color:#06b6d4">🖥️ AI 伺服器 ⭐⭐⭐⭐</div>
        <div class="theme-stocks">
          <span class="mini-chip" style="background:rgba(6,182,212,0.15);color:#06b6d4">DELL</span>
          <span class="mini-chip" style="background:rgba(6,182,212,0.15);color:#06b6d4">HPQ</span>
          <span class="mini-chip" style="background:rgba(6,182,212,0.15);color:#06b6d4">SMCI</span>
          <span class="mini-chip" style="background:rgba(6,182,212,0.15);color:#06b6d4">ANET</span>
        </div>
        <p style="font-size:12px;color:var(--text-dim)">CSP資本支出超級周期，伺服器需求爆發</p>
      </div>
      <div class="theme-card">
        <div class="theme-name" style="color:#a855f7">📡 AI 光纖/網路 ⭐⭐⭐⭐</div>
        <div class="theme-stocks">
          <span class="mini-chip" style="background:rgba(168,85,247,0.15);color:#a855f7">CIEN</span>
          <span class="mini-chip" style="background:rgba(168,85,247,0.15);color:#a855f7">GLW</span>
          <span class="mini-chip" style="background:rgba(168,85,247,0.15);color:#a855f7">CSCO</span>
          <span class="mini-chip" style="background:rgba(168,85,247,0.15);color:#a855f7">LUMN</span>
        </div>
        <p style="font-size:12px;color:var(--text-dim)">800G光纖DCI需求爆發，即將突破新高</p>
      </div>
      <div class="theme-card">
        <div class="theme-name" style="color:#24e08a">🔐 AI 資安/雲端 ⭐⭐⭐⭐</div>
        <div class="theme-stocks">
          <span class="mini-chip" style="background:rgba(36,224,138,0.15);color:#24e08a">CRWD</span>
          <span class="mini-chip" style="background:rgba(36,224,138,0.15);color:#24e08a">NET</span>
          <span class="mini-chip" style="background:rgba(36,224,138,0.15);color:#24e08a">PANW</span>
          <span class="mini-chip" style="background:rgba(36,224,138,0.15);color:#24e08a">ZS</span>
          <span class="mini-chip" style="background:rgba(36,224,138,0.15);color:#24e08a">OKta</span>
        </div>
        <p style="font-size:12px;color:var(--text-dim)">AI攻擊增加創造結構性資安剛需</p>
      </div>
      <div class="theme-card">
        <div class="theme-name" style="color:#5b7fff">☁️ AI 雲端平台 ⭐⭐⭐⭐</div>
        <div class="theme-stocks">
          <span class="mini-chip" style="background:rgba(91,127,255,0.15);color:#5b7fff">GOOGL</span>
          <span class="mini-chip" style="background:rgba(91,127,255,0.15);color:#5b7fff">MSFT</span>
          <span class="mini-chip" style="background:rgba(91,127,255,0.15);color:#5b7fff">AMZN</span>
          <span class="mini-chip" style="background:rgba(91,127,255,0.15);color:#5b7fff">META</span>
        </div>
        <p style="font-size:12px;color:var(--text-dim)">企業AI訂閱覆蓋率加速，Capital Light</p>
      </div>
    </div>
  </div>

  <!-- ABOUT -->
  <div class="section" id="about">
    <div class="section-header">
      <h2>關於本研究</h2>
    </div>
    <div class="card">
      <p style="font-size:13.5px;color:var(--text-dim);line-height:1.8">
        本報告由 AI 自動生成，每日追蹤覆蓋 AI 基礎建設全產業鏈：從電力、散熱、網路、光纖、晶片、封裝、伺服器、儲存到資安、軟體、雲端平台。<br><br>
        <strong style="color:var(--text)">分析方法：</strong>結合 Barchart 技術信號（100% Buy評等）+ Yahoo Finance 現時報價 + AI 自身判斷。每檔股票均有 AI 原生推薦理由與核心邏輯分析。<br><br>
        <strong style="color:var(--text)">覆蓋廣度：</strong>52 檔候選股 → AI 精選 47 檔納入報告（Buy/Strong Buy/Partial Buy）<br>
        <strong style="color:var(--text)">資料來源：</strong>Barchart（技術信號）、Yahoo Finance（即時報價、52W區間、成交量）<br>
        <strong style="color:var(--text)">風險提示：</strong>本報告僅供參考，不構成投資建議。投資人需自行承擔投資決策風險。
      </p>
    </div>
  </div>

  <div class="footer">
    AI 基礎建設研究報告 | {today} | 精選 {len(selected)} 檔核心標的<br>
    本報告僅供參考，不構成投資建議。數據來源：Yahoo Finance、Barchart<br>
    <span style="color:var(--text-muted)">© 2026 AI Infrastructure Research</span>
  </div>
</div>
</body>
</html>
'''

index_path = '/home/matt/.openclaw/workspace/stock-reports/index.html'
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(index_content)

print(f"Index updated: {index_path}")
print(f"Report generated: {report_path}")
print(f"Total stocks in report: {len(selected)}")
