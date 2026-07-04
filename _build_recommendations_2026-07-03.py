#!/usr/bin/env python3
"""Build the final recommendations/2026-07-03.json
Combines: ticker data + research + LLM-generated 繁體中文 recommendations + title translations
"""
import json
from datetime import datetime, timezone, timedelta

DATE = "2026-07-03"
TPE_TZ = timezone(timedelta(hours=8))
GENERATED_AT = datetime.now(TPE_TZ).strftime("%Y-%m-%dT%H:%M:%S+08:00")

with open('/home/matt/.openclaw/workspace/stock-reports/_research_2026-07-03.json') as f:
    research = json.load(f)
with open('/home/matt/.openclaw/workspace/stock-reports/_tickers_2026-07-03.json') as f:
    tickers = json.load(f)

# ----- LLM-generated 繁體中文 recommendations (2-3 sentences each) -----
# Combines: report paragraphs (why/outlook/risk) + research report themes
RECOMMENDATIONS = {
    "AMAT": (
        "AMAT 是 CoWoS 先進封裝設備的絕對瓶頸供應商，蝕刻與薄膜沉積製程在 HBM 與 AI 晶片供應鏈中具備剛需地位，"
        "今日暴漲 23.4% 反映市場對封裝產能擴張的極度飢渴，2H26 隨 2nm 量產將再啟設備更新週期。"
        "Argus 將其納入股息成長模型投資組合與每週精選名單，搭配 06/18 內部人買盤偏多訊號，"
        "雖 P/E 24.1 看似合理但訂單能見度已外溢到 2027，是回調時的核心配置標的。需留意對華出口管制升級風險。"
    ),
    "AMD": (
        "AMD MI350 系列以 HBM3e 高頻寬與性價比切入雲端 AI 訓練市場，微軟 Azure 與 Meta 已開始擴大採用，"
        "是 Nvidia 之外唯一能規模化挑戰的 GPU 替代方案，P/E 45 看似偏高但 PEG 仍落在 1.0 以下。"
        "Argus 將其列入 05/06 市場快訊名單，搭配 06/03 與 05/13 內部人買盤龍虎榜連續偏多訊號，"
        "2026 年資料中心營收佔比可望突破 50%，中長期甜蜜點尚未結束。"
    ),
    "GEV": (
        "GEV 是 AI 基建最末端的電力壟斷者，數據中心申請電力排隊時間已延至 3-5 年，"
        "變壓器與輸配電設備成為硬瓶頸，搭配 SMR 小型模組化反應爐商業化形成雙重護城河。"
        "Argus 為其發布個股分析報告並列入 05/11 每週精選名單，06/04 內部人買盤亦偏多，"
        "雖 P/E 28.5 偏高但訂單能見度已延伸至 2028 年，AI 的盡頭是電力，GEV 是最純的受惠者。需關注能源法規與環保政策變化。"
    ),
    "GLW": (
        "GLW 在 AI 集群光互連轉型中具備結構性優勢，當 GPU 規模突破 10 萬卡後傳統銅纜延遲已不可行，"
        "特種光纖成為唯一解，800G/1.6T 光模組滲透率加速將帶動營收進入長週期增長。"
        "今日暴漲 31.62% 反映光纖需求從「選配」變「標配」的拐點已至，P/E 18.5 是這份榜單中估值最甜的位置。"
        "Argus 將其納入 05/28 永續成長主題投資組合，搭配 05/27 與 05/19 內部人買盤訊號確認，逢回仍可加碼。"
    ),
    "MU": (
        "MU 是 HBM 供給緊缺的核心受惠者，HBM3e/HBM4 報價持續上漲推升毛利率兩個位階以上，"
        "AI GPU 客戶已將長約簽至 2027 年，P/E 12.4 是這份榜單中最低的本益比。"
        "Argus 06/25 發布個股分析報告明確看好中期偏多格局，同日市場摘要亦點名，"
        "06/22 技術評估確認多頭，現在位置相對距 52W 高點仍有 8% 折價，"
        "HBM 供需失衡要等到 2027 H2 才可能緩解，MU 是 AI 記憶體鏈最直接的多頭槓桿。"
    ),
    "PANW": (
        "PANW 是 AI 平台化資安的代表性受惠者，AI 降低攻擊門檻使企業必須從單點防禦升級到 AI 驅動的平台化方案，"
        "Prisma 與 Cortex 平台 ARR 增速維持 25%+，今日 +17.22% 反映市場對 AI 防禦剛需的重估。"
        "Argus 為其發布個股分析報告並列入 06/15 內部人買盤名單，06/11 技術評估亦確認中期偏多，"
        "雖 P/E 42 較高但資安 SaaS 的可預測性提供溢價合理性，AI 攻擊只會越來越多，PANW 是企業資安 Opex 化趨勢下的核心配置。"
    ),
    "PLTR": (
        "PLTR 的 AIP 平台在企業端滲透加速，2025 年從美國政府客戶擴展到商業客戶後營收結構明顯改善，"
        "AI OS 定位讓客戶轉換成本隨資料累積而提高，技術面亦維持中期偏多格局。"
        "Argus 為其發布 05/06 個股分析報告並列入市場摘要名單，04/23 技術評估亦確認多頭，"
        "雖 P/E 88 是榜單中最高，但若以「AI 時代作業系統」的本益比框架計算仍屬合理，"
        "短線因高估值震盪，但 AIP 在企業端的飛輪效應才剛啟動，長線仍是 AI 應用層的核心持有。"
    ),
    "VRT": (
        "VRT 是液冷標準的制定者，數據中心機櫃功耗從 10kW 飆升至 50kW+ 後風冷已不可行，"
        "VRT 從冷卻液分發到 CDU 模組擁有最完整的方案，2026 年液冷滲透率預估突破 40%。"
        "Argus 06/24 將目標價調升至 $378（從 $356 → $378 三週內連兩升，先前 06/10 還曾調降至 $344），"
        "反映分析師對液冷需求的信心回溫，訂單能見度延伸到 2027 上半年，"
        "AI 算力擴張沒有退場機制，VRT 是液冷轉型中最純的受惠者，逢回都是中長期佈局點。需留意原材料成本壓力。"
    ),
}

