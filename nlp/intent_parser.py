# nlp/intent_parser.py
import re
from datetime import datetime, timedelta
from typing import Dict, List

class IntentParser:
    """修复版用户意图解析器 - 正确处理时间范围"""
    
    def __init__(self):
        # 修正时间关键词映射 - 按优先级排序，精确匹配优先
        self.time_patterns = [
            (r'半年', 180),           # 半年 = 180天
            (r'(\d+)\s*年', lambda x: int(x) * 365),
            (r'(\d+)\s*个月', lambda x: int(x) * 30),
            (r'(\d+)\s*周', lambda x: int(x) * 7),
            (r'(\d+)\s*天', lambda x: int(x)),
            (r'最近|近期', 90),       # 最近 = 90天
            (r'历史|长期', 1825),     # 历史 = 5年
        ]
        
        self.keyword_mappings = {
            '基差': ['basis'],
            '仓储|库存': ['inventory'],
            '产量|生产': ['production'],
            '开工率|开工': ['operation'],
            '供应|出货': ['supply'],
            '消费|需求|表观需求': ['demand'],
            '宏观|宏观经济': ['macro'],
            '技术面|价格走势': ['technical'],
            '量化|算法|回测': ['quantitative'],
            '交易|操作|执行': ['trading'],
            '策略|建议': ['strategy'],
            '套利': ['arbitrage']
        }
    
    def parse_intent(self, user_input: str) -> Dict:
        """解析用户意图"""
        time_range = self._extract_time_range(user_input)
        keywords = self._extract_keywords(user_input)
        task_configs = self._identify_tasks(keywords)
        commodity = self._extract_commodity(user_input)
        
        return {
            'commodity': commodity or "沥青",
            'time_range': time_range,
            'keywords': keywords,
            'task_configs': task_configs,
            'original_input': user_input
        }
    
    def _extract_time_range(self, text: str) -> Dict[str, str]:
        """提取时间范围 - 修正版"""
        end_date = datetime.now().strftime("%Y-%m-%d")
        
        # 默认设置为半年（180天）
        days_back = 180
        
        # 按优先级顺序检查时间模式
        found_match = False
        for pattern, day_value in self.time_patterns:
            match = re.search(pattern, text)
            if match:
                if isinstance(day_value, int):
                    days_back = day_value
                else:
                    # 处理lambda函数
                    try:
                        if pattern.startswith(r'(\d+)'):
                            days_back = day_value(match.group(1))
                        else:
                            days_back = day_value(None)
                    except:
                        days_back = 180
                found_match = True
                break  # 找到第一个匹配就停止（按优先级）
        
        # 如果没有找到任何时间关键词，使用默认半年
        if not found_match:
            days_back = 180
        
        start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        return {'start_date': start_date, 'end_date': end_date}
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        found_keywords = set()
        text_lower = text.lower()
        
        for keyword_pattern, categories in self.keyword_mappings.items():
            if re.search(keyword_pattern, text_lower):
                found_keywords.update(categories)
        
        return list(found_keywords)
    
    def _identify_tasks(self, keywords: List[str]) -> List[Dict]:
        """识别需要执行的任务"""
        task_types = {
            'basis': 'basis',
            'inventory': 'inventory',
            'production': 'supply_demand',
            'operation': 'supply_demand',
            'supply': 'supply_demand',
            'demand': 'apparent_demand',
            'macro': 'macro_economic',
            'technical': 'price_technical',
            'quantitative': 'quant_strategy',
            'trading': 'trading',
            'strategy': 'final_strategy',
            'arbitrage': 'basis'
        }
        
        tasks = {}
        for keyword in keywords:
            if keyword in task_types:
                task_type = task_types[keyword]
                tasks[task_type] = {'type': task_type}
        
        # 如果包含最终/综合等词，添加最终策略
        if any(word in ['最终', '综合', '完整'] for word in keywords):
            tasks['final_strategy'] = {'type': 'final_strategy'}
        
        return list(tasks.values())
    
    def _extract_commodity(self, text: str) -> str:
        """提取商品名称"""
        commodities = ['沥青', '螺纹钢', '铜', '原油', '铝']
        for comm in commodities:
            if comm in text:
                return comm
        return "沥青"
