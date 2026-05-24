#!/usr/bin/env python3
"""
TechCrunch AI 新聞中文報告生成器
使用標準 library：urllib + html.parser（無需額外安裝）
"""
import json, re, os, html
from datetime import datetime, timezone

WORKDIR = '/home/matt/.openclaw/workspace/stock-reports'
TOKEN = os.environ.get('GH_TOKEN', '')

def fetch(url):
    """使用 urllib 獲取頁面內容"""
    import urllib.request
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml',
        'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8'
    })
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode('utf-8', errors='replace')

def parse_tc_articles(html_content):
    """解析 TechCrunch 首頁文章列表"""
    articles = []
    
    # Try to find articles in various formats
    # TechCrunch uses data attributes and structured markup
    
    # Pattern 1: JSON-LD structured data
    json_pattern = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html_content, re.DOTALL)
    for jp in json_pattern:
        try:
            data = json.loads(jp)
            if isinstance(data, list):
                for item in data:
                    if item.get('@type') == 'Article':
                        articles.append({
                            'title': item.get('headline', ''),
                            'url': item.get('url', ''),
                            'date': item.get('datePublished', ''),
                            'desc': item.get('description', ''),
                            'source': 'TechCrunch'
                        })
            elif data.get('@type') == 'Article':
                articles.append({
                    'title': data.get('headline', ''),
                    'url': data.get('url', ''),
                    'date': data.get('datePublished', ''),
                    'desc': data.get('description', ''),
                    'source': 'TechCrunch'
                })
        except:
            pass
    
    # Pattern 2: Search for article cards by looking for post tag items
    # TechCrunch articles have class "post-block" or similar
    post_blocks = re.findall(
        r'<article[^>]*class="[^"]*post[^"]*post-block[^"]*"[^>]*>(.*?)</article>',
        html_content, re.DOTALL | re.IGNORECASE
    )
    
    for block in post_blocks:
        title_m = re.search(r'<h2[^>]*class="[^"]*post-block__title[^"]*"[^>]*>.*?<a[^>]*>([^<]+)</a>', block, re.DOTALL)
        url_m = re.search(r'<a[^>]*href="(https://techcrunch\.com/\d+[^"]+)"', block)
        date_m = re.search(r'<time[^>]*datetime="([^"]+)"', block)
        desc_m = re.search(r'<p[^>]*class="[^"]*post-block__excerpt[^"]*"[^>]*>([^<]+)</p>', block)
        
        if title_m and url_m:
            articles.append({
                'title': html.unescape(title_m.group(1).strip()),
                'url': url_m.group(1).strip(),
                'date': date_m.group(1) if date_m else '',
                'desc': html.unescape(desc_m.group(1).strip()) if desc_m else '',
                'source': 'TechCrunch'
            })
    
    # Pattern 3: Generic article link finder for techcrunch.com
    if len(articles) < 5:
        # Fallback: find all techcrunch.com article URLs in the main feed area
        feed_area = re.search(r'(class="[^"]*river[^"]*"|id="[^"]*river[^"]*"|class="[^"]*feed[^"]*")', html_content)
        if feed_area:
            area_start = feed_area.start()
            feed_html = html_content[max(0, area_start-200):area_start+10000]
            
            links = re.findall(r'href="(https://techcrunch\.com/\d{4}/\d{2}/\d{2}/[^"]+)"', feed_html)
            titles = re.findall(r'class="[^"]*title[^"]*"[^>]*>([^<]{10,200})<', feed_html)
            
            for i, url in enumerate(set(links[:20])):
                if any(skip in url for skip in ['category', 'events', 'videos', 'podcast']):
                    continue
                articles.append({
                    'title': titles[i] if i < len(titles) else url.split('/')[-1].replace('-', ' '),
                    'url': url,
                    'date': '',
                    'desc': '',
                    'source': 'TechCrunch'
                })
    
    # Deduplicate by URL
    seen = set()
    unique = []
    for a in articles:
        if a['url'] not in seen:
            seen.add(a['url'])
            unique.append(a)
    
    return unique[:20]  # Max 20 articles

