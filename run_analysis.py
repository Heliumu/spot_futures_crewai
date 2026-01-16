# run_debug_analysis.py
from config.logging_config import setup_logging
from main.analysis_workflow import AnalysisWorkflow

def main():
    """主函数 - 调试模式"""
    # 设置日志
    setup_logging()
    
    workflow = AnalysisWorkflow()
    
    # 获取用户输入
    user_input = input("请输入您的分析需求: ")
    if not user_input.strip():
        user_input = "沥青 半年库存分析"
    
    result = workflow.execute_analysis(user_input)
    
    print("\n" + "="*50)
    print("分析结果:")
    print(result)
    
    print("\n" + "="*50)
    print("详细数据日志已保存到 logs/ 目录")
    print("您可以查看日志文件了解完整的数据获取过程")

if __name__ == "__main__":
    main()
