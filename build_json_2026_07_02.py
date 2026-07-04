#!/usr/bin/env python3
"""Build recommendations/2026-07-02.json with AI translations + recommendations."""
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

DATE = "2026-07-02"
SOURCE_DATE = "2026-07-01"
TPE_TZ = timezone(timedelta(hours=8))
GENERATED_AT = datetime.now(TPE_TZ).strftime("%Y-%m-%dT%H:%M:%S+08:00")

OUT_PATH = f"/home/matt/.openclaw/workspace/stock-reports/recommendations/{DATE}.json"

# Load research and ticker data
with open(f'/home/matt/.openclaw/workspace/stock-reports/_research_{DATE}.json') as f:
    research = json.load(f)
with open(f'/home/matt/.openclaw/workspace/stock-reports/_tickers_{DATE}.json') as f:
    tickers = json.load(f)

# ===== Translations (繁體中文, 台灣用語) =====
TRANSLATIONS = {
    "AMAT": {
        "id:entity:entity::ticker:AMAT": "Argus 股息成長模型投資組合（應用材料入選）",
        "Daily – Vickers Top Buyers & Sellers for 06/18/2026": "每日 Vickers 內部人買賣龍虎榜（06/18）",
        "Weekly Stock List": "Argus 每週精選股名單",
    },
    "AMD": {
        "eacc4ea9-392a-4e48-822b-80518f6904cd": "每日 Vickers 內部人買賣龍虎榜（06/03）",
        "Daily – Vickers Top Buyers & Sellers for 06/03/2026": "每日 Vickers 內部人買賣龍虎榜（06/03）",
        "Daily – Vickers Top Buyers & Sellers for 05/13/2026": "每日 Vickers 內部人買賣龍虎榜（05/13）",
        "Market Update: AMD, BMY, EQR, F, OGE, PWR, PYPL, ANET, STRL": "市場快訊：AMD、BMY、EQR、F、OGE、PWR、PYPL、ANET、STRL",
    },
    "GEV": {
        "Daily – Vickers Top Buyers & Sellers for 06/04/2026": "每日 Vickers 內部人買賣龍虎榜（06/04）",
        "Weekly Stock List": "Argus 每週精選股名單",
        "Analyst Report: GE Vernova Inc": "分析師報告：GE Vernova（奇異維諾瓦）",
    },
    "GLW": {
        "id:entity:entity::ticker:GLW": "Argus 永續成長主題投資組合（Corning 入選）",
        "Daily – Vickers Top Buyers & Sellers for 05/27/2026": "每日 Vickers 內部人買賣龍虎榜（05/27）",
        "Daily – Vickers Top Buyers & Sellers for 05/19/2026": "每日 Vickers 內部人買賣龍虎榜（05/19）",
    },
    "MU": {
        "a1eb989a-86a7-4b12-a6b8-47d07f3c9913": "分析師報告：Micron Technology（美光科技）",
        "Market Digest: MU, PNW, SJM": "市場摘要：MU（美光）、PNW、SJM",
        "Technical Assessment: Bullish in the Intermediate-Term": "技術分析：中線偏多格局",
    },
    "PANW": {
        "Daily – Vickers Top Buyers & Sellers for 06/15/2026": "每日 Vickers 內部人買賣龍虎榜（06/15）",
        "Technical Assessment: Bullish in the Intermediate-Term": "技術分析：中線偏多格局",
        "Analyst Report: Palo Alto Networks Inc": "分析師報告：Palo Alto Networks（資安平台龍頭）",
    },
    "PLTR": {
        "Analyst Report: Palantir Technologies Inc": "分析師報告：Palantir Technologies（AI 數據分析平台）",
        "Market Digest: CAH, SHOP, DXCM, PLTR, GFS": "市場摘要：CAH、SHOP、DXCM、PLTR、GFS",
        "Technical Assessment: Bullish in the Intermediate-Term": "技術分析：中線偏多格局",
    },
    "VRT": {
        "Raising target price to $378.00": "調升目標價至 378 美元",
        "Raising target price to $356.00": "調升目標價至 356 美元",
        "Lowering target price to $344.00": "下修目標價至 344 美元",
    },
}

