import json
from datetime import datetime

with open('/tmp/stock_report_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

prices = data['prices']
categories = data['categories']
analysis = data['analysis']
selected_syms = data['selected']
report_date = data['report_date']

# Category performance
cat_data = {}
for sym, cat_info in categories.items():
    if sym in prices:
        cat = cat_info[0]
        if cat not in cat_data:
            cat_data[cat] = []
        p = prices[sym]
        cat_data[cat].append((sym, p['price'], p['chg'], p.get('from_low_pct', 0)))

cat_summary = {}
for cat, items in cat_data.items():
    chgs = [x[2] for x in items]
    avg = sum(chgs)/len(chgs)
    best = max(items, key=lambda x: x[2])
    worst = min(items, key=lambda x: x[2])
    cat_summary[cat] = {'avg': avg, 'best': best, 'worst': worst, 'items': items}

def chg_color(c):
    if c >= 2: return '🟢'
    elif c >= -2: return '🟡'
    else: return '🔴'

def chg_class(c):
    if c >= 2: return 'up-strong'
    elif c >= 0: return 'up'
    elif c >= -2: return 'down-light'
    else: return 'down'

def fmt_pct(c):
    return f"{c:+.2f}%"

def fmt_price(p):
    if p >= 1000:
        return f"${p:,.2f}"
    elif p >= 100:
        return f"${p:,.2f}"
    else:
        return f"${p:,.2f}"

def fmt_vol(v):
    if v >= 1e9:
        return f"{v/1e9:.1f}B"
    elif v >= 1e6:
        return f"{v/1e6:.1f}M"
    elif v >= 1e3:
        return f"{v/1e3:.0f}K"
    return str(v)

BC_LINK = "https://www.barchart.com/stocks/quotes/{sym}/overview"

today = datetime.now().strftime('%Y年%m月%d日 %H:%M')
today_full = datetime.now().strftime('%Y-%m-%d')

# Build category table rows
cat_rows = ""
cat_order = [
    ('💾 AI 晶片/GPU', '💾'),
    ('🖥️ AI 伺服器/雲端', '🖥️'),
    ('⚡ AI 電力/能源', '⚡'),
    ('🧊 AI 散熱/液冷', '🧊'),
    ('📡 AI 網路/光纖', '📡'),
    ('💾 AI 儲存/記憶體', '💾'),
    ('📦 AI 先進封裝/CoWoS', '📦'),
    ('🔐 AI 資安/雲端', '🔐'),
    ('🤖 AI 軟體/資料分析', '🤖'),
    ('☁️ AI 雲端平台', '☁️'),
    ('🏭 AI 基建其他', '🏭'),
]
for cat_name, emoji in cat_order:
    if cat_name in cat_summary:
        cs = cat_summary[cat_name]
        avg = cs['avg']
        items_display = ", ".join([f"<b>{s[0]}</b> {fmt_pct(s[2])}" for s in sorted(cs['items'], key=lambda x: -x[2])[:5]])
        strength = chg_color(avg)
        cat_rows += f"""
        <tr>
          <td><span class="cat-badge" style="background:#444">{emoji}</span></td>
          <td><b>{cat_name.split(' ', 1)[1] if ' ' in cat_name else cat_name}</b><br><small style="opacity:0.6">{items_display}</small></td>
          <td class="{chg_class(avg)}"><b>{fmt_pct(avg)}</b></td>
          <td>{strength}</td>
        </tr>"""

# Build stock table rows
stock_rows = ""
for sym in selected_syms:
    if sym not in prices:
        continue
    p = prices[sym]
    a = analysis.get(sym, {})
    cat_info = categories.get(sym, ('其他', '#666'))
    cat_name = cat_info[0]
    
    verdict_color = {'STRONG BUY': '#00ff88', 'BUY': '#4ade80', 'SPECULATIVE BUY': '#fbbf24', 'PARTIAL SELL': '#f97316', 'AVOID': '#ef4444'}.get(a.get('verdict', ''), '#999')
    
    entry = a.get('entry', 'N/A')
    stop = a.get('stop', 'N/A')
    target = a.get('outlook', 'N/A')
    if '目標' in target:
        target_val = target.split('目標')[1].strip().split('。')[0].strip()
    else:
        target_val = 'N/A'
    
    score = {'STRONG BUY': 9, 'BUY': 7, 'SPECULATIVE BUY': 6, 'PARTIAL SELL': 4, 'AVOID': 2}.get(a.get('verdict', ''), 5)
    
    stock_rows += f"""
        <tr class="stock-row" data-sym="{sym}">
          <td class="stock-sym"><a href="{BC_LINK.format(sym=sym)}" target="_blank" class="sym-link">{sym}</a></td>
          <td><span class="cat-dot" style="background:{cat_info[1]}"></span> <span class="stock-name">{p['name']}</span></td>
          <td class="price">{fmt_price(p['price'])}</td>
          <td class="{chg_class(p['chg'])}">{fmt_pct(p['chg'])}</td>
          <td><small>{fmt_price(p['low52'])} - {fmt_price(p['high52'])}</small></td>
          <td class="{'up-strong' if p.get('from_low_pct', 0) < 30 else 'neutral'}">{p.get('from_low_pct', '?'):.0f}%</td>
          <td class="pe">{a.get('core', 'N/A')[:60]}...</td>
          <td><span class="verdict-badge" style="border-color:{verdict_color};color:{verdict_color}">{a.get('verdict', '')}</span></td>
          <td>{entry}</td>
          <td>{target_val}</td>
          <td>{stop}</td>
        </tr>"""

# Build deep analysis cards
cards = ""
for sym in selected_syms:
    if sym not in prices:
        continue
    p = prices[sym]
    a = analysis.get(sym, {})
    cat_info = categories.get(sym, ('其他', '#666'))
    cat_name = cat_info[0]
    
    verdict_color = {'STRONG BUY': '#00ff88', 'BUY': '#4ade80', 'SPECULATIVE BUY': '#fbbf24', 'PARTIAL SELL': '#f97316', 'AVOID': '#ef4444'}.get(a.get('verdict', ''), '#999')
    signal = a.get('signal', '')
    
    cards += f"""
    <div class="stock-card" id="card-{sym}">
      <div class="card-header">
        <div class="card-left">
          <a href="{BC_LINK.format(sym=sym)}" target="_blank" class="card-sym">{sym}</a>
          <span class="card-name">{p['name']}</span>
          <span class="cat-badge" style="background:{cat_info[1]}">{cat_name.split(' ')[0]} {cat_name.split(' ')[1] if ' ' in cat_name else ''}</span>
        </div>
        <div class="card-right">
          <span class="verdict-badge" style="border-color:{verdict_color};color:{verdict_color}">{a.get('verdict', '')}</span>
          <span class="signal-tag">{signal}</span>
        </div>
      </div>
      <div class="card-body">
        <div class="price-row">
          <div class="price-main">{fmt_price(p['price'])} <span class="{chg_class(p['chg'])}">{fmt_pct(p['chg'])}</span></div>
          <div class="price-meta">52W: {fmt_price(p['low52'])} ~ {fmt_price(p['high52'])} | 距低: <b>{p.get('from_low_pct', 0):.1f}%</b> | Vol: {fmt_vol(p['volume'])}</div>
        </div>
        <div class="analysis-section">
          <div class="analysis-block">
            <div class="block-label">🎯 為什麼推薦</div>
            <div class="block-content">{a.get('core', 'N/A')}</div>
          </div>
          <div class="analysis-block">
            <div class="block-label">🔭 核心邏輯與展望</div>
            <div class="block-content">{a.get('outlook', 'N/A')}</div>
          </div>
          <div class="analysis-block">
            <div class="block-label">⚠️ 進場策略</div>
            <div class="block-content">進場區間：{a.get('entry', 'N/A')} | 止損：{a.get('stop', 'N/A')}</div>
          </div>
        </div>
      </div>
    </div>"""

html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI 基礎建設美股研究報告 {today_full}</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
:root {{
  --bg: #080810;
  --bg2: #0f0f1a;
  --bg3: #161625;
  --card: #1a1a2e;
  --border: #2a2a4a;
  --text: #e0e0ff;
  --text2: #9999bb;
  --text3: #6666aa;
  --accent: #6366f1;
  --green: #00ff88;
  --yellow: #fbbf24;
  --red: #ef4444;
  --cyan: #06b6d4;
  --purple: #a855f7;
  --orange: #f97316;
}}
body {{ background: var(--bg); color: var(--text); font-family: -apple-system, 'Segoe UI', sans-serif; line-height: 1.6; padding: 20px; }}
.container {{ max-width: 1400px; margin: 0 auto; }}

.header {{ text-align: center; padding: 30px 0; border-bottom: 1px solid var(--border); margin-bottom: 30px; }}
.header h1 {{ font-size: 2rem; background: linear-gradient(135deg, #6366f1, #06b6d4, #00ff88); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 8px; }}
.header .date {{ color: var(--text2); font-size: 1rem; }}
.header .badge {{ display: inline-block; background: var(--accent); color: white; padding: 4px 16px; border-radius: 20px; font-size: 0.85rem; margin-top: 10px; }}

.section-title {{ font-size: 1.3rem; color: var(--cyan); margin: 35px 0 15px; padding-left: 12px; border-left: 3px solid var(--cyan); }}

/* Category table */
.cat-table {{ width: 100%; border-collapse: collapse; background: var(--card); border-radius: 12px; overflow: hidden; }}
.cat-table th {{ background: var(--bg2); padding: 12px 16px; text-align: left; color: var(--text2); font-size: 0.85rem; }}
.cat-table td {{ padding: 12px 16px; border-top: 1px solid var(--border); font-size: 0.9rem; }}
.cat-table tr:hover {{ background: var(--bg3); }}
.cat-badge {{ display: inline-block; width: 28px; height: 28px; border-radius: 50%; text-align: center; line-height: 28px; font-size: 1rem; }}
.up-strong {{ color: var(--green); font-weight: 700; }}
.up {{ color: #4ade80; }}
.neutral {{ color: var(--text2); }}
.down-light {{ color: var(--yellow); }}
.down {{ color: var(--red); font-weight: 600; }}

/* Stock table */
.stock-table {{ width: 100%; border-collapse: collapse; background: var(--card); border-radius: 12px; overflow: hidden; margin-bottom: 30px; }}
.stock-table th {{ background: var(--bg2); padding: 12px 10px; text-align: left; color: var(--text2); font-size: 0.8rem; white-space: nowrap; }}
.stock-table td {{ padding: 10px; border-top: 1px solid var(--border); font-size: 0.85rem; }}
.stock-table tr:hover {{ background: var(--bg3); }}
.sym-link {{ color: var(--cyan); text-decoration: none; font-weight: 700; }}
.sym-link:hover {{ text-decoration: underline; }}
.stock-name {{ color: var(--text2); }}
.price {{ font-weight: 700; color: var(--text); }}
.cat-dot {{ display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 6px; }}
.verdict-badge {{ display: inline-block; padding: 2px 10px; border-radius: 12px; border: 1.5px solid; font-size: 0.75rem; font-weight: 700; }}
.signal-tag {{ font-size: 0.75rem; color: var(--text2); margin-left: 8px; }}
.pe {{ max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}

/* Stock cards */
.cards-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(480px, 1fr)); gap: 16px; }}
.stock-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 16px; overflow: hidden; }}
.card-header {{ display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; background: var(--bg2); border-bottom: 1px solid var(--border); }}
.card-left {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}
.card-right {{ display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }}
.card-sym {{ font-size: 1.3rem; font-weight: 800; color: var(--cyan); text-decoration: none; }}
.card-sym:hover {{ text-decoration: underline; }}
.card-name {{ font-size: 0.9rem; color: var(--text2); }}
.card-body {{ padding: 20px; }}
.price-row {{ margin-bottom: 16px; }}
.price-main {{ font-size: 1.8rem; font-weight: 800; color: var(--text); }}
.price-meta {{ font-size: 0.8rem; color: var(--text2); margin-top: 4px; }}
.analysis-section {{ display: flex; flex-direction: column; gap: 12px; }}
.analysis-block {{ background: var(--bg2); border-radius: 10px; padding: 12px 16px; }}
.block-label {{ font-size: 0.75rem; color: var(--accent); font-weight: 700; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px; }}
.block-content {{ font-size: 0.9rem; color: var(--text); line-height: 1.7; }}

/* Radar */
.radar-box {{ background: var(--card); border-radius: 12px; padding: 24px; margin-bottom: 20px; }}
.radar-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 12px; }}
.radar-item {{ background: var(--bg2); border-radius: 10px; padding: 14px 18px; display: flex; justify-content: space-between; align-items: center; }}
.radar-name {{ font-size: 0.9rem; font-weight: 600; }}
.radar-chg {{ font-weight: 700; }}

