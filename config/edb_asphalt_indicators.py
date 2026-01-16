# config/edb_asphalt_indicators.py
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import date, datetime

@dataclass
class EDBIndicatorConfig:
    """EDB指标配置"""
    code: str
    name: str
    frequency: str  # daily, weekly, monthly
    unit: str
    source: str
    update_time: str
    start_time: str
    end_time: str
    country: str
    category: str = ""  # price, cost_profit, production, supply, inventory, operation, freight, trade, consumption
    sub_category: str = ""
    region: str = ""
    product_type: str = ""

# ========== 完整的沥青EDB指标映射表 ==========
ASPHALT_EDB_INDICATORS: Dict[str, EDBIndicatorConfig] = {
    # ========== 价格类指标 ==========
    # 现货价格 - 70#重交沥青
    "S002861328": EDBIndicatorConfig(
        code="S002861328",
        name="出厂均价:沥青(70#重交沥青):华北",
        frequency="daily",
        unit="元/吨",
        source="同花顺金融",
        update_time="20260109",
        start_time="20090104",
        end_time="20260109",
        country="中国"
    ),
    "S002861333": EDBIndicatorConfig(
        code="S002861333",
        name="出厂均价:沥青(70#重交沥青):华东",
        frequency="daily",
        unit="元/吨",
        source="同花顺金融",
        update_time="20260109",
        start_time="20090104",
        end_time="20260109",
        country="中国"
    ),
    "S002861337": EDBIndicatorConfig(
        code="S002861337",
        name="出厂均价:沥青(70#重交沥青):华南",
        frequency="daily",
        unit="元/吨",
        source="同花顺金融",
        update_time="20260109",
        start_time="20090104",
        end_time="20260109",
        country="中国"
    ),
    "S004156245": EDBIndicatorConfig(
        code="S004156245",
        name="出厂均价:沥青(70#重交沥青):山东",
        frequency="daily",
        unit="元/吨",
        source="同花顺金融",
        update_time="20260109",
        start_time="20060517",
        end_time="20260109",
        country="中国"
    ),
    "S002861347": EDBIndicatorConfig(
        code="S002861347",
        name="出厂均价:沥青(70#重交沥青):西南",
        frequency="daily",
        unit="元/吨",
        source="同花顺金融",
        update_time="20260109",
        start_time="20090104",
        end_time="20260109",
        country="中国"
    ),
    "S002861322": EDBIndicatorConfig(
        code="S002861322",
        name="出厂均价:沥青(70#重交沥青):东北",
        frequency="daily",
        unit="元/吨",
        source="同花顺金融",
        update_time="20260109",
        start_time="20060104",
        end_time="20260109",
        country="中国"
    ),
    
    # 现货价格 - 90#重交沥青
    "S002861329": EDBIndicatorConfig(
        code="S002861329",
        name="出厂均价:沥青(90#重交沥青):华北",
        frequency="daily",
        unit="元/吨",
        source="同花顺金融",
        update_time="20260109",
        start_time="20090104",
        end_time="20260109",
        country="中国"
    ),
    "S002861334": EDBIndicatorConfig(
        code="S002861334",
        name="出厂均价:沥青(90#重交沥青):华东",
        frequency="daily",
        unit="元/吨",
        source="同花顺金融",
        update_time="20260109",
        start_time="20090104",
        end_time="20260109",
        country="中国"
    ),
    "S002861338": EDBIndicatorConfig(
        code="S002861338",
        name="出厂均价:沥青(90#重交沥青):华南",
        frequency="daily",
        unit="元/吨",
        source="同花顺金融",
        update_time="20260109",
        start_time="20090104",
        end_time="20260109",
        country="中国"
    ),
    "S004156257": EDBIndicatorConfig(
        code="S004156257",
        name="出厂均价:沥青(90#重交沥青):山东",
        frequency="daily",
        unit="元/吨",
        source="同花顺金融",
        update_time="20260109",
        start_time="20120104",
        end_time="20260109",
        country="中国"
    ),
    "S002861342": EDBIndicatorConfig(
        code="S002861342",
        name="出厂均价:沥青(90#重交沥青):西北",
        frequency="daily",
        unit="元/吨",
        source="同花顺金融",
        update_time="20260109",
        start_time="20090104",
        end_time="20260109",
        country="中国"
    ),
    "S002861346": EDBIndicatorConfig(
        code="S002861346",
        name="出厂均价:沥青(90#重交沥青):西北",
        frequency="daily",
        unit="元/吨",
        source="同花顺金融",
        update_time="20260109",
        start_time="20090104",
        end_time="20260109",
        country="中国"
    ),
    
    # 市场估价
    "S006899687": EDBIndicatorConfig(
        code="S006899687",
        name="市场估价:70#沥青:东北",
        frequency="daily",
        unit="元/吨",
        source="同花顺金融",
        update_time="20260109",
        start_time="20191112",
        end_time="20260109",
        country="中国"
    ),
    "S006899682": EDBIndicatorConfig(
        code="S006899682",
        name="市场估价:70#沥青:华南",
        frequency="daily",
        unit="元/吨",
        source="同花顺金融",
        update_time="20260109",
        start_time="20191112",
        end_time="20260109",
        country="中国"
    ),
    "S006899684": EDBIndicatorConfig(
        code="S006899684",
        name="市场估价:70#沥青:华中/华北",
        frequency="daily",
        unit="元/吨",
        source="同花顺金融",
        update_time="20260109",
        start_time="20191112",
        end_time="20260109",
        country="中国"
    ),
    "S006899685": EDBIndicatorConfig(
        code="S006899685",
        name="市场估价:70#沥青:江浙沪",
        frequency="daily",
        unit="元/吨",
        source="同花顺金融",
        update_time="20260109",
        start_time="20191112",
        end_time="20260109",
        country="中国"
    ),
    "S006899686": EDBIndicatorConfig(
        code="S006899686",
        name="市场估价:70#沥青:山东",
        frequency="daily",
        unit="元/吨",
        source="同花顺金融",
        update_time="20260109",
        start_time="20191112",
        end_time="20260109",
        country="中国"
    ),
    "S006899688": EDBIndicatorConfig(
        code="S006899688",
        name="市场估价:70#沥青:西北",
        frequency="daily",
        unit="元/吨",
        source="同花顺金融",
        update_time="20260109",
        start_time="20191112",
        end_time="20260109",
        country="中国"
    ),
    "S006899683": EDBIndicatorConfig(
        code="S006899683",
        name="市场估价:70#沥青:西南",
        frequency="daily",
        unit="元/吨",
        source="同花顺金融",
        update_time="20260109",
        start_time="20191112",
        end_time="20260109",
        country="中国"
    ),
    
    # 国际价格
    "S006853437": EDBIndicatorConfig(
        code="S006853437",
        name="国际市场价:道路沥青(到岸价CFR):新加坡:华南收:中间价",
        frequency="daily",
        unit="美元/吨",
        source="同花顺金融",
        update_time="20260112",
        start_time="20191216",
        end_time="20260112",
        country="新加坡"
    ),
    "S006853438": EDBIndicatorConfig(
        code="S006853438",
        name="国际市场价:道路沥青(到岸价CFR):新加坡:华东收:中间价",
        frequency="daily",
        unit="美元/吨",
        source="同花顺金融",
        update_time="20260112",
        start_time="20191216",
        end_time="20260112",
        country="新加坡"
    ),
    "S006853445": EDBIndicatorConfig(
        code="S006853445",
        name="国际市场价:道路沥青(离岸价FOB):新加坡:中间价",
        frequency="daily",
        unit="美元/吨",
        source="同花顺金融",
        update_time="20260112",
        start_time="20191216",
        end_time="20260112",
        country="新加坡"
    ),
    
    # 期货价格
    "S012195660": EDBIndicatorConfig(
        code="S012195660",
        name="期货收盘价(活跃):石油沥青(BU)",
        frequency="daily",
        unit="元/吨",
        source="上海期货交易所",
        update_time="20260112",
        start_time="20131009",
        end_time="20260112",
        country="中国"
    ),
    "S012195681": EDBIndicatorConfig(
        code="S012195681",
        name="期货结算价(活跃):石油沥青(BU)",
        frequency="daily",
        unit="元/吨",
        source="上海期货交易所",
        update_time="20260112",
        start_time="20131009",
        end_time="20260112",
        country="中国"
    ),
    "S012195705": EDBIndicatorConfig(
        code="S012195705",
        name="期货成交量(活跃):石油沥青(BU)",
        frequency="daily",
        unit="手",
        source="上海期货交易所",
        update_time="20260112",
        start_time="20131009",
        end_time="20260112",
        country="中国"
    ),
    "S012195704": EDBIndicatorConfig(
        code="S012195704",
        name="期货持仓量(活跃):石油沥青(BU)",
        frequency="daily",
        unit="手",
        source="上海期货交易所",
        update_time="20260112",
        start_time="20131009",
        end_time="20260112",
        country="中国"
    ),
    
    # ========== 成本利润类指标 ==========
    "S016936189": EDBIndicatorConfig(
        code="S016936189",
        name="周度利润:沥青:加工稀释:环比增减",
        frequency="weekly",
        unit="元/吨",
        source="同花顺金融",
        update_time="20260107",
        start_time="20210507",
        end_time="20260109",
        country="中国"
    ),
    "S016936188": EDBIndicatorConfig(
        code="S016936188",
        name="周度利润:沥青:加工稀释",
        frequency="weekly",
        unit="元/吨",
        source="同花顺金融",
        update_time="20260107",
        start_time="20210507",
        end_time="20260109",
        country="中国"
    ),
    
    # ========== 产量类指标 ==========
    "S009134934": EDBIndicatorConfig(
        code="S009134934",
        name="周产量:沥青:中国",
        frequency="weekly",
        unit="万吨",
        source="同花顺金融",
        update_time="20260108",
        start_time="20160108",
        end_time="20260109",
        country="中国"
    ),
    "S009134935": EDBIndicatorConfig(
        code="S009134935",
        name="周产量:沥青:分归属统计:地炼",
        frequency="weekly",
        unit="万吨",
        source="同花顺金融",
        update_time="20260108",
        start_time="20190308",
        end_time="20260109",
        country="中国"
    ),
    "S009134936": EDBIndicatorConfig(
        code="S009134936",
        name="周产量:沥青:分归属统计:中海油",
        frequency="weekly",
        unit="万吨",
        source="同花顺金融",
        update_time="20260108",
        start_time="20190308",
        end_time="20260109",
        country="中国"
    ),
    "S009134937": EDBIndicatorConfig(
        code="S009134937",
        name="周产量:沥青:分归属统计:中石油",
        frequency="weekly",
        unit="万吨",
        source="同花顺金融",
        update_time="20260108",
        start_time="20190308",
        end_time="20260109",
        country="中国"
    ),
    "S009134938": EDBIndicatorConfig(
        code="S009134938",
        name="周产量:沥青:分归属统计:中石化",
        frequency="weekly",
        unit="万吨",
        source="同花顺金融",
        update_time="20260108",
        start_time="20190308",
        end_time="20260109",
        country="中国"
    ),
    "S019295590": EDBIndicatorConfig(
        code="S019295590",
        name="检修损失量:石油沥青:当周值",
        frequency="weekly",
        unit="万吨",
        source="同花顺金融",
        update_time="20260108",
        start_time="20180105",
        end_time="20260109",
        country="中国"
    ),
    
    # ========== 供应类指标 ==========
    "S016936186": EDBIndicatorConfig(
        code="S016936186",
        name="出货量:沥青:国内",
        frequency="weekly",
        unit="万吨",
        source="同花顺金融",
        update_time="20260107",
        start_time="20210611",
        end_time="20260109",
        country="中国"
    ),
    "S016936187": EDBIndicatorConfig(
        code="S016936187",
        name="出货量:沥青:环比",
        frequency="weekly",
        unit="%",
        source="同花顺金融",
        update_time="20260107",
        start_time="20210611",
        end_time="20260109",
        country="中国"
    ),
    
    # ========== 库存类指标 ==========
    # 厂家库存
    "S004494160": EDBIndicatorConfig(
        code="S004494160",
        name="厂家库存:沥青:国内样本企业:合计:当周环比",
        frequency="weekly",
        unit="%",
        source="同花顺金融",
        update_time="20260106",
        start_time="20180504",
        end_time="20260109",
        country="中国"
    ),
    "S004494153": EDBIndicatorConfig(
        code="S004494153",
        name="厂家库存:沥青:国内样本企业:合计:期末值",
        frequency="weekly",
        unit="万吨",
        source="同花顺金融",
        update_time="20260106",
        start_time="20180427",
        end_time="20260109",
        country="中国"
    ),
    
    # 社会库存
    "S004494146": EDBIndicatorConfig(
        code="S004494146",
        name="社会库存:沥青:国内样本企业:合计:当周环比",
        frequency="weekly",
        unit="%",
        source="同花顺金融",
        update_time="20260106",
        start_time="20180615",
        end_time="20260109",
        country="中国"
    ),
    "S004494138": EDBIndicatorConfig(
        code="S004494138",
        name="社会库存:沥青:国内样本企业:合计:期末值",
        frequency="weekly",
        unit="万吨",
        source="同花顺金融",
        update_time="20260106",
        start_time="20180608",
        end_time="20260109",
        country="中国"
    ),
    
    # ========== 开工类指标 ==========
    "S004494167": EDBIndicatorConfig(
        code="S004494167",
        name="开工率:沥青:国内样本企业:综合",
        frequency="daily",
        unit="%",
        source="同花顺金融",
        update_time="20260109",
        start_time="20180531",
        end_time="20260107",
        country="中国"
    ),
    "S004494162": EDBIndicatorConfig(
        code="S004494162",
        name="开工率:沥青:东北地区",
        frequency="daily",
        unit="%",
        source="同花顺金融",
        update_time="20260109",
        start_time="20120915",
        end_time="20260107",
        country="中国"
    ),
    "S004494164": EDBIndicatorConfig(
        code="S004494164",
        name="开工率:沥青:华中及华北地区",
        frequency="daily",
        unit="%",
        source="同花顺金融",
        update_time="20260109",
        start_time="20120915",
        end_time="20260107",
        country="中国"
    ),
    "S004494165": EDBIndicatorConfig(
        code="S004494165",
        name="开工率:沥青:华东地区",
        frequency="daily",
        unit="%",
        source="同花顺金融",
        update_time="20260109",
        start_time="20120915",
        end_time="20260107",
        country="中国"
    ),
    "S005972926": EDBIndicatorConfig(
        code="S005972926",
        name="开工率:沥青:华南地区",
        frequency="daily",
        unit="%",
        source="同花顺金融",
        update_time="20260109",
        start_time="20210120",
        end_time="20260107",
        country="中国"
    ),
    "S004494163": EDBIndicatorConfig(
        code="S004494163",
        name="开工率:沥青:山东地区",
        frequency="daily",
        unit="%",
        source="同花顺金融",
        update_time="20260109",
        start_time="20120915",
        end_time="20260107",
        country="中国"
    ),
    "S004494161": EDBIndicatorConfig(
        code="S004494161",
        name="开工率:沥青:西北地区",
        frequency="daily",
        unit="%",
        source="同花顺金融",
        update_time="20260109",
        start_time="20120915",
        end_time="20260107",
        country="中国"
    ),
    "S005972927": EDBIndicatorConfig(
        code="S005972927",
        name="开工率:沥青:西南地区",
        frequency="daily",
        unit="%",
        source="同花顺金融",
        update_time="20260109",
        start_time="20120915",
        end_time="20260107",
        country="中国"
    ),
    
    # ========== 运费类指标 ==========
    "S019294526": EDBIndicatorConfig(
        code="S019294526",
        name="船运费:沥青:韩国-南京",
        frequency="daily",
        unit="美元/吨",
        source="同花顺金融",
        update_time="20260109",
        start_time="20211108",
        end_time="20260108",
        country="中国"
    ),
    "S019294527": EDBIndicatorConfig(
        code="S019294527",
        name="船运费:沥青:韩国-渤海湾",
        frequency="daily",
        unit="美元/吨",
        source="同花顺金融",
        update_time="20260109",
        start_time="20211108",
        end_time="20260108",
        country="中国"
    ),
    "S019294528": EDBIndicatorConfig(
        code="S019294528",
        name="船运费:沥青:新加坡-黄埔",
        frequency="daily",
        unit="美元/吨",
        source="同花顺金融",
        update_time="20260109",
        start_time="20211108",
        end_time="20260108",
        country="中国"
    ),
    "S019294529": EDBIndicatorConfig(
        code="S019294529",
        name="船运费:沥青:新加坡-南京",
        frequency="daily",
        unit="美元/吨",
        source="同花顺金融",
        update_time="20260109",
        start_time="20211108",
        end_time="20260108",
        country="中国"
    ),
    
    # ========== 贸易类指标 ==========
    # 进口
    "S004450419": EDBIndicatorConfig(
        code="S004450419",
        name="石油沥青(27132000):进口数量:当月值",
        frequency="monthly",
        unit="吨",
        source="海关总署",
        update_time="20251120",
        start_time="20041231",
        end_time="20251031",
        country="中国"
    ),
    "S004450420": EDBIndicatorConfig(
        code="S004450420",
        name="石油沥青(27132000):进口数量:累计值",
        frequency="monthly",
        unit="吨",
        source="海关总署",
        update_time="20251202",
        start_time="20041231",
        end_time="20251031",
        country="中国"
    ),
    "S004450423": EDBIndicatorConfig(
        code="S004450423",
        name="石油沥青(27132000):进口金额:当月值",
        frequency="monthly",
        unit="万美元",
        source="海关总署",
        update_time="20251120",
        start_time="20041231",
        end_time="20251031",
        country="中国"
    ),
    "S004450427": EDBIndicatorConfig(
        code="S004450427",
        name="石油沥青(27132000):进口均价:当月值",
        frequency="monthly",
        unit="美元/吨",
        source="海关总署",
        update_time="20251120",
        start_time="20041231",
        end_time="20251031",
        country="中国"
    ),
    
    # 出口
    "S004451029": EDBIndicatorConfig(
        code="S004451029",
        name="石油沥青(27132000):出口数量:当月值",
        frequency="monthly",
        unit="吨",
        source="海关总署",
        update_time="20251222",
        start_time="20041231",
        end_time="20251130",
        country="中国"
    ),
    "S004451033": EDBIndicatorConfig(
        code="S004451033",
        name="石油沥青(27132000):出口金额:当月值",
        frequency="monthly",
        unit="万美元",
        source="海关总署",
        update_time="20251222",
        start_time="20041231",
        end_time="20251130",
        country="中国"
    ),
    "S004451037": EDBIndicatorConfig(
        code="S004451037",
        name="石油沥青(27132000):出口均价:当月值",
        frequency="monthly",
        unit="美元/吨",
        source="海关总署",
        update_time="20251222",
        start_time="20041231",
        end_time="20251130",
        country="中国"
    ),
    
    # ========== 消费类指标 ==========
    "S019295593": EDBIndicatorConfig(
        code="S019295593",
        name="总需求量:沥青:当月值",
        frequency="monthly",
        unit="万吨",
        source="同花顺金融",
        update_time="20251229",
        start_time="20220630",
        end_time="20251231",
        country="中国"
    ),
    "S019295591": EDBIndicatorConfig(
        code="S019295591",
        name="总供应量:沥青:当月值",
        frequency="monthly",
        unit="万吨",
        source="同花顺金融",
        update_time="20251229",
        start_time="20220630",
        end_time="20251231",
        country="中国"
    ),
    "S019295592": EDBIndicatorConfig(
        code="S019295592",
        name="下游消费量:沥青:当月值",
        frequency="monthly",
        unit="万吨",
        source="同花顺金融",
        update_time="20251229",
        start_time="20220630",
        end_time="20251231",
        country="中国"
    )
}

# 按类别分组
CATEGORY_INDICATORS = {}
for code, config in ASPHALT_EDB_INDICATORS.items():
    if config.category not in CATEGORY_INDICATORS:
        CATEGORY_INDICATORS[config.category] = []
    CATEGORY_INDICATORS[config.category].append(code)

def get_indicators_by_category(category: str) -> List[str]:
    """根据类别获取指标代码列表"""
    return CATEGORY_INDICATORS.get(category, [])

def get_indicator_config(code: str) -> Optional[EDBIndicatorConfig]:
    """根据指标代码获取配置"""
    return ASPHALT_EDB_INDICATORS.get(code)
