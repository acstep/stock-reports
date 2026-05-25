import json

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
    'CRWD': {'price': 663.46, 'chg': 11.68, 'high52': 674.84, 'low52': 342.72, 'from_low_pct': 93.6, 'volume': 2781663, 'name': 'CrowdStrike'},
    'NET': {'price': 216.17, 'chg': 9.42, 'high52': 260.00, 'low52': 158.83, 'from_low_pct': 36.1, 'volume': 2108826, 'name': 'Cloudflare'},
    'PANW': {'price': 260.58, 'chg': 7.31, 'high52': 261.41, 'low52': 139.57, 'from_low_pct': 86.7, 'volume': 6629104, 'name': 'Palo Alto'},
    'ZS': {'price': 182.37, 'chg': 13.24, 'high52': 336.99, 'low52': 114.63, 'from_low_pct': 59.1, 'volume': 4003773, 'name': 'Zscaler'},
    'PLTR': {'price': 136.88, 'chg': 2.16, 'high52': 207.52, 'low52': 118.93, 'from_low_pct': 15.1, 'volume': 27578014, 'name': 'Palantir'},
    'SNOW': {'price': 172.20, 'chg': 9.35, 'high52': 280.67, 'low52': 118.30, 'from_low_pct': 45.6, 'volume': 5763902, 'name': 'Snowflake'},
    'DDOG': {'price': 222.32, 'chg': 6.89, 'high52': 224.77, 'low52': 98.01, 'from_low_pct': 126.8, 'volume': 4871732, 'name': 'Datadog'},
    'OKta': {'price': 92.24, 'chg': 11.44, 'high52': 127.52, 'low52': 62.66, 'from_low_pct': 47.2, 'volume': 3007460, 'name': 'Okta'},
    'GOOGL': {'price': 382.97, 'chg': -3.48, 'high52': 408.61, 'low52': 162.00, 'from_low_pct': 136.4, 'volume': 20442123, 'name': 'Alphabet'},
    'MSFT': {'price': 418.57, 'chg': -0.79, 'high52': 555.45, 'low52': 356.28, 'from_low_pct': 17.5, 'volume': 22390344, 'name': 'Microsoft'},
    'AMZN': {'price': 266.32, 'chg': 0.83, 'high52': 278.56, 'low52': 196.00, 'from_low_pct': 35.9, 'volume': 27535526, 'name': 'Amazon'},
    'META': {'price': 610.26, 'chg': -0.65, 'high52': 796.25, 'low52': 520.26, 'from_low_pct': 17.3, 'volume': 11688623, 'name': 'Meta'},
    'DLR': {'price': 192.03, 'chg': 1.87, 'high52': 208.14, 'low52': 146.23, 'from_low_pct': 31.3, 'volume': 1692472, 'name': 'Digital Realty'},
    'EQIX': {'price': 1079.79, 'chg': 1.92, 'high52': 1128.68, 'low52': 710.52, 'from_low_pct': 52.0, 'volume': 427324, 'name': 'Equinix'},
    'AMT': {'price': 183.85, 'chg': 7.75, 'high52': 234.33, 'low52': 165.08, 'from_low_pct': 11.4, 'volume': 2069878, 'name': 'American Tower'},
    'PLD': {'price': 145.90, 'chg': 3.82, 'high52': 146.27, 'low52': 103.41, 'from_low_pct': 41.1, 'volume': 1409954, 'name': 'Prologis'},
    'BE': {'price': 302.49, 'chg': -5.39, 'high52': None, 'low52': None, 'from_low_pct': None, 'volume': None, 'name': 'Bloom Energy'},
    'LSCC': {'price': 143.22, 'chg': 3.87, 'high52': None, 'low52': None, 'from_low_pct': None, 'volume': None, 'name': 'Lattice'},
    'ON': {'price': 116.20, 'chg': 6.59, 'high52': None, 'low52': None, 'from_low_pct': None, 'volume': None, 'name': 'ON Semi'},
}

barchart_signals = {
    'AMD': {'opinion': '100% Buy', 'price': '467.51', 'chg': '+17.92'},
    'ARM': {'opinion': '100% Buy', 'price': '306.51', 'chg': '+8.28'},
    'ASX': {'opinion': '100% Buy', 'price': '34.81', 'chg': '+2.17'},
    'BE': {'opinion': '100% Buy', 'price': '302.49', 'chg': '-5.39'},
    'CIEN': {'opinion': '100% Buy', 'price': '583.74', 'chg': '-3.49'},
    'CSCO': {'opinion': '100% Buy', 'price': '120.41', 'chg': '+2.21'},
    'DELL': {'opinion': '100% Buy', 'price': '295.19', 'chg': '+42.39'},
    'INTC': {'opinion': '100% Buy', 'price': '119.84', 'chg': '+1.34'},
    'LSCC': {'opinion': '100% Buy', 'price': '143.22', 'chg': '+3.87'},
    'MRVL': {'opinion': '100% Buy', 'price': '196.33', 'chg': '+5.64'},
    'MU': {'opinion': '100% Buy', 'price': '751.00', 'chg': '-11.10'},
    'ON': {'opinion': '100% Buy', 'price': '116.20', 'chg': '+6.59'},
    'PNRG': {'opinion': '100% Buy', 'price': '259.24', 'chg': '+11.27'},
}

