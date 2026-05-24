#!/usr/bin/env python3
"""
AI 美股新聞蒐集器
抓取 Yahoo Finance 和 CNBC 的 AI/科技新聞
"""
import urllib.request, json, re, sys
from datetime import datetime

TODAY = datetime.now().strftime('%Y-%m-%d')

def fetch_yahoo_news(query, max_results=8):
    """從 Yahoo Finance 搜尋新聞"""
    try:
        url = f'https://query2.finance.yahoo.com/v1/finance/search?q={urllib.request.quote(query)}&quotesCount=0&newsCount={max_results}&enableFuzzyQuery=false'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            d = json.loads(resp.read())
            results = []
            for item in d.get('news', [])[:max_results]:
                title = item.get('title', '')
                link = item.get('link', '')
                source = item.get('publisher', 'Yahoo Finance')
                pubDate = item.get('pubDate', '')[:10] if item.get('pubDate') else TODAY
                if title and link and len(title) > 20:
                    results.append({
                        'title': title.strip(),
                        'link': link,
                        'source': source,
                        'date': pubDate,
                        'summary': item.get('summary', '')[:150] if item.get('summary') else ''
                    })
            return results
    except Exception as e:
        print(f'Yahoo error for "{query}": {e}', file=sys.stderr)
        return []

def fetch_cnbc_tech():
    """抓取 CNBC 科技頭條"""
    try:
        url = 'https://www.cnbc.com/technology/'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode('utf-8', errors='replace')
        
        # Find article links with dates
        articles = []
        # Try to find news cards with title and link
        patterns = [
            r'<a[^>]+href="(/technology/[^"]+)"[^>]*>\s*<[^>]*class="[^"]*Card[^"]*"[^>]*>\s*[^<]*<[^>]*>[^<]*</[^>]*>\s*<[^>]*>\s*([^<]{20,100})',
            r'href="(https://www\.cnbc\.com/[^"]+)"[^>]*>\s*([^<]{20,80}AI[^<]{0,200})',
            r'"title":"([^"]{30,150})"[^}]*"url":"(https://www\.cnbc\.com/[^"]+)"',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if len(matches[0]) >= 2:
                    link = match[0] if match[0].startswith('http') else 'https://www.cnbc.com' + match[0]
                    title = match[1].strip()
                    if title and 'cnbc.com' in link:
                        articles.append({
                            'title': re.sub(r'<[^>]+>', '', title),
                            'link': link,
                            'source': 'CNBC',
                            'date': TODAY
                        })
        
        seen = set()
        unique = []
        for a in articles:
            if a['title'] not in seen and len(a['title']) > 25:
                seen.add(a['title'])
                unique.append(a)
        return unique[:8]
    except Exception as e:
        print(f'CNBC error: {e}', file=sys.stderr)
        return []

def main():
    print('Fetching AI stock news...', file=sys.stderr)
    
    # Try specific AI stocks queries first
    queries = [
        'NVDA artificial intelligence chip GPU',
        'VST CEG data center power nuclear energy',
        'SMCI AMD server AI semiconductor',
        'AI infrastructure cooling fiber data center',
        'artificial intelligence market',
        'MU Micron HBM memory AI',
        'PLTR CRWD AI cybersecurity',
        'AI stocks earnings outlook 2025',
    ]
    
    all_news = []
    for q in queries:
        news = fetch_yahoo_news(q, max_results=5)
        all_news.extend(news)
    
    # Deduplicate by title
    seen = set()
    unique_news = []
    for n in all_news:
        if n['title'] not in seen:
            seen.add(n['title'])
            unique_news.append(n)
    
    # Sort by title length (prefer longer, more descriptive titles)
    unique_news.sort(key=lambda x: len(x['title']), reverse=True)
    
    print(f'Got {len(unique_news)} unique news items', file=sys.stderr)
    
    # Output as JSON for use in HTML generation
    print(json.dumps(unique_news[:12], ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()