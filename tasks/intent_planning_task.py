# tasks/intent_planning_task.py
from crewai import Task
from agents.intent_agent import intent_planner

def create_intent_planning_task(user_query: str) -> Task:
    """创建意图规划任务"""
    return Task(
        description=f"""
请分析用户查询："${user_query}"。

你需要识别：
1. **商品名称** (commodity): 如 "铜", "原油", "比特币"
2. **市场区域** (market): 必须是以下之一:
   - 'cn': 沪/大商所/郑商所 (如 "沪铜", "螺纹钢")
   - 'us': CBOT/CME/NYMEX (如 "CBOT大豆", "WTI原油")
   - 'global': LME/ICE (如 "LME铜", "布伦特原油")
   - 'crypto': 加密货币 (如 "比特币", "以太坊")
   - 'forex': 外汇 (如 "美元兑人民币")
   默认为 'cn'。
3. **标准化代码** (ticker): 小写标准代码，如:
   - 沪铜→'cu', LME铜→'hg'
   - 螺纹钢→'rb', 豆粕→'m'
   - WTI→'cl', 布伦特→'brn'
   - 比特币→'btcusd'

分析类型映射（仅限以下）:
- "技术面"/"价格走势" → "price_technical"
- "基差" → "basis"
- "宏观" → "macro"
- "社会库存" → "inventory_social"
- "工厂库存" → "inventory_factory"
- "供需" → "supply_demand"
- "表观需求" → "apparent_demand"
- "需求预测" → "demand_forecasting"

输出严格JSON，字段: commodity, market, ticker, task_configs。
只输出JSON，无其他内容。
        """,
        expected_output="包含 commodity, market, ticker, task_configs 的JSON字符串",
        agent=intent_planner,
        output_json=True  # 确保输出为JSON格式
    )
