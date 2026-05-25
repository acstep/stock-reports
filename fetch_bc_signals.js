const puppeteer = require('puppeteer-core');
const fs = require('fs');

const EMAIL = 'MarkConner7735@outlook.com';
const PASSWORD = 'Tech20222@';
// Try Top Signal Strength page
const SIGNAL_URL = 'https://www.barchart.com/stocks/signals/top-bottom?viewName=main&orderBy=signalsRating&orderDir=desc';

async function main() {
  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/google-chrome-stable',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--single-process']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1400, height: 900 });
  await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36');

  // Step 1: Login
  process.stderr.write('Logging into Barchart...\n');
  await page.goto('https://www.barchart.com/login', { waitUntil: 'networkidle2', timeout: 30000 });
  await new Promise(r => setTimeout(r, 3000));
  await page.type('input[name="email"]', EMAIL, { delay: 80 }).catch(async () => {
    await page.type('input[type="email"]', EMAIL, { delay: 80 });
  });
  await page.type('input[name="password"]', PASSWORD, { delay: 80 }).catch(async () => {
    await page.type('input[type="password"]', PASSWORD, { delay: 80 });
  });
  await page.click('button[type="submit"]').catch(() => {});
  await new Promise(r => setTimeout(r, 8000));
  process.stderr.write(`After login URL: ${page.url()}\n`);

  // Step 2: Go to signal strength page
  process.stderr.write('Navigating to signals page...\n');
  await page.goto(SIGNAL_URL, { waitUntil: 'networkidle2', timeout: 30000 });
  await new Promise(r => setTimeout(r, 6000));

  // Debug: try to find data grids
  const debugInfo = await page.evaluate(() => {
    // Check for various table/data patterns
    const allTables = document.querySelectorAll('table');
    const divs = document.querySelectorAll('[class*="data"], [class*="table"], [class*="grid"]');
    const spans = document.querySelectorAll('span[class*="symbol"], a[class*="symbol"]');
    const symbolLinks = [];
    document.querySelectorAll('a[href*="/stocks/quotes/"]').forEach(a => {
      const href = a.getAttribute('href');
      const text = a.innerText.trim();
      if (text && /^[A-Z\.\-]+$/.test(text) && text.length <= 6) {
        symbolLinks.push({ text, href });
      }
    });
    return {
      tableCount: allTables.length,
      tableClasses: Array.from(allTables).map(t => t.className),
      divCount: divs.length,
      divClasses: Array.from(divs).slice(0, 5).map(d => d.className),
      spanCount: spans.length,
      symbolLinkCount: symbolLinks.length,
      symbolLinks: symbolLinks.slice(0, 50),
      bodyTextSnippet: document.body.innerText.substring(0, 5000),
    };
  });

  process.stderr.write(`Tables: ${debugInfo.tableCount}\n`);
  process.stderr.write(`Symbol links found: ${debugInfo.symbolLinkCount}\n`);
  if (debugInfo.symbolLinks.length > 0) {
    process.stderr.write(`First symbols: ${debugInfo.symbolLinks.slice(0,30).map(s=>s.text).join(', ')}\n`);
  }
  process.stderr.write(`Body snippet:\n${debugInfo.bodyTextSnippet.substring(0, 3000)}\n`);

  fs.writeFileSync('/tmp/bc_signals_debug.json', JSON.stringify(debugInfo, null, 2));
  console.log(JSON.stringify({ success: true, symbols: debugInfo.symbolLinks.slice(0,50).map(s=>s.text) }));
  await browser.close();
}

main().catch(err => { console.error('ERROR:', err.message); process.exit(1); });