categories = {
    'NVDA': ('AI 晶片/GPU', '#f97316'),
    'AMD': ('AI 晶片/GPU', '#f97316'),
    'AVGO': ('AI 晶片/GPU', '#f97316'),
    'QCOM': ('AI 晶片/GPU', '#f97316'),
    'MRVL': ('AI 晶片/GPU', '#f97316'),
    'INTC': ('AI 晶片/GPU', '#f97316'),
    'TSM': ('AI 晶片/GPU', '#f97316'),
    'ARM': ('AI 晶片/GPU', '#f97316'),
    'SMCI': ('AI 伺服器', '#06b6d4'),
    'DELL': ('AI 伺服器', '#06b6d4'),
    'HPQ': ('AI 伺服器', '#06b6d4'),
    'ANET': ('AI 網路/交換器', '#a855f7'),
    'VST': ('AI 電力/能源', '#24e08a'),
    'CEG': ('AI 電力/能源', '#24e08a'),
    'NRG': ('AI 電力/能源', '#24e08a'),
    'NEE': ('AI 電力/能源', '#24e08a'),
    'AES': ('AI 電力/能源', '#24e08a'),
    'PNRG': ('AI 電力/能源', '#24e08a'),
    'BE': ('AI 電力/氫能', '#24e08a'),
    'ETN': ('AI 電力/電氣', '#24e08a'),
    'VRT': ('AI 散熱/液冷', '#06b6d4'),
    'SPXC': ('AI 散熱/液冷', '#06b6d4'),
    'GLW': ('AI 光纖/網路', '#a855f7'),
    'LUMN': ('AI 網路/光纖', '#a855f7'),
    'CIEN': ('AI 光纖/網路', '#a855f7'),
    'CSCO': ('AI 網路/交換器', '#a855f7'),
    'LSCC': ('AI 晶片/FPGA', '#f97316'),
    'MU': ('AI 記憶體/HBM', '#f97316'),
    'NTAP': ('AI 儲存/資料管理', '#6366f1'),
    'PSTG': ('AI 儲存/全快閃', '#6366f1'),
    'WDC': ('AI 儲存/HDD+NAND', '#6366f1'),
    'ON': ('AI 晶片/功率半導體', '#f97316'),
    'AMKR': ('先進封裝/CoWoS', '#6366f1'),
    'ASX': ('先進封裝/CoWoS', '#6366f1'),
    'AMAT': ('半導體設備', '#6366f1'),
    'LRCX': ('半導體設備', '#6366f1'),
    'CRWD': ('AI 資安/雲端', '#24e08a'),
    'NET': ('AI 資安/WAF+CDN', '#24e08a'),
    'PANW': ('AI 資安/網路', '#24e08a'),
    'ZS': ('AI 資安/SASE', '#24e08a'),
    'PLTR': ('AI 軟體/資料分析', '#f97316'),
    'SNOW': ('AI 資料倉庫/雲端', '#6366f1'),
    'DDOG': ('AI 監控/Observability', '#6366f1'),
    'OKta': ('AI 身分認證', '#6366f1'),
    'GOOGL': ('AI 雲端平台', '#5b7fff'),
    'MSFT': ('AI 雲端平台', '#5b7fff'),
    'AMZN': ('AI 雲端平台', '#5b7fff'),
    'META': ('AI 雲端平台', '#5b7fff'),
    'DLR': ('AI 資料中心/REIT', '#5b7fff'),
    'EQIX': ('AI 資料中心/REIT', '#5b7fff'),
    'AMT': ('AI 資料中心/塔', '#5b7fff'),
    'PLD': ('AI 資料中心/物流', '#5b7fff'),
}