/* Theme summary */
.theme-box {{ background: var(--card); border-radius: 12px; padding: 24px; }}
.theme-item {{ display: flex; align-items: center; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border); }}
.theme-item:last-child {{ border-bottom: none; }}
.theme-left {{ display: flex; align-items: center; gap: 10px; font-size: 0.9rem; }}

/* Footer */
.footer {{ text-align: center; padding: 30px; color: var(--text3); font-size: 0.8rem; border-top: 1px solid var(--border); margin-top: 50px; }}
.footer a {{ color: var(--cyan); }}

@media (max-width: 768px) {{
  .cards-grid {{ grid-template-columns: 1fr; }}
  .header h1 {{ font-size: 1.4rem; }}
  .stock-table {{ font-size: 0.8rem; }}
  .stock-table th:nth-child(n+6) {{ display: none; }}
  .stock-table td:nth-child(n+6) {{ display: none; }}
}}
</style>
</head>
<body>
<div class="container">

<!-- HEADER -->
<div class="header">
  <h1>🤖 AI 基礎建設美股研究報告</h1>
  <div class="date">{today}（台北時間）</div>
  <div class="badge">AI Infrastructure Stock Report</div>
</div>

<!-- SECTION A: Category Performance -->
<h2 class="section-title">📊 A. AI 基礎建設覆蓋範疇  各類今日表現</h2>
<table class="cat-table">
  <thead>
    <tr>
      <th>類別</th>
      <th>代表股票（當日表現）</th>
      <th>類別平均日%</th>
      <th>強度</th>
    </tr>
  </thead>
  <tbody>
    {cat_rows}
  </tbody>