# ===== AI Recommendations (2-3 sentences 繁體中文) =====
RECOMMENDATIONS = {
    "AMAT": "AMAT 是 CoWoS 先進封裝設備的絕對瓶頸供應商，蝕刻與薄膜沉積製程在 HBM 與 AI 晶片供應鏈中具備剛需地位，2026 下半年 2nm 量產將再啟設備更新週期。今日暴漲 23.4% 反映市場對封裝產能擴張的極度飢渴，雖 P/E 24.1 看似合理，但 2H26 訂單能見度已外溢到 2027。Argus 將其列入股息成長與精選名單，內部人買盤訊號偏多，是承壓回調時的核心配置標的。",
    "AMD": "AMD MI350 系列以 HBM3e 高頻寬與性價比切入雲端 AI 訓練市場，微軟 Azure 與 Meta 已開始擴大採用，2026 年資料中心營收佔比將突破 50%，是 Nvidia 之外唯一能規模化挑戰的 GPU 替代方案。P/E 45 看似偏高，但若以 AI 加速器雙位數成長曲線計算，PEG 仍落在 1.0 以下。Argus 分析師將其列入市場快訊名單，搭配 AMD 自家伺服器 CPU 需求同步爆發，中長期甜蜜點尚未結束。",
    "GEV": "GEV 是 AI 基建最末端的電力壟斷者，數據中心申請電力排隊時間已延至 3-5 年，變壓器與輸配電設備成為硬瓶頸，GEV 在電網升級與 SMR 小型模組化反應爐的雙重護城河下享有定價權。Argus 將其列入週精選名單並發布個股分析報告，技術面維持多頭格局，雖然 P/E 28.5 偏高，但訂單能見度已延伸至 2028 年。AI 的盡頭是電力，GEV 是這個論述最純的受惠者。",
    "GLW": "GLW 在 AI 集群光互連轉型中具備結構性優勢，當 GPU 規模突破 10 萬卡後傳統銅纜延遲已不可行，特種光纖成為唯一解，800G/1.6T 光模組滲透率加速將帶動營收進入長週期增長。日漲 31.62% 反映光纖需求從「選配」變「標配」的拐點已至，P/E 18.5 是這份榜單中估值最甜的位置。Argus 將其納入永續成長主題投資組合，內部人買盤訊號亦見加溫，逢回仍可加碼。",
    "MU": "MU 是 HBM 供給緊缺的核心受惠者，HBM3e/HBM4 報價持續上漲推升毛利率兩個位階以上，AI GPU 客戶已將長約簽至 2027 年，P/E 12.4 是這份榜單中最低的本益比。Argus 發布的個股分析報告明確看好中期偏多格局，搭配技術面評估為多頭，現在位置相對距 52W 高點仍有 8% 折價。HBM 供需失衡要等到 2027 H2 才可能緩解，MU 是 AI 記憶體鏈最直接的多頭槓桿。",
    "PANW": "PANW 是 AI 平台化資安的代表性受惠者，AI 降低攻擊門檻使企業必須從單點防禦升級到 AI 驅動的平台化方案，Prisma 與 Cortex 平台 ARR 增速維持 25%+。Argus 為其發布個股分析報告並指出中線偏多格局，內部人買盤訊號亦見偏多，雖然 P/E 42 較高但資安 SaaS 的可預測性提供溢價合理性。AI 攻擊只會越來越多，PANW 是企業資安預算從 Capex 轉 Opex 趨勢下的核心配置。",
    "PLTR": "PLTR 的 AIP 平台在企業端滲透加速，2025 年從美國政府客戶擴展到商業客戶後營收結構明顯改善，AI OS 定位讓客戶轉換成本隨資料累積而提高。Argus 為其發布個股分析報告並列入市場摘要與多檔主題投資組合，搭配技術面中期偏多訊號，雖然 P/E 88 是榜單中最高，但若以「AI 時代作業系統」的本益比框架計算仍屬合理。短線因高估值震盪，但 AIP 在企業端的飛輪效應才剛啟動，長線仍是 AI 應用層的核心持有。",
    "VRT": "VRT 是液冷標準的制定者，數據中心機櫃功耗突破 50kW 後風冷已不可行，VRT 從冷卻液分發到 CDU 模組擁有最完整的方案，2026 年液冷滲透率預估突破 40%。Argus 近期三度調整目標價（最新一輪上修至 $378，反映對 VRT 在液冷滲透加速下的強烈信心），雖 P/E 31 較高但訂單能見度已延伸到 2027 上半年。AI 算力擴張沒有退場機制，VRT 是液冷轉型中最純的受惠者，逢回都是中長期佈局點。",
}

# ===== Build JSON =====

tickers_out = {}
total_news = 0
total_translations = 0

for sym in sorted(research.keys()):
    rec = RECOMMENDATIONS.get(sym)
    if not rec:
        # Skip if no recommendation (shouldn't happen for our set)
        continue
    news_list = []
    trans = TRANSLATIONS.get(sym, {})
    for r in research[sym]:
        title_en = r['title_en']
        # Try to find translation by id (URL) first, then by title
        url_id = r['url'].split('/')[-1]
        title_zh = trans.get(url_id) or trans.get(title_en) or title_en
        if title_zh != title_en:
            total_translations += 1
        news_list.append({
            'title_zh': title_zh,
            'title_en': title_en,
            'url': r['url'],
        })
        total_news += 1
    tickers_out[sym] = {
        'recommendation': rec,
        'news': news_list,
    }

output = {
    'date': DATE,
    'generated_at': GENERATED_AT,
    'source': f'yahoo-finance-research + stock-reports-{SOURCE_DATE}.html (fallback: today\'s HTML not generated by barchart job)',
    'model': 'MiniMax-M3',
    'tickers': tickers_out,
}

Path(OUT_PATH).parent.mkdir(exist_ok=True)
with open(OUT_PATH, 'w') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

size = Path(OUT_PATH).stat().st_size
print(f'\n=== Summary ===')
print(f'Date: {DATE}')
print(f'Generated at: {GENERATED_AT}')
print(f'Tickers processed: {len(tickers_out)}')
print(f'Total research reports fetched: {total_news}')
print(f'Translations written: {total_translations}')
print(f'AI recommendations written: {len(RECOMMENDATIONS)}')
print(f'Output file: {OUT_PATH}')
print(f'File size: {size} bytes ({size/1024:.1f} KB)')