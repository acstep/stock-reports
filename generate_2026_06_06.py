#!/usr/bin/env python3
"""Generate 2026-06-06 AI Infrastructure Stock Research Report"""
import json
from datetime import datetime

# Load basic market data
with open('/tmp/ai_basic_data.json') as f:
    market = json.load(f)

# Helper: build Barchart link
def bc(sym):
    return f'https://www.barchart.com/stocks/quotes/{sym}/overview'

# ========== CATEGORIES ==========
# Each stock: symbol -> dict of metadata + analysis
CATEGORIES = {
    'chip': {
        'icon': '💾', 'name': 'AI 晶片/GPU',
        'stocks': ['NVDA', 'AMD', 'AVGO', 'MRVL', 'ARM', 'MU', 'ALAB', 'INTC', 'QCOM', 'TSM']
    },
    'server': {
        'icon': '🖥️', 'name': 'AI 伺服器/雲端',
        'stocks': ['SMCI', 'DELL', 'HPE', 'ORCL', 'IBM', 'CRWV']
    },
    'power': {
        'icon': '⚡', 'name': 'AI 電力/能源',
        'stocks': ['VST', 'CEG', 'ETN', 'VRT', 'NRG', 'NEE', 'BE']
    },
    'cooling': {
        'icon': '🧊', 'name': 'AI 散熱/液冷',
        'stocks': ['SPXC', 'VRT', 'TT']
    },
    'network': {
        'icon': '📡', 'name': 'AI 網路/光纖',
        'stocks': ['ANET', 'CSCO', 'CIEN', 'GLW', 'LUMN', 'NET']
    },
    'storage': {
        'icon': '💾', 'name': 'AI 儲存/記憶體',
        'stocks': ['MU', 'NTAP', 'WDC', 'STX', 'SNDK', 'PSTG']
    },
    'packaging': {
        'icon': '📦', 'name': 'AI 先進封裝/CoWoS',
        'stocks': ['AMKR', 'ASX', 'AMAT', 'KLAC', 'LRCX']
    },
    'security': {
        'icon': '🔐', 'name': 'AI 資安/雲端',
        'stocks': ['CRWD', 'PANW', 'ZS', 'FTNT', 'S', 'NET']
    },
    'software': {
        'icon': '🤖', 'name': 'AI 軟體/資料分析',
        'stocks': ['PLTR', 'SNOW', 'DDOG', 'MDB', 'ESTC']
    },
    'cloud': {
        'icon': '☁️', 'name': 'AI 雲端平台',
        'stocks': ['GOOGL', 'MSFT', 'AMZN', 'META', 'AAPL', 'ORCL']
    },
    'infra': {
        'icon': '🏭', 'name': 'AI 基礎建設其他',
        'stocks': ['SIEGY', 'ALFVY']
    },
}

