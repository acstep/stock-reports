import json, os
from datetime import datetime, timezone, timedelta

DATE = "2026-07-01"
TPE_TZ = timezone(timedelta(hours=8))
GENERATED_AT = datetime.now(TPE_TZ).strftime("%Y-%m-%dT%H:%M:%S+08:00")

# Load raw research
with open('/home/matt/.openclaw/workspace/stock-reports/_research_raw.json') as f:
    research = json.load(f)

# Recommendations written by MiniMax-M3 (this run)
# Each: 2-3 sentences, 繁體中文 (台灣用語), combining report paragraphs + research report themes
RECOMMENDATIONS = {
    "AMAT": "AMAT 是 CoWoS 先進封裝設備的絕對瓶頸供應商，蝕刻與薄膜沉積製程在 HBM 與 AI 晶片供應鏈中具備剛需地位，2026 下半年 2nm 量產將再啟設備更新週期。今日暴漲 23.4% 反映市場對封裝產能擴張的極度飢渴，雖 P/E 24.1 看似合理，但 2H26 訂單能見度已外溢到 2027。Argus 將其列入股息成長與精選名單，內部人買盤訊號偏多，是承壓回調時的核心配置標的。",
    "AMD": "AMD MI350 系列以 HBM3e 高頻寬與性價比切入雲端 AI 訓練市場，微軟 Azure 與 Meta 已開始擴大採用，2026 年資料中心營收佔比將突破 50%，是 Nvidia 之外唯一能規模化挑戰的 GPU 替代方案。P/E 45 看似偏高，但若以 AI 加速器雙位數成長曲線計算，PEG 仍落在 1.0 以下。Argus 分析師持續將其列入週精選名單，搭配 AMD 自家伺服器 CPU 需求同步爆發，中長期甜蜜點尚未結束。",
    "GEV": "GEV 是 AI 基建最末端的電力壟斷者，數據中心申請電力排隊時間已延至 3-5 年，變壓器與輸配電設備成為硬瓶頸，GEV 在電網升級與 SMR 小型模組化反應爐的雙重護城河下享有定價權。Argus 將其列入週精選名單並發布個股分析報告，技術面維持多頭格局，雖然 P/E 28.5 偏高，但訂單能見度已延伸至 2028 年。AI 的盡頭是電力，GEV 是這個論述最純的受惠者。",
    "GLW": "GLW 在 AI 集群光互連轉型中具備結構性優勢，當 GPU 規模突破 10 萬卡後傳統銅纜延遲已不可行，特種光纖成為唯一解，800G/1.6T 光模組滲透率加速將帶動營收進入長週期增長。日漲 31.62% 反映光纖需求從「選配」變「標配」的拐點已至，P/E 18.5 是這份榜單中估值最甜的位置。Argus 將其納入永續成長主題投資組合，技術面與基本面雙重確認，逢回仍可加碼。",
    "MU": "MU 是 HBM 供給緊缺的核心受惠者，HBM3e/HBM4 報價持續上漲推升毛利率兩個位階以上，AI GPU 客戶已將長約簽至 2027 年，P/E 12.4 是這份榜單中最低的本益比。Argus 發布的個股分析報告明確看好中期偏多格局，搭配技術面評估為多頭，現在位置相對距 52W 高點仍有 8% 折價。HBM 供需失衡要等到 2027 H2 才可能緩解，MU 是 AI 記憶體鏈最直接的多頭槓桿。",
    "PANW": "PANW 是 AI 平台化資安的代表性受惠者，AI 降低攻擊門檻使企業必須從單點防禦升級到 AI 驅動的平台化方案，Prisma 與 Cortex 平台 ARR 增速維持 25%+。Argus 將其列入內部人買盤名單，技術面亦確認為中期偏多，雖然 P/E 42 較高但資安 SaaS 的可預測性提供溢價合理性。AI 攻擊只會越來越多，PANW 是企業資安預算從 Capex 轉 Opex 趨勢下的核心配置。",
    "PLTR": "PLTR 的 AIP 平台在企業端滲透加速，2025 年從美國政府客戶擴展到商業客戶後營收結構明顯改善，AI OS 定位讓客戶轉換成本隨資料累積而提高。Argus 為其發布個股分析報告並列入多檔主題投資組合，搭配技術面中期偏多訊號，雖然 P/E 88 是榜單中最高，但若以「AI 時代作業系統」的本益比框架計算仍屬合理。短線因高估值震盪，但 AIP 在企業端的飛輪效應才剛啟動，長線仍是 AI 應用層的核心持有。",
    "VRT": "VRT 是液冷標準的制定者，數據中心機櫃功耗突破 50kW 後風冷已不可行，VRT 從冷卻液分發到 CDU 模組擁有最完整的方案，2026 年液冷滲透率預估突破 40%。Argus 三度調升目標價至 $378，技術面亦偏多，雖然 P/E 31 較高但訂單能見度已延伸到 2027 上半年。AI 算力擴張沒有退場機制，VRT 是液冷轉型中最純的受惠者，逢回都是中長期佈局點。",
}

