const CRED = require('/home/matt/.openclaw/workspace/.credentials.js');
const puppeteer = require('puppeteer-core');

const EMAIL = CRED.barchart.email;
const PASSWORD = CRED.barchart.password;

async function fetchStock(page, symbol) {
  const url = `https://www.barchart.com/stocks/quotes/${symbol}/overview`;
  try {
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 20000 });
    await new Promise(r => setTimeout(r, 4000));
    const data = await page.evaluate(() => {
      return { _raw: document.body?.innerText.substring(0, 8000) || '' };
    });
    return { symbol, ...data, success: true };
  } catch(e) {
    return { symbol, error: e.message, success: false };
  }
}

async function main() {
  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/google-chrome-stable',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--single-process']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 900 });
  await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36');

  await page.goto('https://www.barchart.com/login', { waitUntil: 'networkidle2', timeout: 30000 });
  await new Promise(r => setTimeout(r, 2000));
  await page.type('input[name="email"]', EMAIL, { delay: 80 });
  await page.type('input[name="password"]', PASSWORD, { delay: 80 });
  await page.click('button[type="submit"]');
  await new Promise(r => setTimeout(r, 6000));
  process.stderr.write(`Post-login URL: ${page.url()}\n`);

  const symbols = ['NVDA', 'AMD', 'MU', 'SMCI', 'AVGO', 'NET', 'CRWD', 'VST', 'ENPH'];
  const results = [];
  for (const sym of symbols) {
    process.stderr.write(`Fetching ${sym}...\n`);
    const r = await fetchStock(page, sym);
    results.push(r);
    await new Promise(r => setTimeout(r, 2500));
  }
  
  const fs = require('fs');
  fs.writeFileSync('/tmp/bc_raw_data.json', JSON.stringify(results, null, 2));
  console.log('Results written to /tmp/bc_raw_data.json');
  await browser.close();
}

main().catch(err => { console.error('ERROR:', err.message); process.exit(1); });