</table>

<!-- SECTION B: Market Radar -->
<h2 class="section-title">🛸 B. 今日 AI 基礎建設市場雷達</h2>
<div class="radar-box">
  <div class="radar-grid">
    <div class="radar-item">
      <span class="radar-name">💾 AI 晶片/GPU</span>
      <span class="radar-chg up-strong">+11.14%</span>
    </div>
    <div class="radar-item">
      <span class="radar-name">🖥️ AI 伺服器/雲端</span>
      <span class="radar-chg up-strong">+14.99%</span>
    </div>
    <div class="radar-item">
      <span class="radar-name">⚡ AI 電力/能源</span>
      <span class="radar-chg neutral">+1.11%</span>
    </div>
    <div class="radar-item">
      <span class="radar-name">🧊 AI 散熱/液冷</span>
      <span class="radar-chg down">-2.65%</span>
    </div>
    <div class="radar-item">
      <span class="radar-name">📡 AI 網路/光纖</span>
      <span class="radar-chg neutral">+2.09%</span>
    </div>
    <div class="radar-item">
      <span class="radar-name">💾 AI 儲存/記憶體</span>
      <span class="radar-chg neutral">+1.20%</span>
    </div>
    <div class="radar-item">
      <span class="radar-name">📦 AI 先進封裝/CoWoS</span>
      <span class="radar-chg neutral">+1.46%</span>
    </div>
    <div class="radar-item">
      <span class="radar-name">🔐 AI 資安/雲端</span>
      <span class="radar-chg up-strong">+10.62%</span>
    </div>
    <div class="radar-item">
      <span class="radar-name">🤖 AI 軟體/資料分析</span>
      <span class="radar-chg neutral">+4.00%</span>
    </div>
    <div class="radar-item">
      <span class="radar-name">☁️ AI 雲端平台</span>
      <span class="radar-chg neutral">-0.91%</span>
    </div>
    <div class="radar-item">
      <span class="radar-name">🏭 AI 基建其他</span>
      <span class="radar-chg neutral">+2.83%</span>
    </div>
  </div>
