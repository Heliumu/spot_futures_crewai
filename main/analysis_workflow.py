# main/analysis_workflow_fixed.py
from crewai import Crew, Process
from datetime import datetime
from nlp.intent_parser import IntentParser
from agents.ifind_agent import *
from tasks.dynamic_task_factory import create_dynamic_tasks
import logging
from config.logging_config import setup_logging

# 设置日志
logger = setup_logging()

class AnalysisWorkflowFixed:
    """修复版分析工作流引擎"""
    
    def __init__(self):
        self.intent_parser = IntentParser()
        logger.info("分析工作流初始化完成")
    
    def execute_analysis(self, user_input: str):
        """执行完整分析流程"""
        try:
            print(f"=== 收到用户请求 ===\n{user_input}\n")
            logger.info(f"收到用户请求: {user_input}")
            
            # 1. 解析用户意图
            intent_result = self.intent_parser.parse_intent(user_input)
            print(f"=== 意图解析结果 ===")
            print(f"商品: {intent_result['commodity']}")
            print(f"时间范围: {intent_result['time_range']['start_date']} 至 {intent_result['time_range']['end_date']}")
            print(f"识别任务: {[t['type'] for t in intent_result['task_configs']]}")
            logger.info(f"意图解析完成: {intent_result}")
            
            # 2. 创建动态任务
            tasks = create_dynamic_tasks(intent_result)
            if not tasks:
                return "未能识别有效的分析任务，请提供更具体的分析需求。"
            
            print(f"\n=== 创建了 {len(tasks)} 个分析任务 ===")
            logger.info(f"创建了 {len(tasks)} 个分析任务")
            
            # 3. 创建Crew并执行
            agents = [
                basis_analyst,
                inventory_analyst,
                supply_demand_analyst,
                macro_analyst,
                price_technical_analyst,
                quant_strategist,
                trading_analyst
            ]
            
            crew = Crew(
                agents=agents,
                tasks=tasks,
                process=Process.sequential,
                verbose=True
            )
            
            print("\n=== 开始执行分析 ===")
            logger.info("开始执行分析流程")
            result = crew.kickoff()
            
            print("\n=== 分析完成 ===")
            logger.info("分析流程完成")
            return result
            
        except KeyboardInterrupt:
            logger.warning("分析被用户中断")
            return "分析被用户中断"
        except Exception as e:
            error_msg = f"分析过程中发生错误: {str(e)}"
            logger.exception(f"分析过程异常: {e}")
            return error_msg
