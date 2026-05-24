#!/usr/bin/env node
/**
 * Fetch ALL Barchart Top 1% Signal Strength stocks
 * AI analysis will be done in Python to dynamically identify AI/Space related stocks
 */
const puppeteer = require('puppeteer-core');
const fs = require('fs');

const EMAIL = 'MarkConner7735@outlook.com';
const PASSWORD = '***';

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
  console.log(`Fetched ALL ${allRows.length} Signal Strength stocks`);
  
  // Save ALL stocks - AI analysis done in Python
  fs.writeFileSync('/tmp/bc_signal_all.json', JSON.stringify(allRows, null, 2));
  console.log('Saved to /tmp/bc_signal_all.json');
  
  // Also keep the ai_filtered version for backwards compat
  const AI_KEYWORDS = ['ai','artificial','machine learning','semicon','chip','gpu','memory','data center','cloud','cyber','security','network','fiber','optical','power','energy','cooling','robot','sensor','automation','software','serv','nvidia','amd','micron','broadcom','qualcomm','intel','marvell','lattice','navitas','tower semi','magnachip','ambiq','arm','cisco','arista','juniper','ciena','lumen','corning','a10','on semi','bloom energy','energy','power','cool','heat','battery','nuclear','solar','wind','fuel cell','datacenter','storage','ssd','hdd','nand','dram','hyperscale','rocket','space','satellite','aero','launch','orbital','leo','moon','aerospace','planet lab','blacksky','satellogic'];
  const SPACE_SYM = new Set(['RKLB','LUNR','BKSY','PL','SATL','SPCE','VACN','HOOK','LIDA','ASTR','NPA','GOT','GFARR','RDW','MAXR','AIRI','ATCX','LMAC','RCRTF','LDHA','VTOL','AVT']);
  
  const aiRows = allRows.filter(r => {
    const name = (r.symbolName || '').toLowerCase();
    return AI_KEYWORDS.some(k => name.includes(k)) || SPACE_SYM.has(r.symbol);
  });
  
  fs.writeFileSync('/tmp/bc_signal_ai.json', JSON.stringify(aiRows, null, 2));
  console.log(`AI/Space filter found ${aiRows.length} stocks`);
  aiRows.forEach(r => console.log(`  ${r.symbol} | ${r.symbolName}`));
  
  await browser.close();
})().catch(e => { console.error('ERROR:', e.message); process.exit(1); });