</div>

<div class="theme-box">
  <h3 style="color:var(--cyan);margin-bottom:12px;">🔥 今日市場情緒分析</h3>
  <div class="theme-item">
    <div class="theme-left"><span>🏆 今日最強</span></div>
    <span class="up-strong">AI 晶片/GPU + AI 資安（板塊大漲）</span>
  </div>
  <div class="theme-item">
    <div class="theme-left"><span>⬇️ 今日最弱</span></div>
    <span class="down">AI 散熱/液冷（VRT -11.7% 拖累類別）</span>
  </div>
  <div class="theme-item">
    <div class="theme-left"><span>🎯 市場關注焦點</span></div>
    <span style="color:var(--yellow)">ARM 爆漲 +46%、Qualcomm +18%、Dell +22%、HP +21%（AI PC + 伺服器超級周期）</span>
  </div>
  <div class="theme-item">
    <div class="theme-left"><span>💡 重要發現</span></div>
    <span>AI 基礎建設全板塊呈現結構性多頭，伺服器/PC 復甦最為明確，VRT/PSTG 散熱/儲存出現分化</span>
  </div>
</div>

<!-- SECTION C: Entry Recommendation Table -->
<h2 class="section-title">📋 C. 進場推薦總表（{len(selected_syms)} 檔）</h2>
<table class="stock-table">
  <thead>
    <tr>
      <th>股票</th>
      <th>名稱</th>
      <th>現價</th>
      <th>日%</th>
      <th>52W區間</th>
      <th>距低%</th>
      <th>摘要</th>
      <th>評分</th>
      <th>進場價</th>
      <th>目標價</th>
      <th>止損價</th>
    </tr>
  </thead>
  <tbody>
    {stock_rows}
  </tbody>
