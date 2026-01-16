# tasks/enhanced_intent_planning_task.py
import json
from crewai import Task
from agents.intent_agent import intent_planner
from nlp.intent_parser import EnhancedIntentParser
from config.ifind_edb_mapping import IFindEDBMapping
from typing import Dict, List

def create_enhanced_intent_planning_task(
    user_query: str
) -> Task:
    """
    创建增强版意图规划任务
    """
    parser = EnhancedIntentParser()
    edb_mapping = IFindEDBMapping()
    
    # 解析用户意图
    parsed_result = parser.parse_intent(user_query)
    
    # 构建详细的任务配置
    task_configs = []
    for task_config in parsed_result['task_configs']:
        task_type = task_config['type']
        indicators = edb_mapping.get_required_indicators(task_type)
        
        task_configs.append({
            'type': task_type,
            'indicators': indicators,
            'start_date': parsed_result['time_range']['start_date'],
            'end_date': parsed_result['time_range']['end_date'],
            'commodity': parsed_result['commodity_name']
        })
    
    # 构建描述
    description = f"""
请分析用户查询："${user_query}"。

你需要识别：
1. **商品名称** (commodity): {parsed_result['commodity_name']}
2. **市场区域** (market): cn (中国)
3. **标准化代码** (ticker): bu (沥青期货代码)

分析类型映射:
{json.dumps([t['type'] for t in task_configs], ensure_ascii=False)}

每个任务的具体配置:
{json.dumps(task_configs, ensure_ascii=False, indent=2)}

输出严格JSON，字段: commodity, market, ticker, task_configs。
只输出JSON，无其他内容。
    """
    
    return Task(
        description=description,
        expected_output="包含 commodity, market, ticker, task_configs 的JSON字符串",
        agent=intent_planner,
        output_json=True
    )
