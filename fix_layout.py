#!/usr/bin/env python3
"""Fix the deep analysis layout in generate_full_report.py"""

with open('generate_full_report.py') as f:
    content = f.read()

old_block = '''
for cat_tag, syms in sorted_ai_cats:
    cat_label = CAT_LABELS.get(cat_tag, cat_tag)
    html += f"""  <div class="cat-header">
    <div class="cat-icon">{cat_tag}</div>
    <div class="cat-title">{cat_label}（{len(syms)}檔）</div>
  </div>
  <div class="stock-grid">
"""
    # Sort by score desc then by price desc
    for sym in sorted(syms, key=lambda s: (final_data[s].get('score',0), final_data[s].get('curr_price',0)), reverse=True):
        d = final_data[sym]
        info = signal_lookup.get(sym, {})
        score_c = '#24e08a' if d['score']>=8 else '#5b7fff' if d['score']>=5 else '#ffc107' if d['score']>=3 else '#666'
        cc = change_cls(d.get('change'))
        
        html += f"""    <div class="stock-card">
      <div class="card-header">
        <div>
          <div class="sym"><a href="https://www.barchart.com/stocks/quotes/{sym}/overview" target="_blank" class="bc-link">{sym}</a></div>
          <div class="name">{d['name']}</div>
          <span class="tag">{d.get('tag','')}</span>
        </div>
        <div class="score-badge" style="background:rgba(91,127,255,0.1);color:{score_c}">{d['score']}分</div>
      </div>
      
      <div class="price-row">
        <div class="price">{d.get('price','—')}</div>
        <div class="change {cc}">{d.get('change','—')}</div>
      </div>
      <div class="range">52週 {d.get('low52','—')} ~ {d.get('high52','—')}</div>
      
      <div class="metrics">
        <div class="metric"><div class="val">{d.get('pe','—')}</div><div class="lbl">P/E</div></div>
        <div class="metric"><div class="val">{d.get('beta','—')}</div><div class="lbl">Beta</div></div>
        <div class="metric"><div class="val">{d.get('mktcap','—')}</div><div class="lbl">市值</div></div>
        <div class="metric"><div class="val">{info.get('opinion','100% Buy').replace('100% ','')}</div><div class="lbl">信號</div></div>
      </div>
      
      <div class="signals">
        <div class="sig" style="color:#8090c0;font-weight:600;margin-bottom:6px">📋 {d.get('category','—')}</div>
        <div class="sig" style="color:#c0c8e0">{d.get('desc','')[:200]}</div>
        <div class="sig" style="color:#24e08a;font-weight:600">⚡ 供需邏輯：{d.get('supply','')[:150]}</div>
      </div>
      
      <a class="bc-link" href="https://www.barchart.com/stocks/quotes/{sym}/overview" target="_blank">📊 詳細報價 → Barchart</a>
    </div>
"""
    html += "  </div>\n"

html += """  </div>
</div>
"""

# TechCrunch News'''

CAT_ACCENT = {
    '💾': ('#5b7fff', 'rgba(91,127,255,0.07)'),
    '📡': ('#24e08a', 'rgba(36,224,138,0.06)'),
    '⚡': ('#ffc107', 'rgba(255,193,7,0.06)'),
    '🚀': ('#e879f0', 'rgba(232,121,240,0.06)'),
    '🖥️': ('#4ecdc4', 'rgba(78,205,196,0.06)'),
    '🧊': ('#67e8f9', 'rgba(103,232,249,0.06)'),
    '🔐': ('#f97316', 'rgba(249,115,22,0.06)'),
    '🤖': ('#a78bfa', 'rgba(167,139,250,0.06)'),
    '☢️': ('#22d3ee', 'rgba(34,211,238,0.06)'),
    '其他': ('#8090c0', 'rgba(128,144,192,0.05)'),
}

