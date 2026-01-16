"""
AI交易Agent - 基于分析结果执行交易
"""
from crewai import Agent
from llm_config.factory import get_llm
from tools.trading_tool import TradingTool
from trading.trading_manager import trading_manager

deepseek_llm = get_llm("deepseek")

def create_trading_agent():
    """创建AI交易Agent"""
    trading_agent = Agent(
        role='AI交易执行官',
        goal='根据市场分析结果和风险控制规则，执行具体的交易操作',
        backstory="""你是一位经验丰富的AI交易员，具备以下能力：
        1. 分析市场信号并执行相应交易
        2. 严格遵守风险控制规则
        3. 监控交易执行状态
        4. 优化交易执行时机""",
        verbose=True,
        allow_delegation=False,
        llm=deepseek_llm,
        tools=[
            TradingTool()
        ]
    )
    return trading_agent
