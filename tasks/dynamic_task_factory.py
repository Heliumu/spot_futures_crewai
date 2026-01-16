# tasks/dynamic_task_factory_complete.py
from crewai import Task
from typing import Dict, List
from datetime import datetime

def create_dynamic_tasks(intent_result: Dict) -> List[Task]:
    """根据意图解析结果创建动态任务"""
    tasks = []
    commodity = intent_result['commodity']
    start_date = intent_result['time_range']['start_date']
    end_date = intent_result['time_range']['end_date']
    
    for task_config in intent_result['task_configs']:
        task_type = task_config['type']
        task = _create_task_by_type(task_type, commodity, start_date, end_date)
        if task:
            tasks.append(task)
    
    return tasks

def _create_task_by_type(task_type: str, commodity: str, start_date: str, end_date: str) -> Task:
    """根据任务类型创建具体任务"""
    
    # 基差分析任务
    if task_type == 'basis':
        description = f"""
你是一位资深基差分析师，专注于【{commodity}】。
请对{commodity}进行基差分析。

请严格按照以下步骤执行：
1. **获取基差数据**：使用 '获取EDB数据用于基差分析' 工具获取 {commodity} 从 {start_date} 到 {end_date} 的基差相关数据。
   - start_date: {start_date}
   - end_date: {end_date}

2. **执行分析**：基于获取到的数据，你需要从以下几个核心维度进行深入分析：
   a) **全国基差走势**：计算年度、季度基差的均价、最大/最小值和波动区间；识别季节性规律；重点分析近1个月的变化。
   b) **区域基差差异**：对比主要产销区（如华北、华南、华东）的基差强弱；识别稳定价差的区域对；计算并明确跨区域套利的触发阈值。

3. **撰写报告**：将你的所有分析结果，严格遵循给定的 Markdown 模板格式，撰写最终的专业报告。
"""
        
        expected_output = f"""
# {commodity} 基差分析报告

## 数据来源与方法声明
本报告数据来源于iFinD经济数据库，时间范围为 {start_date} 至 {end_date}。

---

## 一、全国基差走势分析 ({start_date} - {end_date})

- **历史统计特征**:
    - **年度均价**: [计算并填写]
    - **季度均价**: [计算并填写]
    - **历史最大值**: [填写数值和日期]
    - **历史最小值**: [填写数值和日期]
    - **主要波动区间**: [描述]

- **季节性规律**:
    - [描述基差在一年中的季节性变化规律]

- **近期变化分析 (近1个月)**:
    - [描述近1个月基差的具体变化趋势]

---

## 二、区域基差差异分析 ({start_date} - {end_date})

- **主要产销区基差对比**:
    - **华北**: [描述该区域基差的强弱特征]
    - **华南**: [描述该区域基差的强弱特征]
    - **华东**: [描述该区域基差的强弱特征]

- **跨区域套利机会分析**:
    - **稳定价差区域对**: [识别出价差关系稳定的区域对]
    - **套利触发阈值**: **[计算并明确指出当A地与B地价差超过多少元/吨时，套利窗口打开]**。

---

## 三、基差走势预测与交易策略

- **未来1-3个月基差走势预测**:
    - [基于历史规律和当前市场状况，预测未来基差的走势方向]

- **交易策略与风险提示**:
    - **策略建议**: [基于基差视角，提出具体的交易策略，如期现套利、跨期套利等。]
    - **风险提示**: [指出可能影响基差走势的主要风险点]

---

## 四、核心总结

[用一段话总结当前 {commodity} 基差市场的核心特征和主要机会/风险。]
"""
        
        from agents.ifind_agent import basis_analyst
        return Task(
            description=description,
            expected_output=expected_output,
            agent=basis_analyst,
            async_execution=False
        )
    
    # 库存分析任务
    elif task_type == 'inventory':
        description = f"""
你是一位专业的库存分析师，专注于【{commodity}】。
请对{commodity}进行库存分析。

请严格按照以下步骤执行：
1. **获取库存数据**：使用 '获取EDB数据用于库存分析' 工具获取 {commodity} 从 {start_date} 到 {end_date} 的库存相关数据。
   - start_date: {start_date}
   - end_date: {end_date}

2. **执行分析**：基于获取到的数据，分析厂家库存、社会库存、期货仓单等维度。

3. **撰写报告**：将分析结果整理成专业的库存分析报告。
"""
        
        expected_output = f"""
# {commodity} 库存分析报告

## 分析时间
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 一、核心观点
[在此处填写你的核心判断，1-2句话]

## 二、库存总览
- **总量与变化**: [社会库存总量及周度/月度变化]
- **主要集散地**: [列出库存量排名靠前的仓库或港口]

## 三、产业链库存动态
- **上游情况**: [原料库存状态]
- **中游情况**: [贸易商库存及心态]
- **下游情况**: [加工企业原料库存水平]

## 四、市场展望与策略
- **库存趋势预判**: [对未来库存变化的判断]
- **价格影响评估**: [库存变化对价格的影响]
- **投资机会提示**: [基于分析发现的潜在机会]
- **风险提示**: [需要关注的风险因素]
"""
        
        from agents.ifind_agent import inventory_analyst
        return Task(
            description=description,
            expected_output=expected_output,
            agent=inventory_analyst,
            async_execution=False
        )
    
    # 供需分析任务
    elif task_type == 'supply_demand':
        description = f"""
你是一位资深的产业链研究员，专注于【{commodity}】。
请对{commodity}进行供需分析。

请严格按照以下步骤执行：
1. **获取供需数据**：使用 '获取EDB数据用于供需分析' 工具获取 {commodity} 从 {start_date} 到 {end_date} 的供需相关数据。
   - start_date: {start_date}
   - end_date: {end_date}

2. **执行分析**：基于获取到的数据，分析产量、开工率、进出口、消费等维度。

3. **撰写报告**：将分析结果整理成专业的供需分析报告。
"""
        
        expected_output = f"""
# {commodity} 供需分析报告

## 一、供应端分析

### 1. 国内产量与进口量
- **国内产量趋势 ({start_date} - {end_date})**: [描述近3-5年的变化趋势]
- **进口量趋势 ({start_date} - {end_date})**: [描述进口量的变化]
- **主要来源国及占比**: [列出主要进口来源国及其近年来的占比变化]

### 2. 全球市场动态
- **主要生产国情况**: [分析全球主要生产国的产量、库存和出口政策变化]
- **全球供需格局**: [对全球整体供需状况进行简要描述]

## 二、需求端分析

### 1. 国内表观消费量
- **消费量趋势 ({start_date} - {end_date})**: [描述国内表观消费量的变化趋势]
- **下游主要行业需求**: [分析下游主要行业的需求变化和驱动因素]

### 2. 长期影响因素
- **替代品影响**: [分析是否有替代品在冲击市场需求]
- **技术变革**: [分析技术变革对长期需求的潜在影响]

## 三、库存状况与市场定性

### 1. 库存水平分析
- **港口/工厂/下游库存**: [分析各环节库存的近3-5年同期水平]
- **库存消费比**: [根据数据计算并分析库存消费比的变化]

### 2. 市场基本面定性判断
**最终结论**: [从“供需宽松”、“供需紧张”、“供需基本平衡”三选一，并给出简要理由]
"""
        
        from agents.ifind_agent import supply_demand_analyst
        return Task(
            description=description,
            expected_output=expected_output,
            agent=supply_demand_analyst,
            async_execution=False
        )
    
    # 表观需求分析任务
    elif task_type == 'apparent_demand':
        description = f"""
你是一位专业的表观需求分析师，专注于【{commodity}】。
请对{commodity}进行表观需求分析。

请严格按照以下步骤执行：
1. **获取表观需求数据**：使用 '获取EDB数据用于表观需求分析' 工具获取 {commodity} 从 {start_date} 到 {end_date} 的表观需求相关数据。
   - start_date: {start_date}
   - end_date: {end_date}

2. **执行分析**：基于获取到的数据，分析表观需求的变化趋势和驱动因素。

3. **撰写报告**：将分析结果整理成专业的表观需求分析报告。
"""
        
        expected_output = f"""
# {commodity} 表观需求分析报告

## 一、表观需求计算
- **表观需求公式**: 产量 + 进口量 - 出口量
- **历史表观需求趋势**: [描述表观需求的历史变化]

## 二、需求驱动因素
- **宏观经济因素**: [分析GDP、PMI等宏观指标对需求的影响]
- **行业特定因素**: [分析下游行业的景气度变化]

## 三、需求预测
- **短期需求展望**: [未来1-3个月的需求预期]
- **中长期需求趋势**: [未来6-12个月的需求趋势]

## 四、结论
[总结表观需求的核心观点和主要风险点]
"""
        
        from agents.ifind_agent import supply_demand_analyst
        return Task(
            description=description,
            expected_output=expected_output,
            agent=supply_demand_analyst,
            async_execution=False
        )
    
    # 需求预测任务
    elif task_type == 'demand_forecasting':
        description = f"""
你是一位大宗商品量化预测分析师，专注于【{commodity}】。
请对{commodity}进行需求预测。

请严格按照以下步骤执行：
1. **获取需求预测数据**：使用 '获取EDB数据用于需求预测' 工具获取 {commodity} 从 {start_date} 到 {end_date} 的需求预测相关数据。
   - start_date: {start_date}
   - end_date: {end_date}

2. **执行分析**：基于获取到的数据，构建需求预测模型。

3. **撰写报告**：将分析结果整理成专业的需求预测报告。
"""
        
        expected_output = f"""
# {commodity} 未来需求预测报告

## 数据来源与方法声明
本报告基于历史数据及权威机构的宏观、行业前瞻性预测。预测模型采用多因素情景分析法，旨在提供未来3个季度的需求展望。

---

## 一、预测摘要

| 情景 | 未来1季度需求预测 | 未来2季度需求预测 | 未来3季度需求预测 |
| :--- | :--- | :--- | :--- |
| **基准情景** | [预测值] | [预测值] | [预测值] |
| **乐观情景** | [预测值] | [预测值] | [预测值] |
| **悲观情景** | [预测值] | [预测值] | [预测值] |

---

## 二、模型逻辑与核心假设

- **预测框架**:
    - [描述你使用的预测模型，例如：基于下游行业开工率和PMI的多元回归模型，或基于领先指标的加权评分模型。]

- **核心假设**:
    - [列出本次预测所依赖的最重要的3-5个假设]

---

## 三、关键驱动变量展望

- **宏观经济指标**:
    - [分析GDP、PMI等关键宏观指标的未来预期]

- **行业特定指标**:
    - [分析关键下游行业的未来景气度预测]

---

## 四、预测结果与不确定性

- **预测走势图**:
    - [描述历史需求与未来三种情景下预测需求的走势图]

- **核心风险与不确定性**:
    - [列出可能对预测结果产生重大影响的负面和正面风险]

---

## 五、结论

[用一段话总结对未来3个季度 {commodity} 需求的核心判断，以及最需要关注的变量和风险点。]
"""
        
        from agents.ifind_agent import supply_demand_analyst
        return Task(
            description=description,
            expected_output=expected_output,
            agent=supply_demand_analyst,
            async_execution=False
        )
    
    # 宏观经济分析任务
    elif task_type == 'macro_economic':
        description = f"""
你是一位专业的宏观经济分析师，专注于【{commodity}】。
请对{commodity}进行宏观经济分析。

请严格按照以下步骤执行：
1. **获取宏观经济数据**：使用 '获取EDB数据用于宏观经济分析' 工具获取 {commodity} 从 {start_date} 到 {end_date} 的宏观经济相关数据。
   - start_date: {start_date}
   - end_date: {end_date}

2. **执行分析**：基于获取到的数据，分析宏观经济对商品市场的影响。

3. **撰写报告**：将分析结果整理成专业的宏观经济分析报告。
"""
        
        expected_output = f"""
# {commodity} 宏观经济分析报告

## 一、宏观经济环境
- **GDP增长**: [描述GDP增长趋势及其对商品需求的影响]
- **货币政策**: [分析利率、流动性等货币政策对商品价格的影响]
- **财政政策**: [分析财政刺激、基建投资等对商品需求的影响]

## 二、商品市场宏观驱动
- **通胀水平**: [分析CPI、PPI等通胀指标对商品定价的影响]
- **汇率变动**: [分析汇率变动对进口成本和出口竞争力的影响]
- **政策导向**: [分析产业政策、环保政策等对供需的影响]

## 三、宏观展望
- **短期宏观预期**: [未来3-6个月的宏观环境预期]
- **中长期宏观趋势**: [未来1-2年的宏观趋势判断]

## 四、结论与建议
[总结宏观面对{commodity}的核心影响和投资建议]
"""
        
        from agents.ifind_agent import macro_analyst
        return Task(
            description=description,
            expected_output=expected_output,
            agent=macro_analyst,
            async_execution=False
        )
    
    # 价格技术分析任务
    elif task_type == 'price_technical':
        description = f"""
你是一位专业的技术分析师，专注于【{commodity}】。
请对{commodity}进行价格技术分析。

请严格按照以下步骤执行：
1. **获取价格技术数据**：使用 '获取EDB数据用于价格技术分析' 工具获取 {commodity} 从 {start_date} 到 {end_date} 的价格技术相关数据。
   - start_date: {start_date}
   - end_date: {end_date}

2. **执行分析**：基于获取到的数据，进行技术面分析。

3. **撰写报告**：将分析结果整理成专业的价格技术分析报告。
"""
        
        expected_output = f"""
# {commodity} 技术面分析报告

## 一、趋势分析
- **主要趋势**: [判断当前主要趋势方向（上涨、下跌、震荡）]
- **趋势强度**: [评估趋势的强度和持续性]

## 二、关键位置
- **支撑位**: [识别重要的支撑位]
- **阻力位**: [识别重要的阻力位]
- **突破信号**: [分析潜在的突破信号]

## 三、量价关系
- **成交量验证**: [结合成交量验证价格走势]
- **持仓量分析**: [分析持仓量变化对价格的影响]

## 四、技术指标
- **均线系统**: [分析MA、EMA等均线系统的信号]
- **动量指标**: [分析MACD、RSI等动量指标的状态]
- **波动率指标**: [分析布林带、ATR等波动率指标]

## 五、技术展望
- **短期技术预期**: [未来1-2周的技术面预期]
- **中期技术目标**: [未来1-3个月的技术目标位]

## 六、结论
[总结技术面的核心观点和交易建议]
"""
        
        from agents.ifind_agent import price_technical_analyst
        return Task(
            description=description,
            expected_output=expected_output,
            agent=price_technical_analyst,
            async_execution=False
        )
    
    # 量化策略任务
    elif task_type == 'quant_strategy':
        description = f"""
你是一位专业的量化分析师，专注于【{commodity}】。
请对{commodity}进行量化策略分析。

请严格按照以下步骤执行：
1. **获取量化策略数据**：使用 '获取EDB数据用于量化策略' 工具获取 {commodity} 从 {start_date} 到 {end_date} 的量化策略相关数据。
   - start_date: {start_date}
   - end_date: {end_date}

2. **执行分析**：基于获取到的数据，开发量化交易策略。

3. **撰写报告**：将分析结果整理成专业的量化策略报告。
"""
        
        expected_output = f"""
### **{commodity} 结构化策略设计方案**
**设计时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

#### **一、核心市场观点提炼**
[基于前面的分析报告，用1-2句话总结对{commodity}未来价格走势的核心判断]

#### **二、策略一：单边套期保值方案**
*   **适用场景**：[例如：下游企业担心未来{commodity}原料价格上涨，锁定采购成本。]
*   **策略结构**：
    *   **操作**：买入看涨期权 或 卖出看跌期权
    *   **标的**：{commodity}主力合约
    *   **期权类型**：[例如：看涨期权]
    *   **行权价 (K)**：[建议一个具体的行权价]
    *   **到期日**：[建议一个到期月份]
    *   **数量**：[例如：对应100吨现货的头寸]
    *   **权利金 (C)**：[估算一个权利金]

#### **三、策略二：成本优化方案**
*   **适用场景**：[例如：持有现货库存，希望通过期权降低仓储资金成本或增厚收益。]
*   **策略结构**：
    *   **操作**：备兑开仓 或 卖出看涨期权
    *   **标的**：{commodity}主力合约
    *   **期权类型**：[例如：看涨期权]
    *   **行权价 (K)**：[建议一个具体的行权价]
    *   **到期日**：[建议一个到期月份]
    *   **数量**：[例如：与持有的现货数量相等]
    *   **权利金收入 (C)**：[估算一个权利金收入]

#### **四、策略三：利润增厚方案**
*   **适用场景**：[例如：预期市场将温和上涨或盘整，希望在有限风险下获取额外收益。]
*   **策略结构**：
    *   **操作**：牛市价差 或 熊市价差
    *   **标的**：{commodity}主力合约
    *   **期权类型**：[例如：买入低行权价看涨期权 + 卖出高行权价看涨期权]
    *   **行权价组合 (K1, K2)**：[建议两个具体的行权价]
    *   **到期日**：[建议一个到期月份]
    *   **数量**：[例如：1:1配对]
    *   **净权利金**：[例如：净支出20元/吨]

#### **五、综合风险提示**
*   **模型风险**：[例如：策略基于历史数据，市场极端情况下可能失效。]
*   **流动性风险**：[例如：远月或虚值期权可能流动性不足，影响开平仓。]
*   **执行风险**：[例如：交易滑点和手续费对策略收益的影响。]
*   **希腊字母风险**：[简要提及Vega、Theta等风险]
"""
        
        from agents.ifind_agent import quant_strategist
        return Task(
            description=description,
            expected_output=expected_output,
            agent=quant_strategist,
            async_execution=False
        )
    
    # 交易执行任务
    elif task_type == 'trading':
        description = f"""
你是一位专业的交易执行专家，专注于【{commodity}】。
请对{commodity}制定交易执行计划。

请严格按照以下步骤执行：
1. **获取交易执行数据**：使用 '获取EDB数据用于交易执行' 工具获取 {commodity} 从 {start_date} 到 {end_date} 的交易执行相关数据。
   - start_date: {start_date}
   - end_date: {end_date}

2. **执行分析**：基于获取到的数据，制定具体的交易计划。

3. **撰写报告**：将分析结果整理成专业的交易执行报告。
"""
        
        expected_output = f"""
# {commodity} 交易执行计划

## 一、交易策略概述
- **策略类型**: [例如：趋势跟踪、均值回归、套利等]
- **交易方向**: [多头/空头/双向]
- **持仓周期**: [日内/短线/中线/长线]

## 二、入场条件
- **技术信号**: [具体的入场技术条件]
- **基本面确认**: [基本面的入场确认条件]
- **风险管理**: [入场时的风险控制措施]

## 三、出场条件
- **止盈条件**: [具体的止盈条件和目标]
- **止损条件**: [具体的止损条件和位置]
- **时间退出**: [时间相关的退出条件]

## 四、仓位管理
- **初始仓位**: [建议的初始仓位大小]
- **加仓策略**: [加仓的条件和方式]
- **减仓策略**: [减仓的条件和方式]

## 五、执行细节
- **交易时段**: [最佳的交易时段]
- **订单类型**: [建议的订单类型]
- **滑点控制**: [滑点控制的建议]

## 六、风险控制
- **最大回撤**: [可接受的最大回撤]
- **风险敞口**: [单笔交易的最大风险敞口]
- **应急措施**: [市场异常时的应急处理措施]
"""
        
        from agents.ifind_agent import trading_analyst
        return Task(
            description=description,
            expected_output=expected_output,
            agent=trading_analyst,
            async_execution=False
        )
    
    # 默认通用任务
    else:
        description = f"""
你是一位专业的{task_type}分析师，专注于【{commodity}】。
请对{commodity}进行{task_type}分析。

请严格按照以下步骤执行：
1. **获取数据**：使用相应的EDB数据工具获取 {commodity} 从 {start_date} 到 {end_date} 的相关数据。
2. **执行分析**：基于获取到的数据进行专业分析。
3. **撰写报告**：将分析结果整理成专业的报告。
"""
        
        expected_output = f"""
# {commodity} {task_type}分析报告

## 分析概述
[在此处填写分析概述]

## 详细分析
[在此处填写详细分析内容]

## 结论与建议
[在此处填写结论和建议]
"""
        
        # 根据任务类型选择对应的Agent
        agent_map = {
            'supply_demand': supply_demand_analyst,
            'apparent_demand': supply_demand_analyst,
            'demand_forecasting': supply_demand_analyst,
            'macro_economic': macro_analyst,
            'price_technical': price_technical_analyst,
            'quant_strategy': quant_strategist,
            'trading': trading_analyst,
            'basis': basis_analyst,
            'inventory': inventory_analyst
        }
        
        agent = agent_map.get(task_type, basis_analyst)
        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent,
            async_execution=False
        )
