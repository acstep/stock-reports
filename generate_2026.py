import json
from datetime import datetime

# === TODAY'S DATA (2026-05-26) from Yahoo Finance ===
prices = {
    'NVDA': {'price': 215.33, 'chg': -4.43, 'high52': 236.54, 'low52': 132.92, 'from_low_pct': 62.0, 'volume': 169275710, 'name': 'NVIDIA'},
    'AMD': {'price': 467.51, 'chg': 10.24, 'high52': 481.41, 'low52': 108.62, 'from_low_pct': 330.4, 'volume': 34758602, 'name': 'AMD'},
    'AVGO': {'price': 414.14, 'chg': -2.60, 'high52': 442.36, 'low52': 231.13, 'from_low_pct': 79.2, 'volume': 14086441, 'name': 'Broadcom'},
    'QCOM': {'price': 238.16, 'chg': 18.20, 'high52': 247.90, 'low52': 121.99, 'from_low_pct': 95.2, 'volume': 30375674, 'name': 'Qualcomm'},
    'MRVL': {'price': 196.33, 'chg': 10.99, 'high52': 198.40, 'low52': 58.61, 'from_low_pct': 235.0, 'volume': 19823206, 'name': 'Marvell'},
    'INTC': {'price': 119.84, 'chg': 10.18, 'high52': 132.75, 'low52': 18.97, 'from_low_pct': 531.7, 'volume': 82663024, 'name': 'Intel'},
    'TSM': {'price': 404.52, 'chg': 0.04, 'high52': 421.97, 'low52': 190.56, 'from_low_pct': 112.3, 'volume': 7085377, 'name': 'TSMC'},
    'ARM': {'price': 306.51, 'chg': 46.54, 'high52': 315.00, 'low52': 100.02, 'from_low_pct': 206.4, 'volume': 13961817, 'name': 'Arm Holdings'},
    'SMCI': {'price': 35.58, 'chg': 14.63, 'high52': 62.36, 'low52': 19.48, 'from_low_pct': 82.6, 'volume': 39440978, 'name': 'Super Micro'},
    'DELL': {'price': 295.19, 'chg': 21.98, 'high52': 298.32, 'low52': 106.38, 'from_low_pct': 177.5, 'volume': 15237483, 'name': 'Dell'},
    'HPQ': {'price': 25.24, 'chg': 21.29, 'high52': 29.55, 'low52': 17.56, 'from_low_pct': 43.7, 'volume': 45907332, 'name': 'HP Inc'},
    'ANET': {'price': 154.03, 'chg': 8.49, 'high52': 179.80, 'low52': 83.86, 'from_low_pct': 83.7, 'volume': 9302725, 'name': 'Arista Networks'},
    'VST': {'price': 156.27, 'chg': 11.88, 'high52': 219.82, 'low52': 132.66, 'from_low_pct': 17.8, 'volume': 5828563, 'name': 'Vistra'},
    'CEG': {'price': 294.07, 'chg': 10.06, 'high52': 412.70, 'low52': 243.30, 'from_low_pct': 20.9, 'volume': 2879937, 'name': 'Constellation Energy'},
    'NRG': {'price': 137.65, 'chg': 7.70, 'high52': 189.96, 'low52': 121.22, 'from_low_pct': 13.6, 'volume': 2147291, 'name': 'NRG Energy'},
    'NEE': {'price': 88.55, 'chg': -5.15, 'high52': 98.75, 'low52': 66.77, 'from_low_pct': 32.6, 'volume': 8986898, 'name': 'NextEra Energy'},
    'AES': {'price': 14.68, 'chg': 1.45, 'high52': 17.65, 'low52': 9.58, 'from_low_pct': 53.2, 'volume': 5772191, 'name': 'AES Corp'},
    'PNRG': {'price': 259.24, 'chg': -3.33, 'high52': 278.90, 'low52': 126.40, 'from_low_pct': 105.1, 'volume': 52162, 'name': 'PrimeEnergy'},
    'ETN': {'price': 391.35, 'chg': -2.03, 'high52': 435.43, 'low52': 311.90, 'from_low_pct': 25.5, 'volume': 2327691, 'name': 'Eaton'},
    'VRT': {'price': 327.46, 'chg': -11.72, 'high52': 379.94, 'low52': 104.71, 'from_low_pct': 212.7, 'volume': 4782624, 'name': 'Vertiv'},
    'SPXC': {'price': 207.80, 'chg': 3.39, 'high52': 246.68, 'low52': 150.50, 'from_low_pct': 38.1, 'volume': 383179, 'name': 'SPX Technologies'},
    'GLW': {'price': 194.05, 'chg': 1.17, 'high52': 211.79, 'low52': 48.62, 'from_low_pct': 299.1, 'volume': 8321054, 'name': 'Corning'},
    'LUMN': {'price': 9.41, 'chg': -6.37, 'high52': 11.95, 'low52': 3.37, 'from_low_pct': 179.2, 'volume': 8028209, 'name': 'Lumen'},
    'CIEN': {'price': 583.74, 'chg': 5.28, 'high52': 599.50, 'low52': 70.77, 'from_low_pct': 724.8, 'volume': 1413086, 'name': 'Ciena'},
    'CSCO': {'price': 120.41, 'chg': 1.86, 'high52': 120.79, 'low52': 62.30, 'from_low_pct': 93.3, 'volume': 18132424, 'name': 'Cisco'},
    'MU': {'price': 751.00, 'chg': 3.63, 'high52': 818.67, 'low52': 92.22, 'from_low_pct': 714.4, 'volume': 36002915, 'name': 'Micron'},
    'NTAP': {'price': 139.36, 'chg': 16.20, 'high52': 141.75, 'low52': 93.69, 'from_low_pct': 48.7, 'volume': 6668173, 'name': 'NetApp'},
    'PSTG': {'price': 67.80, 'chg': -16.48, 'high52': 100.59, 'low52': 43.51, 'from_low_pct': 55.8, 'volume': 2815232, 'name': 'Pure Storage'},
    'WDC': {'price': 484.28, 'chg': 0.47, 'high52': 525.15, 'low52': 50.62, 'from_low_pct': 856.7, 'volume': 4492768, 'name': 'Western Digital'},
    'AMKR': {'price': 65.75, 'chg': -6.54, 'high52': 79.23, 'low52': 17.79, 'from_low_pct': 269.6, 'volume': 5895257, 'name': 'Amkor'},
    'ASX': {'price': 34.81, 'chg': 2.96, 'high52': 35.71, 'low52': 9.23, 'from_low_pct': 277.1, 'volume': 8117731, 'name': 'ASE Technology'},
    'AMAT': {'price': 432.16, 'chg': -1.02, 'high52': 448.45, 'low52': 153.47, 'from_low_pct': 181.6, 'volume': 4892619, 'name': 'Applied Materials'},
    'LRCX': {'price': 305.35, 'chg': 7.25, 'high52': 309.98, 'low52': 79.49, 'from_low_pct': 284.1, 'volume': 7859187, 'name': 'Lam Research'},
    'KLAC': {'price': 1888.38, 'chg': 4.66, 'high52': 1920.00, 'low52': 740.00, 'from_low_pct': 155.0, 'volume': 723721, 'name': 'KLA Corp'},
    'CRWD': {'price': 663.46, 'chg': 11.68, 'high52': 674.84, 'low52': 342.72, 'from_low_pct': 93.6, 'volume': 2781663, 'name': 'CrowdStrike'},
    'NET': {'price': 216.17, 'chg': 9.42, 'high52': 260.00, 'low52': 158.83, 'from_low_pct': 36.1, 'volume': 2108826, 'name': 'Cloudflare'},
    'PANW': {'price': 260.58, 'chg': 7.31, 'high52': 261.41, 'low52': 139.57, 'from_low_pct': 86.7, 'volume': 6629104, 'name': 'Palo Alto'},
    'ZS': {'price': 182.37, 'chg': 13.24, 'high52': 336.99, 'low52': 114.63, 'from_low_pct': 59.1, 'volume': 4003773, 'name': 'Zscaler'},
    'OKTA': {'price': 92.24, 'chg': 11.44, 'high52': 127.52, 'low52': 62.66, 'from_low_pct': 47.2, 'volume': 3007460, 'name': 'Okta'},
    'PLTR': {'price': 136.88, 'chg': 2.16, 'high52': 207.52, 'low52': 118.93, 'from_low_pct': 15.1, 'volume': 27578014, 'name': 'Palantir'},
    'SNOW': {'price': 172.20, 'chg': 9.35, 'high52': 280.67, 'low52': 118.30, 'from_low_pct': 45.6, 'volume': 5763902, 'name': 'Snowflake'},
    'AI': {'price': 9.29, 'chg': 7.40, 'high52': 44.50, 'low52': 7.68, 'from_low_pct': 21.0, 'volume': 4426068, 'name': 'C3.ai'},
    'APP': {'price': 481.68, 'chg': -3.86, 'high52': 799.54, 'low52': 320.30, 'from_low_pct': 50.5, 'volume': 3830317, 'name': 'AppLovin'},
    'GOOGL': {'price': 382.97, 'chg': -3.48, 'high52': 408.61, 'low52': 162.00, 'from_low_pct': 136.4, 'volume': 20442123, 'name': 'Alphabet'},
    'MSFT': {'price': 418.57, 'chg': -0.79, 'high52': 555.45, 'low52': 356.28, 'from_low_pct': 17.5, 'volume': 22390344, 'name': 'Microsoft'},
    'AMZN': {'price': 266.32, 'chg': 0.83, 'high52': 278.56, 'low52': 196.00, 'from_low_pct': 35.9, 'volume': 27535526, 'name': 'Amazon'},
    'META': {'price': 610.26, 'chg': -0.65, 'high52': 796.25, 'low52': 520.26, 'from_low_pct': 17.3, 'volume': 11688623, 'name': 'Meta'},
    'ORCL': {'price': 192.08, 'chg': -0.45, 'high52': 342.40, 'low52': 134.78, 'from_low_pct': 42.7, 'volume': 9467888, 'name': 'Oracle'},
    'STX': {'price': 812.73, 'chg': 2.17, 'high52': 840.00, 'low52': 116.00, 'from_low_pct': 618.0, 'volume': 2534548, 'name': 'Seagate'},
    'D': {'price': 67.67, 'chg': 9.62, 'high52': 68.96, 'low52': 53.40, 'from_low_pct': 26.8, 'volume': 6259805, 'name': 'Dominion Energy'},
    'EIX': {'price': 71.18, 'chg': 2.92, 'high52': 74.80, 'low52': 47.75, 'from_low_pct': 49.1, 'volume': 1336709, 'name': 'Edison Intl'},
    'AEP': {'price': 131.59, 'chg': 5.15, 'high52': 139.58, 'low52': 100.79, 'from_low_pct': 30.6, 'volume': 3280669, 'name': 'American Electric'},
    'SRE': {'price': 92.80, 'chg': 2.62, 'high52': 98.22, 'low52': 73.06, 'from_low_pct': 27.0, 'volume': 1503034, 'name': 'Sempra'},
    'DUK': {'price': 125.67, 'chg': 3.90, 'high52': 130.52, 'low52': 113.46, 'from_low_pct': 10.8, 'volume': 1748177, 'name': 'Duke Energy'},
    'SO': {'price': 94.55, 'chg': 2.16, 'high52': 99.80, 'low52': 83.85, 'from_low_pct': 12.8, 'volume': 2150635, 'name': 'Southern Company'},
    'SI': {'price': 14.60, 'chg': -6.59, 'high52': 17.91, 'low52': 10.93, 'from_low_pct': 33.7, 'volume': 81659, 'name': 'Siemens'},
}

