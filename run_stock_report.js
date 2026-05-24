#!/usr/bin/env node
/**
 * AI 美股研究報告生成器
 * 使用內建備用數據直接生成報告
 */
const { spawn } = require('child_process');
const path = require('path');

const WORKDIR = '/home/matt/.openclaw/workspace/stock-reports';
const PY_SCRIPT = path.join(WORKDIR, 'generate_full_report.py');

function run(cmd, args, env = {}) {
    return new Promise((resolve, reject) => {
        const opts = { cwd: WORKDIR, stdio: 'pipe', env: { ...process.env, ...env } };
        const child = spawn(cmd, args, opts);
        let out = '', err = '';
        child.stdout.on('data', d => out += d.toString());
        child.stderr.on('data', d => err += d.toString());
        child.on('close', code => code === 0 ? resolve(out) : reject(new Error(`Exit ${code}: ${err||out}`)));
    });
}

async function main() {
    console.log('[1/4] 抓取 Barchart Top 1% Signal Strength AI 股票...');
    try {
        await run('node', [path.join(WORKDIR, 'fetch_bc_signal_strength.js')], { cwd: WORKDIR });
        console.log('  ✓ Signal Strength 數據已更新');
    } catch(e) {
        console.error('  ⚠ Signal Strength 抓取失敗:', e.message);
    }

    console.log('[2/4] 生成 HTML 報告...');
    try {
        const out = await run('python3', [PY_SCRIPT]);
        if (out.includes('Ranked stocks')) {
            const lines = out.split('\n').filter(l => l.trim().match(/^#\d+/));
            lines.slice(0,5).forEach(l => console.log(' ', l.trim()));
        }
        console.log('  ✓ HTML 報告生成完成');
    } catch(e) {
        console.error('  ✗ Python 生成失敗:', e.message);
        throw e;
    }

    console.log('[2/3] Git 提交並推送...');
    const date = new Date().toISOString().slice(0,10);
    const GitEnv = { 
        GIT_TERMINAL_PROMPT: '0',
        HOME: '/home/matt'
    };
    
    try {
        await run('git', ['add', '.'], GitEnv);
        const statusOut = await run('git', ['status', '--porcelain'], GitEnv);
        if (!statusOut.trim()) {
            console.log('  → 無變更，跳過提交');
        } else {
            await run('git', ['commit', '-m', `Stock report ${date}`], GitEnv);
            // Use credential helper via netrc
            await run('git', ['push', 'https://github.com/acstep/stock-reports.git', 'main'], GitEnv);
            console.log('  ✓ 已推送至 GitHub');
        }
    } catch(e) {
        console.error('  ✗ Git 推送失敗:', e.message);
        throw e;
    }

    console.log('✅ 美股報告完成');
}

main().catch(err => {
    console.error('FATAL:', err.message);
    process.exit(1);
});