import json
from datetime import datetime

# Prepared data based on the fetched research reports and existing ticker logic
recommendations = {
    "date": "2026-07-08",
    "generated_at": datetime.now().isoformat(),
    "source": "yahoo-finance-research + stock-reports-2026-07-08.html",
    "model": "MiniMax-M3",
    "tickers": {
        "CRWD": {
            "recommendation": "CrowdStrike 在雲端安全市場持續展現強勁防禦韌性，AI 自動化威脅偵測需求是其核心支撐。技術面上該股維持強勢，適合作為 AI 基礎建設護城河的優質標的。",
            "news": [
                {"title_zh": "技術分析月度回顧：市場震盪中的復甦跡象", "title_en": "The stock market ended June in recovery mode...", "url": "https://finance.yahoo.com/research/reports/47486_Technical%20Analysis_1782904853000"},
                {"title_zh": "每日內部交易活動報告", "title_en": "The Vickers Top Buyers & Sellers is a daily report...", "url": "https://finance.yahoo.com/research/reports/47416_Top/Bottom%20Insider%20Activity_1782298722000"}
            ]
        },
        "NEE": {
            "recommendation": "NextEra Energy 作為公用事業與潔淨能源轉型的領軍者，將持續受益於 AI 資料中心對電力的剛性需求。其穩健的輸配電業務與再生能源組合，提供了良好的防禦性與成長潛力。",
            "news": [
                {"title_zh": "NextEra Energy 分析師報告", "title_en": "Headquartered in Juno Beach, Florida, NextEra Energy provides...", "url": "https://finance.yahoo.com/research/reports/2983_Analyst%20Report_1777054562000"},
                {"title_zh": "市場更新：經濟情緒與消費者信心調查", "title_en": "Stocks are a mixed bag at midday on Friday...", "url": "https://finance.yahoo.com/research/reports/46845_Market%20Update_1777053662000"}
            ]
        },
        "PLTR": {
            "recommendation": "Palantir 憑藉其 AI 數據平台展現強大的企業與政府端商業化能力，數據分析核心競爭力穩定。隨著數據轉型需求爆發，預計其獲利能力將持續攀升。",
            "news": [
                {"title_zh": "Palantir 分析師報告", "title_en": "Palantir develops and provides software that enables customers...", "url": "https://finance.yahoo.com/research/reports/6302_Analyst%20Report_1778065523000"},
                {"title_zh": "月度經濟、利率與股市調查", "title_en": "A Fragile Truce: Our Monthly Survey of the Economy, Interest Rates, and Stocks...", "url": "https://finance.yahoo.com/research/reports/46942_Market%20Summary_1778065523000"}
            ]
        },
        "SNOW": {
            "recommendation": "Snowflake 作為雲原生數據倉庫，其高黏著度平台對於高品質 AI 訓練需求至關重要。隨企業 AI 模型應用增加，Snowflake 的數據雲架構預計將獲取更多長期穩定增長。",
            "news": [
                {"title_zh": "第一季財報趨勢分析與企業展望", "title_en": "The first-quarter earnings season has been sensational...", "url": "https://finance.yahoo.com/research/reports/47193_Stock%20Picks_1780315198000"},
                {"title_zh": "Snowflake 分析師報告", "title_en": "Snowflake calls itself an AI data cloud company...", "url": "https://finance.yahoo.com/research/reports/6355_Analyst%20Report_1780053669000"}
            ]
        }
    }
}

with open('/home/matt/.openclaw/workspace/stock-reports/recommendations/2026-07-08.json', 'w') as f:
    json.dump(recommendations, f, indent=2, ensure_ascii=False)