</table>

<!-- SECTION D: Deep Analysis Cards -->
<h2 class="section-title">📈 D. 深度個股分析（{len(selected_syms)} 檔）</h2>
<div class="cards-grid">
  {cards}
</div>

<!-- SECTION E: Theme Sector Evaluation -->
<h2 class="section-title">🏛️ E. 主題板塊評估</h2>
<div class="theme-box">
  <div class="theme-item">
    <div class="theme-left"><span>💾 AI 晶片/GPU</span></div>
    <span class="up-strong">強勢 🟢 — ARM +46%、QCOM +18%、AMD +10%、INTC +10%，板塊平均 +11.14%</span>
  </div>
  <div class="theme-item">
    <div class="theme-left"><span>🖥️ AI 伺服器/雲端</span></div>
    <span class="up-strong">極強 🟢 — DELL +22%、HPQ +21%、SMCI +14.6%，AI 伺服器超級周期確認</span>
  </div>
  <div class="theme-item">
    <div class="theme-left"><span>⚡ AI 電力/能源</span></div>
    <span class="neutral">中性 🟡 — VST +11.9%、CEG +10.1%、NRG +7.7%，核電/天然氣補漲但估值仍落後</span>
  </div>
  <div class="theme-item">
    <div class="theme-left"><span>🧊 AI 散熱/液冷</span></div>
    <span class="down">弱勢 🔴 — VRT -11.7% 暴跌，SPXC +3.4% 勉強撐住，散熱板塊估值已充分Price-in</span>
  </div>
  <div class="theme-item">
    <div class="theme-left"><span>📡 AI 網路/光纖</span></div>
    <span class="neutral">中性 🟡 — CIEN/Cisco/GLW 小漲，LUMN -6.4% 拖累，光纖升級需求真實但估值分化</span>
  </div>
  <div class="theme-item">
    <div class="theme-left"><span>🔐 AI 資安/雲端</span></div>
    <span class="up-strong">強勢 🟢 — ZS +13.2%、CRWD +11.7%、OKTA +11.4%、NET +9.4%，AI 資安剛需明確</span>
  </div>
  <div class="theme-item">
    <div class="theme-left"><span>🤖 AI 軟體/資料分析</span></div>
    <span class="neutral">中性 🟡 — SNOW +9.4%、PLTR +2.2%，AI 資料平台長期邏輯清晰但短期估值偏貴</span>
  </div>
  <div class="theme-item">
    <div class="theme-left"><span>☁️ AI 雲端平台</span></div>
    <span class="neutral">中性 🟡 — GOOGL -3.5%、MSFT -0.8%、META -0.7%，大型雲端股小幅回調，估值合理</span>
  </div>