new_block = '''
# ── Deep Analysis: each category as a styled subsection ──
html += f"""
<div class="section">
  <h2>💼 深度個股分析（AI 供應鏈核心標的）</h2>
  <p style="color:#8090b0;font-size:13px;margin-bottom:28px">共 {len(final_data)} 檔個股，完整來自 Barchart Top 1% Signal Strength 強勢股名單（按評分排序）。</p>
"""

for cat_tag, syms in sorted_ai_cats:
    cat_label = CAT_LABELS.get(cat_tag, cat_tag)
    accent, bg = CAT_ACCENT.get(cat_tag, ('#8090c0', 'rgba(128,144,192,0.05)'))

    html += f"""  <div style="margin-bottom:28px;background:{bg};border:1px solid rgba(255,255,255,0.05);border-radius:14px;padding:16px 20px 20px">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid rgba(255,255,255,0.05)">
      <span style="font-size:22px">{cat_tag}</span>
      <span style="color:{accent};font-weight:700;font-size:15px">{cat_label}</span>
      <span style="background:{accent};color:#000;font-size:11px;font-weight:800;padding:2px 9px;border-radius:10px">{len(syms)}檔</span>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:12px">
"""

    for sym in sorted(syms, key=lambda s: (final_data[s].get('score', 0), final_data[s].get('curr_price', 0)), reverse=True):
        d = final_data[sym]
        info = signal_lookup.get(sym, {})
        score_c = '#24e08a' if d['score'] >= 8 else '#5b7fff' if d['score'] >= 5 else '#ffc107' if d['score'] >= 3 else '#666'
        cc = change_cls(d.get('change'))
        desc_val = d.get('desc', '')[:130] if d.get('desc') else ''
        supply_val = d.get('supply', '')[:120] if d.get('supply') else ''

        html += f"""      <div class="stock-card" style="border-left:3px solid {accent}">
        <div class="card-header">
          <div>
            <div class="sym"><a href="https://www.barchart.com/stocks/quotes/{sym}/overview" target="_blank" class="bc-link">{sym}</a></div>
            <div class="name">{d['name']}</div>
            <span class="tag">{d.get('tag', '')}</span>
          </div>
          <div class="score-badge" style="background:rgba(91,127,255,0.12);color:{score_c};font-size:12px;font-weight:700">{d['score']}分</div>
        </div>
        <div class="price-row">
          <div class="price">{d.get('price', '—')}</div>
          <div class="change {cc}">{d.get('change', '—')}</div>
        </div>
        <div class="range" style="font-size:11px">52週 {d.get('low52', '—')} ~ {d.get('high52', '—')}</div>
        <div class="metrics">
          <div class="metric"><div class="val">{d.get('pe', '—')}</div><div class="lbl">P/E</div></div>
          <div class="metric"><div class="val">{d.get('beta', '—')}</div><div class="lbl">Beta</div></div>
          <div class="metric"><div class="val">{info.get('opinion', '100% Buy').replace('100% ', '')}</div><div class="lbl">信號</div></div>
        </div>
        <div class="signals">
          <div class="sig" style="color:#8090c0;font-weight:600;margin-bottom:4px;font-size:11px">📋 {d.get('category', '—')}</div>
          <div class="sig" style="color:#c0c8e0;font-size:11px;line-height:1.45">{desc_val}</div>
          {f'<div class="sig" style="color:#24e08a;font-weight:600;font-size:11px;margin-top:4px">⚡ {supply_val}</div>' if supply_val else ''}
        </div>
        <a class="bc-link" href="https://www.barchart.com/stocks/quotes/{sym}/overview" target="_blank" style="font-size:11px">📊 Barchart 報價 →</a>
      </div>
"""

    html += """    </div>
  </div>
"""

html += """</div>

# TechCrunch News'''

if old_block in content:
    content = content.replace(old_block, new_block)
    print("✅ Replacement successful!")
else:
    print("❌ Pattern not found!")
    import sys
    sys.exit(1)

with open('generate_full_report.py', 'w') as f:
    f.write(content)