#!/usr/bin/env node
/**
 * Fetch Barchart Top-Bottom Signals main view
 */
const puppeteer = require('puppeteer-core');
const fs = require('fs');

const EMAIL = 'MarkConner7735@outlook.com';
const PASSWORD = 'Tech20222@';

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/google-chrome-stable',
    headless: true,
    args: ['--no-sandbox','--disable-setuid-sandbox','--disable-dev-shm-usage','--disable-gpu','--single-process']
  });
  const page = await browser.newPage();
  await page.setViewport({width: 1400, height: 900});
  await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36');

  let xsrfToken = '';
  page.on('request', req => {
    if (req.url().includes('signals_ratings') || req.url().includes('quotes/get')) xsrfToken = req.headers()['x-xsrf-token'] || '';
  });

  await page.goto('https://www.barchart.com/login', {waitUntil: 'networkidle2', timeout: 30000});
  await new Promise(r => setTimeout(r, 2000));
  await page.type('input[name="email"]', EMAIL, {delay: 80});
  await page.type('input[name="password"]', PASSWORD, {delay: 80});
  await page.click('button[type="submit"]');
  await new Promise(r => setTimeout(r, 6000));

  const cookies = await page.cookies();
  const cookieStr = cookies.map(c => `${c.name}=${c.value}`).join('; ');

  // Visit the URL specified in the task
  await page.goto('https://www.barchart.com/stocks/signals/top-bottom?viewName=main&orderBy=symbol&orderDir=asc', {waitUntil: 'networkidle2', timeout: 30000});
  await new Promise(r => setTimeout(r, 8000));

  // Try multiple API endpoints to get a comprehensive list
  const allData = await page.evaluate(async (token, cookies) => {
    const endpoints = [
      'https://www.barchart.com/proxies/core-api/v1/quotes/get?lists=stocks.us.signals_ratings.v2_top_signal_strength&orderDir=asc&fields=symbol%2CsymbolName%2ClastPrice%2CpriceChange%2CpercentChange%2Copinion%2CsymbolCode%2CsymbolType%2ChasOptions&orderBy=symbol&meta=field.shortName%2Cfield.type%2Cfield.description%2Clists.lastUpdate&hasOptions=true&raw=1',
      'https://www.barchart.com/proxies/core-api/v1/quotes/get?lists=stocks.us.signals_ratings.v2_top_signal_strength&orderDir=desc&fields=symbol%2CsymbolName%2ClastPrice%2CpriceChange%2CpercentChange%2Copinion%2CsymbolCode%2CsymbolType%2ChasOptions&orderBy=percentChange&meta=field.shortName%2Cfield.type%2Cfield.description%2Clists.lastUpdate&hasOptions=true&raw=1',
      'https://www.barchart.com/proxies/core-api/v1/quotes/get?lists=stocks.us.signals_ratings.v2_bottom_signal_strength&orderDir=asc&fields=symbol%2CsymbolName%2ClastPrice%2CpriceChange%2CpercentChange%2Copinion%2CsymbolCode%2CsymbolType%2ChasOptions&orderBy=symbol&meta=field.shortName%2Cfield.type%2Cfield.description%2Clists.lastUpdate&hasOptions=true&raw=1',
      'https://www.barchart.com/proxies/core-api/v1/quotes/get?lists=stocks.us.signals_ratings.v2_bottom_signal_strength&orderDir=asc&fields=symbol%2CsymbolName%2ClastPrice%2CpriceChange%2CpercentChange%2Copinion%2CsymbolCode%2CsymbolType%2ChasOptions&orderBy=percentChange&meta=field.shortName%2Cfield.type%2Cfield.description%2Clists.lastUpdate&hasOptions=true&raw=1',
    ];
    const results = {};
    for (const url of endpoints) {
      try {
        const res = await fetch(url, {
          headers: {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.barchart.com/', 'Cookie': cookies, 'X-Xsrf-Token': token, 'Accept': 'application/json'}
        });
        const j = await res.json();
        const key = url.match(/v2_\w+/)[0];
        results[key] = j.data || [];
      } catch(e) { results['err_' + url.substring(60, 90)] = e.message; }
    }
    return results;
  }, xsrfToken, cookieStr);

  const allRows = [
    ...(allData.v2_top_signal_strength || []),
    ...(allData.v2_bottom_signal_strength || []),
  ];
  
  // Dedupe by symbol
  const seen = new Set();
  const unique = [];
  for (const r of allRows) {
    if (!seen.has(r.symbol)) {
      seen.add(r.symbol);
      unique.push(r);
    }
  }
  
  console.log(`Total unique: ${unique.length}`);
  fs.writeFileSync('/tmp/bc_signals_main.json', JSON.stringify(unique, null, 2));
  console.log('Saved to /tmp/bc_signals_main.json');
  console.log('First 30 symbols:', unique.slice(0, 30).map(r => r.symbol).join(', '));
  
  await browser.close();
})().catch(e => { console.error('ERROR:', e.message); process.exit(1); });
