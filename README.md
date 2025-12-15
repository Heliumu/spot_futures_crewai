spot_futures_crewai/
├── schemas/                     # 【核心】数据契约，所有项目共享
│   ├── __init__.py
│   └── models.py                # Pydantic V2 数据模型
│
├── agents/                      # 【智能】定义各个领域的专家Agent
│   ├── __init__.py
│   ├── basis_agent.py
│   ├── price_agent.py
│   ├── inventory_agent.py
│   ├── macro_agent.py
│   ├── fundamental_agent.py
│   ├── strategy_agent.py
│   └── summarizer_agent.py
│
├── tasks/                       # 【任务】定义每个Agent需要完成的具体任务
│   ├── __init__.py
│   ├── basis_analysis_task.py
│   ├── price_analysis_task.py
│   ├── ...
│   └── final_report_task.py
│
├── tools/                       # 【工具】Agent可以使用的工具，如数据获取
│   ├── __init__.py
│   └── data_fetching_tool.py
│
├── core/                        # 【配置】核心配置，如LLM统一接口
│   ├── __init__.py
│   └── llm_config.py
│
├── crews/                       # 【编排】将Agent和Task组装成工作流
│   ├── __init__.py
│   └── market_analysis_crew.py
│
├── main.py                      # 【入口】程序启动入口
├── requirements.txt             # 【依赖】项目依赖
└── README.md                    # 【文档】项目说明




由于tools目录下的zhipu_web_search_tool.py文件和.env文件不在同一目录下 load_dotenv() 无法加载到环境变量
暂时搁置这个问题 直接将api_key写在zhipu_web_search_tool.py文件中