# ========== AI PICKS - DETAILED ANALYSIS ==========
# 38 final picks, each with: score (1-10), why_pick, core_logic, future_view, risk, target_upside_pct, analyst_target, analysts
PICKS = {
    'NVDA': {
        'score': 9, 'cat': 'chip',
        'why': 'AI GPU 龍頭地位無可撼動。週五大跌 6.2% 至 $205，分析師仍給 62 個 Strong Buy 共識，目標價中位數 $288（+40%）。H100/H200/B200/B300 仍持續主導 AI 訓練市場，Blackwell 出貨進入爆發期。',
        'logic': '1) 2026 財年營收預估 $391B（年增 81%），EPS $8.94（年增 87%），2027 財年再成長 40%。2) Rubin 系列 2026 H2 接力，繼續維持 1 年一代的製程領先。3) 網路/汽車/機器人新市場打開。',
        'outlook': '短線修正為加碼機會。中長期目標價 $288-$350（Bank of America 樂觀給 $350），距當前有 40-70% 上漲空間。',
        'risk': '估值已反映高成長預期，毛利率波動、客戶集中度（超大規模 CSP 占比過高）、Rubin 推遲風險。',
        'target': 298.42, 'analysts': 62, 'consensus': 'Strong Buy', 'entry': 200, 'stop': 180, 'tp': 280
    },
    'AMD': {
        'score': 8, 'cat': 'chip',
        'why': 'AI GPU 第二供應商位置確立。MI300/MI325 系列 2026 進入放量期，週五跌 10.9% 至 $466。51 位分析師中 36 個 Strong Buy，目標價 $479.77（+2.87%）。',
        'logic': '1) 2026 營收預估 $49.4B（年增 43%），EPS $5.43（年增 105%）。2) MI400 系列搭載 HBM4，2026 下半年出貨。3) 微軟/Meta/Oracle 採用擴大。',
        'outlook': '修正後 PE 26x 接近 NVDA。目標價 $480（Evercore $579、Barclays $665）。週五下殺後是相對合理進場點。',
        'risk': '市占率仍遠低於 NVDA，軟體生態（CUDA）落後，毛利率 55% 不到 NVDA 的 75%。',
        'target': 479.77, 'analysts': 51, 'consensus': 'Strong Buy', 'entry': 455, 'stop': 400, 'tp': 540
    },
    'AVGO': {
        'score': 9, 'cat': 'chip',
        'why': '客製化 AI ASIC 霸主，與 Google/ Meta 深度綁定。週五跌 7.9% 至 $385.7，48 位分析師 36 個 Strong Buy，目標價 $512.73（+32.92%）。',
        'logic': '1) 2026 營收預估 $106B（年增 66%），EPS $11.62（年增 70%）。2) AI 營收 2026 Q1 已達 $4.1B，預期 2027 衝 $8B+。3) VMware 收購整合效應釋放。',
        'outlook': 'ASIC 客製化趨勢下，AVGO 將成 NVDA 之外最大受惠者。中長期目標 $525-$582。',
        'risk': '客戶集中度高（Google 占 AI 營收 約 40%）、VMware 整合不確定性、半導體景氣循環。',
        'target': 512.73, 'analysts': 48, 'consensus': 'Strong Buy', 'entry': 380, 'stop': 340, 'tp': 500
    },
    'MU': {
        'score': 9, 'cat': 'chip',
        'why': 'HBM 記憶體三巨頭之一，AI 記憶體超級週期最大受惠者。週五大跌 13.3% 至 $864，44 位分析師 30 個 Strong Buy，目標價 $739（-14%，但高盛、摩根史丹利上看 $1,050+）。',
        'logic': '1) 2026 營收預估 $110B（年增 195%），EPS $58.87（年增 610%）。2) HBM3E 滿載出貨給 NVDA、AMD、Google，HBM4 已進入設計驗證。3) NAND Flash 同步進入缺貨循環。',
        'outlook': '雖分析師目標價中位數低於現價，但長期成長動能無虞。Wells Fargo $550、Raymond James $1,100、摩根史丹利 $1,050。修正後是 5-10 年 AI 記憶體週期的最佳標的。',
        'risk': 'HBM 供應鏈擴張過快，2027 H2 供需可能反轉；HBM4 量產延遲；NAND 價格波動。',
        'target': 739.48, 'analysts': 44, 'consensus': 'Strong Buy', 'entry': 850, 'stop': 720, 'tp': 1100
    },
    'ARM': {
        'score': 8, 'cat': 'chip',
        'why': 'AI 邊緣運算+伺服器 CPU 雙引擎。週五暴跌 12.8% 至 $342，但 25 位分析師中 21 個 Buy，目標價 $272（已過時）。近期升級至 $500（Mizuho）、$410（Wells Fargo）。',
        'logic': '1) 2026 營收預估 $5.97B（年增 21%），EPS $2.17（年增 23%）。2) CSS 運算平台（Neoverse）拿下 AWS Graviton4、Google Axion。3) 智慧手機與車用 AI 授權金持續成長。',
        'outlook': 'Royalty 模式毛利率 95%+，商業模式優異。目標價 $300-$360（Barclays），長期 $500（Mizuho）。',
        'risk': 'AI 伺服器 CPU 滲透率提升慢、智慧手機復甦疲弱、客戶自行設計晶片（Apple）。',
        'target': 272, 'analysts': 25, 'consensus': 'Buy', 'entry': 340, 'stop': 280, 'tp': 420
    },
    'ALAB': {
        'score': 7, 'cat': 'chip',
        'why': 'AI 互連/重定時器晶片純標的，NVDA 供應鏈。週五跌 11.5% 至 $317，26 位分析師共識 $245（-22.7%），但 Evercore 升至 $297 看好。',
        'logic': '1) 2026 營收預估 $1.55B（年增 81%），EPS $3.00（年增 63%）。2) Aries/Condo 為 NVDA 平台標配，滲透率持續提升。3) 光通訊新品切入資料中心。',
        'outlook': 'NVDA AI 機櫃內部互連的關鍵受惠者。目標價 $245-$297。當前 PE 100x+ 反映高成長，但 81% 營收增速可消化估值。',
        'risk': '高度依賴 NVDA 平台（占營收 70%+）、競爭加劇（博通、Marvell 切入）、估值偏高。',
        'target': 244.97, 'analysts': 26, 'consensus': 'Buy', 'entry': 310, 'stop': 250, 'tp': 360
    },
    'MRVL': {
        'score': 7, 'cat': 'chip',
        'why': '客製化 AI ASIC 第二把交椅。週五暴跌 16.7% 至 $263（最大跌幅之一），但長期成長動能仍在。ARTY ETF 持倉 9.53% 為第一大成分股。',
        'logic': '1) 客製化矽（Custom Silicon）業務：Google、Amazon Trainium、AWS Inferentia 訂單持續。2) 2026 營收 $5.5-6B 預期。3) 光通訊與資料中心互連新動能。',
        'outlook': '修正後 PE 28x 接近歷史低點。目標價 $280-$320。AI ASIC 滲透率從 10% 向 25% 提升的過程中，Marvell 將是核心受惠者。',
        'risk': '客戶集中（Amazon 占營收 約 20%）、Q1 2026 業績展望曾令人失望、資料中心需求週期反轉。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 260, 'stop': 215, 'tp': 320
    },
    'SMCI': {
        'score': 7, 'cat': 'server',
        'why': 'AI 伺服器純標的。週五跌 11.2% 至 $41.6，距 52W 高點 $62 已回調 33%。18 位分析師共識 Hold，目標價 $37.6（-9.6%）。但 Goldman Sachs 給 Sell $30，多空分歧。',
        'logic': '1) 2026 營收預估 $39.7B（年增 81%），EPS $2.60。2) 液冷伺服器領導者，與 ASX、NVDA 合作 B200 liquid-cooled rack。3) 延宕的審計問題已大致解決。',
        'outlook': '本益比僅 16x，遠低於同業。目標價 $44（Mizuho）/$45（Raymond James），上漲空間 5-10%。修正為買點，但需嚴設停損。',
        'risk': '審計歷史問題、毛利率僅 8%（結構性偏低）、大客戶集中（占營收 40%+）、競爭加劇。',
        'target': 37.63, 'analysts': 18, 'consensus': 'Hold', 'entry': 40, 'stop': 35, 'tp': 50
    },
    'DELL': {
        'score': 9, 'cat': 'server',
        'why': 'AI 伺服器最大受惠者之一，PowerEdge XE9680/XE8640 為 CSP 標配。週五跌 6.6% 至 $394，距 52W 高 $469 已回調 16%。',
        'logic': '1) AI 伺服器訂單堆積至 2027 年。2) 與 NVDA、AMD、Intel 戰略合作。3) PowerStore 與 PowerScale 進入 AI 推理週期。4) 毛利率持續優化（從 18% 提升至 25%）。',
        'outlook': '目標價 $440-$500（高盛、摩根史丹利），距當前有 12-27% 上漲空間。週五修正後是中長線最佳進場點。',
        'risk': 'AI 伺服器供應鏈瓶頸（GPU 供應）、毛利提升速度不如預期、PC 業務復甦緩慢。',
        'target': 0, 'analysts': 0, 'consensus': 'Strong Buy', 'entry': 390, 'stop': 340, 'tp': 470
    },
    'HPE': {
        'score': 7, 'cat': 'server',
        'why': 'HPE 私有雲 AI 解決方案獨特優勢，週五跌 8.4% 至 $49.2，距 52W 高 $64.3 已回調 23%。',
        'logic': '1) Juniper Networks 收購整合（完成中），強化 AI 網路。2) HPE Private Cloud AI 與 NVIDIA AI Enterprise 整合。3) Aruba Networking AI 驅動網管。',
        'outlook': '目標價 $60-$70，AI 整合題材提供 20-40% 上漲空間。Juniper 收購後的網路業務與 AI 伺服器交叉銷售是主要催化劑。',
        'risk': 'Juniper 整合風險、企業 IT 預算縮減、傳統伺服器業務衰退。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 48, 'stop': 42, 'tp': 62
    },
    'CRWV': {
        'score': 7, 'cat': 'server',
        'why': 'AI 雲端運算新創，ARTY ETF 持倉 4.05%。週五跌 7.1% 至 $100，25 位分析師共識 Buy，目標價 $132.68（+32.16%）。',
        'logic': '1) 2026 營收預估 $12.67B（年增 147%）。2) 與 OpenAI、IBM、Microsoft 等簽訂長約，GPU 算力供不應求。3) 已建立 360MW+ 資料中心。',
        'outlook': '目標價 $132（北國證券 $165、D.A. Davidson 給 $100 偏空），上漲空間 30%。但 EPS 仍為負值，估值依賴營收增速維持。',
        'risk': '資本支出過高、與超大規模 CSP 競爭加劇、長約執約風險（OpenAI 集中度過高）、股價波動劇烈。',
        'target': 132.68, 'analysts': 25, 'consensus': 'Buy', 'entry': 100, 'stop': 80, 'tp': 140
    },
    'VST': {
        'score': 9, 'cat': 'power',
        'why': 'AI 電力最純標的，週五僅跌 3.2% 至 $148.7（強勢抗跌）。19 位分析師 14 個 Strong Buy，目標價中位數 $227（+52.6%）。Wells Fargo 升至 $259。',
        'logic': '1) 2026 營收預估 $23.3B（年增 31%），EPS $8.59（年增 80%）。2) 與大型科技公司簽訂 10-20 年 PPA 電力合約。3) 天然氣 + 核能雙引擎。4) 模組化小型反應爺（SMR）合作開發。',
        'outlook': '目標價 $225（+51%），Wells Fargo 樂觀至 $259。距 52W 高點 $220 仍有上行空間。AI 電力緊缺是 5-10 年結構性主題。',
        'risk': '電力價格週期、監管風險、再生能源補貼政策變化、Free Cash Flow 波動。',
        'target': 225.29, 'analysts': 19, 'consensus': 'Strong Buy', 'entry': 148, 'stop': 130, 'tp': 200
    },
    'CEG': {
        'score': 9, 'cat': 'power',
        'why': '全美最大無碳能源供應商，核能 AI 電力霸主。週五跌 3.7% 至 $254.8，21 位分析師 13 個 Strong Buy，目標價 $367（+44%）。Wells Fargo 升至 $516。',
        'logic': '1) 2026 營收預估 $34.7B（年增 36%），EPS $11.75（年增 25%）。2) 與 Microsoft 簽 20 年 835MW PPA（重啟 Three Mile Island 機組）。3) Meta、Google 都在洽談核能供應。',
        'outlook': '目標價中位數 $377，距當前有 48% 上漲空間。Wells Fargo 樂觀 $516（+102%）。核能 AI 電力供不應求的結構性受惠者。',
        'risk': '核能監管風險、新機組建設延遲、再生能源政策轉向、天然氣價格波動。',
        'target': 367.12, 'analysts': 21, 'consensus': 'Strong Buy', 'entry': 250, 'stop': 220, 'tp': 350
    },
    'VRT': {
        'score': 9, 'cat': 'power',
        'why': '液冷+電力基礎設施龍頭，AI 機房必備。週五跌 7.2% 至 $300.5，26 位分析師 18 個 Strong Buy，目標價 $377（+25%）。RBC $435、Evercore $425。',
        'logic': '1) 2026 營收預估 $13.9B（年增 36%），EPS $6.49（年增 55%）。2) 液冷 CDU 全球市占第一，NVDA 標準採用。3) UPS、電源管理系統全面 AI 化升級週期。',
        'outlook': '目標價 $377-Evercore $425，距離高點 $380 仍有上行空間。AI 機房液冷滲透率從 10% 提升到 50% 的過程中，VRT 是最大受惠者。',
        'risk': '客戶集中度、液冷技術替代風險、銅鋁等原材料價格波動、評價已偏高。',
        'target': 376.8, 'analysts': 26, 'consensus': 'Buy', 'entry': 295, 'stop': 260, 'tp': 370
    },
    'BE': {
        'score': 7, 'cat': 'power',
        'why': '燃料電池+固態氧化物技術龍頭，AI 分散式電力解決方案。週五跌 9.5% 至 $263.6，27 位分析師 9 個 Strong Buy，目標價 $263.13（持平）。Daiwa 升至 $324。',
        'logic': '1) 2026 營收預估 $3.71B（年增 83%），EPS $2.13（年增 180%）。2) 與 Oracle、Equinix 等簽訂大型燃料電池資料中心合約。3) AI 訓練+推理電力負載最佳化方案。',
        'outlook': '目標價中位數 $283，距當前有 7% 上漲空間。Daiwa 樂觀 $324（+23%）。氫能政策與綠能資料中心趨勢的純受惠者。',
        'risk': '氫能基礎設施尚未成熟、客戶集中、評價波動劇烈、FC 技術替代風險。',
        'target': 263.13, 'analysts': 27, 'consensus': 'Buy', 'entry': 260, 'stop': 220, 'tp': 320
    },
    'ETN': {
        'score': 8, 'cat': 'power',
        'why': 'AI 配電系統龍頭，UPS、電氣化解決方案。週五跌 5.4% 至 $395.9。',
        'logic': '1) AI 資料中心電力分配單元（PDU）、電氣化基礎設施。2) 與超大規模 CSP 簽訂長約。3) 2026 EPS 預期 $10.4（年增 16%），毛利率持續優化。',
        'outlook': '目標價 $440-$460，距當前 11-16% 上漲空間。AI 電力需求結構性增長的核心受惠者。',
        'risk': '評價偏高、工業景氣循環、銅等原材料成本。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 390, 'stop': 350, 'tp': 450
    },
    'SPXC': {
        'score': 8, 'cat': 'cooling',
        'why': '液冷技術純標的，AI 機房散熱核心。週五僅跌 3.5%（抗跌），12 位分析師 10 個 Strong Buy，目標價 $266（+17%）。',
        'logic': '1) AI 液冷 CDU、Tank、Heat Exchanger 全球前三大供應商。2) 與 Vertiv、CoolIT 合作，覆蓋 NVDA、AMD 平台。3) 收購 ASPEQ 強化液冷產品線。',
        'outlook': '目標價 $266（+17%），最高 $310（+36%）。AI 液冷滲透率提升週期中，SPXC 為純標的且本益比僅 28x 合理。',
        'risk': '客戶集中、收購整合風險、AI 機房建置速度放緩。',
        'target': 266.25, 'analysts': 12, 'consensus': 'Strong Buy', 'entry': 225, 'stop': 195, 'tp': 270
    },
    'TT': {
        'score': 7, 'cat': 'cooling',
        'why': 'Trane 商用 HVAC + AI 機房冷卻。週五僅跌 1.5%（超抗跌），顯示防禦性強。',
        'logic': '1) AI 資料中心 HVAC 與冷卻水系統。2) Thermo King 冷鏈與 AI 邊緣運算。3) 高毛利率（22%+）與穩定現金流。',
        'outlook': '目標價 $530-$570，距當前 16-25% 上漲空間。AI 機房散熱需求與冷鏈數位化雙引擎。',
        'risk': '傳統 HVAC 業務成長放緩、AI 業務占比仍小。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 450, 'stop': 400, 'tp': 520
    },
    'ANET': {
        'score': 9, 'cat': 'network',
        'why': 'AI 資料中心高速乙太網路霸主。週五跌 7.1% 至 $154.3，距 52W 高 $180 已回調 14%。',
        'logic': '1) 800G 乙太網路交換器領導者，Meta 微軟採用擴大。2) 2026 營收預估 $8.5B（年增 25%），毛利率 65%+。3) 與 NVIDIA Spectrum-X 平台競爭。',
        'outlook': '目標價 $180-$200，距當前 17-30% 上漲空間。AI 機房從 InfiniBand 轉向乙太網路的趨勢中，Arista 是核心受惠者。',
        'risk': 'NVDA Spectrum 競爭加壓、客戶集中（Meta 占比 15%+）。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 152, 'stop': 130, 'tp': 185
    },
    'CSCO': {
        'score': 8, 'cat': 'network',
        'why': 'AI 網路+資安整合平台。週五跌 6.4% 至 $121.6，距離高點 $129 僅 6%，相對抗跌。',
        'logic': '1) Splunk 收購整合後的 AI 數據分析平台。2) AI 資料中心交換器、超融合基礎設施。3) Hypershield AI 資安平台。4) 國防 AI 應用（與 NVIDIA、HPC）。',
        'outlook': '目標價 $140-$155，距當前 15-27% 上漲空間。AI 整合度高、現金流穩定、股息 3%+ 提供下檔保護。',
        'risk': '傳統網路業務衰退、競爭加劇（Juniper、HPE）、監管不確定性。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 120, 'stop': 105, 'tp': 145
    },
    'CIEN': {
        'score': 7, 'cat': 'network',
        'why': '光通訊+AI 互連核心。週五跌 8.9% 至 $488.2，距 52W 高 $637 已回調 23%。',
        'logic': '1) 800G/1.6T 光模組領導者。2) AI 機房內部 DCI 互連需求爆發。3) WaveLogic 6 平台 2026 量產。',
        'outlook': '目標價 $580-$640，距當前 19-31% 上漲空間。修正為買點，光通訊 AI 應用的純標的。',
        'risk': 'CSP 自研光模組（Inphi/Marvell 切入）、景氣循環、毛利率壓力。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 485, 'stop': 420, 'tp': 600
    },
    'GLW': {
        'score': 7, 'cat': 'network',
        'why': '光纖+AI 玻璃基板。週五跌 10.2% 至 $177.6，距 52W 高 $212 已回調 16%。',
        'logic': '1) AI GPU 玻璃基板（取代有機基板）2026 Q3 量產。2) 光纖電纜需求爆發。3) 與 NVDA、AMD 合作 Glass Core Substrate。',
        'outlook': '目標價 $200-$230，距當前 13-30% 上漲空間。玻璃基板是 AI 晶片封裝的下一個重要升級，Corning 是核心供應商。',
        'risk': '玻璃基板量產時程、競爭（AGC、Schott）、運營效率。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 175, 'stop': 150, 'tp': 220
    },
    'LUMN': {
        'score': 7, 'cat': 'network',
        'why': '光纖+AI 邊緣運算。週五跌 10% 至 $8.91，距 52W 高 $11.95 已回調 25%。',
        'logic': '1) 與 Microsoft 簽訂 8 年 50 億美元光纖合約。2) 與 Corning 合作大規模光纖部署。3) AI 邊緣運算（PCF）轉型。',
        'outlook': '目標價 $11-$15，距當前 23-68% 上漲空間。AI 光纖需求結構性增長 + 業務轉型故事。',
        'risk': '債務問題、轉型執行風險、營收結構調整陣痛。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 8.5, 'stop': 6.5, 'tp': 12
    },
    'NTAP': {
        'score': 8, 'cat': 'storage',
        'why': 'AI 儲存領導者，週五跌 6.6% 至 $167，距 52W 高 $193 已回調 13%。',
        'logic': '1) ONTAP AI 與 NVIDIA AI Enterprise 整合。2) 與 NVDA DGX SuperPOD 標配。3) 2026 營收預估 $5B+（年增 10%），毛利率 70%+。',
        'outlook': '目標價 $190-$210，距當前 14-26% 上漲空間。AI NAS 全快閃陣列標的，AI 訓練資料儲存的純受惠者。',
        'risk': '純儲存業務面臨雲端原生挑戰、AI NAS 競爭加劇。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 165, 'stop': 140, 'tp': 195
    },
    'WDC': {
        'score': 7, 'cat': 'storage',
        'why': 'NAND + AI HDD 雙引擎。週五跌 11% 至 $511.7，距 52W 高 $602 已回調 15%。',
        'logic': '1) AI 訓練大容量 HDD 需求爆發。2) NAND Flash 漲價週期。3) SanDisk 分拆後更聚焦儲存。',
        'outlook': '目標價 $600-$700，距當前 17-37% 上漲空間。NAND + HDD 雙產品線受惠 AI 與資料中心需求。',
        'risk': 'NAND 價格波動、SanDisk 分拆後整合不確定性。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 510, 'stop': 440, 'tp': 620
    },
    'STX': {
        'score': 7, 'cat': 'storage',
        'why': 'AI HDD 龍頭，Mass Capacity 領導者。週五跌 8.5% 至 $847.5。',
        'logic': '1) Mozaic 3+ HAMR 技術 2026 Q2 進入量產，單碟 3TB+。2) 與 Microsoft、AWS 簽訂大規模 AI 訓練 HDD 長約。3) 2026 營收預估 $11B（年增 30%）。',
        'outlook': '目標價 $900-$1000，距當前 6-18% 上漲空間。HAMR 技術領先，AI 訓練大量冷資料儲存的最佳選擇。',
        'risk': 'HAMR 量產時程、SSD 替代 HDD 的長期風險、價格戰。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 845, 'stop': 730, 'tp': 950
    },
    'SNDK': {
        'score': 6, 'cat': 'storage',
        'why': 'NAND Flash 純標的，AI 儲存漲價週期。週五跌 11.4% 至 $1559。',
        'logic': '1) 從 WDC 分拆後專注 NAND 業務。2) BiCS 8 232 層 NAND 領先技術。3) AI 訓練資料儲存需求爆發。',
        'outlook': '目標價 $1800-$2200，AI NAND 漲價週期中具備高 Beta 屬性。風險與機會並存。',
        'risk': 'NAND 價格週期劇烈、與 Samsung、SK Hynix、鎧俠競爭、技術節奏。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 1550, 'stop': 1300, 'tp': 1900
    },
    'PSTG': {
        'score': 6, 'cat': 'storage',
        'why': '全快閃 AI 資料平台，週五暴跌 13.6% 至 $67.8（被嚴重超賣）。',
        'logic': '1) AI 訓練+推理全快閃資料平台。2) AIRI 與 NVIDIA DGX 整合。3) Evergreen 訂閱模式提供穩定營收。',
        'outlook': '目標價 $90-$100，距當前 33-47% 上漲空間。被超賣後 PE 12x 接近歷史低點。',
        'risk': '全快閃陣列景氣循環、AI 訓練儲存轉向雲端、SAN 替代風險。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 67, 'stop': 55, 'tp': 90
    },
    'AMKR': {
        'score': 7, 'cat': 'packaging',
        'why': 'CoWoS 先進封裝領導者，週五跌 12% 至 $65，距 52W 高 $79.5 已回調 18%。',
        'logic': '1) 為 NVDA、AMD 提供 CoWoS-S/CoWoS-L 封裝服務。2) 2026 營收預估 $7.5B（年增 25%）。3) 與 TSMC 戰略合作。',
        'outlook': '目標價 $85-$100，距當前 31-54% 上漲空間。AI 先進封裝瓶頸的最大受惠者之一。',
        'risk': 'TSMC 競爭、CoWoS 良率、客戶集中。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 64, 'stop': 52, 'tp': 85
    },
    'ASX': {
        'score': 7, 'cat': 'packaging',
        'why': 'ASE Technology 全球封測龍頭，週五跌 11.4% 至 $34。',
        'logic': '1) 為 NVDA、AMD、Marvell 等提供高階封裝。2) FOCoS、SoIC 等先進封裝技術領先。3) 2026 營收預估 $19B（年增 12%）。',
        'outlook': '目標價 $40-$45，距當前 18-32% 上漲空間。AI 先進封測的純標的，本益比 14x 合理。',
        'risk': '傳統封測業務衰退壓力、毛利率波動、客戶集中。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 33, 'stop': 28, 'tp': 42
    },
    'AMAT': {
        'score': 8, 'cat': 'packaging',
        'why': 'AI 半導體設備龍頭，週五跌 9.7% 至 $453。',
        'logic': '1) 先進製程+先進封裝設備領導者。2) Black Diamond、Producer XP 等 AI 製程設備。3) 2026 營收預估 $32B（年增 10%）。',
        'outlook': '目標價 $550-$600，距當前 21-32% 上漲空間。AI 製程升級週期中，AMAT 是最大受惠者。',
        'risk': '半導體景氣循環、中國市場監管、技術節奏。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 450, 'stop': 390, 'tp': 550
    },
    'LRCX': {
        'score': 7, 'cat': 'packaging',
        'why': '蝕刻設備領導者，AI HBM 與 3D NAND 製程關鍵供應商，週五跌 9.9% 至 $303。',
        'logic': '1) HBM TSV 蝕刻設備龍頭。2) 3D NAND 高深寬比蝕刻獨家。3) 與 MU、SK Hynix 合作下一代 HBM4 製程。',
        'outlook': '目標價 $340-$380，距當前 12-25% 上漲空間。AI 記憶體製程升級的核心受惠者。',
        'risk': '半導體景氣循環、中國市場、HBM 製程節奏。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 300, 'stop': 260, 'tp': 360
    },
    'KLAC': {
        'score': 7, 'cat': 'packaging',
        'why': '製程控管設備龍頭，週五跌 9.5% 至 $1929。',
        'logic': '1) 每片晶圓必經 KLA 檢測。2) AI 製程升級（3nm/2nm/1.4nm）提高檢測需求。3) 2026 營收預估 $13B（年增 12%）。',
        'outlook': '目標價 $2200-$2400，距當前 14-24% 上漲空間。AI 製程的「品質守門員」，具備定價權。',
        'risk': '評價偏高、半導體景氣循環、技術節奏。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 1920, 'stop': 1700, 'tp': 2300
    },
    'CRWD': {
        'score': 8, 'cat': 'security',
        'why': 'AI 資安領導者，週五跌 6.7% 至 $671，54 位分析師 31 個 Strong Buy，目標價 $707.5（+5.4%）。',
        'logic': '1) Falcon 平台 AI 原生設計。2) Charlotte AI 自動化資安分析師。3) 2026 營收預估 $5.94B（年增 23%），EPS $4.92。4) 與 AWS、Azure、GCP 三大雲端深度整合。',
        'outlook': '目標價中位數 $750，距當前 12% 上漲空間。AI 資安的長期領導者，2027 EPS 預期突破 $6.22。',
        'risk': '競爭加劇（SentinelOne、Palo Alto）、客戶流失、評價偏高。',
        'target': 707.47, 'analysts': 54, 'consensus': 'Buy', 'entry': 665, 'stop': 580, 'tp': 780
    },
    'PANW': {
        'score': 8, 'cat': 'security',
        'why': 'AI 平台型資安，週五跌 2.6% 至 $272（強勢抗跌）。',
        'logic': '1) Prisma Cloud + Cortex AI 平台。2) AI 驅動次世代 SIEM 與 XDR。3) 2026 營收預估 $10B+（年增 14%）。',
        'outlook': '目標價 $320-$350，距當前 18-29% 上漲空間。AI 資安整合平台的領導者，2026 從高速成長轉向獲利優質化。',
        'risk': '評價偏高、客戶轉移雲端、競爭加劇。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 270, 'stop': 235, 'tp': 320
    },
    'ZS': {
        'score': 7, 'cat': 'security',
        'why': 'Zero Trust AI 資安領導者，週五跌 3.3% 至 $130.8，距 52W 高 $337 已回調 61%。',
        'logic': '1) Zscaler Zero Trust 平台 AI 整合。2) AI 驅動資安自動化。3) 與 Microsoft、AWS 整合。',
        'outlook': '目標價 $170-$200，距當前 30-53% 上漲空間。被嚴重超賣後 PE 接近歷史低點，AI 資安的純標的。',
        'risk': '企業資安預算縮減、客戶流失、評價仍偏高。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 130, 'stop': 110, 'tp': 170
    },
    'FTNT': {
        'score': 7, 'cat': 'security',
        'why': 'Fortinet AI 防火牆+網路安全，週五跌 3.3% 至 $144.7，距 52W 高 $149 僅 3% 距離。',
        'logic': '1) FortiAI 安全助理。2) AI 訓練資料中心內部防火牆。3) 與 NVIDIA BlueField DPU 整合。',
        'outlook': '目標價 $170-$180，距當前 17-24% 上漲空間。AI 機房內部網路安全的標的。',
        'risk': '傳統防火牆市場飽和、競爭加劇、營收增速放緩。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 142, 'stop': 125, 'tp': 170
    },
    'PLTR': {
        'score': 9, 'cat': 'software',
        'why': 'AI 軟體/資料分析霸主，週五跌 4.4% 至 $135.5，31 位分析師共識 Buy，目標價 $183.7（+35.6%）。',
        'logic': '1) AIP（AI Platform）商業化爆發。2) 與 Oracle、AWS、Microsoft、Carahsoft 深度合作。3) 2026 營收預估 $7.72B（年增 72%），EPS $1.46（年增 95%）。4) 美國政府 AI 大客戶深度綁定。',
        'outlook': '目標價中位數 $200，距當前 48% 上漲空間。Rosenblatt $225、Phillip $202、William Blair 看好。AI 軟體的旗艦標的。',
        'risk': '評價偏高（PE 80x+）、客戶集中度、軍工業務波動。',
        'target': 183.73, 'analysts': 31, 'consensus': 'Buy', 'entry': 134, 'stop': 115, 'tp': 175
    },
    'SNOW': {
        'score': 9, 'cat': 'software',
        'why': 'AI 資料雲端龍頭，週五跌 2.4% 至 $238.3（抗跌）。',
        'logic': '1) Snowflake Cortex AI 全方位平台。2) 與 NVIDIA AI Enterprise 整合。3) 與 Anthropic、OpenAI 等模型供應商深度合作。4) 2026 營收預估 $5B+（年增 28%）。',
        'outlook': '目標價 $280-$300，距當前 17-26% 上漲空間。AI 資料雲端的領導者，與 Databricks 雙雄並立。',
        'risk': 'Databricks 競爭、雲端支出放緩、客戶集中。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 235, 'stop': 200, 'tp': 280
    },
    'DDOG': {
        'score': 8, 'cat': 'software',
        'why': 'AI 監控+可觀測性龍頭，週五跌 3.9% 至 $234.1。',
        'logic': '1) Watchdog AI 自動化監控。2) 與 OpenAI、Anthropic 等 AI 應用商深度整合。3) 2026 營收預估 $3.2B（年增 25%）。4) AI 推理成本監控需求爆發。',
        'outlook': '目標價 $280-$310，距當前 20-32% 上漲空間。AI 應用爆發的純受惠者，每多一個 AI 應用 → 多一個 Datadog Agent。',
        'risk': 'AI 應用成長速度、Snowflake 等整合監控方案、評價偏高。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 230, 'stop': 195, 'tp': 280
    },
    'MDB': {
        'score': 7, 'cat': 'software',
        'why': 'MongoDB Atlas AI 整合，週五跌 7.7% 至 $350.7。',
        'logic': '1) Atlas Vector Search + AI 應用開發。2) 與多家 LLM 供應商整合。3) 2026 營收預估 $2.2B（年增 22%）。',
        'outlook': '目標價 $400-$450，距當前 14-28% 上漲空間。AI 應用爆發的 NoSQL 資料庫領導者。',
        'risk': '傳統 MongoDB 業務壓力、雲端原生資料庫競爭、評價偏高。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 345, 'stop': 290, 'tp': 420
    },
    'NET': {
        'score': 8, 'cat': 'network',
        'why': 'Cloudflare 邊緣 AI 平台，週五跌 6.9% 至 $250.1，距 52W 高 $274 僅 9% 距離。',
        'logic': '1) Workers AI 邊緣運算平台。2) AI 推理從集中式走向分散式。3) 與多家 LLM 整合（Anthropic、Hugging Face）。4) 2026 營收預估 $2.1B（年增 28%）。',
        'outlook': '目標價 $280-$310，距當前 12-24% 上漲空間。AI 邊緣運算的代表標的，從 CDN 轉型為 AI 平台的故事仍在進行。',
        'risk': '評價偏高、營收增速放緩、AWS 等大客戶轉移。',
        'target': 0, 'analysts': 0, 'consensus': 'Buy', 'entry': 245, 'stop': 210, 'tp': 295
    },
}

