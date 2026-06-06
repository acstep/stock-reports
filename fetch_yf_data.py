#!/usr/bin/env python3
"""Fetch stock fundamentals from Yahoo Finance for AI infrastructure stocks."""
import json
import sys
import time
import urllib.request
import urllib.parse
import re
from datetime import datetime

# Comprehensive AI infrastructure universe across 11 categories
UNIVERSE = {
    "💾 AI晶片_GPU": ["NVDA", "AMD", "INTC", "QCOM", "AVGO", "MRVL", "ARM"],
    "🖥️ AI伺服器_雲端": ["SMCI", "DELL", "HPQ", "LEN", "MSFT", "AMZN", "ORCL", "IBM"],
    "⚡ AI電力_能源": ["VST", "CEG", "ETN", "VRT", "AES", "NRG", "NEE", "PNRG", "GEV", "TLN", "BEP"],
    "🧊 AI散熱_液冷": ["SPXC", "VRT", "ALFVY", "DKILY"],
    "📡 AI網路_光纖": ["GLW", "LUMN", "CIEN", "JNPR", "CSCO", "ANET", "NET", "COHR", "APH", "FICO"],
    "💾 AI儲存_記憶體": ["MU", "NTAP", "PSTG", "WDC", "STX", "SNPX"],
    "📦 AI封裝_CoWoS": ["AMKR", "ASX", "AMAT", "LRCX", "KLAC", "TER", "ONTO", "GFS"],
    "🔐 AI資安_雲端": ["CRWD", "NET", "PANW", "ZS", "S", "OKTA", "FTNT"],
    "🤖 AI軟體_資料": ["PLTR", "SNOW", "DDOG", "MDB", "ESTC", "AI", "SOUN", "PATH"],
    "☁️ AI雲端平台": ["GOOGL", "GOOG", "META", "MSFT", "AMZN"],
    "🏭 AI基礎建設": ["SMNEY", "SIEGY", "ABB", "AOSL", "POWI", "ENPH", "FSLR", "JKS", "NXT", "QS"],
}

def fetch_yahoo(symbol):
    """Fetch stock data from Yahoo Finance using the v8 chart API."""
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1y"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/125.0.0.0'
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        result = data['chart']['result'][0]
        meta = result['meta']
        quote = result.get('indicators', {}).get('quote', [{}])[0]
        closes = quote.get('close', [])
        volumes = quote.get('volume', [])
        highs = quote.get('high', [])
        lows = quote.get('low', [])
        # 52W stats
        valid_highs = [h for h in highs if h is not None]
        valid_lows = [l for l in lows if l is not None]
        high_52w = max(valid_highs) if valid_highs else meta.get('fiftyTwoWeekHigh', 0)
        low_52w = min(valid_lows) if valid_lows else meta.get('fiftyTwoWeekLow', 0)
        current = meta.get('regularMarketPrice', 0)
        # 52W position
        if high_52w > low_52w > 0:
            position_52w = (current - low_52w) / (high_52w - low_52w) * 100
        else:
            position_52w = 50
        # Avg volume
        valid_vols = [v for v in volumes if v is not None]
        avg_volume = sum(valid_vols[-30:]) / 30 if len(valid_vols) >= 30 else (sum(valid_vols) / len(valid_vols) if valid_vols else 0)
        return {
            'symbol': symbol,
            'name': meta.get('longName') or meta.get('shortName', symbol),
            'currency': meta.get('currency', 'USD'),
            'exchange': meta.get('fullExchangeName', ''),
            'price': current,
            'previous_close': meta.get('chartPreviousClose', meta.get('previousClose', 0)),
            'day_high': meta.get('regularMarketDayHigh', 0),
            'day_low': meta.get('regularMarketDayLow', 0),
            'fifty_two_week_high': high_52w,
            'fifty_two_week_low': low_52w,
            'position_52w_pct': round(position_52w, 1),
            'avg_volume_30d': int(avg_volume),
            'market_state': meta.get('marketState', ''),
            'success': True
        }
    except Exception as e:
        return {'symbol': symbol, 'success': False, 'error': str(e)}


