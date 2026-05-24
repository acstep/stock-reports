#!/usr/bin/env node
/**
 * Fetch Barchart Top 1% Signal Strength AI-related stocks
 * Sets up auth via puppeteer then calls API, saves to /tmp/bc_signal_ai.json
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
  await page.setViewport({width: 1280, height: 900});
  await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36');

  let xsrfToken = '';
  page.on('request', req => {
    if (req.url().includes('signals_ratings')) {
      xsrfToken = req.headers()['x-xsrf-token'] || '';
    }
  });

  // Login
  await page.goto('https://www.barchart.com/login', {waitUntil: 'networkidle2', timeout: 30000});
  await new Promise(r => setTimeout(r, 2000));
  await page.type('input[name="email"]', EMAIL, {delay: 80});
  await page.type('input[name="password"]', PASSWORD, {delay: 80});
  await page.click('button[type="submit"]');
  await new Promise(r => setTimeout(r, 6000));

  const cookies = await page.cookies();
  const cookieStr = cookies.map(c => `${c.name}=${c.value}`).join('; ');

  // Trigger signal strength page to get token
  await page.goto('https://www.barchart.com/stocks/signals/direction-strength?viewName=main&orderBy=symbol&orderDir=asc&page=all', {waitUntil: 'networkidle2', timeout: 30000});
  await new Promise(r => setTimeout(r, 8000));

  if (!xsrfToken) {
    // Try to extract token from cookie or page
    const pageContent = await page.content();
    const tokenMatch = pageContent.match(/xsrf-token["\s>]+([^"<]+)/i);
    if (tokenMatch) xsrfToken = tokenMatch[1];
  }

  if (!xsrfToken) {
    console.error('Could not get XSRF token');
    process.exit(1);
  }

  const apiUrl = 'https://www.barchart.com/proxies/core-api/v1/quotes/get?lists=stocks.us.signals_ratings.v2_top_signal_strength&orderDir=asc&fields=symbol%2CsymbolName%2ClastPrice%2CpriceChange%2CpercentChange%2Copinion%2CopinionPrevious%2CopinionLastWeek%2CopinionLastMonth%2CsymbolCode%2CsymbolType%2ChasOptions&orderBy=symbol&meta=field.shortName%2Cfield.type%2Cfield.description%2Clists.lastUpdate&hasOptions=true&raw=1';

  const result = await page.evaluate(async (url, token, cookies) => {
    const res = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36',
        'Referer': 'https://www.barchart.com/stocks/signals/direction-strength',
        'Cookie': cookies,
        'X-Xsrf-Token': token,
        'Accept': 'application/json'
      }
    });
    return res.json();
  }, apiUrl, xsrfToken, cookieStr);

  const allRows = result.data || [];
  
  // AI infrastructure symbols
  const aiSigSet = new Set(['AMD','ARM','AVGO','NVDA','SMCI','MU','CSCO','ON','LSCC','MX','NVTS','TSEM','AMBQ','CIEN','ATEN','BE','KEYS','PWR','FSLR','SPXC','GLW','ENPH','VST','AMKR','CRWD','NET','PLTR','SWKS','QRVO','LRCX','AMAT','ASML']);
  
  const aiRows = allRows.filter(r => aiSigSet.has(r.symbol));
  
  fs.writeFileSync('/tmp/bc_signal_ai.json', JSON.stringify(aiRows, null, 2));
  console.log('Written', aiRows.length, 'AI stocks to /tmp/bc_signal_ai.json');
  
  await browser.close();
})().catch(e => { console.error('ERROR:', e.message); process.exit(1); });