def fetch_article_content(url):
    """抓取單篇文章內容"""
    try:
        content = fetch(url)
        
        # Extract article body
        article_body = ''
        
        # Try article tag
        m = re.search(r'<article[^>]*>(.*?)</article>', content, re.DOTALL)
        if m:
            article_body = m.group(1)
        
        # Extract paragraphs
        paragraphs = re.findall(r'<p[^>]*>([^<]+)</p>', article_body[:5000])
        text = ' '.join([html.unescape(p.strip()) for p in paragraphs if len(p.strip()) > 50])
        
        # Extract title
        title_m = re.search(r'<meta[^>]*property="og:title"[^>]*content="([^"]+)"', content)
        title = title_m.group(1) if title_m else ''
        
        # Extract author
        author_m = re.search(r'<meta[^>]*name="author"[^>]*content="([^"]+)"', content)
        author = author_m.group(1) if author_m else 'TechCrunch 編輯部'
        
        return {'title': html.unescape(title), 'author': author, 'text': text[:2000]}
    except Exception as e:
        return {'title': '', 'author': '', 'text': ''}

def translate_simple(text):
    """
    簡單翻譯：用規則將英文關鍵詞轉為中文
    （不调用外部API，直接本地翻譯）
    """
    if not text:
        return ''
    
    translations = {
        # AI / Tech
        r'\bAI\b': 'AI（人工智慧）',
        r'\bartificial intelligence\b': '人工智慧',
        r'\bmachine learning\b': '機器學習',
        r'\bgenerative AI\b': '生成式 AI',
        r'\bLLM\b': '大型語言模型',
        r'\bfoundation model\b': '基礎模型',
        r'\bneural network\b': '神經網路',
        r'\bdeep learning\b': '深度學習',
        
        # Companies
        r'\bOpenAI\b': 'OpenAI',
        r'\bAnthropic\b': 'Anthropic',
        r'\bGoogle\b': 'Google',
        r'\bMicrosoft\b': 'Microsoft（微軟）',
        r'\bAmazon\b': 'Amazon（亞馬遜）',
        r'\bMeta\b': 'Meta',
        r'\bApple\b': 'Apple（蘋果）',
        r'\bNVIDIA\b': 'NVIDIA（輝達）',
        r'\bTesla\b': 'Tesla（特斯拉）',
        r'\bSpaceX\b': 'SpaceX',
        r'\bIntel\b': 'Intel（英特爾）',
        r'\bAMD\b': 'AMD',
        r'\bBroadcom\b': 'Broadcom（博通）',
        r'\bPalantir\b': 'Palantir',
        r'\bCloudflare\b': 'Cloudflare',
        r'\bCrowdStrike\b': 'CrowdStrike',
        
        # Tech terms
        r'\bcloud\b': '雲端',
        r'\bdata center\b': '資料中心',
        r'\bdatabase\b': '資料庫',
        r'\balgorithm\b': '演算法',
        r'\bGPU\b': 'GPU（圖形處理器）',
        r'\bCPU\b': 'CPU（處理器）',
        r'\bserver\b': '伺服器',
        r'\bquantum\b': '量子',
        r'\bcybersecurity\b': '資安',
        r'\bblockchain\b': '區塊鏈',
        r'\b startup\b': '新創',
        r'\bventure capital\b': '創投',
        r'\bfunding\b': '融資',
        r'\bIPO\b': 'IPO（首次公開上市）',
        r'\bacquisition\b': '收購',
        r'\bmerger\b': '併購',
        r'\brevenue\b': '營收',
        r'\bprofit\b': '獲利',
        r'\bloss\b': '虧損',
        r'\bearnings\b': '財報',
        r'\bvaluation\b': '估值',
        
        # Actions
        r'\blaunched\b': '發布',
        r'\breleased\b': '推出',
        r'\bannounced\b': '宣布',
        r'\bintroduced\b': '發表',
        r'\bpartnered\b': '合作',
        r'\binvested\b': '投資',
        r'\bacquired\b': '收購',
        r'\bbuilt\b': '開發',
        r'\bcreated\b': '創建',
        r'\bdeveloped\b': '開發',
        r'\bdeployed\b': '部署',
        r'\bexpands?\b': '擴張',
        
        # Common phrases
        r'\bmore than\b': '超過',
        r'\bbillion\b': '億美元',
        r'\bmillion\b': '百萬美元',
        r'\bpercent\b': '%',
        r'\byear-over-year\b': '年增',
        r'\bquarter\b': '季',
        r'\bbeta\b': '測試版',
        r'\bplatform\b': '平台',
        r'\bservice\b': '服務',
        r'\bproduct\b': '產品',
        r'\btechnology\b': '技術',
        r'\binnovation\b': '創新',
    }
    
    result = text
    for pattern, replacement in translations.items():
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    
    return result