def fetch_fundamentals(symbol):
    """Fetch additional fundamental data from Yahoo Finance statistics module."""
    try:
        url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{symbol}?modules=defaultKeyStatistics,summaryDetail,price,financialData"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/125.0.0.0'
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        result = data['quoteSummary']['result'][0]
        def num(metric):
            return metric.get('raw') if metric else None
        ks = result.get('defaultKeyStatistics', {})
        sd = result.get('summaryDetail', {})
        fd = result.get('financialData', {})
        pr = result.get('price', {})
        market_cap = num(pr.get('marketCap'))
        trailing_pe = num(sd.get('trailingPE')) or num(ks.get('trailingPE'))
        forward_pe = num(sd.get('forwardPE')) or num(ks.get('forwardPE'))
        peg = num(ks.get('pegRatio')) or num(sd.get('pegRatio'))
        beta = num(ks.get('beta')) or num(sd.get('beta'))
        roe = num(fd.get('returnOnEquity'))
        gross_margins = num(fd.get('grossMargins'))
        profit_margins = num(fd.get('profitMargins'))
        revenue_growth = num(fd.get('revenueGrowth'))
        earnings_growth = num(fd.get('earningsGrowth'))
        total_revenue = num(fd.get('totalRevenue'))
        total_cash = num(fd.get('totalCash'))
        total_debt = num(fd.get('totalDebt'))
        debt_to_equity = num(fd.get('debtToEquity'))
        current_price = num(fd.get('currentPrice'))
        target_mean = num(fd.get('targetMeanPrice'))
        recommendation = (fd.get('recommendationKey') or '').replace('_', ' ').title()
        return {
            'market_cap': market_cap,
            'trailing_pe': round(trailing_pe, 2) if trailing_pe else None,
            'forward_pe': round(forward_pe, 2) if forward_pe else None,
            'peg': round(peg, 2) if peg else None,
            'beta': round(beta, 2) if beta else None,
            'roe': round(roe * 100, 2) if roe else None,
            'gross_margins': round(gross_margins * 100, 2) if gross_margins else None,
            'profit_margins': round(profit_margins * 100, 2) if profit_margins else None,
            'revenue_growth_pct': round(revenue_growth * 100, 2) if revenue_growth else None,
            'earnings_growth_pct': round(earnings_growth * 100, 2) if earnings_growth else None,
            'total_revenue': total_revenue,
            'total_cash': total_cash,
            'total_debt': total_debt,
            'debt_to_equity': round(debt_to_equity, 2) if debt_to_equity else None,
            'target_mean_price': target_mean,
            'recommendation': recommendation,
            'success': True
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


def main():
    # Collect all unique symbols
    all_symbols = []
    symbol_to_category = {}
    for cat, syms in UNIVERSE.items():
        for s in syms:
            if s not in symbol_to_category:
                symbol_to_category[s] = []
            symbol_to_category[s].append(cat)
            all_symbols.append(s)
    print(f"Total unique symbols: {len(all_symbols)}", file=sys.stderr)

    results = {}
    for i, sym in enumerate(all_symbols):
        sys.stderr.write(f"[{i+1}/{len(all_symbols)}] Fetching {sym}...\n")
        sys.stderr.flush()
        chart = fetch_yahoo(sym)
        fund = fetch_fundamentals(sym) if chart.get('success') else {'success': False}
        results[sym] = {
            'categories': symbol_to_category[sym],
            'chart': chart,
            'fundamentals': fund
        }
        time.sleep(0.3)  # rate limit
    # Write output
    with open('/tmp/yf_data.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"Done. Wrote {len(results)} symbols to /tmp/yf_data.json")
    # Summary
    success = sum(1 for r in results.values() if r['chart'].get('success'))
    print(f"Success: {success}/{len(results)}")


if __name__ == '__main__':
    main()