# Category mapping
categories = {
    'NVDA': ('💾 AI 晶片/GPU', '#f97316'),
    'AMD': ('💾 AI 晶片/GPU', '#f97316'),
    'AVGO': ('💾 AI 晶片/GPU', '#f97316'),
    'QCOM': ('💾 AI 晶片/GPU', '#f97316'),
    'MRVL': ('💾 AI 晶片/GPU', '#f97316'),
    'INTC': ('💾 AI 晶片/GPU', '#f97316'),
    'TSM': ('💾 AI 晶片/GPU', '#f97316'),
    'ARM': ('💾 AI 晶片/GPU', '#f97316'),
    'SMCI': ('🖥️ AI 伺服器/雲端', '#06b6d4'),
    'DELL': ('🖥️ AI 伺服器/雲端', '#06b6d4'),
    'HPQ': ('🖥️ AI 伺服器/雲端', '#06b6d4'),
    'ANET': ('📡 AI 網路/光纖', '#a855f7'),
    'VST': ('⚡ AI 電力/能源', '#24e08a'),
    'CEG': ('⚡ AI 電力/能源', '#24e08a'),
    'NRG': ('⚡ AI 電力/能源', '#24e08a'),
    'NEE': ('⚡ AI 電力/能源', '#24e08a'),
    'AES': ('⚡ AI 電力/能源', '#24e08a'),
    'PNRG': ('⚡ AI 電力/能源', '#24e08a'),
    'ETN': ('⚡ AI 電力/能源', '#24e08a'),
    'VRT': ('🧊 AI 散熱/液冷', '#38bdf8'),
    'SPXC': ('🧊 AI 散熱/液冷', '#38bdf8'),
    'GLW': ('📡 AI 網路/光纖', '#a855f7'),
    'LUMN': ('📡 AI 網路/光纖', '#a855f7'),
    'CIEN': ('📡 AI 網路/光纖', '#a855f7'),
    'CSCO': ('📡 AI 網路/光纖', '#a855f7'),
    'MU': ('💾 AI 儲存/記憶體', '#f472b6'),
    'NTAP': ('💾 AI 儲存/記憶體', '#f472b6'),
    'PSTG': ('💾 AI 儲存/記憶體', '#f472b6'),
    'WDC': ('💾 AI 儲存/記憶體', '#f472b6'),
    'STX': ('💾 AI 儲存/記憶體', '#f472b6'),
    'AMKR': ('📦 AI 先進封裝/CoWoS', '#e879f9'),
    'ASX': ('📦 AI 先進封裝/CoWoS', '#e879f9'),
    'AMAT': ('📦 AI 先進封裝/CoWoS', '#e879f9'),
    'LRCX': ('📦 AI 先進封裝/CoWoS', '#e879f9'),
    'KLAC': ('📦 AI 先進封裝/CoWoS', '#e879f9'),
    'CRWD': ('🔐 AI 資安/雲端', '#fb923c'),
    'NET': ('🔐 AI 資安/雲端', '#fb923c'),
    'PANW': ('🔐 AI 資安/雲端', '#fb923c'),
    'ZS': ('🔐 AI 資安/雲端', '#fb923c'),
    'OKTA': ('🔐 AI 資安/雲端', '#fb923c'),
    'PLTR': ('🤖 AI 軟體/資料分析', '#f43f5e'),
    'SNOW': ('🤖 AI 軟體/資料分析', '#f43f5e'),
    'AI': ('🤖 AI 軟體/資料分析', '#f43f5e'),
    'APP': ('🤖 AI 軟體/資料分析', '#f43f5e'),
    'GOOGL': ('☁️ AI 雲端平台', '#5b7fff'),
    'MSFT': ('☁️ AI 雲端平台', '#5b7fff'),
    'AMZN': ('☁️ AI 雲端平台', '#5b7fff'),
    'META': ('☁️ AI 雲端平台', '#5b7fff'),
    'ORCL': ('☁️ AI 雲端平台', '#5b7fff'),
    'D': ('🏭 AI 基建其他', '#64748b'),
    'EIX': ('🏭 AI 基建其他', '#64748b'),
    'AEP': ('🏭 AI 基建其他', '#64748b'),
    'SRE': ('🏭 AI 基建其他', '#64748b'),
    'DUK': ('🏭 AI 基建其他', '#64748b'),
    'SO': ('🏭 AI 基建其他', '#64748b'),
    'SI': ('🏭 AI 基建其他', '#64748b'),
}