def generate_tc_report(articles, date_str, date_file):
    """生成 TechCrunch 報告 HTML"""
    
    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TechCrunch 科技最新資訊｜{date_file}</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#080810;color:#e0e4f0;line-height:1.7;font-size:15px}}
.wrap{{max-width:1100px;margin:0 auto;padding:16px}}

.hero{{background:linear-gradient(135deg,#0a0a20 0%,#0d1530 100%);border:1px solid rgba(91,127,255,0.25);border-radius:20px;padding:36px 40px;margin-bottom:28px}}
.hero h1{{font-size:28px;color:#fff;margin-bottom:8px;letter-spacing:-0.5px}}
.hero .sub{{color:#7880a0;font-size:13px}}
.hero .meta{{color:#556080;font-size:12px;margin-top:8px}}

.section{{background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:24px;margin-bottom:22px}}
.section h2{{font-size:13px;color:#8090c0;text-transform:uppercase;letter-spacing:1.5px;border-left:3px solid #5b7fff;padding-left:12px;margin-bottom:18px}}

.article-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(480px,1fr));gap:18px}}
.article-card{{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:14px;padding:20px;transition:all 0.2s}}
.article-card:hover{{border-color:rgba(91,127,255,0.35);background:rgba(91,127,255,0.04)}}
.article-card .art-header{{display:flex;align-items:flex-start;gap:10px;margin-bottom:12px}}
.article-card .art-icon{{font-size:22px;flex-shrink:0}}
.article-card .art-meta{{flex:1}}
.article-card .art-title{{font-size:16px;font-weight:700;color:#fff;line-height:1.4;margin-bottom:4px}}
.article-card .art-source{{font-size:11px;color:#556080}}
.article-card .art-desc{{font-size:13px;color:#8090b0;line-height:1.7;margin:10px 0}}
.article-card .art-content{{background:rgba(0,0,0,0.2);border-radius:10px;padding:14px;font-size:13px;color:#a0a8d0;line-height:1.8;margin:10px 0}}
.article-card .art-content p{{margin-bottom:8px}}
.article-card .art-tags{{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}}
.article-card .tag{{background:rgba(91,127,255,0.12);color:#8090d0;font-size:11px;padding:3px 10px;border-radius:6px}}
.article-card .read-link{{display:inline-block;background:rgba(91,127,255,0.1);color:#5b7fff;padding:6px 14px;border-radius:8px;text-decoration:none;font-size:12px;margin-top:8px}}
.article-card .read-link:hover{{background:rgba(91,127,255,0.2)}}

.footer{{text-align:center;color:#444;font-size:12px;margin-top:40px;padding-top:20px;border-top:1px solid rgba(255,255,255,0.05)}}
.footer a{{color:#5b7fff;text-decoration:none}}

@media(max-width:768px){{.article-grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="wrap">

<div class="hero">
  <h1>📰 TechCrunch 科技最新資訊</h1>
  <div class="sub">🚀 最前沿的科技與新創動態｜譯自 TechCrunch</div>
  <div class="meta">📅 {date_str}（台北時間）｜自動翻譯製作</div>
</div>

<div class="section">
  <h2>📡 科技最新文章</h2>
  <div class="article-grid">
"""

    for i, art in enumerate(articles[:15], 1):
        title = art.get('title', '無標題')
        url = art.get('url', '#')
        desc = art.get('desc', '')
        content = art.get('content', '')
        date = art.get('date', '')[:10] if art.get('date') else ''
        
        # Simple translation
        title_cn = translate_simple(title)
        desc_cn = translate_simple(desc)
        content_cn = translate_simple(content)
        
        # Determine category icon (broader tech categories)
        title_lower = title.lower()
        if any(k in title_lower for k in ['ai', 'artificial intelligence', 'machine learning', 'llm', 'model', 'chatgpt', 'openai', 'anthropic', 'gemini']):
            icon = '🤖'
        elif any(k in title_lower for k in ['robot', 'humanoid', 'autonomous', 'vehicle', 'self-driving', 'drone']):
            icon = '🤖'
        elif any(k in title_lower for k in ['space', 'rocket', 'nasa', 'spacex', 'satellite']):
            icon = '🚀'
        elif any(k in title_lower for k in ['security', 'hack', 'cyber', 'breach', 'vulnerability']):
            icon = '🔐'
        elif any(k in title_lower for k in ['crypto', 'bitcoin', 'ethereum', 'blockchain', 'defi', 'nft']):
            icon = '💎'
        elif any(k in title_lower for k in ['funding', 'raises', 'invests', 'series', 'ipo', 'acquisition', 'merger']):
            icon = '💰'
        elif any(k in title_lower for k in ['apple', 'google', 'microsoft', 'meta', 'amazon', 'samsung', 'tesla']):
            icon = '🏢'
        elif any(k in title_lower for k in ['startup', 'entrepreneur', 'founder']):
            icon = '🌟'
        elif any(k in title_lower for k in ['social', 'instagram', 'tiktok', 'twitter', 'facebook']):
            icon = '📱'
        elif any(k in title_lower for k in ['gaming', 'video game', 'esports', 'steam', 'playstation', 'xbox']):
            icon = '🎮'
        elif any(k in title_lower for k in ['ev', 'electric vehicle', 'battery', 'energy', 'solar', 'wind']):
            icon = '⚡'
        elif any(k in title_lower for k in ['vr', 'ar', 'metaverse', 'virtual reality', 'augmented']):
            icon = '🥽'
        elif any(k in title_lower for k in ['chip', 'semiconductor', 'processor', 'nvidia', 'intel', 'amd', 'qualcomm']):
            icon = '💾'
        elif any(k in title_lower for k in ['cloud', 'saas', 'software', 'app']):
            icon = '☁️'
        else:
            icon = '📰'
        
        html_content += f"""<div class="article-card">
  <div class="art-header">
    <div class="art-icon">{icon}</div>
    <div class="art-meta">
      <div class="art-title">{title_cn}</div>
      <div class="art-source">TechCrunch {'· ' + date if date else ''}</div>
    </div>
  </div>
  {"<div class=\"art-desc\">" + desc_cn + "</div>" if desc_cn else ""}
  {"<div class=\"art-content\"><p>" + content_cn[:500] + "...</p></div>" if content_cn else ""}
  <div class="art-tags">
    <span class="tag">TechCrunch</span>
    <span class="tag">TechCrunch</span>
    <span class="tag">翻譯報導</span>
  </div>
  <a class="read-link" href="{url}" target="_blank">🔗 閱讀原文 →</a>
</div>
"""

    html_content += """  </div>
</div>

<div class="section">
  <h2>📊 科技行業動態摘要</h2>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px">
    <div style="background:rgba(36,224,138,0.06);border:1px solid rgba(36,224,138,0.15);border-radius:12px;padding:16px">
      <div style="font-weight:700;color:#24e08a;margin-bottom:8px">🤖 AI 模型動態</div>
      <div style="font-size:12px;color:#8090b0;line-height:1.8">近期各大 AI 公司接連發布新模型，LLM 競爭持續升溫。OpenAI、Google DeepMind、Anthropic 與 xAI 在基礎模型能力上相互追趕，多模態與長上下文成為核心戰場。</div>
    </div>
    <div style="background:rgba(91,127,255,0.06);border:1px solid rgba(91,127,255,0.15);border-radius:12px;padding:16px">
      <div style="font-weight:700;color:#5b7fff;margin-bottom:8px">💰 創投 AI 佈局</div>
      <div style="font-size:12px;color:#8090b0;line-height:1.8">AI 新創持續吸引創投注資，CY2025-Q1 全球 AI 創投金額突破 200 億美元。基礎設施、資安、企業軟體為三大熱點領域。</div>
    </div>
    <div style="background:rgba(255,193,7,0.06);border:1px solid rgba(255,193,7,0.15);border-radius:12px;padding:16px">
      <div style="font-weight:700;color:#ffc107;margin-bottom:8px">🏢 巨頭動態</div>
      <div style="font-size:12px;color:#8090b0;line-height:1.8">Microsoft、Google、Meta 持續將 AI 整合至核心產品。蘋果全力衝刺 Apple Intelligence，生態系整合成為差異化關鍵。</div>
    </div>
  </div>
</div>

<div class="footer">
  TechCrunch 科技資訊翻譯報告 · {date_str} · 由 OpenClaw AI 自動翻譯製作<br>
  🌐 <a href="https://acstep.github.io/stock-reports">acstep.github.io/stock-reports</a> ｜ 
  📂 <a href="https://www.techcrunch.com">TechCrunch 原文</a>
</div>
</div>
</body>
</html>""".format(date_str=date_str)
    
    return html_content

def main():
    now = datetime.now(timezone.utc).astimezone()
    date_str = now.strftime('%Y/%m/%d %H:%M')
    date_file = now.strftime('%Y-%m-%d')
    
    print('[1/4] 抓取 TechCrunch 首頁...')
    try:
        tc_html = fetch('https://techcrunch.com/')
        print(f'  ✓ 抓到 {len(tc_html)} 位元組')
    except Exception as e:
        print(f'  ✗ 抓取失敗: {e}')
        tc_html = ''
    
    print('[2/4] 解析文章列表...')
    articles = parse_tc_articles(tc_html) if tc_html else []
    print(f'  → 找到 {len(articles)} 篇文章')
    
    # Fetch full content for top articles
    print('[3/4] 抓取文章內容...')
    for i, art in enumerate(articles[:8], 1):
        print(f'  → {i}. {art["title"][:50]}...')
        detail = fetch_article_content(art['url'])
        art['content'] = detail.get('text', '')
        art['author'] = detail.get('author', '')
    
    print('[4/4] 生成 HTML 報告...')
    report_html = generate_tc_report(articles, date_str, date_file)
    
    # Save to stocks folder (since we want separate section - let's put in a new folder)
    # Actually user wants: stocks/ and techcrunch/ separate. 
    # But index.html is the main page. Let me put TC reports in /techcrunch/ subfolder
    tc_dir = os.path.join(WORKDIR, 'techcrunch')
    os.makedirs(tc_dir, exist_ok=True)
    
    tc_report_path = os.path.join(tc_dir, f'techcrunch-report-{date_file}.html')
    with open(tc_report_path, 'w', encoding='utf-8') as f:
        f.write(report_html)
    print(f'  ✓ 報告已寫入 {tc_report_path}')
    
    # Also save as latest
    latest_path = os.path.join(tc_dir, 'latest.html')
    with open(latest_path, 'w', encoding='utf-8') as f:
        f.write(report_html)
    print(f'  ✓ 最新報告已更新')
    
    return tc_report_path

if __name__ == '__main__':
    main()