#!/usr/bin/env python3
"""Fetch live Yahoo Finance prices for Barchart Signal Strength AI stocks"""
import urllib.request, json, re, sys, time

# AI stocks from Barchart Signal Strength
AI_SIG_SYMBOLS = ['AMBQ', 'AMD', 'ARM', 'ATEN', 'BE', 'CIEN', 'CSCO', 'LSCC', 'MU', 'MX', 'NVTS', 'ON', 'TSEM']

# Additional AI infrastructure stocks to include
EXTRA_SYMBOLS = ['NVDA', 'AVGO', 'SMCI', 'VST', 'CEG', 'GLW', 'LUMN', 'AMKR', 'SPXC', 'CRWD', 'NET', 'PLTR', 'ETN', 'ENPH']

ALL_SYMBOLS = list(dict.fromkeys(AI_SIG_SYMBOLS + EXTRA_SYMBOLS))

print(f'Fetching prices for {len(ALL_SYMBOLS)} symbols...')

results = {}
# Process in batches of 5 to avoid rate limits
BATCH_SIZE = 5
for i in range(0, len(ALL_SYMBOLS), BATCH_SIZE):
    batch = ALL_SYMBOLS[i:i+BATCH_SIZE]
    for sym in batch:
        try:
            url = f'https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=5d'
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                d = json.loads(resp.read())
                r = d['chart']['result'][0]
                meta = r['meta']
                curr = meta.get('regularMarketPrice')
                prev = meta.get('chartPreviousClose') or meta.get('previousClose', {}).get('raw')
                chg = round((curr - prev) / prev * 100, 2) if prev and curr else 0
                high52 = meta.get('fiftyTwoWeekHigh')
                low52 = meta.get('fiftyTwoWeekLow')
                from_low = round((curr - low52) / low52 * 100, 1) if low52 and curr else None
                results[sym] = {
                    'price': curr,
                    'change_pct': chg,
                    'high52': high52,
                    'low52': low52,
                    'mktcap': meta.get('marketCap'),
                    'pe': meta.get('trailingPE'),
                    'eps': meta.get('trailingEps'),
                    'volume': meta.get('regularMarketVolume'),
                    'name': meta.get('shortName', sym),
                    'from_low_pct': from_low,
                }
                print(f'  {sym}: ${curr} ({chg:+.2f}%) from_low={from_low}%')
        except Exception as e:
            print(f'  {sym}: ERROR {e}')
    # Delay between batches to avoid rate limits
    if i + BATCH_SIZE < len(ALL_SYMBOLS):
        time.sleep(1.0)

with open('/tmp/signal_live_prices.json', 'w') as f:
    json.dump(results, f, indent=2)
print(f'Saved {len(results)} stocks to /tmp/signal_live_prices.json')