# ========== CALCULATE CATEGORY STATS ==========
cat_stats = {}
for cat_id, cat in CATEGORIES.items():
    syms = cat['stocks']
    chgs = [market[s]['change_pct'] for s in syms if s in market]
    if chgs:
        avg = sum(chgs) / len(chgs)
        cat_stats[cat_id] = {
            'avg': avg,
            'stocks': [{'sym': s, 'name': market[s]['name'][:25], 'chg': market[s]['change_pct']} for s in syms if s in market]
        }

# Sort picks by score
sorted_picks = sorted(PICKS.items(), key=lambda x: -x[1]['score'])

# ========== GENERATE HTML ==========
date_str = "2026年6月6日（週六）"
gen_time = "2026年6月6日 台北時間 14:10"

# Calculate overall market stats
total_picks = len(PICKS)
avg_change = sum(market[s]['change_pct'] for s in PICKS.keys() if s in market) / total_picks
gainer_count = sum(1 for s in PICKS.keys() if s in market and market[s]['change_pct'] > 0)
loser_count = sum(1 for s in PICKS.keys() if s in market and market[s]['change_pct'] < -2)
strong_buy_count = sum(1 for s, p in PICKS.items() if p.get('consensus') == 'Strong Buy')

# Build category performance HTML
cat_html = ""
for cat_id, cat in CATEGORIES.items():
    if cat_id not in cat_stats: continue
    stats = cat_stats[cat_id]
    avg = stats['avg']
    if avg >= 2:
        badge = '<span class="badge badge-green">🟢 強勢</span>'
    elif avg <= -2:
        badge = '<span class="badge badge-red">🔴 弱勢</span>'
    else:
        badge = '<span class="badge badge-yellow">🟡 中性</span>'
    rep_stocks = []
    for st in stats['stocks'][:5]:
        chg_cls = 'pos' if st['chg'] >= 0 else 'neg'
        rep_stocks.append(f'<a href="{bc(st["sym"])}" class="ticker" target="_blank">{st["sym"]}</a> <span class="{chg_cls}">{st["chg"]:+.2f}%</span>')
    cat_html += f'''<tr>
  <td>{cat['icon']} {cat['name']}</td>
  <td>{' / '.join(rep_stocks)}</td>
  <td class="num"><span class="{'pos' if avg>=0 else 'neg'}">{avg:+.2f}%</span></td>
  <td>{badge}</td>
</tr>
'''

