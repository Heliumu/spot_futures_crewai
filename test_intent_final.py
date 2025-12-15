import json
import sys
from dotenv import load_dotenv
from crewai import Crew, Process

# 0. 在所有其他导入之前，加载环境变量
load_dotenv()

# 1. 导入所有需要的 Agent 实例
from agents import chief_strategy_agent
from agents import price_technical_agent
from agents import basis_agent
from agents import inventory_agent
from agents import macro_economic_agent
from agents import supply_demand_agent
from agents.intent_agent import intent_planner
from agents.demand_forecasting_analyst import demand_forecasting_analyst
from agents.apparent_demand_analyst import apparent_demand_analyst



# 2. 导入所有任务的“工厂函数”（动态创建的任务）
from tasks.price_technical_analysis_task import create_price_technical_analysis_task
from tasks.basis_analysis_task import create_basis_analysis_task
from tasks.inventory_analysis_task import create_inventory_analysis_task
from tasks.macro_economic_analysis_task import create_macro_economic_analysis_task
from tasks.supply_demand_analysis_task import create_supply_demand_analysis_task
from tasks.intent_planning_task import create_intent_planning_task
from tasks.demand_forecasting_task import create_demand_forecasting_task
from tasks.apparent_demand_analysis_task import create_apparent_demand_analysis_task


# 3. 【方案A核心】直接导入最终战略任务的静态实例
from tasks.final_strategy_task import final_strategy_task


def analyze_user_query(user_query: str):
    """
    根据用户查询，动态规划并执行分析任务。
    """
    print(f"🤖 收到用户查询: '{user_query}'")

    # --- 阶段 1: 意图规划 ---
    if not intent_planner.llm:
        return "❌ 错误：意图规划 Agent (intent_planner) 未配置 LLM。请检查其定义。"

    planning_crew = Crew(
        agents=[intent_planner],
        tasks=[create_intent_planning_task(user_query)],
        verbose=True
    )
    
    # 【修改点 1】从 CrewOutput 对象中获取原始字符串
    crew_output = planning_crew.kickoff()
    plan_json_str = crew_output.raw
    
    try:
        plan = json.loads(plan_json_str)
        commodity = plan['commodity']
        task_configs = plan['task_configs']
        print(f"📋 分析计划已生成: {json.dumps(plan, indent=2, ensure_ascii=False)}")
    except (json.JSONDecodeError, KeyError) as e:
        return f"❌ 无法解析分析计划: {e}\n原始输出: {plan_json_str}"

    # --- 阶段 2: 动态组装和执行 ---
    tasks_to_run = []
    
    for task_name, config in task_configs.items():
        if task_name == "basis":
            tasks_to_run.append(create_basis_analysis_task(commodity_name=commodity, **config))
        elif task_name == "macro":
            tasks_to_run.append(create_macro_economic_analysis_task(commodity_name=commodity, **config))
        elif task_name == "supply_demand":
            tasks_to_run.append(create_supply_demand_analysis_task(commodity_name=commodity, **config))
        elif task_name == "price_technical":
            tasks_to_run.append(create_price_technical_analysis_task(commodity_name=commodity, **config))
        elif task_name == "inventory_social":
            tasks_to_run.append(create_inventory_analysis_task(commodity_name=commodity, inventory_type='social', **config))
        elif task_name == "inventory_factory":
            tasks_to_run.append(create_inventory_analysis_task(commodity_name=commodity, inventory_type='factory', **config))
        elif task_name == "demand_forecasting":
            tasks_to_run.append(create_demand_forecasting_task(commodity_name=commodity, forecast_horizon="2个季度", **config))
        elif task_name == "apparent_demand":
            tasks_to_run.append(create_apparent_demand_analysis_task(commodity_name=commodity, **config))



        else:
            print(f"⚠️ 警告: 未知的任务类型 '{task_name}'，已跳过。")

    if not tasks_to_run:
        return "❌ 根据您的意图，未能生成任何具体的分析任务。"
    
    # 如果任务超过一个，则添加最终战略任务
    if len(tasks_to_run) > 1:
        # 【核心修改】使用 context 属性设置任务间的顺序依赖
        for i in range(1, len(tasks_to_run)):
            # 第 i 个任务依赖于第 i-1 个任务的输出
            tasks_to_run[i].context = [tasks_to_run[i-1]]
        
        # 创建并配置最终任务
        final_task = final_strategy_task
        # 最终任务依赖于所有前置任务（传入Task对象列表）
        final_task.context = [task for task in tasks_to_run]
        tasks_to_run.append(final_task)

    agents_needed = list({task.agent for task in tasks_to_run})

    # --- 阶段 3: 执行最终 Crew ---
    analysis_crew = Crew(
        agents=agents_needed,
        tasks=tasks_to_run,
        process=Process.sequential,
        verbose=True
    )
    
    # 【修改点 2】从 CrewOutput 对象中获取最终的字符串报告
    crew_output = analysis_crew.kickoff()
    result = crew_output.raw
    return result


if __name__ == "__main__":
    # 【重要】请确保你的 intent_planner 在 agents/__init__.py 中被正确创建并配置了 LLM
    # 例如，在 agents/__init__.py 中:
    # from llm_config.factory import get_llm
    # from .intent_agent import intent_planner as _intent_planner
    # _intent_planner.llm = get_llm("gpt-4o") # 配置 LLM
    # intent_planner = _intent_planner

    # 模拟用户输入
    query1 = "帮我分析一下最近三个月沥青的基差情况。"
    query2 = "对沥青进行一次全面的分析，包括宏观和技术面。"
    query3 = "分析沥青最近一年的社会库存和技术面情况。"
    
    # 执行并打印结果
    queries_to_run = [query1,query2,query3]
    
    for i, query in enumerate(queries_to_run, 1):
        print(f"\n\n{'='*20} 开始执行查询 {i}: {query} {'='*20}")
        result = analyze_user_query(query)
        print(f"\n\n{'='*20} 查询 {i} 最终报告 {'='*20}\n")
        print(result)
        print("\n" + "#"*50 + "\n")

