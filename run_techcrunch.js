#!/usr/bin/env node
/**
 * TechCrunch 報告生成器
 */
const { spawn } = require('child_process');
const path = require('path');

const WORKDIR = '/home/matt/.openclaw/workspace/stock-reports';
const PY_SCRIPT = path.join(WORKDIR, 'run_techcrunch.py');

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
    console.log('[1/3] 抓取並生成 TechCrunch 報告...');
    try {
        const out = await run('python3', [PY_SCRIPT]);
        console.log(out);
    } catch(e) {
        console.error('  ✗ 報告生成失敗:', e.message);
        throw e;
    }

    console.log('[2/3] Git 提交並推送...');
    const date = new Date().toISOString().slice(0,10);
    const GitEnv = { GIT_TERMINAL_PROMPT: '0', HOME: '/home/matt' };
    
    try {
        await run('git', ['add', 'techcrunch/'], GitEnv);
        const statusOut = await run('git', ['status', '--porcelain'], GitEnv);
        if (!statusOut.trim()) {
            console.log('  → 無變更，跳過提交');
        } else {
            await run('git', ['commit', '-m', `TechCrunch report ${date}`], GitEnv);
            await run('git', ['push', 'https://github.com/acstep/stock-reports.git', 'main'], GitEnv);
            console.log('  ✓ 已推送至 GitHub');
        }
    } catch(e) {
        console.error('  ✗ Git 推送失敗:', e.message);
        throw e;
    }

    console.log('✅ TechCrunch 報告完成');
}

main().catch(err => {
    console.error('FATAL:', err.message);
    process.exit(1);
});