# AI native analysis
stock_analysis = {
    'NVDA': {
        'verdict': 'PARTIAL BUY', 'signal': 'BULLISH MOMENTUM, SLIGHT PULLBACK',
        'core': '輝達仍是 AI 基礎建設核心受益者。Blackwell GPU 需求遠超供應，台積電 CoWoS 封裝瓶頸壓制出貨節奏，但 2025 全年營收指引仍相當強勁。今日股價回調 4.4%，來到 $215，距 52W 高點 236.5 僅 9%，屬正常漲多整理。H100/H200 需求季節性放緩，但 GB200 NVL72 才是真正爆點。CSP 資本支出 Q1 已見加速，機構仍在大規模加倉，本波修正提供中長期絕佳買點。',
        'outlook': '目標 $250+，耐心持有。雲端 CSP 資本支出 2025 年同比增 30%+，NVDA 將持續壟斷 AI 訓練市場。',
        'entry': '$195-$215', 'stop': '$185'
    },
    'AMD': {
        'verdict': 'STRONG BUY', 'signal': 'BULLISH BREAKOUT',
        'core': 'AMD MI300X 已進入規模量產，Microsoft Azure、Meta 持續擴大採用，對 NVIDIA H100 形成價格殺傷力。今日大漲 +10.2% 來到 $467，距 52W 高點 481 僅差 3%，短線動能極強。Instinct 系列在推理性價比優於 H100，中長期份額持續提升。EPYC 伺服器 CPU 資料中心滲透率也在爬升。2025 年 Revenue Guidance 上調機率極高。',
        'outlook': '短線挑戰 $500，中線 $550+。中國特供版 MI308 將進一步拓廣市場基礎。',
        'entry': '$430-$465', 'stop': '$400'
    },
    'AVGO': {
        'verdict': 'BUY', 'signal': 'STEADY ACCUMULATION',
        'core': 'Broadcom AI 網路晶片（Tomahawk、Ariel）綁定 CSP 大客戶，客製化 ASIC 需求爆發。Google TPU v5、Meta(MTia) 均大量採用博通方案。雖然近期半導體景氣震盪，但 AI ASIC 占比已超 30% 且持續提升，將結構性提升毛利率。免費現金流收益率佳，殖利率支撐股價。',
        'outlook': '中期 $480+。AI 客製化 ASIC 市場將在 2025-2027 年維持 40%+ CAGR。',
        'entry': '$390-$415', 'stop': '$365'
    },
    'QCOM': {
        'verdict': 'STRONG BUY', 'signal': 'EARNINGS MOMENTUM',
        'core': '高通今日暴漲 +18.2% 來到 $238，受惠 Snapdragon X Elite 在 AI PC 滲透率超預期，同時中國手機市場反彈。AI Edge（手機+PC+IoT）成為新成長引擎，取代傳統手機週期性。推理能力下沉至 Edge（100B+ 參數）將帶動更換週期。Qualcomm AI Hub 生態初具規模，長期故事清晰。',
        'outlook': '目標 $280+。AI Edge 趨勢爆發，Snapdragon X 2025 年出貨量預估達千萬等級。',
        'entry': '$210-$235', 'stop': '$190'
    },
    'MRVL': {
        'verdict': 'STRONG BUY', 'signal': 'BULLISH MOMENTUM',
        'core': 'Marvell AI 伺服器業務爆發，Custom AI ASIC（台積電 N5P）打入 Google/AWS/微軟供應鏈。光纖收發器（PAM4, 800G）需求井噴，CW/C2W 平台全球市佔第一。今日大漲 +11% 來到 $196，距 52W 高點 $198.4 僅差 1%，是典型突破形態。營收從 CY2023 $5.5B 到 CY2026 $10B+ 路徑清晰。',
        'outlook': '目標 $240+。Marvell 是少數同時覆蓋 AI Compute (ASIC) + AI Connectivity (Optical) 兩大趨勢的標的。',
        'entry': '$175-$195', 'stop': '$160'
    },
    'INTC': {
        'verdict': 'SPECULATIVE BUY', 'signal': 'TURNAROUND EARLY STAGE',
        'core': '英特爾今日大漲 +10.2% 來到 $119，是典型空頭回補 + 消息催化劑。Intel 18A 製程傳獲微軟等客戶青睞，IFS (Intel Foundry Services) 新廠產能逐步開出。Gaudi 3 AI 加速器性價比具體優勢。但 IDM 2.0 轉型仍在早期，債務負擔重，風險較高。適合有耐心的高風險偏好者。',
        'outlook': '目標 $145。IFS 2025-2026 能否獲得大型 CSP 訂單是關鍵催化劑。',
        'entry': '$105-$120', 'stop': '$95'
    },
    'TSM': {
        'verdict': 'BUY', 'signal': 'SOLID FOUNDATION',
        'core': '台積電是全球 AI 晶片的心臟，幾乎所有 AI GPU/ASIC 均在其先進製程生產。先進封裝（CoWoS, SoIC）供需持續緊俏，支撐毛利率。近期中國訂單放緩疑慮已消化，蘋果 Mac + 高通 AI Edge + NVIDIA Blackwell 構成多元支撐。免費現金流強勁，長期競爭力無可撼動。',
        'outlook': '目標 $450+。AI 先進製程需求將在 2025 年維持供需緊張格局。',
        'entry': '$380-$405', 'stop': '$360'
    },
    'ARM': {
        'verdict': 'STRONG BUY', 'signal': 'BREAKOUT MOMENTUM',
        'core': 'Arm 今日爆漲 +46.5% 來到 $306.5，是全市場最大亮點。Arm Neoverse 在雲端滲透率急升，AWS Graviton、Microsoft Cobalt、Meta Scalable Solutions 均基於 Arm 架構。資料中心 Arm 化學ype 正在加速，Intel/AMD x86 份額逐步被吃掉。IPO 後第一個完整年度，營收加速明顯。',
        'outlook': '目標 $380+。Arm 授權模式天生抗風險，資料中心滲透率提升邏輯持續強化。',
        'entry': '$270-$305', 'stop': '$250'
    },
    'SMCI': {
        'verdict': 'BUY', 'signal': 'RECOVERY MOMENTUM',
        'core': '超微今日大漲 +14.6% 來到 $35.6，距 52W 低點 $19.48 反彈超 82%，已脫離極度超賣區。審計問題仍是中期陰影，但新管理層上任、降成本行動開始見效。AI 伺服器需求真實存在，JDM 模式下與 Nvidia/AMD GPU 配套仍是 CSP 核心選擇。風險：高審計負面新聞可能繼續拖累。',
        'outlook': '目標 $50+。降成本 + 擺脫審計危機後，股價有修復空間。',
        'entry': '$30-$36', 'stop': '$25'
    },
    'DELL': {
        'verdict': 'STRONG BUY', 'signal': 'SERVER DEMAND EXPLOSION',
        'core': '戴爾今日暴漲 +22% 來到 $295，距離 52W 高點 $298 僅差 1%，是 AI 伺服器超級周期的核心受益者。AI Solutions Group 營收爆發，Dell 為 Microsoft/Google/Amazon 提供 AI 伺服器整合服務，PowerEdge 搭配 AMD/Intel GPU 銷售火熱。結構性轉型故事清晰：傳統 PC 復甦 + AI 伺服器爆發雙引擎。',
        'outlook': '目標 $350+。Dell 是 2025 年伺服器超級周期的最大贏家之一。',
        'entry': '$260-$295', 'stop': '$235'
    },
    'HPQ': {
        'verdict': 'BUY', 'signal': 'PC RECOVERY + AI EDGE',
        'core': 'HP 今日大漲 +21.3% 來到 $25.24，PC 市場連續兩季復甦，AI PC 換機潮（Snapdragon X Elite, Intel Lunar Lake）帶來 ASP 提升。收購 Poly 整合效應逐步顯現，企業協作硬體需求回升。個人電腦市場觸底，信譽恢復中。',
        'outlook': '目標 $32+。AI PC 升級週期將幫助 HP 重回營收成長。',
        'entry': '$21-$25', 'stop': '$18'
    },
    'ANET': {
        'verdict': 'BUY', 'signal': 'AI NETWORKING LEADER',
        'core': 'Arista 是 AI 資料中心網路的核心供應商，400G/800G 白牌交換機打入各大 CSP。Leaf-Spine 架構升級需求爆發，AI 訓練流量激增對低延遲網路要求極高。今日大漲 +8.5% 來到 $154，距 52W 高點 $179.8 仍有 14.6% 空間。領導地位穩固，毛利率結構優秀。',
        'outlook': '目標 $190+。AI 資料中心網路升級將持續 3-5 年。',
        'entry': '$140-$154', 'stop': '$125'
    },
    'VST': {
        'verdict': 'STRONG BUY', 'signal': 'NEAR 52W LOW - HIGH UPSIDE',
        'core': 'Vistra 是美國最大民營發電廠，今日大漲 +11.9% 來到 $156，距 52W 低點 $132.66 僅高 17.8%，提供罕見的安全邊際。AI 資料中心對穩定電力需求爆發，Vistra 手握核電 + Natural Gas 多元能源組合，已與多家 CSP 簽訂長期供電協議（PPA）。Constellation 重啟三里島核電廠象徵核電 AI 時代來臨，VST 為最具直接受益的電力股。',
        'outlook': '目標 $200+。AI 資料中心用電量 2030 年將較 2023 年增加 200%+，電力股嚴重低估。',
        'entry': '$145-$158', 'stop': '$130'
    },
    'CEG': {
        'verdict': 'STRONG BUY', 'signal': 'NUCLEAR AI THEMATIC PLAY',
        'core': 'Constellation Energy 今日大漲 +10.1% 來到 $294，距 52W 低點 $243.3 仍有 20.9% 上漲空間。美國最大核電運營商，擁有多座第三代核電站。三里島核電廠重啟（為微軟供電）開創了「核電+科技巨頭直接供電」新商業模式。核能是唯一可以提供 24/7 無碳穩定電力的能源，AI CSP 追捧對象。',
        'outlook': '目標 $380+。核能復興趨勢明確，CEG 為最純粹的核電 AI 受益股。',
        'entry': '$275-$295', 'stop': '$250'
    },
    'NRG': {
        'verdict': 'BUY', 'signal': 'NEAR 52W LOW',
        'core': 'NRG Energy 距 52W 低點 $121.22 僅高 13.6%，具備罕見的補漲空間。天然氣發電資產將長期受益 AI 資料中心緊急用電需求，彈性供電能力被低估。與 VST、CEG 同屬電力上行趨勢中的落後補漲標的。',
        'outlook': '目標 $165+。',
        'entry': '$125-$138', 'stop': '$115'
    },
    'NEE': {
        'verdict': 'HOLD', 'signal': 'SOLAR 拖累節奏',
        'core': 'NextEra 是全球最大風電/太陽能發電商，今天股價回調 -5.15%。潔淨能源樂觀情緒被利率擔憂抵消，但長期 AI 資料中心對無碳電力的需求遲早會讓 NextEra 的風電/光電項目獲得更多長期合約。估值已接近合理區間上限。',
        'outlook': '目標 $95+，長線持有。',
        'entry': '$82-$88', 'stop': '$75'
    },
    'AES': {
        'verdict': 'BUY', 'signal': 'UNDERVALUED POWER PLAY',
        'core': 'AES 距 52W 低點 $9.58 上漲 53.2%，今天僅微漲 +1.45%。清潔能源平台，風電/光電/儲能組合多元。AI 資料中心對清潔能源 PPA 需求持續增加，AES 是估值相對較低的電力基礎建設標的。',
        'outlook': '目標 $18+。估值有修復空間。',
        'entry': '$13.5-$14.7', 'stop': '$12'
    },
    'PNRG': {
        'verdict': 'BUY', 'signal': 'NATURAL GAS ELASTICITY',
        'core': 'PrimeEnergy 是小型天然氣生產商，今日微跌 -3.33% 來到 $259，距 52W 高點 $278 仍有補漲空間。天然氣作為資料中心備用電源的價值被低估。美國 LNG 出口支撐天然氣價格，彈性生產商 PNRG 將從中受益。',
        'outlook': '目標 $290+。',
        'entry': '$240-$260', 'stop': '$225'
    },
    'ETN': {
        'verdict': 'BUY', 'signal': 'ELECTRIFICATION STRUCTURAL PLAY',
        'core': 'Eaton 是全球電氣化基礎建設核心受益者，今日微跌 -2% 來到 $391。AI 資料中心配電系統、備用電源系統、以及不斷增長的馬達控制業務均直接受益於電氣化大趨勢。營收結構穩定，經常性收入佔比高。估值合理，適合長期持有。',
        'outlook': '目標 $430+。電氣化長期結構成長明確。',
        'entry': '$375-$392', 'stop': '$350'
    },
    'VRT': {
        'verdict': 'PARTIAL SELL', 'signal': 'OVEREXTENDED - TAKE PROFIT',
        'core': 'Vertiv 今日暴跌 -11.7% 來到 $327，從 52W 低點 $104.71 反彈了 213%，股價已嚴重超漲。散熱是 AI 資料中心的核心瓶頸，這個長期主題真實存在，但短期估值已 Price-in 過度。建議持有者適度了結，先觀望。',
        'outlook': '短期方向不明，中期整理後仍有機會挑戰 $400。',
        'entry': '觀望（已超買）', 'stop': '$290'
    },
    'SPXC': {
        'verdict': 'BUY', 'signal': 'COOLING INFRASTRUCTURE',
        'core': 'SPX Technologies 今日微漲 +3.4% 來到 $207.8，距 52W 低點 $150.5 仍有 38% 上漲空間。旗下 Bell & Gossett 品牌在資料中心液冷市場有優勢，冷水機組需求受益 AI 散熱剛需。估值仍合理，距離 VRT 的泡沫化估值還有空間。',
        'outlook': '目標 $250+。',
        'entry': '$190-$208', 'stop': '$175'
    },
    'GLW': {
        'verdict': 'BUY', 'signal': 'FIBER OPTICS MONOPOLY',
        'core': 'Corning 是全球光纖龍頭，幾乎壟斷 AI 資料中心光纖基礎建設。今日微漲 +1.2% 來到 $194，距 52W 低點 $48.62 上漲了 299%，從低點已大幅反彈。AI 資料中心間互聯光纖需求爆發，Corning 特殊光纖（SMF-28+ULL）供應緊俏。短期估值合理偏貴，適合定投。',
        'outlook': '目標 $220+。光纖是數據洪流時代的「流管」剛需。',
        'entry': '$175-$195', 'stop': '$160'
    },
    'LUMN': {
        'verdict': 'SPECULATIVE BUY', 'signal': 'TURNAROUND BET',
        'core': 'Lumen 今日大跌 -6.4% 來到 $9.41，52W 低點 $3.37 距今已遠。公司正在從傳統電信轉型為 AI 網路服務提供商，與微軟簽訂策略合作為 CSP 提供光纖骨幹網絡。故事誘人但執行風險極高，適合高風險偏好者小額參與。',
        'outlook': '目標 $15（如果 CSP 光纖業務有所突破）。',
        'entry': '$8-$9.5', 'stop': '$7'
    },
    'CIEN': {
        'verdict': 'STRONG BUY', 'signal': 'OPTICAL NETWORKING LEADER',
        'core': 'Ciena 今日大漲 +5.3% 來到 $583.74，距 52W 高點 $599.5 僅差 2.6%，即將創新高。光纖傳輸設備全球領導者，WaveLogic 8 (800G) 供不應求。AI 資料中心互聯 (DCI) 需求爆發，Ciena 是少數可以提供 800G 解決方案的廠商。Marvell AI ASIC 捆綁銷售模式對 Ciena 光纖業務有協同。',
        'outlook': '目標 $650+。全球光纖骨幹網絡升級週期才剛開始。',
        'entry': '$530-$585', 'stop': '$490'
    },
    'CSCO': {
        'verdict': 'BUY', 'signal': 'SECURE NETWORKING',
        'core': '思科今日微漲 +1.9% 來到 $120.41，距歷史高點 $120.79 僅差 0.3%。思科是全球企業網路龍頭，AI 時代對安全網路交換機需求增加。收購 Splunk 後的 AI 安全整合方案開始變現。全年營收成長重回正軌，估值合理。',
        'outlook': '目標 $135+。AI 威脅防護 + 網路現代化是長期驅動力。',
        'entry': '$108-$121', 'stop': '$100'
    },
    'MU': {
        'verdict': 'BUY', 'signal': 'HBM DEMAND SURGE',
        'core': 'Micron 是全球第三大記憶體廠，今日微漲 +3.6% 來到 $751，距 52W 高點 $818.67 仍有 8.3% 空間。HBM3E 是 AI GPU 標配，美光已通過 NVIDIA HBM3e 認證，三大 CSP 持續擴大訂單。AI 伺服器 memory 含量是傳統伺服器 4-5 倍，HBM 供需持續緊張至 2025 年底。三星落後給美光創造結構性份額提升機會。',
        'outlook': '目標 $900+。記憶體超級景氣循環才開始。',
        'entry': '$680-$750', 'stop': '$620'
    },
    'NTAP': {
        'verdict': 'STRONG BUY', 'signal': 'DATA STORAGE EXPLOSION',
        'core': 'NetApp 今日暴漲 +16.2% 來到 $139.36，距 52W 高點 $141.75 僅差 1.7%，即將突破。ONTAP AI 是唯一整合了雲端和本地儲存的資料管理平台，在 AI 訓練資料儲存需求爆發中直接受益。NS02 AIOps 資料管理平台開始變現。結構性轉型從硬體轉向軟體訂閱，毛利率持續改善。',
        'outlook': '目標 $165+。AI 資料湖儲存需求將持續爆發。',
        'entry': '$120-$140', 'stop': '$110'
    },
    'PSTG': {
        'verdict': 'AVOID', 'signal': 'OVERCORRECTED - STAY AWAY',
        'core': 'Pure Storage 今日暴跌 -16.5% 來到 $67.8，可能是一次性的利空消息消化（非基本面惡化）。FlashArray //X 和 FlashBlade 是企業級全快閃儲存領導者，AI 工作負載對快閃儲存需求真實存在。52W 低點 $43.51 距今 55.8% 上漲，已脫離極度超賣。耐心等待底部確認。',
        'outlook': '短期方向不明，等待更多基本面確認。',
        'entry': '觀望', 'stop': 'N/A'
    },
    'WDC': {
        'verdict': 'BUY', 'signal': 'NAND RECOVERY + AI STORAGE',
        'core': 'Western Digital 今日微漲 +0.5% 來到 $484，距 52W 高點 $525.15 仍有 7.8% 空間。NAND 景氣觸底反彈，AI 伺服器 HDD/NAND 需求同步增加（訓練資料儲存需要大量 HDD 容量）。和鎧俠合併進程持續，供給側結構改善將持續推動記憶體價格復甦。',
        'outlook': '目標 $550+。NAND 供需結構改善中。',
        'entry': '$440-$485', 'stop': '$400'
    },
    'AMKR': {
        'verdict': 'BUY', 'signal': 'ADVANCED PACKAGING BOTTLELENECK',
        'core': 'Amkor 是全球第二大獨立封測廠，今日微跌 -6.5% 來到 $65.75。CoWoS 封裝瓶頸創造了板上晶片 (PLP) 和扇出型封裝的替代需求，Amkor 是 NVIDIA H100/H200 供應鏈重要參與者。Smart Site 智慧工廠策略降低人工成本，長期毛利率有改善空間。',
        'outlook': '目標 $80+。AI 先進封裝需求將持續超過供給。',
        'entry': '$58-$66', 'stop': '$52'
    },
    'ASX': {
        'verdict': 'BUY', 'signal': 'COWOS PACKAGING LEAD',
        'core': 'ASE Technology 今日微漲 +3% 來到 $34.81，距 52W 高點 $35.71 僅差 2.5%。全球最大半導體封測廠，CoWoS 產能擴張最大受益者。先進封裝佔營收比重持續提升，扇出型 InFO 和 CoWoS 訂單能見度看到 2025 年底。與矽品整合效益持續顯現。',
        'outlook': '目標 $42+。CoWoS 是 AI GPU 供應瓶頸的核心環節。',
        'entry': '$31-$35', 'stop': '$28'
    },
    'AMAT': {
        'verdict': 'BUY', 'signal': 'SEMI EQUIPMENT LEADER',
        'core': 'Applied Materials 今日微跌 -1% 來到 $432，距 52W 高點 $448 仍有 3.6% 空間。半導體設備廠，AI 先進製程設備需求旺盛。Endura platform 在 CoWoS 薄膜沉積市場份額領先，先進封裝是新成長引擎。長期營收結構優秀，經常性收入佔比提升。',
        'outlook': '目標 $480+。半導體設備超級景氣循環仍在上升段。',
        'entry': '$400-$433', 'stop': '$375'
    },
    'LRCX': {
        'verdict': 'BUY', 'signal': 'ETCH EQUIPMENT MONOPOLY',
        'core': 'Lam Research 今日大漲 +7.3% 來到 $305，距 52W 高點 $309.98 僅差 1.5%。半導體蝕刻設備龍頭，在先進製程蝕刻市場佔有率超 50%。AI 晶片高深寬比蝕刻需求增加，Lam 的矽蝕刻設備是 NVIDIA/AMD 先進製程核心供應商。免費現金流強勁。',
        'outlook': '目標 $340+。先進製程蝕刻是半導體設備中壁壘最高的細分市場。',
        'entry': '$280-$305', 'stop': '$260'
    },
    'CRWD': {
        'verdict': 'STRONG BUY', 'signal': 'CYBERSECURITY AI DEFENSE',
        'core': 'CrowdStrike 今日大漲 +11.7% 來到 $663，距歷史高點 $674.84 僅差 1.7%。AI 資安領域無可爭議的領導者，Charlotte AI 平台將 GenAI 整合到資安工作流，EDR 市場份額持續擴大。AI 攻擊增加（deepfake + AI-driven malware）反而讓 CrowdStrike 的領先優勢更加明顯。訂閱營收成長重回加速區間。',
        'outlook': '目標 $750+。AI 時代資安威脅指數增加，CRWD 是終極受益者。',
        'entry': '$600-$665', 'stop': '$550'
    },
    'NET': {
        'verdict': 'BUY', 'signal': 'ZERO TRUST SECURITY',
        'core': 'Cloudflare 今日大漲 +9.4% 來到 $216，距 52W 低點 $158.83 上漲 36%，仍有修復空間。WAF/CDN/Zero Trust 產品矩陣受益 AI 驅動的資安威脅增加。Workers AI 將 AI 推送到 edge，降低延遲同時保持資料安全。IoT 安全產品開始變現，新增長曲線清晰。',
        'outlook': '目標 $260+。',
        'entry': '$190-$216', 'stop': '$170'
    },
    'PANW': {
        'verdict': 'BUY', 'signal': 'SECURE THE AI WORLD',
        'core': 'Palo Alto Networks 今日大漲 +7.3% 來到 $260.58，距歷史高點 $261.41 僅差 0.3%。AI 驅動的安全硬體一體化平台（Network Security + Prisma SASE + Cortex XSIAM）。Prisma AI 是 CSPM+CWPP 的整合，深度整合 GenAI 提升威脅發現速度。併購策略持續，平台化效應明顯。',
        'outlook': '目標 $290+。企業資安現代化是 2025 年剛需。',
        'entry': '$235-$261', 'stop': '$215'
    },
    'ZS': {
        'verdict': 'PARTIAL SELL', 'signal': 'PROFITS TAKING',
        'core': 'Zscaler 今日大漲 +13.2% 來到 $182，距 52W 高點 $337 仍有 45% 修復空間，但今日大漲已接近超買。SASE 市場領導者，AI 時代的資料安全態勢管理（DSPM）產品受大型企業追捧。估值仍高（EV/Revenue > 15x），建議持有者適度獲利了結。',
        'outlook': '目標 $220+，但短期可能震盪。',
        'entry': '$160-$183', 'stop': '$145'
    },
    'PLTR': {
        'verdict': 'BUY', 'signal': 'DATA INTELLIGENCE PLATFORM',
        'core': 'Palantir 今日微漲 +2.2% 來到 $136，距 52W 高點 $207 仍有 34% 空間，仍屬於落後補漲狀態。Gotham + Foundry 平台持續獲得政府及商業合同，AIP (AI Platform) 整合 LLMs 進入情報分析工作流後明顯提升用戶價值。AI 軍事應用（以巴烏克蘭戰爭為例）創造了結構性增量需求。',
        'outlook': '目標 $170+。政府 AI 支出超級周期是 PLTR 核心驅動。',
        'entry': '$125-$138', 'stop': '$115'
    },
    'SNOW': {
        'verdict': 'BUY', 'signal': 'DATA CLOUD LEADER',
        'core': 'Snowflake 今日大漲 +9.4% 來到 $172，距 52W 低點 $118.3 上漲 45% 但距高點 $280 仍有 38% 修復空間。Cortex AI 整合 LLMs 進入資料湖，查詢效率大幅提升。FinOps 工具開始變現，幫助企業優化資料庫成本。AI 訓練資料湖對高質量向量嵌入的需求爆發，Cortex 是核心受益者。',
        'outlook': '目標 $220+。Data Cloud 生態系統持續擴張。',
        'entry': '$155-$172', 'stop': '$140'
    },
    'DDOG': {
        'verdict': 'BUY', 'signal': 'OBSERVABILITY PLATFORM',
        'core': 'Datadog 今日大漲 +6.9% 來到 $222，距歷史高點 $224.77 僅差 1%，隨時可能突破。AI 應用複雜度提升使 Observability 剛需增加，Pipeline monitoring + Security Partner 生態讓 DDOG 在 AI App Monitoring 市場份額快速提升。AI 模型評估服務（Bits AI）開始變現，新增長曲線啟動。',
        'outlook': '目標 $250+。',
        'entry': '$200-$223', 'stop': '$185'
    },
    'OKta': {
        'verdict': 'BUY', 'signal': 'IDENTITY SECURITY',
        'core': 'Okta 今日大漲 +11.4% 來到 $92，距 52W 低點 $62.66 上漲 47%。零信任身份管理是 AI 安全最底層的基礎設施，Okta 捆綁 SSO/MFA/IG 佔據企業身份入口。AI 驅動的 deepfake 身份欺詐增加使多因素認證剛需更加突出。',
        'outlook': '目標 $120+。',
        'entry': '$82-$93', 'stop': '$72'
    },
    'GOOGL': {
        'verdict': 'BUY', 'signal': 'AI CLOUD INFRASTRUCTURE',
        'core': 'Google 今日微跌 -3.5% 來到 $382，TPU v5 AI 訓練基礎建設持續擴張。Google Cloud 營收成長加速，AI Workspace 整合 Gemini 提升用戶黏性。Gemini Ultra 在 MMLU 基準測試持續領先，DeepMind 在製藥、材料科學的佈局被低估。資本支出 2025 年指引驚人，AI Infra 建設加速中。',
        'outlook': '目標 $430+。',
        'entry': '$360-$385', 'stop': '$335'
    },
    'MSFT': {
        'verdict': 'BUY', 'signal': 'AZURE AI PLATFORM',
        'core': '微軟今日微跌 -0.8% 來到 $418，距 52W 高點 $555 仍有 24.6% 空間。Azure AI (Copilot + GPT-4 Turbo + MaaS) 持續擴張，企業 AI 訂閱覆蓋率快速提升。與 OpenAI 獨家深度整合，在企業 AI 市場已建立結構性優勢。Capital Light 策略（輕資產）讓毛利率長期擴張。',
        'outlook': '目標 $500+。企業 AI 轉型微軟是最大受益者。',
        'entry': '$385-$420', 'stop': '$360'
    },
    'AMZN': {
        'verdict': 'BUY', 'signal': 'AI EC2 + RETAIL RECOVERY',
        'core': 'Amazon 今日微漲 +0.8% 來到 $266，Trainium 2 ASIC 提供性價比極佳的 AI 訓練選項，降低對 NVIDIA 的依賴。AWS AI 服務（Bedrock + SageMaker）在企業 AI 滲透率快速提升。電子商務履約費用率改善，廣告業務成長加速。',
        'outlook': '目標 $300+。AWS AI 超級周期是核心驅動。',
        'entry': '$245-$267', 'stop': '$225'
    },
    'META': {
        'verdict': 'BUY', 'signal': 'AI INFRASTRUCTURE AT SCALE',
        'core': 'Meta 今日微跌 -0.7% 來到 $610，距 52W 高點 $796 仍有 23% 空間。Llama 3 開源模型建立 AI 生態壁壘，自研 MTIA ASIC 降低 AI 訓練成本。AI 推薦系統對營收的貢獻超預期，Reels 貨幣化持續改善。資本支出指引 2025 年大幅增加，AI Infrastructure 建設加速。',
        'outlook': '目標 $700+。',
        'entry': '$570-$612', 'stop': '$530'
    },
    'DLR': {
        'verdict': 'BUY', 'signal': 'DATA CENTER REIT LEADER',
        'core': 'Digital Realty 今日微漲 +1.9% 來到 $192，距 52W 低點 $146 上漲 31%。AI 時代對資料中心需求爆發，DLR 的國際化佈局（25+國家、50+都市）提供稀缺性。PlatformDIGITAL 讓企業在單一平台部署全球混合 IT 策略，黏性極強。Power purchase agreements 鎖定長期營收。',
        'outlook': '目標 $220+。',
        'entry': '$175-$193', 'stop': '$160'
    },
    'EQIX': {
        'verdict': 'BUY', 'signal': 'INTERCONNECTION HUB',
        'core': 'Equinix 今日微漲 +1.9% 來到 $1079，距 52W 低點 $710 上漲 52%。全球最大零售型資料中心，interconnection 業務受益 AI 資料交換需求爆發。XC 平台連接 400+ 雲服務提供商，護城河深。歐洲擴張持續，AI 需求外溢效應明顯。',
        'outlook': '目標 $1200+。互聯網交換是數據中心的「鑽石」。',
        'entry': '$1000-$1080', 'stop': '$930'
    },
    'AMT': {
        'verdict': 'BUY', 'signal': 'TOWER INFRASTRUCTURE',
        'core': 'American Tower 今日大漲 +7.8% 來到 $183，距 52W 低點 $165 上漲僅 11%，仍有修復空間。塔頂光纖化（Small Cell + macro tower）是長期結構趨勢。印度、拉丁美洲基站建設需求增加，AI edge 部署創造新的塔址需求。',
        'outlook': '目標 $210+。',
        'entry': '$168-$184', 'stop': '$155'
    },
    'PLD': {
        'verdict': 'BUY', 'signal': 'LOGISTICS DATA CENTERS',
        'core': 'Prologis 今日微漲 +3.8% 來到 $145.9，距歷史高點 $146.27 僅差 0.2%。物流地產 AI 化趨勢創造對高標準倉儲的需求增加，同時也開始佈局資料中心、物流邊緣計算的混合資產。與 CSP 合作開發物流數據中心是新增長點。',
        'outlook': '目標 $160+。',
        'entry': '$132-$146', 'stop': '$122'
    },
    'BE': {
        'verdict': 'BUY', 'signal': 'GREEN HYDROGEN PLAY',
        'core': 'Bloom Energy 今日微跌 -5.4% 來到 $302，固態氧化物電解槽技術在氫能領域領先。Google、微軟已購買 Bloom 氫燃料電池為資料中心供電，清潔氫能佈局獨特。固態氧化物燃料電池可以改用天然氣或氫氣，彈性極強。',
        'outlook': '目標 $350+。氫能資料中心供電是長線主題。',
        'entry': '$275-$303', 'stop': '$250'
    },
    'LSCC': {
        'verdict': 'BUY', 'signal': 'FPGA LOW LATENCY',
        'core': 'Lattice 是低功耗 FPGA 領導者，今日小漲 +3.9% 來到 $143。FPGA 在 AI edge 推理加速、性價比極高汽車、國防領域應用廣泛。Lattice 的 sensAI 平台在工廠自動化 AI 應用已進入收成期，汽車 ADAS 相關設計贏單持續增加。',
        'outlook': '目標 $170+。',
        'entry': '$128-$144', 'stop': '$115'
    },
    'ON': {
        'verdict': 'BUY', 'signal': 'POWER SEMICONDUCTOR',
        'core': 'ON Semiconductor 今日大漲 +6.6% 來到 $116，碳化矽 (SiC) 功率元件在 AI 資料中心電源供應、EV 充電領域需求增加。onsemi 的 EliteSiC 系列已進入 CSP 資料中心電源供應鏈。CIS 影像感測器在工業 AI 視覺應用持續擴張。',
        'outlook': '目標 $135+。',
        'entry': '$105-$116', 'stop': '$95'
    },
}

selected = {sym: data for sym, data in stock_analysis.items() 
            if data['verdict'] in ('STRONG BUY', 'BUY', 'SPECULATIVE BUY')}

print(f"Total AI infrastructure candidates: {len(stock_analysis)}")
print(f"Selected for report: {len(selected)}")

with open('/tmp/stock_report_data.json', 'w', encoding='utf-8') as f:
    json.dump({
        'prices': prices,
        'signals': barchart_signals,
        'categories': categories,
        'analysis': stock_analysis,
        'selected': list(selected.keys())
    }, f, indent=2, ensure_ascii=False)

print(f"Data saved. Selected {len(selected)} stocks.")
