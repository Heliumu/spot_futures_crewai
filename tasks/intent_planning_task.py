from datetime import datetime
from crewai import Task
from agents.intent_agent import intent_planner

def create_intent_planning_task(user_query: str) -> Task:
    current_date = datetime.now().strftime("%Y-%m-%d")
    return Task(
        description=(
            f"今天是 {current_date}。\n\n"  # <-- 关键1：告诉 Agent 今天是哪一天
            f"请分析用户的查询意图：'{user_query}'。\n"
            "你需要识别出用户想分析的商品、分析的范围以及时间范围。\n\n"
            # --- 关键2：限定分析类型的白名单 ---
            "你必须从以下预定义的分析类型列表中选择，不要创造新的类型：\n"
            "- basis\n"
            "- macro\n"
            "- supply_demand\n"
            "- price_technical\n"
            "- inventory_social\n"
            "- inventory_factory\n\n"
            "_ apparently_demand\n"
            "_ demand_forecasting\n\n"
            # --- 关键3：建立用户意图到类型的映射 ---
            "请注意映射规则：\n"
            "- 如果用户提到'价格走势'、'技术面'、'技术分析'，请映射到 'price_technical'。\n"
            "- 如果用户提到'基差'，请映射到 'basis'。\n"
            "- 如果用户提到'宏观'，请映射到 'macro'。\n\n"
            "- 如果用户提到'需求'、'需求分析'，请映射到 'supply_demand'。\n"
            "- 如果用户提到'库存'、'社会库存'、'社会库存分析'，请映射到 'inventory_social'。\n"
            "- 如果用户提到'工厂库存'、'工厂库存分析'，请映射到 'inventory_factory'。\n"
            "- 如果用户提到'表观需求'、'表观需求分析'，请映射到 'apparent_demand'。\n"
            "- 如果用户提到'需求预测'、'需求预测分析'，请映射到 'demand_forecasting'。\n\n"
            # --- 关键4：明确日期计算逻辑 ---
            "所有日期范围都必须相对于当前日期 ({current_date}) 计算。\n"
            "结束日期应为当前日期。\n"
            "开始日期根据用户请求计算（例如，'近10年' 意味着开始日期是10年前的今天）。\n"
            "如果用户没有指定时间范围，请根据分析类型给出合理的默认时间范围（这些默认范围也应相对于当前日期计算）。\n\n"
            # --- 原有的结构要求 ---
            "然后，将这些信息整合成一个JSON对象。"
            "JSON对象必须包含两个键：'commodity' (字符串) 和 'task_configs' (对象)。"
            "'task_configs' 是一个字典，其键是上面指定的任务名，值是包含 'start_date' 和 'end_date' 的对象。"
            "只输出JSON，不要有任何其他解释。"
        ),
        expected_output="一个包含 'commodity' 和 'task_configs' 的JSON字符串。",
        agent=intent_planner
    )