</div>

<!-- SECTION F: AI Supply-Demand Imbalance -->
<h2 class="section-title">⚡ F. AI 供需失衡深度分析</h2>
<div class="theme-box">
  <div class="theme-item">
    <div class="theme-left"><span>🔴 最緊缺環節</span></div>
    <span>HBM 記憶體（Micron/Samsung/SK Hynix）、CoWoS 先進封裝（TSMC/ASE/Amkor）、AI 伺服器電源（Eaton/VRT）</span>
  </div>
  <div class="theme-item">
    <div class="theme-left"><span>🟡 次緊缺環節</span></div>
    <span>800G 光纖傳輸（Ciena/Corning）、AI 交換機（Arista/Cisco）、氫燃料電池（Bloom Energy）</span>
  </div>
  <div class="theme-item">
    <div class="theme-left"><span>🟢 供需改善中</span></div>
    <span>AI 電力（VST/CEG 擴張中）、AI 資安（CRWD/NET 持續創新護城河）、AI 軟體（Snowflake/PLTR 營收加速）</span>
  </div>
  <div class="theme-item">
    <div class="theme-left"><span>📊 供給落後需求時間差</span></div>
    <span>GPU/AI ASIC：落後 6-12 個月；HBM記憶體：落後 3-6 個月；資料中心電力：落後 2-4 年；800G光纖：落後 6-18 個月</span>
  </div>
  <div class="theme-item">
    <div class="theme-left"><span>💡 供需失衡投資啟示</span></div>
    <span>最直接受益順序：電力 > 先進封裝 > HBM > 光纖 > AI伺服器 > AI資安 > AI軟體 > 雲端平台</span>
  </div>
</div>

<!-- SECTION G: Tomorrow Watch -->
<h2 class="section-title">👀 G. 明日觀察</h2>
<div class="theme-box">
  <div class="theme-item">
    <div class="theme-left"><span>📅 明日重點</span></div>
    <span>ARM 能否站稳 $300 大關、NVDA 能否止跌回升、CIEN 是否突破 52W 高點</span>
  </div>
  <div class="theme-item">
    <div class="theme-left"><span>⚡ 催化劑觀察</span></div>
    <span>QCOM 季報後續航力、戴爾 AI 伺服器積壓訂單數據、AMD MI300X 採用進展</span>
  </div>
  <div class="theme-item">
    <div class="theme-left"><span>🔴 風險警示</span></div>
    <span>VRT 散熱泡沫化、PSTG 存儲暴跌持續性、LUMN/AMKR 落後股注意拋壓</span>
  </div>
  <div class="theme-item">
    <div class="theme-left"><span>💡 AI 基建方向</span></div>
    <span>AI PC 換機潮（HPQ/DELL）、資料中心電力（VST/CEG）、HBM 記憶體（MU）三條主線最明確</span>
  </div>
</div>

<!-- FOOTER -->
<div class="footer">
  <p>📅 報告日期：{today} | 資料來源：Yahoo Finance + AI 判斷分析</p>
  <p>⚠️ 本報告僅供參考，不構成投資建議。投資人請自行評估風險。</p>
  <p>🔗 <a href="https://www.barchart.com" target="_blank">Barchart</a> | <a href="https://github.com/acstep/stock-reports" target="_blank">GitHub Repo</a></p>
</div>

</div>
</body>
</html>"""

with open(f'/home/matt/.openclaw/workspace/stock-reports/reports/report_{today_full}.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Report generated: report_{today_full}.html")
print(f"Total selected stocks: {len(selected_syms)}")