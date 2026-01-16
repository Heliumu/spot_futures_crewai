# tasks/trading_task.py
"""
AI交易任务
"""
from crewai import Task
from agents.trading_agent import create_trading_agent

def create_trading_task(analysis_result: str, user_query: str) -> Task:
    """创建交易执行任务"""
    trading_agent = create_trading_agent()
    
    return Task(
        description=f"""
        根据以下分析结果执行交易操作：
        {analysis_result}
        
        用户原始查询：{user_query}
        
        请根据分析结果中的信号执行相应的交易操作。
        交易策略：
        1. 如果分析建议买入且当前无持仓，执行买入
        2. 如果分析建议卖出且当前有相应持仓，执行平仓
        3. 如果分析建议加仓且已有持仓，执行加仓
        4. 严格控制风险，单笔交易不超过可用资金的20%
        5. 优先使用市价单确保成交
        
        只输出交易执行结果，包含订单ID和执行状态。
        """,
        expected_output="交易执行结果，包含具体的操作类型、交易代码、数量、价格和订单ID",
        agent=trading_agent,
        output_json=False
    )
