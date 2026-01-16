# main_workflow.py
from crewai import Crew, Process
from datetime import datetime
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()
print(f"Loading .env file from: {project_root / '.env'}")

# 导入模块
try:
    from agents.ifind_agent import *
    
    # 导入所有任务工厂函数
    from tasks.basis_analysis_task import create_basis_analysis_task
    from tasks.inventory_analysis_task import create_inventory_analysis_task
    from tasks.supply_demand_analysis_task import create_supply_demand_analysis_task
    from tasks.apparent_demand_analysis_task import create_apparent_demand_analysis_task
    from tasks.demand_forecasting_task import create_demand_forecasting_task
    from tasks.macro_economic_analysis_task import create_macro_economic_analysis_task
    from tasks.price_technical_analysis_task import create_price_technical_analysis_task
    
    # 导入预定义的任务实例
    from tasks.quant_strategy_task import quant_strategy_task
    from tasks.final_strategy_task import final_strategy_task
    
    print("✅ 所有模块导入成功")
    
except Exception as e:
    print(f"❌ 模块导入失败: {e}")
    raise

def run_full_analysis(commodity_name: str = "沥青"):
    """
    执行完整的分析流程
    """
    # 设置时间范围
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = "2025-12-01"
    
    # 设置标准参数
    region = "cn"  # 中国
    ticker = "bu"  # 沥青期货代码
    forecast_horizon = "3个季度"
    
    print(f"\n=== 开始分析 {commodity_name} ===")
    print(f"时间范围: {start_date} 至 {end_date}")
    print(f"市场区域: {region}, 标准代码: {ticker}")
    
    # 创建所有分析任务
    basis_task = create_basis_analysis_task(
        commodity_name=commodity_name,
        start_date=start_date,
        end_date=end_date
    )
    
    inventory_task = create_inventory_analysis_task(
        commodity_name=commodity_name,
        start_date=start_date,
        end_date=end_date
    )
    
    supply_demand_task = create_supply_demand_analysis_task(
        commodity_name=commodity_name,
        start_date=start_date,
        end_date=end_date
    )
    
    apparent_demand_task = create_apparent_demand_analysis_task(
        commodity_name=commodity_name,
        start_date=start_date,
        end_date=end_date
    )
    
    demand_forecasting_task = create_demand_forecasting_task(
        commodity_name=commodity_name,
        forecast_horizon=forecast_horizon
    )
    
    macro_economic_task = create_macro_economic_analysis_task(
        commodity_name=commodity_name,
        start_date=start_date,
        end_date=end_date
    )
    
    price_technical_task = create_price_technical_analysis_task(
        commodity_name=commodity_name,
        start_date=start_date,
        end_date=end_date,
        region=region,
        ticker=ticker
    )
    
    # 处理量化策略任务（预定义实例）
    if hasattr(quant_strategy_task, 'description'):
        quant_strategy_task.description = quant_strategy_task.description.format(
            commodity_name=commodity_name
        )
    
    if hasattr(quant_strategy_task, 'expected_output'):
        design_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        quant_strategy_report_template = quant_strategy_task.expected_output.replace(
            "{design_time}", design_time
        ).replace(
            "{commodity_name}", commodity_name
        )
        quant_strategy_task.expected_output = quant_strategy_report_template
    
    # 处理最终策略任务（预定义实例）
    if hasattr(final_strategy_task, 'description'):
        final_strategy_task.description = final_strategy_task.description.format(
            commodity_name=commodity_name
        )
    
    if hasattr(final_strategy_task, 'expected_output'):
        final_strategy_task.expected_output = final_strategy_task.expected_output.format(
            commodity_name=commodity_name
        )
    
    # 设置最终策略任务的上下文
    final_strategy_task.context = [
        basis_task, 
        inventory_task, 
        supply_demand_task,
        apparent_demand_task, 
        demand_forecasting_task,
        macro_economic_task, 
        price_technical_task,
        quant_strategy_task
    ]
    
    # 创建Crew
    crew = Crew(
        agents=[
            basis_analyst,
            inventory_analyst,
            supply_demand_analyst,
            macro_analyst,
            price_technical_analyst,
            quant_strategist,
            trading_analyst
        ],
        tasks=[
            basis_task,
            inventory_task,
            supply_demand_task,
            apparent_demand_task,
            demand_forecasting_task,
            macro_economic_task,
            price_technical_task,
            quant_strategy_task,
            final_strategy_task
        ],
        process=Process.sequential,
        verbose=True
    )
    
    # 执行分析
    print("\n=== 开始执行分析流程 ===")
    result = crew.kickoff()
    
    print("\n=== 分析完成 ===")
    return result

def test_system():
    """测试完整系统"""
    try:
        result = run_full_analysis("沥青")
        print("✅ 分析成功完成!")
        print("分析结果:")
        print(result)
    except Exception as e:
        print(f"❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_system()