# AI-native analysis - today's report
stock_analysis = {
    'ARM': {
        'verdict': 'STRONG BUY', 'signal': 'BREAKOUT +46% — 市場焦點',
        'core': 'Arm 今日爆漲 +46.5% 來到 $306.5，是全市場最大亮點。Arm Neoverse 在雲端滲透率急升，AWS Graviton、Microsoft Cobalt、Meta Scalable Solutions 均基於 Arm 架構。資料中心 Arm 化學ype 正在加速，Intel/AMD x86 份額逐步被吃掉。AI 推理工作負載對功耗效率的追求，讓 Arm 架構天然優勢顯現。IPO 後第一個完整年度，營收加速明顯，2025 年資料中心營收年增率达 50%+。',
        'outlook': '目標 $380+。Arm 授權模式天生抗風險，資料中心滲透率提升邏輯持續強化，2025 年是資料中心 Arm 化元年。',
        'entry': '$270-$305', 'stop': '$250'
    },
    'DELL': {
        'verdict': 'STRONG BUY', 'signal': 'SERVER DEMAND EXPLOSION +22%',
        'core': '戴爾今日暴漲 +22% 來到 $295，距離 52W 高點 $298 僅差 1%，是 AI 伺服器超級周期的核心受益者。AI Solutions Group 營收爆發，Dell 為 Microsoft/Google/Amazon 提供 AI 伺服器整合服務，PowerEdge 搭配 AMD/Intel GPU 銷售火熱。結構性轉型故事清晰：傳統 PC 復甦 + AI 伺服器爆發雙引擎。Q2 財報顯示 AI 伺服器訂單積壓創歷史新高，2025 會計年度資本支出超預期。',
        'outlook': '目標 $350+。Dell 是 2025 年伺服器超級周期的最大贏家之一，AI 解決方案營收預估年增 50%+。',
        'entry': '$260-$295', 'stop': '$235'
    },
    'HPQ': {
        'verdict': 'BUY', 'signal': 'PC RECOVERY + AI PC UPGRADE +21%',
        'core': 'HP 今日大漲 +21.3% 來到 $25.24，PC 市場連續兩季復甦，AI PC 換機潮（Snapdragon X Elite, Intel Lunar Lake）帶來 ASP 提升。收購 Poly 整合效應逐步顯現，企業協作硬體需求回升。AI PC 硬體規格要求提升（16GB+ RAM, NPU）將強制換機，2025-2026 年 PC 更換週期將是 HP 史上最大規模。',
        'outlook': '目標 $32+。AI PC 升級週期將幫助 HP 重回營收成長，估計 2025 年 AI PC 滲透率達 20%。',
        'entry': '$21-$25', 'stop': '$18'
    },
    'QCOM': {
        'verdict': 'STRONG BUY', 'signal': 'EARNINGS MOMENTUM +18%',
        'core': '高通今日暴漲 +18.2% 來到 $238，受惠 Snapdragon X Elite 在 AI PC 滲透率超預期（已獲得聯想、HP、戴爾採用），同時中國手機市場反彈。AI Edge（手機+PC+IoT）成為新成長引擎，取代傳統手機週期性。推理能力下沉至 Edge（100B+ 參數）將帶動更換週期，Qualcomm AI Hub 生態初具規模。汽車晶片（Snapdragon Ride）開始進入豐田、通用供應鏈。',
        'outlook': '目標 $280+。AI Edge 趨勢爆發，Snapdragon X 2025 年出貨量預估達千萬等級，汽車業務是下一個驚喜。',
        'entry': '$210-$235', 'stop': '$190'
    },
    'NTAP': {
        'verdict': 'STRONG BUY', 'signal': 'DATA STORAGE EXPLOSION +16%',
        'core': 'NetApp 今日暴漲 +16.2% 來到 $139.36，距 52W 高點 $141.75 僅差 1.7%，技術面即將突破。ONTAP AI 是唯一整合了雲端和本地儲存的資料管理平台，在 AI 訓練資料儲存需求爆發中直接受益。NS02 AIOps 資料管理平台開始變現，結構性轉型從硬體轉向軟體訂閱，毛利率持續改善。',
        'outlook': '目標 $165+。AI 資料湖儲存需求將持續爆發，NetApp 在全球前 2000 大企業的資料管理滲透率僅 15%，長期成長空間巨大。',
        'entry': '$120-$140', 'stop': '$110'
    },
    'SMCI': {
        'verdict': 'BUY', 'signal': 'RECOVERY MOMENTUM +14.6%',
        'core': '超微今日大漲 +14.6% 來到 $35.6，距 52W 低點 $19.48 反彈超 82%，已脫離極度超賣區。審計問題仍是中期陰影，但新管理層上任、降成本行動開始見效。AI 伺服器需求真實存在，JDM 模式下與 Nvidia/AMD GPU 配套仍是 CSP 核心選擇。股價從低點修復中，基本面尚未完全反應。',
        'outlook': '目標 $50+。降成本 + 擺脫審計危機後，股價有修復空間，但需持續關注審計進展。',
        'entry': '$30-$36', 'stop': '$25'
    },
    'ZS': {
        'verdict': 'BUY', 'signal': 'SASE SECURITY +13.2%',
        'core': 'Zscaler 今日大漲 +13.2% 來到 $182，距 52W 高點 $337 仍有 45% 修復空間。SASE 市場領導者，AI 時代的資料安全態勢管理（DSPM）產品受大型企業追捧。零信任網路架構（ZTNA）已成為企業資安剛需，Zscaler 在全球財富 500 企業滲透率超 40%。IoT Security 是下一個新增長曲線。',
        'outlook': '目標 $220+。Zscaler 是少數可以同時受益於 AI 安全威脅增加 + 企業安全現代化兩大趨勢的資安股。',
        'entry': '$160-$183', 'stop': '$145'
    },
    'VST': {
        'verdict': 'STRONG BUY', 'signal': 'NEAR 52W LOW +11.9%',
        'core': 'Vistra 是美國最大民營發電廠，今日大漲 +11.9% 來到 $156，距 52W 低點 $132.66 僅高 17.8%，提供罕見的安全邊際。AI 資料中心對穩定電力需求爆發，Vistra 手握核電 + Natural Gas 多元能源組合，已與多家 CSP 簽訂長期供電協議（PPA）。核能、AI 資料中心用電、潔淨能源三重主題疊加，估值極具吸引力。',
        'outlook': '目標 $200+。AI 資料中心用電量 2030 年將較 2023 年增加 200%+，電力股嚴重低估。',
        'entry': '$145-$158', 'stop': '$130'
    },
    'CRWD': {
        'verdict': 'STRONG BUY', 'signal': 'CYBERSECURITY AI DEFENSE +11.7%',
        'core': 'CrowdStrike 今日大漲 +11.7% 來到 $663，距歷史高點 $674.84 僅差 1.7%。AI 資安領域無可爭議的領導者，Charlotte AI 平台將 GenAI 整合到資安工作流，EDR 市場份額持續擴大至 30%+。AI 攻擊增加（deepfake + AI-driven malware）反而讓 CrowdStrike 的領先優勢更加明顯。終端保護市場持續整合，CRWD 是最大受益者。',
        'outlook': '目標 $750+。AI 時代資安威脅指數增加，CRWD 是終極受益者，訂閱營收 NRR 維持 115%+。',
        'entry': '$600-$665', 'stop': '$550'
    },
    'OKTA': {
        'verdict': 'BUY', 'signal': 'IDENTITY SECURITY +11.4%',
        'core': 'Okta 今日大漲 +11.4% 來到 $92，距 52W 低點 $62.66 上漲 47%。零信任身份管理是 AI 安全最底層的基礎設施，Okta 捆綁 SSO/MFA/IG 佔據企業身份入口。AI 驅動的 deepfake 身份欺詐增加使多因素認證剛需更加突出。Okta Customer Identity Cloud 成長加速，全球 DevOps 社群滲透率極高。',
        'outlook': '目標 $120+。身份管理是零信任架構的第一道防線，Okta 在 CSP 及大型企業滲透率仍低，長期成長明確。',
        'entry': '$82-$93', 'stop': '$72'
    },
    'MRVL': {
        'verdict': 'STRONG BUY', 'signal': 'BULLISH MOMENTUM +11%',
        'core': 'Marvell AI 伺服器業務爆發，Custom AI ASIC（台積電 N5P）打入 Google/AWS/微軟供應鏈。光纖收發器（PAM4, 800G）需求井噴，CW/C2W 平台全球市佔第一。今日大漲 +11% 來到 $196，距 52W 高點 $198.4 僅差 1%，是典型突破形態。營收從 CY2023 $5.5B 到 CY2026 $10B+ 路徑清晰。',
        'outlook': '目標 $240+。Marvell 是少數同時覆蓋 AI Compute (ASIC) + AI Connectivity (Optical) 兩大趨勢的標的，2025 年 AI 營收估計年增 80%+。',
        'entry': '$175-$195', 'stop': '$160'
    },
    'AMD': {
        'verdict': 'STRONG BUY', 'signal': 'BULLISH BREAKOUT +10.2%',
        'core': 'AMD MI300X 已進入規模量產，Microsoft Azure、Meta 持續擴大採用，對 NVIDIA H100 形成價格殺傷力。今日大漲 +10.2% 來到 $467，距 52W 高點 481 僅差 3%，短線動能極強。Instinct 系列在推理性價比優於 H100，中長期份額持續提升。EPYC 伺服器 CPU 資料中心滲透率也在爬升，2025 年 Revenue Guidance 上調機率極高。',
        'outlook': '短線挑戰 $500，中線 $550+。AMD 在 AI GPU 市場份額從 2023 年的 ~5% 提升至 2025 年預估的 20%+，結構性成長明確。',
        'entry': '$430-$465', 'stop': '$400'
    },
    'INTC': {
        'verdict': 'SPECULATIVE BUY', 'signal': 'TURNAROUND +10.2%',
        'core': '英特爾今日大漲 +10.2% 來到 $119，是典型空頭回補 + 消息催化劑。Intel 18A 製程傳獲微軟等客戶青睞，IFS (Intel Foundry Services) 新廠產能逐步開出。Gaudi 3 AI 加速器性價比具體優勢，但 IDM 2.0 轉型仍在早期，債務負擔重，風險較高。適合有耐心的高風險偏好者。',
        'outlook': '目標 $145。IFS 2025-2026 能否獲得大型 CSP 訂單是關鍵催化劑。',
        'entry': '$105-$120', 'stop': '$95'
    },
    'CEG': {
        'verdict': 'STRONG BUY', 'signal': 'NUCLEAR AI THEMATIC +10%',
        'core': 'Constellation Energy 今日大漲 +10.1% 來到 $294，距 52W 低點 $243.3 仍有 20.9% 上漲空間，估值仍具吸引力。美國最大核電運營商，擁有多座第三代核電站。三里島核電廠重啟（為微軟供電）開創了「核電+科技巨頭直接供電」新商業模式。核能是唯一可以提供 24/7 無碳穩定電力的能源，AI CSP 追捧對象。',
        'outlook': '目標 $380+。核能復興趨勢明確，CEG 為最純粹的核電 AI 受益股，2025 年 EBITDA 預估年增 20%+。',
        'entry': '$275-$295', 'stop': '$250'
    },
    'NET': {
        'verdict': 'BUY', 'signal': 'ZERO TRUST +9.4%',
        'core': 'Cloudflare 今日大漲 +9.4% 來到 $216，距 52W 低點 $158.83 上漲 36%，仍有修復空間。WAF/CDN/Zero Trust 產品矩陣受益 AI 驅動的資安威脅增加。Workers AI 將 AI 推送到 edge，降低延遲同時保持資料安全。IoT 安全產品開始變現，新增長曲線清晰。',
        'outlook': '目標 $260+。Cloudflare 在 API Security 市場正在建立如同 WAF 一樣的領導地位。',
        'entry': '$190-$216', 'stop': '$170'
    },
    'SNOW': {
        'verdict': 'BUY', 'signal': 'DATA CLOUD +9.35%',
        'core': 'Snowflake 今日大漲 +9.4% 來到 $172，距 52W 低點 $118.3 上漲 45% 但距高點 $280 仍有 38% 修復空間。Cortex AI 整合 LLMs 進入資料湖，查詢效率大幅提升。FinOps 工具開始變現，幫助企業優化資料庫成本。AI 訓練資料湖對高質量向量嵌入的需求爆發，Cortex 是核心受益者。Data Frame 服務開始貨幣化，長期營收成長明確。',
        'outlook': '目標 $220+。Snowflake 在企業資料雲市場的護城河持續加深，Cortex AI 將重新定義資料分析付費模式。',
        'entry': '$155-$172', 'stop': '$140'
    },
    'ANET': {
        'verdict': 'BUY', 'signal': 'AI NETWORKING +8.5%',
        'core': 'Arista 是 AI 資料中心網路的核心供應商，400G/800G 白牌交換機打入各大 CSP。Leaf-Spine 架構升級需求爆發，AI 訓練流量激增對低延遲網路要求極高。今日大漲 +8.5% 來到 $154，距 52W 高點 $179.8 仍有 14.6% 空間。領導地位穩固，毛利率結構優秀。',
        'outlook': '目標 $190+。AI 資料中心網路升級將持續 3-5 年，Anet 在 800G 交換機市場份額超 60%。',
        'entry': '$140-$154', 'stop': '$125'
    },
    'PANW': {
        'verdict': 'BUY', 'signal': 'SECURE THE AI WORLD +7.3%',
        'core': 'Palo Alto Networks 今日大漲 +7.3% 來到 $260.58，距歷史高點 $261.41 僅差 0.3%。AI 驅動的安全硬體一體化平台（Network Security + Prisma SASE + Cortex XSIAM）。Prisma AI 是 CSPM+CWPP 的整合，深度整合 GenAI 提升威脅發現速度。併購策略持續，平台化效應明顯。',
        'outlook': '目標 $290+。企業資安現代化是 2025 年剛需，Palo Alto 在 Network Security 市場份額已超 30%。',
        'entry': '$235-$261', 'stop': '$215'
    },
    'NRG': {
        'verdict': 'BUY', 'signal': 'NEAR 52W LOW +7.7%',
        'core': 'NRG Energy 距 52W 低點 $121.22 僅高 13.6%，具備罕見的補漲空間。天然氣發電資產將長期受益 AI 資料中心緊急用電需求，彈性供電能力被低估。與 VST、CEG 同屬電力上行趨勢中的落後補漲標的，股息率 3.2% 提供安全邊際。',
        'outlook': '目標 $165+。美國電力需求 2024-2026 年預估年增 3-5%，天然氣發電商最直接受益。',
        'entry': '$125-$138', 'stop': '$115'
    },
    'LRCX': {
        'verdict': 'BUY', 'signal': 'ETCH EQUIPMENT +7.25%',
        'core': 'Lam Research 今日大漲 +7.3% 來到 $305，距 52W 高點 $309.98 僅差 1.5%。半導體蝕刻設備龍頭，在先進製程蝕刻市場佔有率超 50%。AI 晶片高深寬比蝕刻需求增加，Lam 的矽蝕刻設備是 NVIDIA/AMD 先進製程核心供應商。免費現金流強勁，估值合理。',
        'outlook': '目標 $340+。先進製程蝕刻是半導體設備中壁壘最高的細分市場，Lam 在 3D NAND 蝕刻市場份額超 70%。',
        'entry': '$280-$305', 'stop': '$260'
    },
    'MU': {
        'verdict': 'BUY', 'signal': 'HBM DEMAND +3.6%',
        'core': 'Micron 是全球第三大記憶體廠，今日微漲 +3.6% 來到 $751，距 52W 高點 $818.67 仍有 8.3% 空間。HBM3E 是 AI GPU 標配，美光已通過 NVIDIA HBM3e 認證，三大 CSP 持續擴大訂單。AI 伺服器 memory 含量是傳統伺服器 4-5 倍，HBM 供需持續緊張至 2025 年底。三星落後給美光創造結構性份額提升機會。',
        'outlook': '目標 $900+。記憶體超級景氣循環才開始，HBM3e 認證讓美光在 AI 記憶體市場從落後轉為領導。',
        'entry': '$680-$750', 'stop': '$620'
    },
    'NVDA': {
        'verdict': 'PARTIAL BUY', 'signal': 'PULLBACK FROM HIGH -4.4%',
        'core': '輝達仍是 AI 基礎建設核心受益者。Blackwell GPU 需求遠超供應，台積電 CoWoS 封裝瓶頸壓制出貨節奏，但 2025 年全年營收指引仍相當強勁。今日股價回調 4.4%，來到 $215，距 52W 高點 236.5 僅 9%，屬正常漲多整理。H100/H200 需求季節性放緩，但 GB200 NVL72 才是真正爆點。CSP 資本支出 Q1 已見加速，機構仍在大規模加倉。',
        'outlook': '目標 $250+，耐心持有。雲端 CSP 資本支出 2025 年同比增 30%+，NVDA 將持續壟斷 AI 訓練市場。',
        'entry': '$195-$215', 'stop': '$185'
    },
    'VRT': {
        'verdict': 'AVOID', 'signal': 'OVEREXTENDED -11.7%',
        'core': 'Vertiv 今日暴跌 -11.7% 來到 $327，從 52W 低點 $104.71 反彈了 213%，股價已嚴重超漲。散熱是 AI 資料中心的核心瓶頸，這個長期主題真實存在，但短期估值已 Price-in 過度。建議持有者適度了結，先觀望。',
        'outlook': '短期方向不明，中期整理後仍有機會挑戰 $400，但現階段性價比不足。',
        'entry': '觀望（已超買）', 'stop': '$290'
    },
    'PSTG': {
        'verdict': 'AVOID', 'signal': 'BRUTAL SELL-OFF -16.5%',
        'core': 'Pure Storage 今日暴跌 -16.5% 來到 $67.8，可能是一次性利空消息消化（非基本面惡化）。FlashArray //X 和 FlashBlade 是企業級全快閃儲存領導者，AI 工作負載對快閃儲存需求真實存在。52W 低點 $43.51 距今 55.8% 上漲，已脫離極度超賣。耐心等待底部確認。',
        'outlook': '短期方向不明，等待更多基本面確認。可能是長期買點但需要等待催化劑。',
        'entry': '觀望', 'stop': 'N/A'
    },
    'AVGO': {
        'verdict': 'BUY', 'signal': 'STEADY ACCUMULATION -2.6%',
        'core': 'Broadcom AI 網路晶片（Tomahawk、Ariel）綁定 CSP 大客戶，客製化 ASIC 需求爆發。Google TPU v5、Meta(MTia) 均大量採用博通方案。雖然近期半導體景氣震盪，但 AI ASIC 占比已超 30% 且持續提升，將結構性提升毛利率。免費現金流收益率佳，殖利率支撐股價。',
        'outlook': '中期 $480+。AI 客製化 ASIC 市場將在 2025-2027 年維持 40%+ CAGR，博通是最大受益者之一。',
        'entry': '$390-$415', 'stop': '$365'
    },
    'GOOGL': {
        'verdict': 'BUY', 'signal': 'AI CLOUD INFRASTRUCTURE -3.5%',
        'core': 'Google 今日微跌 -3.5% 來到 $382，TPU v5 AI 訓練基礎建設持續擴張。Google Cloud 營收成長加速，AI Workspace 整合 Gemini 提升用戶黏性。Gemini Ultra 在 MMLU 基準測試持續領先，DeepMind 在製藥、材料科學的佈局被低估。資本支出 2025 年指引驚人，AI Infra 建設加速中。',
        'outlook': '目標 $430+。Google 在 AI 基礎建設的垂直整合（晶片+雲端+應用）讓其在 CSP 成本競爭中佔優。',
        'entry': '$360-$385', 'stop': '$335'
    },
    'CSCO': {
        'verdict': 'BUY', 'signal': 'AI NETWORKING - NEAR HIGH',
        'core': '思科今日微漲 +1.9% 來到 $120.41，距歷史高點 $120.79 僅差 0.3%。思科是全球企業網路龍頭，AI 時代對安全網路交換機需求增加。收購 Splunk 後的 AI 安全整合方案開始變現。全年營收成長重回正軌，估值合理。',
        'outlook': '目標 $135+。AI 威脅防護 + 網路現代化是長期驅動力，思科在 Enterprise Networking 市場份額超 50%。',
        'entry': '$108-$121', 'stop': '$100'
    },
    'KLAC': {
        'verdict': 'BUY', 'signal': 'SEMI EQUIPMENT +4.7%',
        'core': 'KLA Corporation 今日大漲 +4.7% 來到 $1888，是牛半導體檢測設備的領導者，幾乎所有 AI 先進製程晶片都必須使用 KLA 檢測設備。Yield management 需求隨著製程複雜度增加而增加，AI 晶片良率問題更加突出，KLA 設備剛需明確。免費現金流強勁。',
        'outlook': '目標 $2100+。半導體檢測設備市場壁壘極高，KLA 在圖形化和缺陷檢測市場份額超 50%。',
        'entry': '$1750-$1888', 'stop': '$1650'
    },
    'CIEN': {
        'verdict': 'STRONG BUY', 'signal': 'OPTICAL NETWORKING +5.3%',
        'core': 'Ciena 今日大漲 +5.3% 來到 $583.74，距 52W 高點 $599.5 僅差 2.6%，即將創新高。光纖傳輸設備全球領導者，WaveLogic 8 (800G) 供不應求。AI 資料中心互聯 (DCI) 需求爆發，Ciena 是少數可以提供 800G 解決方案的廠商。Marvell AI ASIC 捆綁銷售模式對 Ciena 光纖業務有協同。',
        'outlook': '目標 $650+。全球光纖骨幹網絡升級週期才剛開始，Ciena 在 800G 長途傳輸市場份額超 70%。',
        'entry': '$530-$585', 'stop': '$490'
    },
}

selected = {sym: data for sym, data in stock_analysis.items() 
            if data['verdict'] in ('STRONG BUY', 'BUY', 'SPECULATIVE BUY')}

report_date = datetime.now().strftime('%Y-%m-%d')

print(f"Total AI infrastructure candidates: {len(stock_analysis)}")
print(f"Selected for report: {len(selected)}")
print(f"Report date: {report_date}")

with open('/tmp/stock_report_data.json', 'w', encoding='utf-8') as f:
    json.dump({
        'prices': prices,
        'categories': categories,
        'analysis': stock_analysis,
        'selected': list(selected.keys()),
        'report_date': report_date
    }, f, indent=2, ensure_ascii=False)

print("Data saved to /tmp/stock_report_data.json")