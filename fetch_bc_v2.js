const puppeteer = require('puppeteer-core');
const fs = require('fs');

const EMAIL = 'MarkConner7735@outlook.com';
const PASSWORD = 'Tech20222@';

async function main() {
  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/google-chrome-stable',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--single-process']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1400, height: 900 });
  await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36');

  // Login
  process.stderr.write('Logging in...\n');
  await page.goto('https://www.barchart.com/login', { waitUntil: 'networkidle2', timeout: 30000 });
  await new Promise(r => setTimeout(r, 2000));
  await page.type('input[name="email"]', EMAIL, { delay: 80 });
  await page.type('input[name="password"]', PASSWORD, { delay: 80 });
  await page.click('button[type="submit"]');
  await new Promise(r => setTimeout(r, 8000));

  // Try multiple Barchart signal/leaderboard pages
  const pages_to_try = [
    'https://www.barchart.com/stocks/signals/top-bottom?viewName=main&orderBy=symbol&orderDir=asc',
    'https://www.barchart.com/stocks/signals/buy?viewName=main&orderBy=signalsRating&orderDir=desc',
    'https://www.barchart.com/stocks/signals/sell?viewName=main&orderBy=signalsRating&orderDir=desc',
  ];

  let allSymbols = [];
  for (const url of pages_to_try) {
    process.stderr.write(`\n=== ${url} ===\n`);
    try {
      await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
      await new Promise(r => setTimeout(r, 6000));
      // Try to interact with grid/table
      const symbols = await page.evaluate(() => {
        const out = [];
        // Find all anchor elements that look like stock symbols
        document.querySelectorAll('a').forEach(a => {
          const href = a.getAttribute('href') || '';
          const txt = a.innerText.trim();
          if (href.includes('/stocks/quotes/') && /^[A-Z][A-Z\.\-]{0,5}$/.test(txt)) {
            out.push(txt);
          }
        });
        // Also try table rows
        document.querySelectorAll('tr, [role="row"]').forEach(row => {
          const cells = row.querySelectorAll('td, [role="gridcell"]');
          if (cells.length > 3) {
            const first = cells[0]?.innerText?.trim();
            if (first && /^[A-Z][A-Z\.\-]{0,5}$/.test(first) && !out.includes(first)) {
              out.push(first);
            }
          }
        });
        return [...new Set(out)];
      });
      process.stderr.write(`Found ${symbols.length} symbols\n`);
      if (symbols.length > 0) {
        process.stderr.write(`First: ${symbols.slice(0, 30).join(', ')}\n`);
        allSymbols = [...new Set([...allSymbols, ...symbols])];
      }
    } catch (e) {
      process.stderr.write(`Error: ${e.message}\n`);
    }
  }
  
  // Also visit symbol pages to get Barchart signal strength for AI infrastructure stocks
  const aiSymbols = ['NVDA', 'AMD', 'MU', 'SMCI', 'AVGO', 'NET', 'CRWD', 'VST', 'CEG', 'VRT', 'ANET', 'ENPH', 'FSLR', 'PLTR', 'SNOW', 'META', 'GOOGL', 'AMZN', 'MSFT', 'TSM', 'ASML', 'AMAT', 'LRCX', 'KLAC', 'COHR', 'APH', 'PANW', 'ZS', 'OKTA', 'DDOG', 'MRVL', 'ARM', 'QCOM', 'INTC', 'DELL', 'HPQ', 'ORCL', 'IBM', 'TLN', 'GEV', 'ETN', 'PNRG', 'NRG', 'AES', 'NEE', 'AOSL', 'POWI', 'GFS', 'TER', 'ONTO', 'CIEN', 'CSCO', 'JNPR', 'GLW', 'LUMN', 'STX', 'WDC', 'NTAP', 'PSTG', 'AMKR', 'ASX', 'FTNT', 'MDB', 'ESTC', 'AI', 'SOUN', 'PATH'];
  const signalData = {};
  for (const sym of aiSymbols) {
    try {
      await page.goto(`https://www.barchart.com/stocks/quotes/${sym}/overview`, { waitUntil: 'networkidle2', timeout: 20000 });
      await new Promise(r => setTimeout(r, 2500));
      const data = await page.evaluate(() => {
        const text = document.body.innerText;
        // Extract key fields
        const get = (re) => {
          const m = text.match(re);
          return m ? m[1].trim() : null;
        };
        const priceMatch = text.match(/Last Price[^\d\-]+([\d,]+\.\d+)/i) || text.match(/Last Sale[^\d\-]+([\d,]+\.\d+)/i);
        const high52w = text.match(/52W High[^\d\-]+([\d,]+\.\d+)/i);
        const low52w = text.match(/52W Low[^\d\-]+([\d,]+\.\d+)/i);
        const signal = text.match(/Barchart Opinion[^\d]*(\d+)/i) || text.match(/Signal Strength[^\d]*(\d+)/i);
        return {
          price: priceMatch ? priceMatch[1] : null,
          high_52w: high52w ? high52w[1] : null,
          low_52w: low52w ? low52w[1] : null,
          signal: signal ? signal[1] : null
        };
      });
      signalData[sym] = data;
      process.stderr.write(`${sym}: ${JSON.stringify(data)}\n`);
    } catch (e) {
      signalData[sym] = { error: e.message };
    }
  }

  fs.writeFileSync('/tmp/bc_v2_data.json', JSON.stringify({ allSymbols, signalData }, null, 2));
  console.log(`Total symbols from lists: ${allSymbols.length}`);
  console.log(`AI symbols with signal data: ${Object.keys(signalData).length}`);
  await browser.close();
}

main().catch(err => { console.error('ERROR:', err.message); process.exit(1); });