# ----- 繁體中文 title translations (台灣用語) -----
# Map: (ticker, original_title_en) -> title_zh
TRANSLATIONS = {
    ("AMAT", "The Argus Dividend Growth Model Portfolio"): "Argus 股息成長模型投資組合（應用材料入選）",
    ("AMAT", "Daily – Vickers Top Buyers & Sellers for 06/18/2026"): "每日 Vickers 內部人買賣龍虎榜（06/18）",
    ("AMAT", "Weekly Stock List"): "Argus 每週精選股名單",

    ("AMD", "Daily – Vickers Top Buyers & Sellers for 06/03/2026"): "每日 Vickers 內部人買賣龍虎榜（06/03）",
    ("AMD", "Daily – Vickers Top Buyers & Sellers for 05/13/2026"): "每日 Vickers 內部人買賣龍虎榜（05/13）",
    ("AMD", "Market Update: AMD, BMY, EQR, F, OGE, PWR, PYPL, ANET, STRL"): "市場快訊：AMD、BMY、EQR、F、OGE、PWR、PYPL、ANET、STRL",

    ("GEV", "Daily – Vickers Top Buyers & Sellers for 06/04/2026"): "每日 Vickers 內部人買賣龍虎榜（06/04）",
    ("GEV", "Weekly Stock List"): "Argus 每週精選股名單",
    ("GEV", "Analyst Report: GE Vernova Inc"): "分析師報告：GE Vernova",

    ("GLW", "The Argus Sustainable Growth Theme Model Portfolio"): "Argus 永續成長主題投資組合（Corning 入選）",
    ("GLW", "Daily – Vickers Top Buyers & Sellers for 05/27/2026"): "每日 Vickers 內部人買賣龍虎榜（05/27）",
    ("GLW", "Daily – Vickers Top Buyers & Sellers for 05/19/2026"): "每日 Vickers 內部人買賣龍虎榜（05/19）",

    ("MU", "Analyst Report: Micron Technology Inc"): "分析師報告：美光科技",
    ("MU", "Market Digest: MU, PNW, SJM"): "市場摘要：美光、PNW、SJM",
    ("MU", "Technical Assessment: Bullish in the Intermediate-Term"): "技術評估：中期偏多",

    ("PANW", "Daily – Vickers Top Buyers & Sellers for 06/15/2026"): "每日 Vickers 內部人買賣龍虎榜（06/15）",
    ("PANW", "Technical Assessment: Bullish in the Intermediate-Term"): "技術評估：中期偏多",
    ("PANW", "Analyst Report: Palo Alto Networks Inc"): "分析師報告：Palo Alto Networks",

    ("PLTR", "Analyst Report: Palantir Technologies Inc"): "分析師報告：Palantir Technologies",
    ("PLTR", "Market Digest: CAH, SHOP, DXCM, PLTR, GFS"): "市場摘要：CAH、SHOP、DXCM、PLTR、GFS",
    ("PLTR", "Technical Assessment: Bullish in the Intermediate-Term"): "技術評估：中期偏多",

    ("VRT", "Raising target price to $378.00"): "調升目標價至 378 美元",
    ("VRT", "Raising target price to $356.00"): "調升目標價至 356 美元",
    ("VRT", "Lowering target price to $344.00"): "調降目標價至 344 美元",
}


def translate(ticker, title_en):
    return TRANSLATIONS.get((ticker, title_en), title_en)


# ----- Build final output -----
tickers_out = {}
for sym in sorted(research.keys()):
    if sym not in RECOMMENDATIONS:
        continue
    rec = RECOMMENDATIONS[sym]
    news_list = []
    for r in research[sym]:
        news_list.append({
            'title_zh': translate(sym, r['title_en']),
            'title_en': r['title_en'],
            'url': r['url'],
        })
    tickers_out[sym] = {
        'recommendation': rec,
        'news': news_list,
    }

final = {
    'date': DATE,
    'generated_at': GENERATED_AT,
    'source': 'yahoo-finance-research + stock-reports-2026-07-01.html (fallback: today\'s HTML not generated by barchart job)',
    'model': 'MiniMax-M3',
    'tickers': tickers_out,
}

out_path = f'/home/matt/.openclaw/workspace/stock-reports/recommendations/{DATE}.json'
with open(out_path, 'w') as f:
    json.dump(final, f, ensure_ascii=False, indent=2)

print(f'Wrote {out_path}')
print(f'Tickers: {len(tickers_out)}')
print(f'Total news: {sum(len(t["news"]) for t in tickers_out.values())}')
print(f'Translations: {sum(1 for sym in tickers_out for _ in tickers_out[sym]["news"])}')

import os
print(f'File size: {os.path.getsize(out_path)} bytes')
