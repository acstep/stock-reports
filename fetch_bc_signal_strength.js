#!/usr/bin/env node
/**
 * Fetch Barchart Top 1% Signal Strength AI-related stocks
 * Broad AI infra filter: chips, memory, storage, networking, power, cooling, security, software, cloud
 */
const puppeteer = require('puppeteer-core');
const fs = require('fs');

const EMAIL = 'MarkConner7735@outlook.com';
const PASSWORD = 'Tech20222@';

// Broad AI infrastructure + SPACE/AEROSPACE/SATELLITES symbols
const AI_SET = new Set([
  // AI CHIPS/GPU/SEMICON
  'NVDA','AMD','AVGO','MRVL','INTC','QCOM','TXN','ADI','MCHP','ON','LSCC','MX','NVTS','TSEM','AMBQ','ARM','IBM',
  // AI MEMORY/STORAGE
  'MU','WDC','SNDK','NTAP','PSTG','SMCI','DELL','HPQ',
  // AI SERVERS/DATACENTER
  'SMCI','DELL','HPQ','ANET','ARISTA','JNPR',
  // AI NETWORKING/FIBER/OPTICAL
  'CIEN','CSCO','ATEN','GLW','LUMN','FTR','VWRE',
  // AI POWER/ENERGY
  'VST','CEG','ETN','PWR','FSLR','AES','NRG','NEE','DUK','SO','D','EXC','XEL','BE','FCEL','NGL','PAA','TRP','PNRG','TUSK',
  // AI COOLING
  'SPXC','VRT',
  // AI PACKAGING
  'AMKR','ASML','AMAT','LRCX',
  // AI SECURITY
  'CRWD','NET','PANW','ZS','OKTA','CY','FTNT','AKAM',
  // AI SOFTWARE/DATA
  'PLTR','SNOW','DLOB','AI','APP','AZPN',
  // AI CLOUD
  'GOOGL','MSFT','AMZN','META',
  // AI ETFs
  'SMH','SOXX','XSD','IGV','HACK','CIBR',
  // OTHERS
  'KEYS','ENPH','SEDG','RUN','SPWR',
]);

// Space/Aerospace/Satellite symbols
const SPACE_SET = new Set([
  'RKLB','LUNR','BKSY','PL','SATL',
  'SPCE','VACN','HOOK','LIDA','ASTR','NPA','GOT','GFARR','RDW',
  'MAXR','AIRI','ATCX','LMAC','RCRTF','LDHA','VTOL','AVT',
]);

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
    if (req.url().includes('signals_ratings')) xsrfToken = req.headers()['x-xsrf-token'] || '';
  });

  await page.goto('https://www.barchart.com/login', {waitUntil: 'networkidle2', timeout: 30000});
  await new Promise(r => setTimeout(r, 2000));
  await page.type('input[name="email"]', EMAIL, {delay: 80});
  await page.type('input[name="password"]', PASSWORD, {delay: 80});
  await page.click('button[type="submit"]');
  await new Promise(r => setTimeout(r, 6000));

  const cookies = await page.cookies();
  const cookieStr = cookies.map(c => `${c.name}=${c.value}`).join('; ');

  await page.goto('https://www.barchart.com/stocks/signals/direction-strength?viewName=main&orderBy=symbol&orderDir=asc&page=all', {waitUntil: 'networkidle2', timeout: 30000});
  await new Promise(r => setTimeout(r, 8000));

  const result = await page.evaluate(async (token, cookies) => {
    const res = await fetch('https://www.barchart.com/proxies/core-api/v1/quotes/get?lists=stocks.us.signals_ratings.v2_top_signal_strength&orderDir=asc&fields=symbol%2CsymbolName%2ClastPrice%2CpriceChange%2CpercentChange%2Copinion%2CopinionPrevious%2CopinionLastWeek%2CopinionLastMonth%2CsymbolCode%2CsymbolType%2ChasOptions&orderBy=symbol&meta=field.shortName%2Cfield.type%2Cfield.description%2Clists.lastUpdate&hasOptions=true&raw=1', {
      headers: {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.barchart.com/', 'Cookie': cookies, 'X-Xsrf-Token': token, 'Accept': 'application/json'}
    });
    return res.json();
  }, xsrfToken, cookieStr);

  const allRows = result.data || [];
  
  const aiRows = allRows.filter(r => AI_SET.has(r.symbol) || SPACE_SET.has(r.symbol));
  
  console.log(`Found ${aiRows.length} AI-related Top Signal Strength stocks:`);
  aiRows.forEach(r => {
    console.log(`  ${r.symbol} | ${r.symbolName} | $${r.lastPrice} | ${r.percentChange} | ${r.opinion}`);
  });
  
  fs.writeFileSync('/tmp/bc_signal_ai.json', JSON.stringify(aiRows, null, 2));
  console.log(`Written ${aiRows.length} stocks to /tmp/bc_signal_ai.json`);
  
  await browser.close();
})().catch(e => { console.error('ERROR:', e.message); process.exit(1); });