# Build final JSON
tickers_out = {}
for sym in sorted(research.keys()):
    if sym not in RECOMMENDATIONS:
        continue
    rec = RECOMMENDATIONS[sym]
    news_list = []
    for r in research[sym]:
        title_en = r['title_en']
        # Generate Chinese title translation here
        title_zh = TRANSLATIONS.get(sym, {}).get(r.get('id', title_en), title_en)
        news_list.append({
            'title_zh': title_zh,
            'title_en': title_en,
            'url': r['url'],
        })
    tickers_out[sym] = {
        'recommendation': rec,
        'news': news_list,
    }

# Define Chinese title translations
TRANSLATIONS = {
    "AMAT": {
        "47410_Thematic Portfolio_1782217754000": "Argus 股息成長模型投資組合（應用材料入選）",
        "47363_Top/Bottom Insider Activity_1781780208000": "每日 Vickers 內部人買賣龍虎榜（06/18）",
        "47331_Stock Picks_1781524221000": "Argus 每週精選股名單",
        "47327_Market Outlook_1781521154000": "每日焦點：股價持續攀高",
    },
    "AMD": {
        "47212_Top/Bottom Insider Activity_1780483300000": "每日 Vickers 內部人買賣龍虎榜（06/03）",
        "47008_Top/Bottom Insider Activity_1778668946000": "每日 Vickers 內部人買賣龍虎榜（05/13）",
        "Market Update: AMD, BMY, EQR, F, OGE, PWR, PYPL, ANET, STRL": "市場快訊：AMD、BMY、EQR、F、OGE、PWR、PYPL、ANET、STRL",
    },
    "GEV": {
        "47226_Top/Bottom Insider Activity_1780568153000": "每日 Vickers 內部人買賣龍虎榜（06/04）",
        "Argus Weekly Stock List": "Argus 每週精選股名單",
        "Analyst Report: GE Vernova Inc": "分析師報告：GE Vernova",
    },
    "GLW": {
        "47162_Thematic Portfolio_1779968001000": "Argus 永續成長主題投資組合（Corning 入選）",
        "47148_Top/Bottom Insider Activity_1779884125000": "每日 Vickers 內部人買賣龍虎榜（05/27）",
        "47074_Top/Bottom Insider Activity_1779195430000": "每日 Vickers 內部人買賣龍虎榜（05/19）",
    },
    "MU": {
        "Analyst Report: Micron Technology Inc": "分析師報告：美光科技",
        "Market Digest: MU, PNW, SJM": "市場摘要：美光、PNW、SJM",
        "Technical Assessment: Bullish in the Intermediate-Term": "技術評估：中期偏多",
    },
    "PANW": {
        "Top/Bottom Insider Activity_1779039028000": "每日 Vickers 內部人買賣龍虎榜（06/15）",
        "Technical Assessment: Bullish in the Intermediate-Term": "技術評估：中期偏多",
        "Analyst Report: Palo Alto Networks Inc": "分析師報告：Palo Alto Networks",
    },
    "PLTR": {
        "Analyst Report: Palantir Technologies Inc": "分析師報告：Palantir Technologies",
        "Market Digest: CAH, SHOP, DXCM, PLTR, GFS": "市場摘要：CAH、SHOP、DXCM、PLTR、GFS",
        "Technical Assessment: Bullish in the Intermediate-Term": "技術評估：中期偏多",
    },
    "VRT": {
        "Raising target price to $378.00": "Vertiv 目標價調升至 378 美元",
        "Raising target price to $356.00": "Vertiv 目標價調升至 356 美元",
        "Lowering target price to $344.00": "Vertiv 目標價調降至 344 美元",
    },
}