# Build top picks summary table
picks_html = ""
for sym, p in sorted_picks:
    if sym not in market: continue
    m = market[sym]
    chg_cls = 'pos' if m['change_pct'] >= 0 else 'neg'
    score_cls = f"s{p['score']}"
    target_pct = ((p.get('target', m['price']) - m['price']) / m['price'] * 100) if p.get('target', 0) > 0 else 0
    target_str = f"+{target_pct:.1f}%" if target_pct > 0 else f"{target_pct:.1f}%"
    picks_html += f'''<tr>
  <td><a href="{bc(sym)}" class="ticker" target="_blank">{sym}</a></td>
  <td>{m['name'][:22]}</td>
  <td class="num price-cell">${m['price']:.2f}</td>
  <td class="num {chg_cls}">{m['change_pct']:+.2f}%</td>
  <td class="num" style="font-size:11px;color:#888;">${m['low52']:.0f}-${m['high52']:.0f}</td>
  <td class="num">{m['from_low_pct']:.0f}%</td>
  <td class="num"><span class="score {score_cls}">{p['score']}</span></td>
  <td class="num">${p['entry']}</td>
  <td class="num">${p['tp']}</td>
  <td class="num">${p['stop']}</td>
  <td style="font-size:12px;">{p['why'][:140]}...</td>
  <td style="font-size:12px;">{p['logic'][:120]}...</td>
</tr>
'''

