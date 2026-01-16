# main/analysis_workflow_debug.py
from crewai import Crew, Process
from datetime import datetime
from nlp.intent_parser import IntentParser
from agents.ifind_agent import *  # 使用正式版Agent
from tasks.dynamic_task_factory import create_dynamic_tasks
import logging
from config.logging_config import setup_logging

# 设置日志
logger = setup_logging()

class AnalysisWorkflow:
    """调试版分析工作流引擎"""
    
    def __init__(self):
        self.intent_parser = IntentParser()
        logger.info("调试版分析工作流初始化完成")
    
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
            
            # 2. 验证时间范围
            if not self._validate_time_range(intent_result['time_range']):
                error_msg = "❌ 时间范围不合理，请使用合理的日期范围（如：最近3个月、近半年等）"
                logger.warning(error_msg)
                return error_msg
            
            # 3. 创建动态任务
            tasks = create_dynamic_tasks(intent_result)
            if not tasks:
                error_msg = "未能识别有效的分析任务，请提供更具体的分析需求。"
                logger.warning(error_msg)
                return error_msg
            
            print(f"\n=== 创建了 {len(tasks)} 个分析任务 ===")
            logger.info(f"创建了 {len(tasks)} 个分析任务")
            
            # 4. 创建Crew并执行
            agents = self._get_all_agents()
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
            logger.exception(f"分析过程异常: {e}")  # 记录完整堆栈
            return error_msg
    
    def _validate_time_range(self, time_range: dict) -> bool:
        """验证时间范围的合理性"""
        try:
            from datetime import datetime, timedelta
            start_date = datetime.strptime(time_range['start_date'], "%Y-%m-%d")
            end_date = datetime.strptime(time_range['end_date'], "%Y-%m-%d")
            today = datetime.now()
            
            if start_date > end_date:
                return False
            if end_date > today + timedelta(days=30):
                return False
            if start_date < today - timedelta(days=365*10):
                return False
                
            return True
        except ValueError:
            return False
    
    def _get_all_agents(self):
        """获取所有可用的Agent"""
        return [
            basis_analyst,
            inventory_analyst,
            supply_demand_analyst,
            macro_analyst,
            price_technical_analyst,
            quant_strategist,
            trading_analyst
        ]
