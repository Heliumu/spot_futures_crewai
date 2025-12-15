# main.py

# 1. 在所有其他导入之前，最先加载环境变量
from dotenv import load_dotenv

from tasks.price_technical_analysis_task import create_price_technical_analysis_task

# find_dotenv() 会自动从当前目录开始，向上查找 .env 文件，非常可靠
load_dotenv()

# 2. 现在可以安全地导入你的其他模块了
from crewai import Agent, Crew, Task
from llm_config.factory import get_llm
from tools.data_fetching_tool import DataFetchingTool
from tools.zhipu_web_search_tool import ZhipuWebSearchTool

# 假设你的 Agent 定义在 agents.py 文件中
# from agents import price_technical_analyst 
# 为了演示，我们把 Agent 定义也放在这里
price_technical_analyst = Agent(
    role='期货交易分析师',
    goal='结合技术分析和市场情绪，对指定商品的期货价格进行研判，并给出未来展望和交易观点',
    backstory="""你是一位拥有超过10年实盘经验的资深期货交易分析师。
    你精通各种技术分析理论（如道氏理论、波浪理论、江恩理论等），对K线形态、技术指标和量价关系有深刻的理解。
    同时，你对市场情绪和突发新闻对价格的短期冲击有敏锐的洞察力。
    你的分析报告以数据驱动、观点鲜明、贴近实战而著称。""",
    verbose=True,
    allow_delegation=False,
    llm=get_llm("deepseek"),
    tools=[DataFetchingTool(), ZhipuWebSearchTool()]
)

# 3. 定义任务和执行 Crew
task_soybean_meal_recent = create_price_technical_analysis_task(
    commodity_name="豆粕",
    start_date="2024-01-01",
    end_date="2025-01-01"
)

crew = Crew(
    agents=[price_technical_analyst],
    tasks=[task_soybean_meal_recent],
    verbose=False
)

if __name__ == "__main__":
    print("启动期货分析任务...")
    result = crew.kickoff()
    print("\n\n===== 最终分析结果 =====")
    print(result)