# Build detailed stock cards
cards_html = ""
for sym, p in sorted_picks:
    if sym not in market: continue
    m = market[sym]
    chg_cls = 'pos' if m['change_pct'] >= 0 else 'neg'
    cat = CATEGORIES[p['cat']]
    cat_full = f"{cat['icon']} {cat['name']}"
    target_pct = ((p.get('target', m['price']) - m['price']) / m['price'] * 100) if p.get('target', 0) > 0 else 0
    target_color = '#00ff88' if target_pct > 0 else '#ff4466'
    analyst_str = f"{p.get('analysts', '?')} 位分析師" if p.get('analysts', 0) > 0 else "分析師覆蓋"
    
    cards_html += f'''<div class="card" style="--accent: {target_color};">
  <div class="card-header">
    <div>
      <div class="card-title"><a href="{bc(sym)}" class="ticker" target="_blank" style="font-size:1.2em;">{sym}</a> <span class="card-symbol">{m['name'][:28]}</span></div>
      <div class="card-badge" style="background:rgba(91,127,255,0.15);color:#5b7fff;border:1px solid #5b7fff;">{cat_full}</div>
    </div>
    <div class="card-price">
      <div class="price">${m['price']:.2f}</div>
      <div class="chg {chg_cls}">{m['change_pct']:+.2f}%</div>
    </div>
  </div>
  
  <div class="card-section">
    <h4>📊 基本概況</h4>
    <p>現價 <strong style="color:#fff;">${m['price']:.2f}</strong> ｜ 52W 區間 <strong style="color:#fff;">${m['low52']:.2f} - ${m['high52']:.2f}</strong> ｜ 距 52W 低 <strong style="color:#00ff88;">{m['from_low_pct']:.1f}%</strong> ｜ 距 52W 高 <strong style="color:#ff8888;">{m['from_high_pct']:.1f}%</strong></p>
    <p>成交量 <strong style="color:#fff;">{m['volume']/1e6:.1f}M</strong> ｜ 當日區間 <strong style="color:#fff;">${m['day_low']:.2f} - ${m['day_high']:.2f}</strong></p>
  </div>
  
  <div class="card-section">
    <h4>🎯 為什麼入選（評分 {p['score']}/10）</h4>
    <p>{p['why']}</p>
  </div>
  
  <div class="card-section">
    <h4>💡 核心邏輯與展望</h4>
    <p>{p['logic']}</p>
  </div>
  
  <div class="card-section">
    <h4>📈 供需邏輯與未來展望</h4>
    <p>{p['outlook']}</p>
  </div>
  
  <div class="card-section">
    <h4>⚠️ 風險因素</h4>
    <p style="color:#ff8888;">{p['risk']}</p>
  </div>
  
  <div class="card-tags">
    <span class="tag">進場 ${p['entry']}</span>
    <span class="tag green">目標 ${p['tp']}</span>
    <span class="tag red">止損 ${p['stop']}</span>
    <span class="tag">{p.get('consensus', 'Buy')}</span>
    <span class="tag">{analyst_str}</span>
    {f'<span class="tag green">目標價 {target_pct:+.1f}%</span>' if p.get('target', 0) > 0 else ''}
  </div>
</div>
'''

# ========== FINAL HTML ==========
HTML = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI 基礎建設美股研究報告｜2026-06-06</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #080810; color: #e0e0f0; font-family: 'Segoe UI', 'PingFang TC', sans-serif; font-size: 14px; line-height: 1.6; }}
.wrap {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}

