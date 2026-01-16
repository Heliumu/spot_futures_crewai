# config/ifind_edb_mapping.py
from typing import Dict, List

class IFindEDBMapping:
    """
    iFinD EDB指标ID到项目任务的完整映射
    """
    
    def __init__(self):
        # ========== 核心业务分类 ==========
        self.core_categories = {
            'price': '价格',
            'basis': '基差',
            'inventory': '库存',
            'production': '产量',
            'supply': '供应',
            'demand': '需求',
            'cost_profit': '成本利润',
            'freight': '运费',
            'trade': '贸易',
            'macro': '宏观'
        }
        
        # ========== 指标分组定义 ==========
        self.edb_groups = {
            # 价格类
            'price_spot': [
                "S002861327", "S002861330", "S002861328", "S002861333", "S002861337",
                "S004156245", "S002861347", "S002861322", "S002861329", "S002861334",
                "S002861338", "S004156257", "S002861342", "S002861346", "S006899687",
                "S006899682", "S006899684", "S006899685", "S006899686", "S006899688",
                "S006899683", "S006824509", "S006824497", "S006824505", "S006824514",
                "S006824530", "S006824527", "S006824515", "S006824510", "S006824513",
                "S006824504", "S006824508", "S006824522", "S006824495", "S006824532",
                "S006824537", "S006824531", "S006824503", "S006824501", "S006824506",
                "S006824507", "S006824529", "S006824524", "S006824525", "S006824528",
                "S006824526", "S006824536", "S006824535", "S006824534", "S006824500",
                "S006824502", "S006824499", "S006824498", "S006824497", "S006824496",
                "S006824494", "S006824493", "S006824492", "S006824491", "S006824489",
                "S006824488", "S006824487", "S010471397", "S010471394", "S004157068",
                "S004157065", "S010863406", "S010863415", "S010863427", "S010863409",
                "S010863421", "S004157062", "S010863403", "S010863424", "S010863412",
                "S010863418"
            ],
            
            'price_futures': [
                "S012195660", "S012195681", "S012195705", "S012195704", "S012195647",
                "S003715029", "S003715031", "S004069735", "S004069734", "S004069736",
                "S012195585", "S012195606", "S012195630", "S012195629", "S012195572",
                "S003715030", "S003715032", "S004069731", "S004069732", "S004069733",
                "S004162657", "S004162658", "S004241719", "S004241720", "S004241721"
            ],
            
            'price_international': [
                "S006853437", "S006853438", "S006853439", "S006853440", "S006853441",
                "S006853442", "S006853443", "S006853444", "S006853445", "S006853447",
                "S006853446", "S006853448"
            ],
            
            # 库存类
            'inventory_manufacturer': [
                "S004494160", "S004494153", "S004494155", "S004494148", "S004494157",
                "S004494150", "S004494158", "S004494151", "S004494159", "S004494152",
                "S004494156", "S004494149", "S004494154", "S004494147", "S006155921",
                "S006155920"
            ],
            
            'inventory_social': [
                "S004494146", "S004494138", "S004494141", "S004494133", "S004494142",
                "S004494134", "S004494144", "S004494136", "S004494143", "S004494135",
                "S004494140", "S004494132", "S004494139", "S004494131", "S004494145",
                "S004494137"
            ],
            
            # 期货库存（日）
            'inventory_futures_daily': [
                "S004302779", "S004302777", "S004302778", "S004302764", "S004302766",
                "S004302768", "S004302771", "S004302772", "S004302767", "S004302770",
                "S004302769", "S004302776", "S004302775", "S004302773", "S009224012",
                "S004302781", "S004302782", "S009224013", "S009224015", "S004302784",
                "S009224010", "S006907003", "S006907005", "S006907004", "S009224014",
                "S009224016", "S009224011", "S004302790", "S004302786", "S009224008",
                "S004302791", "S004302787"
            ],
            
            # 期货库存（周）
            'inventory_futures_weekly': [
                "S007247253", "S004302829", "S004302837", "S004302836", "S004302840",
                "S004302839", "S004302835", "S004302833", "S007247429", "S004302811",
                "S004302822", "S007247455", "S004302825", "S004302824", "S004302823",
                "S004302818", "S004302819", "S004302816", "S004302821", "S004302820",
                "S004302817", "S004302815", "S004302813", "S004302827", "S004302826",
                "S004302828", "S004302804", "S007247423", "S004302807", "S004302806",
                "S004302805", "S004302800", "S004302801", "S004302798", "S004302803",
                "S004302802", "S004302799", "S004302797", "S004302795", "S004302809",
                "S004302808", "S004302810", "S004302793", "S007247476", "S004302859",
                "S004302867", "S004302866", "S004302870", "S004302869", "S004302865",
                "S016696683", "S016696681", "S016696682", "S016696684", "S004302860",
                "S007247459", "S004302863", "S004302861", "S004302841", "S004302855",
                "S004302854", "S004302853", "S004302848", "S004302849", "S004302846",
                "S004302851", "S004302850", "S004302847", "S004302845", "S004302843",
                "S004302852", "S004302857", "S004302858", "S004302856"
            ],
            
            # 产量类
            'production_weekly': [
                "S009134934", "S009134935", "S009134936", "S009134937", "S009134938",
                "S019295590"
            ],
            
            'production_monthly': [
                "S009135170", "S009135156", "S009135161", "S009135157", "S009135168",
                "S009135167", "S009135164", "S009135165", "S009135172", "S009135162",
                "S009135163", "S009135169", "S009135158", "S009135160", "S009135171",
                "S009135166", "S009135159"
            ],
            
            # 开工率类
            'operation_daily': [
                "S004494162", "S004494167", "S004494164", "S004494165", "S005972926",
                "S004494163", "S004494161", "S005972927"
            ],
            
            'operation_weekly': [
                "S019295428", "S019295422", "S019295426", "S019295424", "S019295423",
                "S019295427", "S019295429", "S019295425", "S019295430"
            ],
            
            # 供应类
            'supply_weekly': [
                "S016936186", "S016936187"
            ],
            
            # 贸易类
            'trade_import': [
                "S004450419", "S004450420", "S004450421", "S004450422", "S004450423",
                "S004450424", "S004450425", "S004450426", "S004450427", "S004450428"
            ],
            
            'trade_export': [
                "S004451029", "S004451030", "S004451031", "S004451032", "S004451033",
                "S004451034", "S004451035", "S004451036", "S004451037", "S004451038"
            ],
            
            # 成本利润类
            'cost_profit_weekly': [
                "S016936189", "S016936188", "S018556807"
            ],
            
            # 运费类
            'freight_daily': [
                "S019294526", "S019294527", "S019294528", "S019294529"
            ],
            
            # 消费类
            'consumption_monthly': [
                "S019295593", "S019295591", "S019295592"
            ]
        }
        
        # ========== 任务类型到指标分组的映射 ==========
        self.task_type_to_groups = {
            'basis': [
                'price_spot', 'price_futures', 'price_international',
                'inventory_social', 'inventory_futures_weekly',
                'freight_daily', 'cost_profit_weekly'
            ],
            
            'inventory': [
                'inventory_manufacturer', 'inventory_social',
                'inventory_futures_daily', 'inventory_futures_weekly',
                'production_weekly', 'operation_daily'
            ],
            
            'supply_demand': [
                'production_weekly', 'production_monthly',
                'operation_daily', 'operation_weekly',
                'supply_weekly',
                'inventory_manufacturer', 'inventory_social',
                'trade_import', 'trade_export'
            ],
            
            'apparent_demand': [
                'production_weekly', 'trade_import',
                'inventory_social', 'consumption_monthly'
            ],
            
            'demand_forecasting': [
                'consumption_monthly', 'production_weekly',
                'operation_daily', 'inventory_social',
                'price_futures', 'inventory_futures_weekly'
            ],
            
            'final_strategy': [
                'price_spot', 'price_futures', 'price_international',
                'inventory_manufacturer', 'inventory_social', 'inventory_futures_weekly',
                'production_weekly', 'production_monthly',
                'operation_daily', 'operation_weekly',
                'supply_weekly',
                'trade_import', 'trade_export',
                'cost_profit_weekly',
                'freight_daily',
                'consumption_monthly'
            ],
            
            'macro_economic': [
                'price_futures', 'price_international',
                'production_weekly', 'operation_daily',
                'inventory_social', 'inventory_futures_weekly',
                'trade_import', 'trade_export'
            ],
            
            'price_technical': [
                'price_futures',
                'inventory_futures_weekly',
                'production_weekly',
                'operation_daily'
            ],
            
            'quant_strategy': [
                'price_futures',
                'inventory_futures_weekly',
                'production_weekly',
                'operation_daily',
                'supply_weekly',
                'cost_profit_weekly',
                'freight_daily'
            ],
            
            'trading': [
                'price_futures',
                'inventory_futures_daily',
                'operation_daily',
                'cost_profit_weekly'
            ]
        }
    
    def get_required_indicators(self, task_type: str) -> List[str]:
        """根据任务类型获取所需的所有指标ID"""
        if task_type not in self.task_type_to_groups:
            return []
        
        groups = self.task_type_to_groups[task_type]
        indicators = set()
        
        for group_name in groups:
            if group_name in self.edb_groups:
                indicators.update(self.edb_groups[group_name])
        
        return list(indicators)
