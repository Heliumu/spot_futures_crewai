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


# 2. 导入所有任务的“工厂函数”（动态创建的任务）
from tasks.price_technical_analysis_task import create_price_technical_analysis_task
from tasks.basis_analysis_task import create_basis_analysis_task
from tasks.inventory_analysis_task import create_inventory_analysis_task
from tasks.macro_economic_analysis_task import create_macro_economic_analysis_task
from tasks.supply_demand_analysis_task import create_supply_demand_analysis_task

# 3. 【方案A核心】直接导入最终战略任务的静态实例
from tasks.final_strategy_task import final_strategy_task


def run_commodity_analysis(
    commodity_name: str,
    task_configs: dict 
) -> str:
    """
    运行一个完整的商品分析流程，并返回最终的战略决策报告。

    Args:
        commodity_name (str): 需要分析的商品名称，例如 "大豆"。
        task_configs (dict): 任务配置字典，包含分析类型和时间范围。

    Returns:
        str: 最终生成的 Markdown 格式战略决策报告。
    """
    print(f"🚀 启动对【{commodity_name}】的综合分析流程...")
    print(f"📅 分析时间范围: {task_configs['start_date']} 至 {task_configs['end_date']}")
    # 示例配置
    

    
    # --- 步骤 1: 动态创建所有前置分析任务 ---
    macro_task = create_macro_economic_analysis_task(
        commodity_name=commodity_name, 
        **task_configs.get("macro", {"start_date": "2022-01-01", "end_date": "2025-01-01"}),
        )
    supply_demand_task = create_supply_demand_analysis_task(
        commodity_name=commodity_name, 
        **task_configs.get("supply_demand", {"start_date": "2021-01-01", "end_date": "2025-01-01"}),
        )
    
    # 【关键】创建两个独立的库存分析任务
    social_inventory_task = create_inventory_analysis_task(
        commodity_name=commodity_name, 
        **task_configs.get("inventory_social", {"start_date": "2023-01-01", "end_date": "2025-01-01"}),
        inventory_type='social'
        )
    factory_inventory_task = create_inventory_analysis_task(
        commodity_name=commodity_name, 
        **task_configs.get("inventory_factory", {"start_date": "2023-01-01", "end_date": "2025-01-01"}),
        inventory_type='factory'
        )
    
    basis_task = create_basis_analysis_task(
        commodity_name=commodity_name, 
        **task_configs.get("basis", {"start_date": "2022-01-01", "end_date": "2025-01-01"}),
        )
    price_task = create_price_technical_analysis_task(
        commodity_name=commodity_name, 
        **task_configs.get("price_technical", {"start_date": "2024-01-01", "end_date": "2025-01-01"}),)

    # --- 步骤 2: 定义前置任务的执行顺序 ---
    (macro_task >> supply_demand_task >> 
     social_inventory_task >> factory_inventory_task >> 
     basis_task >> price_task)

    # --- 步骤 3: 【方案A核心】为静态的最终任务动态设置上下文 ---
    #    将所有前置任务的输出作为最终任务的输入
    final_strategy_task.context = [
        macro_task.output,
        supply_demand_task.output,
        social_inventory_task.output,
        factory_inventory_task.output,
        basis_task.output,
        price_task.output
    ]

    # --- 步骤 4: 创建并配置 Crew ---
    #    tasks 列表中包含所有动态创建的任务和静态导入的最终任务
    final_decision_crew = Crew(
        agents=[
            macro_economic_agent,
            supply_demand_agent,
            inventory_agent,
            basis_agent,
            price_technical_agent,
            chief_strategy_agent  # 最终决策者
        ],
        tasks=[
            macro_task,
            supply_demand_task,
            social_inventory_task,
            factory_inventory_task,
            basis_task,
            price_task,
            final_strategy_task  # 使用静态导入的最终任务实例
        ],
        process=Process.sequential,
        verbose=True  # 建议设为 True 以便调试和观察执行过程
    )

    # --- 步骤 5: 启动 Crew ---
    #    由于所有参数已在任务创建时传入，这里不再需要 inputs 字典
    result = final_decision_crew.kickoff()

    return result


# --- 程序入口 ---
if __name__ == "__main__":
    # 检查 Python 环境
    print(f"当前使用的 Python 解释器: {sys.executable}\n")
    task_configs = {
        "macro": {
            "start_date": "2020-01-01",
            "end_date": "2025-01-01"
        },
        "supply_demand": {
            "start_date": "2021-01-01",
            "end_date": "2025-01-01"
        },
        "inventory_social": {
            "start_date": "2023-01-01",
            "end_date": "2025-01-01"
        },
        "inventory_factory": {
            "start_date": "2023-01-01",
            "end_date": "2025-01-01"
        },
        "basis": {
            "start_date": "2022-01-01",
            "end_date": "2025-01-01"
        },
        "price_technical": {
            "start_date": "2024-01-01",
            "end_date": "2025-01-01"
        }
    }
    # 在这里配置你想要分析的商品
    commodity_to_analyze = "大豆"
    # 你也可以自定义时间范围
    # analysis_start_date = "2023-01-01"
    # analysis_end_date = "2024-12-31"

    try:
        # 调用核心分析函数
        final_report = run_commodity_analysis(commodity_name=commodity_to_analyze)
        
        # 打印最终结果
        print("\n\n======================== 最终战略决策报告 ========================\n")
        print(final_report)

    except Exception as e:
        print(f"\n❌ 分析过程中发生错误: {e}")
        # 在这里可以添加更详细的错误日志记录