/* Header */
.r-header {{ text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #0a0a1a 0%, #1a0a2e 50%, #0a1a2a 100%); border-bottom: 2px solid #2a2a5a; margin-bottom: 30px; }}
.r-header h1 {{ font-size: 2.4em; font-weight: 800; background: linear-gradient(90deg, #00d4ff, #00ff88, #00d4ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-size: 200% auto; animation: shine 3s linear infinite; }}
@keyframes shine {{ to {{ background-position: 200% center; }} }}
.r-header .subtitle {{ color: #8888bb; font-size: 1.1em; margin-top: 8px; }}
.r-header .date-badge {{ display: inline-block; background: rgba(0,212,255,0.15); border: 1px solid #00d4ff; color: #00d4ff; padding: 6px 20px; border-radius: 20px; margin-top: 12px; font-weight: 600; letter-spacing: 1px; }}
.r-header .alert {{ display: inline-block; background: rgba(255,68,102,0.15); border: 1px solid #ff4466; color: #ff4466; padding: 4px 16px; border-radius: 12px; margin-top: 10px; font-size: 0.9em; font-weight: 600; }}

/* Market Radar */
.radar {{ background: linear-gradient(135deg, #0d0d24 0%, #141428 100%); border: 1px solid #2a2a5a; border-radius: 16px; padding: 24px; margin-bottom: 24px; }}
.radar h2 {{ color: #00d4ff; font-size: 1.4em; margin-bottom: 16px; border-left: 4px solid #00d4ff; padding-left: 12px; }}
.radar-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 14px; }}
.radar-card {{ background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 10px; padding: 14px; }}
.radar-card .label {{ color: #666; font-size: 0.8em; text-transform: uppercase; letter-spacing: 1px; }}
.radar-card .value {{ font-size: 1.05em; font-weight: 700; margin-top: 4px; }}
.up {{ color: #00ff88; }} .dn {{ color: #ff4466; }} .neutral {{ color: #ffcc00; }}

/* Category Table */
.cat-table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
.cat-table th {{ background: #12122a; color: #00d4ff; padding: 10px 12px; text-align: left; border-bottom: 2px solid #00d4ff; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.5px; }}
.cat-table td {{ padding: 10px 12px; border-bottom: 1px solid rgba(255,255,255,0.05); }}
.cat-table tr:hover {{ background: rgba(0,212,255,0.04); }}
.badge {{ display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 0.85em; font-weight: 700; }}
.badge-green {{ background: rgba(0,255,136,0.15); color: #00ff88; border: 1px solid #00ff88; }}
.badge-yellow {{ background: rgba(255,204,0,0.15); color: #ffcc00; border: 1px solid #ffcc00; }}
.badge-red {{ background: rgba(255,68,102,0.15); color: #ff4466; border: 1px solid #ff4466; }}
.ticker {{ color: #00d4ff; font-weight: 700; text-decoration: none; }}
.ticker:hover {{ color: #00ff88; text-decoration: underline; }}

/* Report Table */
.report-table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; font-size: 0.85em; }}
.report-table th {{ background: #12122a; color: #00d4ff; padding: 10px 6px; text-align: left; border-bottom: 2px solid #00d4ff; font-size: 0.78em; text-transform: uppercase; letter-spacing: 0.3px; white-space: nowrap; }}
.report-table td {{ padding: 8px 6px; border-bottom: 1px solid rgba(255,255,255,0.05); vertical-align: top; }}
.report-table tr:hover {{ background: rgba(0,212,255,0.05); }}
.report-table .num {{ text-align: right; font-variant-numeric: tabular-nums; }}
.report-table .price-cell {{ font-weight: 700; color: #fff; }}
.report-table .pos {{ color: #00ff88; }} .report-table .neg {{ color: #ff4466; }}
.score {{ display: inline-block; width: 28px; height: 28px; line-height: 28px; text-align: center; border-radius: 6px; font-weight: 800; font-size: 0.85em; }}
.s9 {{ background: #00ff88; color: #000; }} .s8 {{ background: #44ff99; color: #000; }}
.s7 {{ background: #88ffbb; color: #000; }} .s6 {{ background: #ccff00; color: #000; }}
.s5 {{ background: #ffcc00; color: #000; }} .s4 {{ background: #ff9900; color: #000; }}
.s3 {{ background: #ff6644; color: #fff; }}

/* Stock Cards */
.stock-cards {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(420px, 1fr)); gap: 18px; margin-bottom: 30px; }}
.card {{ background: linear-gradient(135deg, #101028 0%, #1a1030 100%); border: 1px solid #2a2a5a; border-radius: 14px; padding: 20px; position: relative; overflow: hidden; transition: transform 0.2s; }}
.card::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, var(--accent, #00d4ff), transparent); }}
.card:hover {{ transform: translateY(-3px); border-color: var(--accent, #00d4ff); }}
.card .card-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px; }}
.card .card-title {{ font-size: 1.2em; font-weight: 800; color: #fff; }}
.card .card-symbol {{ color: #00d4ff; font-weight: 600; font-size: 0.9em; }}
.card .card-price {{ text-align: right; }}
.card .card-price .price {{ font-size: 1.5em; font-weight: 800; color: #fff; }}
.card .card-price .chg {{ font-size: 0.9em; font-weight: 700; }}
.card .card-badge {{ display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 0.72em; font-weight: 700; margin-top: 4px; }}
.card .card-section {{ margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.05); }}
.card .card-section h4 {{ color: #00d4ff; font-size: 0.78em; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }}
.card .card-section p {{ color: #c0c0d8; font-size: 0.85em; line-height: 1.6; }}
.card .card-tags {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.05); }}
.tag {{ background: rgba(0,212,255,0.1); border: 1px solid rgba(0,212,255,0.3); color: #00d4ff; padding: 3px 10px; border-radius: 10px; font-size: 0.75em; font-weight: 600; }}
.tag.green {{ background: rgba(0,255,136,0.1); border-color: rgba(0,255,136,0.3); color: #00ff88; }}
.tag.red {{ background: rgba(255,68,102,0.1); border-color: rgba(255,68,102,0.3); color: #ff4466; }}

/* Theme Section */
.theme-section {{ margin-bottom: 28px; }}
.theme-section h2 {{ color: #00d4ff; font-size: 1.3em; margin-bottom: 14px; border-left: 4px solid #00d4ff; padding-left: 12px; }}
.theme-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; }}
.theme-card {{ background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 10px; padding: 16px; }}
.theme-card .theme-name {{ font-weight: 700; color: #fff; margin-bottom: 6px; font-size: 1.05em; }}
.theme-card .theme-desc {{ color: #8888bb; font-size: 0.85em; line-height: 1.5; }}
.theme-card .theme-stock-list {{ margin-top: 10px; font-size: 0.85em; color: #00d4ff; }}

.section-title {{ color: #00d4ff; font-size: 1.4em; margin: 30px 0 16px; border-left: 4px solid #00d4ff; padding-left: 12px; }}
.analysis-block {{ background: linear-gradient(135deg, #0d0d24 0%, #1a1030 100%); border: 1px solid #2a2a5a; border-radius: 14px; padding: 24px; margin-bottom: 24px; }}
.analysis-block h2 {{ color: #00d4ff; font-size: 1.3em; margin-bottom: 16px; }}

.footer {{ text-align: center; padding: 30px; color: #444466; font-size: 0.8em; border-top: 1px solid #2a2a5a; margin-top: 40px; }}
.footer a {{ color: #00d4ff; text-decoration: none; }}

@media (max-width: 768px) {{
  .stock-cards {{ grid-template-columns: 1fr; }}
  .r-header h1 {{ font-size: 1.6em; }}
  .report-table {{ font-size: 0.7em; }}
  .report-table th, .report-table td {{ padding: 4px 3px; }}
}}
</style>
</head>
<body>

<div class="wrap">

<!-- Header -->
<div class="r-header">
  <h1>AI 基礎建設美股研究報告</h1>
  <div class="subtitle">頂級 AI 基礎建設選股分析師｜每日動態研究</div>
  <div class="date-badge">📅 {date_str}｜台北時間</div>
  <div class="alert">⚠️ 6/5 週五 AI 大回調｜晶片股跌幅 -10%~17%｜完美買點浮現</div>
</div>

<!-- Market Radar -->
<div class="radar">
  <h2>📡 今日 AI 基礎建設市場雷達</h2>
  <div class="radar-grid">
    <div class="radar-card">
      <div class="label">整体板塊情緒</div>
      <div class="value dn">🔴 恐慌回調｜AI 晶片股平均 -10%</div>
    </div>
    <div class="radar-card">
      <div class="label">今日最強主題</div>
      <div class="value" style="color:#00ff88">NEE 抗跌、CSCO/PANW 跌幅較小</div>
    </div>
    <div class="radar-card">
      <div class="label">今日最弱主題</div>
      <div class="value" style="color:#ff4466">MRVL -16.7% / MU -13.3% / ARM -12.8%</div>
    </div>
    <div class="radar-card">
      <div class="label">市場關注焦點</div>
      <div class="value">CSP 雲端資本支出、AI 泡沫疑慮、HBM/CoWoS 供需</div>
    </div>
    <div class="radar-card">
      <div class="label">精選股票數</div>
      <div class="value" style="color:#00ff88">{total_picks} 檔｜平均跌幅 {avg_change:+.2f}%</div>
    </div>
    <div class="radar-card">
      <div class="label">分析師共識</div>
      <div class="value" style="color:#00ff88">{strong_buy_count} 個 Strong Buy｜本週逆勢上修目標</div>
    </div>
  </div>
</div>

<!-- A. Category Performance -->
<h2 class="section-title">📊 A. 各 AI 基建類別今日表現（週五 6/5 收盤）</h2>
<table class="cat-table">
<thead>
<tr>
  <th>類別</th>
  <th>代表股票（当日漲跌）</th>
  <th>類別均幅</th>
  <th>強度</th>
</tr>
</thead>
<tbody>
{cat_html}
</tbody>
</table>

<!-- B. Market Radar Narrative -->
<div class="analysis-block">
  <h2>📡 B. 今日 AI 基礎建設市場深度觀察</h2>
  <p style="line-height:1.8; color:#c0c0d8;">
    <strong style="color:#ff4466;">6/5 週五出現 2026 年以來 AI 基建最大單日回調</strong>——晶片股平均跌幅 -8% 到 -17%，市場對 AI 泡沫疑慮再起，疊加部分分析師對 2026 H2 雲端資本支出放緩的擔憂。MRVL -16.7% / MU -13.3% / ARM -12.8% 為跌幅前三，VRT -7.2% / NVDA -6.2% 屬於第二梯隊，VST/CEG 等電力股僅跌 3% 表現最抗跌。
  </p>
  <p style="line-height:1.8; color:#c0c0d8; margin-top:12px;">
    <strong style="color:#00d4ff;">但是，分析師共識依然強勁</strong>——本週關鍵目標價上修：Wells Fargo 將 VST 從 $152 上調至 <strong style="color:#00ff88;">$259</strong>、上修 CEG 從 $265 至 <strong style="color:#00ff88;">$516</strong>、摩根史丹利將 MU 從 $520 升至 <strong style="color:#00ff88;">$1,050</strong>、Evercore 將 AVGO 維持 $582 Buy。多位分析師認為這是「健康修正」而非趨勢反轉，買點浮現。
  </p>
  <p style="line-height:1.8; color:#c0c0d8; margin-top:12px;">
    <strong style="color:#ffcc00;">AI 核心趨勢未變</strong>：1) 2026 三大 CSP（Microsoft/Google/Meta）CapEx 預期合計 $4,000 億+，年增 35%；2) HBM/CoWoS 持續供不應求到 2026 H2；3) 核能 AI 電力合約持續簽訂（Microsoft-Constellation 20 年 835MW）；4) 客製化 AI ASIC 滲透率從 10% 向 25% 提升。
  </p>
</div>

<!-- C. Top Picks Summary Table -->
<h2 class="section-title">🎯 C. 進場推薦總表（AI 智能精選 {total_picks} 檔）</h2>
<div style="overflow-x:auto;">
<table class="report-table">
<thead>
<tr>
  <th>代號</th>
  <th>名稱</th>
  <th class="num">現價</th>
  <th class="num">日%</th>
  <th class="num">52W區間</th>
  <th class="num">距低%</th>
  <th class="num">評分</th>
  <th class="num">進場</th>
  <th class="num">目標</th>
  <th class="num">止損</th>
  <th>為什麼推薦</th>
  <th>核心邏輯</th>
</tr>
</thead>
<tbody>
{picks_html}
</tbody>
</table>
</div>

<!-- D. Detailed Stock Cards -->
<h2 class="section-title">🔍 D. 深度個股分析（{total_picks} 檔完整評析）</h2>
<p style="color:#8888bb; margin-bottom:16px;">每張卡片包含：基本概況、入選理由、核心邏輯、供需展望、風險因素、進場/目標/止損價位。</p>
<div class="stock-cards">
{cards_html}
</div>

<!-- E. Theme Sector Assessment -->
<h2 class="section-title">🧭 E. 主題板塊評估</h2>
<div class="theme-grid">
  <div class="theme-card">
    <div class="theme-name">🟢 電力/能源（最強防禦）</div>
    <div class="theme-desc">VST/CEG/ETN/VRT 跌幅僅 -3% 到 -7%，遠低於晶片股。AI 電力需求是 5-10 年結構性主題，核能 PPA 與天然氣雙引擎。</div>
    <div class="theme-stock-list">主推：<a href="{bc("VST")}" class="ticker" target="_blank">VST</a>、<a href="{bc("CEG")}" class="ticker" target="_blank">CEG</a>、<a href="{bc("VRT")}" class="ticker" target="_blank">VRT</a>、<a href="{bc("BE")}" class="ticker" target="_blank">BE</a></div>
  </div>
  <div class="theme-card">
    <div class="theme-name">🔴 AI 晶片/GPU（超跌反彈）</div>
    <div class="theme-desc">NVDA/AMD/AVGO/MU/ARM 跌幅 -6% 到 -17%。基本面無虞，分析師持續上修目標價，修正為最佳買點。</div>
    <div class="theme-stock-list">主推：<a href="{bc("NVDA")}" class="ticker" target="_blank">NVDA</a>、<a href="{bc("AVGO")}" class="ticker" target="_blank">AVGO</a>、<a href="{bc("MU")}" class="ticker" target="_blank">MU</a>、<a href="{bc("AMD")}" class="ticker" target="_blank">AMD</a></div>
  </div>
  <div class="theme-card">
    <div class="theme-name">🟡 散熱/液冷（中期主軸）</div>
    <div class="theme-desc">SPXC/VRT/TT 跌幅最小（-1.5% 到 -3.5%），液冷 AI 機房滲透率從 10% 向 50% 提升，3-5 年結構性增長。</div>
    <div class="theme-stock-list">主推：<a href="{bc("SPXC")}" class="ticker" target="_blank">SPXC</a>、<a href="{bc("VRT")}" class="ticker" target="_blank">VRT</a>、<a href="{bc("TT")}" class="ticker" target="_blank">TT</a></div>
  </div>
  <div class="theme-card">
    <div class="theme-name">🟡 伺服器/雲端（持續受惠）</div>
    <div class="theme-desc">SMCI/DELL/HPE/CRWV 跌幅 -6% 到 -11%。AI 機房訂單堆積至 2027，SMCI 估值接近歷史低點。</div>
    <div class="theme-stock-list">主推：<a href="{bc("DELL")}" class="ticker" target="_blank">DELL</a>、<a href="{bc("HPE")}" class="ticker" target="_blank">HPE</a>、<a href="{bc("CRWV")}" class="ticker" target="_blank">CRWV</a></div>
  </div>
  <div class="theme-card">
    <div class="theme-name">🔴 網路/光纖（高 Beta）</div>
    <div class="theme-desc">ANET/CIEN/GLW 跌幅 -7% 到 -10%。800G/1.6T 升級週期未變，修正為加碼機會。</div>
    <div class="theme-stock-list">主推：<a href="{bc("ANET")}" class="ticker" target="_blank">ANET</a>、<a href="{bc("CIEN")}" class="ticker" target="_blank">CIEN</a>、<a href="{bc("GLW")}" class="ticker" target="_blank">GLW</a></div>
  </div>
  <div class="theme-card">
    <div class="theme-name">🔴 儲存/記憶體（HBM 缺貨）</div>
    <div class="theme-desc">MU/WDC/STX/SNDK 跌幅 -8% 到 -14%。HBM3E 滿載、HBM4 開發中、HDD 大容量 AI 訓練需求爆發。</div>
    <div class="theme-stock-list">主推：<a href="{bc("MU")}" class="ticker" target="_blank">MU</a>、<a href="{bc("NTAP")}" class="ticker" target="_blank">NTAP</a>、<a href="{bc("WDC")}" class="ticker" target="_blank">WDC</a></div>
  </div>
  <div class="theme-card">
    <div class="theme-name">🔴 封裝/CoWoS（瓶頸環節）</div>
    <div class="theme-desc">AMKR/ASX/AMAT/LRCX/KLAC 跌幅 -9% 到 -12%。CoWoS 產能擴張慢於需求，2026 全年吃緊。</div>
    <div class="theme-stock-list">主推：<a href="{bc("AMKR")}" class="ticker" target="_blank">AMKR</a>、<a href="{bc("ASX")}" class="ticker" target="_blank">ASX</a>、<a href="{bc("AMAT")}" class="ticker" target="_blank">AMAT</a></div>
  </div>
  <div class="theme-card">
    <div class="theme-name">🟡 資安/雲端（防禦性）</div>
    <div class="theme-desc">CRWD/PANW/ZS/FTNT/NET 跌幅 -3% 到 -7%。AI 資安是每個 AI 應用必備，需求確定性高。</div>
    <div class="theme-stock-list">主推：<a href="{bc("CRWD")}" class="ticker" target="_blank">CRWD</a>、<a href="{bc("PANW")}" class="ticker" target="_blank">PANW</a>、<a href="{bc("NET")}" class="ticker" target="_blank">NET</a></div>
  </div>
  <div class="theme-card">
    <div class="theme-name">🟡 軟體/資料分析（高估值）</div>
    <div class="theme-desc">PLTR/SNOW/DDOG/MDB 跌幅 -4% 到 -8%。AI 軟體旗艦標的，修正提供加碼機會。</div>
    <div class="theme-stock-list">主推：<a href="{bc("PLTR")}" class="ticker" target="_blank">PLTR</a>、<a href="{bc("SNOW")}" class="ticker" target="_blank">SNOW</a>、<a href="{bc("DDOG")}" class="ticker" target="_blank">DDOG</a></div>
  </div>
  <div class="theme-card">
    <div class="theme-name">🟡 雲端平台（CSP）</div>
    <div class="theme-desc">GOOGL/MSFT/AMZN/META 跌幅 -1% 到 -5%。AI 投資規模決定者，CapEx 持續上修。</div>
    <div class="theme-stock-list">主推：<a href="{bc("GOOGL")}" class="ticker" target="_blank">GOOGL</a>、<a href="{bc("MSFT")}" class="ticker" target="_blank">MSFT</a>、<a href="{bc("AMZN")}" class="ticker" target="_blank">AMZN</a></div>
  </div>
</div>

<!-- F. AI Supply-Demand Deep Dive -->
<div class="analysis-block">
  <h2>⚖️ F. AI 供需失衡深度分析（5-10 年結構性）</h2>
  <p style="line-height:1.8; color:#c0c0d8;">
    <strong style="color:#00d4ff;">【需求端爆發性成長】</strong><br>
    1) 三大 CSP 2026 CapEx 預期 <strong style="color:#00ff88;">$4,000 億+</strong>（年增 35%），主因 AI 訓練+推理運算需求爆發<br>
    2) Sovereign AI（國家級 AI）需求興起，歐洲、中東、印度等政府投資千億美元級 AI 基礎設施<br>
    3) Enterprise AI 從 PoC 轉向大規模生產，2026 H2 將出現企業 AI 推理爆發期<br>
    4) AI Agent、機器人、自動駕駛等新型應用 2026 Q4 開始規模化
  </p>
  <p style="line-height:1.8; color:#c0c0d8; margin-top:12px;">
    <strong style="color:#ff8800;">【供給端瓶頸持續】</strong><br>
    1) <strong style="color:#ffcc00;">HBM 記憶體</strong>：TSV 蝕刻、堆疊製程複雜，2026 全年吃緊，HBM4 預計 2027 Q1 才緩解<br>
    2) <strong style="color:#ffcc00;">CoWoS 先進封裝</strong>：TSCC/AMKR 產能擴張緩慢，2026 H2 仍供不應求<br>
    3) <strong style="color:#ffcc00;">AI 電力</strong>：資料中心用電 2030 年預計占全美 8-12%（目前 4%），新建發電設施需 5-7 年<br>
    4) <strong style="color:#ffcc00;">液冷散熱</strong>：CDU、液體管路等從設計到量產需 18-24 個月<br>
    5) <strong style="color:#ffcc00;">光通訊</strong>：800G/1.6T 光模組良率提升緩慢，InP 雷射晶片供應吃緊
  </p>
  <p style="line-height:1.8; color:#c0c0d8; margin-top:12px;">
    <strong style="color:#00ff88;">【投資結論】</strong>：本次 6/5 修正為「健康調整」而非趨勢反轉。AI 基建股的供需失衡結構未變，2026-2030 年是 5 年期超級週期。本週回調反而提供中長線加碼黃金窗口。
  </p>
</div>

<!-- G. Tomorrow's Watchlist -->
<div class="analysis-block">
  <h2>🔮 G. 明日（6/9 週一）觀察重點</h2>
  <p style="line-height:1.8; color:#c0c0d8;">
    <strong style="color:#00d4ff;">【機構動向】</strong><br>
    1) 6/5 大跌後機構是否進場撿便宜（觀察 VST、NVDA、CRWD 6/9 開盤）<br>
    2) 對沖基金是否擴大避險部位（VIX、UVXY）<br>
    3) ETF 6/9 申贖流向（AIQ、ARTY、SOXX）
  </p>
  <p style="line-height:1.8; color:#c0c0d8; margin-top:12px;">
    <strong style="color:#ffcc00;">【個股觀察】</strong><br>
    1) <a href="{bc("NVDA")}" class="ticker" target="_blank">NVDA</a>：能否守穩 $200 整數關卡，$180 為強支撐<br>
    2) <a href="{bc("MU")}" class="ticker" target="_blank">MU</a>：HBM3E 供需是否在 Q3 持續吃緊<br>
    3) <a href="{bc("ARM")}" class="ticker" target="_blank">ARM</a>：伺服器 CPU 滲透率進度<br>
    4) <a href="{bc("SMCI")}" class="ticker" target="_blank">SMCI</a>：是否發布新審計或財報更新<br>
    5) <a href="{bc("VST")}" class="ticker" target="_blank">VST</a>：是否再有新 PPA 合約宣布<br>
    6) <a href="{bc("CRWV")}" class="ticker" target="_blank">CRWV</a>：長約執約進度與新資料中心建設
  </p>
  <p style="line-height:1.8; color:#c0c0d8; margin-top:12px;">
    <strong style="color:#ff4466;">【風險監控】</strong><br>
    1) 任何 CSP（Microsoft/Google/Amazon/Meta）財報前夕放話 CapEx 放緩<br>
    2) 美國經濟數據（CPI、就業）影響聯準會利率路徑<br>
    3) 中美晶片管制升級或鬆綁<br>
    4) 個股突發利空（會計問題、客戶流失、產品瑕疵）
  </p>
</div>

<!-- Summary -->
<div class="analysis-block" style="background: linear-gradient(135deg, #1a0a2e 0%, #2a1a4a 100%);">
  <h2>🏆 H. 報告總結</h2>
  <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap:16px; margin-top:16px;">
    <div>
      <h4 style="color:#00ff88; margin-bottom:8px;">📊 精選數量</h4>
      <p style="font-size:1.2em; font-weight:800; color:#fff;">共 {total_picks} 檔</p>
      <p style="color:#8888bb; font-size:0.85em;">從 60 檔候選股中 AI 智能精選最有價值的 {total_picks} 檔</p>
    </div>
    <div>
      <h4 style="color:#00ff88; margin-bottom:8px;">⭐ 重點推薦（評分 9-10）</h4>
      <p style="color:#fff; font-weight:700; font-size:0.95em;">NVDA、AVGO、MU、VST、CEG、VRT、SPXC、ANET、PLTR、SNOW、DELL</p>
    </div>
    <div>
      <h4 style="color:#ffcc00; margin-bottom:8px;">💡 核心觀點</h4>
      <p style="color:#8888bb; font-size:0.85em; line-height:1.5;">6/5 AI 大回調是健康修正，分析師持續上修目標價。AI 供需失衡結構未變，2026-2030 是 5 年超級週期。買點浮現，建議分批加碼。</p>
    </div>
    <div>
      <h4 style="color:#ff4466; margin-bottom:8px;">⚠️ 最大風險</h4>
      <p style="color:#8888bb; font-size:0.85em; line-height:1.5;">AI 泡沫疑慮、CSP CapEx 放緩、客戶集中度、評價偏高、半導體景氣循環</p>
    </div>
  </div>
</div>

<div class="footer">
  <p>📅 報告生成時間：{gen_time}</p>
  <p>本報告由 AI 基礎建設選股分析師動態生成｜資料僅供參考，不構成投資建議</p>
  <p>stock-reports 自動推送系統｜ <a href="https://github.com/acstep/stock-reports" target="_blank">GitHub Repo</a></p>
</div>

</div>
</body>
</html>'''

# Write report
output_path = '/home/matt/.openclaw/workspace/stock-reports/reports/2026-06-06.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(HTML)
print(f"✅ Wrote {output_path}")
print(f"   Total picks: {total_picks}")
print(f"   Avg change: {avg_change:+.2f}%")
print(f"   Strong Buy: {strong_buy_count} stocks")
print(f"   Categories covered: {len(CATEGORIES)}")
print(f"   File size: {len(HTML):,} bytes")
